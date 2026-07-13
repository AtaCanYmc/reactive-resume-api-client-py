"""Agent API endpoints implementation."""

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
