# 🛠️ Development Guide

This guide provides comprehensive information for developers contributing to the ML Systems Evaluation Framework, including code quality standards, testing practices, and development workflows.

## 🔧 Development Environment Setup

### 🔧 Prerequisites

- 🐍 Python 3.9 or higher
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

Black is configured in `pyproject.toml`:

```toml
[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

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

Ruff is configured in `pyproject.toml`:

```toml
[tool.ruff]
exclude = [ ... ]
line-length = 88
indent-width = 4
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM", "ARG", "PIE", "TCH", "Q", "RUF"]
ignore = ["E203", "E501"]
fixable = ["ALL"]
unfixable = []

[tool.ruff.lint.isort]
known-first-party = ["ml_eval"]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
```

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

Example test structure:

```python
import pytest
from ml_eval.core.framework import EvaluationFramework


class TestEvaluationFramework:
    """Test the main evaluation framework."""
    
    def test_framework_creation(self):
        """Test that framework can be created with valid config."""
        config = {"system": {"name": "test_system"}}
        framework = EvaluationFramework(config)
        assert framework.system_name == "test_system"
    
    def test_framework_with_invalid_config(self):
        """Test that framework handles invalid config gracefully."""
        with pytest.raises(ValueError):
            EvaluationFramework({})
    
    @pytest.mark.integration
    def test_complete_evaluation_workflow(self):
        """Test complete evaluation workflow."""
        # Test implementation
        pass
```

## 📋 Continuous Integration

The project uses GitHub Actions for continuous integration. The workflow runs:

1. **Code Quality Checks**: Black, Ruff
2. **Tests**: Unit, integration, and end-to-end tests
3. **Build**: Package building and validation
4. **Coverage**: Test coverage reporting

### Local CI Simulation

Run the same checks locally that CI runs:

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

### Python Style

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with these modifications:

- **Line Length**: 88 characters (Black default)
- **Import Order**: Use ruff for automatic sorting
- **Type Hints**: Use type hints for all function parameters and return values
- **Docstrings**: Use Google-style docstrings

### Naming Conventions

- **Classes**: PascalCase (e.g., `EvaluationFramework`)
- **Functions/Methods**: snake_case (e.g., `collect_metrics`)
- **Variables**: snake_case (e.g., `metric_data`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DEFAULT_TIMEOUT`)
- **Modules**: snake_case (e.g., `data_collector`)

### Documentation

- **Docstrings**: Document all public functions and classes
- **Type Hints**: Include type hints for all function signatures
- **Comments**: Add comments for complex logic
- **README**: Keep documentation up to date

Example:

```python
from typing import Dict, List, Optional

from .base import BaseCollector
from ..core.config import MetricData


class CustomCollector(BaseCollector):
    """Custom data collector for specific metrics.
    
    This collector implements custom logic for collecting metrics
    from specialized data sources.
    """
    
    def __init__(self, config: Dict[str, any]) -> None:
        """Initialize the custom collector.
        
        Args:
            config: Configuration dictionary containing collector settings.
            
        Raises:
            ValueError: If required configuration is missing.
        """
        super().__init__(config)
        self.endpoint = config.get("endpoint")
        if not self.endpoint:
            raise ValueError("endpoint is required in config")
    
    def collect(self) -> Dict[str, List[MetricData]]:
        """Collect metrics from the configured data source.
        
        Returns:
            Dictionary mapping metric names to lists of MetricData objects.
            
        Raises:
            ConnectionError: If unable to connect to data source.
        """
        # Implementation here
        pass
```

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

## 📊 Performance Considerations

### Code Performance

1. **Profiling**: Use cProfile for performance analysis
2. **Memory Usage**: Monitor memory usage in large data processing
3. **Async/Await**: Use async programming for I/O-bound operations
4. **Caching**: Implement caching for expensive operations

### Testing Performance

1. **Benchmarks**: Write benchmarks for performance-critical code
2. **Load Testing**: Test system performance under load
3. **Memory Testing**: Monitor memory usage during tests
4. **Profiling Tests**: Profile test execution for slow tests

## 🛡️ Security Considerations

### Code Security

1. **Input Validation**: Validate all inputs
2. **Authentication**: Implement proper authentication
3. **Authorization**: Check permissions appropriately
4. **Data Protection**: Handle sensitive data securely

### Security Testing

1. **Vulnerability Scanning**: Regular security scans
2. **Penetration Testing**: Test for security vulnerabilities
3. **Code Review**: Security-focused code reviews
4. **Dependency Updates**: Keep dependencies updated

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

Use conventional commit messages:

```