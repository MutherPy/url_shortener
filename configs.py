from pydantic_settings import BaseSettings, SettingsConfigDict
from dataclasses import dataclass

class DbConfigs(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env"
    )

class AppConfig(BaseSettings):
    BASE_HOST: str

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env"
    )

@dataclass(frozen=True)
class Configs:
    db: DbConfigs
    app: AppConfig

    @classmethod
    def build_configs(cls, db: DbConfigs | None = None, app: AppConfig | None = None):
        if not db:
            db = DbConfigs()
        if not app:
            app = AppConfig()
        return cls(db, app)
