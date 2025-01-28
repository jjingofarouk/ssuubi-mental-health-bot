# services/message_analyzer.py
import re
from typing import Dict, Tuple
from .intents import MessageIntent
from .patterns import get_patterns

class MessageAnalyzer:
    def __init__(self):
        self.patterns = get_patterns()

    def analyze_message(self, message: str) -> Tuple[MessageIntent, Dict]:
        for pattern in self.patterns:
            for regex in pattern.patterns:
                if regex.search(message):
                    return pattern.intent, self._extract_details(message, pattern.intent)
        return MessageIntent.UNKNOWN, {}

    def _extract_details(self, message: str, intent: MessageIntent) -> Dict:
        details = {}

        if intent == MessageIntent.ANXIETY:
            intensity_words = re.findall(r'(very|really|so|extremely|incredibly)\s*anxious', message, re.IGNORECASE)
            details["intensity"] = len(intensity_words)

            time_match = re.search(r'(today|lately|recently|for\s*(a\s*)?while)', message, re.IGNORECASE)
            if time_match:
                details["timeframe"] = time_match.group(1)

        return details