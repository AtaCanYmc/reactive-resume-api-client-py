# Quickstart Guide

Get up and running with the Reactive Resume Python SDK in under 3 minutes.

---

## 🔑 Authentication

Before using the client, you need:
1. **Server URL**: (e.g., `https://rxresu.me` or your self-hosted URL instance).
2. **API Key**: Obtained from the settings page under **Settings -> API Keys** in your Reactive Resume panel.

### Production Environment Best Practices

For security, **never hardcode your credentials**. Load them dynamically using environment variables or a `.env` file helper:

```python
import os
from reactive_resume import AsyncRxResumeClient

# Load securely from system environment
RX_BASE_URL = os.getenv("RXRESUME_BASE_URL", "https://rxresu.me")
RX_API_KEY = os.getenv("RXRESUME_API_KEY")

if not RX_API_KEY:
    raise ValueError("RXRESUME_API_KEY environment variable is not configured.")
```

---

## ⚡ Asynchronous Example (FastAPI / Asyncio)

We recommend using the asynchronous client (`AsyncRxResumeClient`) for modern asynchronous applications to prevent blocking operations:


```python
import asyncio
from reactive_resume import AsyncRxResumeClient
from reactive_resume.models import ResumeImportData, Basics

async def main():
    # Initialize the client (supports context manager)
    async with AsyncRxResumeClient(
        base_url="https://rxresu.me",
        api_key="your_api_key_here"
    ) as client:

        # 1. Define resume import structure
        cv_data = ResumeImportData(
            title="Ata Can Yaymacı - Backend Architect",
            basics=Basics(
                name="Ata Can Yaymacı",
                headline="Backend Engineer",
                email="ata@example.com"
            )
        )

        # 2. Create/Import the resume
        new_cv = await client.resumes.import_resume(cv_data)
        print(f"Successfully created: {new_cv.name} (ID: {new_cv.id})")

        # 3. Retrieve download PDF URL
        pdf_url = await client.resumes.get_pdf_url(new_cv.id)
        print(f"Download your PDF at: {pdf_url}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🚀 Synchronous Example (Scripts / Sync Code)

If you are writing a simple automation script or working in a synchronous context, use `RxResumeClient`:

```python
from reactive_resume import RxResumeClient

with RxResumeClient(base_url="https://rxresu.me", api_key="your_api_key_here") as client:
    resumes = client.resumes.list()
    for cv in resumes:
        print(f"Found CV: {cv.name} | URL Slug: {cv.slug}")
```
