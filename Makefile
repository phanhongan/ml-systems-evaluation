# ML Systems Evaluation Framework - Development Makefile

.PHONY: help install install-dev install-docs test test-verbose test-coverage lint format check clean build docker-build docker-run docs docs-sphinx dev-setup ci-check full-setup quick-test quick-lint quick-format

# Default target
help:
	@echo "ML Systems Evaluation Framework - Development Commands"
	@echo ""
	@echo "Installation:"
	@echo "  install      Install production dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo "  install-docs Install documentation dependencies"
	@echo "  full-setup   Install dev + docs dependencies (recommended)"
	@echo ""
	@echo "Development:"
	@echo "  test         Run tests"
	@echo "  test-verbose Run tests with verbose output"
	@echo "  test-coverage Run tests with coverage"
	@echo "  lint         Run linting checks"
	@echo "  format       Format code"
	@echo "  check        Run all quality checks (lint + format)"
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
	@echo "  docs-sphinx  Build Sphinx documentation (if configured)"
	@echo ""

# Installation
install:
	uv sync --frozen

install-dev:
	uv sync --extra dev --frozen

install-docs:
	uv sync --extra docs --frozen

# Testing
test:
	uv run pytest

test-verbose:
	uv run pytest -v

test-coverage:
	uv run pytest --cov=ml_eval --cov-report=html --cov-report=term

# Code Quality
lint:
	uv run ruff check .

format:
	uv run ruff format .

check: lint format

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
	@echo "Documentation is in Markdown format in the docs/ directory"
	@echo "Available documentation:"
	@echo "  - docs/README.md - Main documentation"
	@echo "  - docs/developer/ - Development guides"
	@echo "  - docs/user-guides/ - User guides"
	@echo "  - docs/reference/ - Reference documentation"
	@echo "  - docs/industries/ - Industry-specific guides"
	@echo ""
	@echo "To build Sphinx documentation (if configured):"
	@echo "  make docs-sphinx"

# Development workflow
dev-setup: install-dev
	@echo "Development environment setup complete!"

ci-check: check test-coverage build
	@echo "All CI checks passed!"

full-setup:
	uv sync --extra dev --extra docs --frozen
	@echo "Full development environment setup complete!"

# Quick development commands
quick-test:
	uv run pytest -x

quick-lint:
	uv run ruff check --fix .

quick-format:
	uv run ruff format --fix .

# Sphinx documentation (if configured)
docs-sphinx: install-docs
	@echo "Checking for Sphinx configuration..."
	@if [ ! -f docs/conf.py ]; then \
		echo "Error: Sphinx configuration not found."; \
		echo "This project uses Markdown documentation in the docs/ directory."; \
		echo "To set up Sphinx documentation, create docs/conf.py first."; \
		exit 1; \
	fi
	uv run sphinx-build -b html docs/ docs/_build/html
