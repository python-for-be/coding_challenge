from fastapi import APIRouter, Request

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def ping_health(request: Request) -> dict[str, str]:
    """Check the server is up and running.

    Returns:
        dict[str, str]: Health check response with status and version.
    """
    return {"status": "OK", "version": request.app.version}
