from marshmallow import Schema, fields
from restservice import RESTError, RESTHandler


class Request(Schema):
    pass


class TestHandler(RESTHandler):
    schema = Request
    method = 'GET'
    path = '/test'

    async def handler(self, data):
        raise RESTError('TEST_ERROR', 'Test error message')
        return {'test': 'ok'}
