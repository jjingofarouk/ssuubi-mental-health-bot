# services/crisis_handler.py
import re

class CrisisHandler:
    def __init__(self):
        self.crisis_patterns = [
            re.compile(r'suicid(?:e|al)', re.IGNORECASE),
            re.compile(r'kill\s*my\s*self', re.IGNORECASE),
            re.compile(r'want\s*to\s*die', re.IGNORECASE),
            re.compile(r'end\s*(?:it\s*all|my\s*life)', re.IGNORECASE)
        ]

    def is_crisis_message(self, message: str) -> bool:
        return any(pattern.search(message) for pattern in self.crisis_patterns)

    def generate_crisis_response(self) -> str:
        return (
            "I'm very concerned about what you're saying. Your life has value and there are "
            "people who want to help. Please reach out to a crisis counselor right now:\n\n"
            "Crisis Line: 1-800-273-8255\n"
            "Crisis Text: Text HOME to 741741\n"
            "Emergency: 911"
        )