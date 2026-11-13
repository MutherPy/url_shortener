from asyncio import Event
from typing import Callable, Awaitable, Type

from asyncpg import Pool
from src.ports.infrastructure.cache.cache_port import IUrlRepositorySeqCache
from src.ports.infrastructure.db.db_conn_proxy_port import IDbConnection
from src.ports.infrastructure.db.dto import UrlCreateDbDTO

class UrlRepository:
    def __init__(self, db_conn_proxy: IDbConnection, seq_cache: IUrlRepositorySeqCache):
        self.__db_conn_proxy = db_conn_proxy
        self.__seq_cache = seq_cache

    async def get_next_seq_list(self, size) -> list[int]:
        async with self.__db_conn_proxy.connection.acquire() as connection:
            return await connection.fetchval(
            """
            SELECT ARRAY(
                SELECT nextval('urls_id_seq')
                FROM generate_series(1, $1::int)
            )
            """,
            size,
        )

    async def get_next_seq(self) -> int:
        return await self.__seq_cache.get()

    async def create(self, url: UrlCreateDbDTO) -> bool:
        """Insert a URL, returning False only when its code is already taken."""
        async with self.__db_conn_proxy.connection.acquire() as connection:
            inserted_code = await connection.fetchval(
                """
                INSERT INTO urls (code, original_url)
                VALUES ($1, $2)
                ON CONFLICT (code) DO NOTHING
                RETURNING code
                """,
                url.code,
                url.original_url
            )
        return inserted_code is not None

    async def get(self, code: str) -> str | None:
        async with self.__db_conn_proxy.connection.acquire() as connection:
            return await connection.fetchval(
                "SELECT original_url FROM urls WHERE code = $1", code
            )
