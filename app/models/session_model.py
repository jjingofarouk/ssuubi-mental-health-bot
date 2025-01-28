from datetime import datetime

class Session:
    def __init__(self, session_id):
        self.session_id = session_id
        self.context = {
            'user_name': None,
            'mood_history': [],
            'risk_level': 'low',
            'topics_discussed': set(),
            'coping_strategies_suggested': set(),
            'last_interaction': datetime.now(),
            'session_duration': 0
        }
        self.conversation_history = []
    
    def update_conversation_history(self, user_message, bot_message):
        self.conversation_history.append({
            'user': user_message,
            'bot': bot_message,
            'timestamp': datetime.now().isoformat()
        })