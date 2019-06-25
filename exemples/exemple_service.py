from aiohttp.web import json_response, RouteTableDef
from restservice import RESTError, RESTService, RESTConfig, RESTHandler


routes = RouteTableDef()


class Config(RESTConfig):
    DB: str


@routes.view(r'/test/{user_id}')
class TestHandler(RESTHandler):
    async def get(self):
        user_id = self.request.match_info.get('user_id')
        db_path = self.config.DB
        if user_id == 'exc':
            raise RESTError('USER_ID_ERROR', 'User id error.')

        return json_response({'user_id': user_id, 'db_path': db_path})


if __name__ == '__main__':
    app = RESTService()
    app.config = Config('config.yaml')
    app.add_routes(routes)
    app.start()
