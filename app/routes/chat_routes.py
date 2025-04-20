from flask import Blueprint, request, jsonify
import traceback
import logging
from typing import Dict
from dataclasses import asdict

from app.services.conversation_handler import ConversationHandler
from app.services.intents import MessageIntent
from app.utils.helpers import validate_session

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__)

conversation_handlers: Dict[str, ConversationHandler] = {}

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            logger.warning("No data provided in request")
            return jsonify({"error": "No data provided"}), 400

        session_id = data.get('session_id')
        user_id = data.get('user_id', f"user_{session_id}")
        message = data.get('message')
        language = data.get('language', 'en')

        if not session_id or not message or not user_id:
            logger.warning("Missing required fields in request")
            return jsonify({"error": "Missing session_id, user_id, or message"}), 400

        if not validate_session(session_id):
            logger.warning(f"Invalid session: {session_id}")
            return jsonify({"error": "Invalid session"}), 401

        handler = _get_or_create_handler(session_id)
        response_data = _process_message(handler, message, session_id, user_id, language)
        _cleanup_old_sessions()

        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return _create_error_response(e)

def _get_or_create_handler(session_id: str) -> ConversationHandler:
    if session_id not in conversation_handlers:
        logger.info(f"Creating new conversation handler for session: {session_id}")
        conversation_handlers[session_id] = ConversationHandler()
    return conversation_handlers[session_id]

def _process_message(handler: ConversationHandler, message: str, session_id: str, user_id: str, language: str) -> dict:
    response = handler.generate_response(message, session_id, user_id, language)
    context = handler.context.get_context(user_id)
    
    response_data = {
        "message": response,
        "context": {
            "interaction_count": context["interaction_count"],
            "identified_themes": list(context["identified_themes"]),
            "crisis_mode": context["crisis_mode"],
            "previous_intent": context.get("previous_intent", None)  # Handle missing previous_intent
        }
    }

    if context["crisis_mode"]:
        response_data.update({
            "priority": "urgent",
            "resources": {
                "crisis_line": "1-800-273-8255",
                "crisis_text": "Text HOME to 741741",
                "emergency": "911"
            }
        })

    return response_data

def _create_error_response(error: Exception) -> tuple:
    response = {
        "error": "Internal server error",
        "message": "I apologize, but something went wrong. Please try again."
    }
    if logger.getEffectiveLevel() == logging.DEBUG:
        response["details"] = str(error)
    return jsonify(response), 500

def _cleanup_old_sessions(max_sessions: int = 1000):
    if len(conversation_handlers) > max_sessions:
        sorted_sessions = sorted(
            conversation_handlers.items(),
            key=lambda x: x[1].context.get_context(x[1].context.get_context(x[1].sessions.get('default-session', Session('default-session', 'default-user')).user_id)["user_id"])["interaction_count"]
        )
        sessions_to_remove = len(conversation_handlers) - max_sessions
        for session_id, _ in sorted_sessions[:sessions_to_remove]:
            logger.info(f"Cleaning up old session: {session_id}")
            del conversation_handlers[session_id]