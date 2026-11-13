from configs import Configs
from src.ports.domain.service_port import IUrlService


class DependenciesContainer:
    def __init__(
            self,
            service: IUrlService,
            configs: Configs,
    ):
        self.__service = service
        self.__configs = configs

    def get_service(self) -> IUrlService:
        return self.__service

    def get_configs(self) -> Configs:
        return self.__configs
