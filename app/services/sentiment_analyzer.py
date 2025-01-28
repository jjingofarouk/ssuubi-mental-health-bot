from transformers import pipeline
import nltk
from nltk.tokenize import word_tokenize
import re

nltk.download('punkt')

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = pipeline("sentiment-analysis")
    
    def analyze_message(self, message):
        sentiment = self.analyzer(message)[0]
        emotion_intensity = self._detect_emotion_intensity(message)
        themes = self._identify_themes(message)
        
        return {
            'sentiment': sentiment,
            'emotion_intensity': emotion_intensity,
            'themes': themes
        }
    
    def _detect_emotion_intensity(self, message):
        intensity_markers = {
            'very': 2,
            'extremely': 3,
            'really': 1.5,
            'so': 1.5,
            'absolutely': 2
        }
        
        words = word_tokenize(message.lower())
        intensity_score = sum(intensity_markers.get(word, 0) for word in words)
        return min(intensity_score, 3)
    
    def _identify_themes(self, message):
        themes = set()
        patterns = {
            'anxiety': r'\b(anxiety|worried|nervous|stress)\b',
            'depression': r'\b(depress|sad|hopeless|down)\b',
            'relationships': r'\b(relationship|partner|friend|family)\b',
            'self_esteem': r'\b(worthless|failure|not good enough)\b',
            'trauma': r'\b(trauma|abuse|ptsd|flashback)\b'
        }
        
        for theme, pattern in patterns.items():
            if re.search(pattern, message.lower()):
                themes.add(theme)
        
        return list(themes)