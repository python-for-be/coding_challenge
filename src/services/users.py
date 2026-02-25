from typing import List, Any

from src.repositories.users import UserRepository
from src.schemas.users import UserCreateSchema, UsersResponse, UserUpdateSchema


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

    async def delete_user(self, user_id: int) -> None:
        """Delete a user by ID.

        Args:
            user_id (int): Unique identifier of the user to delete.
        """
        await self.repository.delete_user(user_id)

    async def update_user(self, user_id: int, user_in: UserUpdateSchema) -> dict[str, Any]:
        """Update an existing user.

        Args:
            user_id (int): Unique identifier of the user to update.
            user_in (UserUpdateSchema): User object to update.
        """
        user_data = user_in.model_dump()
        address_data = user_data.pop("address")
        user = await self.repository.update_user(user_id, user_data, address_data)
        return UsersResponse.model_validate(user).model_dump()
