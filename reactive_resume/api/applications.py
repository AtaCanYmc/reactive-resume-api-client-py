"""Applications API endpoints implementation."""

import builtins
from typing import Any

from ..models.application import Application, ApplicationCreate, ApplicationSummary


class ApplicationsAPI:
    """Synchronous Job Applications operations."""

    def __init__(self, client) -> None:
        self._client = client

    def list(
        self,
        status: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> builtins.list[Application]:
        """List all job applications."""
        params: dict[str, Any] = {}
        if status:
            params["status"] = status
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = self._client._request("GET", "/api/openapi/applications", params=params or None)
        if isinstance(response, dict) and "data" in response:
            items = response["data"]
        else:
            items = response
        return [Application.model_validate(item) for item in items]

    def summary(
        self,
        status: str | None = None,
        tags: builtins.list[str] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> builtins.list[ApplicationSummary]:
        """Retrieve lightweight application summaries without heavy descriptions."""
        params: dict[str, Any] = {}
        if status:
            params["status"] = status
        if tags:
            params["tags"] = ",".join(tags)
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = self._client._request(
            "GET", "/api/openapi/applications/summary", params=params or None
        )
        if isinstance(response, dict) and "data" in response:
            items = response["data"]
        elif isinstance(response, list):
            items = response
        else:
            items = []
        return [ApplicationSummary.model_validate(item) for item in items]

    def close(self, app_id: str, reason: str = "not-selected") -> Application:
        """Close an application with a closedReason (not-selected, withdrew, accepted-other, no-response)."""
        response = self._client._request(
            "PATCH",
            f"/api/openapi/applications/{app_id}",
            json={"stage": "closed", "closedReason": reason},
        )
        return Application.model_validate(response)

    def get(self, app_id: str) -> Application:
        """Retrieve a specific job application by ID."""
        response = self._client._request("GET", f"/api/openapi/applications/{app_id}")
        return Application.model_validate(response)

    def create(self, data: ApplicationCreate) -> Application:
        """Log/create a new job application."""
        payload = data.model_dump(by_alias=True, exclude_none=True)
        response = self._client._request("POST", "/api/openapi/applications", json=payload)
        return Application.model_validate(response)

    def delete(self, app_id: str) -> None:
        """Delete a job application by ID."""
        self._client._request("DELETE", f"/api/openapi/applications/{app_id}")

    def list_tags(self) -> builtins.list[str]:
        """List all application tags."""
        response = self._client._request("GET", "/api/openapi/applications/tags")
        return list(response)

    def get_pipeline_stats(self) -> dict[str, Any]:
        """Get application pipeline statistics."""
        response = self._client._request("GET", "/api/openapi/applications/stats")
        return dict(response)

    def bulk_import(self, items: builtins.list[dict[str, Any]]) -> dict[str, Any]:
        """Bulk import job applications."""
        payload = {"items": items}
        response = self._client._request("POST", "/api/openapi/applications/import", json=payload)
        return dict(response)

    def get_lanes(self) -> builtins.list[dict[str, Any]]:
        """Retrieve custom Kanban lanes/stages for applications."""
        response = self._client._request("GET", "/api/openapi/applications/lanes")
        return list(response)

    def update_lanes(self, lanes: builtins.list[dict[str, Any]]) -> builtins.list[dict[str, Any]]:
        """Create or update application Kanban lanes."""
        response = self._client._request(
            "POST", "/api/openapi/applications/lanes", json={"lanes": lanes}
        )
        return list(response)


class AsyncApplicationsAPI:
    """Asynchronous Job Applications operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def list(
        self,
        status: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> builtins.list[Application]:
        """List all job applications asynchronously."""
        params: dict[str, Any] = {}
        if status:
            params["status"] = status
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = await self._client._request(
            "GET", "/api/openapi/applications", params=params or None
        )
        if isinstance(response, dict) and "data" in response:
            items = response["data"]
        else:
            items = response
        return [Application.model_validate(item) for item in items]

    async def summary(
        self,
        status: str | None = None,
        tags: builtins.list[str] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> builtins.list[ApplicationSummary]:
        """Retrieve lightweight application summaries asynchronously."""
        params: dict[str, Any] = {}
        if status:
            params["status"] = status
        if tags:
            params["tags"] = ",".join(tags)
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = await self._client._request(
            "GET", "/api/openapi/applications/summary", params=params or None
        )
        if isinstance(response, dict) and "data" in response:
            items = response["data"]
        elif isinstance(response, list):
            items = response
        else:
            items = []
        return [ApplicationSummary.model_validate(item) for item in items]

    async def close(self, app_id: str, reason: str = "not-selected") -> Application:
        """Close an application asynchronously with a closedReason."""
        response = await self._client._request(
            "PATCH",
            f"/api/openapi/applications/{app_id}",
            json={"stage": "closed", "closedReason": reason},
        )
        return Application.model_validate(response)

    async def get(self, app_id: str) -> Application:
        """Retrieve a specific job application by ID asynchronously."""
        response = await self._client._request("GET", f"/api/openapi/applications/{app_id}")
        return Application.model_validate(response)

    async def create(self, data: ApplicationCreate) -> Application:
        """Log/create a new job application asynchronously."""
        payload = data.model_dump(by_alias=True, exclude_none=True)
        response = await self._client._request("POST", "/api/openapi/applications", json=payload)
        return Application.model_validate(response)

    async def delete(self, app_id: str) -> None:
        """Delete a job application by ID asynchronously."""
        await self._client._request("DELETE", f"/api/openapi/applications/{app_id}")

    async def list_tags(self) -> builtins.list[str]:
        """List all application tags asynchronously."""
        response = await self._client._request("GET", "/api/openapi/applications/tags")
        return list(response)

    async def get_pipeline_stats(self) -> dict[str, Any]:
        """Get application pipeline statistics asynchronously."""
        response = await self._client._request("GET", "/api/openapi/applications/stats")
        return dict(response)

    async def bulk_import(self, items: builtins.list[dict[str, Any]]) -> dict[str, Any]:
        """Bulk import job applications asynchronously."""
        payload = {"items": items}
        response = await self._client._request(
            "POST", "/api/openapi/applications/import", json=payload
        )
        return dict(response)

    async def get_lanes(self) -> builtins.list[dict[str, Any]]:
        """Retrieve custom Kanban lanes/stages for applications asynchronously."""
        response = await self._client._request("GET", "/api/openapi/applications/lanes")
        return list(response)

    async def update_lanes(
        self, lanes: builtins.list[dict[str, Any]]
    ) -> builtins.list[dict[str, Any]]:
        """Create or update application Kanban lanes asynchronously."""
        response = await self._client._request(
            "POST", "/api/openapi/applications/lanes", json={"lanes": lanes}
        )
        return list(response)
