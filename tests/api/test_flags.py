import pytest
import respx
from httpx import Response
from reactive_resume import RxResumeClient, AsyncRxResumeClient

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
def test_sync_flags(sync_client):
    route = respx.get(f"{BASE_URL}/api/openapi/flags").mock(
        return_value=Response(200, json={"isSignupsDisabled": False})
    )
    flags = sync_client.flags.list()
    assert flags["isSignupsDisabled"] is False
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_async_flags(async_client):
    route = respx.get(f"{BASE_URL}/api/openapi/flags").mock(
        return_value=Response(200, json={"isSignupsDisabled": False})
    )
    flags = await async_client.flags.list()
    assert flags["isSignupsDisabled"] is False
    assert route.called
