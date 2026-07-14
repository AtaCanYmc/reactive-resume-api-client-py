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
def test_sync_global_statistics(sync_client):
    respx.get(f"{BASE_URL}/api/openapi/statistics/users").mock(
        return_value=Response(200, json={"count": 100})
    )
    respx.get(f"{BASE_URL}/api/openapi/statistics/github/stars").mock(
        return_value=Response(200, json={"stars": 5000})
    )
    respx.get(f"{BASE_URL}/api/openapi/statistics/resumes").mock(
        return_value=Response(200, json={"count": 250})
    )

    users = sync_client.statistics.get_users_count()
    stars = sync_client.statistics.get_github_stars()
    resumes = sync_client.statistics.get_resumes_count()

    assert users == {"count": 100}
    assert stars == {"stars": 5000}
    assert resumes == {"count": 250}


@pytest.mark.asyncio
@respx.mock
async def test_async_global_statistics(async_client):
    respx.get(f"{BASE_URL}/api/openapi/statistics/users").mock(
        return_value=Response(200, json={"count": 100})
    )
    respx.get(f"{BASE_URL}/api/openapi/statistics/github/stars").mock(
        return_value=Response(200, json={"stars": 5000})
    )
    respx.get(f"{BASE_URL}/api/openapi/statistics/resumes").mock(
        return_value=Response(200, json={"count": 250})
    )

    users = await async_client.statistics.get_users_count()
    stars = await async_client.statistics.get_github_stars()
    resumes = await async_client.statistics.get_resumes_count()

    assert users == {"count": 100}
    assert stars == {"stars": 5000}
    assert resumes == {"count": 250}
