"""Agent API endpoints implementation."""

from typing import List, Dict, Any, Optional


class AgentAPI:
    """Synchronous AI Agent operations."""

    def __init__(self, client) -> None:
        self._client = client

    def list_threads(self) -> List[Dict[str, Any]]:
        """List all active agent threads."""
        response = self._client._request("GET", "/api/openapi/agent/threads")
        return list(response)

    def get_thread(self, thread_id: str) -> Dict[str, Any]:
        """Get details of a specific agent thread by ID."""
        response = self._client._request("GET", f"/api/openapi/agent/threads/{thread_id}")
        return dict(response)

    def delete_thread(self, thread_id: str) -> None:
        """Delete an agent thread by ID."""
        self._client._request("DELETE", f"/api/openapi/agent/threads/{thread_id}")

    def create_thread(
        self, ai_provider_id: Optional[str] = None, source_resume_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new agent thread."""
        payload = {}
        if ai_provider_id is not None:
            payload["aiProviderId"] = ai_provider_id
        if source_resume_id is not None:
            payload["sourceResumeId"] = source_resume_id
        response = self._client._request("POST", "/api/openapi/agent/threads", json=payload)
        return dict(response)

    def get_or_create_thread_for_resume(
        self, ai_provider_id: Optional[str] = None, source_resume_id: Optional[str] = None
    ) -> Dict[str, Any]:
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
        self, thread_id: str, message: Any, attachment_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
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
        ai_provider_id: Optional[str] = None,
        source_resume_id: Optional[str] = None,
    ) -> Dict[str, Any]:
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

    def stop_run(self, thread_id: str, partial_message: Optional[Any] = None) -> Dict[str, Any]:
        """Stop active agent run."""
        payload = {
            "threadId": thread_id,
        }
        if partial_message is not None:
            payload["partialMessage"] = partial_message
        response = self._client._request("POST", "/api/openapi/agent/messages/stop", json=payload)
        return dict(response)

    def resume_message_stream(self, thread_id: str) -> Any:
        """Resume agent message stream."""
        return self._client._request(
            "GET", f"/api/openapi/agent/messages/resume?threadId={thread_id}"
        )

    def create_attachment(
        self, thread_id: str, filename: str, media_type: str, data: str
    ) -> Dict[str, Any]:
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

    def revert_action(self, action_id: str) -> Dict[str, Any]:
        """Restore agent action snapshot."""
        response = self._client._request("POST", f"/api/openapi/agent/actions/{action_id}/revert")
        return dict(response)


class AsyncAgentAPI:
    """Asynchronous AI Agent operations."""

    def __init__(self, client) -> None:
        self._client = client

    async def list_threads(self) -> List[Dict[str, Any]]:
        """List all active agent threads asynchronously."""
        response = await self._client._request("GET", "/api/openapi/agent/threads")
        return list(response)

    async def get_thread(self, thread_id: str) -> Dict[str, Any]:
        """Get details of a specific agent thread by ID asynchronously."""
        response = await self._client._request("GET", f"/api/openapi/agent/threads/{thread_id}")
        return dict(response)

    async def delete_thread(self, thread_id: str) -> None:
        """Delete an agent thread by ID asynchronously."""
        await self._client._request("DELETE", f"/api/openapi/agent/threads/{thread_id}")

    async def create_thread(
        self, ai_provider_id: Optional[str] = None, source_resume_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new agent thread asynchronously."""
        payload = {}
        if ai_provider_id is not None:
            payload["aiProviderId"] = ai_provider_id
        if source_resume_id is not None:
            payload["sourceResumeId"] = source_resume_id
        response = await self._client._request("POST", "/api/openapi/agent/threads", json=payload)
        return dict(response)

    async def get_or_create_thread_for_resume(
        self, ai_provider_id: Optional[str] = None, source_resume_id: Optional[str] = None
    ) -> Dict[str, Any]:
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
        self, thread_id: str, message: Any, attachment_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
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
        ai_provider_id: Optional[str] = None,
        source_resume_id: Optional[str] = None,
    ) -> Dict[str, Any]:
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

    async def stop_run(
        self, thread_id: str, partial_message: Optional[Any] = None
    ) -> Dict[str, Any]:
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

    async def resume_message_stream(self, thread_id: str) -> Any:
        """Resume agent message stream asynchronously."""
        return await self._client._request(
            "GET", f"/api/openapi/agent/messages/resume?threadId={thread_id}"
        )

    async def create_attachment(
        self, thread_id: str, filename: str, media_type: str, data: str
    ) -> Dict[str, Any]:
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

    async def revert_action(self, action_id: str) -> Dict[str, Any]:
        """Restore agent action snapshot asynchronously."""
        response = await self._client._request(
            "POST", f"/api/openapi/agent/actions/{action_id}/revert"
        )
        return dict(response)
