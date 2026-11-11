from configs import Configs
from src.intrastructure.db.connection import DbConnection

from src.ports.domain.service_port import IUrlService
from src.ports.infrastructure.cache.cache_port import IUrlRepositorySeqCache
from src.ports.infrastructure.db.repository_port import IUrlRepository
from src.ports.services.shortener import IShortener


class DependenciesContainer:
    def __init__(
            self,
            service: type[IUrlService],
            repository: type[IUrlRepository],
            configs: Configs,
            connection: DbConnection,
            shortener: type[IShortener],
            seq_cache: type[IUrlRepositorySeqCache],
    ):
        self.__service = service
        self.__repository = repository
        self.__configs = configs
        self.__connection = connection
        self.__shortener = shortener
        self.__seq_cache = seq_cache

    def init(self):
        self.__repository = self.__repository.build(
            connection=self.__connection.connection,
            seq_cache=self.__seq_cache,
            cache_size=self.__configs.app.CACHE_SIZE
        )
        self.__service = self.__service.build(
            url_repository=self.__repository,
            config=self.__configs.app,
            shortener=self.__shortener
        )

    def get_service(self) -> IUrlService:
        return self.__service

    def get_repository(self) -> IUrlRepository:
        return self.__repository

    def get_configs(self) -> Configs:
        return self.__configs

    def get_shortener(self):
        return self.__shortener

    def get_connection_proxy(self):
        return self.__connection
