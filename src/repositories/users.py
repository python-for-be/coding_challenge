from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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
