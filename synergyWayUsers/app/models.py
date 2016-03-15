import logging
from psycopg2._psycopg import DatabaseError, InternalError

from .db import connection
from . import app


logger = logging.getLogger(__name__)


class ModelError(Exception):
    def __init__(self, message, model):
        super(ModelError, self).__init__(message)

        self.model = model


class UserModel(object):
    def list(self, **kwargs):
        """
        Gets all records from Users table.
        :param kwargs: dict. Includes page to show,
         number of objects to retrieve (for pagination).
         Search query to filter users.
        :return: list of dicts.
        """
        cursor = connection.get_cursor()

        args = [
            kwargs.get('number'),
            kwargs.get('page'),
            kwargs.get('search_str')
        ]

        app.logger.info('Getting User list with args: {}'.format(
            kwargs
        ))

        try:
            cursor.callproc('public.fn_getuserdata', args)
        except (InternalError, DatabaseError) as exc:
            app.logger.info(exc.message)

            connection.db_connection.rollback()
            raise

        records = cursor.fetchall()

        return records

    def get_object(self, id):
        """
        Gets specified record from Users table.
        :param id: integer.
        :return: list.
        """
        if not id:
            raise ModelError('Provide object id.', self.__class__)

        cursor = connection.get_cursor()

        app.logger.info('Getting User object with Id: {}'.format(id))

        try:
            cursor.callproc('public.fn_getuserbyid', [id])
        except (InternalError, DatabaseError) as exc:
            app.logger.info(exc.message)

            connection.db_connection.rollback()
            raise

        records = cursor.fetchall()

        return records

    def update(self, id, data):
        """
        Update specified record in Users table with provided data.
        :param id: integer.
        :param data: dict. Fields with values to update object with.
        :return: boolean. If the record was updated.
        """
        if not id:
            raise ModelError('Provide object id.', UserModel)

        cursor = connection.get_cursor()

        app.logger.info('Updating User object with Id {0} and data: {1}'
                        .format(id, data))

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
        except (InternalError, DatabaseError) as exc:
            app.logger.info(exc.message)

            connection.db_connection.rollback()
            raise

        status = cursor.fetchone()

        return status.get('fn_updateuser', False)

    def delete(self, id):
        """
        Deletes specified record from Users table.
        :param id: integer.
        :return: integer. Number of affected rows.
        """
        if not id:
            raise ModelError('Provide object id.', UserModel)

        cursor = connection.get_cursor()

        app.logger.info('Deleting User object with Id {0}'.format(id))

        try:
            cursor.callproc("public.fn_deleteuser", [id])
        except (InternalError, DatabaseError) as exc:
            app.logger.info(exc.message)

            connection.db_connection.rollback()
            raise

        affected_row = cursor.fetchone()

        return affected_row.get('fn_deleteuser', 0)

    def create(self, data):
        """
        Create record in Users table with provided data.
        :param data: dict. Fields with values to create object with.
        :return: boolean. If record was created.
        """
        cursor = connection.get_cursor()

        app.logger.info('Creating User object with data: {1}'.format(data))

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
        except (InternalError, DatabaseError) as exc:
            app.logger.info(exc.message)

            connection.db_connection.rollback()
            raise

        status = cursor.fetchone()

        return status.get('fn_createuser', False)


class CourseModel(object):
    def list(self, *args, **kwargs):
        """
        Gets all records from Course table.
        :return: list of dicts.
        """
        cursor = connection.get_cursor()

        app.logger.info('Getting Course list.')

        try:
            cursor.callproc('public.fn_getcoursedata')
        except (InternalError, DatabaseError) as exc:
            app.logger.info(exc.message)

            connection.db_connection.rollback()
            raise

        records = cursor.fetchall()

        return records
