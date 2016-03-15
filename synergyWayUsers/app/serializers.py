class UserSerializer(object):
    def __init__(self, data):
        self.data = data

    def serialize_object(self):
        user = self.data[0]
        result = {}

        for name, value in user.iteritems():
            if 'course_' not in name:
                result[name] = value

        result['courses'] = [
            {
                'course_id': obj['course_id'],
                'name': obj['course_name'],
                'code': obj['course_code']
            } for obj in self.data
        ]

        return result

    def serialize_list(self):
        single_user = self.data[0]

        return {
            'count': single_user.get('full_count', 0),
            'data': self.data
        }
