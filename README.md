# Ssuubi Mental Health Chatbot

Ssuubi is a Flask-based mental health support chatbot designed to provide empathetic, intent-based responses to users experiencing mental health challenges. It features a dark-mode, teal-themed UI, in-memory storage for conversation context, and natural language processing for intent detection. The app supports intents like anxiety, depression, crisis, and sleep issues, with crisis mode responses including urgent resources. Built with Flask, Tailwind CSS, and Hugging Face models, Ssuubi operates without a database, making it lightweight for development.

## Features

- **Conversational AI**: Responds to user messages with intent-based replies (e.g., `ANXIETY`, `DEPRESSION`, `CRISIS`, `SLEEP_ISSUES`) using `mental_health_responses.json`.
- **Intent Detection**: Uses regex patterns (`patterns.py`) and Hugging Face models (`distilbert`, `all-MiniLM-L6-v2`) to identify user intents and sentiments.
- **Crisis Handling**: Detects crisis messages (e.g., “I can’t go on”) and provides urgent resources (e.g., 988, Text HOME to 741741) with red-background UI alerts.
- **In-Memory Storage**: Stores conversation context in memory (`context.py`), eliminating database dependencies.
- **Dark-Mode UI**: Features a responsive, teal-accented (`#10A37F`) interface with a dark background (`#202123`) using Tailwind CSS and Font Awesome.
- **Multilingual Support**: Translates messages to English for processing using `googletrans`.
- **Mood Check**: Allows users to select moods (e.g., Good, Not Great) via buttons, triggering relevant bot responses.
- **Session Management**: Tracks user sessions with `session_model.py` and validates sessions with `utils/helpers.py`.

## Repository

- GitHub: [github.com/jjingofarouk-ssuubi-mental-health-bot](https://github.com/jjingofarouk-ssuubi-mental-health-bot)

## Tech Stack

- **Backend**: Flask (Python 3.12), `googletrans`, `transformers`, `sentence-transformers`
- **Frontend**: HTML, Tailwind CSS (v2.2.19), Font Awesome (v6.0.0), JavaScript
- **Models**:
  - `distilbert-base-uncased-finetuned-sst-2-english` (~268 MB)
  - `all-MiniLM-L6-v2` (~90.9 MB)
- **Total Size**: ~341 MB (backend models), ~3 MB (frontend assets)

## Project Structure

/workspaces/ssuubi-mental-health-bot/
├── app/
│   ├── models/
│   │   └── session_model.py
│   ├── routes/
│   │   └── chat_routes.py
│   ├── services/
│   │   ├── context.py
│   │   ├── conversation_handler.py
│   │   ├── crisis_handler.py
│   │   ├── intents.py
│   │   ├── message_analyzer.py
│   │   ├── patterns.py
│   │   ├── response_generator.py
│   │   └── sentiment_analyzer.py
│   ├── utils/
│   │   └── helpers.py
│   └── templates/
│       └── index.html
├── mental_health_responses.json
├── requirements.txt
└── app.py

## Setup Instructions

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/jjingofarouk-ssuubi-mental-health-bot.git
   cd ssuubi-mental-health-bot

	2.	Set Up Python Environment
	•	Requires Python 3.12.
	•	Install dependencies:

pip install -r requirements.txt


	•	Dependencies include Flask, transformers, sentence-transformers, googletrans==3.1.0a0, torch.

	3.	Ensure Models
	•	Hugging Face models (distilbert-base-uncased-finetuned-sst-2-english, all-MiniLM-L6-v2) are downloaded automatically by message_analyzer.py on first run (~341 MB).
	4.	Verify JSON File
	•	Ensure mental_health_responses.json is at /workspaces/ssuubi-mental-health-bot/mental_health_responses.json.
	•	Set permissions:

chmod 644 /workspaces/ssuubi-mental-health-bot/mental_health_responses.json


	•	Contains response templates for GENERAL, ANXIETY, DEPRESSION, CRISIS, STRESS, GRIEF, SLEEP_ISSUES, WORK_ISSUES, FAMILY_ISSUES.

	5.	Run the App

python app.py



	•	Access the UI at: http://127.0.0.1:5000/
	•	Test the API:

curl -X POST http://127.0.0.1:5000/api/chat \
-H "Content-Type: application/json" \
-d '{"message":"I can’t sleep","session_id":"demo-session","user_id":"user123","language":"en"}'



Usage

	•	UI: Open http://127.0.0.1:5000/ in a browser. Type messages in the input field or click mood buttons (e.g., 😴 Tired). The bot responds with empathetic messages, escalating to crisis resources for urgent inputs.
	•	API: Send POST requests to /api/chat with JSON:

{
  "message": "I’m anxious about work",
  "session_id": "demo-session",
  "user_id": "user123",
  "language": "en"
}


	•	Response includes message, context (e.g., interaction_count, crisis_mode, previous_intent), and crisis resources if applicable.
	•	Crisis Mode: Messages like “I can’t go on” trigger red-background responses with crisis hotlines (988, Text HOME to 741741, 911).

Key Files

	•	app.py: Flask app entry point, registers chat_routes.py, serves index.html.
	•	index.html: Dark-mode UI with sidebar, mood buttons, chat interface, and crisis resource footer.
	•	chat_routes.py: Handles /api/chat POST requests, validates sessions, and returns JSON responses.
	•	conversation_handler.py: Integrates message analysis and crisis handling logic.
	•	context.py: In-memory storage for user context.
	•	message_analyzer.py: Detects intents using regex (patterns.py) and sentiment (distilbert).
	•	patterns.py: Defines regex patterns for intents.
	•	response_generator.py: Loads mental_health_responses.json and generates responses.
	•	intents.py: Defines MessageIntent enum.
	•	session_model.py: Manages session data and history.
	•	utils/helpers.py: Provides validate_session for session validation.
	•	mental_health_responses.json: JSON file with structured responses for various intents.

Testing

Run tests to verify intent detection, API responses, and UI integration:

pytest -v

Test Cases

	•	test_chat_endpoint_anxiety: Detects ANXIETY for “I’m very anxious about work”.
	•	test_chat_endpoint_sleep_issues: Detects SLEEP_ISSUES for “I can’t sleep at night”.
	•	test_crisis_response: Confirms crisis mode for “I feel like I can’t go on”.
	•	test_json_loading: Checks response JSON loading.
	•	test_in_memory_context: Validates context.py logic.
	•	test_analyzer_sleep_issues: Ensures analyzer detects SLEEP_ISSUES.

Development Notes

	•	In-Memory Storage: Suitable for development. Consider SQLite for production.
	•	Crisis Resources: US-based (988, Text HOME to 741741, 911). Modify for regional needs.
	•	UI: Dark-mode (#202123), teal-accent (#10A37F). Sidebar includes placeholders for future features.
	•	Error Handling:
	•	Switched from MongoDB to in-memory storage.
	•	Resolved MessageIntent serialization issues.
	•	Handled tokenization warnings (Hugging Face #31884).
	•	Fixed missing intents in intents.py.
	•	React Transition: Planned React + Firebase integration (as of April 13, 2025). Current UI is HTML-based.

Known Issues

	•	Memory Usage: In-memory storage may not scale for many users.
	•	Session Validation: Basic validation. Consider session expiration logic.
	•	Model Size: Large models may be unsuitable for low-resource environments.

Future Improvements

	•	Add SQLite for persistent session/context storage.
	•	Implement React frontend with TypeScript.
	•	Improve regex pattern matching in patterns.py.
	•	Use localStorage to persist user_id.
	•	Expand mental_health_responses.json for sub-themes like panic.

Contributing

	1.	Fork the repository.
	2.	Create a feature branch:

git checkout -b feature-name


	3.	Commit your changes:

git commit -m "Add feature"


	4.	Push to GitHub:

git push origin feature-name


	5.	Open a pull request.

License

MIT License. See LICENSE for details.

Contact

	•	GitHub Issues: github.com/jjingofarouk-ssuubi-mental-health-bot/issues
	•	Maintainer: jjingofarouk

Last Updated: April 20, 2025

