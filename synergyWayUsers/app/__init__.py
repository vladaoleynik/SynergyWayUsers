from __future__ import absolute_import

from flask import Flask

from . import views


# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the routes
app.add_url_rule('/', view_func=views.IndexView.as_view(name='index'))
