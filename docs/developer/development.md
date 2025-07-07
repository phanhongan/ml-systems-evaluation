# 🛠️ Development Guide

This guide provides comprehensive information for developers contributing to the ML Systems Evaluation Framework, including code quality standards, testing practices, and development workflows.

## 🔧 Development Environment Setup

### 🔧 Prerequisites

- 🐍 Python 3.11 or higher
- 📦 Poetry package manager
- 📥 Git for version control

### 🚀 Initial Setup

```bash
# Clone the repository
git clone <repository-url>
cd ml-systems-evaluation

# Install dependencies including development tools
poetry install

# Activate the virtual environment
poetry shell
```

## 🔧 Code Quality Tools

The project uses several tools to maintain code quality and consistency:

### 1. ⚫ Black - Code Formatting

[Black](https://black.readthedocs.io/) is an opinionated code formatter that automatically formats Python code to a consistent style.

#### ⚙️ Configuration

Black is configured in [`pyproject.toml`](../../pyproject.toml). See the `[tool.black]` section for the current configuration.

#### 💻 Usage

```bash
# Format all Python files
poetry run black .

# Check formatting without making changes
poetry run black --check .

# Format specific files
poetry run black ml_eval/core/ tests/
```

#### 🔗 Pre-commit Hook

To automatically format code before commits, install the pre-commit hook:

```bash
# Install pre-commit
poetry run pre-commit install

# Run pre-commit on all files
poetry run pre-commit run --all-files
```

### 2. 🦊 Ruff - Linting, Type Checking, and Import Sorting

[Ruff](https://docs.astral.sh/ruff/) is a fast Python linter, type checker, and import sorter that replaces flake8, mypy, and isort.

#### ⚙️ Configuration

Ruff is configured in [`pyproject.toml`](../../pyproject.toml). See the `[tool.ruff]` section for the current configuration.

#### 💻 Usage

```bash
# Lint, type check, and sort imports in all Python files
poetry run ruff check .

# Auto-fix issues
poetry run ruff check --fix .

# Format code (like black)
poetry run ruff format .

# Check only imports
poetry run ruff check --select I .
```

#### 🔗 Pre-commit Hook

To automatically run ruff before commits, add ruff to your pre-commit config:

```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.0.292
  hooks:
    - id: ruff
    - id: ruff-format
```

## 🔄 Development Workflow

### 1. 🔧 Code Quality Checks

Before committing code, run all quality checks:

```bash
# Format code
poetry run black .

# Lint, type check, and sort imports
poetry run ruff check .

# Format code with ruff
poetry run ruff format .

# Run tests
poetry run pytest
```

### 2. Automated Quality Checks

The project includes a script to run all quality checks:

```bash
# Run all quality checks
poetry run black --check .
poetry run ruff check .
poetry run ruff format --check .
poetry run pytest
```

### 3. Pre-commit Hooks

Install pre-commit hooks to automatically run quality checks:

```bash
# Install pre-commit
poetry run pre-commit install

# Run all hooks
poetry run pre-commit run --all-files
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=ml_eval --cov-report=html --cov-report=term

# Run specific test categories
poetry run pytest tests/test_core.py
poetry run pytest tests/test_collectors.py
poetry run pytest tests/test_evaluators.py

# Run tests with verbose output
poetry run pytest -v

# Run tests in parallel
poetry run pytest -n auto
```

### Test Categories

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows
- **Performance Tests**: Test system performance under load
- **Safety Tests**: Test safety-critical functionality

### Writing Tests

Follow these guidelines when writing tests:

1. **Test Structure**: Use descriptive test names and organize tests logically
2. **Fixtures**: Use pytest fixtures for common setup
3. **Mocking**: Mock external dependencies appropriately
4. **Coverage**: Aim for high test coverage, especially for critical paths
5. **Documentation**: Document complex test scenarios

See [`tests/test_core.py`](../../tests/test_core.py) for real test examples showing the actual testing patterns used in this project.

## 📋 Continuous Integration

The project uses GitHub Actions for continuous integration. The workflow runs:

1. **Code Quality Checks**: Black, Ruff
2. **Tests**: Unit, integration, and end-to-end tests
3. **Build**: Package building and validation
4. **Coverage**: Test coverage reporting

### Local CI Simulation

Run the same checks locally that CI runs. See [`.github/workflows/test.yml`](../../.github/workflows/test.yml) for the exact CI configuration:

```bash
# Install all dependencies
poetry install

# Run quality checks
poetry run black --check .
poetry run ruff check .
poetry run ruff format --check .

# Run tests
poetry run pytest --cov=ml_eval --cov-report=xml

# Build package
poetry build
```

## 📝 Code Style Guidelines

Code style is automatically enforced by Black and Ruff. See [`pyproject.toml`](../../pyproject.toml) for configuration details.

For examples of the project's coding patterns, see:
- [`ml_eval/collectors/`](../../ml_eval/collectors/) for collector implementations
- [`tests/test_core.py`](../../tests/test_core.py) for testing patterns

## 🛡️ Debugging

### Debugging Tools

1. **pdb**: Python debugger for interactive debugging
2. **pytest --pdb**: Drop into debugger on test failures
3. **logging**: Use structured logging for debugging
4. **print statements**: For quick debugging (remove before committing)

### Common Debugging Scenarios

1. **Type Errors**: Use ruff to catch type-related issues
2. **Import Errors**: Use ruff to organize imports
3. **Style Issues**: Use ruff for consistent formatting
4. **Test Failures**: Use pytest with verbose output for detailed error information

## 🛡️ Security Considerations

Follow standard Python security best practices. If handling sensitive data or authentication, consult a project maintainer for guidance.

## 📋 Contributing

### Pull Request Process

1. **Fork**: Fork the repository
2. **Branch**: Create a feature branch
3. **Develop**: Make your changes
4. **Test**: Run all tests and quality checks
5. **Commit**: Commit with descriptive messages
6. **Push**: Push to your fork
7. **PR**: Create a pull request

### Commit Messages

Use [conventional commit messages](https://www.conventionalcommits.org/) for all commits. See the full specification for more details.
