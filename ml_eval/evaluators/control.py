"""Control evaluator for control system performance evaluation

This evaluator handles control system evaluation including:
- Actuator control accuracy and responsiveness
- Control system stability and performance
- Command execution accuracy and latency
- Control system safety and fault tolerance
- Feedback loop performance
"""

from datetime import datetime
from typing import Any

from .base import BaseEvaluator


class ControlEvaluator(BaseEvaluator):
    """Evaluate control system performance with actuator and feedback analysis"""

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.actuator_config = config.get("actuators", {})
        self.control_config = config.get("control", {})
        self.feedback_config = config.get("feedback", {})
        self.safety_config = config.get("safety", {})
        self.performance_thresholds = config.get("performance_thresholds", {})

    def get_required_metrics(self) -> list[str]:
        """Get required metrics for control evaluation"""
        metrics = []

        # Actuator control metrics
        for actuator_name in self.actuator_config:
            metrics.extend(
                [
                    f"{actuator_name}_control_accuracy",
                    f"{actuator_name}_response_time",
                    f"{actuator_name}_command_execution_rate",
                    f"{actuator_name}_actuator_health",
                ]
            )

        # Control system metrics
        metrics.extend(
            [
                "control_system_stability",
                "control_loop_latency_p95",
                "control_command_accuracy",
                "control_system_availability",
            ]
        )

        # Feedback metrics
        metrics.extend(
            [
                "feedback_loop_performance",
                "sensor_feedback_accuracy",
                "feedback_latency_p95",
                "feedback_consistency",
            ]
        )

        # Safety metrics
        metrics.extend(
            [
                "control_safety_margin",
                "actuator_fault_tolerance",
                "emergency_control_response",
                "control_system_redundancy",
            ]
        )

        return metrics

    def evaluate(self, metrics: dict[str, float]) -> dict[str, Any]:
        """Evaluate control metrics with comprehensive analysis"""
        if not self.validate_metrics(metrics):
            return {"error": "Missing required control metrics"}

        results: dict[str, Any] = {
            "actuator_performance": {},
            "control_system": {},
            "feedback_analysis": {},
            "safety_analysis": {},
            "overall_control_score": 0.0,
            "alerts": [],
            "recommendations": [],
        }

        # Evaluate actuator performance
        for actuator_name in self.actuator_config:
            actuator_results = self._evaluate_actuator_performance(
                actuator_name, metrics
            )
            results["actuator_performance"][actuator_name] = actuator_results

        # Evaluate control system performance
        control_results = self._evaluate_control_system(metrics)
        results["control_system"] = control_results

        # Evaluate feedback performance
        feedback_results = self._evaluate_feedback_performance(metrics)
        results["feedback_analysis"] = feedback_results

        # Evaluate safety aspects
        safety_results = self._evaluate_control_safety(metrics)
        results["safety_analysis"] = safety_results

        # Calculate overall control score
        results["overall_control_score"] = self._calculate_overall_control_score(
            results
        )

        # Generate alerts and recommendations
        results["alerts"] = self._generate_control_alerts(results)
        results["recommendations"] = self._generate_control_recommendations(results)

        return results

    def _evaluate_actuator_performance(
        self, actuator_name: str, metrics: dict[str, float]
    ) -> dict[str, Any]:
        """Evaluate performance of a specific actuator"""
        actuator_metrics = {
            "control_accuracy": metrics.get(f"{actuator_name}_control_accuracy", 0.0),
            "response_time": metrics.get(
                f"{actuator_name}_response_time", float("inf")
            ),
            "command_execution_rate": metrics.get(
                f"{actuator_name}_command_execution_rate", 0.0
            ),
            "actuator_health": metrics.get(f"{actuator_name}_actuator_health", 0.0),
        }

        # Check against thresholds
        thresholds = self.actuator_config.get(actuator_name, {}).get("thresholds", {})
        performance_status = {}

        for metric_name, value in actuator_metrics.items():
            threshold = thresholds.get(metric_name, {})
            min_value = threshold.get("min", 0.0)
            max_value = threshold.get("max", float("inf"))
            critical = threshold.get("critical", False)

            passed = min_value <= value <= max_value
            performance_status[metric_name] = {
                "value": value,
                "threshold": threshold,
                "passed": passed,
                "critical": critical,
                "timestamp": datetime.now().isoformat(),
            }

        return {
            "metrics": actuator_metrics,
            "performance_status": performance_status,
            "overall_score": self._calculate_actuator_score(
                actuator_metrics, thresholds
            ),
        }

    def _evaluate_control_system(self, metrics: dict[str, float]) -> dict[str, Any]:
        """Evaluate overall control system performance"""
        control_metrics = {
            "stability": metrics.get("control_system_stability", 0.0),
            "latency_p95": metrics.get("control_loop_latency_p95", float("inf")),
            "command_accuracy": metrics.get("control_command_accuracy", 0.0),
            "availability": metrics.get("control_system_availability", 0.0),
        }

        # Check against thresholds
        thresholds = self.control_config.get("thresholds", {})
        performance_status = {}

        for metric_name, value in control_metrics.items():
            threshold = thresholds.get(metric_name, {})
            min_value = threshold.get("min", 0.0)
            max_value = threshold.get("max", float("inf"))
            critical = threshold.get("critical", False)

            passed = min_value <= value <= max_value
            performance_status[metric_name] = {
                "value": value,
                "threshold": threshold,
                "passed": passed,
                "critical": critical,
                "timestamp": datetime.now().isoformat(),
            }

        return {
            "metrics": control_metrics,
            "performance_status": performance_status,
            "overall_score": self._calculate_control_system_score(
                control_metrics, thresholds
            ),
        }

    def _evaluate_feedback_performance(
        self, metrics: dict[str, float]
    ) -> dict[str, Any]:
        """Evaluate feedback loop performance"""
        feedback_metrics = {
            "loop_performance": metrics.get("feedback_loop_performance", 0.0),
            "sensor_accuracy": metrics.get("sensor_feedback_accuracy", 0.0),
            "latency_p95": metrics.get("feedback_latency_p95", float("inf")),
            "consistency": metrics.get("feedback_consistency", 0.0),
        }

        # Check against thresholds
        thresholds = self.feedback_config.get("thresholds", {})
        performance_status = {}

        for metric_name, value in feedback_metrics.items():
            threshold = thresholds.get(metric_name, {})
            min_value = threshold.get("min", 0.0)
            max_value = threshold.get("max", float("inf"))
            critical = threshold.get("critical", False)

            passed = min_value <= value <= max_value
            performance_status[metric_name] = {
                "value": value,
                "threshold": threshold,
                "passed": passed,
                "critical": critical,
                "timestamp": datetime.now().isoformat(),
            }

        return {
            "metrics": feedback_metrics,
            "performance_status": performance_status,
            "overall_score": self._calculate_feedback_score(
                feedback_metrics, thresholds
            ),
        }

    def _evaluate_control_safety(self, metrics: dict[str, float]) -> dict[str, Any]:
        """Evaluate safety aspects of control system"""
        safety_metrics = {
            "safety_margin": metrics.get("control_safety_margin", 0.0),
            "fault_tolerance": metrics.get("actuator_fault_tolerance", 0.0),
            "emergency_response": metrics.get("emergency_control_response", 0.0),
            "redundancy": metrics.get("control_system_redundancy", 0.0),
        }

        # Check against thresholds
        thresholds = self.safety_config.get("thresholds", {})
        performance_status = {}

        for metric_name, value in safety_metrics.items():
            threshold = thresholds.get(metric_name, {})
            min_value = threshold.get("min", 0.0)
            max_value = threshold.get("max", float("inf"))
            critical = threshold.get(
                "critical", True
            )  # Safety metrics are critical by default

            passed = min_value <= value <= max_value
            performance_status[metric_name] = {
                "value": value,
                "threshold": threshold,
                "passed": passed,
                "critical": critical,
                "timestamp": datetime.now().isoformat(),
            }

        return {
            "metrics": safety_metrics,
            "performance_status": performance_status,
            "overall_score": self._calculate_control_safety_score(
                safety_metrics, thresholds
            ),
        }

    def _calculate_actuator_score(
        self, metrics: dict[str, float], thresholds: dict[str, Any]
    ) -> float:
        """Calculate actuator performance score"""
        weights = {
            "control_accuracy": 0.3,
            "response_time": 0.3,
            "command_execution_rate": 0.2,
            "actuator_health": 0.2,
        }

        score = 0.0
        for metric_name, weight in weights.items():
            if metric_name in metrics:
                value = metrics[metric_name]
                threshold = thresholds.get(metric_name, {})
                max_value = threshold.get("max", 1.0)
                min_value = threshold.get("min", 0.0)

                # Normalize score based on threshold
                if max_value > min_value:
                    normalized_score = (value - min_value) / (max_value - min_value)
                    score += normalized_score * weight

        return min(score, 1.0)

    def _calculate_control_system_score(
        self, metrics: dict[str, float], thresholds: dict[str, Any]
    ) -> float:
        """Calculate control system performance score"""
        weights = {
            "stability": 0.3,
            "latency_p95": 0.3,
            "command_accuracy": 0.2,
            "availability": 0.2,
        }

        score = 0.0
        for metric_name, weight in weights.items():
            if metric_name in metrics:
                value = metrics[metric_name]
                threshold = thresholds.get(metric_name, {})
                max_value = threshold.get("max", 1.0)
                min_value = threshold.get("min", 0.0)

                # Normalize score based on threshold
                if max_value > min_value:
                    normalized_score = (value - min_value) / (max_value - min_value)
                    score += normalized_score * weight

        return min(score, 1.0)

    def _calculate_feedback_score(
        self, metrics: dict[str, float], thresholds: dict[str, Any]
    ) -> float:
        """Calculate feedback performance score"""
        weights = {
            "loop_performance": 0.3,
            "sensor_accuracy": 0.3,
            "latency_p95": 0.2,
            "consistency": 0.2,
        }

        score = 0.0
        for metric_name, weight in weights.items():
            if metric_name in metrics:
                value = metrics[metric_name]
                threshold = thresholds.get(metric_name, {})
                max_value = threshold.get("max", 1.0)
                min_value = threshold.get("min", 0.0)

                # Normalize score based on threshold
                if max_value > min_value:
                    normalized_score = (value - min_value) / (max_value - min_value)
                    score += normalized_score * weight

        return min(score, 1.0)

    def _calculate_control_safety_score(
        self, metrics: dict[str, float], thresholds: dict[str, Any]
    ) -> float:
        """Calculate control safety score"""
        weights = {
            "safety_margin": 0.3,
            "fault_tolerance": 0.3,
            "emergency_response": 0.2,
            "redundancy": 0.2,
        }

        score = 0.0
        for metric_name, weight in weights.items():
            if metric_name in metrics:
                value = metrics[metric_name]
                threshold = thresholds.get(metric_name, {})
                max_value = threshold.get("max", 1.0)
                min_value = threshold.get("min", 0.0)

                # Normalize score based on threshold
                if max_value > min_value:
                    normalized_score = (value - min_value) / (max_value - min_value)
                    score += normalized_score * weight

        return min(score, 1.0)

    def _calculate_overall_control_score(self, results: dict[str, Any]) -> float:
        """Calculate overall control score"""
        # Calculate average actuator score
        actuator_scores = []
        for actuator_results in results.get("actuator_performance", {}).values():
            if "overall_score" in actuator_results:
                actuator_scores.append(actuator_results["overall_score"])

        avg_actuator_score = (
            sum(actuator_scores) / len(actuator_scores) if actuator_scores else 0.0
        )

        # Get other component scores
        control_score = results.get("control_system", {}).get("overall_score", 0.0)
        feedback_score = results.get("feedback_analysis", {}).get("overall_score", 0.0)
        safety_score = results.get("safety_analysis", {}).get("overall_score", 0.0)

        # Weighted average
        weights = {"actuator": 0.3, "control": 0.3, "feedback": 0.2, "safety": 0.2}

        overall_score = (
            avg_actuator_score * weights["actuator"]
            + control_score * weights["control"]
            + feedback_score * weights["feedback"]
            + safety_score * weights["safety"]
        )

        return min(overall_score, 1.0)

    def _generate_control_alerts(self, results: dict[str, Any]) -> list[str]:
        """Generate alerts for control issues"""
        alerts = []

        # Check actuator performance
        for actuator_name, actuator_results in results.get(
            "actuator_performance", {}
        ).items():
            for metric_name, status in actuator_results.get(
                "performance_status", {}
            ).items():
                if not status.get("passed", True) and status.get("critical", False):
                    alerts.append(f"Critical {actuator_name} {metric_name} violation")

        # Check control system
        for metric_name, status in (
            results.get("control_system", {}).get("performance_status", {}).items()
        ):
            if not status.get("passed", True) and status.get("critical", False):
                alerts.append(f"Critical control system {metric_name} violation")

        # Check feedback
        for metric_name, status in (
            results.get("feedback_analysis", {}).get("performance_status", {}).items()
        ):
            if not status.get("passed", True) and status.get("critical", False):
                alerts.append(f"Critical feedback {metric_name} violation")

        # Check safety (all safety violations are critical)
        for metric_name, status in (
            results.get("safety_analysis", {}).get("performance_status", {}).items()
        ):
            if not status.get("passed", True):
                alerts.append(f"Control safety violation: {metric_name}")

        return alerts

    def _generate_control_recommendations(self, results: dict[str, Any]) -> list[str]:
        """Generate recommendations for control improvements"""
        recommendations = []

        # Analyze actuator performance
        for actuator_name, actuator_results in results.get(
            "actuator_performance", {}
        ).items():
            score = actuator_results.get("overall_score", 0.0)
            if score < 0.8:
                recommendations.append(
                    f"Improve {actuator_name} performance - current score: {score:.2f}"
                )

        # Analyze control system
        control_score = results.get("control_system", {}).get("overall_score", 0.0)
        if control_score < 0.8:
            recommendations.append(
                f"Improve control system performance - current score: {control_score:.2f}"
            )

        # Analyze feedback
        feedback_score = results.get("feedback_analysis", {}).get("overall_score", 0.0)
        if feedback_score < 0.8:
            recommendations.append(
                f"Improve feedback performance - current score: {feedback_score:.2f}"
            )

        # Analyze safety
        safety_score = results.get("safety_analysis", {}).get("overall_score", 0.0)
        if safety_score < 0.9:  # Higher threshold for safety
            recommendations.append(
                f"Improve control safety - current score: {safety_score:.2f}"
            )

        return recommendations
