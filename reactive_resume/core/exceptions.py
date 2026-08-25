"""Custom exceptions for the Reactive Resume API Client."""

from typing import Any


class ReactiveResumeError(Exception):
    """Base exception for all Reactive Resume client errors."""


class ValidationError(ReactiveResumeError):
    """Raised when request data fails client-side validation."""


class ReactiveResumeAPIError(ReactiveResumeError):
    """Raised when the Reactive Resume API returns an error response."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body

    def __str__(self) -> str:
        code_str = f" [Status {self.status_code}]" if self.status_code else ""
        return f"{super().__str__()}{code_str}"


class AuthenticationError(ReactiveResumeAPIError):
    """Raised when authentication fails (401/403)."""


class NotFoundError(ReactiveResumeAPIError):
    """Raised when a requested resource is not found (404)."""
