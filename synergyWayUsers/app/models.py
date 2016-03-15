import logging
from psycopg2._psycopg import DatabaseError, InternalError

from .db import connection


logger = logging.getLogger(__name__)


class ModelError(Exception):
    def __init__(self, message, model):
        super(ModelError, self).__init__(message)

        self.model = model


class BaseModel(object):
    _all_proc_name = None
    _one_proc_name = None
    _paginated = True

    def get_all(self, *args, **kwargs):
        if self._all_proc_name is None:
            raise NotImplementedError('_all_proc_name must be overriden!')

        cursor = connection.get_cursor()

        args = [kwargs.get('number'),
                kwargs.get('page'),
                kwargs.get('search_str')]

        try:
            cursor.callproc(self._all_proc_name, args)
        except (InternalError, DatabaseError):
            connection.db_connection.rollback()
            raise

        records = cursor.fetchall()

        return records

    def get_object(self, id):
        if self._one_proc_name is None:
            raise NotImplementedError('_one_proc_name must be overriden!')

        cursor = connection.get_cursor()

        try:
            cursor.callproc(self._one_proc_name, [id])
        except (InternalError, DatabaseError):
            connection.db_connection.rollback()
            raise

        records = cursor.fetchall()

        return records


class UserModel(BaseModel):
    _all_proc_name = 'public.fn_getuserdata'
    _one_proc_name = 'public.fn_getuserbyid'

    def update_object(self, id, data):
        if not id:
            raise ModelError('Provide object id.', UserModel)

        cursor = connection.get_cursor()

        try:
            cursor.callproc(
                "public.fn_updateuser", [
                    data.get('user_id'),
                    data.get('name'),
                    data.get('email'),
                    data.get('mobile'),
                    data.get('phone'),
                    data.get('status'),
                    data.get('course_ids')
                ]
            )
        except (InternalError, DatabaseError):
            connection.db_connection.rollback()
            raise

        status = cursor.fetchone()

        return status.get('fn_updateuser', False)

    def delete_object(self, id):
        if not id:
            raise ModelError('Provide object id.', UserModel)

        cursor = connection.get_cursor()

        try:
            cursor.callproc("public.fn_deleteuser", [id])
        except (InternalError, DatabaseError):
            connection.db_connection.rollback()
            raise

        affected_row = cursor.fetchone()

        return affected_row.get('fn_deleteuser', 0)

    def create_object(self, data):
        cursor = connection.get_cursor()

        try:
            cursor.callproc(
                "public.fn_createuser", [
                    data.get('name'),
                    data.get('email'),
                    data.get('mobile'),
                    data.get('phone'),
                    data.get('status'),
                    data.get('course_ids')
                ]
            )
        except (InternalError, DatabaseError):
            connection.db_connection.rollback()
            raise

        status = cursor.fetchone()

        return status.get('fn_createuser', False)


class CourseModel(BaseModel):
    _all_proc_name = 'public.fn_getcoursedata'
