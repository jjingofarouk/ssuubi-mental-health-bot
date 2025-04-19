from typing import Dict, Set
from pymongo import MongoClient

class ConversationContext:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['ssuubi']
        self.context_collection = self.db['context']

    def update_context(self, user_id: str, intent: str, interaction_count: int, identified_themes: Set[str], crisis_mode: bool, details: Dict, preferences: Dict):
        context = {
            'user_id': user_id,
            'previous_intent': intent,
            'interaction_count': interaction_count,
            'identified_themes': list(identified_themes),
            'crisis_mode': crisis_mode,
            'details': details,
            'preferences': preferences,
            'emotional_state': 'validation',  # Start with validation
            'last_updated': datetime.utcnow()
        }
        self.context_collection.update_one(
            {'user_id': user_id},
            {'$set': context},
            upsert=True
        )

    def get_context(self, user_id: str) -> Dict:
        context = self.context_collection.find_one({'user_id': user_id})
        return context or {
            'previous_intent': None,
            'interaction_count': 0,
            'identified_themes': set(),
            'crisis_mode': False,
            'details': {},
            'preferences': {},
            'emotional_state': 'validation'
        }