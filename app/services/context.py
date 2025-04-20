from typing import Dict, Set, Optional
import logging
import pymongo
from pymongo.errors import ServerSelectionTimeoutError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConversationContext:
    def __init__(self):
        self.in_memory = False
        try:
            # Attempt to connect to MongoDB (replace with your MongoDB URI if using Atlas)
            self.client = pymongo.MongoClient(
                "mongodb://localhost:27017/",
                serverSelectionTimeoutMS=5000
            )
            # Test connection
            self.client.server_info()
            self.db = self.client["ssuubi_db"]
            self.context_collection = self.db["context"]
            logger.info("Connected to MongoDB")
        except (ServerSelectionTimeoutError, Exception) as e:
            logger.warning(f"MongoDB connection failed: {str(e)}. Using in-memory storage.")
            self.in_memory = True
            self.context_store: Dict[str, Dict] = {}

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
        """Update user context in MongoDB or in-memory store."""
        context = {
            "user_id": user_id,
            "intent": intent,
            "interaction_count": interaction_count,
            "identified_themes": list(identified_themes or set()),
            "crisis_mode": crisis_mode,
            "details": details or {},
            "preferences": preferences or {},
            "emotional_state": emotional_state or "validation",
            "last_updated": pymongo.datetime.datetime.utcnow()
        }
        try:
            if self.in_memory:
                self.context_store[user_id] = context
            else:
                self.context_collection.update_one(
                    {"user_id": user_id},
                    {"$set": context},
                    upsert=True
                )
            logger.debug(f"Updated context for user {user_id}")
        except Exception as e:
            logger.error(f"Failed to update context for user {user_id}: {str(e)}")

    def get_context(self, user_id: str) -> Dict:
        """Retrieve user context from MongoDB or in-memory store."""
        try:
            if self.in_memory:
                return self.context_store.get(user_id, {
                    "user_id": user_id,
                    "intent": None,
                    "interaction_count": 0,
                    "identified_themes": [],
                    "crisis_mode": False,
                    "details": {},
                    "preferences": {"preferred_technique": "breathing"},
                    "emotional_state": "validation"
                })
            context = self.context_collection.find_one({"user_id": user_id})
            if context:
                context["identified_themes"] = set(context["identified_themes"])
                return context
            return {
                "user_id": user_id,
                "intent": None,
                "interaction_count": 0,
                "identified_themes": set(),
                "crisis_mode": False,
                "details": {},
                "preferences": {"preferred_technique": "breathing"},
                "emotional_state": "validation"
            }
        except Exception as e:
            logger.error(f"Failed to retrieve context for user {user_id}: {str(e)}")
            return {
                "user_id": user_id,
                "intent": None,
                "interaction_count": 0,
                "identified_themes": set(),
                "crisis_mode": False,
                "details": {},
                "preferences": {"preferred_technique": "breathing"},
                "emotional_state": "validation"
            }