class ResourceError(Exception):
    """Base exception for errors."""


class ConfigurationError(ResourceError):
    """Raised when there's a configuration-related error."""


class APIError(ResourceError):
    """Raised when there's an error in the API request or response."""
