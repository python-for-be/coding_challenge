from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_async_session
from src.repositories.users import UserRepository
from src.schemas.users import UsersResponse
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
