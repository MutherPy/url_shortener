from typing import Protocol

from src.ports.infrastructure.db.dto import UrlCreateDbDTO


class IUrlRepository(Protocol):
    async def get_next_seq(self) -> int:
        pass

    async def create(self, url: UrlCreateDbDTO):
        pass

    async def get(self, code: str) -> str:
        pass

    @classmethod
    def build(cls, connection):
        pass
