FROM python:3.13-slim-bullseye AS builder

LABEL maintainer="your_email@domain.com"

# Install package manager
RUN pip install "poetry==2.1.2"

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set working directory
WORKDIR /app

# Copy poetry files to be used to create deterministic builds
COPY poetry.lock pyproject.toml /app/

# Don't install the current project into the virtual environment or download cache
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root

# Small image to use for our runtime
FROM python:3.13-slim-bullseye AS runtime

# Only copy the virtual environment
ENV VIRTUAL_ENV=/app/.venv \
PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Create and switch to a new user
RUN useradd --create-home appuser

WORKDIR /home/appuser

USER appuser

COPY /src/ src

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]