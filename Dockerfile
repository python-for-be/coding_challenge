FROM python:3.13.2-slim-bullseye AS builder

# Set environment variables for Python and Poetry
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set working directory
WORKDIR /app

# Install Poetry and dependencies
RUN pip install --no-cache-dir "poetry==2.1.2"

# Copy poetry files to be used to create deterministic builds
COPY poetry.lock pyproject.toml ./

# Install dependencies only
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root

# Runtime stage
FROM python:3.13.2-slim-bullseye AS runtime

LABEL maintainer="your_email@domain.com"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1 \
VIRTUAL_ENV=/app/.venv \
PATH="/app/.venv/bin:$PATH"

# Install curl for healthcheck, create a non-root user
RUN apt-get update && apt-get install -y --no-install-recommends \
curl \
&& rm -rf /var/lib/apt/lists/* \
&& useradd --create-home appuser

# Set working directory
WORKDIR /app

# Copy the virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy source code and change ownership
COPY --chown=appuser:appuser src/ src/

# Switch to non-root user
USER appuser

EXPOSE 8000

# Healthcheck to ensure container is healthy
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]