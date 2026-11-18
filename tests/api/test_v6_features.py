import pytest
import respx
from httpx import Response

from reactive_resume import RxResumeClient
from reactive_resume.models import CoverLetter

BASE_URL = "https://rxresu.me"

MOCK_LETTER = {
    "id": "cl-1",
    "name": "Cover Letter Google",
    "slug": "cl-google",
    "userId": "user-1",
    "content": "Dear Hiring Manager...",
    "tags": ["tech"],
    "isLocked": False,
    "createdAt": "2026-01-01T00:00:00Z",
    "updatedAt": "2026-01-01T00:00:00Z",
}


@pytest.fixture
def sync_client():
    with RxResumeClient(base_url=BASE_URL, api_key="test-key") as client:
        yield client


@respx.mock
def test_cover_letters_crud(sync_client):
    respx.get(f"{BASE_URL}/api/openapi/cover-letters").mock(
        return_value=Response(200, json=[MOCK_LETTER])
    )
    respx.get(f"{BASE_URL}/api/openapi/cover-letters/cl-1").mock(
        return_value=Response(200, json=MOCK_LETTER)
    )
    respx.get(f"{BASE_URL}/api/openapi/cover-letters/cl-1/exports/pdf").mock(
        return_value=Response(200, content=b"%PDF-sample")
    )
    respx.delete(f"{BASE_URL}/api/openapi/cover-letters/cl-1").mock(
        return_value=Response(200, json={"success": True})
    )

    letters = sync_client.cover_letters.list()
    assert len(letters) == 1
    assert isinstance(letters[0], CoverLetter)
    assert letters[0].name == "Cover Letter Google"

    letter = sync_client.cover_letters.get("cl-1")
    assert letter.id == "cl-1"

    pdf_bytes = sync_client.cover_letters.export("cl-1", format="pdf")
    assert pdf_bytes.startswith(b"%PDF")

    sync_client.cover_letters.delete("cl-1")


@respx.mock
def test_documents_and_trash(sync_client):
    respx.get(f"{BASE_URL}/api/openapi/documents/counts").mock(
        return_value=Response(200, json={"resumes": 3, "coverLetters": 1, "trash": 0})
    )
    respx.put(f"{BASE_URL}/api/openapi/documents/resume/res-1/trash").mock(
        return_value=Response(200, json={"success": True})
    )
    respx.post(f"{BASE_URL}/api/openapi/documents/restore").mock(
        return_value=Response(200, json={"success": True})
    )
    respx.post(f"{BASE_URL}/api/openapi/documents/purge").mock(
        return_value=Response(200, json={"success": True})
    )

    counts = sync_client.documents.get_counts()
    assert counts["resumes"] == 3

    sync_client.documents.trash("resume", "res-1")
    sync_client.documents.restore("res-1")
    sync_client.documents.purge("res-1")


@respx.mock
def test_custom_domain(sync_client):
    respx.get(f"{BASE_URL}/api/openapi/custom-domain").mock(
        return_value=Response(200, json={"hostname": "cv.example.com", "verified": True})
    )
    respx.put(f"{BASE_URL}/api/openapi/custom-domain").mock(
        return_value=Response(200, json={"hostname": "cv.example.com", "status": "pending"})
    )
    respx.post(f"{BASE_URL}/api/openapi/custom-domain/verify").mock(
        return_value=Response(200, json={"verified": True})
    )
    respx.delete(f"{BASE_URL}/api/openapi/custom-domain").mock(
        return_value=Response(200, json={"success": True})
    )

    info = sync_client.custom_domain.get()
    assert info["hostname"] == "cv.example.com"
    sync_client.custom_domain.set("cv.example.com")
    sync_client.custom_domain.verify()
    sync_client.custom_domain.delete()


@respx.mock
def test_resume_exports_and_preview(sync_client):
    respx.get(f"{BASE_URL}/api/openapi/resumes/res-1/exports/docx").mock(
        return_value=Response(200, content=b"PK-docx-mock")
    )
    respx.get(f"{BASE_URL}/api/openapi/resumes/res-1/web-page/preview").mock(
        return_value=Response(200, json={"previewUrl": "https://rxresu.me/preview/123"})
    )

    docx = sync_client.resumes.export("res-1", format="docx")
    assert docx == b"PK-docx-mock"

    preview = sync_client.resumes.get_preview_url("res-1")
    assert "previewUrl" in preview


@respx.mock
def test_application_summary_and_close(sync_client):
    respx.get(f"{BASE_URL}/api/openapi/applications/summary").mock(
        return_value=Response(
            200,
            json=[
                {
                    "id": "app-1",
                    "company": "Stripe",
                    "position": "Backend",
                    "stage": "closed",
                    "closedReason": "withdrew",
                }
            ],
        )
    )
    respx.patch(f"{BASE_URL}/api/openapi/applications/app-1").mock(
        return_value=Response(
            200,
            json={
                "id": "app-1",
                "userId": "u-1",
                "company": "Stripe",
                "position": "Backend",
                "stage": "closed",
                "closedReason": "withdrew",
                "date": "2026-01-01T00:00:00Z",
                "createdAt": "2026-01-01T00:00:00Z",
                "updatedAt": "2026-01-01T00:00:00Z",
            },
        )
    )

    summaries = sync_client.applications.summary()
    assert len(summaries) == 1
    assert summaries[0].stage == "closed"
    assert summaries[0].closed_reason == "withdrew"

    app = sync_client.applications.close("app-1", reason="withdrew")
    assert app.stage == "closed"
    assert app.closed_reason == "withdrew"


@respx.mock
def test_resume_checks_and_job_matches(sync_client):
    respx.get(f"{BASE_URL}/api/openapi/resumes/res-1/checks").mock(
        return_value=Response(200, json={"score": 95, "issues": []})
    )
    respx.post(f"{BASE_URL}/api/openapi/resumes/res-1/job-matches").mock(
        return_value=Response(200, json={"matchScore": 88, "matchedKeywords": ["python", "api"]})
    )
    respx.post(f"{BASE_URL}/api/openapi/resumes/res-1/slug-check").mock(
        return_value=Response(200, json={"available": True})
    )

    checks = sync_client.resumes.get_checks("res-1")
    assert checks["score"] == 95

    matches = sync_client.resumes.match_job("res-1", "Python API Developer")
    assert matches["matchScore"] == 88

    slug_info = sync_client.resumes.check_slug("res-1", "my-slug")
    assert slug_info["available"] is True


@respx.mock
def test_files_and_career_and_lanes(sync_client):
    respx.get(f"{BASE_URL}/api/openapi/statistics").mock(
        return_value=Response(200, json={"totalUsers": 100, "totalResumes": 250})
    )
    respx.post(f"{BASE_URL}/api/openapi/files").mock(
        return_value=Response(200, json={"url": "https://rxresu.me/uploads/avatar.png"})
    )
    respx.delete(f"{BASE_URL}/api/openapi/files").mock(
        return_value=Response(200, json={"success": True})
    )
    respx.get(f"{BASE_URL}/api/openapi/applications/lanes").mock(
        return_value=Response(200, json=[{"id": "lane-1", "name": "Applied"}])
    )
    respx.post(f"{BASE_URL}/api/openapi/applications/lanes").mock(
        return_value=Response(200, json=[{"id": "lane-1", "name": "Applied"}])
    )
    respx.get(f"{BASE_URL}/api/openapi/career/profile").mock(
        return_value=Response(200, json={"bio": "Software Engineer"})
    )
    respx.get(f"{BASE_URL}/api/openapi/career/facts").mock(
        return_value=Response(200, json=[{"id": "f-1", "fact": "Led backend migration"}])
    )

    overview = sync_client.statistics.get_overview()
    assert overview["totalUsers"] == 100

    upload_res = sync_client.files.upload(b"fake-image-bytes", filename="avatar.png")
    assert "url" in upload_res
    sync_client.files.delete("avatar.png")

    lanes = sync_client.applications.get_lanes()
    assert len(lanes) == 1
    updated_lanes = sync_client.applications.update_lanes(lanes)
    assert len(updated_lanes) == 1

    profile = sync_client.career.get_profile()
    assert profile["bio"] == "Software Engineer"
    facts = sync_client.career.list_facts()
    assert len(facts) == 1


def test_structured_dates_model():
    from reactive_resume.models import ResumeItemDates, WorkItem

    item = WorkItem(
        id="w-1",
        company="Acme Corp",
        position="Senior Developer",
        date="2022 - Present",
        dates=ResumeItemDates(start="2022-01-01", end="", present=True),
    )
    assert item.dates is not None
    assert item.dates.present is True
    assert item.dates.start == "2022-01-01"
