import pytest
import respx
from httpx import Response
from reactive_resume import RxResumeClient, AsyncRxResumeClient
from reactive_resume.models import ResumeStats

BASE_URL = "https://rxresu.me"
API_KEY = "test-api-key"


@pytest.fixture
def sync_client():
    with RxResumeClient(base_url=BASE_URL, api_key=API_KEY) as client:
        yield client


@pytest.fixture
async def async_client():
    async with AsyncRxResumeClient(base_url=BASE_URL, api_key=API_KEY) as client:
        yield client


@respx.mock
def test_sync_statistics(sync_client):
    mock_stats = {"views": 100, "downloads": 25, "history": {}}
    route = respx.get(f"{BASE_URL}/api/openapi/statistics/resume-123").mock(
        return_value=Response(200, json=mock_stats)
    )
    stats = sync_client.statistics.get("resume-123")
    assert isinstance(stats, ResumeStats)
    assert stats.views == 100
    assert stats.downloads == 25
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_async_statistics(async_client):
    mock_stats = {"views": 100, "downloads": 25, "history": {}}
    route = respx.get(f"{BASE_URL}/api/openapi/statistics/resume-123").mock(
        return_value=Response(200, json=mock_stats)
    )
    stats = await async_client.statistics.get("resume-123")
    assert isinstance(stats, ResumeStats)
    assert stats.views == 100
    assert stats.downloads == 25
    assert route.called
