import logging
import psycopg2
import psycopg2.extras

from flask import current_app

from . import app

logger = logging.getLogger(__name__)


class Connection(object):
    def __init__(self):
        self.db_connection = None
        self.cursor = None

    def get_cursor(self, cursor_factory=None):
        if not cursor_factory:
            cursor_factory = psycopg2.extras.RealDictCursor

        if not self.db_connection:
            self.get_db_connection()

        return self.db_connection.cursor(cursor_factory=cursor_factory)

    def get_db_connection(self):
        try:
            self.db_connection = psycopg2.connect(
                database=current_app.config['DB_NAME'],
                user=current_app.config['DB_USER'],
                password=current_app.config['DB_PASS'],
                host=current_app.config['DB_HOST'],
                port=current_app.config['DB_PORT']
            )
            app.logger.info('Opened database successfully.')
        except psycopg2.DatabaseError as e:
            app.logger.info('Error {0}.'.format(e))
            return


connection = Connection()
