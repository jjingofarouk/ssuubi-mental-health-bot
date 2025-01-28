import logging
from flask.logging import default_handler

def setup_logger(app):
    logging.basicConfig(level=logging.INFO)
    app.logger.removeHandler(default_handler)
    handler = logging.FileHandler('app.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)