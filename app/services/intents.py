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
    
    