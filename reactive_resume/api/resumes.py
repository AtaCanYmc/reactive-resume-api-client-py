"""Resumes endpoints implementation aligned with Postman collection."""

from typing import List, Dict, Any, Optional
from ..models.resume import Resume, ResumeImportData


class ResumesAPI:
    """Synchronous Resume operations."""

    def __init__(self, client) -> None:
        self._client = client

    def list(self) -> List[Resume]:
        """List all resumes for the authenticated user."""
        response = self._client._request("GET", "/api/openapi/resumes")
        if isinstance(response, dict) and "data" in response:
            items = response["data"]
        else:
            items = response
        return [Resume.model_validate(item) for item in items]

    def get(self, resume_id: str) -> Resume:
        """Retrieve a specific resume by ID."""
        response = self._client._request("GET", f"/api/openapi/resumes/{resume_id}")
        return Resume.model_validate(response)

    def create(self, data: ResumeImportData) -> Resume:
        """Create a new resume."""
        payload = data.model_dump(by_alias=True, exclude_none=True)
        response = self._client._request("POST", "/api/openapi/resumes", json=payload)
        return Resume.model_validate(response)

    def import_resume(self, data: ResumeImportData) -> Resume:
        """Import a resume."""
        payload = data.model_dump(by_alias=True, exclude_none=True)
        response = self._client._request("POST", "/api/openapi/resumes/import", json=payload)
        return Resume.model_validate(response)

    def update(self, resume_id: str, data: Dict[str, Any]) -> Resume:
        """Update a resume using PATCH or PUT (maps to PATCH)."""
        response = self._client._request("PATCH", f"/api/openapi/resumes/{resume_id}", json=data)
        return Resume.model_validate(response)

    def update_put(self, resume_id: str, data: Dict[str, Any]) -> Resume:
        """Update a resume using PUT."""
        response = self._client._request("PUT", f"/api/openapi/resumes/{resume_id}", json=data)
        return Resume.model_validate(response)

    def delete(self, resume_id: str) -> None:
        """Delete a resume by ID."""
        self._client._request("DELETE", f"/api/openapi/resumes/{resume_id}")

    def get_pdf_url(self, resume_id: str) -> str:
        """Get the URL to download the PDF for a specific resume."""
        return f"{self._client.base_url}/api/openapi/resumes/{resume_id}/pdf"

    def tags(self) -> List[str]:
        """List all unique tags among user's resumes."""
        response = self._client._request("GET", "/api/openapi/resumes/tags")
        return list(response)

    def set_password(self, resume_id: str, password: str) -> None:
        """Set a password for a resume."""
        self._client._request(
            "PUT", f"/api/openapi/resumes/{resume_id}/password", json={"password": password}
        )

    def remove_password(self, resume_id: str) -> None:
        """Remove password security from a resume."""
        self._client._request("DELETE", f"/api/openapi/resumes/{resume_id}/password")

    def verify_password(self, resume_id: str, password: str) -> bool:
        """Verify the password of a protected resume."""
        response = self._client._request(
            "POST", f"/api/openapi/resumes/{resume_id}/password", json={"password": password}
        )
        return bool(response.get("success", True))

    def get_public_resume(self, username: str, slug: str) -> Resume:
        """Get a public resume by username and slug."""
        response = self._client._request("GET", f"/api/openapi/resumes/{username}/{slug}")
        return Resume.model_validate(response)

    def get_latest_analysis(self, resume_id: str) -> Dict[str, Any]:
        """Get the latest AI analysis for a resume."""
        response = self._client._request("GET", f"/api/openapi/resumes/{resume_id}/analysis")
        return dict(response)

    def get_versions(self, resume_id: str) -> List[Dict[str, Any]]:
        """Get the version history of a resume."""
        response = self._client._request("GET", f"/api/openapi/resumes/{resume_id}/versions")
        return list(response)

    def duplicate(
        self, resume_id: str, name: str, slug: str, tags: Optional[List[str]] = None
    ) -> Resume:
        """Duplicate an existing resume."""
        payload = {"name": name, "slug": slug, "tags": tags or []}
        response = self._client._request(
            "POST", f"/api/openapi/resumes/{resume_id}/duplicate", json=payload
        )
        return Resume.model_validate(response)

    def lock(self, resume_id: str, is_locked: bool) -> None:
        """Lock or unlock a resume."""
        self._client._request(
            "POST", f"/api/openapi/resumes/{resume_id}/lock", json={"isLocked": is_locked}
        )


class AsyncResumesAPI:
    """Asynchronous Resume operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def list(self) -> List[Resume]:
        """List all resumes asynchronously."""
        response = await self._client._request("GET", "/api/openapi/resumes")
        if isinstance(response, dict) and "data" in response:
            items = response["data"]
        else:
            items = response
        return [Resume.model_validate(item) for item in items]

    async def get(self, resume_id: str) -> Resume:
        """Retrieve a specific resume asynchronously."""
        response = await self._client._request("GET", f"/api/openapi/resumes/{resume_id}")
        return Resume.model_validate(response)

    async def create(self, data: ResumeImportData) -> Resume:
        """Create a new resume asynchronously."""
        payload = data.model_dump(by_alias=True, exclude_none=True)
        response = await self._client._request("POST", "/api/openapi/resumes", json=payload)
        return Resume.model_validate(response)

    async def import_resume(self, data: ResumeImportData) -> Resume:
        """Import a resume asynchronously."""
        payload = data.model_dump(by_alias=True, exclude_none=True)
        response = await self._client._request("POST", "/api/openapi/resumes/import", json=payload)
        return Resume.model_validate(response)

    async def update(self, resume_id: str, data: Dict[str, Any]) -> Resume:
        """Update a resume asynchronously using PATCH."""
        response = await self._client._request(
            "PATCH", f"/api/openapi/resumes/{resume_id}", json=data
        )
        return Resume.model_validate(response)

    async def update_put(self, resume_id: str, data: Dict[str, Any]) -> Resume:
        """Update a resume asynchronously using PUT."""
        response = await self._client._request(
            "PUT", f"/api/openapi/resumes/{resume_id}", json=data
        )
        return Resume.model_validate(response)

    async def delete(self, resume_id: str) -> None:
        """Delete a resume asynchronously."""
        await self._client._request("DELETE", f"/api/openapi/resumes/{resume_id}")

    async def get_pdf_url(self, resume_id: str) -> str:
        """Get the URL to download the PDF asynchronously."""
        return f"{self._client.base_url}/api/openapi/resumes/{resume_id}/pdf"

    async def tags(self) -> List[str]:
        """List all unique tags among user's resumes asynchronously."""
        response = await self._client._request("GET", "/api/openapi/resumes/tags")
        return list(response)

    async def set_password(self, resume_id: str, password: str) -> None:
        """Set a password for a resume asynchronously."""
        await self._client._request(
            "PUT", f"/api/openapi/resumes/{resume_id}/password", json={"password": password}
        )

    async def remove_password(self, resume_id: str) -> None:
        """Remove password security from a resume asynchronously."""
        await self._client._request("DELETE", f"/api/openapi/resumes/{resume_id}/password")

    async def verify_password(self, resume_id: str, password: str) -> bool:
        """Verify the password of a protected resume asynchronously."""
        response = await self._client._request(
            "POST", f"/api/openapi/resumes/{resume_id}/password", json={"password": password}
        )
        return bool(response.get("success", True))

    async def get_public_resume(self, username: str, slug: str) -> Resume:
        """Get a public resume asynchronously."""
        response = await self._client._request("GET", f"/api/openapi/resumes/{username}/{slug}")
        return Resume.model_validate(response)

    async def get_latest_analysis(self, resume_id: str) -> Dict[str, Any]:
        """Get the latest AI analysis asynchronously."""
        response = await self._client._request("GET", f"/api/openapi/resumes/{resume_id}/analysis")
        return dict(response)

    async def get_versions(self, resume_id: str) -> List[Dict[str, Any]]:
        """Get the version history asynchronously."""
        response = await self._client._request("GET", f"/api/openapi/resumes/{resume_id}/versions")
        return list(response)

    async def duplicate(
        self, resume_id: str, name: str, slug: str, tags: Optional[List[str]] = None
    ) -> Resume:
        """Duplicate an existing resume asynchronously."""
        payload = {"name": name, "slug": slug, "tags": tags or []}
        response = await self._client._request(
            "POST", f"/api/openapi/resumes/{resume_id}/duplicate", json=payload
        )
        return Resume.model_validate(response)

    async def lock(self, resume_id: str, is_locked: bool) -> None:
        """Lock or unlock a resume asynchronously."""
        await self._client._request(
            "POST", f"/api/openapi/resumes/{resume_id}/lock", json={"isLocked": is_locked}
        )
