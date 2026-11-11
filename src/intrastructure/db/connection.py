from asyncpg import Connection, create_pool

from configs import DbConfigs


class DbConnection:
    def __init__(self, config: DbConfigs):
        self._config = config
        self._pool: Connection

    async def connect(self) -> Connection:
        """Create a database connection that the caller is responsible for closing."""
        self._pool = await create_pool(
            host=self._config.POSTGRES_HOST,
            port=self._config.POSTGRES_PORT,
            user=self._config.POSTGRES_USER,
            password=self._config.POSTGRES_PASSWORD,
            database=self._config.POSTGRES_DB
        )
        return self._pool

    @property
    def connection(self) -> Connection:
        return self._pool

    async def close(self):
        await self._pool.close()
