from configs import Configs
from src.intrastructure.db.connection import DbConnection

from src.ports.domain.service_port import IUrlService
from src.ports.infrastructure.db.repository_port import IUrlRepository
from src.ports.services.shortener import IShortener


class DependenciesContainer:
    def __init__(
            self,
            service: type[IUrlService],
            repository: type[IUrlRepository],
            configs: Configs,
            connection: DbConnection,
            shortener: type[IShortener]
    ):
        self.__service = service
        self.__repository = repository
        self.__configs = configs
        self.__connection = connection
        self.__shortener = shortener

    def get_service(self) -> IUrlService:
        return self.__service.build(
            url_repository=self.get_repository(),
            config=self.get_configs().app,
            shortener=self.get_shortener()
        )

    def get_repository(self) -> IUrlRepository:
        return self.__repository.build(
            connection=self.get_connection()
        )

    def get_configs(self) -> Configs:
        return self.__configs

    def get_connection(self):
        return self.__connection.connection

    def get_shortener(self):
        return self.__shortener

    def get_connection_proxy(self):
        return self.__connection
