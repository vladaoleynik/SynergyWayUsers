from flask import render_template
from flask.views import View

from . import app


class IndexView(View):
    def dispatch_request(self):
        return render_template('index.html')


# Define the routes
app.add_url_rule('/', view_func=IndexView.as_view(name='index'))
