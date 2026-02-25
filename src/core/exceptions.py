class DomainException(Exception):
    """Base class for domain-specific exceptions."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class DateFormatError(DomainException):
    """Raised when the date format is invalid."""

    pass
