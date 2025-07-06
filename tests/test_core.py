"""Unit tests for core framework components"""

import pytest
from datetime import datetime, timedelta
from typing import Dict, Any

from ml_eval.core.types import SystemType, CriticalityLevel, ComplianceStandard
from ml_eval.core.config import SLOConfig, ErrorBudget, MetricData, EvaluationResult
from ml_eval.core.framework import EvaluationFramework


class TestSystemType:
    """Test SystemType enum"""

    def test_system_type_values(self):
        """Test that all system types have correct values"""
        assert SystemType.SINGLE_MODEL.value == "single_model"
        assert SystemType.WORKFLOW.value == "workflow"
        assert SystemType.PIPELINE.value == "pipeline"
        assert SystemType.DISTRIBUTED.value == "distributed"

    def test_system_type_from_string(self):
        """Test creating SystemType from string"""
        assert SystemType("single_model") == SystemType.SINGLE_MODEL
        assert SystemType("workflow") == SystemType.WORKFLOW


class TestCriticalityLevel:
    """Test CriticalityLevel enum"""

    def test_criticality_level_values(self):
        """Test that all criticality levels have correct values"""
        assert CriticalityLevel.SAFETY_CRITICAL.value == "safety_critical"
        assert CriticalityLevel.BUSINESS_CRITICAL.value == "business_critical"
        assert CriticalityLevel.OPERATIONAL.value == "operational"
        assert CriticalityLevel.EXPERIMENTAL.value == "experimental"

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
        assert ComplianceStandard.ISO_26262.value == "ISO-26262"
        assert ComplianceStandard.IEC_61508.value == "IEC-61508"
        assert ComplianceStandard.FDA_510K.value == "FDA-510K"
        assert ComplianceStandard.SOX.value == "SOX"
        assert ComplianceStandard.GDPR.value == "GDPR"

    def test_compliance_standard_from_string(self):
        """Test creating ComplianceStandard from string"""
        assert ComplianceStandard("DO-178C") == ComplianceStandard.DO_178C
        assert ComplianceStandard("ISO-26262") == ComplianceStandard.ISO_26262


class TestSLOConfig:
    """Test SLOConfig class"""

    def test_slo_config_creation(self):
        """Test basic SLO configuration creation"""
        slo = SLOConfig(
            name="test_slo",
            target=0.95,
            window="30d",
            error_budget=0.05,
            description="Test SLO",
        )

        assert slo.name == "test_slo"
        assert slo.target == 0.95
        assert slo.window == "30d"
        assert slo.error_budget == 0.05
        assert slo.description == "Test SLO"
        assert slo.safety_critical is False
        assert slo.compliance_standard is None

    def test_safety_critical_slo_validation(self):
        """Test safety-critical SLO validation"""
        # Should pass with small error budget
        slo = SLOConfig(
            name="safety_slo",
            target=0.999,
            window="1h",
            error_budget=0.001,
            safety_critical=True,
        )
        assert slo.safety_critical is True

        # Should fail with large error budget
        with pytest.raises(
            ValueError, match="Safety-critical SLO.*must have error budget <= 0.001"
        ):
            SLOConfig(
                name="invalid_safety_slo",
                target=0.999,
                window="1h",
                error_budget=0.01,
                safety_critical=True,
            )

    def test_compliance_standard_validation(self):
        """Test compliance standard validation"""
        # Valid compliance standards
        valid_standards = [
            "DO-178C",
            "ISO-26262",
            "IEC-61508",
            "FDA-510K",
            "SOX",
            "GDPR",
        ]
        for standard in valid_standards:
            slo = SLOConfig(
                name="test_slo",
                target=0.95,
                window="30d",
                error_budget=0.05,
                compliance_standard=standard,
            )
            assert slo.compliance_standard == standard

        # Invalid compliance standard
        with pytest.raises(ValueError, match="Unsupported compliance standard"):
            SLOConfig(
                name="test_slo",
                target=0.95,
                window="30d",
                error_budget=0.05,
                compliance_standard="INVALID_STANDARD",
            )

    def test_slo_with_environmental_conditions(self):
        """Test SLO with environmental conditions"""
        slo = SLOConfig(
            name="environmental_slo",
            target=0.95,
            window="30d",
            error_budget=0.05,
            environmental_conditions=["high_pressure", "salt_water"],
        )

        assert slo.environmental_conditions == ["high_pressure", "salt_water"]


class TestErrorBudget:
    """Test ErrorBudget class"""

    def test_error_budget_creation(self):
        """Test basic error budget creation"""
        budget = ErrorBudget(
            slo_name="test_slo", budget_remaining=0.03, burn_rate=0.001
        )

        assert budget.slo_name == "test_slo"
        assert budget.budget_remaining == 0.03
        assert budget.burn_rate == 0.001
        assert budget.safety_violation is False
        assert budget.regulatory_violation is False

    def test_error_budget_properties(self):
        """Test error budget properties"""
        # Not exhausted
        budget = ErrorBudget(
            slo_name="test_slo", budget_remaining=0.03, burn_rate=0.001
        )
        assert budget.is_exhausted is False
        assert budget.requires_immediate_action is False

        # Exhausted
        budget = ErrorBudget(slo_name="test_slo", budget_remaining=0.0, burn_rate=0.001)
        assert budget.is_exhausted is True
        assert budget.requires_immediate_action is True

    def test_error_budget_alerts(self):
        """Test error budget alert functionality"""
        budget = ErrorBudget(
            slo_name="test_slo", budget_remaining=0.03, burn_rate=0.001
        )

        budget.add_alert("Test warning", "warning")
        budget.add_alert("Test critical", "critical")

        assert len(budget.alerts) == 2
        assert "[WARNING] Test warning" in budget.alerts
        assert "[CRITICAL] Test critical" in budget.alerts

    def test_safety_violation_detection(self):
        """Test safety violation detection in alerts"""
        budget = ErrorBudget(
            slo_name="test_slo", budget_remaining=0.03, burn_rate=0.001
        )

        budget.add_alert("Safety violation detected", "critical")
        assert budget.safety_violation is True
        assert budget.regulatory_violation is False

    def test_regulatory_violation_detection(self):
        """Test regulatory violation detection in alerts"""
        budget = ErrorBudget(
            slo_name="test_slo", budget_remaining=0.03, burn_rate=0.001
        )

        budget.add_alert("Compliance violation detected", "critical")
        assert budget.regulatory_violation is True
        assert budget.safety_violation is False


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
        assert metric.environmental_conditions is None
        assert metric.compliance_context is None

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
        compliance_context = {"standard": "DO-178C", "level": "A"}

        metric = MetricData(
            timestamp=timestamp, value=0.95, compliance_context=compliance_context
        )

        assert metric.compliance_context == compliance_context


class TestEvaluationResult:
    """Test EvaluationResult class"""

    def test_evaluation_result_creation(self):
        """Test basic evaluation result creation"""
        result = EvaluationResult(
            system_name="test_system",
            evaluation_time=datetime.now(),
            slo_compliance={"accuracy": True},
            error_budgets={},
        )

        assert result.system_name == "test_system"
        assert result.slo_compliance == {"accuracy": True}
        assert result.error_budgets == {}
        assert result.incidents == []
        assert result.recommendations == []

    def test_evaluation_result_properties(self):
        """Test evaluation result properties"""
        # No violations
        result = EvaluationResult(
            system_name="test_system",
            evaluation_time=datetime.now(),
            slo_compliance={"accuracy": True},
            error_budgets={},
        )
        assert result.has_critical_violations is False
        assert result.requires_emergency_shutdown is False

        # With safety violation
        result = EvaluationResult(
            system_name="test_system",
            evaluation_time=datetime.now(),
            slo_compliance={"accuracy": True},
            error_budgets={},
            safety_violations=[{"test": "violation"}],
        )
        assert result.has_critical_violations is True

    def test_add_safety_violation(self):
        """Test adding safety violation"""
        result = EvaluationResult(
            system_name="test_system",
            evaluation_time=datetime.now(),
            slo_compliance={"accuracy": True},
            error_budgets={},
        )

        result.add_safety_violation("test_slo", {"details": "test"})

        assert len(result.safety_violations) == 1
        violation = result.safety_violations[0]
        assert violation["slo_name"] == "test_slo"
        assert violation["severity"] == "critical"
        assert "details" in violation["details"]

    def test_add_regulatory_violation(self):
        """Test adding regulatory violation"""
        result = EvaluationResult(
            system_name="test_system",
            evaluation_time=datetime.now(),
            slo_compliance={"accuracy": True},
            error_budgets={},
        )

        result.add_regulatory_violation("test_slo", "DO-178C", {"details": "test"})

        assert len(result.regulatory_violations) == 1
        violation = result.regulatory_violations[0]
        assert violation["slo_name"] == "test_slo"
        assert violation["compliance_standard"] == "DO-178C"
        assert violation["severity"] == "critical"

    def test_add_environmental_alert(self):
        """Test adding environmental alert"""
        result = EvaluationResult(
            system_name="test_system",
            evaluation_time=datetime.now(),
            slo_compliance={"accuracy": True},
            error_budgets={},
        )

        result.add_environmental_alert("high_temperature", {"temp": 50.0})

        assert len(result.environmental_alerts) == 1
        alert = result.environmental_alerts[0]
        assert alert["condition"] == "high_temperature"
        assert alert["details"]["temp"] == 50.0


class TestEvaluationFramework:
    """Test EvaluationFramework class"""

    def test_framework_creation(self, sample_config):
        """Test framework creation with sample config"""
        framework = EvaluationFramework(sample_config)

        assert framework.system_name == "test_system"
        assert framework.system_type == SystemType.SINGLE_MODEL
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
        assert accuracy_slo.error_budget == 0.05

    def test_framework_add_collector(self, sample_config, mock_collector):
        """Test adding collector to framework"""
        framework = EvaluationFramework(sample_config)
        collector = mock_collector({"name": "test_collector"})

        framework.add_collector(collector)
        assert len(framework.collectors) == 1
        assert framework.collectors[0] == collector

    def test_framework_add_evaluator(self, sample_config, mock_evaluator):
        """Test adding evaluator to framework"""
        framework = EvaluationFramework(sample_config)
        evaluator = mock_evaluator({"name": "test_evaluator"})

        framework.add_evaluator(evaluator)
        assert len(framework.evaluators) == 1
        assert framework.evaluators[0] == evaluator

    def test_framework_validate_configuration(self, safety_critical_config):
        """Test framework configuration validation"""
        framework = EvaluationFramework(safety_critical_config)

        # Should fail without safety-critical SLO
        assert framework.validate_configuration() is False

        # Add safety-critical SLO
        safety_slo = SLOConfig(
            name="safety_slo",
            target=0.999,
            window="1h",
            error_budget=0.001,
            safety_critical=True,
        )
        framework.slos.append(safety_slo)

        # Add required RegulatoryCollector for compliance standards
        from ml_eval.collectors.regulatory import RegulatoryCollector

        regulatory_collector = RegulatoryCollector(
            {"name": "regulatory_collector", "standards": ["DO-178C"]}
        )
        framework.add_collector(regulatory_collector)

        # Should pass with safety-critical SLO and regulatory collector
        assert framework.validate_configuration() is True

    def test_framework_get_system_summary(self, sample_config):
        """Test getting system summary"""
        framework = EvaluationFramework(sample_config)

        summary = framework.get_system_summary()

        assert summary["name"] == "test_system"
        assert summary["type"] == "single_model"
        assert summary["criticality"] == "operational"
        assert summary["slo_count"] == 2
        assert summary["collector_count"] == 0
        assert summary["evaluator_count"] == 0

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
        # Should fail validation due to invalid SLO
        assert framework.validate_configuration() is False

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
        assert result.evaluation_time is not None
        assert hasattr(result, "slo_compliance")
        assert hasattr(result, "error_budgets")
        assert hasattr(result, "incidents")
        assert hasattr(result, "recommendations")
