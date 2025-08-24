from logging.config import dictConfig
import os
from os import environ
from dotenv import load_dotenv, find_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
import certifi
#---------------------------------
# Default Config
#---------------------------------

# Loading secretes/variabels from .env file
load_dotenv(find_dotenv())

# APP_SECRET
SECRET_KEY = environ.get('SECRET_KEY')

# MongoDB setting
MONGODB_SETTINGS = {'DB':'LibM', 'host':environ.get('MONGO_URI'),'tlsCAFile':certifi.where()}

# Flask-WTF flag for CSRF
CSRF_ENABLED = environ.get('CSRF_ENABLED', True)

# debug mode
DEBUG = environ.get('DEBUG', False)

# # log level
LOG_LEVEL = environ.get('LOG_LEVEL', 'INFO')

#-----------------------------
