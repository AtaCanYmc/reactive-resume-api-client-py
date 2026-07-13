"""API endpoints and service groups."""

from .auth import AuthAPI, AsyncAuthAPI
from .resumes import ResumesAPI, AsyncResumesAPI
from .applications import ApplicationsAPI, AsyncApplicationsAPI
from .statistics import StatisticsAPI, AsyncStatisticsAPI
from .storage import StorageAPI, AsyncStorageAPI
from .agent import AgentAPI, AsyncAgentAPI
from .ai_providers import AiProvidersAPI, AsyncAiProvidersAPI

__all__ = [
    "AuthAPI",
    "AsyncAuthAPI",
    "ResumesAPI",
    "AsyncResumesAPI",
    "ApplicationsAPI",
    "AsyncApplicationsAPI",
    "StatisticsAPI",
    "AsyncStatisticsAPI",
    "StorageAPI",
    "AsyncStorageAPI",
    "AgentAPI",
    "AsyncAgentAPI",
    "AiProvidersAPI",
    "AsyncAiProvidersAPI",
]
