# 🛠️ Development Guide

This guide provides information for developers contributing to the ML Systems Evaluation Framework, including code quality standards, testing practices, and development workflows.

## 🔧 Development Environment Setup

### Prerequisites
- 🐍 Python 3.11 or higher
- 📥 Git for version control
- 📦 UV package manager

### Quick Setup
```bash
# Clone and setup
git clone <repository-url>
cd ml-systems-evaluation
uv sync --extra dev
uv shell
```

## 🔧 Code Quality & Workflow

The project uses Ruff for all code quality tasks. Use these commands for development:

### Code Quality Commands
```bash
# Quick development workflow
make check      # Format, lint, and test
make format     # Format code only
make lint       # Lint and type check
make test       # Run tests

# Manual commands
uv run ruff format .     # Format code
uv run ruff check .      # Lint and type check
uv run ruff check --fix . # Auto-fix issues
uv run pytest           # Run tests
```

### Pre-commit Setup
Add to your pre-commit config:
```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.0.292
  hooks:
    - id: ruff
    - id: ruff-format
```

## 🧪 Testing

### Test Commands
```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run specific tests
uv run pytest tests/test_core.py
uv run pytest tests/test_evaluators.py

# Run in parallel
uv run pytest -n auto
```

### Test Structure
- **Unit Tests**: `tests/test_*.py`
- **Integration Tests**: `tests/test_integration.py`
- **Industry Tests**: `tests/industry/`

## 📋 Development Standards

### Code Quality
- Use Ruff for formatting and linting
- Follow type hints throughout
- Write comprehensive tests
- Document public APIs

### Git Workflow
1. Create feature branch
2. Make changes with tests
3. Run quality checks
4. Submit pull request

### Documentation
- Keep docs in sync with code
- Use clear, concise language
- Include practical examples
- Follow established structure
