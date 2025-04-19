import random
import json
from typing import Dict
from .intents import MessageIntent
from .patterns import get_patterns

class ResponseGenerator:
    def __init__(self):
        self.patterns = get_patterns()
        with open('mental_health_responses.json') as f:
            self.json_responses = json.load(f)
        self.user_history = {}  # {user_id: set(used_responses)}
        self.user_state = {}  # {user_id: {'stage': 'validation', 'intent': MessageIntent}}

    def generate_response(self, intent: MessageIntent, context: Dict) -> str:
        user_id = context.get('user_id', 'default')
        sentiment = context.get('sentiment_analysis', {})
        details = context.get('details', {})
        used_responses = self.user_history.get(user_id, set())
        state = self.user_state.get(user_id, {'stage': 'validation', 'intent': intent})

        # Crisis prioritization
        if intent == MessageIntent.CRISIS:
            return (
                "I’m very concerned about you. Please call 988 or text HOME to 741741 for immediate support.\n\n"
                "Would you like me to stay with you and talk more?"
            )

        # JSON-based response
        json_key = intent.value.lower()
        if json_key in self.json_responses:
            responses = []
            for theme in sentiment.get('themes', []):
                if theme in self.json_responses[json_key]:
                    responses.extend(self.json_responses[json_key][theme])
            if responses:
                responses = [r for r in responses if r not in used_responses] or responses
                response_data = random.choice(responses)
                self.user_history.setdefault(user_id, set()).add(response_data)
                # Update state
                if state['stage'] == 'validation':
                    self.user_state[user_id] = {'stage': 'exploration', 'intent': intent}
                elif state['stage'] == 'exploration':
                    self.user_state[user_id] = {'stage': 'coping', 'intent': intent}
                return self._format_response(response_data, details)

        # Fallback to patterns
        pattern = next((p for p in self.patterns if p.intent == intent), None)
        if pattern:
            responses = {
                'validation': [r for r in pattern.responses if 'validation' in str(r).lower()],
                'exploration': [r for r in pattern.responses if 'followup' in r],
                'coping': [r for r in pattern.responses if r.get('techniques')]
            }.get(state['stage'], pattern.responses)
            responses = [r for r in responses if r not in used_responses] or responses
            response_data = random.choice(responses)
            self.user_history.setdefault(user_id, set()).add(response_data)
            # Update state
            if state['stage'] == 'validation':
                self.user_state[user_id] = {'stage': 'exploration', 'intent': intent}
            elif state['stage'] == 'exploration':
                self.user_state[user_id] = {'stage': 'coping', 'intent': intent}
            return self._format_response(response_data, details)

        return self._generate_fallback_response(context)

    def _format_response(self, response_data: Union[str, Dict], details: Dict) -> str:
        if isinstance(response_data, str):
            return response_data
        response = response_data['message'].format(**details)
        if response_data.get('techniques'):
            response += "\n\nTry these: " + ", ".join(response_data['techniques'])
        if response_data.get('followup'):
            response += f"\n\n{response_data['followup']}"
        return response

    def _generate_fallback_response(self, context: Dict) -> str:
        themes = context.get('sentiment_analysis', {}).get('themes', [])
        fallbacks = {
            'anxiety': "It sounds like you’re feeling anxious. Want to share more?",
            'depression': "I’m here for you. Can you tell me how you’re feeling?",
            'crisis': "I’m concerned. Please call 988 or text HOME to 741741.",
            'default': "I’m here to listen. Can you tell me more?"
        }
        for theme in themes:
            if theme in fallbacks:
                return fallbacks[theme]
        return random.choice([fallbacks['default']])