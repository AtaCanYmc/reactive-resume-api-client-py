"""Statistics API endpoints implementation."""

from ..models.statistics import ResumeStats


class StatisticsAPI:
    """Synchronous Statistics operations."""

    def __init__(self, client) -> None:
        self._client = client

    def get(self, resume_id: str) -> ResumeStats:
        """Retrieve interaction statistics for a specific resume."""
        response = self._client._request("GET", f"/api/openapi/resumes/{resume_id}/statistics")
        return ResumeStats.model_validate(response)

    def get_daily(self, resume_id: str, day: int = 30) -> ResumeStats:
        """Retrieve daily interaction statistics for a specific resume."""
        response = self._client._request(
            "GET", f"/api/openapi/resumes/{resume_id}/statistics/daily?day={day}"
        )
        return ResumeStats.model_validate(response)


class AsyncStatisticsAPI:
    """Asynchronous Statistics operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def get(self, resume_id: str) -> ResumeStats:
        """Retrieve interaction statistics for a specific resume asynchronously."""
        response = await self._client._request(
            "GET", f"/api/openapi/resumes/{resume_id}/statistics"
        )
        return ResumeStats.model_validate(response)

    async def get_daily(self, resume_id: str, day: int = 30) -> ResumeStats:
        """Retrieve daily interaction statistics for a specific resume asynchronously."""
        response = await self._client._request(
            "GET", f"/api/openapi/resumes/{resume_id}/statistics/daily?day={day}"
        )
        return ResumeStats.model_validate(response)
