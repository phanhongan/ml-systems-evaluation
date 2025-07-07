# 🧪 Testing Guide

This guide provides practical testing information for the ML Systems Evaluation Framework.

## 🏗️ Testing Strategy

The framework follows a multi-layered testing approach to ensure reliability and correctness:

```
                    E2E Tests
                ┌─────────────┐
                │  (Few)      │
                │ Complete    │
                │ Workflows   │
                └─────────────┘
            Integration Tests
        ┌─────────────────────┐
        │     (Some)          │
        │ Component           │
        │ Interactions        │
        └─────────────────────┘
            Unit Tests
    ┌─────────────────────────────┐
    │         (Many)              │
    │ Individual                  │
    │ Components                  │
    └─────────────────────────────┘
```

- **Unit Tests**: Test individual collectors, evaluators, reports
- **Integration Tests**: Test component interactions and data flow  
- **E2E Tests**: Test complete evaluation workflows with real configurations

## 🚀 Running Tests

### Basic Test Execution

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=ml_eval --cov-report=html --cov-report=term

# Run specific test files
poetry run pytest tests/test_core.py
poetry run pytest tests/test_collectors.py
poetry run pytest tests/test_evaluators.py

# Run with verbose output
poetry run pytest -v
```

### Test Configuration

See [`pytest.ini`](../../pytest.ini) for test configuration and [`tests/conftest.py`](../../tests/conftest.py) for shared test fixtures.

## 🏗️ Test Structure

### Unit Tests

See these test files for examples:
- [`tests/test_core.py`](../../tests/test_core.py) - Core framework tests
- [`tests/test_collectors.py`](../../tests/test_collectors.py) - Data collector tests
- [`tests/test_evaluators.py`](../../tests/test_evaluators.py) - Evaluation engine tests
- [`tests/test_reports.py`](../../tests/test_reports.py) - Report generation tests

### Integration Tests

See [`tests/test_integration.py`](../../tests/test_integration.py) for complete workflow testing.

## 🔧 Testing Custom Components

When creating custom components, follow the patterns shown in the existing test files:

```python
# Example test for custom collector
import pytest
from ml_eval.collectors.base import BaseCollector

class TestCustomCollector:
    def test_collector_creation(self):
        config = {"name": "test_collector"}
        collector = CustomCollector(config)
        assert collector.name == "test_collector"
    
    def test_collect_method(self):
        collector = CustomCollector({"name": "test"})
        result = collector.collect()
        assert isinstance(result, dict)
```

## 🤖 CI/CD Testing

The project uses GitHub Actions for automated testing. See [`.github/workflows/test.yml`](../../.github/workflows/test.yml) for the CI configuration.

### Local CI Simulation

```bash
# Run the same checks as CI
poetry run black --check .
poetry run ruff check .
poetry run pytest --cov=ml_eval --cov-report=xml
poetry build
```

## 📊 Test Coverage

The framework maintains high test coverage across all components. Run coverage reports to identify areas needing additional tests:

```bash
poetry run pytest --cov=ml_eval --cov-report=html
```

This will generate an HTML coverage report showing which code is tested and which areas need more test coverage.
