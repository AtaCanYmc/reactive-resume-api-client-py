import pytest
import respx
from httpx import Response
from reactive_resume import RxResumeClient, AsyncRxResumeClient

BASE_URL = "https://rxresu.me"
API_KEY = "test-api-key"


@pytest.fixture
def sync_client():
    with RxResumeClient(base_url=BASE_URL, api_key=API_KEY) as client:
        yield client


@pytest.fixture
async def async_client():
    async with AsyncRxResumeClient(base_url=BASE_URL, api_key=API_KEY) as client:
        yield client


@respx.mock
def test_sync_ai_endpoints(sync_client):
    # 1. parse pdf
    route_pdf = respx.post(f"{BASE_URL}/api/openapi/ai/parse-pdf").mock(
        return_value=Response(200, json={"basics": {"name": "Parsed PDF"}})
    )
    res_pdf = sync_client.ai.parse_pdf("resume.pdf", "base64data", "openai-id")
    assert res_pdf["basics"]["name"] == "Parsed PDF"
    assert route_pdf.called

    # 2. parse docx
    route_docx = respx.post(f"{BASE_URL}/api/openapi/ai/parse-docx").mock(
        return_value=Response(200, json={"basics": {"name": "Parsed DOCX"}})
    )
    res_docx = sync_client.ai.parse_docx("resume.docx", "base64data", "openai-id")
    assert res_docx["basics"]["name"] == "Parsed DOCX"
    assert route_docx.called

    # 3. chat
    route_chat = respx.post(f"{BASE_URL}/api/openapi/ai/chat").mock(
        return_value=Response(200, json={"reply": "AI response"})
    )
    res_chat = sync_client.ai.chat({"message": "hi"})
    assert res_chat["reply"] == "AI response"
    assert route_chat.called

    # 4. analyze
    route_analyze = respx.post(f"{BASE_URL}/api/openapi/ai/analyze-resume").mock(
        return_value=Response(200, json={"grammar": []})
    )
    res_analyze = sync_client.ai.analyze_resume("resume-1", "openai-id")
    assert "grammar" in res_analyze
    assert route_analyze.called


@pytest.mark.asyncio
@respx.mock
async def test_async_ai_endpoints(async_client):
    # 1. parse pdf
    route_pdf = respx.post(f"{BASE_URL}/api/openapi/ai/parse-pdf").mock(
        return_value=Response(200, json={"basics": {"name": "Parsed PDF"}})
    )
    res_pdf = await async_client.ai.parse_pdf("resume.pdf", "base64data", "openai-id")
    assert res_pdf["basics"]["name"] == "Parsed PDF"
    assert route_pdf.called

    # 2. parse docx
    route_docx = respx.post(f"{BASE_URL}/api/openapi/ai/parse-docx").mock(
        return_value=Response(200, json={"basics": {"name": "Parsed DOCX"}})
    )
    res_docx = await async_client.ai.parse_docx("resume.docx", "base64data", "openai-id")
    assert res_docx["basics"]["name"] == "Parsed DOCX"
    assert route_docx.called

    # 3. chat
    route_chat = respx.post(f"{BASE_URL}/api/openapi/ai/chat").mock(
        return_value=Response(200, json={"reply": "AI response"})
    )
    res_chat = await async_client.ai.chat({"message": "hi"})
    assert res_chat["reply"] == "AI response"
    assert route_chat.called

    # 4. analyze
    route_analyze = respx.post(f"{BASE_URL}/api/openapi/ai/analyze-resume").mock(
        return_value=Response(200, json={"grammar": []})
    )
    res_analyze = await async_client.ai.analyze_resume("resume-1", "openai-id")
    assert "grammar" in res_analyze
    assert route_analyze.called
