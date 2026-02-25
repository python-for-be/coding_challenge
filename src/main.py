from fastapi import FastAPI

from src.routes import health, users

app = FastAPI(
    contact={"name": "admin", "email": "admin@coding-challenge.com"},
    docs_url="/",
    summary="User Management API",
    title="Coding Challenge",
    version="0.0.1",
)

app.include_router(health.router)
app.include_router(users.router)
