from __future__ import absolute_import
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask


# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Set logger handler
handler = RotatingFileHandler('logs.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

from . import views, api