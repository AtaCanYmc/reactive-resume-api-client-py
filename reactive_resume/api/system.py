"""System and Health API endpoints implementation."""

from ..models.health import SystemHealth


class SystemAPI:
    """Synchronous System and Health operations."""

    def __init__(self, client) -> None:
        self._client = client

    def get_health(self) -> SystemHealth:
        """Retrieve system health and version details (/api/health)."""
        response = self._client._request("GET", "/api/health")
        return SystemHealth.model_validate(response)


class AsyncSystemAPI:
    """Asynchronous System and Health operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def get_health(self) -> SystemHealth:
        """Retrieve system health and version details asynchronously (/api/health)."""
        response = await self._client._request("GET", "/api/health")
        return SystemHealth.model_validate(response)
