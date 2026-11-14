from fastapi import FastAPI
import uvicorn
from src.app.deps import DependenciesContainer
from src.app.lifespan import build_lifespan
from src.api.router import router
from src.app.container import Container
from src.domain.url_service import UrlService
from src.services.short_enc_deco import ShortenerService
from src.intrastructure.cache.seq_cache import UrlRepositorySeqCache
from src.intrastructure.db.connection import DbConnection
from src.intrastructure.db.repository import UrlRepository

from configs import Configs

configs = Configs.build_configs()

db_conn = DbConnection(config=configs.db)
repository_cache = UrlRepositorySeqCache(cache_size=configs.app.CACHE_SIZE)
url_repository = UrlRepository(db_conn_proxy=db_conn, seq_cache=repository_cache)
repository_cache.set_retrieve_fn(url_repository.get_next_seq_list)
url_service = UrlService(url_repository=url_repository, shortener=ShortenerService, config=configs.app)

deps = DependenciesContainer(
    service=url_service,
    configs=configs
)

container = Container(
    connection=db_conn,
    to_start = [
        repository_cache,
    ]
)

app = FastAPI(
    lifespan=build_lifespan(container=container, deps=deps)
)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=5, loop="uvloop")
