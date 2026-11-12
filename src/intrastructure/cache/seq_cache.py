from asyncio import Lock, create_task
from typing import Callable, Awaitable
from collections import deque

from time import monotonic, time


class UrlRepositorySeqCache:
    def __init__(self, cache_size: int) -> None:
        self.__cache = deque()
        self.__lock = Lock()
        self.__retrieve_fn: Callable[[int], Awaitable[list[int]]]

        self.__cache_size = cache_size
        self.__refill_size = self.__cache_size // 3

    def set_retrieve_fn(self, retrieve_fn: Callable[[int], Awaitable[list[int]]]):
        self.__retrieve_fn = retrieve_fn

    async def _set(self):
        async with self.__lock:
            id_seq = await self.__retrieve_fn(self.__cache_size)
            self.__cache.extend(id_seq)

    async def get(self) -> int:
        if not self.__lock.locked() and len(self.__cache) <= self.__cache_size // 3:
            await self._set()
        return self.__cache.popleft()
