from flask import json, abort, request
from flask.views import MethodView

from . import models, serializers


class UserAPI(MethodView):
    def __init__(self):
        self.user_model = models.UserModel()

    def get(self, user_id=None):
        page = request.args.get('page', 1)
        number = request.args.get('number', 15)

        if user_id is None:
            try:
                users = self.user_model.get_all(page=page, number=number)
                return json.dumps(users)
            except Exception:
                abort(500)
        else:
            try:
                user = self.user_model.get_object(user_id)
                serializer = serializers.UserSerializer(user)
                user = serializer.serialize_object()
                if not user:
                    abort(404)
                return json.dumps(user)
            except Exception as exc:
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
            courses = self.course_model.get_all()
            return json.dumps(courses)
        except Exception:
            abort(500)


