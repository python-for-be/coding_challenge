import logging
from contextlib import asynccontextmanager, _AsyncGeneratorContextManager
from typing import AsyncIterator, Callable, Any

from fastapi import FastAPI


def setup_lifespan() -> Callable[..., _AsyncGeneratorContextManager[Any, None]]:
    """Return a lifespan context manager for the app.

    Keep resource setup/teardown here (e.g., warming caches, starting schedulers,
    opening/closing connections, etc.).
    """

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        """Context manager for lifespan events.

        Args:
            app (FastAPI): The FastAPI application instance.

        Returns: None
        """
        # Startup: initialize resources
        lifespan_logger = logging.getLogger(__name__)
        lifespan_logger.info("Application starting up...")

        yield

        # Shutdown: dispose resources
        lifespan_logger.info("Application shutting down...")

    return lifespan
