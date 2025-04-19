from typing import Dict, Tuple, List
import re
import time
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from .intents import MessageIntent
from .patterns import get_patterns

class MessageAnalyzer:
    def __init__(self):
        self.patterns = get_patterns()
        # Set clean_up_tokenization_spaces=False to preserve spaces
        self.classifier = pipeline(
            "zero-shot-classification",
            model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
            tokenizer_kwargs={"clean_up_tokenization_spaces": False}
        )
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.user_history = {}  # {user_id: [(message, intent, timestamp)]}
        self.intent_theme_map = {
            'anxiety': MessageIntent.ANXIETY,
            'depression': MessageIntent.DEPRESSION,
            'grief': MessageIntent.GRIEF,
            'loneliness': MessageIntent.LONELINESS,
            'stress': MessageIntent.STRESS,
            'crisis': MessageIntent.CRISIS,
            'relationships': MessageIntent.RELATIONSHIP,
            'sleep': MessageIntent.SLEEP,
            'anger': MessageIntent.ANGER,
            'self_care': MessageIntent.SELF_CARE,
            'motivation': MessageIntent.MOTIVATION,
            'work_stress': MessageIntent.WORK_STRESS,
            'family': MessageIntent.FAMILY,
            'trauma': MessageIntent.TRAUMA,
            'self_esteem': MessageIntent.SELF_ESTEEM
        }

    def analyze_message(self, message: str, context: Dict = None) -> Tuple[MessageIntent, Dict]:
        """Analyze message to determine intent and extract details."""
        context = context or {}
        user_id = context.get('user_id', 'default')
        sentiment_result = context.get('sentiment_analysis', {})

        for pattern in self.patterns:
            for regex in pattern.patterns:
                if regex.search(message):
                    details = self._extract_details(message, pattern.intent, sentiment_result)
                    self._update_history(user_id, message, pattern.intent)
                    return pattern.intent, details

        intent = self._detect_intent_nlp(message, sentiment_result.get('themes', []))
        details = self._extract_details(message, intent, sentiment_result)
        self._update_history(user_id, message, intent)
        return intent, details

    def _detect_intent_nlp(self, message: str, themes: List[str]) -> MessageIntent:
        """Use NLP to classify intent, refined by sentiment themes."""
        candidate_labels = [intent.value for intent in MessageIntent]
        result = self.classifier(message, candidate_labels, multi_label=False)
        top_intent = result['labels'][0]

        for theme in themes:
            if theme in self.intent_theme_map and self.intent_theme_map[theme].value in candidate_labels:
                return self.intent_theme_map[theme]

        message_embedding = self.embedding_model.encode(message, convert_to_tensor=True)
        max_similarity = 0
        best_intent = MessageIntent.UNKNOWN
        for intent in MessageIntent:
            if intent == MessageIntent.UNKNOWN:
                continue
            pattern = next((p for p in self.patterns if p.intent == intent), None)
            if pattern:
                pattern_texts = [str(r) for r in pattern.responses]
                pattern_embeddings = self.embedding_model.encode(pattern_texts, convert_to_tensor=True)
                similarity = util.cos_sim(message_embedding, pattern_embeddings).max().item()
                if similarity > max_similarity and similarity > 0.5:
                    max_similarity = similarity
                    best_intent = intent

        try:
            return best_intent if best_intent != MessageIntent.UNKNOWN else MessageIntent(top_intent)
        except ValueError:
            return MessageIntent.UNKNOWN

    def _extract_details(self, message: str, intent: MessageIntent, sentiment_result: Dict) -> Dict:
        """Extract contextual details based on intent and sentiment."""
        details = {
            'themes': sentiment_result.get('themes', []),
            'intensity': sentiment_result.get('emotion_intensity', 0),
            'sentiment_trend': sentiment_result.get('context', {}).get('sentiment_trend', 'neutral')
        }

        if intent == MessageIntent.ANXIETY:
            intensity_words = re.findall(
                r'(very|really|so|extremely|incredibly|terribly|awfully|highly|severely|'
                r'tremendously|unbearably|overwhelmingly|desperately|profoundly)\s*(anxious|nervous|worried)',
                message, re.IGNORECASE
            )
            details['intensity'] += len(intensity_words)
            details['intensity_words'] = [word[0] for word in intensity_words]
            time_match = re.search(
                r'(today|lately|recently|for\s*(a\s*)?(while|week|month|year)|'
                r'yesterday|this\s*(week|month)|always|constantly|ongoing|since\s*\w+)',
                message, re.IGNORECASE
            )
            details['timeframe'] = time_match.group(0) if time_match else None
            trigger_match = re.search(r'(about|because\s*of|due\s*to)\s*([\w\s]+)', message, re.IGNORECASE)
            details['trigger'] = trigger_match.group(2).strip() if trigger_match else None

        elif intent == MessageIntent.DEPRESSION:
            intensity_words = re.findall(
                r'(very|really|so|extremely|incredibly|terribly|awfully|deeply|'
                r'profoundly|hopelessly)\s*(depressed|sad|down|hopeless)',
                message, re.IGNORECASE
            )
            details['intensity'] += len(intensity_words)
            details['intensity_words'] = [word[0] for word in intensity_words]
            time_match = re.search(
                r'(today|lately|recently|for\s*(a\s*)?(while|week|month|year)|'
                r'yesterday|this\s*(week|month)|always|constantly|ongoing|since\s*\w+)',
                message, re.IGNORECASE
            )
            details['timeframe'] = time_match.group(0) if time_match else None
            symptom_match = re.search(
                r'(can\'t\s*(sleep|eat|focus)|no\s*(energy|motivation)|feel\s*empty)',
                message, re.IGNORECASE
            )
            details['symptom'] = symptom_match.group(0) if symptom_match else None

        elif intent == MessageIntent.RELATIONSHIP:
            intensity_words = re.findall(
                r'(very|really|so|extremely|incredibly)\s*(hurt|betrayed|upset)',
                message, re.IGNORECASE
            )
            details['intensity'] += len(intensity_words)
            details['intensity_words'] = [word[0] for word in intensity_words]
            relationship_type = re.search(r'(partner|friend|family|spouse)', message, re.IGNORECASE)
            details['relationship_type'] = relationship_type.group(0) if relationship_type else None
            conflict_match = re.search(r'(fight|conflict|argument)\s*with\s*([\w\s]+)', message, re.IGNORECASE)
            details['conflict'] = conflict_match.group(2).strip() if conflict_match else None

        elif intent == MessageIntent.GRIEF:
            intensity_words = re.findall(
                r'(very|really|so|extremely|incredibly|terribly)\s*(heartbroken|sorrowful|devastated)',
                message, re.IGNORECASE
            )
            details['intensity'] += len(intensity_words)
            details['intensity_words'] = [word[0] for word in intensity_words]
            loss_match = re.search(r'loss\s*of\s*([\w\s]+)', message, re.IGNORECASE)
            details['loss_type'] = loss_match.group(1).strip() if loss_match else None

        elif intent == MessageIntent.SLEEP:
            intensity_words = re.findall(
                r'(very|really|so|extremely|incredibly)\s*(tired|exhausted)',
                message, re.IGNORECASE
            )
            details['intensity'] += len(intensity_words)
            details['intensity_words'] = [word[0] for word in intensity_words]
            sleep_issue = re.search(r'(can\'t\s*sleep|insomnia|up\s*all\s*night|trouble\s*(falling|staying)\s*asleep)', message, re.IGNORECASE)
            details['sleep_issue'] = sleep_issue.group(0) if sleep_issue else None

        elif intent == MessageIntent.CRISIS:
            urgency_words = re.findall(
                r'(immediately|now|urgent|can\'t\s*go\s*on|desperate|help\s*me)',
                message, re.IGNORECASE
            )
            details['urgency'] = len(urgency_words)
            details['urgency_words'] = urgency_words
            crisis_match = re.search(
                r'(suicid(e|al)|harm\s*myself|end\s*it|kill\s*myself|want\s*to\s*die)',
                message, re.IGNORECASE
            )
            details['crisis_type'] = crisis_match.group(0) if crisis_match else None

        elif intent == MessageIntent.GREETING:
            tone_match = re.search(r'(hi|hello|hey|yo)\s*(buddy|friend|mate)?', message, re.IGNORECASE)
            details['tone'] = tone_match.group(1) if tone_match else 'neutral'
            details['friendly'] = bool(tone_match and tone_match.group(2))

        elif intent == MessageIntent.FAREWELL:
            tone_match = re.search(r'(bye|goodbye|see\s*you|later)', message, re.IGNORECASE)
            details['tone'] = tone_match.group(1) if tone_match else 'neutral'

        elif intent == MessageIntent.GRATITUDE:
            gratitude_match = re.search(r'(thank\s*(you|s)|appreciate|grateful)', message, re.IGNORECASE)
            details['expression'] = gratitude_match.group(0) if gratitude_match else None

        elif intent == MessageIntent.STRESS:
            intensity_words = re.findall(
                r'(very|really|so|extremely|incredibly)\s*(stressed|overwhelmed|pressured)',
                message, re.IGNORECASE
            )
            details['intensity'] += len(intensity_words)
            details['intensity_words'] = [word[0] for word in intensity_words]
            source_match = re.search(r'(work|school|family|life)', message, re.IGNORECASE)
            details['source'] = source_match.group(0) if source_match else None

        elif intent == MessageIntent.LONELINESS:
            intensity_words = re.findall(
                r'(very|really|so|extremely|incredibly)\s*(lonely|alone|isolated)',
                message, re.IGNORECASE
            )
            details['intensity'] += len(intensity_words)
            details['intensity_words'] = [word[0] for word in intensity_words]
            context_match = re.search(r'(no\s*one|nobody|without\s*anyone)', message, re.IGNORECASE)
            details['context'] = context_match.group(0) if context_match else None

        elif intent == MessageIntent.ANGER:
            intensity_words = re.findall(
                r'(very|really|so|extremely|incredibly)\s*(angry|mad|furious)',
                message, re.IGNORECASE
            )
            details['intensity'] += len(intensity_words)
            details['intensity_words'] = [word[0] for word in intensity_words]
            cause_match = re.search(r'(because\s*of|at\s*([\w\s]+))', message, re.IGNORECASE)
            details['cause'] = cause_match.group(2).strip() if cause_match and cause_match.group(2) else None

        elif intent == MessageIntent.SELF_CARE:
            activity_match = re.search(r'(meditat(e|ion)|exercise|relax|self\s*care)', message, re.IGNORECASE)
            details['activity'] = activity_match.group(0) if activity_match else None

        elif intent == MessageIntent.MOTIVATION:
            goal_match = re.search(r'(want\s*to|trying\s*to)\s*([\w\s]+)', message, re.IGNORECASE)
            details['goal'] = goal_match.group(2).strip() if goal_match else None

        elif intent == MessageIntent.WORK_STRESS:
            intensity_words = re.findall(
                r'(very|really|so|extremely|incredibly)\s*(stressed|overwhelmed)',
                message, re.IGNORECASE
            )
            details['intensity'] += len(intensity_words)
            details['intensity_words'] = [word[0] for word in intensity_words]
            work_issue = re.search(r'(job|work|boss|deadline|project)', message, re.IGNORECASE)
            details['work_issue'] = work_issue.group(0) if work_issue else None

        elif intent == MessageIntent.FAMILY:
            intensity_words = re.findall(
                r'(very|really|so|extremely|incredibly)\s*(upset|stressed|worried)',
                message, re.IGNORECASE
            )
            details['intensity'] += len(intensity_words)
            details['intensity_words'] = [word[0] for word in intensity_words]
            family_issue = re.search(r'(parent|sibling|child|family)\s*([\w\s]+)', message, re.IGNORECASE)
            details['family_issue'] = family_issue.group(2).strip() if family_issue else None

        elif intent == MessageIntent.TRAUMA:
            intensity_words = re.findall(
                r'(very|really|so|extremely|incredibly)\s*(scared|haunted|traumatized)',
                message, re.IGNORECASE
            )
            details['intensity'] += len(intensity_words)
            details['intensity_words'] = [word[0] for word in intensity_words]
            event_match = re.search(r'(past|trauma|event)\s*([\w\s]+)', message, re.IGNORECASE)
            details['event'] = event_match.group(2).strip() if event_match else None

        elif intent == MessageIntent.SELF_ESTEEM:
            intensity_words = re.findall(
                r'(very|really|so|extremely|incredibly)\s*(worthless|insecure|low)',
                message, re.IGNORECASE
            )
            details['intensity'] += len(intensity_words)
            details['intensity_words'] = [word[0] for word in intensity_words]
            feeling_match = re.search(r'(feel\s*like|think\s*i\'m)\s*([\w\s]+)', message, re.IGNORECASE)
            details['feeling'] = feeling_match.group(2).strip() if feeling_match else None

        return details

    def _update_history(self, user_id: str, message: str, intent: MessageIntent):
        """Update user conversation history."""
        self.user_history.setdefault(user_id, []).append((message, intent, time.time()))
        self.user_history[user_id] = self.user_history[user_id][-10:]

    def get_user_context(self, user_id: str) -> Dict:
        """Retrieve user context based on recent messages."""
        history = self.user_history.get(user_id, [])
        recent_intents = [entry[1] for entry in history]
        return {
            'recent_intents': recent_intents,
            'last_intent': recent_intents[-1] if recent_intents else None,
            'message_count': len(history)
        }