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

# Install UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    ln -s /root/.cargo/bin/uv /usr/local/bin/uv

# Copy only dependency files first for better caching
COPY pyproject.toml ./
COPY uv.lock ./
COPY README.md ./

# Install dependencies (cached unless dependencies change)
RUN uv sync --frozen

# Now copy the source code
COPY ml_eval ./ml_eval

# Install the package (now that code is present)
RUN uv sync --frozen

# Expose a volume for configs and results
VOLUME ["/app/config", "/app/results"]

# Set default entrypoint to the CLI
ENTRYPOINT ["ml-eval"]
CMD ["--help"]
