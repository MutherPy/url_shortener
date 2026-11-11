from src.app.deps import DependenciesContainer


class Container:
    def __init__(self, connection):
        self.__connection = connection

    async def init(self):
        await self.__connection.connect()

    async def start(self):
        ...

    async def stop(self):
        await self.__connection.close()


def build_app_container(deps: DependenciesContainer) -> Container:
    return Container(
        connection=deps.get_connection_proxy(),
    )

__all__ = ["build_app_container", "Container"]