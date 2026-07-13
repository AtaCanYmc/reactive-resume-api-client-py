"""Pydantic models representing job applications in Reactive Resume."""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class Application(BaseModel):
    """Represents a job application in the tracker."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    user_id: str = Field(..., alias="userId")
    company: str
    position: str
    stage: str = "Applied"  # Applied, Interviewing, Offered, Rejected
    date: datetime
    summary: str = ""
    url: str = ""
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")


class ApplicationCreate(BaseModel):
    """Payload to log/create a new job application."""

    company: str
    position: str
    stage: Optional[str] = "Applied"
    date: Optional[datetime] = None
    summary: Optional[str] = ""
    url: Optional[str] = ""
