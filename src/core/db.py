from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings

engine = create_async_engine(settings.database_url, future=True, echo=False)

async_session_maker = async_sessionmaker(engine, expire_on_commit=True, class_=AsyncSession)


class Base(DeclarativeBase):
    """Base class for table models."""

    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async session with automatic commit/rollback."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
