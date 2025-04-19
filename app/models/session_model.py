from datetime import datetime
from typing import List, Dict, Set

class Session:
    def __init__(self, session_id: str, user_id: str):
        """Initialize a session with a unique ID and user ID."""
        self.session_id = session_id
        self.user_id = user_id
        self.context = {
            'user_name': None,
            'user_id': user_id,  # Store user_id for context
            'mood_history': [],
            'risk_level': 'low',
            'topics_discussed': set(),
            'coping_strategies_suggested': set(),
            'last_interaction': datetime.now(),
            'session_duration': 0
        }
        self.conversation_history: List[Dict] = []

    def update_conversation_history(self, user_message: str, bot_message: str) -> None:
        """Add a user-bot message pair to the conversation history."""
        self.conversation_history.append({
            'user': user_message,
            'bot': bot_message,
            'timestamp': datetime.now().isoformat()
        })

    def get_history(self) -> List[Dict]:
        """Return the conversation history."""
        return self.conversation_history