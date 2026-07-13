"""Authentication endpoints implementation."""

from typing import Tuple
from ..models.user import User


class AuthAPI:
    """Synchronous Authentication operations."""

    def __init__(self, client) -> None:
        self._client = client

    def login(self, email: str, password: str) -> Tuple[str, User]:
        """Log in with email and password.

        Args:
            email: User's email.
            password: User's password.

        Returns:
            A tuple of (access_token, User object).
        """
        payload = {"identifier": email, "password": password}
        response = self._client._request("POST", "/api/auth/login", json=payload)
        
        # Typically returns token in cookies or response body
        # Let's extract token and user
        token = response.get("token") or response.get("accessToken", "")
        user_data = response.get("user") or response
        user = User.model_validate(user_data)
        return token, user

    def me(self) -> User:
        """Get the current authenticated user profile."""
        response = self._client._request("GET", "/api/user/me")
        return User.model_validate(response)


class AsyncAuthAPI:
    """Asynchronous Authentication operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def login(self, email: str, password: str) -> Tuple[str, User]:
        """Log in asynchronously with email and password.

        Args:
            email: User's email.
            password: User's password.

        Returns:
            A tuple of (access_token, User object).
        """
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
