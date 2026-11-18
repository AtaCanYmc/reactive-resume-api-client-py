"""FastMCP server implementation for Reactive Resume.

Provides MCP tools, resources, and prompt templates for LLMs to inspect,
create, export, and tailor resumes and job applications.
"""

from __future__ import annotations

import base64
import sys
from typing import Any

try:
    from fastmcp import FastMCP

    _HAS_FASTMCP = True
except ImportError:
    FastMCP = Any  # type: ignore[misc,assignment]
    _HAS_FASTMCP = False

from reactive_resume.cli.config import get_client
from reactive_resume.core.client import RxResumeClient
from reactive_resume.models import CoverLetterCreate


def create_mcp_server(
    url: str | None = None,
    api_key: str | None = None,
    token: str | None = None,
    profile: str | None = None,
) -> FastMCP:
    """Create and configure the FastMCP Reactive Resume server."""
    if not _HAS_FASTMCP:
        raise ImportError(
            "FastMCP is not installed. Install it using: pip install 'rxresume-python[mcp]'"
        )

    mcp = FastMCP(
        name="Reactive Resume",
    )

    def _client() -> RxResumeClient:
        return get_client(url=url, api_key=api_key, token=token, profile=profile)

    # --- TOOLS ---

    @mcp.tool()
    def check_health() -> dict[str, Any]:
        """Check Reactive Resume server, version, database, and storage health."""
        client = _client()
        health = client.health()
        return health.model_dump()

    @mcp.tool()
    def list_resumes(limit: int = 10, offset: int = 0) -> list[dict[str, Any]]:
        """List user resumes with optional pagination limit and offset."""
        client = _client()
        resumes = client.resumes.list(limit=limit, offset=offset)
        return [r.model_dump() for r in resumes]

    @mcp.tool()
    def get_resume(resume_id: str) -> dict[str, Any]:
        """Retrieve complete resume details (sections, work experience, education, skills)."""
        client = _client()
        resume = client.resumes.get(resume_id)
        return resume.model_dump()

    @mcp.tool()
    def export_resume(resume_id: str, format: str = "json") -> str:
        """Export a resume in the specified format: 'pdf', 'docx', 'md', or 'json'.

        For text formats (md, json) returns the decoded string.
        For binary formats (pdf, docx) returns a base64-encoded string.
        """
        client = _client()
        data = client.resumes.export(resume_id, format=format)
        if format in ("md", "markdown", "json"):
            return data.decode("utf-8", errors="replace")
        return base64.b64encode(data).decode("ascii")

    @mcp.tool()
    def get_resume_checks(resume_id: str) -> dict[str, Any]:
        """Run ATS compatibility, content quality, and editor grammar checks on a resume."""
        client = _client()
        return client.resumes.get_checks(resume_id)

    @mcp.tool()
    def match_job_description(resume_id: str, job_description: str) -> dict[str, Any]:
        """Match resume against job posting text to extract matched/missing keywords and fit score."""
        client = _client()
        return client.resumes.match_job(resume_id, job_description)

    @mcp.tool()
    def list_cover_letters() -> list[dict[str, Any]]:
        """List standalone cover letters."""
        client = _client()
        letters = client.cover_letters.list()
        return [cl.model_dump() for cl in letters]

    @mcp.tool()
    def create_cover_letter(name: str, slug: str, content: str) -> dict[str, Any]:
        """Create a new standalone cover letter document."""
        client = _client()
        created = client.cover_letters.create(
            CoverLetterCreate(title=name, slug=slug, content=content)
        )
        return created.model_dump()

    @mcp.tool()
    def list_job_applications(
        status: str | None = None, limit: int = 20, offset: int = 0
    ) -> list[dict[str, Any]]:
        """List job applications in the user's tracking pipeline."""
        client = _client()
        apps = client.applications.list(status=status, limit=limit, offset=offset)
        return [app.model_dump() for app in apps]

    @mcp.tool()
    def close_job_application(app_id: str, reason: str = "not-selected") -> dict[str, Any]:
        """Close a job application with a reason ('not-selected', 'withdrew', 'accepted-other', 'no-response')."""
        client = _client()
        app = client.applications.close(app_id, reason=reason)
        return app.model_dump()

    @mcp.tool()
    def get_document_counts() -> dict[str, Any]:
        """Get counts of active resumes, cover letters, and items in trash."""
        client = _client()
        return client.documents.get_counts()

    @mcp.tool()
    def trash_document(doc_type: str, document_id: str) -> dict[str, Any]:
        """Move a document ('resume' or 'cover_letter') to 30-day trash."""
        client = _client()
        client.documents.trash(doc_type, document_id)
        return {"success": True, "id": document_id, "type": doc_type}

    @mcp.tool()
    def restore_document(document_id: str) -> dict[str, Any]:
        """Restore a document from 30-day trash."""
        client = _client()
        client.documents.restore(document_id)
        return {"success": True, "id": document_id}

    @mcp.tool()
    def list_career_facts(application_id: str | None = None) -> list[dict[str, Any]]:
        """List stored career memory facts for the user, optionally filtered by application."""
        client = _client()
        return client.career.list_facts(application_id=application_id)

    @mcp.tool()
    def create_career_fact(fact_text: str) -> dict[str, Any]:
        """Store a new career fact into the user's career memory bank."""
        client = _client()
        return client.career.create_fact({"fact": fact_text})

    # --- RESOURCES ---

    @mcp.resource("rxresume://health")
    def health_resource() -> str:
        """System health and version status resource."""
        client = _client()
        return client.health().model_dump_json()

    @mcp.resource("rxresume://resumes/{resume_id}")
    def resume_resource(resume_id: str) -> str:
        """Resume document JSON schema resource by ID."""
        client = _client()
        return client.resumes.get(resume_id).model_dump_json()

    # --- PROMPTS ---

    @mcp.prompt()
    def tailor_resume_for_job(resume_id: str, job_description: str) -> str:
        """Prompt template for tailoring a resume to a specific job posting."""
        return f"""Please review the resume with ID '{resume_id}' and tailor it for the following job posting:

Job Posting:
{job_description}

Instructions:
1. Call 'get_resume' with ID '{resume_id}' to retrieve current resume data.
2. Call 'match_job_description' with ID '{resume_id}' to identify matched and missing keywords.
3. Suggest concrete rewrites for the summary, work experience bullet points, and skills to highlight relevant experience without fabricating false information.
"""

    @mcp.prompt()
    def write_cover_letter_for_job(resume_id: str, company: str, job_description: str) -> str:
        """Prompt template for drafting a targeted cover letter."""
        return f"""Please draft a professional cover letter applying to {company} using resume '{resume_id}'.

Job Description:
{job_description}

Instructions:
1. Retrieve the resume using 'get_resume' with ID '{resume_id}'.
2. Craft a compelling 3-4 paragraph cover letter aligning the candidate's achievements with the company's needs.
3. Offer to call 'create_cover_letter' with the drafted content to save it to Reactive Resume.
"""

    return mcp


def main() -> None:
    """Run FastMCP server using stdio or sse transport."""
    import argparse

    parser = argparse.ArgumentParser(description="Reactive Resume FastMCP Server")
    parser.add_argument("--url", help="Base URL of the Reactive Resume instance")
    parser.add_argument("--api-key", help="API key for authentication")
    parser.add_argument("--token", help="Bearer token for authentication")
    parser.add_argument("--profile", help="Configuration profile to use")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="MCP transport protocol (default: stdio)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for SSE transport (default: 8000)",
    )

    args = parser.parse_args()

    mcp = create_mcp_server(
        url=args.url,
        api_key=args.api_key,
        token=args.token,
        profile=args.profile,
    )

    if args.transport == "sse":
        print(
            f"Starting Reactive Resume FastMCP server on SSE port {args.port}...", file=sys.stderr
        )
        mcp.run(transport="sse", port=args.port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
