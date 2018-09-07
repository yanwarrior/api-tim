import json
from copy import copy


def json_parser(request):
    request = copy(request)
    return json.loads(request.body.decode('utf-8'))

