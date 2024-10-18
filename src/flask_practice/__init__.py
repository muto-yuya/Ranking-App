"""Ranking website.

initiating flask.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)
from .models import ranking  # noqa: E402, I001

import flask_practice.views  # noqa: E402
