# services/response_generator.py
import random
from typing import Dict, List
from .intents import MessageIntent
from .patterns import get_patterns

class ResponseGenerator:
    def __init__(self):
        self.patterns = get_patterns()

    def generate_response(self, intent: MessageIntent, context: Dict) -> str:
        pattern = next((p for p in self.patterns if p.intent == intent), None)

        if pattern:
            response_data = random.choice(pattern.responses)

            if isinstance(response_data, dict):
                response = response_data["message"]
                if response_data.get("techniques"):
                    response += "\n\nHere are some techniques that might help:\n"
                    response += "\n".join(f"- {t}" for t in response_data["techniques"])
                if response_data.get("followup"):
                    response += f"\n\n{response_data['followup']}"
            else:
                response = response_data
        else:
            response = self._generate_fallback_response()

        return response

    def _generate_fallback_response(self) -> str:
        fallbacks = [
            "I'm here to listen. Can you tell me more about what you're experiencing?",
            "That sounds difficult. Would you like to explore these feelings further?",
            "Thank you for sharing that with me. How can I best support you right now?"
        ]
        return random.choice(fallbacks)