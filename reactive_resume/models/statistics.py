"""Pydantic models representing resume interaction statistics."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class ResumeStats(BaseModel):
    """Represents view and download statistics for a resume."""

    model_config = ConfigDict(populate_by_name=True)

    views: int = 0
    downloads: int = 0
    history: dict[str, Any] = {}
