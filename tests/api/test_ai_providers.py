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
def test_sync_ai_providers(sync_client):
    mock_providers = [{"name": "openai", "enabled": True}]
    route = respx.get(f"{BASE_URL}/api/openapi/ai-providers").mock(
        return_value=Response(200, json=mock_providers)
    )
    providers = sync_client.ai_providers.list()
    assert len(providers) == 1
    assert providers[0]["name"] == "openai"
    assert route.called

    route_create = respx.post(f"{BASE_URL}/api/openapi/ai-providers").mock(
        return_value=Response(201, json={"id": "provider-1", "label": "GPT-4"})
    )
    new_provider = sync_client.ai_providers.create("GPT-4", "gpt-4", "sk-123")
    assert new_provider["id"] == "provider-1"
    assert route_create.called

    route_delete = respx.delete(f"{BASE_URL}/api/openapi/ai-providers/provider-1").mock(
        return_value=Response(204)
    )
    sync_client.ai_providers.delete("provider-1")
    assert route_delete.called

    route_test = respx.post(f"{BASE_URL}/api/openapi/ai-providers/provider-1/test").mock(
        return_value=Response(200, json={"success": True})
    )
    assert sync_client.ai_providers.test("provider-1") is True
    assert route_test.called

    route_update = respx.patch(f"{BASE_URL}/api/openapi/ai-providers/provider-1").mock(
        return_value=Response(200, json={"enabled": False})
    )
    updated = sync_client.ai_providers.update("provider-1", {"enabled": False})
    assert updated["enabled"] is False
    assert route_update.called


@pytest.mark.asyncio
@respx.mock
async def test_async_ai_providers(async_client):
    mock_providers = [{"name": "openai", "enabled": True}]
    route = respx.get(f"{BASE_URL}/api/openapi/ai-providers").mock(
        return_value=Response(200, json=mock_providers)
    )
    providers = await async_client.ai_providers.list()
    assert len(providers) == 1
    assert providers[0]["name"] == "openai"
    assert route.called

    route_create = respx.post(f"{BASE_URL}/api/openapi/ai-providers").mock(
        return_value=Response(201, json={"id": "provider-1", "label": "GPT-4"})
    )
    new_provider = await async_client.ai_providers.create("GPT-4", "gpt-4", "sk-123")
    assert new_provider["id"] == "provider-1"
    assert route_create.called

    route_delete = respx.delete(f"{BASE_URL}/api/openapi/ai-providers/provider-1").mock(
        return_value=Response(204)
    )
    await async_client.ai_providers.delete("provider-1")
    assert route_delete.called

    route_test = respx.post(f"{BASE_URL}/api/openapi/ai-providers/provider-1/test").mock(
        return_value=Response(200, json={"success": True})
    )
    assert await async_client.ai_providers.test("provider-1") is True
    assert route_test.called

    route_update = respx.patch(f"{BASE_URL}/api/openapi/ai-providers/provider-1").mock(
        return_value=Response(200, json={"enabled": False})
    )
    updated = await async_client.ai_providers.update("provider-1", {"enabled": False})
    assert updated["enabled"] is False
    assert route_update.called
