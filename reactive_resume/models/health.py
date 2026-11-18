"""Pydantic models representing system health and version."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DependencyHealth(BaseModel):
    """Health status of an external dependency (database, storage, redis)."""

    model_config = ConfigDict(populate_by_name=True)

    status: str
    latency_ms: float = Field(..., alias="latencyMs")
    error: str | None = None


class SystemHealth(BaseModel):
    """Application health and version response from /api/health."""

    model_config = ConfigDict(populate_by_name=True)

    service: str = "reactive-resume"
    version: str
    revision: str | None = None
    status: str
    timestamp: datetime
    uptime: str
    database: DependencyHealth
    storage: DependencyHealth
    redis: DependencyHealth | None = None
