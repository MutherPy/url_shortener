from src.app.deps import DependenciesContainer


class Container:
    def __init__(self, connection, deps: DependenciesContainer):
        self.__connection = connection
        self.__deps = deps

    async def init(self):
        await self.__connection.connect()
        self.__deps.init()

    async def start(self):
        ...

    async def stop(self):
        await self.__connection.close()


__all__ = ["Container"]