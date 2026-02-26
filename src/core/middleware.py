import logging
import time

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import RequestResponseEndpoint

logger = logging.getLogger(__name__)


def setup_middleware(app: FastAPI) -> None:
    """Register all middleware for the application in one place."""

    @app.middleware("http")
    async def log_processing_times(request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Logs each incoming HTTP request and its corresponding time taken to process the request.

        Args:
            request (Request): Incoming HTTP request to be processed.
            call_next (RequestResponseEndpoint): Function to call the next middleware
            or the endpoint handling the request.

        Returns:
            Response: The HTTP response returned after processing the request.

        """
        logger.info(f"Request: {request.method} {request.url}")
        start_time: float = time.perf_counter()

        response: Response = await call_next(request)

        process_time: float = time.perf_counter() - start_time
        logger.info(f"Response status: {response.status_code} - Time: {process_time:.2f}s")
        return response
