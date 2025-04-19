from .message_analyzer import MessageAnalyzer
from .response_generator import ResponseGenerator
from .crisis_handler import CrisisHandler
from .context import ConversationContext
from .intents import MessageIntent
from .sentiment_analyzer import SentimentAnalyzer

class ConversationHandler:
    def __init__(self):
        self.analyzer = MessageAnalyzer()
        self.response_generator = ResponseGenerator()
        self.crisis_handler = CrisisHandler()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.context = ConversationContext()

    def generate_response(self, message: str, session_id: str, user_id: str) -> str:
        # Analyze sentiment
        sentiment_result = self.sentiment_analyzer.analyze_message(message, {'user_id': user_id})
        context = self.context.get_context()
        context.update({
            'sentiment_analysis': sentiment_result,
            'user_id': user_id,
            'preferences': {'preferred_technique': 'breathing'}  # From user profile
        })

        if self.crisis_handler.is_crisis_message(message):
            self.context.update_context(
                intent=MessageIntent.CRISIS,
                interaction_count=context['interaction_count'] + 1,
                identified_themes=sentiment_result['themes'],
                crisis_mode=True
            )
            return self.crisis_handler.generate_crisis_response()

        intent, details = self.analyzer.analyze_message(message, context)
        context['details'] = details
        self.context.update_context(
            intent=intent,
            interaction_count=context['interaction_count'] + 1,
            identified_themes=sentiment_result['themes'],
            crisis_mode=False
        )

        return self.response_generator.generate_response(intent, context)