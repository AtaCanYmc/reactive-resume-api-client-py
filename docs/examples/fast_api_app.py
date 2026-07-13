"""Example demonstrating integration of AsyncRxResumeClient into a FastAPI application.

Run using: uvicorn fast_api_app:app --reload
"""

from fastapi import FastAPI, Depends, HTTPException, status
from typing import AsyncGenerator
from reactive_resume import AsyncRxResumeClient
from reactive_resume.core.exceptions import AuthenticationError, NotFoundError

app = FastAPI(title="ResuMesh Backend API Gateway")

# Configuration
RX_RESUME_URL = "https://rxresu.me"
RX_RESUME_API_KEY = "your_api_key_here"


# Dependency Injection for Async Client
async def get_resume_client() -> AsyncGenerator[AsyncRxResumeClient, None]:
    async with AsyncRxResumeClient(base_url=RX_RESUME_URL, api_key=RX_RESUME_API_KEY) as client:
        yield client


@app.get("/cv/{resume_id}/pdf")
async def get_cv_pdf_link(
    resume_id: str,
    client: AsyncRxResumeClient = Depends(get_resume_client),
):
    """Retrieve the direct PDF download URL for a candidate's resume."""
    try:
        # Check if resume exists
        await client.resumes.get(resume_id)
        # Construct and return PDF download URL
        pdf_url = await client.resumes.get_pdf_url(resume_id)
        return {"resume_id": resume_id, "pdf_url": pdf_url}
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"API key authentication failed on Reactive Resume: {e}",
        )
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found in the remote server.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error interfacing with SDK: {e}",
        )
