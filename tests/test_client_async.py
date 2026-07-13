import pytest
import respx
import httpx
from httpx import Response
from reactive_resume import (
    AsyncRxResumeClient,
    AuthenticationError,
    NotFoundError,
    ReactiveResumeAPIError,
    ReactiveResumeError,
)
from reactive_resume.models import ResumeImportData, Resume, User

BASE_URL = "https://rxresu.me"
API_KEY = "test-api-key"


@pytest.fixture
async def async_client():
    async with AsyncRxResumeClient(base_url=BASE_URL, api_key=API_KEY) as c:
        yield c


@pytest.mark.asyncio
@respx.mock
async def test_list_resumes_async(async_client):
    mock_resume = {
        "id": "test-resume-id",
        "name": "Test CV",
        "slug": "test-cv",
        "userId": "user-123",
        "visibility": "public",
        "locked": False,
        "data": {
            "basics": {
                "name": "John Doe",
                "headline": "Software Developer",
                "email": "john@example.com",
                "phone": "123456",
                "website": "https://john.me",
                "location": "Earth",
                "picture": "",
                "profiles": [],
            },
            "sections": {},
        },
        "createdAt": "2026-07-13T12:00:00Z",
        "updatedAt": "2026-07-13T12:00:00Z",
    }

    route = respx.get(f"{BASE_URL}/api/openapi/resumes").mock(
        return_value=Response(200, json=[mock_resume])
    )

    resumes = await async_client.resumes.list()
    assert len(resumes) == 1
    assert isinstance(resumes[0], Resume)
    assert resumes[0].id == "test-resume-id"
    assert resumes[0].data.basics.name == "John Doe"
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_get_resume_async(async_client):
    mock_resume = {
        "id": "resume-1",
        "name": "Test CV 1",
        "slug": "test-cv-1",
        "userId": "user-123",
        "data": {"basics": {}, "sections": {}},
        "createdAt": "2026-07-13T12:00:00Z",
        "updatedAt": "2026-07-13T12:00:00Z",
    }
    route = respx.get(f"{BASE_URL}/api/openapi/resume/resume-1").mock(
        return_value=Response(200, json=mock_resume)
    )

    resume = await async_client.resumes.get("resume-1")
    assert resume.id == "resume-1"
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_create_resume_async(async_client):
    mock_resume = {
        "id": "new-resume",
        "name": "My New CV",
        "slug": "my-new-cv",
        "userId": "user-123",
        "data": {"basics": {}, "sections": {}},
        "createdAt": "2026-07-13T12:00:00Z",
        "updatedAt": "2026-07-13T12:00:00Z",
    }
    route = respx.post(f"{BASE_URL}/api/openapi/resumes").mock(
        return_value=Response(201, json=mock_resume)
    )

    import_data = ResumeImportData(title="My New CV")
    resume = await async_client.resumes.import_resume(import_data)
    assert resume.id == "new-resume"
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_update_resume_async(async_client):
    mock_resume = {
        "id": "resume-1",
        "name": "Updated CV Name",
        "slug": "updated-cv-name",
        "userId": "user-123",
        "data": {"basics": {}, "sections": {}},
        "createdAt": "2026-07-13T12:00:00Z",
        "updatedAt": "2026-07-13T12:00:00Z",
    }
    route = respx.patch(f"{BASE_URL}/api/openapi/resume/resume-1").mock(
        return_value=Response(200, json=mock_resume)
    )

    resume = await async_client.resumes.update("resume-1", {"name": "Updated CV Name"})
    assert resume.name == "Updated CV Name"
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_delete_resume_async(async_client):
    route = respx.delete(f"{BASE_URL}/api/openapi/resume/resume-1").mock(return_value=Response(204))
    await async_client.resumes.delete("resume-1")
    assert route.called


@pytest.mark.asyncio
async def test_get_pdf_url_async(async_client):
    pdf_url = await async_client.resumes.get_pdf_url("resume-1")
    assert pdf_url == f"{BASE_URL}/api/openapi/resume/resume-1/pdf"


@pytest.mark.asyncio
@respx.mock
async def test_auth_login_async(async_client):
    mock_user = {
        "id": "user-123",
        "name": "Ata Can",
        "username": "atacan",
        "email": "ata@example.com",
        "provider": "email",
        "createdAt": "2026-07-13T12:00:00Z",
        "updatedAt": "2026-07-13T12:00:00Z",
    }
    route = respx.post(f"{BASE_URL}/api/auth/login").mock(
        return_value=Response(200, json={"token": "fake-jwt-token", "user": mock_user})
    )

    token, user = await async_client.auth.login("ata@example.com", "password123")
    assert token == "fake-jwt-token"
    assert isinstance(user, User)
    assert user.username == "atacan"
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_auth_me_async(async_client):
    mock_user = {
        "id": "user-123",
        "name": "Ata Can",
        "username": "atacan",
        "email": "ata@example.com",
        "provider": "email",
        "createdAt": "2026-07-13T12:00:00Z",
        "updatedAt": "2026-07-13T12:00:00Z",
    }
    route = respx.get(f"{BASE_URL}/api/user/me").mock(return_value=Response(200, json=mock_user))

    user = await async_client.auth.me()
    assert isinstance(user, User)
    assert user.id == "user-123"
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_authentication_error_async(async_client):
    respx.get(f"{BASE_URL}/api/openapi/resumes").mock(
        return_value=Response(401, json={"message": "Invalid API Key"})
    )

    with pytest.raises(AuthenticationError):
        await async_client.resumes.list()


@pytest.mark.asyncio
@respx.mock
async def test_not_found_error_async(async_client):
    respx.get(f"{BASE_URL}/api/openapi/resume/non-existent").mock(
        return_value=Response(404, json={"message": "Not found"})
    )

    with pytest.raises(NotFoundError):
        await async_client.resumes.get("non-existent")


@pytest.mark.asyncio
@respx.mock
async def test_generic_api_error_500_async(async_client):
    respx.get(f"{BASE_URL}/api/openapi/resumes").mock(
        return_value=Response(500, text="Internal Server Error")
    )

    with pytest.raises(ReactiveResumeAPIError) as exc_info:
        await async_client.resumes.list()
    assert exc_info.value.status_code == 500


@pytest.mark.asyncio
@respx.mock
async def test_network_error_async(async_client):
    respx.get(f"{BASE_URL}/api/openapi/resumes").mock(
        side_effect=httpx.ConnectTimeout("Connection timed out")
    )

    with pytest.raises(ReactiveResumeError) as exc_info:
        await async_client.resumes.list()
    assert "Network or connection error occurred" in str(exc_info.value)


@pytest.mark.asyncio
async def test_token_api_key_modifiers_async(async_client):
    async_client.set_token("new-token")
    assert async_client.client.headers["Authorization"] == "Bearer new-token"
    assert "x-api-key" not in async_client.client.headers

    async_client.set_api_key("new-api-key")
    assert async_client.client.headers["x-api-key"] == "new-api-key"
    assert "Authorization" not in async_client.client.headers


@pytest.mark.asyncio
async def test_token_initialization_async():
    async with AsyncRxResumeClient(base_url=BASE_URL, token="initial-token") as c:
        assert c.client.headers["Authorization"] == "Bearer initial-token"
        assert "x-api-key" not in c.client.headers


@pytest.mark.asyncio
@respx.mock
async def test_list_resumes_pagination_async(async_client):
    mock_resume = {
        "id": "paginated-resume-id",
        "name": "Paginated CV",
        "slug": "paginated-cv",
        "userId": "user-123",
        "visibility": "public",
        "locked": False,
        "data": {"basics": {}, "sections": {}},
        "createdAt": "2026-07-13T12:00:00Z",
        "updatedAt": "2026-07-13T12:00:00Z",
    }
    route = respx.get(f"{BASE_URL}/api/openapi/resumes").mock(
        return_value=Response(200, json={"data": [mock_resume]})
    )
    resumes = await async_client.resumes.list()
    assert len(resumes) == 1
    assert resumes[0].id == "paginated-resume-id"
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_applications_crud_async(async_client):
    mock_app = {
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

    # 1. list
    route_list = respx.get(f"{BASE_URL}/api/openapi/applications").mock(
        return_value=Response(200, json=[mock_app])
    )
    apps = await async_client.applications.list()
    assert len(apps) == 1
    assert apps[0].company == "Google"
    assert route_list.called

    # 2. get
    route_get = respx.get(f"{BASE_URL}/api/openapi/applications/app-123").mock(
        return_value=Response(200, json=mock_app)
    )
    app = await async_client.applications.get("app-123")
    assert app.id == "app-123"
    assert route_get.called

    # 3. create
    from reactive_resume.models import ApplicationCreate

    route_create = respx.post(f"{BASE_URL}/api/openapi/applications").mock(
        return_value=Response(201, json=mock_app)
    )
    new_app = await async_client.applications.create(
        ApplicationCreate(company="Google", position="Staff Engineer")
    )
    assert new_app.id == "app-123"
    assert route_create.called

    # 4. update
    route_patch = respx.patch(f"{BASE_URL}/api/openapi/applications/app-123").mock(
        return_value=Response(200, json=mock_app)
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


@pytest.mark.asyncio
@respx.mock
async def test_statistics_async(async_client):
    mock_stats = {"views": 42, "downloads": 7, "history": {}}
    route = respx.get(f"{BASE_URL}/api/openapi/statistics/resume-1").mock(
        return_value=Response(200, json=mock_stats)
    )
    stats = await async_client.statistics.get("resume-1")
    assert stats.views == 42
    assert stats.downloads == 7
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_storage_async(async_client):
    mock_file = {
        "filename": "cv.pdf",
        "url": "https://rxresu.me/storage/cv.pdf",
        "size": 1024,
        "mimeType": "application/pdf",
    }
    route = respx.post(f"{BASE_URL}/api/openapi/storage/upload").mock(
        return_value=Response(201, json=mock_file)
    )
    uploaded = await async_client.storage.upload_file(b"pdf-data", "cv.pdf")
    assert uploaded.filename == "cv.pdf"
    assert uploaded.mime_type == "application/pdf"
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_agent_chat_async(async_client):
    mock_response = {"response": "Here is an optimized resume draft."}
    route = respx.post(f"{BASE_URL}/api/openapi/agent/resume-1/chat").mock(
        return_value=Response(200, json=mock_response)
    )
    response = await async_client.agent.chat("resume-1", "Optimize my summary")
    assert response.response == "Here is an optimized resume draft."
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_ai_providers_async(async_client):
    mock_providers = [{"name": "openai", "enabled": True}]
    route = respx.get(f"{BASE_URL}/api/openapi/ai-providers").mock(
        return_value=Response(200, json=mock_providers)
    )
    providers = await async_client.ai_providers.list()
    assert len(providers) == 1
    assert providers[0]["name"] == "openai"
    assert route.called
