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
uv run ruff format --check .
uv run ruff check .
uv run pytest --cov=ml_eval --cov-report=xml
uv build
```

## 📊 Test Coverage

The framework maintains high test coverage across all components. Run coverage reports to identify areas needing additional tests:

```bash
uv run pytest --cov=ml_eval --cov-report=html
```

This will generate an HTML coverage report showing which code is tested and which areas need more test coverage.

## 🤖 LLM Testing Strategy

The framework includes LLM-enabled evaluators that can make real API calls. For testing, we ensure LLM calls are disabled by default:

### **LLM-Disabled Testing (Default)**

All tests run with LLM disabled to avoid API costs and ensure deterministic results:

```python
# Test configuration with LLM disabled
llm_disabled_config = {
    "evaluators": [
        {
            "type": "interpretability",
            "use_llm": False,  # Explicitly disable LLM
        },
        {
            "type": "edge_case", 
            "use_llm": False,  # Explicitly disable LLM
        },
        {
            "type": "safety",
            "use_llm": False,  # Explicitly disable LLM
        },
    ],
}
```

### **Testing LLM-Enabled Evaluators**

```python
def test_interpretability_evaluator_llm_disabled(llm_disabled_config):
    """Test interpretability evaluator with LLM disabled"""
    from ml_eval.evaluators.interpretability import InterpretabilityEvaluator
    
    # Find evaluator config
    eval_config = None
    for evaluator in llm_disabled_config["evaluators"]:
        if evaluator["type"] == "interpretability":
            eval_config = evaluator
            break
    
    evaluator = InterpretabilityEvaluator(eval_config)
    assert evaluator.use_llm is False
    assert evaluator.llm_assistant is None
    
    # Test evaluation works without LLM
    metrics = {"perception_interpretability": 0.8}
    result = evaluator.evaluate(metrics)
    assert isinstance(result, dict)
    assert result["llm_enhanced"].get("enabled", False) is False
```

### **Fallback Behavior Testing**

LLM-enabled evaluators gracefully fall back to deterministic behavior when LLM is disabled:

```python
def test_evaluators_fallback_behavior(llm_disabled_config):
    """Test that evaluators fall back to deterministic behavior"""
    from ml_eval.evaluators.interpretability import InterpretabilityEvaluator
    from ml_eval.evaluators.edge_case import EdgeCaseEvaluator
    from ml_eval.evaluators.safety import SafetyEvaluator
    
    evaluators = [
        (InterpretabilityEvaluator, "interpretability"),
        (EdgeCaseEvaluator, "edge_case"), 
        (SafetyEvaluator, "safety"),
    ]
    
    for EvaluatorClass, eval_type in evaluators:
        evaluator = EvaluatorClass(eval_config)
        assert evaluator.use_llm is False
        assert evaluator.llm_assistant is None
        
        # Should work without LLM
        result = evaluator.evaluate({"test_metric": 0.8})
        assert isinstance(result, dict)
```

### **LLM Integration Testing (Optional)**

For testing LLM integration with mocked responses, use the `llm_enabled_config` fixture:

```python
def test_llm_integration_with_mock(llm_enabled_config):
    """Test LLM integration with mocked provider"""
    # This would require mocking the LLM provider
    # to avoid real API calls during testing
    pass
```

### **Key Testing Principles**

1. **✅ LLM Disabled by Default**: All tests run without real LLM calls
2. **✅ Deterministic Results**: Tests produce consistent, predictable outcomes  
3. **✅ Fallback Testing**: Verify evaluators work without LLM assistance
4. **✅ No API Costs**: Testing doesn't incur real API charges
5. **✅ Fast Execution**: Tests run quickly without network calls

### **Test Fixtures**

The framework provides test fixtures for LLM testing:

- **`llm_disabled_config`**: Configuration with LLM explicitly disabled
- **`llm_enabled_config`**: Configuration with LLM enabled (for integration testing)
- **LLM-specific test classes**: `TestLLMEnabledEvaluators` for comprehensive testing

This approach ensures comprehensive testing while avoiding real LLM API calls during development and CI/CD.
