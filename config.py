import os
from os import environ

import certifi
from dotenv import find_dotenv, load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

# ---------------------------------
# Default Config
# ---------------------------------

# Loading secretes/variabels from .env file
load_dotenv(find_dotenv())

# APP_SECRET
SECRET_KEY = environ.get("SECRET_KEY")

# MongoDB setting
MONGODB_SETTINGS = {
    "DB": "LibM",
    "host": environ.get("MONGO_URI"),
    "tlsCAFile": certifi.where(),
}

# Flask-WTF flag for CSRF
CSRF_ENABLED = environ.get("CSRF_ENABLED", True)

# debug mode
DEBUG = environ.get("DEBUG", False)

# # log level
LOG_LEVEL = environ.get("LOG_LEVEL", "INFO")

# -----------------------------
