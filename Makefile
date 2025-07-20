# ML Systems Evaluation Framework - Development Makefile

.PHONY: help install install-dev install-docs test test-verbose test-coverage lint format check clean build docker-build docker-run docs docs-sphinx dev-setup ci-check full-setup quick-test quick-lint quick-format api api-dev api-test

# Default target
help:
	@echo "ML Systems Evaluation Framework - Development Commands"
	@echo ""
	@echo "Installation:"
	@echo "  install      Install production dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo "  dev-setup    Install dev dependencies (recommended)"
	@echo ""
	@echo "Development:"
	@echo "  test         Run tests"
	@echo "  test-verbose Run tests with verbose output"
	@echo "  test-coverage Run tests with coverage"
	@echo "  lint         Run linting checks"
	@echo "  format       Format code"
	@echo "  check        Run all quality checks (lint + format)"
	@echo ""
	@echo "API:"
	@echo "  api          Start API server"
	@echo "  api-dev      Start API server in development mode"
	@echo "  api-test     Run API tests"
	@echo ""
	@echo "Build:"
	@echo "  build        Build the package"
	@echo "  clean        Clean build artifacts"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run   Run Docker container"
	@echo ""
	@echo "Documentation:"
	@echo "  docs         Show documentation info"
	@echo "  docs-sphinx  Build Sphinx documentation"
	@echo "  docs-sphinx-serve  Build and serve Sphinx documentation"
	@echo ""

# Installation
install:
	uv sync --frozen

install-dev:
	uv sync --extra dev --frozen

# Testing
test:
	uv run pytest

test-verbose:
	uv run pytest -v

test-coverage:
	uv run pytest --cov=ml_eval --cov-report=html --cov-report=term

# Code Quality
lint:
	uv run ruff check --fix .

format:
	uv run ruff format .

check: lint format

# API
api:
	uv run ml-eval-api

api-dev:
	uv run ml-eval-api --reload

api-test:
	uv run pytest tests/test_api.py -v

# Build
build:
	uv build

clean:
	rm -rf build/ dist/ *.egg-info/ htmlcov/ .coverage .pytest_cache/ .ruff_cache/

# Docker
docker-build:
	docker build -t ml-systems-evaluation .

docker-run:
	docker run -it --rm ml-systems-evaluation

# Documentation
docs:
	@echo "📚 Documentation"
	@echo "  Markdown: docs/README.md"
	@echo "  Sphinx: docs_sphinx/ (served on port 8080)"
	@echo "  API: ml_eval/api/README.md (served on port 8000)"

docs-sphinx:
	cd docs_sphinx && uv run make html

docs-sphinx-serve:
	cd docs_sphinx && uv run make html && cd build/html && python -m http.server 8080

# Development setup
dev-setup: install-dev
	@echo "✅ Development environment ready!"

# CI checks
ci-check: lint test

# Full setup for new developers
full-setup: dev-setup
	@echo "✅ Full development environment ready!"

# Quick commands for development
quick-test:
	uv run pytest -x

quick-lint:
	uv run ruff check .

quick-format:
	uv run ruff format .
