"""Statistics API endpoints implementation."""

from ..models.statistics import ResumeStats


class StatisticsAPI:
    """Synchronous Statistics operations."""

    def __init__(self, client) -> None:
        self._client = client

    def get(self, resume_id: str) -> ResumeStats:
        """Retrieve interaction statistics for a specific resume."""
        response = self._client._request("GET", f"/api/openapi/statistics/{resume_id}")
        return ResumeStats.model_validate(response)


class AsyncStatisticsAPI:
    """Asynchronous Statistics operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def get(self, resume_id: str) -> ResumeStats:
        """Retrieve interaction statistics for a specific resume asynchronously."""
        response = await self._client._request("GET", f"/api/openapi/statistics/{resume_id}")
        return ResumeStats.model_validate(response)
