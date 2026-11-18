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
