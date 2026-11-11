from typing import Protocol

from configs import AppConfig
from src.ports.domain.dto import UrlCreateDomainDTO, UrlCreatedDomainDTO
from src.ports.infrastructure.db.repository_port import IUrlRepository
from src.ports.services.shortener import IShortener


class IUrlService(Protocol):
    async def create(self, url_dto: UrlCreateDomainDTO) -> UrlCreatedDomainDTO:
        pass

    async def get(self, code: str) -> str:
        pass

    @classmethod
    def build(cls, url_repository: IUrlRepository, shortener: IShortener, config: AppConfig):
        pass
