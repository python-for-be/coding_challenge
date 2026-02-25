async def test_health_endpoint_success(async_test_client):
    response = await async_test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK", "version": "0.0.1"}
