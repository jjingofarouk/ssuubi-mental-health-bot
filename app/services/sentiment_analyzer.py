import re
from typing import Dict, List, Set
import nltk
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

nltk.download('punkt')

class SentimentAnalyzer:
    def __init__(self):
        # Initialize sentiment analysis pipeline
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        # Initialize SentenceTransformers for theme detection fallback
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        # Precompute embeddings for theme keywords
        self.theme_keywords = self._get_theme_keywords()
        self.theme_embeddings = {
            theme: self.embedding_model.encode(keywords, convert_to_tensor=True)
            for theme, keywords in self.theme_keywords.items()
        }
        # User history for context
        self.user_history = {}  # {user_id: [(message, themes, timestamp)]}

    def analyze_message(self, message: str, context: Dict = None) -> Dict:
        """
        Analyze message for sentiment, intensity, and themes.
        Args:
            message: User input string.
            context: Optional dict with user_id, preferences, etc.
        Returns:
            Dict with sentiment, emotion_intensity, themes, and context.
        """
        context = context or {}
        user_id = context.get('user_id', 'default')

        # Analyze sentiment
        sentiment = self.sentiment_analyzer(message)[0]
        # Detect intensity
        emotion_intensity = self._detect_emotion_intensity(message)
        # Identify themes (hybrid regex + NLP)
        themes = self._identify_themes(message)
        # Update history
        self._update_history(user_id, message, themes)

        return {
            'sentiment': sentiment,
            'emotion_intensity': emotion_intensity,
            'themes': themes,
            'context': self._get_user_context(user_id)
        }

    def _get_theme_keywords(self) -> Dict[str, List[str]]:
        """
        Define 20 themes with 126 total keywords/phrases.
        """
        return {
            'anxiety': ['anxious', 'worried', 'nervous', 'stressed', 'panicky', 'uneasy', 'restless', 'jittery', 'overwhelmed', 'tense'],
            'depression': ['depressed', 'sad', 'hopeless', 'down', 'blue', 'despair', 'gloomy', 'empty', 'miserable', 'low'],
            'stress': ['stressed', 'overwhelmed', 'pressure', 'strained', 'frazzled', 'burnt out', 'exhausted', 'overworked'],
            'loneliness': ['lonely', 'alone', 'isolated', 'abandoned', 'friendless', 'disconnected', 'solitary', 'lonesome'],
            'anger': ['angry', 'furious', 'mad', 'irritated', 'enraged', 'annoyed', 'frustrated', 'resentful'],
            'self_esteem': ['worthless', 'failure', 'inadequate', 'not good enough', 'useless', 'inferior', 'incompetent'],
            'trauma': ['trauma', 'abuse', 'ptsd', 'flashback', 'triggered', 'haunted', 'scarred'],
            'relationships': ['relationship', 'partner', 'friend', 'family', 'spouse', 'breakup', 'conflict', 'betrayal'],
            'grief': ['grief', 'loss', 'mourning', 'bereaved', 'heartbroken', 'sorrow', 'devastated'],
            'fear': ['afraid', 'scared', 'terrified', 'petrified', 'frightened', 'phobia', 'dread'],
            'guilt': ['guilty', 'ashamed', 'regret', 'remorse', 'sorry', 'blame'],
            'shame': ['shame', 'embarrassed', 'humiliated', 'disgraced', 'mortified', 'awkward'],
            'hopelessness': ['hopeless', 'despairing', 'futile', 'pointless', 'giving up', 'defeated'],
            'fatigue': ['tired', 'exhausted', 'drained', 'weary', 'fatigued', 'burnout'],
            'confusion': ['confused', 'lost', 'uncertain', 'puzzled', 'disoriented', 'unclear'],
            'crisis': ['crisis', 'suicidal', 'harm myself', 'end it', 'desperate', 'breakdown', 'can’t go on'],
            'joy': ['happy', 'joyful', 'elated', 'excited', 'cheerful', 'delighted'],
            'work': ['job', 'work', 'career', 'boss', 'workplace', 'unemployed'],
            'health': ['health', 'illness', 'sick', 'pain', 'chronic', 'injury'],
            'motivation': ['unmotivated', 'no drive', 'lazy', 'stuck', 'apathetic', 'uninspired']
        }

    def _detect_emotion_intensity(self, message: str) -> float:
        """
        Detect emotional intensity based on modifiers.
        """
        intensity_markers = {
            'very': 2.0,
            'extremely': 3.0,
            'really': 1.5,
            'so': 1.5,
            'absolutely': 2.0,
            'terribly': 2.5,
            'awfully': 2.5,
            'incredibly': 2.5,
            'highly': 2.0,
            'severely': 3.0,
            'tremendously': 3.0,
            'unbearably': 3.0,
            'overwhelmingly': 3.0,
            'desperately': 2.5,
            'profoundly': 2.5,
            'slightly': 0.5,
            'barely': 0.5,
            'somewhat': 1.0,
            'moderately': 1.0
        }

        words = word_tokenize(message.lower())
        intensity_score = sum(intensity_markers.get(word, 0) for word in words)
        return min(intensity_score, 5.0)  # Cap at 5 for balance

    def _identify_themes(self, message: str) -> List[str]:
        """
        Identify themes using hybrid regex + NLP approach.
        """
        themes = set()

        # Step 1: Regex-based matching
        patterns = {
            theme: r'\b(' + '|'.join(keywords) + r')\b'
            for theme, keywords in self.theme_keywords.items()
        }
        for theme, pattern in patterns.items():
            if re.search(pattern, message.lower()):
                themes.add(theme)

        # Step 2: NLP fallback if no themes detected or for ambiguous inputs
        if not themes or len(themes) < 2:  # Allow NLP to add more themes
            message_embedding = self.embedding_model.encode(message, convert_to_tensor=True)
            for theme, keyword_embeddings in self.theme_embeddings.items():
                similarity = util.cos_sim(message_embedding, keyword_embeddings).max().item()
                if similarity > 0.6:  # Threshold for relevance
                    themes.add(theme)

        return sorted(list(themes))  # Sort for consistency

    def _update_history(self, user_id: str, message: str, themes: List[str]):
        """
        Update user conversation history.
        """
        import time
        self.user_history.setdefault(user_id, []).append((message, themes, time.time()))
        self.user_history[user_id] = self.user_history[user_id][-10:]  # Keep last 10

    def _get_user_context(self, user_id: str) -> Dict:
        """
        Retrieve user context from history.
        """
        history = self.user_history.get(user_id, [])
        recent_themes = [entry[1] for entry in history]
        return {
            'recent_themes': recent_themes,
            'last_themes': recent_themes[-1] if recent_themes else [],
            'message_count': len(history)
        }