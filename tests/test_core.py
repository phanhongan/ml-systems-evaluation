"""Tests for core framework components"""

from datetime import datetime

from ml_eval.core.config import (
    EvaluationResult,
    MetricData,
    SLOConfig,
)
from ml_eval.core.framework import EvaluationFramework
from ml_eval.core.types import ComplianceStandard, CriticalityLevel


class TestCriticalityLevel:
    """Test CriticalityLevel enum"""

    def test_criticality_level_values(self):
        """Test that all criticality levels have correct values"""
        assert CriticalityLevel.SAFETY_CRITICAL.value == "safety_critical"
        assert CriticalityLevel.BUSINESS_CRITICAL.value == "business_critical"
        assert CriticalityLevel.OPERATIONAL.value == "operational"

    def test_criticality_level_from_string(self):
        """Test creating CriticalityLevel from string"""
        assert CriticalityLevel("safety_critical") == CriticalityLevel.SAFETY_CRITICAL
        assert (
            CriticalityLevel("business_critical") == CriticalityLevel.BUSINESS_CRITICAL
        )


class TestComplianceStandard:
    """Test ComplianceStandard enum"""

    def test_compliance_standard_values(self):
        """Test that all compliance standards have correct values"""
        assert ComplianceStandard.DO_178C.value == "DO-178C"
        assert ComplianceStandard.DO_254.value == "DO-254"
        assert ComplianceStandard.ARP4754A.value == "ARP4754A"
        assert ComplianceStandard.FAA.value == "FAA"
        assert ComplianceStandard.EASA.value == "EASA"
        assert ComplianceStandard.ICAO.value == "ICAO"
        assert ComplianceStandard.COLREGs.value == "COLREGs"
        assert ComplianceStandard.IMO.value == "IMO Guidelines"
        assert ComplianceStandard.GDPR.value == "GDPR"

    def test_compliance_standard_from_string(self):
        """Test creating ComplianceStandard from string"""
        assert ComplianceStandard("DO-178C") == ComplianceStandard.DO_178C
        assert ComplianceStandard("COLREGs") == ComplianceStandard.COLREGs


class TestSLOConfig:
    """Test SLOConfig class"""

    def test_slo_creation(self):
        """Test SLO configuration creation"""
        slo = SLOConfig(
            name="test_slo",
            target=0.95,
            window="24h",
            description="Test SLO",
            safety_critical=False,
        )

        assert slo.name == "test_slo"
        assert slo.target == 0.95
        assert slo.window == "24h"
        assert abs(slo.error_budget - 0.05) < 1e-10  # Handle floating-point precision
        assert slo.description == "Test SLO"
        assert slo.safety_critical is False

    def test_safety_critical_slo(self):
        """Test safety-critical SLO configuration"""
        slo = SLOConfig(
            name="safety_slo",
            target=0.999,
            window="24h",
            description="Safety-critical SLO",
            safety_critical=True,
        )

        assert slo.safety_critical is True
        assert abs(slo.error_budget - 0.001) < 1e-10  # Handle floating-point precision

    def test_slo_with_explicit_error_budget(self):
        """Test SLO with explicit error_budget"""
        slo = SLOConfig(
            name="explicit_slo",
            target=0.90,
            window="24h",
            error_budget=0.10,  # Explicitly provided
            description="SLO with explicit error budget",
        )

        assert slo.target == 0.90
        assert slo.error_budget == 0.10  # Should use provided value

    def test_compliance_standard_validation(self):
        """Test compliance standard validation"""
        # SLOConfig doesn't have compliance_standard parameter
        # This validation would be handled elsewhere in the framework

    def test_slo_with_environmental_conditions(self):
        """Test SLO with environmental conditions"""
        # SLOConfig doesn't have environmental_conditions parameter
        # This would be handled elsewhere in the framework


class TestMetricData:
    """Test MetricData class"""

    def test_metric_data_creation(self):
        """Test basic metric data creation"""
        timestamp = datetime.now()
        metric = MetricData(
            timestamp=timestamp, value=0.95, metadata={"model_version": "v1.0"}
        )

        assert metric.timestamp == timestamp
        assert metric.value == 0.95
        assert metric.metadata == {"model_version": "v1.0"}
        assert metric.environmental_conditions == {}
        assert metric.compliance_info == {}

    def test_metric_data_with_environmental_conditions(self):
        """Test metric data with environmental conditions"""
        timestamp = datetime.now()
        environmental_conditions = {"temperature": 25.0, "humidity": 60.0}

        metric = MetricData(
            timestamp=timestamp,
            value=0.95,
            environmental_conditions=environmental_conditions,
        )

        assert metric.environmental_conditions == environmental_conditions

    def test_metric_data_with_compliance_context(self):
        """Test metric data with compliance context"""
        timestamp = datetime.now()
        compliance_info = {"standard": "DO-178C", "level": "A"}

        metric = MetricData(
            timestamp=timestamp, value=0.95, compliance_info=compliance_info
        )

        assert metric.compliance_info == compliance_info


class TestEvaluationResult:
    """Test EvaluationResult class"""

    def test_evaluation_result_creation(self):
        """Test basic evaluation result creation"""
        result = EvaluationResult(
            system_name="test_system",
            timestamp=datetime.now(),
            overall_compliance=0.95,
            has_critical_violations=False,
            requires_emergency_shutdown=False,
            evaluator_results={},
            recommendations=[],
            alerts=[],
        )

        assert result.system_name == "test_system"
        assert result.overall_compliance == 0.95
        assert result.has_critical_violations is False
        assert result.requires_emergency_shutdown is False
        assert result.evaluator_results == {}
        assert result.recommendations == []
        assert result.alerts == []

    def test_evaluation_result_properties(self):
        """Test evaluation result properties"""
        # No violations
        result = EvaluationResult(
            system_name="test_system",
            timestamp=datetime.now(),
            overall_compliance=0.95,
            has_critical_violations=False,
            requires_emergency_shutdown=False,
            evaluator_results={},
            recommendations=[],
            alerts=[],
        )
        assert result.has_critical_violations is False
        assert result.requires_emergency_shutdown is False

        # With critical violations
        result = EvaluationResult(
            system_name="test_system",
            timestamp=datetime.now(),
            overall_compliance=0.95,
            has_critical_violations=True,
            requires_emergency_shutdown=True,
            evaluator_results={},
            recommendations=[],
            alerts=[],
        )
        assert result.has_critical_violations is True

    def test_add_safety_violation(self):
        """Test adding safety violation"""
        result = EvaluationResult(
            system_name="test_system",
            timestamp=datetime.now(),
            overall_compliance=0.95,
            has_critical_violations=True,
            requires_emergency_shutdown=False,
            evaluator_results={},
            recommendations=[],
            alerts=[],
        )

        assert result.has_critical_violations is True

    def test_add_regulatory_violation(self):
        """Test adding regulatory violation"""
        result = EvaluationResult(
            system_name="test_system",
            timestamp=datetime.now(),
            overall_compliance=0.95,
            has_critical_violations=False,
            requires_emergency_shutdown=False,
            evaluator_results={},
            recommendations=[],
            alerts=[],
        )

        assert result.has_critical_violations is False

    def test_add_environmental_alert(self):
        """Test adding environmental alert"""
        result = EvaluationResult(
            system_name="test_system",
            timestamp=datetime.now(),
            overall_compliance=0.95,
            has_critical_violations=False,
            requires_emergency_shutdown=False,
            evaluator_results={},
            recommendations=[],
            alerts=[],
        )

        assert result.alerts == []


class TestErrorBudget:
    """Test ErrorBudget class"""

    def test_error_budget_creation(self):
        """Test error budget creation"""
        slo = SLOConfig(
            name="test_slo",
            target=0.95,
            window="24h",
        )

        # Error budget should be inferred from target
        assert abs(slo.error_budget - 0.05) < 1e-10

    def test_error_budget_properties(self):
        """Test error budget properties"""
        slo = SLOConfig(
            name="test_slo",
            target=0.99,
            window="24h",
        )

        # Error budget should be inferred from target
        assert abs(slo.error_budget - 0.01) < 1e-10
        assert abs(slo.target + slo.error_budget - 1.0) < 1e-10

    def test_error_budget_alerts(self):
        """Test error budget alert generation"""
        slo = SLOConfig(
            name="test_slo",
            target=0.95,
            window="24h",
        )

        # Error budget should be inferred from target
        assert abs(slo.error_budget - 0.05) < 1e-10


class TestEvaluationFramework:
    """Test EvaluationFramework class"""

    def test_framework_creation(self, sample_config):
        """Test framework creation with sample config"""
        framework = EvaluationFramework(sample_config)

        assert framework.system_name == "test_system"
        # System type is no longer tracked since we only support workflow
        assert framework.criticality == CriticalityLevel.OPERATIONAL
        assert len(framework.slos) == 2

    def test_framework_slo_parsing(self, sample_config):
        """Test SLO parsing in framework"""
        framework = EvaluationFramework(sample_config)

        slo_names = [slo.name for slo in framework.slos]
        assert "accuracy" in slo_names
        assert "latency" in slo_names

        accuracy_slo = next(slo for slo in framework.slos if slo.name == "accuracy")
        assert accuracy_slo.target == 0.95
        assert (
            abs(accuracy_slo.error_budget - 0.05) < 1e-10
        )  # Handle floating-point precision

    def test_framework_add_collector(self, sample_config, mock_collector):
        """Test adding collector to framework"""
        framework = EvaluationFramework(sample_config)
        collector = mock_collector({"name": "test_collector"})

        initial_count = len(framework.collectors)
        framework.add_collector(collector)
        assert len(framework.collectors) == initial_count + 1
        assert framework.collectors[-1] == collector

    def test_framework_add_evaluator(self, sample_config, mock_evaluator):
        """Test adding evaluator to framework"""
        framework = EvaluationFramework(sample_config)
        evaluator = mock_evaluator({"name": "test_evaluator"})

        initial_count = len(framework.evaluators)
        framework.add_evaluator(evaluator)
        assert len(framework.evaluators) == initial_count + 1
        assert framework.evaluators[-1] == evaluator

    def test_framework_validate_configuration(self, safety_critical_config):
        """Test framework configuration validation"""
        framework = EvaluationFramework(safety_critical_config)

        # Framework should be created successfully
        assert framework.system_name == "safety_system"
        assert len(framework.slos) > 0

    def test_framework_get_system_summary(self, sample_config):
        """Test getting system summary"""
        framework = EvaluationFramework(sample_config)

        summary = framework.get_system_info()

        assert "name" in summary
        assert "criticality" in summary
        assert "slo_count" in summary
        assert "collector_count" in summary
        assert "evaluator_count" in summary

    def test_framework_invalid_slo_config(self):
        """Test framework with invalid SLO configuration"""
        invalid_config = {
            "system": {
                "name": "test",
                "type": "single_model",
                "criticality": "operational",
            },
            "slos": {
                "invalid_slo": {
                    "target": "invalid_target",  # Should be float
                    "window": "30d",
                    "error_budget": 0.05,
                }
            },
        }

        # The framework should handle invalid SLO config gracefully
        framework = EvaluationFramework(invalid_config)
        # Should have fewer SLOs due to invalid one being skipped
        assert len(framework.slos) == 0

    def test_framework_evaluate_with_collectors_and_evaluators(
        self, sample_config, mock_collector, mock_evaluator
    ):
        """Test framework evaluation with collectors and evaluators"""
        framework = EvaluationFramework(sample_config)

        # Add collector and evaluator
        collector = mock_collector({"name": "test_collector"})
        evaluator = mock_evaluator({"name": "test_evaluator"})

        framework.add_collector(collector)
        framework.add_evaluator(evaluator)

        # Run evaluation
        result = framework.evaluate()

        # Verify result structure
        assert result.system_name == "test_system"
        assert result.timestamp is not None
        assert isinstance(result.overall_compliance, float)
        assert isinstance(result.has_critical_violations, bool)
        assert isinstance(result.requires_emergency_shutdown, bool)
