"""Agent API endpoints implementation."""

from typing import List, Dict, Any
from ..models.agent import AgentRequest, AgentResponse


class AgentAPI:
    """Synchronous AI Agent operations."""

    def __init__(self, client) -> None:
        self._client = client

    def chat(self, resume_id: str, prompt: str) -> AgentResponse:
        """Send a prompt to the AI Agent relative to a specific resume context."""
        payload = AgentRequest(prompt=prompt).model_dump()
        response = self._client._request(
            "POST",
            f"/api/openapi/agent/{resume_id}/chat",
            json=payload,
        )
        return AgentResponse.model_validate(response)

    def list_threads(self) -> List[Dict[str, Any]]:
        """List all active agent threads."""
        response = self._client._request("GET", "/api/openapi/agent/threads")
        return list(response)

    def get_thread(self, thread_id: str) -> Dict[str, Any]:
        """Get details of a specific agent thread by ID."""
        response = self._client._request("GET", f"/api/openapi/agent/threads/{thread_id}")
        return dict(response)


class AsyncAgentAPI:
    """Asynchronous AI Agent operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def chat(self, resume_id: str, prompt: str) -> AgentResponse:
        """Send a prompt to the AI Agent asynchronously relative to a specific resume context."""
        payload = AgentRequest(prompt=prompt).model_dump()
        response = await self._client._request(
            "POST",
            f"/api/openapi/agent/{resume_id}/chat",
            json=payload,
        )
        return AgentResponse.model_validate(response)

    async def list_threads(self) -> List[Dict[str, Any]]:
        """List all active agent threads asynchronously."""
        response = await self._client._request("GET", "/api/openapi/agent/threads")
        return list(response)

    async def get_thread(self, thread_id: str) -> Dict[str, Any]:
        """Get details of a specific agent thread by ID asynchronously."""
        response = await self._client._request("GET", f"/api/openapi/agent/threads/{thread_id}")
        return dict(response)
