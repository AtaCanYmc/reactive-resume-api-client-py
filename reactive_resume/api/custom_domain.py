"""Custom Domain API endpoints implementation aligned with Reactive Resume v6."""

from typing import Any


class CustomDomainAPI:
    """Synchronous Custom Domain management."""

    def __init__(self, client) -> None:
        self._client = client

    def get(self) -> dict[str, Any]:
        """Get custom domain configuration, DNS target, and verification status."""
        response = self._client._request("GET", "/api/openapi/custom-domain")
        return dict(response)

    def set(self, hostname: str) -> dict[str, Any]:
        """Configure or update custom domain hostname."""
        response = self._client._request(
            "PUT", "/api/openapi/custom-domain", json={"hostname": hostname}
        )
        return dict(response)

    def verify(self) -> dict[str, Any]:
        """Trigger DNS verification for the configured custom domain."""
        response = self._client._request("POST", "/api/openapi/custom-domain/verify")
        return dict(response)

    def delete(self) -> None:
        """Remove custom domain configuration."""
        self._client._request("DELETE", "/api/openapi/custom-domain")


class AsyncCustomDomainAPI:
    """Asynchronous Custom Domain management."""

    def __init__(self, client) -> None:
        self._client = client

    async def get(self) -> dict[str, Any]:
        """Get custom domain configuration asynchronously."""
        response = await self._client._request("GET", "/api/openapi/custom-domain")
        return dict(response)

    async def set(self, hostname: str) -> dict[str, Any]:
        """Configure or update custom domain hostname asynchronously."""
        response = await self._client._request(
            "PUT", "/api/openapi/custom-domain", json={"hostname": hostname}
        )
        return dict(response)

    async def verify(self) -> dict[str, Any]:
        """Trigger DNS verification asynchronously."""
        response = await self._client._request("POST", "/api/openapi/custom-domain/verify")
        return dict(response)

    async def delete(self) -> None:
        """Remove custom domain configuration asynchronously."""
        await self._client._request("DELETE", "/api/openapi/custom-domain")
