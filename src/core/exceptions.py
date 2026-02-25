class DomainException(Exception):
    """Base class for domain-specific exceptions."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class DateFormatError(DomainException):
    """Raised when the date format is invalid."""

    pass


class MinimumAgeError(DomainException):
    """Raised when the date format is invalid."""

    pass


class UserNotFoundError(DomainException):
    """Raised when a user record is not found in the database."""

    pass
