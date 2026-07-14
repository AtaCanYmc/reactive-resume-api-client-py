import pytest
import respx
from httpx import Response
from reactive_resume import RxResumeClient, AsyncRxResumeClient
from reactive_resume.models import AgentResponse

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
def test_sync_agent(sync_client):
    route_chat = respx.post(f"{BASE_URL}/api/openapi/agent/resume-123/chat").mock(
        return_value=Response(200, json={"response": "Draft updated!"})
    )
    res = sync_client.agent.chat("resume-123", "Write details")
    assert isinstance(res, AgentResponse)
    assert res.response == "Draft updated!"
    assert route_chat.called

    route_threads = respx.get(f"{BASE_URL}/api/openapi/agent/threads").mock(
        return_value=Response(200, json=[{"id": "thread-1"}])
    )
    threads = sync_client.agent.list_threads()
    assert len(threads) == 1
    assert threads[0]["id"] == "thread-1"
    assert route_threads.called

    route_thread = respx.get(f"{BASE_URL}/api/openapi/agent/threads/thread-1").mock(
        return_value=Response(200, json={"id": "thread-1", "messages": []})
    )
    thread = sync_client.agent.get_thread("thread-1")
    assert thread["id"] == "thread-1"
    assert route_thread.called


@pytest.mark.asyncio
@respx.mock
async def test_async_agent(async_client):
    route_chat = respx.post(f"{BASE_URL}/api/openapi/agent/resume-123/chat").mock(
        return_value=Response(200, json={"response": "Draft updated!"})
    )
    res = await async_client.agent.chat("resume-123", "Write details")
    assert isinstance(res, AgentResponse)
    assert res.response == "Draft updated!"
    assert route_chat.called

    route_threads = respx.get(f"{BASE_URL}/api/openapi/agent/threads").mock(
        return_value=Response(200, json=[{"id": "thread-1"}])
    )
    threads = await async_client.agent.list_threads()
    assert len(threads) == 1
    assert threads[0]["id"] == "thread-1"
    assert route_threads.called

    route_thread = respx.get(f"{BASE_URL}/api/openapi/agent/threads/thread-1").mock(
        return_value=Response(200, json={"id": "thread-1", "messages": []})
    )
    thread = await async_client.agent.get_thread("thread-1")
    assert thread["id"] == "thread-1"
    assert route_thread.called
