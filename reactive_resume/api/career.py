"""Career and Facts API implementation for v6 AI career assistant."""

import builtins
from typing import Any


class CareerAPI:
    """Synchronous Career and Facts operations."""

    def __init__(self, client) -> None:
        self._client = client

    def get_profile(self) -> dict[str, Any]:
        """Retrieve user's global career profile."""
        response = self._client._request("GET", "/api/openapi/career/profile")
        return dict(response)

    def update_profile(self, data: dict[str, Any]) -> dict[str, Any]:
        """Update user's global career profile."""
        response = self._client._request("PUT", "/api/openapi/career/profile", json=data)
        return dict(response)

    def list_facts(self, application_id: str | None = None) -> builtins.list[dict[str, Any]]:
        """List career facts, optionally filtered by application."""
        params: dict[str, Any] = {}
        if application_id:
            params["applicationId"] = application_id
        response = self._client._request("GET", "/api/openapi/career/facts", params=params or None)
        return list(response)

    def create_fact(self, fact_data: dict[str, Any]) -> dict[str, Any]:
        """Create a new career fact."""
        response = self._client._request("POST", "/api/openapi/career/facts", json=fact_data)
        return dict(response)

    def delete_fact(self, fact_id: str) -> None:
        """Delete a career fact by ID."""
        self._client._request("DELETE", f"/api/openapi/career/facts/{fact_id}")


class AsyncCareerAPI:
    """Asynchronous Career and Facts operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def get_profile(self) -> dict[str, Any]:
        """Retrieve user's global career profile asynchronously."""
        response = await self._client._request("GET", "/api/openapi/career/profile")
        return dict(response)

    async def update_profile(self, data: dict[str, Any]) -> dict[str, Any]:
        """Update user's global career profile asynchronously."""
        response = await self._client._request("PUT", "/api/openapi/career/profile", json=data)
        return dict(response)

    async def list_facts(self, application_id: str | None = None) -> builtins.list[dict[str, Any]]:
        """List career facts asynchronously."""
        params: dict[str, Any] = {}
        if application_id:
            params["applicationId"] = application_id
        response = await self._client._request(
            "GET", "/api/openapi/career/facts", params=params or None
        )
        return list(response)

    async def create_fact(self, fact_data: dict[str, Any]) -> dict[str, Any]:
        """Create a new career fact asynchronously."""
        response = await self._client._request("POST", "/api/openapi/career/facts", json=fact_data)
        return dict(response)

    async def delete_fact(self, fact_id: str) -> None:
        """Delete a career fact by ID asynchronously."""
        await self._client._request("DELETE", f"/api/openapi/career/facts/{fact_id}")
