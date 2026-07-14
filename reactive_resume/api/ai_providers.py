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

    def create(self, label: str, model: str, api_key: str, base_url: str = "") -> Dict[str, Any]:
        """Create a new AI provider configuration."""
        payload = {
            "label": label,
            "model": model,
            "apiKey": api_key,
            "baseURL": base_url,
        }
        response = self._client._request("POST", "/api/openapi/ai-providers", json=payload)
        return dict(response)

    def delete(self, provider_id: str) -> None:
        """Delete an AI provider configuration."""
        self._client._request("DELETE", f"/api/openapi/ai-providers/{provider_id}")

    def test(self, provider_id: str) -> bool:
        """Test the connection of a saved AI provider."""
        response = self._client._request("POST", f"/api/openapi/ai-providers/{provider_id}/test")
        return bool(response.get("success", True))

    def update(self, provider_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an AI provider configuration."""
        response = self._client._request(
            "PATCH", f"/api/openapi/ai-providers/{provider_id}", json=data
        )
        return dict(response)


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

    async def create(
        self, label: str, model: str, api_key: str, base_url: str = ""
    ) -> Dict[str, Any]:
        """Create a new AI provider configuration asynchronously."""
        payload = {
            "label": label,
            "model": model,
            "apiKey": api_key,
            "baseURL": base_url,
        }
        response = await self._client._request("POST", "/api/openapi/ai-providers", json=payload)
        return dict(response)

    async def delete(self, provider_id: str) -> None:
        """Delete an AI provider configuration asynchronously."""
        await self._client._request("DELETE", f"/api/openapi/ai-providers/{provider_id}")

    async def test(self, provider_id: str) -> bool:
        """Test the connection of a saved AI provider asynchronously."""
        response = await self._client._request(
            "POST", f"/api/openapi/ai-providers/{provider_id}/test"
        )
        return bool(response.get("success", True))

    async def update(self, provider_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an AI provider configuration asynchronously."""
        response = await self._client._request(
            "PATCH", f"/api/openapi/ai-providers/{provider_id}", json=data
        )
        return dict(response)
