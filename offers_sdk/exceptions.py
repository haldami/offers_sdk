"""Custom exceptions for Offers SDK."""


class InvalidAPIRequestException(Exception):
    """Raised when the API request is invalid (HTTP 400)."""

    pass


class InvalidClientTypeException(Exception):
    """Raised when an unsupported HTTP client type is used."""

    pass


class APIException(Exception):
    """Raised for unhandled API errors or unexpected responses."""

    pass


class AuthException(Exception):
    """Raised when authentication fails (HTTP 401)."""

    pass


class ValidationException(Exception):
    """When validation error occurs (HTTP 422)."""
