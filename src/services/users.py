from typing import List, Any

from src.repositories.users import UserRepository
from src.schemas.users import UsersResponse, UserCreateSchema


class UserService:
    """Service for user-related business logic."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_all_users(self) -> List[dict[str, Any]]:
        """Retrieve all users."""
        users = await self.repository.list_users()
        return [UsersResponse.model_validate(user).model_dump() for user in users]

    async def create_user(self, user_in: UserCreateSchema) -> dict[str, Any]:
        """Create a new user.

        Args:
            user_in (UserCreateSchema): User object to create.
        """
        user_data = user_in.model_dump()
        address_data = user_data.pop("address")
        user = await self.repository.create_user(user_data, address_data)
        return UsersResponse.model_validate(user).model_dump()
