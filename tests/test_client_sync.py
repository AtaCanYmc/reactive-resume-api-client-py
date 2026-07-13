import pytest
import respx
from httpx import Response
from reactive_resume import RxResumeClient, AuthenticationError, NotFoundError
from reactive_resume.models import ResumeImportData, Resume

BASE_URL = "https://rxresu.me"
API_KEY = "test-api-key"


@pytest.fixture
def client():
    with RxResumeClient(base_url=BASE_URL, api_key=API_KEY) as c:
        yield c


@respx.mock
def test_list_resumes(client):
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

    resumes = client.resumes.list()
    assert len(resumes) == 1
    assert isinstance(resumes[0], Resume)
    assert resumes[0].id == "test-resume-id"
    assert resumes[0].data.basics.name == "John Doe"
    assert route.called


@respx.mock
def test_get_resume(client):
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

    resume = client.resumes.get("resume-1")
    assert resume.id == "resume-1"
    assert route.called


@respx.mock
def test_create_resume(client):
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
    resume = client.resumes.import_resume(import_data)
    assert resume.id == "new-resume"
    assert route.called


@respx.mock
def test_authentication_error(client):
    respx.get(f"{BASE_URL}/api/openapi/resumes").mock(
        return_value=Response(401, json={"message": "Invalid API Key"})
    )

    with pytest.raises(AuthenticationError):
        client.resumes.list()


@respx.mock
def test_not_found_error(client):
    respx.get(f"{BASE_URL}/api/openapi/resume/non-existent").mock(
        return_value=Response(404, json={"message": "Not found"})
    )

    with pytest.raises(NotFoundError):
        client.resumes.get("non-existent")
