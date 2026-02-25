FROM python:3.13

LABEL maintainer="<your_email>@domain.com"

# Install package manager
RUN pip install "poetry==2.1.2"

# Set working directory
WORKDIR /app

# Copy poetry files to be used to create deterministic builds
COPY poetry.lock pyproject.toml /app/

RUN poetry install

COPY ./ ./

EXPOSE 8000

CMD ["poetry", "run", "python", "-m", "uvicorn", \
"src.main:app", "--host", "0.0.0.0", "--port", "8000"]