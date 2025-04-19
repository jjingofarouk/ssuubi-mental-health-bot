import random
import json
import logging
from typing import Dict, Union, Set, List
from datetime import datetime
from .intents import MessageIntent
from .patterns import get_patterns

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResponseGenerator:
    def __init__(self):
        self.patterns = get_patterns()
        # Load JSON responses
        try:
            with open('mental_health_responses.json', 'r') as f:
                self.json_responses = json.load(f)
        except FileNotFoundError:
            logger.warning("mental_health_responses.json not found, using empty responses")
            self.json_responses = {}
        self.user_history = {}  # {user_id: set(used_response_strings)}
        self.user_state = {}   # {user_id: {'stage': str, 'intent': MessageIntent, 'last_updated': datetime}}

    def generate_response(self, intent: MessageIntent, context: Dict) -> str:
        """
        Generate a context-aware response based on intent and context.
        Args:
            intent: Detected intent (e.g., ANXIETY, CRISIS).
            context: Dict with sentiment_analysis, details, user_id, preferences, emotional_state.
        Returns:
            Personalized response string.
        """
        user_id = context.get('user_id', 'default')
        sentiment = context.get('sentiment_analysis', {})
        details = context.get('details', {})
        preferences = context.get('preferences', {'preferred_technique': 'breathing'})
        used_responses = self.user_history.get(user_id, set())
        state = self.user_state.get(user_id, {
            'stage': 'validation',
            'intent': intent,
            'last_updated': datetime.utcnow()
        })

        # Crisis prioritization
        if intent == MessageIntent.CRISIS or 'crisis' in sentiment.get('themes', []):
            response = (
                "I’m deeply concerned about you. Please reach out now:\n"
                "Call 988 or text HOME to 741741 (US)\nEmergency: 911\n\n"
                "Would you like me to stay with you and talk?"
            )
            self.user_history.setdefault(user_id, set()).add(response)
            logger.info(f"Generated crisis response for user {user_id}")
            return response

        # JSON-based response
        json_key = intent.value.lower()
        if json_key in self.json_responses:
            responses = []
            for theme in sentiment.get('themes', []):
                if theme in self.json_responses.get(json_key, {}):
                    responses.extend(self.json_responses[json_key][theme])
            if responses:
                # Filter by emotional stage and preferences
                stage_responses = self._filter_by_stage(responses, state['stage'], preferences)
                # Serialize responses for comparison
                stage_responses = [r for r in stage_responses if json.dumps(r, sort_keys=True) not in used_responses] or stage_responses
                if stage_responses:
                    response_data = random.choice(stage_responses)
                    self.user_history.setdefault(user_id, set()).add(json.dumps(response_data, sort_keys=True))
                    self._update_state(user_id, intent, state['stage'])
                    return self._format_response(response_data, details, preferences)

        # Fallback to patterns
        pattern = next((p for p in self.patterns if p.intent == intent), None)
        if pattern:
            stage_responses = self._filter_by_stage(pattern.responses, state['stage'], preferences)
            # Serialize responses for comparison
            stage_responses = [r for r in stage_responses if json.dumps(r, sort_keys=True) not in used_responses] or stage_responses
            if stage_responses:
                response_data = random.choice(stage_responses)
                self.user_history.setdefault(user_id, set()).add(json.dumps(response_data, sort_keys=True))
                self._update_state(user_id, intent, state['stage'])
                return self._format_response(response_data, details, preferences)

        # Fallback response
        logger.warning(f"No matching response for intent {intent} and themes {sentiment.get('themes', [])}")
        return self._generate_fallback_response(context)

    def _filter_by_stage(self, responses: List[Union[str, Dict]], stage: str, preferences: Dict) -> List[Union[str, Dict]]:
        """
        Filter responses by emotional stage and user preferences.
        Args:
            responses: List of possible responses.
            stage: Current emotional stage ('validation', 'exploration', 'coping').
            preferences: User preferences (e.g., preferred_technique).
        Returns:
            Filtered list of responses.
        """
        if stage == 'validation':
            return [r for r in responses if 'validation' in str(r).lower() or 'sorry' in str(r).lower()]
        elif stage == 'exploration':
            return [r for r in responses if isinstance(r, dict) and 'followup' in r]
        elif stage == 'coping':
            preferred = preferences.get('preferred_technique', 'breathing').lower()
            return [
                r for r in responses
                if isinstance(r, dict) and 'techniques' in r and r['techniques']  # Ensure techniques exist
                and any(preferred in t.lower() for t in r['techniques'])
            ] or [r for r in responses if isinstance(r, dict) and 'techniques' in r]
        return responses

    def _update_state(self, user_id: str, intent: MessageIntent, current_stage: str) -> None:
        """
        Update user's emotional state for progression.
        Args:
            user_id: Unique user identifier.
            intent: Current intent.
            current_stage: Current emotional stage.
        """
        stages = ['validation', 'exploration', 'coping']
        next_stage = stages[min(stages.index(current_stage) + 1, len(stages) - 1)] if current_stage in stages else 'validation'
        self.user_state[user_id] = {
            'stage': next_stage,
            'intent': intent,
            'last_updated': datetime.utcnow()
        }
        logger.debug(f"Updated state for user {user_id}: stage={next_stage}, intent={intent}")

    def _format_response(self, response_data: Union[str, Dict], details: Dict, preferences: Dict) -> str:
        """
        Format response with details and preferences.
        Args:
            response_data: Response data (string or dict).
            details: Extracted details (e.g., trigger, intensity_words).
            preferences: User preferences (e.g., preferred_technique).
        Returns:
            Formatted response string.
        """
        if isinstance(response_data, str):
            return response_data

        if not isinstance(response_data, dict) or 'message' not in response_data:
            logger.error(f"Invalid response_data format: {response_data}")
            return "I’m here to help. Can you tell me more?"

        # Replace placeholders with details
        response = response_data['message']
        try:
            response = response.format(**{k: v or '' for k, v in details.items()})
        except (KeyError, ValueError) as e:
            logger.warning(f"Failed to format response with details: {e}")

        # Add techniques based on preferences
        if response_data.get('techniques'):
            preferred = preferences.get('preferred_technique', 'breathing').lower()
            techniques = [t for t in response_data['techniques'] if preferred in t.lower()] or response_data['techniques']
            if techniques:  # Ensure non-empty
                response += f"\n\nTry this: {random.choice(techniques)}"
            else:
                logger.debug("No techniques available for response")
        if response_data.get('followup'):
            response += f"\n\n{response_data['followup']}"
        if details.get('suggestion'):
            response += f"\n\n{details['suggestion']}"

        return response

    def _generate_fallback_response(self, context: Dict) -> str:
        """
        Generate a fallback response based on themes.
        Args:
            context: Dict with sentiment_analysis and other context.
        Returns:
            Fallback response string.
        """
        themes = context.get('sentiment_analysis', {}).get('themes', [])
        fallbacks = {
            'anxiety': "It sounds like you’re feeling anxious. Want to share more about what’s going on?",
            'depression': "I’m here for you. Can you tell me more about how you’re feeling?",
            'loneliness': "Feeling lonely is tough. Would you like to talk about it?",
            'grief': "I’m so sorry for your loss. Can I listen to what’s on your mind?",
            'default': "I’m here to listen. Can you tell me more about what you’re experiencing?"
        }
        for theme in themes:
            if theme in fallbacks:
                return fallbacks[theme]
        return fallbacks['default']