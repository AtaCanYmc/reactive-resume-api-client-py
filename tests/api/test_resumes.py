import pytest
import respx
from httpx import Response
from reactive_resume import RxResumeClient, AsyncRxResumeClient
from reactive_resume.models import ResumeImportData

BASE_URL = "https://rxresu.me"
API_KEY = "test-api-key"

MOCK_RESUME = {
    "id": "resume-123",
    "name": "Ata Can - CV",
    "slug": "ata-can-cv",
    "userId": "user-123",
    "visibility": "public",
    "locked": False,
    "data": {
        "basics": {
            "name": "Ata Can",
            "headline": "Architect",
            "email": "ata@example.com",
            "phone": "555",
            "website": "",
            "location": "",
            "picture": "",
            "profiles": [],
        },
        "sections": {},
    },
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
def test_sync_resume_crud(sync_client):
    # 1. list
    route_list = respx.get(f"{BASE_URL}/api/openapi/resumes").mock(
        return_value=Response(200, json=[MOCK_RESUME])
    )
    resumes = sync_client.resumes.list()
    assert len(resumes) == 1
    assert resumes[0].id == "resume-123"
    assert route_list.called

    # 1b. list with pagination wrapper {"data": [...]}
    route_list_paginated = respx.get(f"{BASE_URL}/api/openapi/resumes").mock(
        return_value=Response(200, json={"data": [MOCK_RESUME]})
    )
    resumes_pag = sync_client.resumes.list()
    assert len(resumes_pag) == 1
    assert resumes_pag[0].id == "resume-123"
    assert route_list_paginated.called

    # 2. get
    route_get = respx.get(f"{BASE_URL}/api/openapi/resume/resume-123").mock(
        return_value=Response(200, json=MOCK_RESUME)
    )
    resume = sync_client.resumes.get("resume-123")
    assert resume.name == "Ata Can - CV"
    assert route_get.called

    # 3. create/import
    route_create = respx.post(f"{BASE_URL}/api/openapi/resumes").mock(
        return_value=Response(201, json=MOCK_RESUME)
    )
    new_resume = sync_client.resumes.import_resume(ResumeImportData(title="Ata Can - CV"))
    assert new_resume.id == "resume-123"
    assert route_create.called

    # 4. update
    route_patch = respx.patch(f"{BASE_URL}/api/openapi/resume/resume-123").mock(
        return_value=Response(200, json=MOCK_RESUME)
    )
    updated = sync_client.resumes.update("resume-123", {"name": "New Name"})
    assert updated.id == "resume-123"
    assert route_patch.called

    # 5. delete
    route_delete = respx.delete(f"{BASE_URL}/api/openapi/resume/resume-123").mock(
        return_value=Response(204)
    )
    sync_client.resumes.delete("resume-123")
    assert route_delete.called

    # 6. pdf url
    pdf_url = sync_client.resumes.get_pdf_url("resume-123")
    assert pdf_url == f"{BASE_URL}/api/openapi/resume/resume-123/pdf"


@pytest.mark.asyncio
@respx.mock
async def test_async_resume_crud(async_client):
    # 1. list
    route_list = respx.get(f"{BASE_URL}/api/openapi/resumes").mock(
        return_value=Response(200, json=[MOCK_RESUME])
    )
    resumes = await async_client.resumes.list()
    assert len(resumes) == 1
    assert resumes[0].id == "resume-123"
    assert route_list.called

    # 1b. list with pagination wrapper
    route_list_pag = respx.get(f"{BASE_URL}/api/openapi/resumes").mock(
        return_value=Response(200, json={"data": [MOCK_RESUME]})
    )
    resumes_pag = await async_client.resumes.list()
    assert len(resumes_pag) == 1
    assert route_list_pag.called

    # 2. get
    route_get = respx.get(f"{BASE_URL}/api/openapi/resume/resume-123").mock(
        return_value=Response(200, json=MOCK_RESUME)
    )
    resume = await async_client.resumes.get("resume-123")
    assert resume.name == "Ata Can - CV"
    assert route_get.called

    # 3. create/import
    route_create = respx.post(f"{BASE_URL}/api/openapi/resumes").mock(
        return_value=Response(201, json=MOCK_RESUME)
    )
    new_resume = await async_client.resumes.import_resume(ResumeImportData(title="Ata Can - CV"))
    assert new_resume.id == "resume-123"
    assert route_create.called

    # 4. update
    route_patch = respx.patch(f"{BASE_URL}/api/openapi/resume/resume-123").mock(
        return_value=Response(200, json=MOCK_RESUME)
    )
    updated = await async_client.resumes.update("resume-123", {"name": "New Name"})
    assert updated.id == "resume-123"
    assert route_patch.called

    # 5. delete
    route_delete = respx.delete(f"{BASE_URL}/api/openapi/resume/resume-123").mock(
        return_value=Response(204)
    )
    await async_client.resumes.delete("resume-123")
    assert route_delete.called

    # 6. pdf url
    pdf_url = await async_client.resumes.get_pdf_url("resume-123")
    assert pdf_url == f"{BASE_URL}/api/openapi/resume/resume-123/pdf"
