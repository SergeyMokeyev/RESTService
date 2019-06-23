from marshmallow import Schema, fields
from restservice.handler import RESTHandler


class Request(Schema):
    pass
    test = fields.Str(required=True)


class TestHandler(RESTHandler):
    schema = Request
    method = 'GET'
    path = r'/test/{user_id}'

    async def handler(self, data, user_id):
        print(user_id)
        print(data)
        return {'test': 'ok'}
