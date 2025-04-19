from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from typing import Dict, Tuple
from .intents import MessageIntent
from .patterns import get_patterns
import time

class MessageAnalyzer:
    def __init__(self):
        self.patterns = get_patterns()
        self.classifier = pipeline("zero-shot-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # For theme similarity
        self.user_history = {}

    def analyze_message(self, message: str, context: Dict = None) -> Tuple[MessageIntent, Dict]:
        context = context or {}
        user_id = context.get('user_id', 'default')
        sentiment_result = context.get('sentiment_analysis', {})

        # Combine regex and theme-based intent detection
        for pattern in self.patterns:
            for regex in pattern.patterns:
                if regex.search(message):
                    details = self._extract_details(message, pattern.intent, sentiment_result)
                    self._update_history(user_id, message, pattern.intent)
                    return pattern.intent, details

        # NLP fallback with theme influence
        intent = self._detect_intent_nlp(message, sentiment_result.get('themes', []))
        details = self._extract_details(message, intent, sentiment_result)
        self._update_history(user_id, message, intent)
        return intent, details

    def _detect_intent_nlp(self, message: str, themes: List[str]) -> MessageIntent:
        candidate_labels = [intent.value for intent in MessageIntent]
        result = self.classifier(message, candidate_labels, multi_label=False)
        top_intent = result['labels'][0]
        # Boost intent based on themes
        theme_intent_map = {
            'anxiety': MessageIntent.ANXIETY,
            'depression': MessageIntent.DEPRESSION,
            'grief': MessageIntent.GRIEF,
            'loneliness': MessageIntent.LONELINESS,
            # Add mappings for all themes
        }
        for theme in themes:
            if theme in theme_intent_map and theme_intent_map[theme].value in candidate_labels:
                return theme_intent_map[theme]
        try:
            return MessageIntent(top_intent)
        except ValueError:
            return MessageIntent.UNKNOWN

    def _extract_details(self, message: str, intent: MessageIntent, sentiment_result: Dict) -> Dict:
        details = {'themes': sentiment_result.get('themes', [])}

        if intent == MessageIntent.ANXIETY:
            # Existing logic
            intensity_words = re.findall(
                r'(very|really|so|extremely|incredibly|terribly|awfully|highly|severely|'
                r'tremendously|unbearably|overwhelmingly|desperately|profoundly)\s*(anxious|nervous|worried)',
                message, re.IGNORECASE
            )
            details["intensity"] = len(intensity_words) + sentiment_result.get('emotion_intensity', 0)
            details["intensity_words"] = [word[0] for word in intensity_words]
            time_match = re.search(
                r'(today|lately|recently|for\s*(a\s*)?(while|week|month|year)|'
                r'yesterday|this\s*(week|month)|always|constantly|ongoing|since\s*\w+)',
                message, re.IGNORECASE
            )
            details["timeframe"] = time_match.group(0) if time_match else None
            trigger_match = re.search(r'(about|because\s*of|due\s*to)\s*([\w\s]+)', message, re.IGNORECASE)
            details["trigger"] = trigger_match.group(2).strip() if trigger_match else None

        elif intent == MessageIntent.RELATIONSHIP:
            intensity_words = re.findall(
                r'(very|really|so|extremely|incredibly)\s*(hurt|betrayed|upset)',
                message, re.IGNORECASE
            )
            details["intensity"] = len(intensity_words) + sentiment_result.get('emotion_intensity', 0)
            details["intensity_words"] = [word[0] for word in intensity_words]
            relationship_type = re.search(r'(partner|friend|family|spouse)', message, re.IGNORECASE)
            details["relationship_type"] = relationship_type.group(0) if relationship_type else None

        # Add similar logic for GRIEF, SLEEP, MOTIVATION, etc.

        return details