import pytest
import respx
from httpx import Response
from reactive_resume import RxResumeClient, AsyncRxResumeClient
from reactive_resume.models import ResumeImportData, ResumeStats

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
    route_get = respx.get(f"{BASE_URL}/api/openapi/resumes/resume-123").mock(
        return_value=Response(200, json=MOCK_RESUME)
    )
    resume = sync_client.resumes.get("resume-123")
    assert resume.name == "Ata Can - CV"
    assert route_get.called

    # 3. create/import
    route_create = respx.post(f"{BASE_URL}/api/openapi/resumes").mock(
        return_value=Response(201, json=MOCK_RESUME)
    )
    new_resume = sync_client.resumes.create(ResumeImportData(title="Ata Can - CV"))
    assert new_resume.id == "resume-123"
    assert route_create.called

    route_import = respx.post(f"{BASE_URL}/api/openapi/resumes/import").mock(
        return_value=Response(201, json=MOCK_RESUME)
    )
    imported_resume = sync_client.resumes.import_resume(ResumeImportData(title="Ata Can - CV"))
    assert imported_resume.id == "resume-123"
    assert route_import.called

    # 4. update PATCH
    route_patch = respx.patch(f"{BASE_URL}/api/openapi/resumes/resume-123").mock(
        return_value=Response(200, json=MOCK_RESUME)
    )
    updated = sync_client.resumes.update("resume-123", {"name": "New Name"})
    assert updated.id == "resume-123"
    assert route_patch.called

    # 4b. update PUT
    route_put = respx.put(f"{BASE_URL}/api/openapi/resumes/resume-123").mock(
        return_value=Response(200, json=MOCK_RESUME)
    )
    updated_put = sync_client.resumes.update_put("resume-123", {"name": "New Name"})
    assert updated_put.id == "resume-123"
    assert route_put.called

    # 5. delete
    route_delete = respx.delete(f"{BASE_URL}/api/openapi/resumes/resume-123").mock(
        return_value=Response(204)
    )
    sync_client.resumes.delete("resume-123")
    assert route_delete.called

    # 6. pdf url
    pdf_url = sync_client.resumes.get_pdf_url("resume-123")
    assert pdf_url == f"{BASE_URL}/api/openapi/resumes/resume-123/pdf"

    # 7. tags
    route_tags = respx.get(f"{BASE_URL}/api/openapi/resumes/tags").mock(
        return_value=Response(200, json=["work", "tech"])
    )
    assert "work" in sync_client.resumes.tags()
    assert route_tags.called

    # 8. password
    route_set_pass = respx.put(f"{BASE_URL}/api/openapi/resumes/resume-123/password").mock(
        return_value=Response(200)
    )
    sync_client.resumes.set_password("resume-123", "secret")
    assert route_set_pass.called

    route_rem_pass = respx.delete(f"{BASE_URL}/api/openapi/resumes/resume-123/password").mock(
        return_value=Response(200)
    )
    sync_client.resumes.remove_password("resume-123")
    assert route_rem_pass.called

    route_ver_pass = respx.post(f"{BASE_URL}/api/openapi/resumes/resume-123/password").mock(
        return_value=Response(200, json={"success": True})
    )
    assert sync_client.resumes.verify_password("resume-123", "secret") is True
    assert route_ver_pass.called

    # 9. public
    route_pub = respx.get(f"{BASE_URL}/api/openapi/resumes/atacan/cv").mock(
        return_value=Response(200, json=MOCK_RESUME)
    )
    pub = sync_client.resumes.get_public_resume("atacan", "cv")
    assert pub.id == "resume-123"
    assert route_pub.called

    # 10. analysis
    route_analysis = respx.get(f"{BASE_URL}/api/openapi/resumes/resume-123/analysis").mock(
        return_value=Response(200, json={"grammar": 90})
    )
    analysis = sync_client.resumes.get_latest_analysis("resume-123")
    assert analysis["grammar"] == 90
    assert route_analysis.called

    # 11. versions
    route_versions = respx.get(f"{BASE_URL}/api/openapi/resumes/resume-123/versions").mock(
        return_value=Response(200, json=[{"id": "v1"}])
    )
    versions = sync_client.resumes.get_versions("resume-123")
    assert len(versions) == 1
    assert route_versions.called

    # 12. duplicate
    route_dup = respx.post(f"{BASE_URL}/api/openapi/resumes/resume-123/duplicate").mock(
        return_value=Response(201, json=MOCK_RESUME)
    )
    dup = sync_client.resumes.duplicate("resume-123", "Dup", "dup-slug")
    assert dup.id == "resume-123"
    assert route_dup.called

    # 13. lock
    route_lock = respx.post(f"{BASE_URL}/api/openapi/resumes/resume-123/lock").mock(
        return_value=Response(200)
    )
    sync_client.resumes.lock("resume-123", True)
    assert route_lock.called

    # 14. download pdf
    route_pdf = respx.get(f"{BASE_URL}/api/openapi/resumes/resume-123/pdf").mock(
        return_value=Response(200, content=b"pdf-content")
    )
    pdf = sync_client.resumes.download_pdf("resume-123")
    assert pdf == b"pdf-content"
    assert route_pdf.called

    # 15. get statistics
    route_stats = respx.get(f"{BASE_URL}/api/openapi/resumes/resume-123/statistics").mock(
        return_value=Response(200, json={"views": 10, "downloads": 2, "history": {}})
    )
    stats = sync_client.resumes.get_statistics("resume-123")
    assert isinstance(stats, ResumeStats)
    assert stats.views == 10
    assert route_stats.called

    # 16. get daily statistics
    route_daily = respx.get(
        f"{BASE_URL}/api/openapi/resumes/resume-123/statistics/daily?day=30"
    ).mock(return_value=Response(200, json={"views": 5, "downloads": 1, "history": {}}))
    daily = sync_client.resumes.get_daily_statistics("resume-123", 30)
    assert isinstance(daily, ResumeStats)
    assert daily.views == 5
    assert route_daily.called


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
    route_get = respx.get(f"{BASE_URL}/api/openapi/resumes/resume-123").mock(
        return_value=Response(200, json=MOCK_RESUME)
    )
    resume = await async_client.resumes.get("resume-123")
    assert resume.name == "Ata Can - CV"
    assert route_get.called

    # 3. create/import
    route_create = respx.post(f"{BASE_URL}/api/openapi/resumes").mock(
        return_value=Response(201, json=MOCK_RESUME)
    )
    new_resume = await async_client.resumes.create(ResumeImportData(title="Ata Can - CV"))
    assert new_resume.id == "resume-123"
    assert route_create.called

    route_import = respx.post(f"{BASE_URL}/api/openapi/resumes/import").mock(
        return_value=Response(201, json=MOCK_RESUME)
    )
    imported = await async_client.resumes.import_resume(ResumeImportData(title="Ata Can - CV"))
    assert imported.id == "resume-123"
    assert route_import.called

    # 4. update PATCH
    route_patch = respx.patch(f"{BASE_URL}/api/openapi/resumes/resume-123").mock(
        return_value=Response(200, json=MOCK_RESUME)
    )
    updated = await async_client.resumes.update("resume-123", {"name": "New Name"})
    assert updated.id == "resume-123"
    assert route_patch.called

    # 4b. update PUT
    route_put = respx.put(f"{BASE_URL}/api/openapi/resumes/resume-123").mock(
        return_value=Response(200, json=MOCK_RESUME)
    )
    updated_put = await async_client.resumes.update_put("resume-123", {"name": "New Name"})
    assert updated_put.id == "resume-123"
    assert route_put.called

    # 5. delete
    route_delete = respx.delete(f"{BASE_URL}/api/openapi/resumes/resume-123").mock(
        return_value=Response(204)
    )
    await async_client.resumes.delete("resume-123")
    assert route_delete.called

    # 6. pdf url
    pdf_url = await async_client.resumes.get_pdf_url("resume-123")
    assert pdf_url == f"{BASE_URL}/api/openapi/resumes/resume-123/pdf"

    # 7. tags
    route_tags = respx.get(f"{BASE_URL}/api/openapi/resumes/tags").mock(
        return_value=Response(200, json=["work", "tech"])
    )
    assert "work" in await async_client.resumes.tags()
    assert route_tags.called

    # 8. password
    route_set_pass = respx.put(f"{BASE_URL}/api/openapi/resumes/resume-123/password").mock(
        return_value=Response(200)
    )
    await async_client.resumes.set_password("resume-123", "secret")
    assert route_set_pass.called

    route_rem_pass = respx.delete(f"{BASE_URL}/api/openapi/resumes/resume-123/password").mock(
        return_value=Response(200)
    )
    await async_client.resumes.remove_password("resume-123")
    assert route_rem_pass.called

    route_ver_pass = respx.post(f"{BASE_URL}/api/openapi/resumes/resume-123/password").mock(
        return_value=Response(200, json={"success": True})
    )
    assert await async_client.resumes.verify_password("resume-123", "secret") is True
    assert route_ver_pass.called

    # 9. public
    route_pub = respx.get(f"{BASE_URL}/api/openapi/resumes/atacan/cv").mock(
        return_value=Response(200, json=MOCK_RESUME)
    )
    pub = await async_client.resumes.get_public_resume("atacan", "cv")
    assert pub.id == "resume-123"
    assert route_pub.called

    # 10. analysis
    route_analysis = respx.get(f"{BASE_URL}/api/openapi/resumes/resume-123/analysis").mock(
        return_value=Response(200, json={"grammar": 90})
    )
    analysis = await async_client.resumes.get_latest_analysis("resume-123")
    assert analysis["grammar"] == 90
    assert route_analysis.called

    # 11. versions
    route_versions = respx.get(f"{BASE_URL}/api/openapi/resumes/resume-123/versions").mock(
        return_value=Response(200, json=[{"id": "v1"}])
    )
    versions = await async_client.resumes.get_versions("resume-123")
    assert len(versions) == 1
    assert route_versions.called

    # 12. duplicate
    route_dup = respx.post(f"{BASE_URL}/api/openapi/resumes/resume-123/duplicate").mock(
        return_value=Response(201, json=MOCK_RESUME)
    )
    dup = await async_client.resumes.duplicate("resume-123", "Dup", "dup-slug")
    assert dup.id == "resume-123"
    assert route_dup.called

    # 13. lock
    route_lock = respx.post(f"{BASE_URL}/api/openapi/resumes/resume-123/lock").mock(
        return_value=Response(200)
    )
    await async_client.resumes.lock("resume-123", True)
    assert route_lock.called

    # 14. download pdf
    route_pdf = respx.get(f"{BASE_URL}/api/openapi/resumes/resume-123/pdf").mock(
        return_value=Response(200, content=b"pdf-content")
    )
    pdf = await async_client.resumes.download_pdf("resume-123")
    assert pdf == b"pdf-content"
    assert route_pdf.called

    # 15. get statistics
    route_stats = respx.get(f"{BASE_URL}/api/openapi/resumes/resume-123/statistics").mock(
        return_value=Response(200, json={"views": 10, "downloads": 2, "history": {}})
    )
    stats = await async_client.resumes.get_statistics("resume-123")
    assert isinstance(stats, ResumeStats)
    assert stats.views == 10
    assert route_stats.called

    # 16. get daily statistics
    route_daily = respx.get(
        f"{BASE_URL}/api/openapi/resumes/resume-123/statistics/daily?day=30"
    ).mock(return_value=Response(200, json={"views": 5, "downloads": 1, "history": {}}))
    daily = await async_client.resumes.get_daily_statistics("resume-123", 30)
    assert isinstance(daily, ResumeStats)
    assert daily.views == 5
    assert route_daily.called
