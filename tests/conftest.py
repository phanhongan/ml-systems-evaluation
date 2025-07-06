"""Pytest configuration and common fixtures for ML Systems Evaluation Framework tests"""

import pytest
import tempfile
import os
import yaml
from datetime import datetime, timedelta
from typing import Dict, Any, List

from ml_eval.core.types import SystemType, CriticalityLevel, ComplianceStandard
from ml_eval.core.config import SLOConfig, ErrorBudget, MetricData


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
                "window": "30d",
                "error_budget": 0.05,
                "description": "Model accuracy SLO",
            },
            "latency": {
                "target": 0.99,
                "window": "1h",
                "error_budget": 0.01,
                "description": "Response time SLO",
            },
        },
    }


@pytest.fixture
def safety_critical_config():
    """Configuration for safety-critical system testing"""
    return {
        "system": {
            "name": "safety_system",
            "type": "single_model",
            "criticality": "safety_critical",
        },
        "slos": {
            "safety_decision": {
                "target": 0.999,
                "window": "1h",
                "error_budget": 0.001,
                "description": "Safety-critical decision accuracy",
                "safety_critical": True,
                "compliance_standard": "DO-178C",
            }
        },
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
                "error_budget": 0.02,
                "description": "Quality control defect detection",
                "business_impact": "millions_per_hour",
            },
            "prediction_latency": {
                "target": 0.99,
                "window": "1h",
                "error_budget": 0.01,
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
def temp_config_file():
    """Create a temporary configuration file"""

    def _create_temp_config(config: Dict[str, Any]):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config, f)
            return f.name

    return _create_temp_config


@pytest.fixture
def mock_collector():
    """Mock collector for testing"""

    class MockCollector:
        def __init__(self, config: Dict[str, Any]):
            self.config = config
            self.name = config.get("name", "MockCollector")

        def collect(self) -> Dict[str, List[MetricData]]:
            now = datetime.now()
            return {
                "mock_metric": [
                    MetricData(timestamp=now, value=0.95, metadata={"source": "mock"})
                ]
            }

        def health_check(self) -> bool:
            return True

        def validate_config(self) -> bool:
            return True

    return MockCollector


@pytest.fixture
def mock_evaluator():
    """Mock evaluator for testing"""

    class MockEvaluator:
        def __init__(self, config: Dict[str, Any]):
            self.config = config

        def evaluate(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
            return {
                "slo_compliance": {"accuracy": True, "latency": True},
                "error_budgets": {},
                "incidents": [],
                "recommendations": ["Mock recommendation"],
            }

        def get_required_metrics(self) -> List[str]:
            return ["mock_metric"]

        def validate_metrics(self, metrics: Dict[str, Any]) -> bool:
            return True

    return MockEvaluator


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
def evaluation_result():
    """Sample evaluation result for testing"""
    from ml_eval.core.config import EvaluationResult

    return EvaluationResult(
        system_name="test_system",
        evaluation_time=datetime.now(),
        slo_compliance={"accuracy": True, "latency": True},
        error_budgets={},
        incidents=[],
        recommendations=["Test recommendation"],
        safety_violations=[],
        regulatory_violations=[],
        environmental_alerts=[],
        business_impact_assessment={},
    )


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
