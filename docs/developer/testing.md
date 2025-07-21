# 🧪 Testing Guide

This guide provides practical testing information for the ML Systems Evaluation Framework.

## 🏗️ Testing Strategy

The framework follows a multi-layered testing approach:

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

### Test Commands
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=ml_eval --cov-report=html --cov-report=term

# Run specific test files
uv run pytest tests/test_core.py
uv run pytest tests/test_collectors.py
uv run pytest tests/test_evaluators.py

# Run with verbose output
uv run pytest -v
```

### Test Structure
- **Unit Tests**: `tests/test_*.py`
- **Integration Tests**: `tests/test_integration.py`
- **Industry Tests**: `tests/industry/`

## 🔧 Testing Custom Components

When creating custom components, follow the patterns shown in existing test files:

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
make ci-check
```

## 📋 Testing Standards

### Test Guidelines
- Write descriptive test names
- Use pytest fixtures for common setup
- Mock external dependencies appropriately
- Aim for high test coverage
- Document complex test scenarios

### Test Examples
See these files for real examples:
- [`tests/test_core.py`](../../tests/test_core.py) - Core framework tests
- [`tests/test_collectors.py`](../../tests/test_collectors.py) - Data collector tests
- [`tests/test_evaluators.py`](../../tests/test_evaluators.py) - Evaluation engine tests
