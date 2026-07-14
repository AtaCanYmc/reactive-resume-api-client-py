"""AI API endpoints implementation."""

from typing import Dict, Any


class AIAPI:
    """Synchronous AI operations."""

    def __init__(self, client) -> None:
        self._client = client

    def parse_pdf(self, file_name: str, file_data: str, provider_id: str) -> Dict[str, Any]:
        """Parse a PDF file into resume data.

        Args:
            file_name: Name of the file.
            file_data: Base64 or binary data representation.
            provider_id: The ID of the configured AI provider.
        """
        payload = {
            "file": {"name": file_name, "data": file_data},
            "aiProviderId": provider_id,
        }
        response = self._client._request("POST", "/api/openapi/ai/parse-pdf", json=payload)
        return dict(response)

    def parse_docx(self, file_name: str, file_data: str, provider_id: str) -> Dict[str, Any]:
        """Parse a DOCX file into resume data."""
        payload = {
            "file": {"name": file_name, "data": file_data},
            "aiProviderId": provider_id,
        }
        response = self._client._request("POST", "/api/openapi/ai/parse-docx", json=payload)
        return dict(response)

    def chat(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Chat with AI to modify resume."""
        response = self._client._request("POST", "/api/openapi/ai/chat", json=payload)
        return dict(response)

    def analyze_resume(self, resume_id: str, provider_id: str) -> Dict[str, Any]:
        """Analyze a resume and persist the latest analysis."""
        payload = {
            "resumeId": resume_id,
            "aiProviderId": provider_id,
        }
        response = self._client._request("POST", "/api/openapi/ai/analyze-resume", json=payload)
        return dict(response)


class AsyncAIAPI:
    """Asynchronous AI operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def parse_pdf(self, file_name: str, file_data: str, provider_id: str) -> Dict[str, Any]:
        """Parse a PDF file into resume data asynchronously."""
        payload = {
            "file": {"name": file_name, "data": file_data},
            "aiProviderId": provider_id,
        }
        response = await self._client._request("POST", "/api/openapi/ai/parse-pdf", json=payload)
        return dict(response)

    async def parse_docx(self, file_name: str, file_data: str, provider_id: str) -> Dict[str, Any]:
        """Parse a DOCX file into resume data asynchronously."""
        payload = {
            "file": {"name": file_name, "data": file_data},
            "aiProviderId": provider_id,
        }
        response = await self._client._request("POST", "/api/openapi/ai/parse-docx", json=payload)
        return dict(response)

    async def chat(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Chat with AI asynchronously to modify resume."""
        response = await self._client._request("POST", "/api/openapi/ai/chat", json=payload)
        return dict(response)

    async def analyze_resume(self, resume_id: str, provider_id: str) -> Dict[str, Any]:
        """Analyze a resume asynchronously and persist the latest analysis."""
        payload = {
            "resumeId": resume_id,
            "aiProviderId": provider_id,
        }
        response = await self._client._request(
            "POST", "/api/openapi/ai/analyze-resume", json=payload
        )
        return dict(response)
