from src.ports.infrastructure.db.db_conn_proxy_port import IDbConnection
from typing import Protocol
from asyncio import gather

class StartStop(Protocol):
    async def start(self):
        pass
    async def stop(self):
        pass


class Container:
    def __init__(self, connection: IDbConnection, to_start: list[StartStop]):
        self.__connection = connection
        self.to_start = to_start

    async def init(self):
        await self.__connection.connect()

    async def start(self):
        await gather(*map(lambda x: x.start(), self.to_start))

    async def stop(self):
        await self.__connection.close()
        await gather(*map(lambda x: x.stop(), self.to_start))


__all__ = ["Container"]