# Reactive Resume Python SDK (`rxresume-python`)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Pydantic v2](https://img.shields.io/badge/pydantic-v2-red.svg)](https://docs.pydantic.dev/)
[![HTTPX](https://img.shields.io/badge/http--client-httpx-brightgreen.svg)](https://www.python-httpx.org/)

An unofficial modern, type-safe Python API Client (SDK) for **Reactive Resume v4**.

It supports both synchronous (`httpx.Client`) and asynchronous (`httpx.AsyncClient`) clients, ensures fully typed request/response schemas using **Pydantic v2**, and maps API errors to clean, descriptive Python exceptions.

---

## Features

- **Dual client modes**: Support for both sync and async APIs.
- **Full API coverage**: Integrated modules for Resume management, Auth, Job Tracker (Applications), AI Agent prompts, AI Providers configurations, Statistics, and Storage uploads.
- **Type safety**: Fully typed models for all entities using Pydantic V2.
- **Robust error handling**: Raw API status errors are automatically parsed into specific exceptions (`AuthenticationError`, `NotFoundError`, etc.).
- **Developer Experience (DX)**: Code-completion ready with clear typing and docstrings.


---

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

            # Fetch the generated PDF URL
            pdf_url = await client.resumes.get_pdf_url(new_resume.id)
            print(f"PDF URL: {pdf_url}")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Synchronous Client

```python
from reactive_resume import RxResumeClient
from reactive_resume.models import ResumeImportData

with RxResumeClient(base_url="https://rxresu.me", api_key="your_api_key") as client:
    resumes = client.resumes.list()
    for resume in resumes:
        print(f"Resume: {resume.name} (Slug: {resume.slug})")
```

### 3. Advanced Features (AI Agent, Storage, Statistics, Applications)

```python
with RxResumeClient(base_url="https://rxresu.me", api_key="your_api_key") as client:
    # 1. Ask the AI agent to optimize a resume summary
    ai_response = client.agent.chat("resume_id_here", "Suggest a professional summary for a software developer.")
    print(f"AI Suggestion: {ai_response.response}")

    # 2. Upload a profile image to storage
    with open("avatar.png", "rb") as f:
        file_metadata = client.storage.upload_file(f.read(), "avatar.png")
    print(f"Uploaded Image URL: {file_metadata.url}")

    # 3. Retrieve resume metrics
    stats = client.statistics.get("resume_id_here")
    print(f"Views: {stats.views}, Downloads: {stats.downloads}")

    # 4. Log a new job application
    from reactive_resume.models import ApplicationCreate
    app = client.applications.create(ApplicationCreate(
        company="Google",
        position="Senior Backend Engineer",
        stage="Interviewing"
    ))
    print(f"Logged Application ID: {app.id}")

    # 5. Parse a PDF resume into raw resume data
    parsed_cv = client.ai.parse_pdf("my_resume.pdf", "base64_encoded_file_data_here", "ai_provider_id_here")
    print(f"Parsed Name: {parsed_cv.get('basics', {}).get('name')}")

    # 6. Check server-side feature flags
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
