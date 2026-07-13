import pytest
import respx
from httpx import Response
from reactive_resume import RxResumeClient, AsyncRxResumeClient
from reactive_resume.models import StorageFile

BASE_URL = "https://rxresu.me"
API_KEY = "test-api-key"

MOCK_FILE = {
    "filename": "portfolio.png",
    "url": "https://rxresu.me/storage/portfolio.png",
    "size": 2048,
    "mimeType": "image/png",
}


@pytest.fixture
def sync_client():
    with RxResumeClient(base_url=BASE_URL, api_key=API_KEY) as client:
        yield client


@pytest.fixture
async def async_client():
    async with AsyncRxResumeClient(base_url=BASE_URL, api_key=API_KEY) as client:
        yield client


@respx.mock
def test_sync_storage_upload(sync_client):
    route = respx.post(f"{BASE_URL}/api/openapi/storage/upload").mock(
        return_value=Response(201, json=MOCK_FILE)
    )
    file_info = sync_client.storage.upload_file(b"raw-image-bytes", "portfolio.png")
    assert isinstance(file_info, StorageFile)
    assert file_info.filename == "portfolio.png"
    assert file_info.mime_type == "image/png"
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_async_storage_upload(async_client):
    route = respx.post(f"{BASE_URL}/api/openapi/storage/upload").mock(
        return_value=Response(201, json=MOCK_FILE)
    )
    file_info = await async_client.storage.upload_file(b"raw-image-bytes", "portfolio.png")
    assert isinstance(file_info, StorageFile)
    assert file_info.filename == "portfolio.png"
    assert file_info.mime_type == "image/png"
    assert route.called
