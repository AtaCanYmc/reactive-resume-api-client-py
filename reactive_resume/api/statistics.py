"""Statistics API endpoints implementation."""

from typing import Any


class StatisticsAPI:
    """Synchronous Statistics operations."""

    def __init__(self, client) -> None:
        self._client = client

    def get_users_count(self) -> Any:
        """Retrieve total number of users."""
        return self._client._request("GET", "/api/openapi/statistics/users")

    def get_github_stars(self) -> Any:
        """Retrieve GitHub star count."""
        return self._client._request("GET", "/api/openapi/statistics/github/stars")

    def get_resumes_count(self) -> Any:
        """Retrieve total number of resumes."""
        return self._client._request("GET", "/api/openapi/statistics/resumes")


class AsyncStatisticsAPI:
    """Asynchronous Statistics operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def get_users_count(self) -> Any:
        """Retrieve total number of users asynchronously."""
        return await self._client._request("GET", "/api/openapi/statistics/users")

    async def get_github_stars(self) -> Any:
        """Retrieve GitHub star count asynchronously."""
        return await self._client._request("GET", "/api/openapi/statistics/github/stars")

    async def get_resumes_count(self) -> Any:
        """Retrieve total number of resumes asynchronously."""
        return await self._client._request("GET", "/api/openapi/statistics/resumes")
