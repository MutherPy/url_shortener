from typing import Protocol

from src.ports.infrastructure.db.dto import UrlCreateDbDTO


class IUrlRepository(Protocol):
    async def get_next_seq(self) -> int:
        pass

    async def create(self, url: UrlCreateDbDTO) -> bool:
        """Return True on insertion, or False if the code is already taken."""
        pass

    async def get(self, code: str) -> str | None:
        pass

    @classmethod
    def build(cls, connection):
        pass
