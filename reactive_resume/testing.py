"""Offline mock clients for local testing and demonstration without network connectivity."""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator, Iterator
from datetime import datetime
from typing import Any, Self

from .models.agent import AgentStreamEvent
from .models.application import Application, ApplicationCreate
from .models.cover_letter import CoverLetter, CoverLetterCreate
from .models.health import DependencyHealth, SystemHealth
from .models.resume import Basics, Resume, ResumeData, ResumeImportData


class _MockResumesAPI:
    def __init__(self, storage: dict[str, Any]) -> None:
        self._storage = storage

    def list(self, limit: int | None = None, offset: int | None = None) -> list[Resume]:
        resumes = list(self._storage["resumes"].values())
        if offset is not None:
            resumes = resumes[offset:]
        if limit is not None:
            resumes = resumes[:limit]
        return resumes

    def get(self, resume_id: str) -> Resume:
        if resume_id not in self._storage["resumes"]:
            raise KeyError(f"Resume '{resume_id}' not found.")
        return self._storage["resumes"][resume_id]

    def create(self, data: ResumeImportData) -> Resume:
        r_id = f"mock-res-{uuid.uuid4().hex[:8]}"
        now = datetime.now()
        r_data = ResumeData(
            basics=data.basics or Basics(),
            sections=data.sections or {},
        )
        resume = Resume(
            id=r_id,
            name=data.title,
            slug=data.slug or data.title.lower().replace(" ", "-"),
            data=r_data,
            created_at=now,
            updated_at=now,
        )
        self._storage["resumes"][r_id] = resume
        return resume

    def import_resume(self, data: ResumeImportData) -> Resume:
        return self.create(data)

    def update(self, resume_id: str, data: dict[str, Any]) -> Resume:
        res = self.get(resume_id)
        dump = res.model_dump()
        dump.update(data)
        dump["updatedAt"] = datetime.now()
        updated = Resume.model_validate(dump)
        self._storage["resumes"][resume_id] = updated
        return updated

    def delete(self, resume_id: str) -> None:
        res = self.get(resume_id)
        self._storage["trash"][resume_id] = {"item": res, "type": "resume"}
        del self._storage["resumes"][resume_id]

    def export(self, resume_id: str, format: str = "pdf") -> bytes:
        self.get(resume_id)
        fmt = format.lower()
        if fmt == "json":
            return b'{"mock": true}'
        if fmt == "md":
            return b"# Mock Resume Markdown\n"
        return b"%PDF-1.4 Mock Binary PDF Content\n"

    def export_json_resume(self, resume_id: str) -> dict[str, Any]:
        from .utils.json_resume import to_json_resume

        res = self.get(resume_id)
        return to_json_resume(res)

    def duplicate(self, resume_id: str, name: str, slug: str) -> Resume:
        orig = self.get(resume_id)
        basics = orig.data.basics if orig.data else None
        sections = orig.data.sections if orig.data else None
        return self.create(
            ResumeImportData(title=name, slug=slug, basics=basics, sections=sections)
        )

    def lock(self, resume_id: str, is_locked: bool = True) -> Resume:
        res = self.get(resume_id)
        res.is_locked = is_locked
        res.locked = is_locked
        return res

    def get_checks(self, resume_id: str) -> dict[str, Any]:
        self.get(resume_id)
        return {"status": "ok", "atsScore": 95, "checks": []}

    def match_job(self, resume_id: str, job_description: str) -> dict[str, Any]:
        self.get(resume_id)
        return {"matchScore": 88, "matchingKeywords": ["Python", "API"], "missingKeywords": []}


class _MockCoverLettersAPI:
    def __init__(self, storage: dict[str, Any]) -> None:
        self._storage = storage

    def list(self) -> list[CoverLetter]:
        return list(self._storage["cover_letters"].values())

    def get(self, cover_letter_id: str) -> CoverLetter:
        if cover_letter_id not in self._storage["cover_letters"]:
            raise KeyError(f"Cover letter '{cover_letter_id}' not found.")
        return self._storage["cover_letters"][cover_letter_id]

    def create(self, data: CoverLetterCreate) -> CoverLetter:
        cl_id = f"mock-cl-{uuid.uuid4().hex[:8]}"
        now = datetime.now()
        cl = CoverLetter(
            id=cl_id,
            name=data.title,
            slug=data.slug or data.title.lower().replace(" ", "-"),
            content=data.content or "",
            created_at=now,
            updated_at=now,
        )
        self._storage["cover_letters"][cl_id] = cl
        return cl

    def delete(self, cover_letter_id: str) -> None:
        cl = self.get(cover_letter_id)
        self._storage["trash"][cover_letter_id] = {"item": cl, "type": "cover_letter"}
        del self._storage["cover_letters"][cover_letter_id]


class _MockDocumentsAPI:
    def __init__(self, storage: dict[str, Any]) -> None:
        self._storage = storage

    def get_counts(self) -> dict[str, int]:
        return {
            "resumes": len(self._storage["resumes"]),
            "coverLetters": len(self._storage["cover_letters"]),
            "trash": len(self._storage["trash"]),
        }

    def trash(self, document_id: str, doc_type: str = "resume") -> None:
        if doc_type == "resume" and document_id in self._storage["resumes"]:
            self._storage["trash"][document_id] = {
                "item": self._storage["resumes"].pop(document_id),
                "type": "resume",
            }
        elif doc_type == "cover_letter" and document_id in self._storage["cover_letters"]:
            self._storage["trash"][document_id] = {
                "item": self._storage["cover_letters"].pop(document_id),
                "type": "cover_letter",
            }

    def restore(self, document_id: str, doc_type: str = "resume") -> None:
        if document_id in self._storage["trash"]:
            entry = self._storage["trash"].pop(document_id)
            if entry["type"] == "resume":
                self._storage["resumes"][document_id] = entry["item"]
            else:
                self._storage["cover_letters"][document_id] = entry["item"]

    def purge(self, document_id: str, doc_type: str = "resume") -> None:
        self._storage["trash"].pop(document_id, None)


class _MockApplicationsAPI:
    def __init__(self, storage: dict[str, Any]) -> None:
        self._storage = storage

    def list(self) -> list[Application]:
        return list(self._storage["applications"].values())

    def get(self, application_id: str) -> Application:
        if application_id not in self._storage["applications"]:
            raise KeyError(f"Application '{application_id}' not found.")
        return self._storage["applications"][application_id]

    def create(self, data: ApplicationCreate) -> Application:
        app_id = f"mock-app-{uuid.uuid4().hex[:8]}"
        now = datetime.now()
        app = Application(
            id=app_id,
            user_id="mock-user-1",
            company=data.company,
            position=data.position,
            stage=data.stage or "Applied",
            date=now,
            created_at=now,
            updated_at=now,
        )
        self._storage["applications"][app_id] = app
        return app

    def close(self, application_id: str, reason: str = "not-selected") -> Application:
        app = self.get(application_id)
        app.stage = "closed"
        app.closed_reason = reason
        return app

    def delete(self, application_id: str) -> None:
        self.get(application_id)
        del self._storage["applications"][application_id]


class _MockAgentAPI:
    def __init__(self, storage: dict[str, Any]) -> None:
        self._storage = storage

    def list_threads(self) -> list[dict[str, Any]]:
        return list(self._storage["threads"].values())

    def create_thread(self, ai_provider_id: str | None = None) -> dict[str, Any]:
        t_id = f"thread-{uuid.uuid4().hex[:8]}"
        t = {"id": t_id, "aiProviderId": ai_provider_id or "mock", "messages": []}
        self._storage["threads"][t_id] = t
        return t

    def send_message(self, thread_id: str, message: Any) -> dict[str, Any]:
        return {"threadId": thread_id, "success": True}

    def resume_message_stream(
        self, thread_id: str, raw: bool = False
    ) -> Iterator[AgentStreamEvent] | Iterator[str]:
        events = [
            AgentStreamEvent(event="start", data='{"status": "started"}'),
            AgentStreamEvent(event="message", data='{"content": "Mock offline agent response."}'),
            AgentStreamEvent(event="done", data='{"done": true}'),
        ]
        if raw:
            for ev in events:
                yield f"event: {ev.event}\ndata: {ev.data}\n\n"
        else:
            yield from events


class _MockCustomDomainAPI:
    def __init__(self, storage: dict[str, Any]) -> None:
        self._storage = storage

    def get(self) -> dict[str, Any]:
        return {"hostname": self._storage.get("custom_domain", "")}

    def set(self, hostname: str) -> dict[str, Any]:
        self._storage["custom_domain"] = hostname
        return {"hostname": hostname, "status": "configured"}

    def verify(self) -> dict[str, Any]:
        return {"verified": True}

    def delete(self) -> None:
        self._storage.pop("custom_domain", None)


class MockRxResumeClient:
    """Synchronous offline mock client implementing full Reactive Resume SDK methods."""

    def __init__(self, base_url: str = "http://offline.mock", api_key: str = "mock-key") -> None:
        self.base_url = base_url
        self.api_key = api_key
        self._storage: dict[str, Any] = {
            "resumes": {},
            "cover_letters": {},
            "applications": {},
            "trash": {},
            "threads": {},
            "custom_domain": "",
        }

        # Initialize mock sample resume
        sample_id = "mock-sample-resume"
        now = datetime.now()
        self._storage["resumes"][sample_id] = Resume(
            id=sample_id,
            name="Sample Mock Resume",
            slug="sample-mock-resume",
            data=ResumeData(
                basics=Basics(
                    name="Mock User", headline="Software Engineer", email="mock@local.test"
                )
            ),
            created_at=now,
            updated_at=now,
        )

        self.resumes = _MockResumesAPI(self._storage)
        self.cover_letters = _MockCoverLettersAPI(self._storage)
        self.documents = _MockDocumentsAPI(self._storage)
        self.applications = _MockApplicationsAPI(self._storage)
        self.agent = _MockAgentAPI(self._storage)
        self.custom_domain = _MockCustomDomainAPI(self._storage)

    def health(self) -> SystemHealth:
        return SystemHealth(
            status="healthy",
            version="6.1.1-mock",
            uptime="offline",
            timestamp=datetime.now(),
            database=DependencyHealth(status="healthy", latency_ms=0.0),
            storage=DependencyHealth(status="healthy", latency_ms=0.0),
            redis=DependencyHealth(status="healthy", latency_ms=0.0),
        )

    def reset(self) -> None:
        self._storage.clear()
        self._storage.update(
            {
                "resumes": {},
                "cover_letters": {},
                "applications": {},
                "trash": {},
                "threads": {},
                "custom_domain": "",
            }
        )
        sample_id = "mock-sample-resume"
        now = datetime.now()
        self._storage["resumes"][sample_id] = Resume(
            id=sample_id,
            name="Sample Mock Resume",
            slug="sample-mock-resume",
            data=ResumeData(
                basics=Basics(
                    name="Mock User", headline="Software Engineer", email="mock@local.test"
                )
            ),
            created_at=now,
            updated_at=now,
        )

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        pass


class _AsyncMockResumesAPI:
    def __init__(self, sync_api: _MockResumesAPI) -> None:
        self._sync = sync_api

    async def list(self, limit: int | None = None, offset: int | None = None) -> list[Resume]:
        return self._sync.list(limit=limit, offset=offset)

    async def get(self, resume_id: str) -> Resume:
        return self._sync.get(resume_id)

    async def create(self, data: ResumeImportData) -> Resume:
        return self._sync.create(data)

    async def import_resume(self, data: ResumeImportData) -> Resume:
        return self._sync.import_resume(data)

    async def update(self, resume_id: str, data: dict[str, Any]) -> Resume:
        return self._sync.update(resume_id, data)

    async def delete(self, resume_id: str) -> None:
        self._sync.delete(resume_id)

    async def export(self, resume_id: str, format: str = "pdf") -> bytes:
        return self._sync.export(resume_id, format=format)

    async def export_json_resume(self, resume_id: str) -> dict[str, Any]:
        return self._sync.export_json_resume(resume_id)


class _AsyncMockCoverLettersAPI:
    def __init__(self, sync_api: _MockCoverLettersAPI) -> None:
        self._sync = sync_api

    async def list(self) -> list[CoverLetter]:
        return self._sync.list()

    async def get(self, cover_letter_id: str) -> CoverLetter:
        return self._sync.get(cover_letter_id)

    async def create(self, data: CoverLetterCreate) -> CoverLetter:
        return self._sync.create(data)

    async def delete(self, cover_letter_id: str) -> None:
        self._sync.delete(cover_letter_id)


class _AsyncMockDocumentsAPI:
    def __init__(self, sync_api: _MockDocumentsAPI) -> None:
        self._sync = sync_api

    async def get_counts(self) -> dict[str, int]:
        return self._sync.get_counts()

    async def trash(self, document_id: str, doc_type: str = "resume") -> None:
        self._sync.trash(document_id, doc_type=doc_type)

    async def restore(self, document_id: str, doc_type: str = "resume") -> None:
        self._sync.restore(document_id, doc_type=doc_type)

    async def purge(self, document_id: str, doc_type: str = "resume") -> None:
        self._sync.purge(document_id, doc_type=doc_type)


class _AsyncMockAgentAPI:
    def __init__(self, sync_api: _MockAgentAPI) -> None:
        self._sync = sync_api

    async def list_threads(self) -> list[dict[str, Any]]:
        return self._sync.list_threads()

    async def create_thread(self, ai_provider_id: str | None = None) -> dict[str, Any]:
        return self._sync.create_thread(ai_provider_id=ai_provider_id)

    def resume_message_stream(
        self, thread_id: str, raw: bool = False
    ) -> AsyncIterator[AgentStreamEvent] | AsyncIterator[str]:
        async def _agen():
            for item in self._sync.resume_message_stream(thread_id, raw=raw):
                yield item

        return _agen()


class AsyncMockRxResumeClient:
    """Asynchronous offline mock client implementing full Reactive Resume SDK methods."""

    def __init__(self, base_url: str = "http://offline.mock", api_key: str = "mock-key") -> None:
        self._sync_client = MockRxResumeClient(base_url=base_url, api_key=api_key)
        self.resumes = _AsyncMockResumesAPI(self._sync_client.resumes)
        self.cover_letters = _AsyncMockCoverLettersAPI(self._sync_client.cover_letters)
        self.documents = _AsyncMockDocumentsAPI(self._sync_client.documents)
        self.agent = _AsyncMockAgentAPI(self._sync_client.agent)

    async def health(self) -> SystemHealth:
        return self._sync_client.health()

    def reset(self) -> None:
        self._sync_client.reset()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args: object) -> None:
        pass
