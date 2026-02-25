from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def ping_health():
    """Check the server is up and running.

    Returns:
         dict[str, str]: Health check response with status and version.
    """
    return {"status": "OK", "version": "0.0.1"}
