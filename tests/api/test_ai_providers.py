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
def test_sync_ai_providers_list(sync_client):
    mock_providers = [{"name": "openai", "enabled": True}]
    route = respx.get(f"{BASE_URL}/api/openapi/ai-providers").mock(
        return_value=Response(200, json=mock_providers)
    )
    providers = sync_client.ai_providers.list()
    assert len(providers) == 1
    assert providers[0]["name"] == "openai"
    assert route.called

    # Test single-provider dict response fallback coverage
    route_single = respx.get(f"{BASE_URL}/api/openapi/ai-providers").mock(
        return_value=Response(200, json={"name": "anthropic"})
    )
    providers_single = sync_client.ai_providers.list()
    assert len(providers_single) == 1
    assert providers_single[0]["name"] == "anthropic"
    assert route_single.called


@pytest.mark.asyncio
@respx.mock
async def test_async_ai_providers_list(async_client):
    mock_providers = [{"name": "openai", "enabled": True}]
    route = respx.get(f"{BASE_URL}/api/openapi/ai-providers").mock(
        return_value=Response(200, json=mock_providers)
    )
    providers = await async_client.ai_providers.list()
    assert len(providers) == 1
    assert providers[0]["name"] == "openai"
    assert route.called

    # Test single-provider dict response fallback coverage
    route_single = respx.get(f"{BASE_URL}/api/openapi/ai-providers").mock(
        return_value=Response(200, json={"name": "anthropic"})
    )
    providers_single = await async_client.ai_providers.list()
    assert len(providers_single) == 1
    assert providers_single[0]["name"] == "anthropic"
    assert route_single.called
