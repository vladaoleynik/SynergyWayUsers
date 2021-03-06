from psycopg2._psycopg import DatabaseError, InternalError

from flask import json, abort, request, make_response, jsonify
from flask.views import MethodView

from . import models, serializers, app
from .models import ModelError


@app.errorhandler(404)
def not_found(error):
    return make_response(
        jsonify({
            'status': 'error',
            'error': 'Not found'
        }), 404
    )


@app.errorhandler(500)
def internal_error(error):
    return make_response(
        jsonify({
            'status': 'error',
            'error': 'Internal error'
        }), 500
    )


class UserAPI(MethodView):
    def __init__(self):
        self.user_model = models.UserModel()

    def get(self, user_id=None):
        """
        GET method to return data for all users or for concrete one.
        :param user_id: int
        :return: JSON array or object
        """
        page = request.args.get('page', 1)
        number = request.args.get('number', 15)
        search_str = request.args.get('search_str')

        if user_id is None:
            # Need to retrieve all users from DB
            users = []

            try:
                users = self.user_model.list(
                    page=page, number=number, search_str=search_str
                )
            except (ModelError, DatabaseError, InternalError):
                abort(500)

            serializer = serializers.UserSerializer(users)
            users = serializer.serialize_list()

            return jsonify(users)

        user = None
        try:
            user = self.user_model.get_object(user_id)
        except (ModelError, DatabaseError, InternalError):
            abort(500)

        if not user:
            abort(404)

        serializer = serializers.UserSerializer(user)
        user = serializer.serialize_object()

        return jsonify(user)

    def put(self, user_id):
        """
        PUT method to update data for user.
        :param user_id: int
        :return: JSON object with status
        """
        if not user_id:
            abort(404)

        if not request.json:
            abort(400)

        updated = None
        try:
            updated = self.user_model.update(user_id, request.json)
        except (ModelError, DatabaseError, InternalError):
            abort(500)

        if not updated:
            abort(500)

        return jsonify({
            'status': 'success'
        })

    def delete(self, user_id):
        """
        DELETE method to delete user.
        :param user_id: int
        :return: JSON object with status
        """
        if not user_id:
            abort(404)

        deleted_rows = None
        try:
            deleted_rows = self.user_model.delete(user_id)
        except (ModelError, DatabaseError, InternalError):
            abort(500)

        if not deleted_rows:
            abort(500)

        return jsonify({
            'status': 'success'
        })

    def post(self):
        """
        POST method to create user.
        :return: JSON object with status
        """
        if not request.json:
            abort(400)

        created = None
        try:
            created = self.user_model.create(request.json)
        except (ModelError, DatabaseError, InternalError):
            abort(500)

        if not created:
            abort(500)

        return jsonify({
            'status': 'success'
        }), 201


class CourseAPI(MethodView):
    def __init__(self):
        self.course_model = models.CourseModel()

    def get(self):
        """
        GET method to return data for all courses.
        :return: JSON array
        """
        courses = []
        try:
            courses = self.course_model.list()
        except (ModelError, DatabaseError, InternalError):
            abort(500)

        if courses is None:
            abort(500)

        return json.dumps(courses)


# User API
user_view = UserAPI.as_view('user_api')
app.add_url_rule('/api/users',
                 view_func=user_view,
                 methods=['GET', 'POST'])
app.add_url_rule('/api/users/<int:user_id>',
                 view_func=user_view,
                 methods=['GET', 'PUT', 'DELETE'])

# Course API
course_view = CourseAPI.as_view('course_api')
app.add_url_rule('/api/courses',
                 view_func=course_view,
                 methods=['GET'])



