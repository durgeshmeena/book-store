import logging
from flask import Flask
from flask.logging import default_handler
from flask_mongoengine import MongoEngine

app = Flask(__name__, static_url_path='', static_folder='static')
app.config.from_object('config')

# format logs
formatter = logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
# Remove default Flask handler and add custom handler
app.logger.removeHandler(default_handler)
app.logger.addHandler(handler)
app.logger.setLevel(app.config.get("LOG_LEVEL", logging.INFO))


app.logger.info("Configuration loaded.")
app.logger.info(f"Debug mode is {'on' if app.config['DEBUG'] else 'off'}.")

db = MongoEngine(app)


from app import views
