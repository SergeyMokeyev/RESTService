import os
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp.web import json_response, Response, Request
from restservice import RESTService, RESTConfig, RESTHandler, RESTError
from marshmallow import Schema, fields


class TestSchema(Schema):
    a = fields.Int(required=True)
    b = fields.Str(required=True)


class TestConfig(RESTConfig):
    TEST_PARAM: str


class TestHandler(RESTHandler):
    async def get(self):
        if self.request.query:
            return json_response(dict(self.request.query), status=202)
        return json_response(self.request.match_info)

    async def post(self):
        request = TestSchema().load(await self.request.json())
        return json_response(request, status=201)

    async def put(self):
        return json_response({self.config.ENVIRONMENT: self.config.TEST_PARAM})

    async def delete(self):
        if self.request.match_info['name'] == 'bob':
            raise RESTError(
                error='TEST_ERROR',
                message='Test message.',
                detail=None,
                status=500
            )
        raise RuntimeError


class MyAppTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = RESTService()
        app.config = TestConfig(f'{os.path.dirname(os.path.abspath(__file__))}/test_config.yaml')
        app.router.add_view(r'/test', TestHandler)
        app.router.add_view(r'/test/{name}', TestHandler)

        return app

    @unittest_run_loop
    async def test_valid_request(self):
        resp = await self.client.request('GET', '/test?a=1&b=2')
        assert resp.status == 202
        assert await resp.json() == {'a': '1', 'b': '2'}

        resp = await self.client.request('GET', '/test/bob')
        assert resp.status == 200
        assert await resp.json() == {'name': 'bob'}

        resp = await self.client.request('POST', '/test/bob', json={'a': 1, 'b': 'string'})
        assert resp.status == 201
        assert await resp.json() == {'a': 1, 'b': 'string'}

    @unittest_run_loop
    async def test_config_env(self):
        os.environ['ENVIRONMENT'] = ''
        self.app.config = TestConfig(f'{os.path.dirname(os.path.abspath(__file__))}/test_config.yaml')
        resp = await self.client.request('PUT', '/test/bob')
        assert await resp.json() == {'DEFAULT': 'test'}

        os.environ['ENVIRONMENT'] = 'dev'
        self.app.config = TestConfig(f'{os.path.dirname(os.path.abspath(__file__))}/test_config.yaml')
        resp = await self.client.request('PUT', '/test/bob')
        assert await resp.json() == {'DEV': 'test'}

        os.environ['ENVIRONMENT'] = 'prod'
        self.app.config = TestConfig(f'{os.path.dirname(os.path.abspath(__file__))}/test_config.yaml')
        resp = await self.client.request('PUT', '/test/bob')
        assert await resp.json() == {'PROD': 'prod'}

    @unittest_run_loop
    async def test_invalid_request(self):
        resp = await self.client.request('POST', '/test/bob')
        assert resp.status == 400
        assert await resp.json() == {
            'error': 'JSON_DECODE_ERROR',
            'message': 'Json decode error.',
            'detail': 'Expecting value'
        }

        resp = await self.client.request('POST', '/404')
        assert resp.status == 404
        assert await resp.json() == {
            'error': 'HTTP_NOT_FOUND',
            'message': 'Http not found.',
            'detail': None
        }

        resp = await self.client.request('POST', '/test', json={'a': 'string'})
        assert resp.status == 400
        assert await resp.json() == {
            'error': 'VALIDATION_ERROR',
            'message': 'Validation error.',
            'detail': {
                'b': ['Missing data for required field.'],
                'a': ['Not a valid integer.']
            }
        }

        resp = await self.client.request('DELETE', '/test/bob')
        assert resp.status == 500
        assert await resp.json() == {
            'error': 'TEST_ERROR',
            'message': 'Test message.',
            'detail': None
        }

        resp = await self.client.request('DELETE', '/test/not_bob')
        assert resp.status == 500
        assert await resp.json() == {
            'error': 'RUNTIME_ERROR',
            'message': 'Runtime error.',
            'detail': None
        }
