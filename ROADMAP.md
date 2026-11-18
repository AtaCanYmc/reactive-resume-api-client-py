# Project Roadmap

This roadmap documents the architectural progression and planned technical milestones for `rxresume-python`.

## Milestones

### v0.5.0 (Released)
- Core client implementation: Synchronous (`RxResumeClient`) and Asynchronous (`AsyncRxResumeClient`).
- Pydantic v2 typed schema validation across all Reactive Resume v4 entities.
- Typed exception hierarchy mapping HTTP 401, 403, 404, and 5xx responses.
- Full unit test suite with `respx` mock integration.

### v0.6.0 (Released)
- Complete Reactive Resume v6.1.1 API alignment: Standalone Cover Letters, Document Trash/Restore, Custom Domains, and System Health endpoint (`/api/health`).
- Enhanced Resumes & Applications APIs with pagination, formats (PDF, DOCX, Markdown, JSON), and v6 closed reason semantics.
- Flask demo application with Docker and Docker Compose support.
- Dependency audit and security remediation: zero known vulnerabilities with `pip-audit`.
- Built-in `rxresume` CLI supporting resume operations, cover letters, trash lifecycle, health status, configuration profiles, document parsing, and agent interactions.
- Built-in FastMCP server for AI assistant and editor integration (Claude Desktop, Cursor, Antigravity).
- Homebrew formula and tap distribution (`brew install AtaCanYmc/tap/rxresume`).
- Development automation via `Makefile` and verified GitHub Actions CI workflows.

### v0.7.0 (Current)
- **Streaming Response Handler**: Real-time Server-Sent Events (SSE) consumer for AI agent interactions (`client.agent.resume_message_stream`) supporting both synchronous and asynchronous iterators.
- **JSON Resume Standard Interoperability**: Bi-directional transformation and JSON Schema validation tools (`to_json_resume`, `from_json_resume`, `validate_json_resume`, `client.resumes.export_json_resume`).
- **Batch Migration CLI**: Mass import command (`rxresume resumes batch-import`) with recursive directory scanning, automatic schema detection (Reactive Resume vs JSON Resume vs PDF), dry-run validation, and tabular execution summaries.
- **Offline Mock Client**: Zero-network test doubles (`MockRxResumeClient` and `AsyncMockRxResumeClient`) with stateful in-memory storage for unit tests, local development, and CI environments without live Reactive Resume instances.

### v0.8.0 (Planned)
- **Automatic Retry & Network Resilience**: Configurable exponential backoff with full jitter for transient 429 rate limits and 5xx network interruptions.
- **Webhook Event Dispatcher**: Typed payload models and signature verification for Reactive Resume server webhook events (resume lifecycle, export readiness, trash callbacks).
- **Career & Voice Media Helpers**: First-class support for audio interview uploads and speech-to-text career fact transcription (`client.career.upload_voice`).
- **Interactive TUI / Prompt CLI**: Terminal wizard (`rxresume resumes create --interactive`) for prompt-driven resume creation and section editing.
- **FastMCP Extended Toolsets**: Bi-directional resume synchronizer tools and semantic search across local cached resumes within MCP clients.

### v1.0.0 (Long-Term / Production Hardened)
- **Bi-directional File Watcher**: Local daemon (`rxresume watch`) keeping local `.json` / `.yaml` resume files continuously in sync with remote Reactive Resume instances.
- **Pluggable Local Cache**: Built-in caching layer (Redis / SQLite) with TTL and ETag support for high-throughput public resume lookups.
- **Multi-Instance / Organization Management**: First-class support for switching between multiple self-hosted instances, workspace contexts, and role-based access controls.
- **Zero-Dependency Core Distribution**: Optional ultralight distribution minimizing transitive dependencies for embedded agent and microservice use.
