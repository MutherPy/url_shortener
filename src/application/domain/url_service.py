from configs import AppConfig
from src.application.domain.exc.domain_exc import CodeGenerationError, NotFoundException
from src.ports.domain.dto import UrlCreateDomainDTO, UrlCreatedDomainDTO
from src.ports.infrastructure.db.dto import UrlCreateDbDTO
from src.ports.infrastructure.db.repository_port import IUrlRepository
from src.ports.services.shortener import IShortener


MAX_CODE_GENERATION_ATTEMPTS = 10


class UrlService:
    def __init__(self, url_repository: IUrlRepository, shortener: IShortener, config: AppConfig) -> None:
        self._url_repository = url_repository
        self._shortener = shortener
        self._app_config = config

    async def create(self, url_dto: UrlCreateDomainDTO) -> UrlCreatedDomainDTO:
        for _ in range(MAX_CODE_GENERATION_ATTEMPTS):
            next_id = await self._url_repository.get_next_seq()
            new_code = self._shortener.encode(next_id)
            new_short_url = self._shortener.generate_short_url(
                base_url=self._app_config.BASE_HOST,
                code=new_code,
            )
            to_db = UrlCreateDbDTO(
                code=new_code,
                original_url=url_dto.original_url,
                short_url=new_short_url,
            )
            if await self._url_repository.create(url=to_db):
                return UrlCreatedDomainDTO(code=new_code, short_url=new_short_url)

        raise CodeGenerationError(
            f"Could not allocate a short code after {MAX_CODE_GENERATION_ATTEMPTS} attempts"
        )

    async def get(self, code: str) -> str:
        if result := await self._url_repository.get(code=code):
            return result
        raise NotFoundException

    @classmethod
    def build(cls, url_repository: IUrlRepository, shortener: IShortener, config: AppConfig) -> 'UrlService':
        return cls(url_repository=url_repository, shortener=shortener, config=config)
