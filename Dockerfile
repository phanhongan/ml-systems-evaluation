# syntax=docker/dockerfile:1
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt update && \
    apt install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
COPY requirements-test.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r requirements-test.txt

# Copy project
COPY ml_eval ./ml_eval
COPY setup.py ./

# Install the package in editable mode
RUN pip install -e .

# Expose a volume for configs and results
VOLUME ["/app/config", "/app/results"]

# Set default entrypoint to the CLI
ENTRYPOINT ["ml-eval"]
CMD ["--help"]
