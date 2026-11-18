"""Cover Letters endpoints implementation aligned with Reactive Resume v6."""

import builtins
from typing import Any

from ..models.cover_letter import CoverLetter, CoverLetterCreate


class CoverLettersAPI:
    """Synchronous Cover Letter operations."""

    def __init__(self, client) -> None:
        self._client = client

    def list(
        self, limit: int | None = None, offset: int | None = None
    ) -> builtins.list[CoverLetter]:
        """List all cover letters for the authenticated user."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = self._client._request("GET", "/api/openapi/cover-letters", params=params or None)
        if isinstance(response, dict) and "items" in response:
            items = response["items"]
        elif isinstance(response, dict) and "data" in response:
            items = response["data"]
        elif isinstance(response, list):
            items = response
        else:
            items = []
        return [CoverLetter.model_validate(item) for item in items]

    def get(self, letter_id: str) -> CoverLetter:
        """Retrieve a specific cover letter by ID."""
        response = self._client._request("GET", f"/api/openapi/cover-letters/{letter_id}")
        return CoverLetter.model_validate(response)

    def create(self, data: CoverLetterCreate | dict[str, Any]) -> CoverLetter:
        """Create a new cover letter."""
        payload = (
            data.model_dump(by_alias=True, exclude_none=True)
            if hasattr(data, "model_dump")
            else data
        )
        response = self._client._request("POST", "/api/openapi/cover-letters", json=payload)
        return CoverLetter.model_validate(response)

    def update(self, letter_id: str, data: dict[str, Any]) -> CoverLetter:
        """Update a cover letter."""
        response = self._client._request(
            "PATCH", f"/api/openapi/cover-letters/{letter_id}", json=data
        )
        return CoverLetter.model_validate(response)

    def delete(self, letter_id: str) -> None:
        """Delete a cover letter (moves to Trash)."""
        self._client._request("DELETE", f"/api/openapi/cover-letters/{letter_id}")

    def export(self, letter_id: str, format: str = "pdf") -> bytes:
        """Export cover letter as a downloadable file (pdf, docx, md, json)."""
        response = self._client._request(
            "GET", f"/api/openapi/cover-letters/{letter_id}/exports/{format}"
        )
        return response if isinstance(response, bytes) else str(response).encode()


class AsyncCoverLettersAPI:
    """Asynchronous Cover Letter operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def list(
        self, limit: int | None = None, offset: int | None = None
    ) -> builtins.list[CoverLetter]:
        """List all cover letters asynchronously."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = await self._client._request(
            "GET", "/api/openapi/cover-letters", params=params or None
        )
        if isinstance(response, dict) and "items" in response:
            items = response["items"]
        elif isinstance(response, dict) and "data" in response:
            items = response["data"]
        elif isinstance(response, list):
            items = response
        else:
            items = []
        return [CoverLetter.model_validate(item) for item in items]

    async def get(self, letter_id: str) -> CoverLetter:
        """Retrieve a specific cover letter by ID asynchronously."""
        response = await self._client._request("GET", f"/api/openapi/cover-letters/{letter_id}")
        return CoverLetter.model_validate(response)

    async def create(self, data: CoverLetterCreate | dict[str, Any]) -> CoverLetter:
        """Create a new cover letter asynchronously."""
        payload = (
            data.model_dump(by_alias=True, exclude_none=True)
            if hasattr(data, "model_dump")
            else data
        )
        response = await self._client._request("POST", "/api/openapi/cover-letters", json=payload)
        return CoverLetter.model_validate(response)

    async def update(self, letter_id: str, data: dict[str, Any]) -> CoverLetter:
        """Update a cover letter asynchronously."""
        response = await self._client._request(
            "PATCH", f"/api/openapi/cover-letters/{letter_id}", json=data
        )
        return CoverLetter.model_validate(response)

    async def delete(self, letter_id: str) -> None:
        """Delete a cover letter asynchronously."""
        await self._client._request("DELETE", f"/api/openapi/cover-letters/{letter_id}")

    async def export(self, letter_id: str, format: str = "pdf") -> bytes:
        """Export cover letter asynchronously."""
        response = await self._client._request(
            "GET", f"/api/openapi/cover-letters/{letter_id}/exports/{format}"
        )
        return response if isinstance(response, bytes) else str(response).encode()
