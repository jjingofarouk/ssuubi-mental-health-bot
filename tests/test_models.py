from app.models.session_model import Session

def test_session_model():
    session = Session("123")
    session.update_conversation_history("Hello", "Hi there")
    assert len(session.conversation_history) == 1