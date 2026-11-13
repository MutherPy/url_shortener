from asyncio import Lock, create_task, sleep
from typing import Callable, Awaitable
from collections import deque
from time import monotonic


class UrlRepositorySeqCache:
    def __init__(self, cache_size: int) -> None:
        self.__cache = deque()
        self.__lock = Lock()
        self.__retrieve_fn: Callable[[int], Awaitable[list[int]]]

        self.__cache_size = cache_size
        self.__refill_size = self.__cache_size // 3

        self.__window_period = 1
        self.__rate = 1000
        self.__max_cache_size = 100_000
        self.__window = deque()

        self.__refill_time = 0.1

    def set_retrieve_fn(self, retrieve_fn: Callable[[int], Awaitable[list[int]]]):
        self.__retrieve_fn = retrieve_fn

    async def _set(self):
        s = monotonic()
        async with self.__lock:
            id_seq = await self.__retrieve_fn(self.__cache_size)
            self.__cache.extend(id_seq)
        self.__refill_time = monotonic() - s

    async def check_window(self):
        while len(self.__window) and int(monotonic() - self.__window[0]) >= self.__window_period:
            self.__window.popleft()

        self.__rate = (len(self.__window) if not 0 else 1) / self.__window_period
        reqs_per_refill_time = (self.__rate * self.__refill_time)

        if self.__rate > self.__cache_size:
            t = round(self.__rate / self.__cache_size)
            new_size = self.__cache_size * t if t >= 1 else 1
            self.__cache_size = new_size if new_size <= self.__max_cache_size else self.__max_cache_size
            self.__refill_size = int(reqs_per_refill_time)

        print(f"{self.__cache_size=}, {self.__refill_size=}, {self.__rate=}, {self.__refill_time=}, {reqs_per_refill_time=}")


    async def get(self) -> int:
        await self.check_window()

        if not self.__lock.locked() and len(self.__cache) <= self.__refill_size:
            await self._set()
        try:
            res = self.__cache.popleft()
            self.__window.append(monotonic())
        except IndexError:
            await self._set()
            res = self.__cache.popleft()
            self.__window.append(monotonic())
        return res
