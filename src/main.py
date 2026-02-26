from fastapi import FastAPI

from src.core.middleware import setup_middleware
from src.core.app_logging import setup_logging
from src.core.exception_handlers import setup_exception_handlers
from src.core.lifespan import setup_lifespan
from src.routes import health, users

setup_logging(log_level="INFO", log_file=None)

app = FastAPI(
    contact={"name": "admin", "email": "admin@coding-challenge.com"},
    docs_url="/",
    lifespan=setup_lifespan(),
    summary="User Management API",
    title="Coding Challenge",
    version="0.0.1",
)

setup_middleware(app=app)
setup_exception_handlers(app)

app.include_router(health.router)
app.include_router(users.router)
