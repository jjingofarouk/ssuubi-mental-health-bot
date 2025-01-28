from datetime import datetime
from app.models.session_model import Session

class ConversationManager:
    def __init__(self):
        self.sessions = {}
    
    def create_session(self, session_id):
        self.sessions[session_id] = Session(session_id)
    
    def update_conversation_history(self, session_id, user_message, bot_message):
        if session_id in self.sessions:
            self.sessions[session_id].update_conversation_history(user_message, bot_message)
    
    def get_context(self, session_id):
        return self.sessions[session_id].context if session_id in self.sessions else None