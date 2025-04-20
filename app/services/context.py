from typing import Dict, Set, Optional
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConversationContext:
    def __init__(self):
        self.in_memory = True
        self.context_store: Dict[str, Dict] = {}
        logger.info("Initialized in-memory context storage")

    def update_context(
        self,
        user_id: str,
        intent: Optional[str] = None,
        interaction_count: int = 0,
        identified_themes: Optional[Set[str]] = None,
        crisis_mode: bool = False,
        details: Optional[Dict] = None,
        preferences: Optional[Dict] = None,
        emotional_state: Optional[str] = None
    ) -> None:
        """Update user context in in-memory store."""
        context = {
            "user_id": user_id,
            "intent": intent,
            "interaction_count": interaction_count,
            "identified_themes": list(identified_themes or set()),
            "crisis_mode": crisis_mode,
            "details": details or {},
            "preferences": preferences or {},
            "emotional_state": emotional_state or "validation",
            "previous_intent": intent,  # Store intent as previous_intent
            "last_updated": datetime.utcnow().isoformat()
        }
        try:
            self.context_store[user_id] = context
            logger.debug(f"Updated context for user {user_id}")
        except Exception as e:
            logger.error(f"Failed to update context for user {user_id}: {str(e)}")

    def get_context(self, user_id: str) -> Dict:
        """Retrieve user context from in-memory store."""
        try:
            return self.context_store.get(user_id, {
                "user_id": user_id,
                "intent": None,
                "interaction_count": 0,
                "identified_themes": [],
                "crisis_mode": False,
                "details": {},
                "preferences": {"preferred_technique": "breathing"},
                "emotional_state": "validation",
                "previous_intent": None,
                "last_updated": datetime.utcnow().isoformat()
            })
        except Exception as e:
            logger.error(f"Failed to retrieve context for user {user_id}: {str(e)}")
            return {
                "user_id": user_id,
                "intent": None,
                "interaction_count": 0,
                "identified_themes": [],
                "crisis_mode": False,
                "details": {},
                "preferences": {"preferred_technique": "breathing"},
                "emotional_state": "validation",
                "previous_intent": None,
                "last_updated": datetime.utcnow().isoformat()
            }