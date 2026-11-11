from fastapi import FastAPI
import uvicorn
from src.app.deps import DependenciesContainer
from src.app.lifespan import build_lifespan
from src.api.router import router
from src.app.container import Container
from src.application.domain.url_service import UrlService
from src.application.services.short_enc_deco import ShortenerService
from src.intrastructure.db.connection import DbConnection
from src.intrastructure.db.repository import UrlRepository

from configs import Configs

configs = Configs.build_configs()

db_conn = DbConnection(config=configs.db)

deps = DependenciesContainer(
    service=UrlService,
    repository=UrlRepository,
    configs=configs,
    connection=db_conn,
    shortener=ShortenerService
)

container = Container(
    deps=deps,
    connection=db_conn,
)

app = FastAPI(
    lifespan=build_lifespan(container=container, deps=deps)
)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
