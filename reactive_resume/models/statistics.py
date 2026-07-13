"""Pydantic models representing resume interaction statistics."""

from pydantic import BaseModel, ConfigDict
from typing import Dict, Any


class ResumeStats(BaseModel):
    """Represents view and download statistics for a resume."""

    model_config = ConfigDict(populate_by_name=True)

    views: int = 0
    downloads: int = 0
    history: Dict[str, Any] = {}
