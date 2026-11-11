from asyncpg import Pool
from src.ports.infrastructure.db.dto import UrlCreateDbDTO


class UrlRepository:
    def __init__(self, connection: Pool):
        self.__connection = connection

    async def get_next_seq(self) -> int:
        async with self.__connection.acquire() as connection:
            return await connection.fetchval("SELECT nextval('urls_id_seq');")

    async def create(self, url: UrlCreateDbDTO):
        async with self.__connection.acquire() as connection:
            await connection.execute(
                "INSERT INTO urls (code, original_url, shortened_url) VALUES ($1, $2, $3)",
            url.code, url.original_url, url.short_url
            )

    async def get(self, code: str) -> str:
        async with self.__connection.acquire() as connection:
            return await connection.fetchval(
                "SELECT original_url FROM urls WHERE code = $1", code
            )

    @classmethod
    def build(cls, connection) -> 'UrlRepository':
        return cls(connection=connection)
