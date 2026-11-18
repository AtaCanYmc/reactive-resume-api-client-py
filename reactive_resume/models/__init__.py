"""Models module for Pydantic schema validation."""

from .agent import AgentStreamEvent
from .application import Application, ApplicationCreate, ApplicationSummary
from .cover_letter import CoverLetter, CoverLetterCreate
from .health import DependencyHealth, SystemHealth
from .resume import (
    AwardItem,
    Basics,
    CertificationItem,
    CustomItem,
    EducationItem,
    InterestItem,
    Item,
    LanguageItem,
    Profile,
    ProjectItem,
    PublicationItem,
    ReferenceItem,
    Resume,
    ResumeData,
    ResumeImportData,
    ResumeItemDates,
    Section,
    SkillItem,
    URLModel,
    VolunteerItem,
    WorkItem,
)
from .statistics import ResumeStats
from .user import User

__all__ = [
    "AgentStreamEvent",
    "Application",
    "ApplicationCreate",
    "ApplicationSummary",
    "AwardItem",
    "Basics",
    "CertificationItem",
    "CoverLetter",
    "CoverLetterCreate",
    "CustomItem",
    "DependencyHealth",
    "EducationItem",
    "InterestItem",
    "Item",
    "LanguageItem",
    "Profile",
    "ProjectItem",
    "PublicationItem",
    "ReferenceItem",
    "Resume",
    "ResumeData",
    "ResumeImportData",
    "ResumeItemDates",
    "ResumeStats",
    "Section",
    "SkillItem",
    "SystemHealth",
    "URLModel",
    "User",
    "VolunteerItem",
    "WorkItem",
]
