"""Pydantic models representing cover letters in Reactive Resume v6."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CoverLetter(BaseModel):
    """Represents a standalone cover letter document."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    slug: str
    user_id: str | None = Field(None, alias="userId")
    content: str = ""
    tags: list[str] = Field(default_factory=list)
    is_locked: bool = Field(False, alias="isLocked")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    metadata: dict[str, Any] | None = None


class CoverLetterCreate(BaseModel):
    """Payload to create a new cover letter."""

    title: str = Field(..., description="Cover letter title or name")
    slug: str | None = None
    content: str | None = ""
    tags: list[str] | None = None
