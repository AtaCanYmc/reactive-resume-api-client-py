import pytest
import respx
import httpx
from httpx import Response
from reactive_resume import (
    RxResumeClient,
    AsyncRxResumeClient,
    AuthenticationError,
    NotFoundError,
    ReactiveResumeAPIError,
    ReactiveResumeError,
)

BASE_URL = "https://rxresu.me"
API_KEY = "test-api-key"


def test_sync_client_init_and_tokens():
    with RxResumeClient(base_url=BASE_URL, api_key=API_KEY) as client:
        assert client.client.headers["x-api-key"] == API_KEY

        client.set_token("new-jwt-token")
        assert client.client.headers["Authorization"] == "Bearer new-jwt-token"
        assert "x-api-key" not in client.client.headers

        client.set_api_key("new-api-key")
        assert client.client.headers["x-api-key"] == "new-api-key"
        assert "Authorization" not in client.client.headers

    with RxResumeClient(base_url=BASE_URL, token="initial-token") as client:
        assert client.client.headers["Authorization"] == "Bearer initial-token"
        assert "x-api-key" not in client.client.headers


@pytest.mark.asyncio
async def test_async_client_init_and_tokens():
    async with AsyncRxResumeClient(base_url=BASE_URL, api_key=API_KEY) as client:
        assert client.client.headers["x-api-key"] == API_KEY

        client.set_token("new-jwt-token")
        assert client.client.headers["Authorization"] == "Bearer new-jwt-token"
        assert "x-api-key" not in client.client.headers

        client.set_api_key("new-api-key")
        assert client.client.headers["x-api-key"] == "new-api-key"
        assert "Authorization" not in client.client.headers

    async with AsyncRxResumeClient(base_url=BASE_URL, token="initial-token") as client:
        assert client.client.headers["Authorization"] == "Bearer initial-token"
        assert "x-api-key" not in client.client.headers


@respx.mock
def test_sync_client_exceptions():
    with RxResumeClient(base_url=BASE_URL, api_key=API_KEY) as client:
        # 401 AuthenticationError
        respx.get(f"{BASE_URL}/api/openapi/resumes").mock(
            return_value=Response(401, json={"message": "Invalid Key"})
        )
        with pytest.raises(AuthenticationError):
            client.resumes.list()

        # 404 NotFoundError
        respx.get(f"{BASE_URL}/api/openapi/resumes").mock(
            return_value=Response(404, json={"message": "Not Found"})
        )
        with pytest.raises(NotFoundError):
            client.resumes.list()

        # 500 ReactiveResumeAPIError
        respx.get(f"{BASE_URL}/api/openapi/resumes").mock(
            return_value=Response(500, text="Internal Error")
        )
        with pytest.raises(ReactiveResumeAPIError) as exc_info:
            client.resumes.list()
        assert exc_info.value.status_code == 500

        # ConnectionTimeout -> ReactiveResumeError
        respx.get(f"{BASE_URL}/api/openapi/resumes").mock(
            side_effect=httpx.ConnectTimeout("Timeout")
        )
        with pytest.raises(ReactiveResumeError) as exc_info_timeout:
            client.resumes.list()
        assert "Network or connection error occurred" in str(exc_info_timeout.value)


@pytest.mark.asyncio
@respx.mock
async def test_async_client_exceptions():
    async with AsyncRxResumeClient(base_url=BASE_URL, api_key=API_KEY) as client:
        # 401 AuthenticationError
        respx.get(f"{BASE_URL}/api/openapi/resumes").mock(
            return_value=Response(401, json={"message": "Invalid Key"})
        )
        with pytest.raises(AuthenticationError):
            await client.resumes.list()

        # 404 NotFoundError
        respx.get(f"{BASE_URL}/api/openapi/resumes").mock(
            return_value=Response(404, json={"message": "Not Found"})
        )
        with pytest.raises(NotFoundError):
            await client.resumes.list()

        # 500 ReactiveResumeAPIError
        respx.get(f"{BASE_URL}/api/openapi/resumes").mock(
            return_value=Response(500, text="Internal Error")
        )
        with pytest.raises(ReactiveResumeAPIError) as exc_info:
            await client.resumes.list()
        assert exc_info.value.status_code == 500

        # ConnectionTimeout -> ReactiveResumeError
        respx.get(f"{BASE_URL}/api/openapi/resumes").mock(
            side_effect=httpx.ConnectTimeout("Timeout")
        )
        with pytest.raises(ReactiveResumeError) as exc_info_timeout:
            await client.resumes.list()
        assert "Network or connection error occurred" in str(exc_info_timeout.value)


def test_exception_string_representation():
    err = ReactiveResumeAPIError("Custom Error Message")
    assert str(err) == "Custom Error Message"

    err_with_code = ReactiveResumeAPIError("Custom Error Message", status_code=400)
    assert str(err_with_code) == "Custom Error Message [Status 400]"
