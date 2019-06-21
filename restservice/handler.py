from abc import ABC, abstractmethod


class RESTHandler(ABC):
    path = None

    async def prepare(self, data):
        if hasattr(self, 'schema'):
            data = self.schema().load(data) if callable(self.schema) else self.schema.load(data)
        return await self.handler(data)

    @abstractmethod
    async def handler(self, data):
        return data
