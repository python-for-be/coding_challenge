from typing import AsyncGenerator, Generator
import asyncio

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine

from src.core.db import get_async_session
from src.main import app
from src.core.db import Base
from src.core.config import settings
from tests.factories import UserFactory, AddressFactory


@pytest.fixture(scope="session", autouse=True)
def override_test_env(monkeypatch_session: pytest.MonkeyPatch) -> None:
    """Overwrites database environment variables for the test session."""
    import os
    from src.core.config import get_settings

    # Here we explicitly override them with TEST_ values if they exist.
    if os.getenv("TEST_DB_HOST"):
        monkeypatch_session.setenv("DB_HOST", os.getenv("TEST_DB_HOST", "localhost"))
        monkeypatch_session.setenv("DB_PORT", os.getenv("TEST_DB_PORT", "5433"))
        monkeypatch_session.setenv("DB_NAME", os.getenv("TEST_DB_NAME", "postgres"))
        monkeypatch_session.setenv("POSTGRES_USER", os.getenv("TEST_POSTGRES_USER", "postgres"))
        monkeypatch_session.setenv("POSTGRES_PASSWORD", os.getenv("TEST_POSTGRES_PASSWORD", "postgres"))

    # Clear the lru_cache to ensure settings are re-loaded with the new env vars
    get_settings.cache_clear()


@pytest.fixture(scope="session")
def monkeypatch_session() -> Generator[pytest.MonkeyPatch, None, None]:
    """Provides a session-scoped monkeypatch fixture."""
    m = pytest.MonkeyPatch()
    yield m
    m.undo()


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    """Creates a global SQLAlchemy asynchronous engine."""
    engine = create_async_engine(settings.database_url, future=True, echo=False)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Creates a global SQLAlchemy session factory."""
    return async_sessionmaker(engine, expire_on_commit=True, class_=AsyncSession)


@pytest.fixture(scope="session", autouse=True)
async def setup_database(engine: AsyncEngine) -> AsyncGenerator[None, None]:
    """Initializes the database schema before the test session starts."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(
    engine: AsyncEngine, session_maker: async_sessionmaker[AsyncSession]
) -> AsyncGenerator[AsyncSession, None]:
    """Provides a transactional database session for an individual test."""
    async with engine.connect() as connection:
        # Start a transaction for the connection
        transaction = await connection.begin()
        # Bind the session to the connection
        async with session_maker(bind=connection) as session:
            UserFactory.__async_session__ = session
            AddressFactory.__async_session__ = session

            yield session
            # Roll back everything, including any commits made during the test
            await transaction.rollback()


@pytest.fixture
async def async_test_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Provides an asynchronous HTTP client for testing API endpoints."""

    async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
