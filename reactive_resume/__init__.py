"""Reactive Resume API Python SDK.

An unofficial client for programmatically interacting with Reactive Resume v6 API.
"""

from .core.async_client import AsyncRxResumeClient
from .core.client import RxResumeClient
from .core.exceptions import (
    AuthenticationError,
    NotFoundError,
    ReactiveResumeAPIError,
    ReactiveResumeError,
    ValidationError,
)
from .testing import AsyncMockRxResumeClient, MockRxResumeClient
from .utils.json_resume import from_json_resume, to_json_resume, validate_json_resume

__version__ = "0.7.0"  # x-release-please-version

__all__ = [
    "AsyncMockRxResumeClient",
    "AsyncRxResumeClient",
    "AuthenticationError",
    "MockRxResumeClient",
    "NotFoundError",
    "ReactiveResumeAPIError",
    "ReactiveResumeError",
    "RxResumeClient",
    "ValidationError",
    "from_json_resume",
    "to_json_resume",
    "validate_json_resume",
]
