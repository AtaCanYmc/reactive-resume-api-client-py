"""Authentication endpoints implementation."""

from typing import Tuple, List, Dict, Any
from ..models.user import User


class AuthAPI:
    """Synchronous Authentication operations."""

    def __init__(self, client) -> None:
        self._client = client

    def login(self, email: str, password: str) -> Tuple[str, User]:
        """Log in with email and password."""
        payload = {"identifier": email, "password": password}
        response = self._client._request("POST", "/api/auth/login", json=payload)
        token = response.get("token") or response.get("accessToken", "")
        user_data = response.get("user") or response
        user = User.model_validate(user_data)
        return token, user

    def me(self) -> User:
        """Get the current authenticated user profile."""
        response = self._client._request("GET", "/api/user/me")
        return User.model_validate(response)

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

    async def login(self, email: str, password: str) -> Tuple[str, User]:
        """Log in asynchronously with email and password."""
        payload = {"identifier": email, "password": password}
        response = await self._client._request("POST", "/api/auth/login", json=payload)
        token = response.get("token") or response.get("accessToken", "")
        user_data = response.get("user") or response
        user = User.model_validate(user_data)
        return token, user

    async def me(self) -> User:
        """Get the current authenticated user profile asynchronously."""
        response = await self._client._request("GET", "/api/user/me")
        return User.model_validate(response)

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
