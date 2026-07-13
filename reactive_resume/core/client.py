"""Synchronous API Client implementation."""

from typing import Any, Optional
import httpx

from .exceptions import (
    ReactiveResumeError,
    ReactiveResumeAPIError,
    AuthenticationError,
    NotFoundError,
)
from ..api.auth import AuthAPI
from ..api.resumes import ResumesAPI


class RxResumeClient:
    """Synchronous client for Reactive Resume v4 API."""

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        token: Optional[str] = None,
        timeout: float = 30.0,
        verify: bool = True,
    ) -> None:
        """Initialize the client.

        Args:
            base_url: The base URL of the Reactive Resume instance.
            api_key: API Key for x-api-key authentication.
            token: Bearer Token for Authorization authentication.
            timeout: Request timeout in seconds.
            verify: Verify SSL certificates.
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.verify = verify

        headers = {
            "Accept": "application/json",
            "User-Agent": "rxresume-python/0.1.0",
        }

        if api_key:
            headers["x-api-key"] = api_key
        elif token:
            headers["Authorization"] = f"Bearer {token}"

        self.client = httpx.Client(
            base_url=self.base_url,
            headers=headers,
            timeout=self.timeout,
            verify=self.verify,
        )

        # Initialize API sections
        self.auth = AuthAPI(self)
        self.resumes = ResumesAPI(self)

    def set_token(self, token: str) -> None:
        """Update client headers with a new Bearer token."""
        self.client.headers["Authorization"] = f"Bearer {token}"
        if "x-api-key" in self.client.headers:
            del self.client.headers["x-api-key"]

    def set_api_key(self, api_key: str) -> None:
        """Update client headers with a new API key."""
        self.client.headers["x-api-key"] = api_key
        if "Authorization" in self.client.headers:
            del self.client.headers["Authorization"]

    def _request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> Any:
        """Perform a synchronous HTTP request and handle errors.

        Args:
            method: HTTP method (GET, POST, etc.).
            url: Target URL path (appended to base_url).
            **kwargs: Extra arguments for httpx request.

        Returns:
            Decoded JSON response or raw content.
        """
        try:
            response = self.client.request(method, url, **kwargs)
            return self._handle_response(response)
        except httpx.HTTPError as e:
            if not isinstance(e, httpx.HTTPStatusError):
                raise ReactiveResumeError(f"Network or connection error occurred: {e}") from e
            raise

    def _handle_response(self, response: httpx.Response) -> Any:
        """Process response data or raise descriptive exceptions.

        Args:
            response: Response object from httpx.
        """
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            status_code = response.status_code
            error_data = None
            try:
                error_data = response.json()
            except ValueError:
                error_data = response.text

            message = ""
            if isinstance(error_data, dict):
                message = error_data.get("message") or error_data.get("error") or str(error_data)
            else:
                message = str(error_data)

            if status_code in (401, 403):
                raise AuthenticationError(
                    f"Authentication failed: {message}",
                    status_code=status_code,
                    response_body=error_data,
                ) from e
            elif status_code == 404:
                raise NotFoundError(
                    f"Resource not found: {message}",
                    status_code=status_code,
                    response_body=error_data,
                ) from e
            else:
                raise ReactiveResumeAPIError(
                    f"API error: {message}",
                    status_code=status_code,
                    response_body=error_data,
                ) from e

        # Success path
        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()
        return response.content

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self.client.close()

    def __enter__(self) -> "RxResumeClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
