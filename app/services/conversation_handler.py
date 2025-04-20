from typing import Dict, Optional
from googletrans import Translator
import logging
from .message_analyzer import MessageAnalyzer
from .response_generator import ResponseGenerator
from .crisis_handler import CrisisHandler
from .context import ConversationContext
from .sentiment_analyzer import SentimentAnalyzer
from .intents import MessageIntent
from app.models.session_model import Session
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConversationHandler:
    def __init__(self):
        self.analyzer = MessageAnalyzer()
        self.response_generator = ResponseGenerator()
        self.crisis_handler = CrisisHandler()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.context = ConversationContext()
        self.translator = Translator()
        self.sessions = {}

    def create_session(self, session_id: str, user_id: str) -> None:
        try:
            self.sessions[session_id] = Session(session_id, user_id)
            self.context.update_context(
                user_id=user_id,
                intent=None,
                interaction_count=0,
                identified_themes=set(),
                crisis_mode=False,
                details={},
                preferences={'preferred_technique': 'breathing'},
                emotional_state='validation'
            )
            logger.info(f"Created session {session_id} for user {user_id}")
        except Exception as e:
            logger.error(f"Failed to create session {session_id}: {str(e)}")
            raise

    def generate_response(self, message: str, session_id: str = None, user_id: str = None, language: str = 'en') -> str:
        original_message = message
        try:
            session_id = session_id or 'default-session'
            user_id = user_id or 'default-user'

            if session_id not in self.sessions:
                self.create_session(session_id, user_id)

            if language != 'en':
                message = self.translator.translate(message, dest='en').text
                logger.debug(f"Translated message from {language} to en: {message}")

            sentiment_result = self.sentiment_analyzer.analyze_message(message, {'user_id': user_id})
            context = self.context.get_context(user_id)
            context.update({
                'sentiment_analysis': sentiment_result,
                'user_id': user_id,
                'session_id': session_id,
                'language': language,
                'preferences': context.get('preferences', {'preferred_technique': 'breathing'})
            })

            if self.crisis_handler.is_crisis_message(message, sentiment_result):
                self.context.update_context(
                    user_id=user_id,
                    intent=MessageIntent.CRISIS.value,  # Convert to string
                    interaction_count=context['interaction_count'] + 1,
                    identified_themes=set(sentiment_result['themes']),
                    crisis_mode=True,
                    details={},
                    preferences=context['preferences'],
                    emotional_state='validation'
                )
                response = self.crisis_handler.generate_crisis_response(context)
                self._update_session(session_id, original_message, response)
                return self.translator.translate(response, dest=language).text if language != 'en' else response

            intent, details = self.analyzer.analyze_message(message, context)
            context['details'] = details

            if 'anxiety' in sentiment_result['themes'] and context['interaction_count'] > 2:
                if context['preferences']['preferred_technique'] in ['breathing', 'grounding']:
                    details['suggestion'] = f"Since you’ve mentioned anxiety before, would you like to try {context['preferences']['preferred_technique']} again?"

            self.context.update_context(
                user_id=user_id,
                intent=intent.value if isinstance(intent, MessageIntent) else intent,  # Convert to string
                interaction_count=context['interaction_count'] + 1,
                identified_themes=set(sentiment_result['themes']),
                crisis_mode=False,
                details=details,
                preferences=context['preferences'],
                emotional_state='validation'
            )

            response = self.response_generator.generate_response(intent, context)
            self._update_session(session_id, original_message, response)
            return self.translator.translate(response, dest=language).text if language != 'en' else response

        except Exception as e:
            logger.error(f"Error in conversation handler: {str(e)}")
            fallback = "I’m having trouble understanding. Can you say that again?"
            self._update_session(session_id, original_message, fallback)
            return self.translator.translate(fallback, dest=language).text if language != 'en' else fallback

    def _update_session(self, session_id: str, user_message: str, bot_message: str) -> None:
        if session_id in self.sessions:
            self.sessions[session_id].update_conversation_history(user_message, bot_message)
            logger.debug(f"Updated session {session_id} with user: {user_message}, bot: {bot_message}")