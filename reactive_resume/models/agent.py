"""Pydantic models representing AI Agent communication in Reactive Resume."""

from pydantic import BaseModel


class AgentRequest(BaseModel):
    """Payload to send to the AI Agent."""

    prompt: str


class AgentResponse(BaseModel):
    """Response returned by the AI Agent."""

    response: str
