"""Models for AI agent thread and message streaming."""

from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel, Field


class AgentStreamEvent(BaseModel):
    """Represents a Server-Sent Event (SSE) or streaming chunk from an agent run."""

    event: str = "message"
    data: str = ""
    id: str | None = None
    retry: int | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    def json_data(self) -> dict[str, Any] | None:
        """Parse the inner text data as a JSON dictionary if possible."""
        try:
            val = json.loads(self.data)
            return val if isinstance(val, dict) else {"value": val}
        except (ValueError, TypeError):
            return None
