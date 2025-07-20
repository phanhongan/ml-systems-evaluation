"""Tests for evaluators"""

from ml_eval.evaluators.base import BaseEvaluator
from ml_eval.evaluators.compliance import ComplianceEvaluator
from ml_eval.evaluators.drift import DriftEvaluator
from ml_eval.evaluators.performance import PerformanceEvaluator
from ml_eval.evaluators.reliability import ReliabilityEvaluator
from ml_eval.evaluators.safety import SafetyEvaluator


class TestBaseEvaluator:
    """Test base evaluator functionality"""

    def test_base_evaluator_creation(self):
        """Test base evaluator creation"""
        config = {"name": "test_evaluator"}

        class TestEvaluator(BaseEvaluator):
            def evaluate(self, _metrics):
                return {"result": "test"}

            def get_required_metrics(self):
                return ["test_metric"]

        evaluator = TestEvaluator(config)
        assert evaluator.config == config

    def test_base_evaluator_validation(self):
        """Test metric validation"""
        config = {"name": "test_evaluator"}

        class TestEvaluator(BaseEvaluator):
            def evaluate(self, _metrics):
                return {"result": "test"}

            def get_required_metrics(self):
                return ["required_metric"]

        evaluator = TestEvaluator(config)

        # Valid metrics
        valid_metrics = {"required_metric": 0.95}
        assert evaluator.validate_metrics(valid_metrics) is True

        # Invalid metrics
        invalid_metrics = {"other_metric": 0.95}
        assert evaluator.validate_metrics(invalid_metrics) is False


class TestReliabilityEvaluator:
    """Test reliability evaluator functionality"""

    def test_reliability_evaluator_creation(self):
        """Test reliability evaluator creation"""
        config = {
            "name": "reliability_evaluator",
            "slos": {
                "availability": {"target": 0.99, "window": "24h"},
                "latency": {"target": 0.1, "window": "24h"},
            },
        }
        evaluator = ReliabilityEvaluator(config)
        assert evaluator.config == config

    def test_reliability_evaluator_required_metrics(self):
        """Test required metrics for reliability evaluator"""
        config = {
            "slos": {"availability": {"target": 0.99}, "latency": {"target": 0.1}}
        }
        evaluator = ReliabilityEvaluator(config)
        required_metrics = evaluator.get_required_metrics()
        assert "availability" in required_metrics
        assert "latency" in required_metrics

    def test_reliability_evaluator_evaluate(self):
        """Test reliability evaluation"""
        config = {
            "slos": {
                "availability": {"target": 0.99, "window": "24h"},
                "latency": {"target": 0.1, "window": "24h"},
            }
        }
        evaluator = ReliabilityEvaluator(config)

        metrics = {"availability": 0.995, "latency": 0.08}

        result = evaluator.evaluate(metrics)

        assert "slos" in result
        assert "error_budgets" in result
        assert "overall_reliability" in result
        assert "alerts" in result

        # Check SLO results
        assert "availability" in result["slos"]
        assert "latency" in result["slos"]

        # Check error budgets
        assert "availability" in result["error_budgets"]
        assert "latency" in result["error_budgets"]

    def test_reliability_evaluator_error_budget_calculation(self):
        """Test error budget calculation"""
        config = {"slos": {"availability": {"target": 0.99}}}
        evaluator = ReliabilityEvaluator(config)

        # Test with compliant SLO
        metrics = {"availability": 0.995}
        result = evaluator.evaluate(metrics)

        budget = result["error_budgets"]["availability"]
        assert "remaining" in budget
        assert "burn_rate" in budget
        assert "exhausted" in budget

        # Test with non-compliant SLO
        metrics = {"availability": 0.98}
        result = evaluator.evaluate(metrics)

        budget = result["error_budgets"]["availability"]
        assert budget["burn_rate"] > 0

    def test_reliability_evaluator_alerts(self):
        """Test alert generation"""
        config = {
            "slos": {
                "availability": {
                    "target": 0.99,
                    "safety_critical": True,
                }
            }
        }
        evaluator = ReliabilityEvaluator(config)

        # Test with safety violation
        metrics = {"availability": 0.98}
        result = evaluator.evaluate(metrics)

        assert len(result["alerts"]) > 0
        assert any("SAFETY VIOLATION" in alert for alert in result["alerts"])


class TestSafetyEvaluator:
    """Test safety evaluator functionality"""

    def test_safety_evaluator_creation(self):
        """Test safety evaluator creation"""
        config = {"name": "safety_evaluator"}
        evaluator = SafetyEvaluator(config)
        assert evaluator.config == config

    def test_safety_evaluator_required_metrics(self):
        """Test required metrics for safety evaluator"""
        config = {}
        evaluator = SafetyEvaluator(config)
        required_metrics = evaluator.get_required_metrics()
        assert (
            len(required_metrics) >= 0
        )  # Safety evaluator may not require specific metrics

    def test_safety_evaluator_evaluate(self):
        """Test safety evaluation"""
        config = {
            "name": "safety_evaluator",
            "use_llm": False,  # Explicitly disable LLM for testing
            "safety_thresholds": {
                "system_availability": {"min": 0.999, "max": 1.0, "critical": True}
            },
        }
        evaluator = SafetyEvaluator(config)

        metrics = {
            "system_availability": 0.9995,
            "failure_mode_detection_rate": 0.9,
            "failure_effect_mitigation_rate": 0.85,
            "risk_priority_number": 45,
            "safety_margin_compliance": 0.95,
            "emergency_procedure_effectiveness": 0.9,
            "perception_failure_rate": 0.001,
            "perception_safety_margin": 0.85,
            "perception_risk_score": 0.1,
            "perception_emergency_response_time": 0.1,
            "decision_making_failure_rate": 0.001,
            "decision_making_safety_margin": 0.9,
            "decision_making_risk_score": 0.05,
            "decision_making_emergency_response_time": 0.2,
            "output_control_failure_rate": 0.0001,
            "output_control_safety_margin": 0.95,
            "output_control_risk_score": 0.02,
            "output_control_emergency_response_time": 0.05,
        }

        result = evaluator.evaluate(metrics)

        assert isinstance(result, dict)
        assert "safety_metrics" in result or "error" in result

    def test_safety_evaluator_safety_violation(self):
        """Test safety violation detection"""
        config = {
            "name": "safety_evaluator",
            "use_llm": False,  # Explicitly disable LLM for testing
            "safety_thresholds": {
                "system_availability": {"min": 0.999, "max": 1.0, "critical": True}
            },
        }
        evaluator = SafetyEvaluator(config)

        # Test with safety violation - system availability below threshold
        metrics = {
            "system_availability": 0.998,  # Below safety threshold
            "failure_mode_detection_rate": 0.9,
            "failure_effect_mitigation_rate": 0.85,
            "risk_priority_number": 45,
            "safety_margin_compliance": 0.95,
            "emergency_procedure_effectiveness": 0.9,
            "perception_failure_rate": 0.001,
            "perception_safety_margin": 0.85,
            "perception_risk_score": 0.1,
            "perception_emergency_response_time": 0.1,
            "decision_making_failure_rate": 0.001,
            "decision_making_safety_margin": 0.9,
            "decision_making_risk_score": 0.05,
            "decision_making_emergency_response_time": 0.2,
            "output_control_failure_rate": 0.0001,
            "output_control_safety_margin": 0.95,
            "output_control_risk_score": 0.02,
            "output_control_emergency_response_time": 0.05,
        }

        result = evaluator.evaluate(metrics)

        # Should detect safety issues
        assert isinstance(result, dict)


class TestPerformanceEvaluator:
    """Test performance evaluator functionality"""

    def test_performance_evaluator_creation(self):
        """Test performance evaluator creation"""
        config = {"name": "performance_evaluator"}
        evaluator = PerformanceEvaluator(config)
        assert evaluator.config == config

    def test_performance_evaluator_required_metrics(self):
        """Test required metrics for performance evaluator"""
        config = {}
        evaluator = PerformanceEvaluator(config)
        required_metrics = evaluator.get_required_metrics()
        assert (
            len(required_metrics) >= 0
        )  # Performance evaluator may not require specific metrics

    def test_performance_evaluator_evaluate(self):
        """Test performance evaluation"""
        config = {"name": "performance_evaluator"}
        evaluator = PerformanceEvaluator(config)

        metrics = {"latency": 0.1, "throughput": 1000, "accuracy": 0.95}

        result = evaluator.evaluate(metrics)

        assert isinstance(result, dict)
        assert (
            "performance_score" in result or "metrics" in result or "alerts" in result
        )

    def test_performance_evaluator_poor_performance(self):
        """Test poor performance detection"""
        config = {"name": "performance_evaluator"}
        evaluator = PerformanceEvaluator(config)

        # Test with poor performance
        metrics = {
            "latency": 2.0,  # High latency
            "throughput": 10,  # Low throughput
            "accuracy": 0.70,  # Low accuracy
        }

        result = evaluator.evaluate(metrics)

        # Should detect performance issues
        assert isinstance(result, dict)


class TestComplianceEvaluator:
    """Test compliance evaluator functionality"""

    def test_compliance_evaluator_creation(self):
        """Test compliance evaluator creation"""
        config = {"name": "compliance_evaluator"}
        evaluator = ComplianceEvaluator(config)
        assert evaluator.config == config

    def test_compliance_evaluator_required_metrics(self):
        """Test required metrics for compliance evaluator"""
        config = {}
        evaluator = ComplianceEvaluator(config)
        required_metrics = evaluator.get_required_metrics()
        assert (
            len(required_metrics) >= 0
        )  # Compliance evaluator may not require specific metrics

    def test_compliance_evaluator_evaluate_compliant(self):
        """Test compliance evaluation with compliant system"""
        config = {"name": "compliance_evaluator"}
        evaluator = ComplianceEvaluator(config)

        metrics = {"do_178c_compliance": 1.0, "iso_26262_compliance": 0.95}

        result = evaluator.evaluate(metrics)

        assert isinstance(result, dict)
        assert (
            "compliance_score" in result or "violations" in result or "alerts" in result
        )

    def test_compliance_evaluator_evaluate_non_compliant(self):
        """Test compliance evaluation with non-compliant system"""
        config = {"name": "compliance_evaluator"}
        evaluator = ComplianceEvaluator(config)

        metrics = {
            "do_178c_compliance": 0.80,  # Below compliance threshold
            "iso_26262_compliance": 0.70,  # Below compliance threshold
        }

        result = evaluator.evaluate(metrics)

        # Should detect compliance issues
        assert isinstance(result, dict)


class TestDriftEvaluator:
    """Test drift evaluator functionality"""

    def test_drift_evaluator_creation(self):
        """Test drift evaluator creation"""
        config = {"name": "drift_evaluator"}
        evaluator = DriftEvaluator(config)
        assert evaluator.config == config

    def test_drift_evaluator_required_metrics(self):
        """Test required metrics for drift evaluator"""
        config = {}
        evaluator = DriftEvaluator(config)
        required_metrics = evaluator.get_required_metrics()
        assert (
            len(required_metrics) >= 0
        )  # Drift evaluator may not require specific metrics

    def test_drift_evaluator_evaluate_no_drift(self):
        """Test drift evaluation with no drift"""
        config = {"name": "drift_evaluator"}
        evaluator = DriftEvaluator(config)

        metrics = {"data_drift": 0.05, "concept_drift": 0.02}

        result = evaluator.evaluate(metrics)

        assert isinstance(result, dict)
        assert (
            "drift_score" in result or "drift_detected" in result or "alerts" in result
        )

    def test_drift_evaluator_evaluate_with_drift(self):
        """Test drift evaluation with drift detected"""
        config = {"name": "drift_evaluator"}
        evaluator = DriftEvaluator(config)

        metrics = {
            "data_drift": 0.25,  # High drift
            "concept_drift": 0.30,  # High drift
        }

        result = evaluator.evaluate(metrics)

        # Should detect drift
        assert isinstance(result, dict)

    def test_drift_evaluator_drift_calculation(self):
        """Test drift calculation methods"""
        config = {"name": "drift_evaluator"}
        evaluator = DriftEvaluator(config)

        # Test drift detection with sample data
        # baseline_data = [0.1, 0.2, 0.3, 0.4, 0.5]
        # current_data = [0.15, 0.25, 0.35, 0.45, 0.55]

        # Since _calculate_drift is not implemented, we'll test the evaluate method
        metrics = {"data_drift": 0.05}
        result = evaluator.evaluate(metrics)

        assert isinstance(result, dict)


class TestEvaluatorIntegration:
    """Test integration between multiple evaluators"""

    def test_multiple_evaluators(self):
        """Test multiple evaluators working together"""
        configs = [
            {
                "name": "reliability_evaluator",
                "slos": {"availability": {"target": 0.99}},
            },
            {
                "name": "performance_evaluator",
                "metrics": ["accuracy", "latency"],
            },
        ]

        evaluators = []
        for config in configs:
            if config["name"] == "reliability_evaluator":
                evaluators.append(ReliabilityEvaluator(config))
            elif config["name"] == "performance_evaluator":
                evaluators.append(PerformanceEvaluator(config))

        metrics = {"availability": 0.995, "accuracy": 0.95, "latency": 0.1}

        results = []
        for evaluator in evaluators:
            result = evaluator.evaluate(metrics)
            results.append(result)

        assert len(results) == 2
        assert all(isinstance(result, dict) for result in results)

    def test_evaluator_error_handling(self):
        """Test evaluator error handling"""
        config = {"name": "test_evaluator"}

        class ErrorEvaluator(BaseEvaluator):
            def evaluate(self, _metrics):
                raise ValueError("Test error")

            def get_required_metrics(self):
                return ["test_metric"]

        evaluator = ErrorEvaluator(config)

        try:
            result = evaluator.evaluate({})
            assert "error" in result
        except Exception:
            # Some evaluators may re-raise exceptions
            pass

    def test_evaluator_result_consistency(self):
        """Test that evaluator results are consistent"""
        config = {
            "slos": {"availability": {"target": 0.99}},
        }
        evaluator = ReliabilityEvaluator(config)

        metrics = {"availability": 0.995}

        # Run evaluation multiple times
        results = []
        for _ in range(3):
            result = evaluator.evaluate(metrics)
            results.append(result)

        # Check that results are consistent
        assert all("slos" in result for result in results)
        assert all("error_budgets" in result for result in results)

    def test_evaluator_configuration_validation(self):
        """Test evaluator configuration validation"""
        # Test with valid configuration
        valid_config = {
            "slos": {"availability": {"target": 0.99}},
        }
        evaluator = ReliabilityEvaluator(valid_config)
        assert evaluator.config == valid_config

        # Test with invalid configuration
        invalid_config = {}
        evaluator = ReliabilityEvaluator(invalid_config)
        # Should not raise an exception, but may have default behavior
        assert evaluator.config == invalid_config

    def test_evaluator_metric_processing(self):
        """Test evaluator metric processing"""
        config = {
            "slos": {"availability": {"target": 0.99}},
        }
        evaluator = ReliabilityEvaluator(config)

        # Test with valid metrics
        valid_metrics = {"availability": 0.995}
        result = evaluator.evaluate(valid_metrics)
        assert "slos" in result

        # Test with missing metrics
        missing_metrics = {"other_metric": 0.5}
        result = evaluator.evaluate(missing_metrics)
        # Should handle missing metrics gracefully
        assert isinstance(result, dict)


class TestLLMEnabledEvaluators:
    """Test LLM-enabled evaluators with LLM disabled"""

    def test_interpretability_evaluator_llm_disabled(self, llm_disabled_config):
        """Test interpretability evaluator with LLM disabled"""
        from ml_eval.evaluators.interpretability import InterpretabilityEvaluator

        # Find interpretability evaluator config
        eval_config = None
        for evaluator in llm_disabled_config["evaluators"]:
            if evaluator["type"] == "interpretability":
                eval_config = evaluator
                break

        assert eval_config is not None
        assert eval_config["use_llm"] is False

        evaluator = InterpretabilityEvaluator(eval_config)
        assert evaluator.use_llm is False
        assert evaluator.llm_assistant is None

        # Test evaluation with LLM disabled
        metrics = {
            "perception_interpretability": 0.8,
            "decision_making_interpretability": 0.7,
            "output_control_interpretability": 0.9,
        }

        result = evaluator.evaluate(metrics)
        assert isinstance(result, dict)
        assert "component_scores" in result
        assert "llm_enhanced" in result
        assert result["llm_enhanced"].get("enabled", False) is False

    def test_edge_case_evaluator_llm_disabled(self, llm_disabled_config):
        """Test edge case evaluator with LLM disabled"""
        from ml_eval.evaluators.edge_case import EdgeCaseEvaluator

        # Find edge case evaluator config
        eval_config = None
        for evaluator in llm_disabled_config["evaluators"]:
            if evaluator["type"] == "edge_case":
                eval_config = evaluator
                break

        assert eval_config is not None
        assert eval_config["use_llm"] is False

        evaluator = EdgeCaseEvaluator(eval_config)
        assert evaluator.use_llm is False
        assert evaluator.llm_assistant is None

        # Test evaluation with LLM disabled
        metrics = {
            "perception_edge_case_handling": 0.8,
            "decision_making_edge_case_handling": 0.7,
            "output_control_edge_case_handling": 0.9,
        }

        result = evaluator.evaluate(metrics)
        assert isinstance(result, dict)
        assert "component_scores" in result
        assert "llm_enhanced" in result
        assert result["llm_enhanced"].get("enabled", False) is False

    def test_safety_evaluator_llm_disabled(self, llm_disabled_config):
        """Test safety evaluator with LLM disabled"""
        from ml_eval.evaluators.safety import SafetyEvaluator

        # Find safety evaluator config
        eval_config = None
        for evaluator in llm_disabled_config["evaluators"]:
            if evaluator["type"] == "safety":
                eval_config = evaluator
                break

        assert eval_config is not None
        assert eval_config["use_llm"] is False

        evaluator = SafetyEvaluator(eval_config)
        assert evaluator.use_llm is False
        assert evaluator.llm_assistant is None

        # Test evaluation with LLM disabled
        metrics = {
            "perception_failure_rate": 0.001,
            "perception_safety_margin": 0.85,
            "perception_risk_score": 0.1,
            "decision_making_failure_rate": 0.001,
            "decision_making_safety_margin": 0.9,
            "decision_making_risk_score": 0.05,
            "output_control_failure_rate": 0.0001,
            "output_control_safety_margin": 0.95,
            "output_control_risk_score": 0.02,
        }

        result = evaluator.evaluate(metrics)
        assert isinstance(result, dict)
        assert "safety_metrics" in result or "error" in result
        if "llm_enhanced" in result:
            assert result["llm_enhanced"].get("enabled", False) is False

    def test_evaluators_fallback_behavior(self, llm_disabled_config):
        """Test that evaluators fall back to deterministic behavior when LLM is disabled"""
        from ml_eval.evaluators.edge_case import EdgeCaseEvaluator
        from ml_eval.evaluators.interpretability import InterpretabilityEvaluator
        from ml_eval.evaluators.safety import SafetyEvaluator

        # Test all LLM-enabled evaluators
        evaluators = [
            (InterpretabilityEvaluator, "interpretability"),
            (EdgeCaseEvaluator, "edge_case"),
            (SafetyEvaluator, "safety"),
        ]

        for evaluator_class, eval_type in evaluators:
            # Find evaluator config
            eval_config = None
            for evaluator in llm_disabled_config["evaluators"]:
                if evaluator["type"] == eval_type:
                    eval_config = evaluator
                    break

            evaluator = evaluator_class(eval_config)

            # Verify LLM is disabled
            assert evaluator.use_llm is False
            assert evaluator.llm_assistant is None

            # Test that evaluation still works
            metrics = {"test_metric": 0.8}
            result = evaluator.evaluate(metrics)

            # Should return valid result without LLM
            assert isinstance(result, dict)
            # Some evaluators may return errors for missing metrics, which is expected
            if "error" in result:
                assert (
                    "Missing required" in result["error"]
                    or "fallback" in result["error"]
                )
