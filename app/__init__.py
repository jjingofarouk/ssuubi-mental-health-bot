from flask import Flask
from .routes.chat_routes import chat_bp
from .routes.home_routes import home_bp
from .utils.logger import setup_logger
from .utils.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Setup logger
    setup_logger(app)
    
    # Register blueprints
    app.register_blueprint(chat_bp)
    app.register_blueprint(home_bp)
    
    return app