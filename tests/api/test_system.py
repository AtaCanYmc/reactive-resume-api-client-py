import pytest
import respx
from httpx import Response

from reactive_resume import AsyncRxResumeClient, RxResumeClient
from reactive_resume.models import SystemHealth

BASE_URL = "https://rxresu.me"

MOCK_HEALTH = {
    "service": "reactive-resume",
    "version": "6.1.1",
    "revision": "a1b2c3d4e5f60718293a4b5c6d7e8f9a0b1c2d3e",
    "status": "healthy",
    "timestamp": "2026-11-18T18:00:00Z",
    "uptime": "14d 2h 30m",
    "database": {"status": "healthy", "latencyMs": 1.5},
    "storage": {"status": "healthy", "latencyMs": 2.1},
    "redis": {"status": "healthy", "latencyMs": 0.8},
}


@pytest.fixture
def sync_client():
    with RxResumeClient(base_url=BASE_URL, api_key="test-key") as client:
        yield client


@pytest.fixture
async def async_client():
    async with AsyncRxResumeClient(base_url=BASE_URL, api_key="test-key") as client:
        yield client


@respx.mock
def test_sync_health(sync_client):
    respx.get(f"{BASE_URL}/api/health").mock(return_value=Response(200, json=MOCK_HEALTH))

    health = sync_client.health()
    assert isinstance(health, SystemHealth)
    assert health.service == "reactive-resume"
    assert health.version == "6.1.1"
    assert health.status == "healthy"
    assert health.database.latency_ms == 1.5
    assert health.storage.status == "healthy"
    assert health.redis is not None
    assert health.redis.latency_ms == 0.8


@respx.mock
async def test_async_health(async_client):
    respx.get(f"{BASE_URL}/api/health").mock(return_value=Response(200, json=MOCK_HEALTH))

    health = await async_client.health()
    assert isinstance(health, SystemHealth)
    assert health.version == "6.1.1"
    assert health.status == "healthy"
