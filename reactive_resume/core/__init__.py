"""Core functionality and HTTP client structures."""

from .exceptions import (
    ReactiveResumeError,
    ReactiveResumeAPIError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
)

__all__ = [
    "ReactiveResumeError",
    "ReactiveResumeAPIError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
]
