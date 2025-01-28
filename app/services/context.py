# services/context.py
from typing import Dict, Set

class ConversationContext:
    def __init__(self):
        self.context: Dict = {
            "previous_intent": None,
            "interaction_count": 0,
            "identified_themes": set(),
            "crisis_mode": False
        }

    def update_context(self, intent: str, interaction_count: int, identified_themes: Set[str], crisis_mode: bool):
        self.context["previous_intent"] = intent
        self.context["interaction_count"] = interaction_count
        self.context["identified_themes"] = identified_themes
        self.context["crisis_mode"] = crisis_mode

    def get_context(self) -> Dict:
        return self.context