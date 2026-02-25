from typing import List, Any

from src.repositories.users import UserRepository
from src.schemas.users import UsersResponse


class UserService:
    """Service for user-related business logic."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_all_users(self) -> List[dict[str, Any]]:
        """Retrieve all users."""
        users = await self.repository.list_users()
        return [UsersResponse.model_validate(user).model_dump() for user in users]
