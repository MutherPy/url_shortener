from typing import Protocol, Callable, Awaitable


class IUrlRepositorySeqCache(Protocol):
    def set_retrieve_fn(self, retrieve_fn: Callable[[int], Awaitable[list[int]]]):
        pass

    async def _set(self):
        pass

    async def get(self) -> int:
        pass

