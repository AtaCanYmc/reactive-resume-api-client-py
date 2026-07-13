"""Resumes endpoints implementation."""

from typing import List, Dict, Any
from ..models.resume import Resume, ResumeImportData


class ResumesAPI:
    """Synchronous Resume operations."""

    def __init__(self, client) -> None:
        self._client = client

    def list(self) -> List[Resume]:
        """List all resumes for the authenticated user.

        Returns:
            A list of Resume objects.
        """
        response = self._client._request("GET", "/api/openapi/resumes")
        # The response is usually a list of resume objects
        if isinstance(response, dict) and "data" in response:
            # Handle potential pagination wrapper
            items = response["data"]
        else:
            items = response
        return [Resume.model_validate(item) for item in items]

    def get(self, resume_id: str) -> Resume:
        """Retrieve a specific resume by ID.

        Args:
            resume_id: Unique identifier for the resume.

        Returns:
            The Resume object.
        """
        response = self._client._request("GET", f"/api/openapi/resume/{resume_id}")
        return Resume.model_validate(response)

    def create(self, data: ResumeImportData) -> Resume:
        """Create or import a new resume.

        Args:
            data: ResumeImportData object containing title, basics, and sections.

        Returns:
            The created Resume object.
        """
        # Convert Pydantic model to dict, matching what API expects
        payload = data.model_dump(by_alias=True, exclude_none=True)
        response = self._client._request("POST", "/api/openapi/resumes", json=payload)
        return Resume.model_validate(response)

    def import_resume(self, data: ResumeImportData) -> Resume:
        """Alias for create, importing a resume.

        Args:
            data: ResumeImportData object containing title, basics, and sections.

        Returns:
            The imported Resume object.
        """
        return self.create(data)

    def update(self, resume_id: str, data: Dict[str, Any]) -> Resume:
        """Update a resume (PATCH).

        Args:
            resume_id: Unique identifier for the resume.
            data: Dictionary of properties to update (e.g. JSON Patch or key-value updates).

        Returns:
            The updated Resume object.
        """
        # Reactive Resume v4 supports PATCH with JSON Patch or direct body updates
        response = self._client._request("PATCH", f"/api/openapi/resume/{resume_id}", json=data)
        return Resume.model_validate(response)

    def delete(self, resume_id: str) -> None:
        """Delete a resume by ID.

        Args:
            resume_id: Unique identifier for the resume.
        """
        self._client._request("DELETE", f"/api/openapi/resume/{resume_id}")

    def get_pdf_url(self, resume_id: str) -> str:
        """Get the URL to download the PDF for a specific resume.

        Args:
            resume_id: Unique identifier for the resume.

        Returns:
            The absolute PDF download URL.
        """
        # The print/pdf download URL format in Reactive Resume V4 API
        # Typically of form: {base_url}/api/openapi/resume/{resume_id}/pdf
        return f"{self._client.base_url}/api/openapi/resume/{resume_id}/pdf"


class AsyncResumesAPI:
    """Asynchronous Resume operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def list(self) -> List[Resume]:
        """List all resumes asynchronously.

        Returns:
            A list of Resume objects.
        """
        response = await self._client._request("GET", "/api/openapi/resumes")
        if isinstance(response, dict) and "data" in response:
            items = response["data"]
        else:
            items = response
        return [Resume.model_validate(item) for item in items]

    async def get(self, resume_id: str) -> Resume:
        """Retrieve a specific resume asynchronously.

        Args:
            resume_id: Unique identifier for the resume.

        Returns:
            The Resume object.
        """
        response = await self._client._request("GET", f"/api/openapi/resume/{resume_id}")
        return Resume.model_validate(response)

    async def create(self, data: ResumeImportData) -> Resume:
        """Create or import a new resume asynchronously.

        Args:
            data: ResumeImportData object.

        Returns:
            The created Resume object.
        """
        payload = data.model_dump(by_alias=True, exclude_none=True)
        response = await self._client._request("POST", "/api/openapi/resumes", json=payload)
        return Resume.model_validate(response)

    async def import_resume(self, data: ResumeImportData) -> Resume:
        """Alias for create, importing a resume asynchronously."""
        return await self.create(data)

    async def update(self, resume_id: str, data: Dict[str, Any]) -> Resume:
        """Update a resume asynchronously."""
        response = await self._client._request(
            "PATCH", f"/api/openapi/resume/{resume_id}", json=data
        )
        return Resume.model_validate(response)

    async def delete(self, resume_id: str) -> None:
        """Delete a resume asynchronously."""
        await self._client._request("DELETE", f"/api/openapi/resume/{resume_id}")

    async def get_pdf_url(self, resume_id: str) -> str:
        """Get the URL to download the PDF asynchronously.

        Args:
            resume_id: Unique identifier for the resume.

        Returns:
            The absolute PDF download URL.
        """
        return f"{self._client.base_url}/api/openapi/resume/{resume_id}/pdf"
