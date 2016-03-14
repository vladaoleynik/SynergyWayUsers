import psycopg2
import psycopg2.extras
import logging

from flask import Flask, current_app

from .decorators import singleton

logger = logging.getLogger(__name__)


@singleton
class BaseModel(object):
    def __init__(self):
        self.db_connection = None
        self.cursor = None

    def get_db_connection(self):
        try:
            self.db_connection = psycopg2.connect(
                database=current_app.config['DB_NAME'],
                user=current_app.config['DB_USER'],
                password=current_app.config['DB_PASS'],
                host=current_app.config['DB_HOST'],
                port=current_app.config['DB_PORT']
            )
            logger.debug('Opened database successfully')
        except psycopg2.DatabaseError as e:
            logger.debug('Error {0}'.format(e))

        return self.db_connection


class UserModel(object):
    def get_users(self, page=1, number=15):
        conn = BaseModel().get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.callproc("public.fn_getuserdata", [number, page])

        records = cursor.fetchall()

        return records


class CourseModel(object):
    def get_courses(self):
        conn = BaseModel().get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.callproc("public.fn_getcoursedata")

        records = cursor.fetchall()

        return records
