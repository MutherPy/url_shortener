ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
BASE = len(ALPHABET)
MAX_CODE_LENGTH = 7
CODE_SPACE = BASE ** MAX_CODE_LENGTH


class ShortenerService:
    @staticmethod
    def encode(number: int) -> str:
        """Encode an integer in at most seven Base62 characters.
        Values wrap modulo CODE_SPACE. The database must resolve collisions.
        """
        number %= CODE_SPACE

        if number == 0:
            return ALPHABET[0]

        result = []

        while number:
            number, remainder = divmod(number, BASE)
            result.append(ALPHABET[remainder])

        return "".join(reversed(result))

    @staticmethod
    def generate_short_url(base_url: str, code: str) -> str:
        return f"{base_url.rstrip('/')}/{code}"
