"""API endpoints and service groups."""

from .auth import AuthAPI, AsyncAuthAPI
from .resumes import ResumesAPI, AsyncResumesAPI

__all__ = [
    "AuthAPI",
    "AsyncAuthAPI",
    "ResumesAPI",
    "AsyncResumesAPI",
]
