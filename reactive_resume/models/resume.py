"""Pydantic models representing resume data in Reactive Resume."""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any, Union


class URLModel(BaseModel):
    """Represents a URL structure in Reactive Resume."""

    label: str = ""
    href: str = ""


class Profile(BaseModel):
    """Represents a social media profile link."""

    id: Optional[str] = None
    network: str = ""
    username: str = ""
    url: Union[URLModel, str] = ""


class Basics(BaseModel):
    """Represents the basic personal information of a candidate."""

    name: str = ""
    headline: str = ""
    email: str = ""
    phone: str = ""
    website: Union[URLModel, str] = ""
    location: str = ""
    picture: str = ""
    profiles: List[Profile] = Field(default_factory=list)


# General item model for list items
class Item(BaseModel):
    """Base model for list items within sections."""

    id: str
    visible: bool = True


class WorkItem(Item):
    """Represents a work experience entry."""

    company: str = ""
    position: str = ""
    location: str = ""
    date: str = ""
    summary: str = ""
    url: Union[URLModel, str] = ""


class EducationItem(Item):
    """Represents an education entry."""

    institution: str = ""
    study_type: str = Field("", alias="studyType")
    area: str = ""
    score: str = ""
    date: str = ""
    summary: str = ""
    url: Union[URLModel, str] = ""

    model_config = ConfigDict(populate_by_name=True)


class ProjectItem(Item):
    """Represents a project entry."""

    name: str = ""
    description: str = ""
    date: str = ""
    summary: str = ""
    keywords: List[str] = Field(default_factory=list)
    url: Union[URLModel, str] = ""


class SkillItem(Item):
    """Represents a skill entry."""

    name: str = ""
    description: str = ""
    level: str = ""
    keywords: List[str] = Field(default_factory=list)


class LanguageItem(Item):
    """Represents a language entry."""

    name: str = ""
    description: str = ""
    level: str = ""


class CertificationItem(Item):
    """Represents a certification entry."""

    name: str = ""
    issuer: str = ""
    date: str = ""
    summary: str = ""
    url: Union[URLModel, str] = ""


class AwardItem(Item):
    """Represents an award or honor entry."""

    title: str = ""
    awarder: str = ""
    date: str = ""
    summary: str = ""
    url: Union[URLModel, str] = ""


class InterestItem(Item):
    """Represents an interest entry."""

    name: str = ""
    keywords: List[str] = Field(default_factory=list)


class ReferenceItem(Item):
    """Represents a reference entry."""

    name: str = ""
    relationship: str = ""
    summary: str = ""
    url: Union[URLModel, str] = ""


class PublicationItem(Item):
    """Represents a publication entry."""

    name: str = ""
    publisher: str = ""
    date: str = ""
    summary: str = ""
    url: Union[URLModel, str] = ""


class VolunteerItem(Item):
    """Represents a volunteer work entry."""

    organization: str = ""
    position: str = ""
    location: str = ""
    date: str = ""
    summary: str = ""
    url: Union[URLModel, str] = ""


class CustomItem(Item):
    """Represents a custom item entry in custom sections."""

    title: str = ""
    subtitle: str = ""
    date: str = ""
    summary: str = ""
    url: Union[URLModel, str] = ""


# Section Models
class Section(BaseModel):
    """Base schema for a resume section."""

    id: str
    name: str
    columns: int = 1
    visible: bool = True
    items: List[Any] = Field(default_factory=list)


class ResumeData(BaseModel):
    """Contains all actual resume sections and basic details."""

    basics: Basics = Field(default_factory=Basics)
    sections: Dict[str, Section] = Field(default_factory=dict)


class Resume(BaseModel):
    """Represents a complete resume object returned by the API."""

    id: str
    name: str
    slug: str
    user_id: Optional[str] = Field(None, alias="userId")
    visibility: str = "public"
    locked: bool = False
    data: Optional[ResumeData] = None
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)


class ResumeImportData(BaseModel):
    """Schema for importing/creating a new resume."""

    title: str = Field(..., description="The name/title of the resume")
    slug: Optional[str] = Field(None, description="Optional custom URL slug")
    basics: Optional[Basics] = None
    sections: Optional[Dict[str, Section]] = None
    metadata: Optional[Dict[str, Any]] = None
