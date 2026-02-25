from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.user import User
from tests.factories import UserFactory


async def test_update_user_success(async_test_client: AsyncClient, db_session: AsyncSession):
    """Verify updating a user through the API."""
    user = await UserFactory.create_async()
    user_id = user.id

    update_data = {
        "firstname": "UpdatedFirst",
        "lastname": "UpdatedLast",
        "date_of_birth": "1995-05-05",
        "address": {
            "number": "999",
            "street_name": "New St",
            "city": "New City",
            "postcode": "NEW1 1AA",
            "country": "UK",
        },
    }

    response = await async_test_client.put(f"/users/{user_id}", json=update_data)

    assert response.status_code == 200
    # Verify API response
    data = response.json()
    assert data["firstname"] == update_data["firstname"]
    assert data["lastname"] == update_data["lastname"]
    assert data["date_of_birth"] == update_data["date_of_birth"]
    assert data["address"] == update_data["address"]

    # Verify database record
    stmt = select(User).where(User.id == user_id).options(selectinload(User.address))
    result = await db_session.execute(stmt)
    db_user = result.scalar_one()

    assert db_user.firstname == update_data["firstname"]
    assert db_user.lastname == update_data["lastname"]
    assert db_user.date_of_birth.isoformat() == update_data["date_of_birth"]
    assert db_user.address.number == update_data["address"]["number"]
    assert db_user.address.street_name == update_data["address"]["street_name"]
    assert db_user.address.city == update_data["address"]["city"]
    assert db_user.address.postcode == update_data["address"]["postcode"]
    assert db_user.address.country == update_data["address"]["country"]
