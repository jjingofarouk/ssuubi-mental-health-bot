from transformers import pipeline
from sentence_transformers import SentenceTransformer
import re
import logging
from typing import Tuple, Dict, Set
from .intents import MessageIntent
from .patterns import get_patterns

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageAnalyzer:
    def __init__(self):
        self.nlp = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            tokenizer="distilbert-base-uncased-finetuned-sst-2-english",
            clean_up_tokenization_spaces=False
        )
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.patterns = get_patterns()
        self.intent_theme_map = {
            MessageIntent.ANXIETY: ["anxiety", "panic", "worry"],
            MessageIntent.DEPRESSION: ["sadness", "hopelessness", "fatigue"],
            MessageIntent.CRISIS: ["suicide", "self-harm", "despair"],
            MessageIntent.STRESS: ["stress", "overwhelm", "pressure"],
            MessageIntent.GRIEF: ["grief", "loss", "mourning"],
            MessageIntent.SLEEP_ISSUES: ["insomnia", "sleep", "restless"],
            MessageIntent.WORK_ISSUES: ["work", "job", "career"],
            MessageIntent.FAMILY_ISSUES: ["family", "relationship", "divorce"],
            MessageIntent.GENERAL: []
        }

    def analyze_message(self, message: str, context: Dict) -> Tuple[MessageIntent, Dict]:
        """Analyze message to determine intent and extract details."""
        try:
            # Sentiment analysis
            sentiment = self.nlp(message)[0]
            sentiment_score = sentiment['score'] if sentiment['label'] == 'POSITIVE' else -sentiment['score']

            # Intent detection using regex patterns
            detected_intent = MessageIntent.GENERAL
            details = {'sentiment': sentiment['label'], 'confidence': abs(sentiment_score)}

            for intent, pattern in self.patterns.items():
                try:
                    if pattern.search(message):
                        detected_intent = intent
                        break
                except AttributeError as e:
                    logger.error(f"Invalid pattern for intent {intent}: {str(e)}")
                    continue

            # Extract themes based on intent
            themes = set(self.intent_theme_map.get(detected_intent, []))
            if 'keywords' in context.get('details', {}):
                themes.update(context['details']['keywords'])

            # Update details with themes and context
            details.update({
                'themes': list(themes),
                'intensity': 'moderate' if abs(sentiment_score) > 0.5 else 'low',
                'keywords': re.findall(r'\w+', message.lower())
            })

            return detected_intent, details

        except Exception as e:
            logger.error(f"Error analyzing message: {str(e)}")
            return MessageIntent.GENERAL, {
                'sentiment': 'NEUTRAL',
                'confidence': 0.0,
                'themes': [],
                'intensity': 'low',
                'keywords': []
            }