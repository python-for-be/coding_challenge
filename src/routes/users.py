from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_async_session
from src.repositories.users import UserRepository
from src.schemas.users import UsersResponse, UserCreateSchema, UserUpdateSchema
from src.services.users import UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    """Dependency for UserService."""
    repository = UserRepository(session)
    return UserService(repository)


@router.get("", response_model=List[UsersResponse])
async def list_users(service: UserService = Depends(get_user_service)) -> List[dict[str, Any]]:
    """List all users."""
    return await service.get_all_users()


@router.post("", response_model=UsersResponse, status_code=201)
async def create_user(user_in: UserCreateSchema, service: UserService = Depends(get_user_service)) -> dict[str, Any]:
    """Create a new user."""
    return await service.create_user(user_in)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, service: UserService = Depends(get_user_service)) -> None:
    """Delete a user record.

    Args:
        user_id (int): ID of the user to delete.

    Returns:
        dict[str, str]: Success message.
    """
    return await service.delete_user(user_id)


@router.put("/{user_id}", response_model=UsersResponse)
async def update_user(
    user_id: int, user_in: UserUpdateSchema, service: UserService = Depends(get_user_service)
) -> dict[str, Any]:
    """Update a user."""
    return await service.update_user(user_id, user_in)
