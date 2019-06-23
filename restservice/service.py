import handlers
import inspect
import inflection
import logging
from aiohttp.web import middleware, Application, run_app, Request, Response, HTTPError, json_response
from marshmallow.exceptions import ValidationError
from json.decoder import JSONDecodeError
from restservice.handler import RESTHandler


class RESTService(Application):
    @middleware
    async def middleware(self, request: Request, handler) -> Response:
        try:
            return await handler(request)
        except Exception as exc:
            status = exc.status if hasattr(exc, 'status') else 400
            if isinstance(exc, (RuntimeError, TypeError)):
                logging.exception(exc)
                status = 500
            error = inflection.underscore(type(exc).__name__).upper()
            message = exc.message if hasattr(exc, 'message') else inflection.humanize(error).capitalize() + '.'
            detail = exc.detail if hasattr(exc, 'detail') else None
            if isinstance(exc, ValidationError):
                detail = exc.messages
            elif isinstance(exc, JSONDecodeError):
                detail = exc.msg
            return json_response(status=status, data=dict(error=error, message=message, detail=detail))

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
