from copy import deepcopy


class UserSerializer(object):
    def __init__(self, data):
        self.data = data

    def serialize_object(self):
        result = deepcopy(self.data[0])
        print self.data
        del result['course_id']
        del result['course_name']
        del result['course_code']

        result['courses'] = [
            {
                'id': obj['course_id'],
                'name': obj['course_name'],
                'code': obj['course_code']
            } for obj in self.data
        ]

        return result
