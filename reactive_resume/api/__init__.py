"""API endpoints and service groups."""

from .agent import AgentAPI, AsyncAgentAPI
from .ai import AIAPI, AsyncAIAPI
from .ai_providers import AiProvidersAPI, AsyncAiProvidersAPI
from .applications import ApplicationsAPI, AsyncApplicationsAPI
from .auth import AsyncAuthAPI, AuthAPI
from .flags import AsyncFlagsAPI, FlagsAPI
from .resumes import AsyncResumesAPI, ResumesAPI
from .statistics import AsyncStatisticsAPI, StatisticsAPI

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
    "AsyncFlagsAPI",
    "AsyncResumesAPI",
    "AsyncStatisticsAPI",
    "AuthAPI",
    "FlagsAPI",
    "ResumesAPI",
    "StatisticsAPI",
]
