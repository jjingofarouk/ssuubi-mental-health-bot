import re
from typing import Dict, Tuple
from .intents import MessageIntent
from .patterns import get_patterns
from transformers import pipeline  # For NLP-based intent detection
import time

class MessageAnalyzer:
    def __init__(self):
        self.patterns = get_patterns()
        # Initialize NLP classifier (lightweight zero-shot model)
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        # Store user conversation history (in-memory for now)
        self.user_history = {}  # {user_id: [(message, intent, timestamp)]}

    def analyze_message(self, message: str, context: Dict = None) -> Tuple[MessageIntent, Dict]:
        """
        Analyze a message to determine intent and extract details.
        Args:
            message: User input string.
            context: Optional dict with user_id, preferences, etc.
        Returns:
            Tuple of (MessageIntent, details dict).
        """
        context = context or {}
        user_id = context.get('user_id', 'default')

        # Step 1: Try regex-based intent detection
        for pattern in self.patterns:
            for regex in pattern.patterns:
                if regex.search(message):
                    details = self._extract_details(message, pattern.intent)
                    self._update_history(user_id, message, pattern.intent)
                    return pattern.intent, details

        # Step 2: Fallback to NLP-based intent detection
        intent = self._detect_intent_nlp(message)
        details = self._extract_details(message, intent)
        self._update_history(user_id, message, intent)
        return intent, details

    def _detect_intent_nlp(self, message: str) -> MessageIntent:
        """
        Use NLP to classify message intent when regex fails.
        """
        candidate_labels = [intent.value for intent in MessageIntent]
        result = self.classifier(message, candidate_labels, multi_label=False)
        try:
            return MessageIntent(result['labels'][0])
        except ValueError:
            return MessageIntent.UNKNOWN

    def _extract_details(self, message: str, intent: MessageIntent) -> Dict:
        """
        Extract contextual details based on intent.
        """
        details = {}

        if intent == MessageIntent.ANXIETY:
            # Expanded intensity words
            intensity_words = re.findall(
                r'(very|really|so|extremely|incredibly|terribly|awfully|highly|severely|'
                r'tremendously|unbearably|overwhelmingly|desperately|profoundly)\s*(anxious|nervous|worried)',
                message, re.IGNORECASE
            )
            details["intensity"] = len(intensity_words)
            details["intensity_words"] = [word[0] for word in intensity_words]  # Store specific words

            # Expanded timeframe matches
            time_match = re.search(
                r'(today|lately|recently|for\s*(a\s*)?(while|week|month|year)|'
                r'yesterday|this\s*(week|month)|always|constantly|ongoing|since\s*\w+)',
                message, re.IGNORECASE
            )
            details["timeframe"] = time_match.group(0) if time_match else None

            # Extract triggers (e.g., "about work", "because of family")
            trigger_match = re.search(r'(about|because\s*of|due\s*to)\s*([\w\s]+)', message, re.IGNORECASE)
            details["trigger"] = trigger_match.group(2).strip() if trigger_match else None

        elif intent == MessageIntent.DEPRESSION:
            # Intensity for sadness
            intensity_words = re.findall(
                r'(very|really|so|extremely|incredibly|terribly|awfully|deeply|'
                r'profoundly|hopelessly)\s*(depressed|sad|down|hopeless)',
                message, re.IGNORECASE
            )
            details["intensity"] = len(intensity_words)
            details["intensity_words"] = [word[0] for word in intensity_words]

            # Timeframe
            time_match = re.search(
                r'(today|lately|recently|for\s*(a\s*)?(while|week|month|year)|'
                r'yesterday|this\s*(week|month)|always|constantly|ongoing|since\s*\w+)',
                message, re.IGNORECASE
            )
            details["timeframe"] = time_match.group(0) if time_match else None

            # Symptoms (e.g., "can't sleep", "no energy")
            symptom_match = re.search(
                r'(can\'t\s*(sleep|eat|focus)|no\s*(energy|motivation)|feel\s*empty)',
                message, re.IGNORECASE
            )
            details["symptom"] = symptom_match.group(0) if symptom_match else None

        elif intent == MessageIntent.STRESS:
            # Intensity for stress
            intensity_words = re.findall(
                r'(very|really|so|extremely|incredibly|terribly|awfully|overwhelmingly)\s*(stressed|overwhelmed)',
                message, re.IGNORECASE
            )
            details["intensity"] = len(intensity_words)
            details["intensity_words"] = [word[0] for word in intensity_words]

            # Timeframe
            time_match = re.search(
                r'(today|lately|recently|for\s*(a\s*)?(while|week|month|year)|'
                r'yesterday|this\s*(week|month)|always|constantly|ongoing|since\s*\w+)',
                message, re.IGNORECASE
            )
            details["timeframe"] = time_match.group(0) if time_match else None

            # Source of stress
            source_match = re.search(r'(at\s*(work|school)|from\s*([\w\s]+))', message, re.IGNORECASE)
            details["source"] = source_match.group(0) if source_match else None

        elif intent == MessageIntent.CRISIS:
            # Urgency indicators
            urgency_words = re.findall(
                r'(immediately|now|urgent|can\'t\s*go\s*on|desperate|help\s*me)',
                message, re.IGNORECASE
            )
            details["urgency"] = len(urgency_words)
            details["urgency_words"] = urgency_words

            # Specific crisis type
            crisis_match = re.search(
                r'(suicid(e|al)|harm\s*myself|end\s*it|kill\s*myself|want\s*to\s*die)',
                message, re.IGNORECASE
            )
            details["crisis_type"] = crisis_match.group(0) if crisis_match else None

        elif intent == MessageIntent.GREETING:
            # Greeting tone
            tone_match = re.search(r'(hi|hello|hey|yo)\s*(buddy|friend|mate)?', message, re.IGNORECASE)
            details["tone"] = tone_match.group(1) if tone_match else "neutral"
            details["friendly"] = bool(tone_match and tone_match.group(2))

        return details

    def _update_history(self, user_id: str, message: str, intent: MessageIntent):
        """
        Update user conversation history for context-aware analysis.
        """
        self.user_history.setdefault(user_id, []).append((message, intent, time.time()))
        # Keep only the last 10 messages to manage memory
        self.user_history[user_id] = self.user_history[user_id][-10:]

    def get_user_context(self, user_id: str) -> Dict:
        """
        Retrieve user context based on recent messages.
        """
        history = self.user_history.get(user_id, [])
        recent_intents = [entry[1] for entry in history]
        return {
            "recent_intents": recent_intents,
            "last_intent": recent_intents[-1] if recent_intents else None,
            "message_count": len(history)
        }