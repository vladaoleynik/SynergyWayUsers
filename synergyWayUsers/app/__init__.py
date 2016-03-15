from __future__ import absolute_import

from flask import Flask


# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

from . import views, api