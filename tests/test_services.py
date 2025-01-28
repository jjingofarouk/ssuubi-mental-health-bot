import pytest
from app.services.conversation_manager import ConversationManager
from app.services.response_generator import ResponseGenerator

def test_conversation_manager():
    manager = ConversationManager()
    manager.create_session("123")
    assert "123" in manager.sessions

def test_response_generator():
    generator = ResponseGenerator()
    response = generator.generate_response("I feel sad", {})
    assert "message" in response