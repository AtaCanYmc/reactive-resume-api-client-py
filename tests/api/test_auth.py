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
def test_sync_auth_endpoints(sync_client):
    mock_user = {
        "id": "user-123",
        "name": "Ata Can",
        "username": "atacan",
        "email": "ata@example.com",
        "provider": "email",
        "createdAt": "2026-07-13T12:00:00Z",
        "updatedAt": "2026-07-13T12:00:00Z",
    }

    # providers
    route_providers = respx.get(f"{BASE_URL}/api/openapi/auth/providers").mock(
        return_value=Response(200, json=["email", "github"])
    )
    providers = sync_client.auth.list_providers()
    assert "github" in providers
    assert route_providers.called

    # export
    route_export = respx.get(f"{BASE_URL}/api/openapi/auth/account/export").mock(
        return_value=Response(200, json={"user": mock_user})
    )
    export_data = sync_client.auth.export_account()
    assert "user" in export_data
    assert route_export.called

    # delete
    route_delete = respx.delete(f"{BASE_URL}/api/openapi/auth/account").mock(
        return_value=Response(204)
    )
    sync_client.auth.delete_account()
    assert route_delete.called


@pytest.mark.asyncio
@respx.mock
async def test_async_auth_endpoints(async_client):
    mock_user = {
        "id": "user-123",
        "name": "Ata Can",
        "username": "atacan",
        "email": "ata@example.com",
        "provider": "email",
        "createdAt": "2026-07-13T12:00:00Z",
        "updatedAt": "2026-07-13T12:00:00Z",
    }

    # providers
    route_providers = respx.get(f"{BASE_URL}/api/openapi/auth/providers").mock(
        return_value=Response(200, json=["email", "github"])
    )
    providers = await async_client.auth.list_providers()
    assert "github" in providers
    assert route_providers.called

    # export
    route_export = respx.get(f"{BASE_URL}/api/openapi/auth/account/export").mock(
        return_value=Response(200, json={"user": mock_user})
    )
    export_data = await async_client.auth.export_account()
    assert "user" in export_data
    assert route_export.called

    # delete
    route_delete = respx.delete(f"{BASE_URL}/api/openapi/auth/account").mock(
        return_value=Response(204)
    )
    await async_client.auth.delete_account()
    assert route_delete.called
