import logging

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

        cursor.callproc(self.__all_proc_name__, list(args))

        records = cursor.fetchall()

        return records

    def get_object(self, id):
        if self.__one_proc_name__ is None:
            raise NotImplementedError('__one_proc_name__ must be overriden!')

        cursor = connection.get_cursor()

        cursor.callproc(self.__one_proc_name__, [id])

        records = cursor.fetchall()

        return records


class UserModel(BaseModel):
    __all_proc_name__ = 'public.fn_getuserdata'
    __one_proc_name__ = 'public.fn_getuserbyid'


class CourseModel(BaseModel):
    __all_proc_name__ = 'public.fn_getcoursedata'
