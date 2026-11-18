"""Tests for offline mock clients (MockRxResumeClient and AsyncMockRxResumeClient)."""

import pytest

from reactive_resume.models import AgentStreamEvent, CoverLetterCreate, ResumeImportData
from reactive_resume.testing import AsyncMockRxResumeClient, MockRxResumeClient


def test_sync_mock_client_operations():
    with MockRxResumeClient() as client:
        # 1. Health
        health = client.health()
        assert health.status == "healthy"
        assert "mock" in health.version

        # 2. Resumes list (initial sample)
        resumes = client.resumes.list()
        assert len(resumes) >= 1

        # 3. Create resume
        created = client.resumes.create(ResumeImportData(title="Offline CV", slug="offline-cv"))
        assert created.name == "Offline CV"
        assert created.id.startswith("mock-res-")

        # 4. Get resume
        fetched = client.resumes.get(created.id)
        assert fetched.slug == "offline-cv"

        # 5. Export
        pdf = client.resumes.export(created.id, format="pdf")
        assert b"%PDF" in pdf

        # 6. JSON Resume Export
        jr = client.resumes.export_json_resume(created.id)
        assert "basics" in jr

        # 7. Lock
        locked = client.resumes.lock(created.id, is_locked=True)
        assert locked.is_locked is True

        # 8. Cover Letters
        cl = client.cover_letters.create(CoverLetterCreate(title="Test Letter", slug="test-letter"))
        assert cl.name == "Test Letter"
        assert len(client.cover_letters.list()) == 1

        # 9. Document Trash & Counts
        counts_before = client.documents.get_counts()
        assert counts_before["resumes"] >= 2
        assert counts_before["trash"] == 0

        client.resumes.delete(created.id)
        counts_after = client.documents.get_counts()
        assert counts_after["trash"] == 1

        # 10. Agent Streaming
        events = list(client.agent.resume_message_stream("thread-1"))
        assert len(events) == 3
        ev0 = events[0]
        assert isinstance(ev0, AgentStreamEvent)
        assert ev0.event == "start"


@pytest.mark.asyncio
async def test_async_mock_client_operations():
    async with AsyncMockRxResumeClient() as client:
        # Health
        health = await client.health()
        assert health.status == "healthy"

        # Resumes
        resumes = await client.resumes.list()
        assert len(resumes) >= 1

        created = await client.resumes.create(
            ResumeImportData(title="Async Offline CV", slug="async-offline-cv")
        )
        assert created.slug == "async-offline-cv"

        fetched = await client.resumes.get(created.id)
        assert fetched.id == created.id

        # Cover letters
        cl = await client.cover_letters.create(CoverLetterCreate(title="Async CL", slug="async-cl"))
        assert cl.name == "Async CL"

        # Agent stream
        stream = client.agent.resume_message_stream("thread-1")
        events = [ev async for ev in stream]
        assert len(events) == 3
        ev2 = events[2]
        assert isinstance(ev2, AgentStreamEvent)
        assert ev2.event == "done"
