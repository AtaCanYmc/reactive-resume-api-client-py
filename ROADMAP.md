# Project Roadmap

This roadmap documents the architectural progression and planned technical milestones for `rxresume-python`.

## Milestones

### v0.5.0 (Released)
- Core client implementation: Synchronous (`RxResumeClient`) and Asynchronous (`AsyncRxResumeClient`).
- Pydantic v2 typed schema validation across all Reactive Resume v4 entities.
- Comprehensive exception hierarchy mapping HTTP 401, 403, 404, and 5xx responses.
- Full unit test suite with `respx` mock integration.

### v0.6.0 (Current)
- Complete Reactive Resume v6.1.1 API alignment: Standalone Cover Letters, Document Trash/Restore, Custom Domains, and System Health endpoint (`/api/health`).
- Enhanced Resumes & Applications APIs with pagination, formats (PDF, DOCX, Markdown, JSON), and v6 closed reason semantics.
- Flask demo application with Docker and Docker Compose support.
- Dependency audit and security remediation: zero known vulnerabilities with `pip-audit`.
- Built-in `rxresume` CLI supporting resume operations, cover letters, trash lifecycle, health status, configuration profiles, document parsing, and agent interactions.
- Development automation via `Makefile` and verified GitHub Actions CI workflows.

### v0.7.0 (Planned)
- Streaming response handler for agent message streams (`client.agent.resume_message_stream`).
- Native JSON resume export and validation utilities compliant with JSON Resume schema.
- Extended batch import CLI command for mass resume migration.
- Offline mock client for local testing without network connectivity.
