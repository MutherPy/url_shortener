from src.ports.infrastructure.db.db_conn_proxy_port import IDbConnection


class Container:
    def __init__(self, connection: IDbConnection):
        self.__connection = connection

    async def init(self):
        await self.__connection.connect()

    async def start(self):
        ...

    async def stop(self):
        await self.__connection.close()


__all__ = ["Container"]