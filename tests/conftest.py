"""Test configuration and fixtures for ML Systems Evaluation Framework"""

import tempfile
from datetime import datetime, timedelta
from typing import Any

import pytest
import yaml

from ml_eval.core.config import (
    ErrorBudget,
    MetricData,
    SLOConfig,
)


@pytest.fixture
def sample_config():
    """Sample configuration for testing"""
    return {
        "system": {
            "name": "test_system",
            "type": "single_model",
            "criticality": "operational",
        },
        "slos": {
            "accuracy": {
                "target": 0.95,
                "window": "24h",
                "description": "Model accuracy",
            },
            "latency": {
                "target": 0.99,
                "window": "1h",
                "description": "Response latency",
            },
        },
        "collectors": [
            {
                "type": "online",
                "endpoints": ["http://localhost:8080/metrics"],
                "metrics": ["accuracy", "latency"],
            }
        ],
        "evaluators": [
            {
                "type": "reliability",
                "slos": {
                    "accuracy": {"target": 0.95, "window": "24h"},
                    "latency": {"target": 0.99, "window": "1h"},
                },
            }
        ],
    }


@pytest.fixture
def safety_critical_config():
    """Safety-critical configuration for testing"""
    return {
        "system": {
            "name": "safety_system",
            "type": "safety_critical",
            "criticality": "safety_critical",
        },
        "slos": {
            "safety_margin": {
                "target": 0.999,
                "window": "24h",
                "description": "Safety margin",
                "safety_critical": True,
            },
            "failure_probability": {
                "target": 0.001,
                "window": "24h",
                "description": "Failure probability",
                "safety_critical": True,
            },
        },
        "collectors": [
            {
                "type": "online",
                "endpoints": ["http://localhost:8080/metrics"],
                "metrics": ["safety_margin", "failure_probability"],
            }
        ],
        "evaluators": [
            {
                "type": "safety",
                "compliance_standards": ["DO-178C"],
                "safety_thresholds": {"safety_margin": 0.999},
            }
        ],
    }


@pytest.fixture
def manufacturing_config():
    """Configuration for manufacturing industry testing"""
    return {
        "system": {
            "name": "quality_control_system",
            "type": "workflow",
            "criticality": "business_critical",
        },
        "slos": {
            "defect_detection": {
                "target": 0.98,
                "window": "24h",
                "description": "Quality control defect detection",
                "business_impact": "millions_per_hour",
            },
            "prediction_latency": {
                "target": 0.99,
                "window": "1h",
                "description": "Real-time prediction latency",
            },
        },
    }


@pytest.fixture
def aviation_config():
    """Configuration for aviation industry testing"""
    return {
        "system": {
            "name": "flight_control_system",
            "type": "single_model",
            "criticality": "safety_critical",
        },
        "slos": {
            "flight_safety": {
                "target": 0.9999,
                "window": "1h",
                "error_budget": 0.0001,
                "description": "Flight safety decision accuracy",
                "safety_critical": True,
                "compliance_standard": "DO-178C",
                "environmental_conditions": ["high_altitude", "turbulence"],
            }
        },
    }


@pytest.fixture
def sample_metrics():
    """Sample metric data for testing"""
    now = datetime.now()
    return {
        "accuracy": [
            MetricData(
                timestamp=now - timedelta(minutes=5),
                value=0.96,
                metadata={"model_version": "v1.0"},
            ),
            MetricData(
                timestamp=now - timedelta(minutes=4),
                value=0.94,
                metadata={"model_version": "v1.0"},
            ),
            MetricData(
                timestamp=now - timedelta(minutes=3),
                value=0.97,
                metadata={"model_version": "v1.0"},
            ),
        ],
        "latency": [
            MetricData(
                timestamp=now - timedelta(minutes=5),
                value=0.15,
                metadata={"endpoint": "/predict"},
            ),
            MetricData(
                timestamp=now - timedelta(minutes=4),
                value=0.12,
                metadata={"endpoint": "/predict"},
            ),
            MetricData(
                timestamp=now - timedelta(minutes=3),
                value=0.18,
                metadata={"endpoint": "/predict"},
            ),
        ],
    }


@pytest.fixture
def sample_slos():
    """Sample SLO configurations for testing"""
    return [
        SLOConfig(
            name="accuracy",
            target=0.95,
            window="30d",
            error_budget=0.05,
            description="Model accuracy SLO",
        ),
        SLOConfig(
            name="latency",
            target=0.99,
            window="1h",
            error_budget=0.01,
            description="Response time SLO",
        ),
    ]


@pytest.fixture
def safety_slos():
    """Safety-critical SLO configurations for testing"""
    return [
        SLOConfig(
            name="safety_decision",
            target=0.999,
            window="1h",
            error_budget=0.001,
            description="Safety-critical decision accuracy",
            safety_critical=True,
            compliance_standard="DO-178C",
        )
    ]


@pytest.fixture
def error_budget():
    """Sample error budget for testing"""
    return ErrorBudget(
        slo_name="accuracy",
        budget_remaining=0.03,
        burn_rate=0.001,
        alerts=["Budget consumption rate is high"],
    )


@pytest.fixture
def temp_config_file():
    """Create a temporary configuration file"""

    def _create_temp_config(config: dict[str, Any]):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config, f)
            return f.name

    return _create_temp_config


@pytest.fixture
def mock_collector():
    """Mock collector for testing"""

    class MockCollector:
        def __init__(self, config: dict[str, Any]):
            self.config = config
            self.name = config.get("name", "MockCollector")

        def collect(self) -> dict[str, list[MetricData]]:
            now = datetime.now()
            return {"mock_metric": [MetricData(timestamp=now, value=1.0, metadata={})]}

        def health_check(self) -> bool:
            return True

        def validate_config(self) -> bool:
            return True

    return MockCollector


@pytest.fixture
def mock_evaluator():
    """Mock evaluator for testing"""

    class MockEvaluator:
        def __init__(self, config: dict[str, Any]):
            self.config = config

        def evaluate(self, _metrics: dict[str, Any]) -> dict[str, Any]:
            return {
                "slo_compliance": {"accuracy": True, "latency": True},
                "error_budgets": {},
                "incidents": [],
                "recommendations": ["Test recommendation"],
            }

        def get_required_metrics(self) -> list[str]:
            return ["mock_metric"]

        def validate_metrics(self, _metrics: dict[str, Any]) -> bool:
            return True

    return MockEvaluator


@pytest.fixture
def evaluation_result():
    """Sample evaluation result for testing"""
    return {
        "system_name": "test_system",
        "timestamp": datetime.now(),
        "overall_compliance": 0.95,
        "has_critical_violations": False,
        "requires_emergency_shutdown": False,
        "evaluator_results": {
            "PerformanceEvaluator": {
                "compliance_score": 0.95,
                "recommendations": ["Monitor performance trends"],
                "alerts": [],
            }
        },
        "recommendations": ["Monitor performance trends"],
        "alerts": [],
    }


@pytest.fixture
def sample_environmental_conditions():
    """Sample environmental conditions for testing"""
    return {
        "temperature": 25.0,
        "humidity": 60.0,
        "pressure": 1013.25,
        "altitude": 1000,
        "vibration": 0.1,
    }


@pytest.fixture
def sample_compliance_data():
    """Sample compliance data for testing"""
    return {
        "standard": "DO-178C",
        "level": "A",
        "certification_date": "2023-01-01",
        "expiry_date": "2025-01-01",
        "audit_status": "compliant",
    }
