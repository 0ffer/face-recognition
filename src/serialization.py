
import base64

from flask.json import JSONEncoder

from src.models import User, Photo


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {
                'id': obj.id,
                'name': obj.name,
            }
        elif isinstance(obj, Photo):
            return {
                'id': obj.id,
                'user_id': obj.user_id,
                'data': base64.b64encode(obj.data).decode()
            }
        return super(CustomJSONEncoder, self).default(obj)
