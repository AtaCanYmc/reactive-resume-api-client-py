"""API endpoints and service groups."""

from .agent import AgentAPI, AsyncAgentAPI
from .ai import AIAPI, AsyncAIAPI
from .ai_providers import AiProvidersAPI, AsyncAiProvidersAPI
from .applications import ApplicationsAPI, AsyncApplicationsAPI
from .auth import AsyncAuthAPI, AuthAPI
from .cover_letters import AsyncCoverLettersAPI, CoverLettersAPI
from .custom_domain import AsyncCustomDomainAPI, CustomDomainAPI
from .documents import AsyncDocumentsAPI, DocumentsAPI
from .flags import AsyncFlagsAPI, FlagsAPI
from .resumes import AsyncResumesAPI, ResumesAPI
from .statistics import AsyncStatisticsAPI, StatisticsAPI
from .system import AsyncSystemAPI, SystemAPI

__all__ = [
    "AIAPI",
    "AgentAPI",
    "AiProvidersAPI",
    "ApplicationsAPI",
    "AsyncAIAPI",
    "AsyncAgentAPI",
    "AsyncAiProvidersAPI",
    "AsyncApplicationsAPI",
    "AsyncAuthAPI",
    "AsyncCoverLettersAPI",
    "AsyncCustomDomainAPI",
    "AsyncDocumentsAPI",
    "AsyncFlagsAPI",
    "AsyncResumesAPI",
    "AsyncStatisticsAPI",
    "AsyncSystemAPI",
    "AuthAPI",
    "CoverLettersAPI",
    "CustomDomainAPI",
    "DocumentsAPI",
    "FlagsAPI",
    "ResumesAPI",
    "StatisticsAPI",
    "SystemAPI",
]
