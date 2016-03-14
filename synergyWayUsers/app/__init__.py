from __future__ import absolute_import

from flask import Flask

from . import views, api


# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the routes
app.add_url_rule('/', view_func=views.IndexView.as_view(name='index'))

# User API
app.add_url_rule('/api/users',
                 view_func=api.UserAPI.as_view(name='users'),
                 methods=['GET'])
app.add_url_rule('/api/users/<int:user_id>',
                 view_func=api.UserAPI.as_view(name='user'),
                 methods=['GET'])

# Course API
app.add_url_rule('/api/courses',
                 view_func=api.CourseAPI.as_view(name='course-list'),
                 methods=['GET'])

