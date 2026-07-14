"""Authentication endpoints implementation."""

from typing import List, Dict, Any


class AuthAPI:
    """Synchronous Authentication operations."""

    def __init__(self, client) -> None:
        self._client = client

    def list_providers(self) -> List[str]:
        """List all configured authentication providers."""
        response = self._client._request("GET", "/api/openapi/auth/providers")
        return list(response)

    def export_account(self) -> Dict[str, Any]:
        """Export user account data."""
        response = self._client._request("GET", "/api/openapi/auth/account/export")
        return dict(response)

    def delete_account(self) -> None:
        """Delete user account."""
        self._client._request("DELETE", "/api/openapi/auth/account")


class AsyncAuthAPI:
    """Asynchronous Authentication operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def list_providers(self) -> List[str]:
        """List all configured authentication providers asynchronously."""
        response = await self._client._request("GET", "/api/openapi/auth/providers")
        return list(response)

    async def export_account(self) -> Dict[str, Any]:
        """Export user account data asynchronously."""
        response = await self._client._request("GET", "/api/openapi/auth/account/export")
        return dict(response)

    async def delete_account(self) -> None:
        """Delete user account asynchronously."""
        await self._client._request("DELETE", "/api/openapi/auth/account")
