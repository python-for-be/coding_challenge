import logging
from datetime import date
from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.exceptions import UserNotFoundError
from src.models.address import Address
from src.models.user import User

logger = logging.getLogger(__name__)


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
        logger.info("Adding new user to database")
        user = User(**user_data)
        address = Address(**address_data)
        user.address = address
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        logger.info(f"User {user.id} added successfully")
        return user

    async def delete_user(self, user_id: int) -> None:
        """Delete a user record by ID."""
        logger.info(f"Attempting to delete user with ID: {user_id}")
        stmt = delete(User).where(User.id == user_id).returning(User.id)
        result = await self.session.execute(stmt)

        deleted_id = result.scalar_one_or_none()
        if deleted_id is None:
            raise UserNotFoundError("User not found.")
        logger.info(f"User with ID {user_id} deleted successfully")

    async def update_user(
        self, user_id: int, user_data: dict[str, date | str | int], address_data: dict[str, str | int]
    ) -> User:
        """Update a user and their address.

        Args:
            user_id (int): Unique identifier of the user to update.
            user_data (dict[str, Any]): User data to update.
            address_data (dict[str, Any]): Address data to update.
        """
        logger.info(f"Attempting to update user with ID: {user_id}")
        stmt = select(User).where(User.id == user_id).options(selectinload(User.address))
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            logger.warning(f"User with ID {user_id} not found for update")
            raise UserNotFoundError(f"User with id {user_id} not found")

        for key, value in user_data.items():
            setattr(user, key, value)

        if user.address:
            for key, value in address_data.items():
                setattr(user.address, key, value)
        else:
            user.address = Address(**address_data)

        await self.session.commit()
        await self.session.refresh(user)
        logger.info(f"User with ID {user.id} updated successfully")
        return user
