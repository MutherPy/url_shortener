from asyncpg import Pool, create_pool
from configs import DbConfigs


class DbConnection:
    def __init__(self, config: DbConfigs):
        self._config = config
        self._pool: Pool

    async def connect(self):
        """Create a database connection that the caller is responsible for closing."""
        self._pool = await create_pool(
            host=self._config.POSTGRES_HOST,
            port=self._config.POSTGRES_PORT,
            user=self._config.POSTGRES_USER,
            password=self._config.POSTGRES_PASSWORD,
            database=self._config.POSTGRES_DB,
            min_size=self._config.MIN_POOL_SIZE,
            max_size=self._config.MAX_POOL_SIZE
        )

    @property
    def connection(self) -> Pool:
        return self._pool

    async def close(self):
        await self._pool.close()
