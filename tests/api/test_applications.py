import pytest
import respx
from httpx import Response
from reactive_resume import RxResumeClient, AsyncRxResumeClient
from reactive_resume.models import ApplicationCreate

BASE_URL = "https://rxresu.me"
API_KEY = "test-api-key"

MOCK_APP = {
    "id": "app-123",
    "userId": "user-123",
    "company": "Google",
    "position": "Staff Engineer",
    "stage": "Interviewing",
    "date": "2026-07-13T12:00:00Z",
    "summary": "Interviews scheduled",
    "url": "https://google.com/jobs",
    "createdAt": "2026-07-13T12:00:00Z",
    "updatedAt": "2026-07-13T12:00:00Z",
}


@pytest.fixture
def sync_client():
    with RxResumeClient(base_url=BASE_URL, api_key=API_KEY) as client:
        yield client


@pytest.fixture
async def async_client():
    async with AsyncRxResumeClient(base_url=BASE_URL, api_key=API_KEY) as client:
        yield client


@respx.mock
def test_sync_applications_crud(sync_client):
    # 1. list
    route_list = respx.get(f"{BASE_URL}/api/openapi/applications").mock(
        return_value=Response(200, json=[MOCK_APP])
    )
    apps = sync_client.applications.list()
    assert len(apps) == 1
    assert apps[0].company == "Google"
    assert route_list.called

    # 1b. list paginated wrapper
    route_list_pag = respx.get(f"{BASE_URL}/api/openapi/applications").mock(
        return_value=Response(200, json={"data": [MOCK_APP]})
    )
    apps_pag = sync_client.applications.list()
    assert len(apps_pag) == 1
    assert route_list_pag.called

    # 2. get
    route_get = respx.get(f"{BASE_URL}/api/openapi/applications/app-123").mock(
        return_value=Response(200, json=MOCK_APP)
    )
    app = sync_client.applications.get("app-123")
    assert app.id == "app-123"
    assert route_get.called

    # 3. create
    route_create = respx.post(f"{BASE_URL}/api/openapi/applications").mock(
        return_value=Response(201, json=MOCK_APP)
    )
    new_app = sync_client.applications.create(
        ApplicationCreate(company="Google", position="Staff Engineer")
    )
    assert new_app.id == "app-123"
    assert route_create.called

    # 4. update
    route_patch = respx.patch(f"{BASE_URL}/api/openapi/applications/app-123").mock(
        return_value=Response(200, json=MOCK_APP)
    )
    updated = sync_client.applications.update("app-123", {"stage": "Offered"})
    assert updated.id == "app-123"
    assert route_patch.called

    # 5. delete
    route_delete = respx.delete(f"{BASE_URL}/api/openapi/applications/app-123").mock(
        return_value=Response(204)
    )
    sync_client.applications.delete("app-123")
    assert route_delete.called


@pytest.mark.asyncio
@respx.mock
async def test_async_applications_crud(async_client):
    # 1. list
    route_list = respx.get(f"{BASE_URL}/api/openapi/applications").mock(
        return_value=Response(200, json=[MOCK_APP])
    )
    apps = await async_client.applications.list()
    assert len(apps) == 1
    assert apps[0].company == "Google"
    assert route_list.called

    # 1b. list paginated wrapper
    route_list_pag = respx.get(f"{BASE_URL}/api/openapi/applications").mock(
        return_value=Response(200, json={"data": [MOCK_APP]})
    )
    apps_pag = await async_client.applications.list()
    assert len(apps_pag) == 1
    assert route_list_pag.called

    # 2. get
    route_get = respx.get(f"{BASE_URL}/api/openapi/applications/app-123").mock(
        return_value=Response(200, json=MOCK_APP)
    )
    app = await async_client.applications.get("app-123")
    assert app.id == "app-123"
    assert route_get.called

    # 3. create
    route_create = respx.post(f"{BASE_URL}/api/openapi/applications").mock(
        return_value=Response(201, json=MOCK_APP)
    )
    new_app = await async_client.applications.create(
        ApplicationCreate(company="Google", position="Staff Engineer")
    )
    assert new_app.id == "app-123"
    assert route_create.called

    # 4. update
    route_patch = respx.patch(f"{BASE_URL}/api/openapi/applications/app-123").mock(
        return_value=Response(200, json=MOCK_APP)
    )
    updated = await async_client.applications.update("app-123", {"stage": "Offered"})
    assert updated.id == "app-123"
    assert route_patch.called

    # 5. delete
    route_delete = respx.delete(f"{BASE_URL}/api/openapi/applications/app-123").mock(
        return_value=Response(204)
    )
    await async_client.applications.delete("app-123")
    assert route_delete.called
