"""Agent API endpoints implementation."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

from ..models.agent import AgentStreamEvent


def _parse_sse_events(lines: Iterator[str]) -> Iterator[AgentStreamEvent]:
    """Parse raw line stream into structured Server-Sent Events."""
    current_event = "message"
    current_data: list[str] = []
    current_id: str | None = None
    current_retry: int | None = None

    for line in lines:
        line = line.rstrip("\r\n")
        if not line:
            if current_data:
                yield AgentStreamEvent(
                    event=current_event,
                    data="\n".join(current_data),
                    id=current_id,
                    retry=current_retry,
                )
                current_event = "message"
                current_data = []
                current_id = None
                current_retry = None
            continue

        if line.startswith(":"):
            continue

        if ":" in line:
            field, _, val = line.partition(":")
            val = val.lstrip(" ")
            if field == "event":
                current_event = val
            elif field == "data":
                current_data.append(val)
            elif field == "id":
                current_id = val
            elif field == "retry":
                try:
                    current_retry = int(val)
                except ValueError:
                    pass
        else:
            if line == "data":
                current_data.append("")

    if current_data:
        yield AgentStreamEvent(
            event=current_event,
            data="\n".join(current_data),
            id=current_id,
            retry=current_retry,
        )


async def _async_parse_sse_events(lines: AsyncIterator[str]) -> AsyncIterator[AgentStreamEvent]:
    """Parse asynchronous raw line stream into structured Server-Sent Events."""
    current_event = "message"
    current_data: list[str] = []
    current_id: str | None = None
    current_retry: int | None = None

    async for line in lines:
        line = line.rstrip("\r\n")
        if not line:
            if current_data:
                yield AgentStreamEvent(
                    event=current_event,
                    data="\n".join(current_data),
                    id=current_id,
                    retry=current_retry,
                )
                current_event = "message"
                current_data = []
                current_id = None
                current_retry = None
            continue

        if line.startswith(":"):
            continue

        if ":" in line:
            field, _, val = line.partition(":")
            val = val.lstrip(" ")
            if field == "event":
                current_event = val
            elif field == "data":
                current_data.append(val)
            elif field == "id":
                current_id = val
            elif field == "retry":
                try:
                    current_retry = int(val)
                except ValueError:
                    pass
        else:
            if line == "data":
                current_data.append("")

    if current_data:
        yield AgentStreamEvent(
            event=current_event,
            data="\n".join(current_data),
            id=current_id,
            retry=current_retry,
        )


class AgentAPI:
    """Synchronous AI Agent operations."""

    def __init__(self, client) -> None:
        self._client = client

    def list_threads(self) -> list[dict[str, Any]]:
        """List all active agent threads."""
        response = self._client._request("GET", "/api/openapi/agent/threads")
        return list(response)

    def get_thread(self, thread_id: str) -> dict[str, Any]:
        """Get details of a specific agent thread by ID."""
        response = self._client._request("GET", f"/api/openapi/agent/threads/{thread_id}")
        return dict(response)

    def delete_thread(self, thread_id: str) -> None:
        """Delete an agent thread by ID."""
        self._client._request("DELETE", f"/api/openapi/agent/threads/{thread_id}")

    def create_thread(
        self, ai_provider_id: str | None = None, source_resume_id: str | None = None
    ) -> dict[str, Any]:
        """Create a new agent thread."""
        payload = {}
        if ai_provider_id is not None:
            payload["aiProviderId"] = ai_provider_id
        if source_resume_id is not None:
            payload["sourceResumeId"] = source_resume_id
        response = self._client._request("POST", "/api/openapi/agent/threads", json=payload)
        return dict(response)

    def get_or_create_thread_for_resume(
        self, ai_provider_id: str | None = None, source_resume_id: str | None = None
    ) -> dict[str, Any]:
        """Get or create an in-resume agent thread."""
        payload = {}
        if ai_provider_id is not None:
            payload["aiProviderId"] = ai_provider_id
        if source_resume_id is not None:
            payload["sourceResumeId"] = source_resume_id
        response = self._client._request(
            "POST", "/api/openapi/agent/threads/for-resume", json=payload
        )
        return dict(response)

    def send_message(
        self, thread_id: str, message: Any, attachment_ids: list[str] | None = None
    ) -> dict[str, Any]:
        """Send an agent message."""
        payload = {
            "threadId": thread_id,
            "message": message,
        }
        if attachment_ids is not None:
            payload["attachmentIds"] = attachment_ids
        response = self._client._request("POST", "/api/openapi/agent/messages/send", json=payload)
        return dict(response)

    def archive_thread(
        self,
        thread_id: str,
        ai_provider_id: str | None = None,
        source_resume_id: str | None = None,
    ) -> dict[str, Any]:
        """Archive an agent thread."""
        payload = {}
        if ai_provider_id is not None:
            payload["aiProviderId"] = ai_provider_id
        if source_resume_id is not None:
            payload["sourceResumeId"] = source_resume_id
        response = self._client._request(
            "POST", f"/api/openapi/agent/threads/{thread_id}/archive", json=payload
        )
        return dict(response)

    def stop_run(self, thread_id: str, partial_message: Any | None = None) -> dict[str, Any]:
        """Stop active agent run."""
        payload = {
            "threadId": thread_id,
        }
        if partial_message is not None:
            payload["partialMessage"] = partial_message
        response = self._client._request("POST", "/api/openapi/agent/messages/stop", json=payload)
        return dict(response)

    def resume_message_stream(
        self, thread_id: str, raw: bool = False
    ) -> Iterator[AgentStreamEvent] | Iterator[str]:
        """Resume agent message stream.

        Args:
            thread_id: The ID of the agent thread.
            raw: If True, yields raw text lines from the HTTP stream.
                 If False (default), yields parsed AgentStreamEvent objects.

        Yields:
            AgentStreamEvent instances or raw text lines.
        """
        line_stream = self._client._stream_request(
            "GET",
            "/api/openapi/agent/messages/resume",
            params={"threadId": thread_id},
            headers={"Accept": "text/event-stream"},
        )
        if raw:
            return line_stream
        return _parse_sse_events(line_stream)

    def create_attachment(
        self, thread_id: str, filename: str, media_type: str, data: str
    ) -> dict[str, Any]:
        """Create agent attachment."""
        payload = {
            "threadId": thread_id,
            "filename": filename,
            "mediaType": media_type,
            "data": data,
        }
        response = self._client._request("POST", "/api/openapi/agent/attachments", json=payload)
        return dict(response)

    def delete_attachment(self, attachment_id: str) -> None:
        """Delete agent attachment."""
        self._client._request("DELETE", f"/api/openapi/agent/attachments/{attachment_id}")

    def revert_action(self, action_id: str) -> dict[str, Any]:
        """Restore agent action snapshot."""
        response = self._client._request("POST", f"/api/openapi/agent/actions/{action_id}/revert")
        return dict(response)


class AsyncAgentAPI:
    """Asynchronous AI Agent operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def list_threads(self) -> list[dict[str, Any]]:
        """List all active agent threads asynchronously."""
        response = await self._client._request("GET", "/api/openapi/agent/threads")
        return list(response)

    async def get_thread(self, thread_id: str) -> dict[str, Any]:
        """Get details of a specific agent thread by ID asynchronously."""
        response = await self._client._request("GET", f"/api/openapi/agent/threads/{thread_id}")
        return dict(response)

    async def delete_thread(self, thread_id: str) -> None:
        """Delete an agent thread by ID asynchronously."""
        await self._client._request("DELETE", f"/api/openapi/agent/threads/{thread_id}")

    async def create_thread(
        self, ai_provider_id: str | None = None, source_resume_id: str | None = None
    ) -> dict[str, Any]:
        """Create a new agent thread asynchronously."""
        payload = {}
        if ai_provider_id is not None:
            payload["aiProviderId"] = ai_provider_id
        if source_resume_id is not None:
            payload["sourceResumeId"] = source_resume_id
        response = await self._client._request("POST", "/api/openapi/agent/threads", json=payload)
        return dict(response)

    async def get_or_create_thread_for_resume(
        self, ai_provider_id: str | None = None, source_resume_id: str | None = None
    ) -> dict[str, Any]:
        """Get or create an in-resume agent thread asynchronously."""
        payload = {}
        if ai_provider_id is not None:
            payload["aiProviderId"] = ai_provider_id
        if source_resume_id is not None:
            payload["sourceResumeId"] = source_resume_id
        response = await self._client._request(
            "POST", "/api/openapi/agent/threads/for-resume", json=payload
        )
        return dict(response)

    async def send_message(
        self, thread_id: str, message: Any, attachment_ids: list[str] | None = None
    ) -> dict[str, Any]:
        """Send an agent message asynchronously."""
        payload = {
            "threadId": thread_id,
            "message": message,
        }
        if attachment_ids is not None:
            payload["attachmentIds"] = attachment_ids
        response = await self._client._request(
            "POST", "/api/openapi/agent/messages/send", json=payload
        )
        return dict(response)

    async def archive_thread(
        self,
        thread_id: str,
        ai_provider_id: str | None = None,
        source_resume_id: str | None = None,
    ) -> dict[str, Any]:
        """Archive an agent thread asynchronously."""
        payload = {}
        if ai_provider_id is not None:
            payload["aiProviderId"] = ai_provider_id
        if source_resume_id is not None:
            payload["sourceResumeId"] = source_resume_id
        response = await self._client._request(
            "POST", f"/api/openapi/agent/threads/{thread_id}/archive", json=payload
        )
        return dict(response)

    async def stop_run(self, thread_id: str, partial_message: Any | None = None) -> dict[str, Any]:
        """Stop active agent run asynchronously."""
        payload = {
            "threadId": thread_id,
        }
        if partial_message is not None:
            payload["partialMessage"] = partial_message
        response = await self._client._request(
            "POST", "/api/openapi/agent/messages/stop", json=payload
        )
        return dict(response)

    def resume_message_stream(
        self, thread_id: str, raw: bool = False
    ) -> AsyncIterator[AgentStreamEvent] | AsyncIterator[str]:
        """Resume agent message stream asynchronously.

        Args:
            thread_id: The ID of the agent thread.
            raw: If True, yields raw text lines from the HTTP stream.
                 If False (default), yields parsed AgentStreamEvent objects.

        Yields:
            AgentStreamEvent instances or raw text lines asynchronously.
        """
        line_stream = self._client._stream_request(
            "GET",
            "/api/openapi/agent/messages/resume",
            params={"threadId": thread_id},
            headers={"Accept": "text/event-stream"},
        )
        if raw:
            return line_stream
        return _async_parse_sse_events(line_stream)

    async def create_attachment(
        self, thread_id: str, filename: str, media_type: str, data: str
    ) -> dict[str, Any]:
        """Create agent attachment asynchronously."""
        payload = {
            "threadId": thread_id,
            "filename": filename,
            "mediaType": media_type,
            "data": data,
        }
        response = await self._client._request(
            "POST", "/api/openapi/agent/attachments", json=payload
        )
        return dict(response)

    async def delete_attachment(self, attachment_id: str) -> None:
        """Delete agent attachment asynchronously."""
        await self._client._request("DELETE", f"/api/openapi/agent/attachments/{attachment_id}")

    async def revert_action(self, action_id: str) -> dict[str, Any]:
        """Restore agent action snapshot asynchronously."""
        response = await self._client._request(
            "POST", f"/api/openapi/agent/actions/{action_id}/revert"
        )
        return dict(response)
