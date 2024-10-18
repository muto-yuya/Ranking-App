"""Dev config file"""

import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = "sqlite:///sample_flask.db"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = os.urandom(32)
