from fastapi import FastAPI

from src.core.exception_handlers import setup_exception_handlers
from src.routes import health, users

app = FastAPI(
    contact={"name": "admin", "email": "admin@coding-challenge.com"},
    docs_url="/",
    summary="User Management API",
    title="Coding Challenge",
    version="0.0.1",
)

setup_exception_handlers(app)

app.include_router(health.router)
app.include_router(users.router)
