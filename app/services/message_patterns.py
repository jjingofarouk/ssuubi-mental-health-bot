# services/message_patterns.py
from dataclasses import dataclass
from typing import List, Pattern, Dict, Union
import re
from .intents import MessageIntent

@dataclass
class MessagePattern:
    intent: MessageIntent
    patterns: List[Pattern]
    responses: List[Union[str, Dict]]

patterns_data = [
MessagePattern(
    intent=MessageIntent.GREETING,
    patterns=[
        re.compile(r'h(?:ello|i|ey)', re.IGNORECASE),
        re.compile(r'good\s*(morning|afternoon|evening)', re.IGNORECASE),
        re.compile(r'hey\s*there', re.IGNORECASE),
        re.compile(r'hi\s*(?:ya|there|everyone|you)?', re.IGNORECASE),
        re.compile(r'(sup|whats\s*up)', re.IGNORECASE),
        re.compile(r'howdy', re.IGNORECASE),
        re.compile(r'yo', re.IGNORECASE),
        re.compile(r'bonjour', re.IGNORECASE),
        re.compile(r'ola', re.IGNORECASE),
        re.compile(r'namaste', re.IGNORECASE),
        re.compile(r'hi\s*everybody', re.IGNORECASE),
        re.compile(r'hey\s*buddy', re.IGNORECASE),
        re.compile(r'how\s*are\s*you', re.IGNORECASE),
        re.compile(r'what\'s\s*going\s*on', re.IGNORECASE),
        re.compile(r'what\'s\s*up\s*doc', re.IGNORECASE),
        re.compile(r'hello\s*there', re.IGNORECASE),
        re.compile(r'(hey|hi|hello)\s*(?:friend|pal|mate|stranger)?', re.IGNORECASE),
        re.compile(r'(how\'s|how\s*are)\s*you\s*(?:doing|feeling|today)?', re.IGNORECASE),
        re.compile(r'how\s*are\s*things', re.IGNORECASE),
        re.compile(r'(greetings|salutations)', re.IGNORECASE),
        re.compile(r'(hey\s*yo|yo\s*yo)', re.IGNORECASE)
    ],
    responses=[
        "Hello! How are you feeling today?",
        "Hi there! I'm here to listen. What's on your mind?",
        "Welcome! How can I support you today?",
        "Hey! It's great to hear from you. How are you doing?",
        "Hey there! How's everything going?",
        "Hello! I’m glad you’re here. How can I assist you?",
        "Hi! What’s going on in your world today?",
        "Hey! It’s nice to meet you. How are you feeling?",
        "Good day! How can I help with your journey today?",
        "Greetings! How’s everything on your end?",
        "Hello, friend! What can I do for you today?",
        "Hey buddy, how’s life treating you?",
        "Hi there! How’s your day going?",
        "Hello, how are you today? I’m here to help!",
        "Namaste! How can I assist you today?",
        "Ola! How are things going for you?",
        "Salut! How’s your day going so far?",
        "Howdy! I hope you’re having a good day. What can I do for you?",
        "Hey, it’s great to see you. How can I help today?",
        "Hello! What’s up? I’m all ears.",
        "Hi there! Feeling anything you want to share?",
        "Hey there, friend! How’s everything with you?",
        "Yo! How are you today?",
        "Good morning! How are you feeling today?",
        "Good afternoon! I’m here to listen if you need me.",
        "Good evening! How can I support you tonight?"
    ]
),
MessagePattern(
    intent=MessageIntent.FAREWELL,
    patterns=[
        re.compile(r'goodbye', re.IGNORECASE),
        re.compile(r'bye', re.IGNORECASE),
        re.compile(r'see\s*ya', re.IGNORECASE),
        re.compile(r'take\s*care', re.IGNORECASE),
        re.compile(r'farewell', re.IGNORECASE),
        re.compile(r'catch\s*you\s*later', re.IGNORECASE),
        re.compile(r'peace\s*out', re.IGNORECASE),
        re.compile(r'laters', re.IGNORECASE),
        re.compile(r'cya', re.IGNORECASE),
        re.compile(r'see\s*you\s*soon', re.IGNORECASE),
        re.compile(r'until\s*next\s*time', re.IGNORECASE),
        re.compile(r'be\s*safe', re.IGNORECASE),
        re.compile(r'take\s*it\s*easy', re.IGNORECASE),
        re.compile(r'hope\s*to\s*see\s*you\s*again', re.IGNORECASE),
        re.compile(r'bye\s*for\s*now', re.IGNORECASE),
        re.compile(r'goodnight', re.IGNORECASE),
        re.compile(r'thank\s*you', re.IGNORECASE),
        re.compile(r'good\s*bye\s*now', re.IGNORECASE),
        re.compile(r'catch\s*you\s*on\s*the\s*flip\s*side', re.IGNORECASE),
        re.compile(r'good\s*day', re.IGNORECASE),
        re.compile(r'good\s*bye\s*for\s*now', re.IGNORECASE),
        re.compile(r'fare\s*thee\s*well', re.IGNORECASE),
        re.compile(r'peace\s*and\s*love', re.IGNORECASE),
        re.compile(r'adios', re.IGNORECASE),
        re.compile(r'adieu', re.IGNORECASE),
        re.compile(r'buh-bye', re.IGNORECASE),
        re.compile(r'see\s*you\s*later\s*alligator', re.IGNORECASE),
        re.compile(r'take\s*care\s*of\s*yourself', re.IGNORECASE),
        re.compile(r'catch\s*you\s*later\s*alligator', re.IGNORECASE),
        re.compile(r'goodbye\s*for\s*now', re.IGNORECASE),
        re.compile(r'thank\s*you\s*for\s*your\s*time', re.IGNORECASE),
        re.compile(r'bye\s*for\s*now\s*and\s*take\s*care', re.IGNORECASE),
        re.compile(r'until\s*next\s*time\s*take\s*care', re.IGNORECASE),
        re.compile(r'been\s*good\s*talking\s*to\s*you', re.IGNORECASE),
        re.compile(r'see\s*you\s*around', re.IGNORECASE),
        re.compile(r'see\s*you\s*later\s*alligator', re.IGNORECASE),
        re.compile(r'catch\s*you\s*on\s*the\s*flip\s*side', re.IGNORECASE),
        re.compile(r'till\s*we\s*meet\s*again', re.IGNORECASE),
        re.compile(r'catch\s*you\s*soon', re.IGNORECASE),
        re.compile(r'be\s*well', re.IGNORECASE),
        re.compile(r'hope\s*you\s*have\s*a\s*good\s*day', re.IGNORECASE),
        re.compile(r'looking\s*forward\s*to\s*our\s*next\s*chat', re.IGNORECASE),
        re.compile(r'it\s*was\s*great\s*talking\s*to\s*you', re.IGNORECASE),
        re.compile(r'will\s*miss\s*you', re.IGNORECASE),
        re.compile(r'it\s*was\s*nice\s*chatting\s*with\s*you', re.IGNORECASE),
        re.compile(r'good\s*to\s*see\s*you', re.IGNORECASE),
        re.compile(r'come\s*back\s*soon', re.IGNORECASE),
        re.compile(r'goodbye\s*for\s*now\s*and\s*stay\s*safe', re.IGNORECASE),
        re.compile(r'good\s*to\s*chat\s*with\s*you', re.IGNORECASE),
        re.compile(r'take\s*good\s*care', re.IGNORECASE),
        re.compile(r'be\s*safe\s*and\s*well', re.IGNORECASE),
        re.compile(r'thanks\s*for\s*chatting', re.IGNORECASE),
        re.compile(r'bye\s*for\s*now\s*take\s*care', re.IGNORECASE),
        re.compile(r'looking\s*forward\s*to\s*our\s*next\s*chat', re.IGNORECASE),
    ],
    responses=[
        "Goodbye! Take care of yourself.",
        "Bye! Remember, I'm here if you need to talk.",
        "See you later! Wishing you a peaceful day.",
        "Take care! Reach out anytime you need support.",
        "Farewell! I hope everything goes well for you.",
        "Catch you later! Stay safe and take care.",
        "Peace out! Wishing you all the best.",
        "Later! Take care and have a wonderful day.",
        "Goodbye for now, I’ll be here if you need me.",
        "Take it easy! Hope to talk to you again soon.",
        "See you soon! Be well until next time.",
        "Take care of yourself! I’ll be waiting here if you need me.",
        "Hope to see you again! Stay safe out there.",
        "Goodbye for now! I’m always here if you need to talk.",
        "Catch you later! Don’t hesitate to come back if you need help.",
        "Take care and be well, until next time!",
        "Thanks for chatting with me today. Take care!",
        "Good night! Wishing you peaceful dreams.",
        "Have a great day ahead! I’ll be here whenever you need me.",
        "Goodbye! Wishing you calm and peace in everything you do.",
        "Hope to see you again soon! Be kind to yourself.",
        "Take care and stay strong! Until next time!",
        "It was a pleasure talking with you! Be well.",
        "Stay safe, and I’ll talk to you later!",
        "Goodbye, and don’t forget I’m here for you.",
        "I’m here whenever you need me. Take care!",
        "See you later! Have a wonderful day ahead.",
        "It’s always good to chat with you. Take care!",
        "Goodbye for now! You’ve got this!",
        "Thanks for spending time with me. Take care and come back anytime.",
        "I’m glad we talked. Wishing you the best!",
        "Take care! Don’t hesitate to reach out when you need support.",
        "Until next time, take care of yourself.",
        "It was nice talking to you! See you soon!",
        "Catch you later, and stay safe!",
        "Thanks for chatting! I’ll be here next time.",
        "Goodbye! Wishing you strength and peace.",
        "See you soon! I’m always here if you need help.",
        "Take care! I’ll be waiting here whenever you’re ready to chat.",
        "Goodbye! Take it easy, and don’t forget to look after yourself.",
        "It’s been a pleasure! Hope to chat again soon.",
        "Wishing you all the best! Take care!",
        "Hope you have a good rest of your day. Take care of yourself.",
        "Until next time! I’ll be here when you’re ready to chat again.",
        "Take care! I’ll be waiting here for our next conversation.",
        "Goodbye! Stay strong and take care of your mental health.",
        "See you next time! Remember, you’re not alone.",
        "It was great talking to you! Take care and be kind to yourself."
    ]
),

MessagePattern(
    intent=MessageIntent.ANXIETY,
    patterns=[
        re.compile(r'(feel(?:ing)?|am)\s*(very|really|so)?\s*(anxious|nervous|worried)', re.IGNORECASE),
        re.compile(r'(having|had)\s*(an?)?\s*anxiety\s*(attack|episode)', re.IGNORECASE),
        re.compile(r'(my|the)\s*anxiety\s*(is|has been)', re.IGNORECASE),
        re.compile(r'panic\s*(attack|feeling)', re.IGNORECASE),
        re.compile(r'overwhelmed\s*with\s*worry', re.IGNORECASE),
        re.compile(r'feeling\s*on\s*edge', re.IGNORECASE),
        re.compile(r'stressed\s*out', re.IGNORECASE),
        re.compile(r'scared\s*about\s*(?:the\s*future|something)', re.IGNORECASE),
        re.compile(r'feel\s*like\s*I\s*can\'t\s*cope', re.IGNORECASE),
        re.compile(r'heart\s*is\s*racing', re.IGNORECASE),
        re.compile(r'can\'t\s*stop\s*thinking\s*about\s*(?:something|it)', re.IGNORECASE),
        re.compile(r'constantly\s*worried', re.IGNORECASE),
        re.compile(r'feel\s*trapped\s*by\s*my\s*thoughts', re.IGNORECASE),
        re.compile(r'getting\s*so\s*stressed', re.IGNORECASE),
        re.compile(r'can\'t\s*focus\s*because\s*of\s*anxiety', re.IGNORECASE),
        re.compile(r'feeling\s*restless', re.IGNORECASE),
        re.compile(r'my\s*nerves\s*are\s*shot', re.IGNORECASE),
        re.compile(r'feeling\s*like\s*I\s*can\'t\s*calm\s*down', re.IGNORECASE),
        re.compile(r'just\s*can\'t\s*relax', re.IGNORECASE),
        re.compile(r'feeling\s*overwhelmed\s*by\s*everything', re.IGNORECASE),
        re.compile(r'feeling\s*tense', re.IGNORECASE),
        re.compile(r'can\'t\s*catch\s*my\s*breath', re.IGNORECASE),
        re.compile(r'feel\s*like\s*I\'m\s*losing\s*control', re.IGNORECASE),
        re.compile(r'my\s*thoughts\s*are\s*racing', re.IGNORECASE),
        re.compile(r'getting\s*panicked\s*over\s*little\s*things', re.IGNORECASE),
        re.compile(r'feeling\s*like\s*I\s*can\'t\s*handle\s*this', re.IGNORECASE),
        re.compile(r'feeling\s*shaky\s*from\s*anxiety', re.IGNORECASE),
        re.compile(r'feeling\s*uneasy\s*and\s*restless', re.IGNORECASE),
        re.compile(r'my\s*body\s*is\s*tight\s*with\s*anxiety', re.IGNORECASE),
        re.compile(r'feeling\s*like\s*I\s*can\'t\s*escape', re.IGNORECASE),
        re.compile(r'short\s*of\s*breath\s*from\s*anxiety', re.IGNORECASE),
        re.compile(r'feeling\s*on\s*edge\s*all\s*the\s*time', re.IGNORECASE),
        re.compile(r'anxiety\s*feels\s*like\s*it\s*won\'t\s*end', re.IGNORECASE),
        re.compile(r'feeling\s*nervous\s*for\s*no\s*reason', re.IGNORECASE),
        re.compile(r'getting\s*anxious\s*when\s*I\s*have\s*to\s*do\s*something', re.IGNORECASE),
        re.compile(r'worried\s*about\s*everything', re.IGNORECASE),
        re.compile(r'anxiety\s*is\s*consuming\s*me', re.IGNORECASE),
        re.compile(r'feel\s*like\s*I\s*can\'t\s*keep\s*up', re.IGNORECASE),
        re.compile(r'feel\s*like\s*I\s*can\'t\s*handle\s*anything', re.IGNORECASE),
        re.compile(r'feel\s*like\s*something\s*bad\s*is\s*going\s*to\s*happen', re.IGNORECASE),
        re.compile(r'feeling\s*really\s*down\s*because\s*of\s*anxiety', re.IGNORECASE),
        re.compile(r'anxiety\s*is\s*taking\s*over\s*my\s*life', re.IGNORECASE),
        re.compile(r'feeling\s*like\s*I\s*am\s*about\s*to\s*freak\s*out', re.IGNORECASE),
        re.compile(r'feeling\s*sick\s*from\s*anxiety', re.IGNORECASE),
        re.compile(r'anxiety\s*is\s*interfering\s*with\s*everything', re.IGNORECASE),
        re.compile(r'feel\s*so\s*overwhelmed\s*right\s*now', re.IGNORECASE),
        re.compile(r'feeling\s*paranoid', re.IGNORECASE),
        re.compile(r'feeling\s*uneasy\s*in\s*my\s*own\s*skin', re.IGNORECASE),
        re.compile(r'can\'t\s*stop\s*focusing\s*on\s*what\s*might\s*go\s*wrong', re.IGNORECASE),
        re.compile(r'my\s*anxiety\s*is\s*making\s*me\s*feel\s*ill', re.IGNORECASE),
        re.compile(r'feeling\s*afraid\s*to\s*be\s*alone', re.IGNORECASE),
        re.compile(r'feeling\s*like\s*everything\s*is\s*too\s*much', re.IGNORECASE),
        re.compile(r'my\s*heart\s*feels\s*heavy\s*from\s*anxiety', re.IGNORECASE),
        re.compile(r'can\'t\s*stop\s*shaking\s*from\s*anxiety', re.IGNORECASE),
        re.compile(r'feeling\s*like\s*I\s*can\'t\s*think\s*straight', re.IGNORECASE),
        re.compile(r'feeling\s*disconnected\s*from\s*reality', re.IGNORECASE),
        re.compile(r'anxiety\s*feels\s*like\s*I\s*am\s*trapped', re.IGNORECASE),
        re.compile(r'getting\s*anxiety\s*attacks\s*for\s*no\s*reason', re.IGNORECASE),
        re.compile(r'feel\s*like\s*I\s*can\'t\s*keep\s*it\s*together', re.IGNORECASE),
        re.compile(r'feeling\s*like\s*everyone\s*is\s*judging\s*me', re.IGNORECASE),
        re.compile(r'feeling\s*like\s*I\s*need\s*to\s*escape', re.IGNORECASE),
        re.compile(r'feeling\s*insecure\s*and\s*anxious', re.IGNORECASE),
        re.compile(r'feeling\s*panicked\s*without\s*warning', re.IGNORECASE),
        re.compile(r'anxiety\s*is\s*making\s*it\s*hard\s*to\s*concentrate', re.IGNORECASE),
        re.compile(r'feeling\s*disoriented\s*and\s*anxious', re.IGNORECASE),
        re.compile(r'anxiety\s*is\s*affecting\s*my\s*sleep', re.IGNORECASE),
        re.compile(r'feeling\s*hopeless\s*and\s*anxious', re.IGNORECASE),
        re.compile(r'anxiety\s*feels\s*like\s*a\s*heavy\s*burden', re.IGNORECASE),
        re.compile(r'feeling\s*like\s*I\s*can\'t\s*move\s*forward', re.IGNORECASE),
        re.compile(r'anxiety\s*is\s*affecting\s*my\s*relationships', re.IGNORECASE),
        re.compile(r'feeling\s*like\s*I\s*am\s*losing\s*my\s*mind', re.IGNORECASE),
        re.compile(r'feeling\s*exhausted\s*from\s*anxiety', re.IGNORECASE),
        re.compile(r'feeling\s*afraid\s*to\s*make\s*decisions', re.IGNORECASE),
        re.compile(r'getting\s*irritable\s*due\s*to\s*anxiety', re.IGNORECASE),
        re.compile(r'feeling\s*nervous\s*for\s*no\s*reason', re.IGNORECASE),
        re.compile(r'feeling\s*paralyzed\s*by\s*anxiety', re.IGNORECASE),
        re.compile(r'can\'t\s*control\s*my\s*thoughts', re.IGNORECASE),
        re.compile(r'feel\s*like\s*I\s*can\'t\s*escape\s*this\s*feeling', re.IGNORECASE),
        re.compile(r'feeling\s*panic\s*and\s*anxiety', re.IGNORECASE),
        re.compile(r'anxiety\s*feels\s*like\s*a\s*shadow', re.IGNORECASE),
        re.compile(r'anxiety\s*is\s*overpowering\s*me', re.IGNORECASE),
        re.compile(r'feeling\s*nervous\s*all\s*the\s*time', re.IGNORECASE),
        re.compile(r'feeling\s*hyperaware\s*of\s*everything', re.IGNORECASE),
    ],
    responses=[
        {
            "message": "I hear that you're feeling anxious. That must be really difficult.",
            "followup": "Can you tell me what triggered these feelings?",
            "techniques": ["deep breathing", "grounding exercises"]
        },
        {
            "message": "Anxiety can feel overwhelming, but you're not alone in this.",
            "followup": "What helps you feel calmer when anxiety hits?",
            "techniques": ["progressive muscle relaxation", "5-4-3-2-1 sensory exercise"]
        },
        {
            "message": "I'm really sorry you're feeling this way. It’s okay to not feel okay sometimes.",
            "followup": "Would you like to try some calming techniques together?",
            "techniques": ["guided meditation", "breathing exercises"]
        },
        {
            "message": "It’s normal to feel anxious sometimes, but I understand it can be very hard.",
            "followup": "Would you like some tips to help you manage this?",
            "techniques": ["mindfulness", "visualization techniques"]
        },
        {
            "message": "I can see that anxiety is affecting you deeply. You don’t have to go through this alone.",
            "followup": "Would you like to discuss how you're feeling a bit more?",
            "techniques": ["muscle relaxation", "journaling"]
        },
        {
            "message": "You're being so strong by talking about it. Anxiety can be tough to deal with.",
            "followup": "What has helped you in the past when you felt anxious?",
            "techniques": ["distraction techniques", "positive affirmations"]
        },
        {
            "message": "It's okay to acknowledge your anxiety. It doesn’t define you, though it can feel very overwhelming.",
            "followup": "Do you want some specific techniques to try right now?",
            "techniques": ["box breathing", "self-soothing techniques"]
        },
    ]
),

    MessagePattern(
        intent=MessageIntent.DEPRESSION,
        patterns=[
            re.compile(r'(feel(?:ing)?|am)\s*(very|really|so)?\s*(depressed|sad|down)', re.IGNORECASE),
            re.compile(r'(having|had)\s*(a)?\s*depression', re.IGNORECASE),
            re.compile(r'(my|the)\s*depression\s*(is|has been)', re.IGNORECASE),
            re.compile(r'can\'t\s*get\s*out\s*of\s*bed', re.IGNORECASE),
            re.compile(r'feel\s*hopeless', re.IGNORECASE),
        ],
        responses=[
            {
                "message": "I'm sorry you're feeling this way. Depression can be really tough.",
                "followup": "What has been on your mind lately?",
                "techniques": ["mindfulness meditation", "journaling your thoughts"]
            },
            {
                "message": "It sounds like you're going through a hard time. You're not alone.",
                "followup": "Is there something specific that's been bothering you?",
                "techniques": ["connecting with a loved one", "engaging in a small, enjoyable activity"]
            }
        ]
    ),
    MessagePattern(
        intent=MessageIntent.GRATITUDE,
        patterns=[
            re.compile(r'thank\s*you', re.IGNORECASE),
            re.compile(r'thanks', re.IGNORECASE),
            re.compile(r'appreciate\s*it', re.IGNORECASE),
            re.compile(r'grateful', re.IGNORECASE),
        ],
        responses=[
            "You're welcome! I'm glad I could help.",
            "No problem at all! Let me know if there's anything else I can do.",
            "It's my pleasure to support you. How are you feeling now?",
            "Thank you for sharing that with me. It means a lot."
        ]
    ),
    MessagePattern(
        intent=MessageIntent.CRISIS,
        patterns=[
            re.compile(r'suicid(?:e|al)', re.IGNORECASE),
            re.compile(r'kill\s*my\s*self', re.IGNORECASE),
            re.compile(r'want\s*to\s*die', re.IGNORECASE),
            re.compile(r'end\s*(?:it\s*all|my\s*life)', re.IGNORECASE),
            re.compile(r'can\'t\s*go\s*on', re.IGNORECASE),
        ],
        responses=[
            {
                "message": "I'm very concerned about what you're saying. Your life has value and there are people who want to help.",
                "followup": "Please reach out to a crisis counselor right now.",
                "resources": {
                    "crisis_line": "1-800-273-8255",
                    "crisis_text": "Text HOME to 741741",
                    "emergency": "911"
                }
            }
        ]
    ),
    MessagePattern(
        intent=MessageIntent.STRESS,
        patterns=[
            re.compile(r'(feel(?:ing)?|am)\s*(very|really|so)?\s*(stressed|overwhelmed)', re.IGNORECASE),
            re.compile(r'(having|had)\s*(a)?\s*stressful\s*(time|day|period)', re.IGNORECASE),
            re.compile(r'can\'t\s*handle\s*the\s*pressure', re.IGNORECASE),
            re.compile(r'too\s*much\s*on\s*my\s*plate', re.IGNORECASE),
        ],
        responses=[
            {
                "message": "Stress can be really overwhelming. Let's work through this together.",
                "followup": "What's been causing you the most stress lately?",
                "techniques": ["time management", "stress relief exercises"]
            }
        ]
    ),
    MessagePattern(
        intent=MessageIntent.LONELINESS,
        patterns=[
            re.compile(r'(feel(?:ing)?|am)\s*(very|really|so)?\s*(lonely|alone)', re.IGNORECASE),
            re.compile(r'no\s*one\s*understands', re.IGNORECASE),
            re.compile(r'feel\s*isolated', re.IGNORECASE),
            re.compile(r'no\s*friends', re.IGNORECASE),
        ],
        responses=[
            {
                "message": "Feeling lonely can be really difficult. I'm here to listen.",
                "followup": "Would you like to talk about what's making you feel this way?",
                "techniques": ["social connection activities", "community engagement"]
            }
        ]
    ),
    MessagePattern(
        intent=MessageIntent.ANGER,
        patterns=[
            re.compile(r'(feel(?:ing)?|am)\s*(very|really|so)?\s*(angry|mad|furious)', re.IGNORECASE),
            re.compile(r'lost\s*my\s*temper', re.IGNORECASE),
            re.compile(r'(want|feel\s*like)\s*to\s*break\s*something', re.IGNORECASE),
        ],
        responses=[
            {
                "message": "I can hear how angry you are. That's a very intense emotion to deal with.",
                "followup": "Would you like to talk about what's making you feel this way?",
                "techniques": ["anger management", "cooling down exercises"]
            }
        ]
    ),
    MessagePattern(
        intent=MessageIntent.SELF_CARE,
        patterns=[
            re.compile(r'need\s*to\s*take\s*care\s*of\s*myself', re.IGNORECASE),
            re.compile(r'how\s*to\s*relax', re.IGNORECASE),
            re.compile(r'self[\s-]care\s*tips', re.IGNORECASE),
        ],
        responses=[
            {
                "message": "Taking care of yourself is so important. Let's explore some self-care strategies.",
                "followup": "What kinds of activities help you feel refreshed?",
                "techniques": ["relaxation exercises", "self-care routines"]
            }
        ]
    ),
    MessagePattern(
        intent=MessageIntent.GENERAL,
        patterns=[
            re.compile(r'how\s*are\s*you', re.IGNORECASE),
            re.compile(r'what\'?s\s*up', re.IGNORECASE),
            re.compile(r'tell\s*me\s*something', re.IGNORECASE),
            re.compile(r'what\s*can\s*you\s*do', re.IGNORECASE),
        ],
        responses=[
            "I'm here to support you. How are you feeling today?",
            "I'm doing well, thank you for asking! How can I help you today?",
            "I can listen and offer support. What's on your mind?",
            "I'm here to help you navigate your emotions. What would you like to discuss?"
        ]
    ),
    MessagePattern(
        intent=MessageIntent.RELATIONSHIP,
        patterns=[
            re.compile(r'(feel(?:ing)?|am)\s*(very|really|so)?\s*(betrayed|hurt)\s*by\s*(partner|friend|family)', re.IGNORECASE),
            re.compile(r'breakup|divorce', re.IGNORECASE),
            re.compile(r'fight\s*with\s*(spouse|friend)', re.IGNORECASE),
            re.compile(r'no\s*one\s*understands\s*me', re.IGNORECASE),
            re.compile(r'conflict\s*with\s*(family|partner)', re.IGNORECASE),
        ],
        responses=[
            {
                "message": "It sounds like your relationships are weighing on you. That’s really tough.",
                "followup": "Can you share more about what happened?",
                "techniques": ["communication strategies", "journaling emotions"]
            }
        ]
    ),
    MessagePattern(
        intent=MessageIntent.GRIEF,
        patterns=[
            re.compile(r'(feel(?:ing)?|am)\s*(very|really|so)?\s*(heartbroken|sorrowful|devastated)', re.IGNORECASE),
            re.compile(r'loss\s*of\s*(loved\s*one|someone)', re.IGNORECASE),
            re.compile(r'mourning|grieving', re.IGNORECASE),
            re.compile(r'can\'t\s*move\s*on', re.IGNORECASE),
        ],
        responses=[
            {
                "message": "I’m so sorry for your loss. Grief can feel overwhelming.",
                "followup": "Would you like to talk about your loved one?",
                "techniques": ["grief journaling", "memorial activities"]
            }
        ]
    ),
    MessagePattern(
        intent=MessageIntent.SLEEP,
        patterns=[
            re.compile(r'can\'t\s*sleep|insomnia', re.IGNORECASE),
            re.compile(r'up\s*all\s*night', re.IGNORECASE),
            re.compile(r'trouble\s*(falling|staying)\s*asleep', re.IGNORECASE),
            re.compile(r'feeling\s*tired\s*all\s*the\s*time', re.IGNORECASE),
        ],
        responses=[
            {
                "message": "Sleep struggles can be exhausting. Let’s find ways to help.",
                "followup": "What’s been keeping you up?",
                "techniques": ["sleep hygiene tips", "relaxation exercises"]
            }
        ]
    ),
    # Update ANXIETY responses for personalization
    MessagePattern(
        intent=MessageIntent.ANXIETY,
        patterns=[...],  # Keep existing patterns
        responses=[
            {
                "message": "I hear you’re feeling {intensity_words} anxious{trigger? about {trigger}}. That’s really tough.",
                "followup": "Can you tell me what’s been triggering this?",
                "techniques": ["deep breathing", "grounding exercises"]
            },
            # Add more responses
        ]
    ),
    MessagePattern(
        intent=MessageIntent.UNKNOWN,
        patterns=[
            re.compile(r'.*', re.IGNORECASE),  # Catch-all pattern
        ],
        responses=[
            "I'm here to listen. Can you tell me more about what you're experiencing?",
            "That sounds challenging. Would you like to explore these feelings further?",
            "Thank you for sharing that with me. How can I best support you right now?"
        ]
    )
]

