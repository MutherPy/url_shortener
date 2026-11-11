from contextlib import asynccontextmanager

from src.app.deps import DependenciesContainer
from src.app.container import Container
from fastapi import FastAPI
from typing import Callable


def build_lifespan(c: Callable[[DependenciesContainer], Container], deps: DependenciesContainer):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        container = c(deps)
        app.state.container = deps
        await container.init()
        await container.start()
        yield
        await container.stop()
    return lifespan