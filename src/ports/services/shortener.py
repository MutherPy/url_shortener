from typing import Protocol

class IShortener(Protocol):
    @staticmethod
    def encode(number: int) -> str:
        pass

    @staticmethod
    def generate_short_url(base_url: str, code: str) -> str:
        pass
