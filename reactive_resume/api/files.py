"""Files API implementation for user uploads (avatar pictures, documents)."""

from typing import Any


class FilesAPI:
    """Synchronous Files operations."""

    def __init__(self, client) -> None:
        self._client = client

    def upload(
        self,
        file_bytes: bytes,
        filename: str = "picture.png",
        content_type: str = "image/png",
    ) -> dict[str, Any]:
        """Upload a file (e.g. profile picture up to 10MB)."""
        response = self._client._request(
            "POST",
            "/api/openapi/files",
            files={"file": (filename, file_bytes, content_type)},
        )
        return dict(response)

    def delete(self, filename: str) -> None:
        """Delete a file by its filename or relative storage path."""
        self._client._request("DELETE", "/api/openapi/files", json={"filename": filename})


class AsyncFilesAPI:
    """Asynchronous Files operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def upload(
        self,
        file_bytes: bytes,
        filename: str = "picture.png",
        content_type: str = "image/png",
    ) -> dict[str, Any]:
        """Upload a file asynchronously."""
        response = await self._client._request(
            "POST",
            "/api/openapi/files",
            files={"file": (filename, file_bytes, content_type)},
        )
        return dict(response)

    async def delete(self, filename: str) -> None:
        """Delete a file asynchronously."""
        await self._client._request("DELETE", "/api/openapi/files", json={"filename": filename})
