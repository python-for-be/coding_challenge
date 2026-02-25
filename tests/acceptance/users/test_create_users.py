from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.user import User


async def test_create_user_success(async_test_client: AsyncClient, db_session: AsyncSession):
    """Verify creating a new user through the API."""
    user_data = {
        "firstname": "John",
        "lastname": "Doe",
        "date_of_birth": "1990-01-01",
        "address": {
            "number": "123",
            "street_name": "Main St",
            "city": "London",
            "postcode": "SW1A 1AA",
            "country": "UK",
        },
    }

    response = await async_test_client.post("/users", json=user_data)

    assert response.status_code == 201
    data = response.json()
    stmt = select(User).where(User.id == data["id"]).options(selectinload(User.address))
    result = await db_session.execute(stmt)
    user = result.scalar_one()

    assert data["id"] == user.id
    assert data["firstname"] == user_data["firstname"]
    assert data["lastname"] == user_data["lastname"]
    assert data["date_of_birth"] == user_data["date_of_birth"]
    assert data["address"] == user_data["address"]

    assert user.firstname == data["firstname"]
    assert user.address.city == user_data["address"]["city"]


async def test_create_user_raises_date_of_birth_validation_error(async_test_client: AsyncClient) -> None:
    """Verify a validation error is raised for incorrect date_of_birth format.

    Args:
        async_test_client (AsyncClient): Test client

    Returns: None

    """
    response = await async_test_client.post(
        "/users",
        json={
            "firstname": "new",
            "lastname": "user",
            "date_of_birth": "01-01-2000",
            "address": {
                "number": "1",
                "street_name": "new street",
                "city": "new city",
                "postcode": "abc123",
                "country": "UK",
            },
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [{"msg": "Invalid date format, expected YYYY-MM-DD", "type": "date_format_error"}]
    }
