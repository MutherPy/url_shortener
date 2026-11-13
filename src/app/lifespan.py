from contextlib import asynccontextmanager

from src.app.deps import DependenciesContainer
from src.app.container import Container
from fastapi import FastAPI

def build_lifespan(container: Container, deps: DependenciesContainer):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            await container.init()
            app.state.container = deps
            await container.start()
            yield
        finally:
            await container.stop()
    return lifespan
