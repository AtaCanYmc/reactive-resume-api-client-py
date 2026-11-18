import pytest
import respx
from httpx import Response

from reactive_resume.mcp.server import create_mcp_server

pytest.importorskip("fastmcp")

BASE_URL = "https://rxresu.me"


MOCK_HEALTH = {
    "service": "reactive-resume",
    "version": "6.1.1",
    "revision": "a1b2c3d4e5f60718293a4b5c6d7e8f9a0b1c2d3e",
    "status": "healthy",
    "timestamp": "2026-11-18T18:00:00Z",
    "uptime": "14d 2h 30m",
    "database": {"status": "healthy", "latencyMs": 1.5},
    "storage": {"status": "healthy", "latencyMs": 2.1},
    "redis": {"status": "healthy", "latencyMs": 0.8},
}


@pytest.mark.asyncio
async def test_mcp_server_registration():
    mcp = create_mcp_server(url=BASE_URL, api_key="test-key")
    assert mcp.name == "Reactive Resume"

    tools = await mcp.list_tools()
    tool_names = [t.name for t in tools]
    assert "check_health" in tool_names
    assert "list_resumes" in tool_names
    assert "get_resume" in tool_names
    assert "export_resume" in tool_names
    assert "get_resume_checks" in tool_names
    assert "match_job_description" in tool_names
    assert "list_cover_letters" in tool_names
    assert "create_cover_letter" in tool_names
    assert "list_job_applications" in tool_names
    assert "close_job_application" in tool_names
    assert "get_document_counts" in tool_names
    assert "trash_document" in tool_names
    assert "restore_document" in tool_names
    assert "list_career_facts" in tool_names
    assert "create_career_fact" in tool_names

    prompts = await mcp.list_prompts()
    prompt_names = [p.name for p in prompts]
    assert "tailor_resume_for_job" in prompt_names
    assert "write_cover_letter_for_job" in prompt_names


@respx.mock
@pytest.mark.asyncio
async def test_mcp_tool_execution():
    respx.get(f"{BASE_URL}/api/health").mock(return_value=Response(200, json=MOCK_HEALTH))
    respx.get(f"{BASE_URL}/api/openapi/documents/counts").mock(
        return_value=Response(200, json={"resumes": 2, "coverLetters": 1, "trash": 0})
    )
    respx.put(f"{BASE_URL}/api/openapi/documents/resume/res-123/trash").mock(
        return_value=Response(200, json={"success": True})
    )

    mcp = create_mcp_server(url=BASE_URL, api_key="test-key")

    # Call tools directly via fastmcp
    health_result = await mcp.call_tool("check_health")
    assert health_result.structured_content is not None
    assert health_result.structured_content["version"] == "6.1.1"

    counts_result = await mcp.call_tool("get_document_counts")
    assert counts_result.structured_content is not None
    assert counts_result.structured_content["resumes"] == 2

    trash_result = await mcp.call_tool(
        "trash_document", arguments={"doc_type": "resume", "document_id": "res-123"}
    )
    assert trash_result.structured_content is not None
    assert trash_result.structured_content["success"] is True
    assert trash_result.structured_content["id"] == "res-123"


def test_cli_mcp_parser():
    from reactive_resume.cli.main import build_parser

    parser = build_parser()
    args = parser.parse_args(["mcp", "--transport", "stdio"])
    assert args.command == "mcp"
    assert args.transport == "stdio"
