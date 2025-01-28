from flask import Blueprint, request, jsonify
from app.services.conversation_manager import ConversationManager
from app.services.response_generator import ResponseGenerator
from app.utils.helpers import validate_session

chat_bp = Blueprint('chat', __name__)

conversation_manager = ConversationManager()
response_generator = ResponseGenerator()

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    session_id = data.get('session_id')
    message = data.get('message')
    
    if not validate_session(session_id):
        return jsonify({"error": "Invalid session"}), 400
    
    if not session_id in conversation_manager.sessions:
        conversation_manager.create_session(session_id)
    
    context = conversation_manager.sessions[session_id].context
    response = response_generator.generate_response(message, context)
    
    conversation_manager.update_conversation_history(session_id, message, response['message'])
    
    return jsonify(response)