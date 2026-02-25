from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def ping_health():
    return {"status": "OK", "version": "0.0.1"}
