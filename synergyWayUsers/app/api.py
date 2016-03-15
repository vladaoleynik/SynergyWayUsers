from psycopg2._psycopg import DatabaseError, InternalError

from flask import json, abort, request, make_response, jsonify
from flask.views import MethodView

from . import models, serializers, app


@app.errorhandler(500)
@app.errorhandler(404)
def not_found(error):
    return make_response(
        jsonify({
            'status': 'error',
            'error': 'Not found'
        }), 404
    )


class UserAPI(MethodView):
    def __init__(self):
        self.user_model = models.UserModel()

    def get(self, user_id=None):
        page = request.args.get('page', 1)
        number = request.args.get('number', 15)
        search_str = request.args.get('search_str')

        if user_id is None:
            users = self.user_model.get_all(
                page=page, number=number, search_str=search_str
            )
            return json.dumps(users)

        user = self.user_model.get_object(user_id)
        if not user:
            abort(404)

        serializer = serializers.UserSerializer(user)
        user = serializer.serialize_object()

        return json.dumps(user)

    def put(self, user_id):
        if not user_id:
            abort(404)

        if not request.json:
            abort(400)

        updated = self.user_model.update_object(user_id, request.json)
        if not updated:
            abort(500)

        return jsonify({
            'status': 'success'
        })

    def delete(self, user_id):
        if not user_id:
            abort(404)

        deleted_rows = self.user_model.delete_object(user_id)
        if not deleted_rows:
            abort(500)

        return jsonify({
            'status': 'success'
        })

    def post(self):
        if not request.json:
            abort(400)

        created = self.user_model.create_object(request.json)
        if not created:
            abort(500)

        return jsonify({
            'status': 'success'
        }), 201


class CourseAPI(MethodView):
    def __init__(self):
        self.course_model = models.CourseModel()

    def get(self):
        courses = self.course_model.get_all()
        if not courses:
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



