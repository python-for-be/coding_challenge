from datetime import date
from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.address import Address
from src.models.user import User


class UserRepository:
    """Repository for User model operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_users(self) -> Sequence[User]:
        """Get all users from the database."""
        stmt = select(User).options(selectinload(User.address))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_user(self, user_data: dict[str, date | str | int], address_data: dict[str, str | int]) -> User:
        """Create a new user with an address.

        Args:
            user_data (dict): User data to create.
            address_data (dict): Address data to create.
        """
        user = User(**user_data)
        address = Address(**address_data)
        user.address = address
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> None:
        """Delete a user by ID.

        Args:
            user_id (int): Unique identifier of the user to delete.
        """
        stmt = delete(User).where(User.id == user_id).returning(User.id)
        await self.session.execute(stmt)
