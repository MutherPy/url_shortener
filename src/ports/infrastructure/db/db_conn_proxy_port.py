from typing import Protocol

from asyncpg import Pool


class IDbConnection(Protocol):
    @property
    def connection(self) -> Pool:
        pass

    async def connect(self):
        pass

    async def close(self):
        pass
