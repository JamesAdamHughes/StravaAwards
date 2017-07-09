from flask.json import JSONEncoder
from datetime import datetime
import arrow

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            print obj
            if isinstance(obj, datetime):
                return arrow.get(obj).for_json()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)