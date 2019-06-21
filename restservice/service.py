import handlers
import inspect
from aiohttp.web import middleware, Application, run_app, json_response
from restservice.handler import RESTHandler
from restservice.exception import RESTError


class RESTService(Application):
    @middleware
    async def middleware(self, request, handler):
        try:
            return json_response(await handler(request))

        except RESTError as exc:
            return json_response(dict(error=exc.error, message=exc.message, detail=exc.detail))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, cls in inspect.getmembers(handlers, inspect.isclass):
            if issubclass(cls, RESTHandler):
                handler = cls()
                self.router.add_route(method=handler.method, path=handler.path, handler=handler.prepare)
        self.middlewares.append(self.middleware)

    def start(self):
        run_app(self)


if __name__ == '__main__':
    RESTService().start()
