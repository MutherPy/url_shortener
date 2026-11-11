ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

class ShortenerService:
    @staticmethod
    def encode(number: int) -> str:
        if number == 0:
            return ALPHABET[0]

        result = []

        while number:
            number, remainder = divmod(number, 64)
            result.append(ALPHABET[remainder])

        return "".join(reversed(result))

    @staticmethod
    def decode(code: str) -> int:
        number = 0

        for char in code:
            number = number * 64 + ALPHABET.index(char)

        return number

    @staticmethod
    def generate_short_url(base_url: str, code: str) -> str:
        return f"{base_url.lstrip('/')}/{code}"