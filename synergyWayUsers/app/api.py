from flask import json, abort, request
from flask.views import MethodView

from . import models


class UserAPI(MethodView):
    def __init__(self):
        self.user_model = models.UserModel()

    def get(self, user_id=None):
        page = request.args.get('page', 1)
        number = request.args.get('number', 15)

        if user_id is None:
            try:
                users = self.user_model.get_users(page=page, number=number)
                return json.dumps(users)
            except Exception:
                abort(500)

        return

    def post(self):
      pass

    def delete(self, user_id):
      pass

    def put(self, user_id):
      pass


class CourseAPI(MethodView):
    def __init__(self):
        self.course_model = models.CourseModel()

    def get(self):
        try:
            courses = self.course_model.get_courses()
            return json.dumps(courses)
        except Exception:
            abort(500)


