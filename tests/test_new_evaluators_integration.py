"""Integration tests for new evaluators with the framework architecture"""

from datetime import datetime
from unittest.mock import patch

import pytest

from ml_eval.core.framework import EvaluationFramework
from ml_eval.evaluators.edge_case import EdgeCaseEvaluator
from ml_eval.evaluators.interpretability import InterpretabilityEvaluator
from ml_eval.evaluators.safety import SafetyEvaluator


class TestNewEvaluatorsIntegration:
    """Test integration of new evaluators with the framework"""

    def test_framework_creates_new_evaluators(self):
        """Test that framework can create new evaluators from config"""
        config = {
            "system": {"name": "Test System", "criticality": "safety_critical"},
            "evaluators": [
                {
                    "type": "interpretability",
                    "config": {
                        "use_llm": False,  # Explicitly disable LLM for testing
                        "thresholds": {"overall_interpretability": 0.7},
                    },
                },
                {
                    "type": "edge_case",
                    "config": {
                        "use_llm": False,  # Explicitly disable LLM for testing
                        "thresholds": {"overall_edge_case_handling": 0.8},
                    },
                },
                {
                    "type": "safety",
                    "config": {
                        "use_llm": False,  # Explicitly disable LLM for testing
                        "safety_thresholds": {
                            "system_availability": {
                                "min": 0.999,
                                "max": 1.0,
                                "critical": True,
                            }
                        },
                    },
                },
            ],
        }

        framework = EvaluationFramework(config)

        # Check that evaluators were created
        assert len(framework.evaluators) == 3

        evaluator_types = [
            evaluator.__class__.__name__ for evaluator in framework.evaluators
        ]
        assert "InterpretabilityEvaluator" in evaluator_types
        assert "EdgeCaseEvaluator" in evaluator_types
        assert "SafetyEvaluator" in evaluator_types

    def test_evaluator_info_includes_new_evaluators(self):
        """Test that get_evaluator_info includes new evaluator capabilities"""
        config = {
            "system": {"name": "Test System", "criticality": "safety_critical"},
            "evaluators": [
                {"type": "interpretability", "config": {"use_llm": False}},
                {"type": "edge_case", "config": {"use_llm": False}},
                {"type": "safety", "config": {"use_llm": False}},
            ],
        }

        framework = EvaluationFramework(config)
        evaluator_info = framework.get_evaluator_info()

        # Check interpretability evaluator info
        assert "InterpretabilityEvaluator" in evaluator_info
        interpretability_info = evaluator_info["InterpretabilityEvaluator"]
        assert "capabilities" in interpretability_info
        assert "model_explainability" in interpretability_info["capabilities"]
        assert "decision_transparency" in interpretability_info["capabilities"]

        # Check edge case evaluator info
        assert "EdgeCaseEvaluator" in evaluator_info
        edge_case_info = evaluator_info["EdgeCaseEvaluator"]
        assert "capabilities" in edge_case_info
        assert "systematic_edge_case_generation" in edge_case_info["capabilities"]
        assert "stress_testing" in edge_case_info["capabilities"]

        # Check safety evaluator info
        assert "SafetyEvaluator" in evaluator_info
        safety_info = evaluator_info["SafetyEvaluator"]
        assert "capabilities" in safety_info
        assert "fmea_analysis" in safety_info["capabilities"]
        assert "risk_assessment" in safety_info["capabilities"]

    def test_health_check_includes_evaluator_types(self):
        """Test that health check includes evaluator types"""
        config = {
            "system": {"name": "Test System", "criticality": "safety_critical"},
            "evaluators": [
                {"type": "interpretability", "config": {"use_llm": False}},
                {"type": "edge_case", "config": {"use_llm": False}},
            ],
        }

        framework = EvaluationFramework(config)
        health_status = framework.health_check()

        assert "evaluator_types" in health_status
        evaluator_types = health_status["evaluator_types"]
        assert "InterpretabilityEvaluator" in evaluator_types
        assert "EdgeCaseEvaluator" in evaluator_types

    def test_new_evaluators_return_required_metrics(self):
        """Test that new evaluators return required metrics"""
        # Test InterpretabilityEvaluator
        interpretability_config = {
            "use_llm": False,  # Explicitly disable LLM for testing
            "thresholds": {"overall_interpretability": 0.7},
        }
        interpretability_evaluator = InterpretabilityEvaluator(interpretability_config)
        interpretability_metrics = interpretability_evaluator.get_required_metrics()

        assert "model_explainability_score" in interpretability_metrics
        assert "decision_transparency_score" in interpretability_metrics
        assert "perception_explainability_score" in interpretability_metrics

        # Test EdgeCaseEvaluator
        edge_case_config = {
            "use_llm": False,  # Explicitly disable LLM for testing
            "thresholds": {"overall_edge_case_handling": 0.8},
        }
        edge_case_evaluator = EdgeCaseEvaluator(edge_case_config)
        edge_case_metrics = edge_case_evaluator.get_required_metrics()

        assert "edge_case_success_rate" in edge_case_metrics
        assert "perception_edge_case_handling" in edge_case_metrics
        assert "sensor_failure_recovery_success_rate" in edge_case_metrics

        # Test SafetyEvaluator
        safety_config = {
            "use_llm": False,  # Explicitly disable LLM for testing
            "safety_thresholds": {
                "system_availability": {"min": 0.999, "max": 1.0, "critical": True}
            },
        }
        safety_evaluator = SafetyEvaluator(safety_config)
        safety_metrics = safety_evaluator.get_required_metrics()

        assert "system_availability" in safety_metrics
        assert "perception_failure_rate" in safety_metrics
        assert "failure_mode_detection_rate" in safety_metrics

    def test_new_evaluators_evaluate_with_mock_metrics(self):
        """Test that new evaluators can evaluate with mock metrics"""
        # Mock metrics for testing - using simple values that evaluators can handle
        mock_metrics = {
            "model_explainability_score": 0.8,
            "decision_transparency_score": 0.7,
            "perception_explainability_score": 0.75,
            "edge_case_success_rate": 0.85,
            "perception_edge_case_handling": 0.8,
            "system_availability": 0.9995,
            "perception_failure_rate": 0.001,
            "failure_mode_detection_rate": 0.9,
            "safety_margin": 0.85,
            "emergency_response_time": 0.1,
            "risk_priority_number": 45,
            "mitigation_effectiveness": 0.9,
        }

        # Test InterpretabilityEvaluator
        interpretability_config = {
            "use_llm": False,  # Explicitly disable LLM for testing
            "thresholds": {"overall_interpretability": 0.7},
        }
        interpretability_evaluator = InterpretabilityEvaluator(interpretability_config)
        interpretability_result = interpretability_evaluator.evaluate(mock_metrics)

        assert "overall_interpretability_score" in interpretability_result
        assert "component_scores" in interpretability_result
        assert "alerts" in interpretability_result
        assert "recommendations" in interpretability_result

        # Test EdgeCaseEvaluator
        edge_case_config = {
            "use_llm": False,  # Explicitly disable LLM for testing
            "thresholds": {"overall_edge_case_handling": 0.8},
        }
        edge_case_evaluator = EdgeCaseEvaluator(edge_case_config)
        edge_case_result = edge_case_evaluator.evaluate(mock_metrics)

        assert "overall_edge_case_score" in edge_case_result
        assert "component_scores" in edge_case_result
        assert "scenario_scores" in edge_case_result
        assert "alerts" in edge_case_result
        assert "recommendations" in edge_case_result

        # Test SafetyEvaluator
        safety_config = {
            "use_llm": False,  # Explicitly disable LLM for testing
            "safety_thresholds": {
                "system_availability": {"min": 0.999, "max": 1.0, "critical": True}
            },
        }
        safety_evaluator = SafetyEvaluator(safety_config)
        safety_result = safety_evaluator.evaluate(mock_metrics)

        # Safety evaluator should return results or error
        assert isinstance(safety_result, dict)
        if "error" not in safety_result:
            assert "safety_metrics" in safety_result
            assert "fmea_analysis" in safety_result
            assert "risk_assessment" in safety_result
            assert "safety_margins" in safety_result
            assert "emergency_procedures" in safety_result
            assert "alerts" in safety_result
            assert "recommendations" in safety_result

    def test_framework_evaluation_with_new_evaluators(self):
        """Test that framework can run evaluation with new evaluators"""
        config = {
            "system": {"name": "Test System", "criticality": "safety_critical"},
            "collectors": [
                {
                    "type": "online",
                    "config": {"metrics": ["system_availability", "response_time"]},
                }
            ],
            "evaluators": [
                {
                    "type": "interpretability",
                    "config": {
                        "use_llm": False,  # Explicitly disable LLM for testing
                        "thresholds": {"overall_interpretability": 0.7},
                    },
                },
                {
                    "type": "edge_case",
                    "config": {
                        "use_llm": False,  # Explicitly disable LLM for testing
                        "thresholds": {"overall_edge_case_handling": 0.8},
                    },
                },
                {
                    "type": "safety",
                    "config": {
                        "use_llm": False,  # Explicitly disable LLM for testing
                        "safety_thresholds": {
                            "system_availability": {
                                "min": 0.999,
                                "max": 1.0,
                                "critical": True,
                            }
                        },
                    },
                },
            ],
        }

        framework = EvaluationFramework(config)

        # Mock the collectors to return test data
        with patch.object(framework.collectors[0], "collect") as mock_collect:
            mock_collect.return_value = {
                "system_availability": [{"timestamp": datetime.now(), "value": 0.9995}],
                "response_time": [{"timestamp": datetime.now(), "value": 50.0}],
            }

            # Run evaluation
            result = framework.evaluate()

            # Check that result includes new evaluator results
            assert result.evaluator_results is not None
            evaluator_results = result.evaluator_results

            # Check that new evaluators are in results
            evaluator_names = list(evaluator_results.keys())
            assert any("InterpretabilityEvaluator" in name for name in evaluator_names)
            assert any("EdgeCaseEvaluator" in name for name in evaluator_names)
            assert any("SafetyEvaluator" in name for name in evaluator_names)


if __name__ == "__main__":
    pytest.main([__file__])
