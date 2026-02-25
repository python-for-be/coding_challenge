import pytest
from httpx import AsyncClient, ASGITransport

from src.main import app


@pytest.fixture
async def async_test_client():
    """Provides an asynchronous test client for HTTP requests.

    Returns:
        AsyncGenerator[AsyncClient, None]: An asynchronous HTTP client for testing.
    """
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
