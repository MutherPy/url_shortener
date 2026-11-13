from typing import Protocol
from src.ports.domain.dto import UrlCreateDomainDTO, UrlCreatedDomainDTO


class IUrlService(Protocol):
    async def create(self, url_dto: UrlCreateDomainDTO) -> UrlCreatedDomainDTO:
        pass

    async def get(self, code: str) -> str:
        pass
