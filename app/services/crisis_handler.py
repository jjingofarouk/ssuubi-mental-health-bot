import re
from typing import Dict

class CrisisHandler:
    def __init__(self):
        self.crisis_patterns = [
            re.compile(r'suicid(?:e|al)', re.IGNORECASE),
            re.compile(r'kill\s*my\s*self', re.IGNORECASE),
            re.compile(r'want\s*to\s*die', re.IGNORECASE),
            re.compile(r'end\s*(?:it\s*all|my\s*life)', re.IGNORECASE),
            re.compile(r'don\'t\s*want\s*to\s*live', re.IGNORECASE),
            re.compile(r'feel\s*like\s*giving\s*up', re.IGNORECASE),
            re.compile(r'no\s*reason\s*to\s*go\s*on', re.IGNORECASE),
        ]

    def is_crisis_message(self, message: str, sentiment_result: Dict = None) -> bool:
        if any(pattern.search(message) for pattern in self.crisis_patterns):
            return True
        if sentiment_result and 'crisis' in sentiment_result.get('themes', []):
            return True
        return False

    def generate_crisis_response(self, context: Dict = None) -> str:
        location = context.get('user_location', 'US') if context else 'US'
        resources = {
            'US': "Call 988 or text HOME to 741741",
            'UK': "Call 116 123 or text SHOUT to 85258",
            # Add more regions
        }
        base_response = (
            f"I’m deeply concerned about you. Your life matters, and help is available.\n\n"
            f"Please reach out now: {resources.get(location, resources['US'])}.\n"
            f"Emergency: {911 if location == 'US' else 999}\n\n"
            "Would you like me to stay with you and talk?"
        )
        return base_response