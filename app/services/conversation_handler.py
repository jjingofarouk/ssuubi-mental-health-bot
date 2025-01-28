# services/conversation_handler.py
from .message_analyzer import MessageAnalyzer
from .response_generator import ResponseGenerator
from .crisis_handler import CrisisHandler
from .context import ConversationContext
from .intents import MessageIntent

class ConversationHandler:
    def __init__(self):
        self.analyzer = MessageAnalyzer()
        self.response_generator = ResponseGenerator()
        self.crisis_handler = CrisisHandler()
        self.context = ConversationContext()

    def generate_response(self, message: str) -> str:
        if self.crisis_handler.is_crisis_message(message):
            self.context.update_context(intent=MessageIntent.CRISIS, interaction_count=self.context.get_context()["interaction_count"] + 1, identified_themes=self.context.get_context()["identified_themes"], crisis_mode=True)
            return self.crisis_handler.generate_crisis_response()

        intent, details = self.analyzer.analyze_message(message)
        self.context.update_context(intent=intent, interaction_count=self.context.get_context()["interaction_count"] + 1, identified_themes=self.context.get_context()["identified_themes"], crisis_mode=False)

        return self.response_generator.generate_response(intent, self.context.get_context())