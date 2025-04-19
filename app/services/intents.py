from enum import Enum

class MessageIntent(Enum):
    GREETING = "greeting"
    FAREWELL = "farewell"
    CRISIS = "crisis"
    ANXIETY = "anxiety"
    DEPRESSION = "depression"
    GRATITUDE = "gratitude"
    GENERAL = "general"
    UNKNOWN = "unknown"
    STRESS = "stress"
    LONELINESS = "loneliness"
    ANGER = "anger"
    SELF_CARE = "self_care"
    RELATIONSHIP = "relationship"
    GRIEF = "grief"
    SLEEP = "sleep"
    MOTIVATION = "motivation"
    WORK_STRESS = "work_stress"
    FAMILY = "family"
    TRAUMA = "trauma"  # New
    SELF_ESTEEM = "self_esteem"  # New
    
    pip install sentence-transformers==3.1.1 transformers==4.44.2 googletrans==4.0.0-rc1 pymongo==4.10.1 nltk==3.9.1
python -c "import nltk; nltk.download('punkt')"