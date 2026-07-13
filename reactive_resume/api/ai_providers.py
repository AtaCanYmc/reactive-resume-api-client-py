"""AI Providers API endpoints implementation."""

from typing import List, Dict, Any


class AiProvidersAPI:
    """Synchronous AI Providers operations."""

    def __init__(self, client) -> None:
        self._client = client

    def list(self) -> List[Dict[str, Any]]:
        """List all configured AI Providers."""
        response = self._client._request("GET", "/api/openapi/ai-providers")
        if isinstance(response, list):
            return response
        return [response]


class AsyncAiProvidersAPI:
    """Asynchronous AI Providers operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def list(self) -> List[Dict[str, Any]]:
        """List all configured AI Providers asynchronously."""
        response = await self._client._request("GET", "/api/openapi/ai-providers")
        if isinstance(response, list):
            return response
        return [response]
