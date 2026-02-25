from httpx import AsyncClient

async def test_health_endpoint_success(async_test_client: AsyncClient) -> None:
    """Verify the health endpoint returns a 200 status code.

    Returns: None
    """
    response = await async_test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK", "version": "0.0.1"}
