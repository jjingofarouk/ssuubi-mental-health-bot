import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'