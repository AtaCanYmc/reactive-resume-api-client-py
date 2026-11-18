"""Documents and Trash API endpoints implementation aligned with Reactive Resume v6."""

from typing import Any


class DocumentsAPI:
    """Synchronous Document lifecycle and trash management."""

    def __init__(self, client) -> None:
        self._client = client

    def get_counts(self) -> dict[str, Any]:
        """Retrieve total counts of documents, cover letters, and trash items."""
        response = self._client._request("GET", "/api/openapi/documents/counts")
        return dict(response)

    def trash(self, doc_type: str, doc_id: str) -> None:
        """Move a document (resume or cover-letter) to trash for 30 days."""
        self._client._request("PUT", f"/api/openapi/documents/{doc_type}/{doc_id}/trash")

    def restore(self, doc_id: str, doc_type: str = "resume") -> None:
        """Restore a trashed document back to active documents."""
        self._client._request(
            "POST", "/api/openapi/documents/restore", json={"id": doc_id, "type": doc_type}
        )

    def purge(self, doc_id: str, doc_type: str = "resume") -> None:
        """Permanently delete a document from trash."""
        self._client._request(
            "POST", "/api/openapi/documents/purge", json={"id": doc_id, "type": doc_type}
        )


class AsyncDocumentsAPI:
    """Asynchronous Document lifecycle and trash management."""

    def __init__(self, client) -> None:
        self._client = client

    async def get_counts(self) -> dict[str, Any]:
        """Retrieve total counts of documents asynchronously."""
        response = await self._client._request("GET", "/api/openapi/documents/counts")
        return dict(response)

    async def trash(self, doc_type: str, doc_id: str) -> None:
        """Move a document to trash asynchronously."""
        await self._client._request("PUT", f"/api/openapi/documents/{doc_type}/{doc_id}/trash")

    async def restore(self, doc_id: str, doc_type: str = "resume") -> None:
        """Restore a trashed document asynchronously."""
        await self._client._request(
            "POST", "/api/openapi/documents/restore", json={"id": doc_id, "type": doc_type}
        )

    async def purge(self, doc_id: str, doc_type: str = "resume") -> None:
        """Permanently delete a document asynchronously."""
        await self._client._request(
            "POST", "/api/openapi/documents/purge", json={"id": doc_id, "type": doc_type}
        )
