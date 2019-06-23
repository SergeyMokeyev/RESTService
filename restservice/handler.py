from abc import ABC, abstractmethod
from aiohttp.web import json_response, Request, Response


class RESTHandler(ABC):
    raw = False
    path = None
    method = None

    def __new__(cls, *args, **kwargs):
        assert isinstance(cls.path, str), 'Missing required attribute path, path must be string.'
        assert isinstance(cls.method, str), 'Missing required attribute method, method must be string.'
        __METHODS = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']
        assert cls.method in __METHODS, f'Attribute method must be one of {__METHODS}.'
        return super().__new__(cls)

    async def prepare(self, request: Request) -> Response:
        if self.raw:
            return await self.handler(request)

        data = await request.json()
        if hasattr(self, 'schema'):
            data = self.schema().load(data) if callable(self.schema) else self.schema.load(data)

        variables = dict(request.match_info)
        if variables:
            return json_response(await self.handler(data, **variables))
        return json_response(await self.handler(data))

    @abstractmethod
    async def handler(self, data, **kwargs):
        return data
