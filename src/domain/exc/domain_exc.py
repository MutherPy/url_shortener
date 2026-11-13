class NotFoundException(Exception):
    ...


class CodeGenerationError(Exception):
    """No free short code was found within the allowed number of attempts."""
