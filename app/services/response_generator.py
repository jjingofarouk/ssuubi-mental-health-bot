import numpy as np
import re
import json
from app.services.sentiment_analyzer import SentimentAnalyzer
from app.models.response_model import Response

class ResponseGenerator:
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        with open('app/data/therapeutic_responses.json', 'r') as f:
            self.therapeutic_responses = json.load(f)
    
    def generate_response(self, message, context):
        analysis = self.sentiment_analyzer.analyze_message(message)
        
        if self._contains_crisis_keywords(message):
            return self._generate_crisis_response()
        
        response = self._select_therapeutic_response(analysis, context)
        return Response(response, analysis).to_dict()
    
    def _contains_crisis_keywords(self, message):
        crisis_keywords = {'suicide', 'kill myself', 'end it all', 'dont want to live', 'want to die', 'harm myself', 'cut myself'}
        return any(keyword in message.lower() for keyword in crisis_keywords)
    
    def _generate_crisis_response(self):
        return {
            "message": "I hear that you're in a lot of pain. Your life has value and there are people who want to help. "
                      "Please reach out to a crisis counselor right now:",
            "resources": {
                "crisis_line": "1-800-273-8255",
                "crisis_text": "Text HOME to 741741",
                "emergency": "911"
            },
            "priority": "urgent"
        }
    
    def _select_therapeutic_response(self, analysis, context):
        theme_responses = self.therapeutic_responses.get(analysis['themes'][0] if analysis['themes'] else 'general')
        
        if analysis['sentiment']['label'] == 'NEGATIVE' and analysis['emotion_intensity'] > 2:
            response_type = 'validation_and_support'
        elif analysis['sentiment']['label'] == 'NEGATIVE':
            response_type = 'exploration'
        else:
            response_type = 'reinforcement'
            
        response = np.random.choice(theme_responses[response_type])
        
        return {
            "message": response,
            "analysis": analysis,
            "suggested_techniques": self._suggest_coping_techniques(analysis['themes']),
            "priority": "normal"
        }
    
    def _suggest_coping_techniques(self, themes):
        techniques = {
            'anxiety': ['deep breathing', 'grounding exercises', 'progressive muscle relaxation'],
            'depression': ['behavioral activation', 'gratitude practice', 'pleasant activity scheduling'],
            'relationships': ['communication skills', 'boundary setting', 'active listening'],
            'self_esteem': ['positive self-talk', 'accomplishment journaling', 'strength identification'],
            'trauma': ['containment exercises', 'safe place visualization', 'present-moment awareness']
        }
        
        suggested_techniques = []
        for theme in themes:
            if theme in techniques:
                suggested_techniques.extend(techniques[theme])
        
        return suggested_techniques[:2]