"""API endpoints and service groups."""

from .auth import AuthAPI, AsyncAuthAPI
from .resumes import ResumesAPI, AsyncResumesAPI
from .statistics import StatisticsAPI, AsyncStatisticsAPI
from .agent import AgentAPI, AsyncAgentAPI
from .ai_providers import AiProvidersAPI, AsyncAiProvidersAPI
from .flags import FlagsAPI, AsyncFlagsAPI
from .ai import AIAPI, AsyncAIAPI

__all__ = [
    "AuthAPI",
    "AsyncAuthAPI",
    "ResumesAPI",
    "AsyncResumesAPI",
    "StatisticsAPI",
    "AsyncStatisticsAPI",
    "AgentAPI",
    "AsyncAgentAPI",
    "AiProvidersAPI",
    "AsyncAiProvidersAPI",
    "FlagsAPI",
    "AsyncFlagsAPI",
    "AIAPI",
    "AsyncAIAPI",
]
