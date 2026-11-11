from asyncio import Lock
from asyncpg import Pool
from src.ports.infrastructure.db.dto import UrlCreateDbDTO

CACHE_SIZE = 1000

class UrlRepositorySeqCache:
    def __init__(self, trtrieve_):
        self.__cache = list()
        self.__lock = Lock()

    async def set(self, id_seq: list[int]):
        async with self.__lock:
            self.__cache = [*self.__cache, *id_seq]

    async def get(self) -> int:
        if l := len(self.__cache):
            if l <= CACHE_SIZE / 3:
                await self.set(id_seq=l)


class UrlRepository:
    def __init__(self, connection: Pool):
        self.__connection = connection

    async def get_next_seq(self) -> int:
        async with self.__connection.acquire() as connection:
            return await connection.fetchval("SELECT nextval('urls_id_seq')")

    async def create(self, url: UrlCreateDbDTO) -> bool:
        """Insert a URL, returning False only when its code is already taken."""
        async with self.__connection.acquire() as connection:
            inserted_code = await connection.fetchval(
                """
                INSERT INTO urls (code, original_url, shortened_url)
                VALUES ($1, $2, $3)
                ON CONFLICT (code) DO NOTHING
                RETURNING code
                """,
                url.code,
                url.original_url,
                url.short_url,
            )
        return inserted_code is not None

    async def get(self, code: str) -> str | None:
        async with self.__connection.acquire() as connection:
            return await connection.fetchval(
                "SELECT original_url FROM urls WHERE code = $1", code
            )

    @classmethod
    def build(cls, connection) -> 'UrlRepository':
        return cls(connection=connection)
