"""Pydantic models representing storage files in Reactive Resume."""

from pydantic import BaseModel, Field, ConfigDict


class StorageFile(BaseModel):
    """Represents a file/blob uploaded to Reactive Resume storage."""

    model_config = ConfigDict(populate_by_name=True)

    filename: str
    url: str
    size: int
    mime_type: str = Field(..., alias="mimeType")
