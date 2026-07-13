"""Reactive Resume API Python SDK.

An unofficial client for programmatically interacting with Reactive Resume v4 API.
"""

from .core.client import RxResumeClient
from .core.async_client import AsyncRxResumeClient
from .core.exceptions import (
    ReactiveResumeError,
    ReactiveResumeAPIError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
)

__version__ = "0.1.0"

__all__ = [
    "RxResumeClient",
    "AsyncRxResumeClient",
    "ReactiveResumeError",
    "ReactiveResumeAPIError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
]
