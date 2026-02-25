from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.core.exceptions import DateFormatError, MinimumAgeError, UserNotFoundError


async def date_format_exception_handler(request: Request, exc: Any) -> JSONResponse:
    """JSON response for date format errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": [{"msg": exc.message, "type": "date_format_error"}]},
    )


async def minimum_age_exception_handler(request: Request, exc: Any) -> JSONResponse:
    """JSON response for minimum age errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": [{"msg": exc.message, "type": "minimum_age_error"}]},
    )


async def user_not_found_exception_handler(request: Request, exc: Any) -> JSONResponse:
    """JSON response for user not found errors."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": [{"msg": exc.message, "type": "user_not_found_error"}]},
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """Register all custom exception handlers to the FastAPI app."""
    app.add_exception_handler(DateFormatError, date_format_exception_handler)
    app.add_exception_handler(MinimumAgeError, minimum_age_exception_handler)
    app.add_exception_handler(UserNotFoundError, user_not_found_exception_handler)
