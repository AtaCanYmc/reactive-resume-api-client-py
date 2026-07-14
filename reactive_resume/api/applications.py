"""Applications API endpoints implementation."""

from typing import List, Dict, Any
from ..models.application import Application, ApplicationCreate


class ApplicationsAPI:
    """Synchronous Job Applications operations."""

    def __init__(self, client) -> None:
        self._client = client

    def list(self) -> List[Application]:
        """List all job applications."""
        response = self._client._request("GET", "/api/openapi/applications")
        if isinstance(response, dict) and "data" in response:
            items = response["data"]
        else:
            items = response
        return [Application.model_validate(item) for item in items]

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

    def list_tags(self) -> List[str]:
        """List all application tags."""
        response = self._client._request("GET", "/api/openapi/applications/tags")
        return list(response)

    def get_pipeline_stats(self) -> Dict[str, Any]:
        """Get application pipeline statistics."""
        response = self._client._request("GET", "/api/openapi/applications/stats")
        return dict(response)

    def bulk_import(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Bulk import job applications."""
        payload = {"items": items}
        response = self._client._request("POST", "/api/openapi/applications/import", json=payload)
        return dict(response)


class AsyncApplicationsAPI:
    """Asynchronous Job Applications operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def list(self) -> List[Application]:
        """List all job applications asynchronously."""
        response = await self._client._request("GET", "/api/openapi/applications")
        if isinstance(response, dict) and "data" in response:
            items = response["data"]
        else:
            items = response
        return [Application.model_validate(item) for item in items]

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

    async def list_tags(self) -> List[str]:
        """List all application tags asynchronously."""
        response = await self._client._request("GET", "/api/openapi/applications/tags")
        return list(response)

    async def get_pipeline_stats(self) -> Dict[str, Any]:
        """Get application pipeline statistics asynchronously."""
        response = await self._client._request("GET", "/api/openapi/applications/stats")
        return dict(response)

    async def bulk_import(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Bulk import job applications asynchronously."""
        payload = {"items": items}
        response = await self._client._request(
            "POST", "/api/openapi/applications/import", json=payload
        )
        return dict(response)
