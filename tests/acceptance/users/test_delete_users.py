from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from tests.factories import UserFactory


async def test_delete_user_success(async_test_client: AsyncClient, db_session: AsyncSession):
    """Verify deleting a user through the API."""
    # First, create a user to delete using polyfactory
    user = await UserFactory.create_async()
    user_id = user.id

    # Delete the user
    delete_response = await async_test_client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 204

    # Verify user is gone from DB
    stmt = select(User).where(User.id == user_id)
    result = await db_session.execute(stmt)
    assert result.scalar_one_or_none() is None


async def test_delete_user_no_record_found_error(async_test_client: AsyncClient) -> None:
    """Verify a user record can be deleted.

    Args:
        async_test_client (AsyncClient): Test client

    Returns: None
    """
    response = await async_test_client.delete("/users/15")
    assert response.status_code == 404
    assert response.json() == {"detail": [{"msg": "User not found.", "type": "user_not_found_error"}]}
