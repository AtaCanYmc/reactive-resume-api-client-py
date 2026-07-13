"""Pydantic models representing user accounts in Reactive Resume."""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime


class User(BaseModel):
    """Represents a user account in Reactive Resume."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique identifier for the user")
    name: str = Field(..., description="Full name of the user")
    username: str = Field(..., description="Username of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    provider: str = Field(
        "email", description="Authentication provider (e.g., email, github, google)"
    )
    created_at: datetime = Field(
        ..., alias="createdAt", description="Timestamp when the user was created"
    )
    updated_at: datetime = Field(
        ..., alias="updatedAt", description="Timestamp when the user was last updated"
    )
