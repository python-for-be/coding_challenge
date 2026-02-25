from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.core.exceptions import DateFormatError


async def date_format_exception_handler(request: Request, exc: Any) -> JSONResponse:
    """JSON response for date format errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": [{"msg": exc.message, "type": "date_format_error"}]},
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """Register all custom exception handlers to the FastAPI app."""
    app.add_exception_handler(DateFormatError, date_format_exception_handler)
