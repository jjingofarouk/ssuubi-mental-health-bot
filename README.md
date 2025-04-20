Ssuubi Mental Health Chatbot
Ssuubi is a Flask-based mental health support chatbot designed to provide empathetic, intent-based responses to users experiencing mental health challenges. It features a dark-mode, teal-themed UI, in-memory storage for conversation context, and natural language processing for intent detection. The app supports intents like anxiety, depression, crisis, and sleep issues, with crisis mode responses including urgent resources. Built with Flask, Tailwind CSS, and Hugging Face models, Ssuubi operates without a database, making it lightweight for development.
Features
	•	Conversational AI: Responds to user messages with intent-based replies (e.g., ANXIETY, DEPRESSION, CRISIS, SLEEP_ISSUES) using mental_health_responses.json.
	•	Intent Detection: Uses regex patterns (patterns.py) and Hugging Face models (distilbert, all-MiniLM-L6-v2) to identify user intents and sentiments.
	•	Crisis Handling: Detects crisis messages (e.g., “I can’t go on”) and provides urgent resources (e.g., 988, Text HOME to 741741) with red-background UI alerts.
	•	In-Memory Storage: Stores conversation context in memory (context.py), eliminating database dependencies.
	•	Dark-Mode UI: Features a responsive, teal-accented (#10A37F) interface with a dark background (#202123) using Tailwind CSS and Font Awesome.
	•	Multilingual Support: Translates messages to English for processing using googletrans.
	•	Mood Check: Allows users to select moods (e.g., Good, Not Great) via buttons, triggering relevant bot responses.
	•	Session Management: Tracks user sessions with session_model.py and validates sessions with utils/helpers.py.
Repository
	•	GitHub: github.com/jjingofarouk-ssuubi-mental-health-bot
Tech Stack
	•	Backend: Flask (Python 3.12), googletrans, transformers, sentence-transformers
	•	Frontend: HTML, Tailwind CSS (v2.2.19), Font Awesome (v6.0.0), JavaScript
	•	Models: Hugging Face distilbert-base-uncased-finetuned-sst-2-english (~268 MB), all-MiniLM-L6-v2 (~90.9 MB)
	•	Total Size: ~341 MB (backend models), ~3 MB (frontend assets)
Project Structure
/workspaces/ssuubi-mental-health-bot/
├── app/
│   ├── models/
│   │   └── session_model.py       # Session management
│   ├── routes/
│   │   └── chat_routes.py         # /api/chat endpoint
│   ├── services/
│   │   ├── context.py             # In-memory context storage
│   │   ├── conversation_handler.py # Orchestrates message processing
│   │   ├── crisis_handler.py      # Crisis response logic
│   │   ├── intents.py             # MessageIntent enum
│   │   ├── message_analyzer.py     # Intent and sentiment analysis
│   │   ├── patterns.py            # Regex patterns for intent detection
│   │   ├── response_generator.py  # Generates responses from JSON
│   │   └── sentiment_analyzer.py  # Sentiment analysis
│   ├── utils/
│   │   └── helpers.py             # Session validation
│   └── templates/
│       └── index.html             # Dark-mode UI
├── mental_health_responses.json   # Response templates for intents
├── requirements.txt               # Python dependencies
└── app.py                         # Flask app entry point
Setup Instructions
	1	Clone the Repository: git clone https://github.com/jjingofarouk-ssuubi-mental-health-bot.git
	2	cd ssuubi-mental-health-bot
	3	
	4	Set Up Python Environment:
	◦	Requires Python 3.12.
	◦	Install dependencies: pip install -r requirements.txt
	◦	
	◦	Dependencies include flask, transformers, sentence-transformers, googletrans==3.1.0a0, torch.
	5	Ensure Models:
	◦	Hugging Face models (distilbert-base-uncased-finetuned-sst-2-english, all-MiniLM-L6-v2) are downloaded automatically by message_analyzer.py on first run (~341 MB).
	6	Verify JSON File:
	◦	Ensure mental_health_responses.json is at /workspaces/ssuubi-mental-health-bot/mental_health_responses.json.
	◦	Set permissions: chmod 644 /workspaces/ssuubi-mental-health-bot/mental_health_responses.json
	◦	
	◦	Contains response templates for GENERAL, ANXIETY, DEPRESSION, CRISIS, STRESS, GRIEF, SLEEP_ISSUES, WORK_ISSUES, FAMILY_ISSUES.
	7	Run the App: python app.py
	8	
	◦	Access the UI at http://127.0.0.1:5000/.
	◦	Test the API: curl -X POST http://127.0.0.1:5000/api/chat -H "Content-Type: application/json" -d '{"message":"I can’t sleep","session_id":"demo-session","user_id":"user123","language":"en"}'
	◦	
Usage
	•	UI: Open http://127.0.0.1:5000/ in a browser. Type messages in the input field or click mood buttons (e.g., 😴 Tired). The bot responds with empathetic messages, escalating to crisis resources for urgent inputs.
	•	API: Send POST requests to /api/chat with JSON: {
	•	  "message": "I’m anxious about work",
	•	  "session_id": "demo-session",
	•	  "user_id": "user123",
	•	  "language": "en"
	•	}
	•	
	◦	Response includes message, context (e.g., interaction_count, crisis_mode, previous_intent), and resources for crisis mode.
	•	Crisis Mode: Messages like “I can’t go on” trigger red-background responses with crisis hotlines (988, Text HOME to 741741, 911).
Key Files
	•	app.py: Flask app entry point, registers chat_routes.py, serves index.html.
	•	index.html: Dark-mode UI with sidebar, mood buttons, chat interface, and crisis resource footer. Uses Tailwind CSS and Font Awesome.
	•	chat_routes.py: Handles /api/chat POST requests, validates sessions, and returns JSON responses.
	•	conversation_handler.py: Orchestrates message processing, integrating message_analyzer.py, response_generator.py, and crisis_handler.py.
	•	context.py: In-memory storage for user context (e.g., intent, previous_intent, emotional_state).
	•	message_analyzer.py: Detects intents using regex (patterns.py) and sentiment (distilbert). Handles tokenizer warning (Hugging Face #31884) with clean_up_tokenization_spaces=False.
	•	patterns.py: Defines regex patterns for intents (e.g., \b(insomnia|can\'t sleep)\b for SLEEP_ISSUES).
	•	response_generator.py: Loads mental_health_responses.json and generates responses based on intent and context.
	•	intents.py: Defines MessageIntent enum (GENERAL, ANXIETY, DEPRESSION, CRISIS, STRESS, GRIEF, SLEEP_ISSUES, WORK_ISSUES, FAMILY_ISSUES).
	•	session_model.py: Manages session data and conversation history.
	•	utils/helpers.py: Provides validate_session for basic session validation.
	•	mental_health_responses.json: JSON file with response templates for each intent, supporting stages like validation_and_support, coping_strategies.
Testing
Run tests to verify intent detection, API responses, and UI integration:
pytest -v
Test Cases:
	•	test_chat_endpoint_anxiety: Ensures ANXIETY intent detection for “I’m very anxious about work”.
	•	test_chat_endpoint_sleep_issues: Verifies SLEEP_ISSUES intent for “I can’t sleep at night”.
	•	test_crisis_response: Confirms crisis mode for “I feel like I can’t go on” with resources.
	•	test_json_loading: Checks mental_health_responses.json loading.
	•	test_in_memory_context: Validates context storage for SLEEP_ISSUES.
	•	test_analyzer_sleep_issues: Ensures MessageAnalyzer detects SLEEP_ISSUES for “I have insomnia”.
Development Notes
	•	In-Memory Storage: Suitable for development. For production, consider SQLite for persistence.
	•	Crisis Resources: Configured for US hotlines (988, Text HOME to 741741, 911). Update chat_routes.py for region-specific numbers.
	•	UI: Responsive dark-mode design (#202123 background, #10A37F accent). Sidebar includes chat history, resources, and settings (placeholders).
	•	Error Handling:
	◦	Fixed MongoDB connection errors by using in-memory storage.
	◦	Resolved MessageIntent serialization (chat_routes.py, conversation_handler.py).
	◦	Handled ellipsis errors in patterns.py and message_analyzer.py.
	◦	Corrected missing SLEEP_ISSUES in intents.py.
	•	React Transition: Planned React integration (per April 13, 2025, Firebase discussions). Current HTML template is functional.
Known Issues
	•	Memory Usage: In-memory storage (context.py) may not scale for many users. Monitor in production.
	•	Session Validation: utils/helpers.py uses basic validation. Enhance with session age checks for production.
	•	Model Size: Hugging Face models (~341 MB) may be heavy for low-resource environments. Consider lighter models (e.g., distilbert-base-uncased).
Future Improvements
	•	Add SQLite for persistent context storage.
	•	Implement React frontend with TypeScript for enhanced UI (e.g., dynamic chat history).
	•	Refine regex patterns in patterns.py for multi-word phrases (e.g., “panic attack”).
	•	Persist user_id in index.html using localStorage.
	•	Expand mental_health_responses.json for sub-themes (e.g., panic under ANXIETY).
Contributing
	1	Fork the repository.
	2	Create a feature branch (git checkout -b feature-name).
	3	Commit changes (git commit -m "Add feature").
	4	Push to the branch (git push origin feature-name).
	5	Open a pull request.
License
MIT License. See LICENSE for details.
Contact
	•	GitHub Issues: github.com/jjingofarouk-ssuubi-mental-health-bot/issues
	•	Maintainer: jjingofarouk
Last Updated: April 20, 2025
