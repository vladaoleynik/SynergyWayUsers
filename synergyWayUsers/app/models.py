import logging
from psycopg2._psycopg import DatabaseError, InternalError

from .db import connection


logger = logging.getLogger(__name__)


class BaseModel(object):
    __all_proc_name__ = None
    __one_proc_name__ = None
    __paginated__ = True

    def get_all(self, *args, **kwargs):
        if self.__all_proc_name__ is None:
            raise NotImplementedError('__all_proc_name__ must be overriden!')

        cursor = connection.get_cursor()

        try:
            cursor.callproc(self.__all_proc_name__, list(args))
        except (InternalError, DatabaseError):
            connection.db_connection.rollback()
            return None

        records = cursor.fetchall()

        return records

    def get_object(self, id):
        if self.__one_proc_name__ is None:
            raise NotImplementedError('__one_proc_name__ must be overriden!')

        cursor = connection.get_cursor()

        try:
            cursor.callproc(self.__one_proc_name__, [id])
        except (InternalError, DatabaseError):
            connection.db_connection.rollback()
            return None

        records = cursor.fetchall()

        return records


class UserModel(BaseModel):
    __all_proc_name__ = 'public.fn_getuserdata'
    __one_proc_name__ = 'public.fn_getuserbyid'

    def update_object(self, id, data):
        if not id:
            return

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
            return None

        records = cursor.fetchone()

        return records

    def delete_object(self, id):
        if not id:
            return

        cursor = connection.get_cursor()

        try:
            cursor.callproc("public.fn_deleteuser", [id])
        except (InternalError, DatabaseError):
            connection.db_connection.rollback()
            return None

        status = cursor.fetchone()

        return status


class CourseModel(BaseModel):
    __all_proc_name__ = 'public.fn_getcoursedata'
