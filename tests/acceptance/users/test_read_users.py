from httpx import AsyncClient

from tests.factories import UserFactory


async def test_read_user_records_success(async_test_client: AsyncClient) -> None:
    """Verify fetching multiple user records."""

    user_1, user_2 = await UserFactory.create_batch_async(size=2)

    response = await async_test_client.get("/users")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": user_1.id,
            "firstname": user_1.firstname,
            "lastname": user_1.lastname,
            "date_of_birth": user_1.date_of_birth.isoformat(),
            "address": {
                "number": user_1.address.number,
                "street_name": user_1.address.street_name,
                "city": user_1.address.city,
                "postcode": user_1.address.postcode,
                "country": user_1.address.country,
            },
        },
        {
            "id": user_2.id,
            "firstname": user_2.firstname,
            "lastname": user_2.lastname,
            "date_of_birth": user_2.date_of_birth.isoformat(),
            "address": {
                "number": user_2.address.number,
                "street_name": user_2.address.street_name,
                "city": user_2.address.city,
                "postcode": user_2.address.postcode,
                "country": user_2.address.country,
            },
        },
    ]
