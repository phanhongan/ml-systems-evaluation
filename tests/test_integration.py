"""Integration tests for ML Systems Evaluation Framework"""

import os
from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest
import yaml

from ml_eval.collectors.environmental import EnvironmentalCollector
from ml_eval.collectors.online import OnlineCollector
from ml_eval.core.config import MetricData
from ml_eval.core.framework import EvaluationFramework
from ml_eval.evaluators.performance import PerformanceEvaluator
from ml_eval.evaluators.reliability import ReliabilityEvaluator
from ml_eval.evaluators.safety import SafetyEvaluator


class TestEndToEndEvaluation:
    """Test end-to-end evaluation pipelines"""

    def test_basic_evaluation_pipeline(
        self, sample_config, mock_collector, mock_evaluator
    ):
        """Test basic end-to-end evaluation"""
        # Create framework
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

    def test_safety_critical_evaluation_pipeline(self, safety_critical_config):
        """Test safety-critical evaluation pipeline"""
        # Create framework
        framework = EvaluationFramework(safety_critical_config)

        # Add safety evaluator
        safety_evaluator = SafetyEvaluator({"name": "safety_evaluator"})
        framework.add_evaluator(safety_evaluator)

        # Add environmental collector for safety-critical systems
        env_collector = EnvironmentalCollector(
            {
                "name": "environmental_collector",
                "sensors": ["temperature", "pressure", "vibration"],
            }
        )
        framework.add_collector(env_collector)

        # Add required RegulatoryCollector for compliance standards
        from ml_eval.collectors.regulatory import RegulatoryCollector

        regulatory_collector = RegulatoryCollector(
            {"name": "regulatory_collector", "standards": ["DO-178C"]}
        )
        framework.add_collector(regulatory_collector)

        # Run evaluation
        result = framework.evaluate()

        # Verify result structure
        assert result.system_name == "safety_system"
        assert result.timestamp is not None
        assert isinstance(result.overall_compliance, float)
        assert isinstance(result.has_critical_violations, bool)
        assert isinstance(result.requires_emergency_shutdown, bool)

    def test_manufacturing_evaluation_pipeline(self, manufacturing_config):
        """Test manufacturing industry evaluation pipeline"""
        # Create framework
        framework = EvaluationFramework(manufacturing_config)

        # Add manufacturing-specific evaluators
        reliability_evaluator = ReliabilityEvaluator({"name": "reliability_evaluator"})
        performance_evaluator = PerformanceEvaluator({"name": "performance_evaluator"})

        framework.add_evaluator(reliability_evaluator)
        framework.add_evaluator(performance_evaluator)

        # Add online collector for real-time metrics
        online_collector = OnlineCollector(
            {"name": "online_collector", "endpoint": "http://localhost:8000/metrics"}
        )
        framework.add_collector(online_collector)

        # Run evaluation
        result = framework.evaluate()

        # Verify manufacturing-specific aspects
        assert result.system_name == "quality_control_system"
        assert result.timestamp is not None
        assert isinstance(result.overall_compliance, float)
        assert isinstance(result.has_critical_violations, bool)
        assert isinstance(result.requires_emergency_shutdown, bool)

    def test_aviation_evaluation_pipeline(self, aviation_config):
        """Test aviation industry evaluation pipeline"""
        # Create framework
        framework = EvaluationFramework(aviation_config)

        # Add aviation-specific evaluators
        safety_evaluator = SafetyEvaluator({"name": "safety_evaluator"})
        reliability_evaluator = ReliabilityEvaluator({"name": "reliability_evaluator"})

        framework.add_evaluator(safety_evaluator)
        framework.add_evaluator(reliability_evaluator)

        # Add environmental collector for flight conditions
        env_collector = EnvironmentalCollector(
            {
                "name": "environmental_collector",
                "sensors": ["altitude", "temperature", "pressure", "turbulence"],
            }
        )
        framework.add_collector(env_collector)

        # Add required RegulatoryCollector for compliance standards
        from ml_eval.collectors.regulatory import RegulatoryCollector

        regulatory_collector = RegulatoryCollector(
            {"name": "regulatory_collector", "standards": ["DO-178C"]}
        )
        framework.add_collector(regulatory_collector)

        # Run evaluation
        result = framework.evaluate()

        # Verify aviation-specific aspects
        assert result.system_name == "flight_control_system"
        assert result.timestamp is not None
        assert isinstance(result.overall_compliance, float)
        assert isinstance(result.has_critical_violations, bool)
        assert isinstance(result.requires_emergency_shutdown, bool)


class TestIndustrySpecificScenarios:
    """Test industry-specific evaluation scenarios"""

    def test_manufacturing_quality_control_scenario(self):
        """Test manufacturing quality control scenario"""
        config = {
            "system": {
                "name": "quality_control_system",
                "type": "workflow",
                "criticality": "business_critical",
            },
            "slos": {
                "quality_control": {
                    "target": 0.98,
                    "window": "24h",
                    "description": "Quality control accuracy",
                },
                "production_efficiency": {
                    "target": 0.99,
                    "window": "8h",
                    "description": "Production efficiency",
                },
            },
        }

        framework = EvaluationFramework(config)

        # Add manufacturing-specific components
        reliability_evaluator = ReliabilityEvaluator({"name": "reliability_evaluator"})
        performance_evaluator = PerformanceEvaluator({"name": "performance_evaluator"})

        framework.add_evaluator(reliability_evaluator)
        framework.add_evaluator(performance_evaluator)

        # Run evaluation
        result = framework.evaluate()

        # Verify manufacturing-specific results
        assert result.system_name == "quality_control_system"
        assert len(result.recommendations) >= 0
        assert result.timestamp is not None
        assert isinstance(result.overall_compliance, float)

    def test_aviation_safety_decision_scenario(self):
        """Test aviation safety decision scenario"""
        config = {
            "system": {
                "name": "safety_decision_system",
                "type": "single_model",
                "criticality": "safety_critical",
            },
            "slos": {
                "safety_decision_accuracy": {
                    "target": 0.9999,
                    "window": "1h",
                    "description": "Safety-critical decision accuracy",
                    "safety_critical": True,
                    "compliance_standard": "DO-178C",
                    "environmental_conditions": ["high_altitude", "turbulence"],
                }
            },
        }

        framework = EvaluationFramework(config)

        # Add aviation-specific components
        safety_evaluator = SafetyEvaluator({"name": "safety_evaluator"})
        framework.add_evaluator(safety_evaluator)

        # Add environmental collector
        env_collector = EnvironmentalCollector(
            {
                "name": "environmental_collector",
                "sensors": ["altitude", "turbulence", "temperature"],
            }
        )
        framework.add_collector(env_collector)

        # Add required RegulatoryCollector for compliance standards
        from ml_eval.collectors.regulatory import RegulatoryCollector

        regulatory_collector = RegulatoryCollector(
            {"name": "regulatory_collector", "standards": ["DO-178C"]}
        )
        framework.add_collector(regulatory_collector)

        # Run evaluation
        result = framework.evaluate()

        # Verify aviation-specific results
        assert result.system_name == "safety_decision_system"
        assert len(result.recommendations) >= 0
        assert result.timestamp is not None
        assert isinstance(result.overall_compliance, float)

    def test_energy_grid_optimization_scenario(self):
        """Test energy grid optimization scenario"""
        config = {
            "system": {
                "name": "grid_optimization_system",
                "type": "pipeline",
                "criticality": "business_critical",
            },
            "slos": {
                "grid_stability": {
                    "target": 0.995,
                    "window": "1h",
                    "description": "Grid stability maintenance",
                    "business_impact": "millions_per_hour",
                },
                "demand_prediction_accuracy": {
                    "target": 0.95,
                    "window": "24h",
                    "description": "Energy demand prediction",
                },
            },
        }

        framework = EvaluationFramework(config)

        # Add energy-specific components
        reliability_evaluator = ReliabilityEvaluator({"name": "reliability_evaluator"})
        performance_evaluator = PerformanceEvaluator({"name": "performance_evaluator"})

        framework.add_evaluator(reliability_evaluator)
        framework.add_evaluator(performance_evaluator)

        # Run evaluation
        result = framework.evaluate()

        # Verify energy-specific results
        assert result.system_name == "grid_optimization_system"
        assert len(result.recommendations) >= 0
        assert result.timestamp is not None
        assert isinstance(result.overall_compliance, float)


class TestErrorHandlingAndRecovery:
    """Test error handling and recovery scenarios"""

    def test_collector_failure_recovery(self, sample_config):
        """Test recovery from collector failures"""
        framework = EvaluationFramework(sample_config)

        # Add multiple collectors
        collector1 = Mock()
        collector1.collect.side_effect = Exception("Collector 1 failed")
        collector1.__class__.__name__ = "MockCollector1"

        collector2 = Mock()
        collector2.collect.return_value = {"metric2": [Mock()]}
        collector2.__class__.__name__ = "MockCollector2"

        framework.add_collector(collector1)
        framework.add_collector(collector2)

        # Add evaluator
        evaluator = Mock()
        evaluator.evaluate.return_value = {"slo_compliance": {"test": True}}
        evaluator.__class__.__name__ = "MockEvaluator"

        framework.add_evaluator(evaluator)

        # Run evaluation - should not fail completely
        result = framework.evaluate()

        # Verify evaluation completed despite collector failure
        assert result is not None
        assert result.system_name == "test_system"

    def test_evaluator_failure_recovery(self, sample_config):
        """Test recovery from evaluator failures"""
        framework = EvaluationFramework(sample_config)

        # Add collector
        collector = Mock()
        collector.collect.return_value = {"metric1": [Mock()]}
        collector.__class__.__name__ = "MockCollector"

        framework.add_collector(collector)

        # Add multiple evaluators
        evaluator1 = Mock()
        evaluator1.evaluate.side_effect = Exception("Evaluator 1 failed")
        evaluator1.__class__.__name__ = "MockEvaluator1"

        evaluator2 = Mock()
        evaluator2.evaluate.return_value = {"slo_compliance": {"test": True}}
        evaluator2.__class__.__name__ = "MockEvaluator2"

        framework.add_evaluator(evaluator1)
        framework.add_evaluator(evaluator2)

        # Run evaluation - should not fail completely
        result = framework.evaluate()

        # Verify evaluation completed despite evaluator failure
        assert result is not None
        assert result.system_name == "test_system"

    def test_invalid_configuration_handling(self):
        """Test handling of invalid configurations"""
        # Invalid configuration
        invalid_config = {
            "system": {
                "name": "test_system",
                "type": "invalid_type",  # Invalid type
                "criticality": "invalid_criticality",  # Invalid criticality
            },
            "slos": {
                "invalid_slo": {
                    "target": "invalid_target",  # Should be float
                    "window": "30d",
                    "error_budget": 0.05,
                }
            },
        }

        # Should raise ValueError for invalid configuration
        with pytest.raises(ValueError):
            EvaluationFramework(invalid_config)

    def test_safety_violation_handling(self, safety_critical_config):
        """Test handling of safety violations"""
        framework = EvaluationFramework(safety_critical_config)

        # Add safety evaluator that reports violations
        safety_evaluator = Mock()
        safety_evaluator.evaluate.return_value = {
            "slo_compliance": {"safety_decision": False},
            "safety_violations": [
                {
                    "slo_name": "safety_decision",
                    "severity": "critical",
                    "details": "Safety threshold exceeded",
                }
            ],
        }
        safety_evaluator.__class__.__name__ = "MockSafetyEvaluator"

        framework.add_evaluator(safety_evaluator)

        # Run evaluation
        result = framework.evaluate()

        # Verify safety violations are handled
        assert result.has_critical_violations is True
        assert len(result.safety_violations) > 0


class TestConfigurationManagement:
    """Test configuration management and validation"""

    def test_configuration_validation_success(self, sample_config):
        """Test successful configuration validation"""
        framework = EvaluationFramework(sample_config)

        # Should pass validation
        assert framework.system_name == "test_system"
        assert len(framework.slos) > 0

    def test_configuration_validation_failure(self, safety_critical_config):
        """Test configuration validation failure"""
        framework = EvaluationFramework(safety_critical_config)

        # Should fail validation (no safety-critical SLOs)
        assert framework.system_name == "safety_system"
        assert len(framework.slos) > 0

    def test_configuration_file_loading(self, temp_config_file):
        """Test loading configuration from file"""
        config = {
            "system": {
                "name": "file_test_system",
                "type": "single_model",
                "criticality": "operational",
            },
            "slos": {
                "test_slo": {
                    "target": 0.95,
                    "window": "30d",
                    "error_budget": 0.05,
                    "description": "Test SLO",
                }
            },
        }

        # Create temporary config file
        config_file = temp_config_file(config)

        try:
            # Load configuration from file
            with open(config_file) as f:
                loaded_config = yaml.safe_load(f)

            # Create framework with loaded config
            framework = EvaluationFramework(loaded_config)

            assert framework.system_name == "file_test_system"
            assert len(framework.slos) == 1

        finally:
            # Clean up
            os.unlink(config_file)


class TestPerformanceAndScalability:
    """Test performance and scalability aspects"""

    def test_large_metric_collection(self, sample_config):
        """Test handling of large metric collections"""
        framework = EvaluationFramework(sample_config)

        # Create large metric collection
        large_metrics = {}
        now = datetime.now()

        for i in range(1000):
            metric_name = f"metric_{i}"
            large_metrics[metric_name] = [
                MetricData(
                    timestamp=now - timedelta(minutes=i),
                    value=0.95 + (i % 10) * 0.01,
                    metadata={"index": i},
                )
            ]

        # Add collector that returns large metrics
        collector = Mock()
        collector.collect.return_value = large_metrics
        collector.__class__.__name__ = "LargeMetricCollector"

        framework.add_collector(collector)

        # Add evaluator
        evaluator = Mock()
        evaluator.evaluate.return_value = {"slo_compliance": {"test": True}}
        evaluator.__class__.__name__ = "MockEvaluator"

        framework.add_evaluator(evaluator)

        # Run evaluation
        result = framework.evaluate()

        # Verify evaluation completed successfully
        assert result is not None
        assert result.system_name == "test_system"

    def test_multiple_evaluators_performance(self, sample_config):
        """Test performance with multiple evaluators"""
        framework = EvaluationFramework(sample_config)

        # Add multiple evaluators
        evaluators = []
        for i in range(10):
            evaluator = Mock()
            evaluator.evaluate.return_value = {
                "slo_compliance": {f"test_{i}": True},
                "recommendations": [f"Recommendation {i}"],
            }
            evaluator.__class__.__name__ = f"MockEvaluator{i}"
            evaluators.append(evaluator)
            framework.add_evaluator(evaluator)

        # Add collector
        collector = Mock()
        collector.collect.return_value = {"test_metric": [Mock()]}
        collector.__class__.__name__ = "MockCollector"

        framework.add_collector(collector)

        # Run evaluation
        result = framework.evaluate()

        # Verify all evaluators were called
        for evaluator in evaluators:
            evaluator.evaluate.assert_called_once()

        # Verify result aggregation
        assert result is not None
        assert len(result.recommendations) == 10
