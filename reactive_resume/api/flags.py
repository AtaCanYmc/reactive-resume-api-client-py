"""Flags API endpoints implementation."""

from typing import Dict, Any


class FlagsAPI:
    """Synchronous Flags operations."""

    def __init__(self, client) -> None:
        self._client = client

    def list(self) -> Dict[str, Any]:
        """List all available feature flags."""
        response = self._client._request("GET", "/api/openapi/flags")
        return dict(response)


class AsyncFlagsAPI:
    """Asynchronous Flags operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def list(self) -> Dict[str, Any]:
        """List all available feature flags asynchronously."""
        response = await self._client._request("GET", "/api/openapi/flags")
        return dict(response)
