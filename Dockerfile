# syntax=docker/dockerfile:1
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt update && \
    apt install -y --no-install-recommends build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy only dependency files first for better caching
COPY pyproject.toml ./
COPY poetry.lock ./
COPY README.md ./

# Install dependencies (cached unless dependencies change)
RUN poetry install --no-root --only main,dev,docs

# Now copy the source code
COPY ml_eval ./ml_eval

# Install the package (now that code is present)
RUN poetry install --only main,dev,docs

# Expose a volume for configs and results
VOLUME ["/app/config", "/app/results"]

# Set default entrypoint to the CLI
ENTRYPOINT ["ml-eval"]
CMD ["--help"]
