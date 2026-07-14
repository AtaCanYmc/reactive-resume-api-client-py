import pytest
import respx
from httpx import Response
from reactive_resume import RxResumeClient, AsyncRxResumeClient
from reactive_resume.models import User

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

    # login
    route_login = respx.post(f"{BASE_URL}/api/auth/login").mock(
        return_value=Response(200, json={"token": "jwt-token", "user": mock_user})
    )
    token, user = sync_client.auth.login("ata@example.com", "password")
    assert token == "jwt-token"
    assert isinstance(user, User)
    assert user.name == "Ata Can"
    assert route_login.called

    # me
    route_me = respx.get(f"{BASE_URL}/api/user/me").mock(return_value=Response(200, json=mock_user))
    me = sync_client.auth.me()
    assert isinstance(me, User)
    assert me.id == "user-123"
    assert route_me.called

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

    # login
    route_login = respx.post(f"{BASE_URL}/api/auth/login").mock(
        return_value=Response(200, json={"token": "jwt-token", "user": mock_user})
    )
    token, user = await async_client.auth.login("ata@example.com", "password")
    assert token == "jwt-token"
    assert isinstance(user, User)
    assert user.name == "Ata Can"
    assert route_login.called

    # me
    route_me = respx.get(f"{BASE_URL}/api/user/me").mock(return_value=Response(200, json=mock_user))
    me = await async_client.auth.me()
    assert isinstance(me, User)
    assert me.id == "user-123"
    assert route_me.called

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
