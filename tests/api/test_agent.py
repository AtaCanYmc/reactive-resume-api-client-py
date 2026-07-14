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
def test_sync_agent(sync_client):
    # list_threads
    respx.get(f"{BASE_URL}/api/openapi/agent/threads").mock(
        return_value=Response(200, json=[{"id": "thread-1"}])
    )
    threads = sync_client.agent.list_threads()
    assert len(threads) == 1
    assert threads[0]["id"] == "thread-1"

    # get_thread
    respx.get(f"{BASE_URL}/api/openapi/agent/threads/thread-1").mock(
        return_value=Response(200, json={"id": "thread-1", "messages": []})
    )
    thread = sync_client.agent.get_thread("thread-1")
    assert thread["id"] == "thread-1"

    # delete_thread
    respx.delete(f"{BASE_URL}/api/openapi/agent/threads/thread-1").mock(return_value=Response(204))
    sync_client.agent.delete_thread("thread-1")

    # create_thread
    respx.post(f"{BASE_URL}/api/openapi/agent/threads").mock(
        return_value=Response(201, json={"id": "new-thread"})
    )
    new_t = sync_client.agent.create_thread(ai_provider_id="provider-1")
    assert new_t["id"] == "new-thread"

    # get_or_create_thread_for_resume
    respx.post(f"{BASE_URL}/api/openapi/agent/threads/for-resume").mock(
        return_value=Response(200, json={"id": "resume-thread"})
    )
    rt = sync_client.agent.get_or_create_thread_for_resume(source_resume_id="resume-1")
    assert rt["id"] == "resume-thread"

    # send_message
    respx.post(f"{BASE_URL}/api/openapi/agent/messages/send").mock(
        return_value=Response(200, json={"success": True})
    )
    res = sync_client.agent.send_message("thread-1", "hello")
    assert res == {"success": True}

    # archive_thread
    respx.post(f"{BASE_URL}/api/openapi/agent/threads/thread-1/archive").mock(
        return_value=Response(200, json={"archived": True})
    )
    arch = sync_client.agent.archive_thread("thread-1")
    assert arch == {"archived": True}

    # stop_run
    respx.post(f"{BASE_URL}/api/openapi/agent/messages/stop").mock(
        return_value=Response(200, json={"stopped": True})
    )
    stop = sync_client.agent.stop_run("thread-1")
    assert stop == {"stopped": True}

    # resume_message_stream
    respx.get(f"{BASE_URL}/api/openapi/agent/messages/resume?threadId=thread-1").mock(
        return_value=Response(200, content=b"stream-data")
    )
    stream = sync_client.agent.resume_message_stream("thread-1")
    assert stream == b"stream-data"

    # create_attachment
    respx.post(f"{BASE_URL}/api/openapi/agent/attachments").mock(
        return_value=Response(201, json={"id": "attachment-1"})
    )
    att = sync_client.agent.create_attachment("thread-1", "file.pdf", "application/pdf", "data")
    assert att == {"id": "attachment-1"}

    # delete_attachment
    respx.delete(f"{BASE_URL}/api/openapi/agent/attachments/attachment-1").mock(
        return_value=Response(204)
    )
    sync_client.agent.delete_attachment("attachment-1")

    # revert_action
    respx.post(f"{BASE_URL}/api/openapi/agent/actions/action-1/revert").mock(
        return_value=Response(200, json={"reverted": True})
    )
    rev = sync_client.agent.revert_action("action-1")
    assert rev == {"reverted": True}


@pytest.mark.asyncio
@respx.mock
async def test_async_agent(async_client):
    # list_threads
    respx.get(f"{BASE_URL}/api/openapi/agent/threads").mock(
        return_value=Response(200, json=[{"id": "thread-1"}])
    )
    threads = await async_client.agent.list_threads()
    assert len(threads) == 1
    assert threads[0]["id"] == "thread-1"

    # get_thread
    respx.get(f"{BASE_URL}/api/openapi/agent/threads/thread-1").mock(
        return_value=Response(200, json={"id": "thread-1", "messages": []})
    )
    thread = await async_client.agent.get_thread("thread-1")
    assert thread["id"] == "thread-1"

    # delete_thread
    respx.delete(f"{BASE_URL}/api/openapi/agent/threads/thread-1").mock(return_value=Response(204))
    await async_client.agent.delete_thread("thread-1")

    # create_thread
    respx.post(f"{BASE_URL}/api/openapi/agent/threads").mock(
        return_value=Response(201, json={"id": "new-thread"})
    )
    new_t = await async_client.agent.create_thread(ai_provider_id="provider-1")
    assert new_t["id"] == "new-thread"

    # get_or_create_thread_for_resume
    respx.post(f"{BASE_URL}/api/openapi/agent/threads/for-resume").mock(
        return_value=Response(200, json={"id": "resume-thread"})
    )
    rt = await async_client.agent.get_or_create_thread_for_resume(source_resume_id="resume-1")
    assert rt["id"] == "resume-thread"

    # send_message
    respx.post(f"{BASE_URL}/api/openapi/agent/messages/send").mock(
        return_value=Response(200, json={"success": True})
    )
    res = await async_client.agent.send_message("thread-1", "hello")
    assert res == {"success": True}

    # archive_thread
    respx.post(f"{BASE_URL}/api/openapi/agent/threads/thread-1/archive").mock(
        return_value=Response(200, json={"archived": True})
    )
    arch = await async_client.agent.archive_thread("thread-1")
    assert arch == {"archived": True}

    # stop_run
    respx.post(f"{BASE_URL}/api/openapi/agent/messages/stop").mock(
        return_value=Response(200, json={"stopped": True})
    )
    stop = await async_client.agent.stop_run("thread-1")
    assert stop == {"stopped": True}

    # resume_message_stream
    respx.get(f"{BASE_URL}/api/openapi/agent/messages/resume?threadId=thread-1").mock(
        return_value=Response(200, content=b"stream-data")
    )
    stream = await async_client.agent.resume_message_stream("thread-1")
    assert stream == b"stream-data"

    # create_attachment
    respx.post(f"{BASE_URL}/api/openapi/agent/attachments").mock(
        return_value=Response(201, json={"id": "attachment-1"})
    )
    att = await async_client.agent.create_attachment(
        "thread-1", "file.pdf", "application/pdf", "data"
    )
    assert att == {"id": "attachment-1"}

    # delete_attachment
    respx.delete(f"{BASE_URL}/api/openapi/agent/attachments/attachment-1").mock(
        return_value=Response(204)
    )
    await async_client.agent.delete_attachment("attachment-1")

    # revert_action
    respx.post(f"{BASE_URL}/api/openapi/agent/actions/action-1/revert").mock(
        return_value=Response(200, json={"reverted": True})
    )
    rev = await async_client.agent.revert_action("action-1")
    assert rev == {"reverted": True}
