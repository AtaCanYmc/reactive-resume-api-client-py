"""Core functionality and HTTP client structures."""

from .exceptions import (
    AuthenticationError,
    NotFoundError,
    ReactiveResumeAPIError,
    ReactiveResumeError,
    ValidationError,
)

__all__ = [
    "AuthenticationError",
    "NotFoundError",
    "ReactiveResumeAPIError",
    "ReactiveResumeError",
    "ValidationError",
]
