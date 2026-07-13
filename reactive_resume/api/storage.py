"""Storage API endpoints implementation."""

from ..models.storage import StorageFile


class StorageAPI:
    """Synchronous Storage operations."""

    def __init__(self, client) -> None:
        self._client = client

    def upload_file(self, file_content: bytes, filename: str) -> StorageFile:
        """Upload a file to storage.

        Args:
            file_content: Raw bytes of the file.
            filename: Target name for the uploaded file.

        Returns:
            Metadata details of the uploaded file.
        """
        files = {"file": (filename, file_content)}
        response = self._client._request(
            "POST",
            "/api/openapi/storage/upload",
            files=files,
        )
        return StorageFile.model_validate(response)


class AsyncStorageAPI:
    """Asynchronous Storage operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def upload_file(self, file_content: bytes, filename: str) -> StorageFile:
        """Upload a file to storage asynchronously.

        Args:
            file_content: Raw bytes of the file.
            filename: Target name for the uploaded file.

        Returns:
            Metadata details of the uploaded file.
        """
        files = {"file": (filename, file_content)}
        response = await self._client._request(
            "POST",
            "/api/openapi/storage/upload",
            files=files,
        )
        return StorageFile.model_validate(response)
