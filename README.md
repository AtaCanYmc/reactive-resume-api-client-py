# Reactive Resume Python SDK (`rxresume-python`)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Pydantic v2](https://img.shields.io/badge/pydantic-v2-red.svg)](https://docs.pydantic.dev/)
[![HTTPX](https://img.shields.io/badge/http--client-httpx-brightgreen.svg)](https://www.python-httpx.org/)

An unofficial modern, type-safe Python API Client (SDK) for **Reactive Resume v4**.

It supports both synchronous (`httpx.Client`) and asynchronous (`httpx.AsyncClient`) clients, ensures fully typed request/response schemas using **Pydantic v2**, and maps API errors to clean, descriptive Python exceptions.

---

## Features

- **Dual client modes**: Support for both sync and async APIs.
- **Full API coverage**: Integrated modules for Resume management, Job Applications tracking, AI Agent, AI Providers configurations, Global Statistics, and Feature Flags.
- **Type safety**: Fully typed models for all entities using Pydantic V2.
- **Robust error handling**: Raw API status errors are automatically parsed into specific exceptions (`AuthenticationError`, `NotFoundError`, etc.).
- **Developer Experience (DX)**: Code-completion ready with clear typing and docstrings.

---

## Architecture

```mermaid
graph TD
    UserApp[User Application / Script] -->|Instantiates| SyncClient[RxResumeClient]
    UserApp -->|Instantiates| AsyncClient[AsyncRxResumeClient]

    subgraph "Service Modules (Sync & Async)"
        SyncClient --> Auth[auth]
        SyncClient --> Resumes[resumes]
        SyncClient --> Stats[statistics]
        SyncClient --> Agent[agent]
        SyncClient --> AIProviders[ai_providers]
        SyncClient --> Flags[flags]
        SyncClient --> AI[ai]
        SyncClient --> Applications[applications]
    end

    Auth -->|HTTP/REST Calls| Backend[Reactive Resume v4 API Backend]
    Resumes -->|HTTP/REST Calls| Backend
    Stats -->|HTTP/REST Calls| Backend
    Agent -->|HTTP/REST Calls| Backend
    AIProviders -->|HTTP/REST Calls| Backend
    Flags -->|HTTP/REST Calls| Backend
    AI -->|HTTP/REST Calls| Backend
    Applications -->|HTTP/REST Calls| Backend
```

---

## Capability Matrix

| Service Module | Sync | Async | Key Mapped Endpoints (Postman Collection) |
| :--- | :---: | :---: | :--- |
| **Resumes** (`client.resumes`) | Yes | Yes | List, Get, Create, Update, Delete, Import, Download PDF, Set/Verify/Remove Password, Duplicate, Lock, Version History, Public Resume, Statistics |
| **Applications** (`client.applications`) | Yes | Yes | List, Get, Create, Delete, List Tags, Pipeline Stats, Bulk Import |
| **Auth** (`client.auth`) | Yes | Yes | List Providers, Export Account, Delete Account |
| **Statistics** (`client.statistics`) | Yes | Yes | Users Count, GitHub Stars, Resumes Count (Global Stats) |
| **Agent** (`client.agent`) | Yes | Yes | List Threads, Create/Get/Delete Threads, Send Message, Stop Active Run, Resume Message Stream, Create/Delete Attachment, Revert Action |
| **AI Providers** (`client.ai_providers`) | Yes | Yes | List, Create, Update, Delete, Test saved AI providers |
| **AI Functions** (`client.ai`) | Yes | Yes | Parse PDF, Parse DOCX, Chat, Analyze Resume |
| **Feature Flags** (`client.flags`) | Yes | Yes | List Server-side Feature Flags |


## Installation

Install the package via `pip` or your favorite package manager:

```bash
pip install rxresume-python
```

---

## Quick Start

### 1. Asynchronous Client (FastAPI / Asynchronous Code)

```python
import asyncio
from reactive_resume import AsyncRxResumeClient
from reactive_resume.models import ResumeImportData, Basics

async def main():
    # Initialize the async client
    async with AsyncRxResumeClient(base_url="https://rxresu.me", api_key="your_api_key") as client:
        # Create a new resume
        import_data = ResumeImportData(
            title="Ata Can Yaymacı - Backend Engineer",
            basics=Basics(
                name="Ata Can Yaymacı",
                headline="Backend Engineer",
                email="ata@example.com",
                phone="+905555555555",
                website="https://example.com"
            ),
            sections={}
        )

        try:
            # Import/Create a new resume
            new_resume = await client.resumes.import_resume(import_data)
            print(f"Created resume: {new_resume.name} (ID: {new_resume.id})")

            # Download the compiled PDF bytes
            pdf_bytes = await client.resumes.download_pdf(new_resume.id)
            print(f"Downloaded PDF: {len(pdf_bytes)} bytes")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Synchronous Client

```python
from reactive_resume import RxResumeClient

with RxResumeClient(base_url="https://rxresu.me", api_key="your_api_key") as client:
    resumes = client.resumes.list()
    for resume in resumes:
        print(f"Resume: {resume.name} (Slug: {resume.slug})")
```

### 3. Advanced Features (AI Agent, Statistics, Applications)

```python
with RxResumeClient(base_url="https://rxresu.me", api_key="your_api_key") as client:
    # 1. Start a new AI Agent thread and send a message
    thread = client.agent.create_thread()
    response = client.agent.send_message(thread["id"], "Suggest a professional summary for a software developer.")
    print(f"AI Suggestion: {response}")

    # 2. Retrieve global resume platform metrics
    users_count = client.statistics.get_users_count()
    print(f"Platform Users: {users_count}")

    # 3. List job applications
    apps = client.applications.list()
    for app in apps:
        print(f"Job application: {app.company} - {app.position} ({app.stage})")

    # 4. Check server-side feature flags
    flags = client.flags.list()
    print(f"Signups disabled: {flags.get('isSignupsDisabled')}")
```


---


## Error Handling

All client API calls map HTTP errors to specific exception classes:

```python
from reactive_resume import RxResumeClient, AuthenticationError, NotFoundError

try:
    with RxResumeClient(base_url="https://rxresu.me", api_key="wrong_key") as client:
        client.resumes.list()
except AuthenticationError as e:
    print(f"Auth error (Status {e.status_code}): {e}")
except NotFoundError as e:
    print(f"Not found: {e}")
except Exception as e:
    print(f"Generic error: {e}")
```

---

## Development & Testing

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/reactive-resume-api-client-py.git
   cd reactive-resume-api-client-py
   ```

2. Install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

3. Run the tests:
   ```bash
   pytest
   ```

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.
