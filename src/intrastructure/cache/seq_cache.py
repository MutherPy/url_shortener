from asyncio import Event
from typing import Callable, Awaitable


class UrlRepositorySeqCache:
    def __init__(self, cache_size: int) -> None:
        self.__cache = list()
        self.__lock = Event()
        self.__lock.set()
        self.__retrieve_fn: Callable[[int], Awaitable[list[int]]]
        self.__cache_size = cache_size

    def set_retrieve_fn(self, retrieve_fn: Callable[[int], Awaitable[list[int]]]):
        self.__retrieve_fn = retrieve_fn

    async def _set(self):
        self.__lock.clear()
        id_seq = await self.__retrieve_fn(self.__cache_size)
        self.__cache = [*self.__cache, *id_seq]
        self.__lock.set()

    async def get(self) -> int:
        await self.__lock.wait()
        if len(self.__cache) <= self.__cache_size // 3:
            await self._set()
        return self.__cache.pop(0)
