import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.fixture
async def async_test_client():
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


async def test_health_endpoint_success(async_test_client):
    response = await async_test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK", "version": "0.0.1"}