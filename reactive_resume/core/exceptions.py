"""Custom exceptions for the Reactive Resume API Client."""

from typing import Optional, Any


class ReactiveResumeError(Exception):
    """Base exception for all Reactive Resume client errors."""
    pass


class ValidationError(ReactiveResumeError):
    """Raised when request data fails client-side validation."""
    pass


class ReactiveResumeAPIError(ReactiveResumeError):
    """Raised when the Reactive Resume API returns an error response."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_body: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body

    def __str__(self) -> str:
        code_str = f" [Status {self.status_code}]" if self.status_code else ""
        return f"{super().__str__()}{code_str}"


class AuthenticationError(ReactiveResumeAPIError):
    """Raised when authentication fails (401/403)."""
    pass


class NotFoundError(ReactiveResumeAPIError):
    """Raised when a requested resource is not found (404)."""
    pass
