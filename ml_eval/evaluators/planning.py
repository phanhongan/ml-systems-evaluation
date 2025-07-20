"""Planning evaluator for path planning and trajectory optimization evaluation

This evaluator handles planning system evaluation including:
- Path planning accuracy and efficiency
- Trajectory optimization performance
- Decision-making quality and consistency
- Planning latency and computational efficiency
- Safety margin validation
"""

from datetime import datetime
from typing import Any

from .base import BaseEvaluator


class PlanningEvaluator(BaseEvaluator):
    """Evaluate planning system performance with path and trajectory optimization"""

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.planning_config = config.get("planning", {})
        self.trajectory_config = config.get("trajectory", {})
        self.decision_config = config.get("decision", {})
        self.safety_config = config.get("safety", {})
        self.performance_thresholds = config.get("performance_thresholds", {})

    def get_required_metrics(self) -> list[str]:
        """Get required metrics for planning evaluation"""
        metrics = []

        # Path planning metrics
        metrics.extend(
            [
                "path_planning_accuracy",
                "path_planning_efficiency",
                "path_planning_latency_p95",
                "path_feasibility_rate",
            ]
        )

        # Trajectory optimization metrics
        metrics.extend(
            [
                "trajectory_smoothness",
                "trajectory_optimality",
                "trajectory_execution_rate",
                "trajectory_planning_latency_p95",
            ]
        )

        # Decision making metrics
        metrics.extend(
            [
                "decision_accuracy",
                "decision_consistency",
                "decision_latency_p95",
                "decision_confidence",
            ]
        )

        # Safety metrics
        metrics.extend(
            [
                "safety_margin_compliance",
                "collision_avoidance_rate",
                "emergency_stop_rate",
                "safety_violation_rate",
            ]
        )

        return metrics

    def evaluate(self, metrics: dict[str, float]) -> dict[str, Any]:
        """Evaluate planning metrics with comprehensive analysis"""
        if not self.validate_metrics(metrics):
            return {"error": "Missing required planning metrics"}

        results: dict[str, Any] = {
            "path_planning": {},
            "trajectory_optimization": {},
            "decision_making": {},
            "safety_analysis": {},
            "overall_planning_score": 0.0,
            "alerts": [],
            "recommendations": [],
        }

        # Evaluate path planning performance
        path_results = self._evaluate_path_planning(metrics)
        results["path_planning"] = path_results

        # Evaluate trajectory optimization
        trajectory_results = self._evaluate_trajectory_optimization(metrics)
        results["trajectory_optimization"] = trajectory_results

        # Evaluate decision making
        decision_results = self._evaluate_decision_making(metrics)
        results["decision_making"] = decision_results

        # Evaluate safety aspects
        safety_results = self._evaluate_safety_analysis(metrics)
        results["safety_analysis"] = safety_results

        # Calculate overall planning score
        results["overall_planning_score"] = self._calculate_overall_planning_score(
            results
        )

        # Generate alerts and recommendations
        results["alerts"] = self._generate_planning_alerts(results)
        results["recommendations"] = self._generate_planning_recommendations(results)

        return results

    def _evaluate_path_planning(self, metrics: dict[str, float]) -> dict[str, Any]:
        """Evaluate path planning performance"""
        path_metrics = {
            "accuracy": metrics.get("path_planning_accuracy", 0.0),
            "efficiency": metrics.get("path_planning_efficiency", 0.0),
            "latency_p95": metrics.get("path_planning_latency_p95", float("inf")),
            "feasibility_rate": metrics.get("path_feasibility_rate", 0.0),
        }

        # Check against thresholds
        thresholds = self.planning_config.get("thresholds", {})
        performance_status = {}

        for metric_name, value in path_metrics.items():
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
            "metrics": path_metrics,
            "performance_status": performance_status,
            "overall_score": self._calculate_path_planning_score(
                path_metrics, thresholds
            ),
        }

    def _evaluate_trajectory_optimization(
        self, metrics: dict[str, float]
    ) -> dict[str, Any]:
        """Evaluate trajectory optimization performance"""
        trajectory_metrics = {
            "smoothness": metrics.get("trajectory_smoothness", 0.0),
            "optimality": metrics.get("trajectory_optimality", 0.0),
            "execution_rate": metrics.get("trajectory_execution_rate", 0.0),
            "latency_p95": metrics.get("trajectory_planning_latency_p95", float("inf")),
        }

        # Check against thresholds
        thresholds = self.trajectory_config.get("thresholds", {})
        performance_status = {}

        for metric_name, value in trajectory_metrics.items():
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
            "metrics": trajectory_metrics,
            "performance_status": performance_status,
            "overall_score": self._calculate_trajectory_score(
                trajectory_metrics, thresholds
            ),
        }

    def _evaluate_decision_making(self, metrics: dict[str, float]) -> dict[str, Any]:
        """Evaluate decision making performance"""
        decision_metrics = {
            "accuracy": metrics.get("decision_accuracy", 0.0),
            "consistency": metrics.get("decision_consistency", 0.0),
            "latency_p95": metrics.get("decision_latency_p95", float("inf")),
            "confidence": metrics.get("decision_confidence", 0.0),
        }

        # Check against thresholds
        thresholds = self.decision_config.get("thresholds", {})
        performance_status = {}

        for metric_name, value in decision_metrics.items():
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
            "metrics": decision_metrics,
            "performance_status": performance_status,
            "overall_score": self._calculate_decision_score(
                decision_metrics, thresholds
            ),
        }

    def _evaluate_safety_analysis(self, metrics: dict[str, float]) -> dict[str, Any]:
        """Evaluate safety aspects of planning"""
        safety_metrics = {
            "safety_margin_compliance": metrics.get("safety_margin_compliance", 0.0),
            "collision_avoidance_rate": metrics.get("collision_avoidance_rate", 0.0),
            "emergency_stop_rate": metrics.get("emergency_stop_rate", 0.0),
            "safety_violation_rate": metrics.get("safety_violation_rate", 1.0),
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
            "overall_score": self._calculate_safety_score(safety_metrics, thresholds),
        }

    def _calculate_path_planning_score(
        self, metrics: dict[str, float], thresholds: dict[str, Any]
    ) -> float:
        """Calculate path planning score"""
        weights = {
            "accuracy": 0.3,
            "efficiency": 0.3,
            "latency_p95": 0.2,
            "feasibility_rate": 0.2,
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

    def _calculate_trajectory_score(
        self, metrics: dict[str, float], thresholds: dict[str, Any]
    ) -> float:
        """Calculate trajectory optimization score"""
        weights = {
            "smoothness": 0.3,
            "optimality": 0.3,
            "execution_rate": 0.2,
            "latency_p95": 0.2,
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

    def _calculate_decision_score(
        self, metrics: dict[str, float], thresholds: dict[str, Any]
    ) -> float:
        """Calculate decision making score"""
        weights = {
            "accuracy": 0.3,
            "consistency": 0.3,
            "latency_p95": 0.2,
            "confidence": 0.2,
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

    def _calculate_safety_score(
        self, metrics: dict[str, float], thresholds: dict[str, Any]
    ) -> float:
        """Calculate safety score"""
        weights = {
            "safety_margin_compliance": 0.3,
            "collision_avoidance_rate": 0.3,
            "emergency_stop_rate": 0.2,
            "safety_violation_rate": 0.2,
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

    def _calculate_overall_planning_score(self, results: dict[str, Any]) -> float:
        """Calculate overall planning score"""
        path_score = results.get("path_planning", {}).get("overall_score", 0.0)
        trajectory_score = results.get("trajectory_optimization", {}).get(
            "overall_score", 0.0
        )
        decision_score = results.get("decision_making", {}).get("overall_score", 0.0)
        safety_score = results.get("safety_analysis", {}).get("overall_score", 0.0)

        # Weighted average with safety having higher weight
        weights = {"path": 0.25, "trajectory": 0.25, "decision": 0.25, "safety": 0.25}

        overall_score = (
            path_score * weights["path"]
            + trajectory_score * weights["trajectory"]
            + decision_score * weights["decision"]
            + safety_score * weights["safety"]
        )

        return min(overall_score, 1.0)

    def _generate_planning_alerts(self, results: dict[str, Any]) -> list[str]:
        """Generate alerts for planning issues"""
        alerts = []

        # Check path planning
        for metric_name, status in (
            results.get("path_planning", {}).get("performance_status", {}).items()
        ):
            if not status.get("passed", True) and status.get("critical", False):
                alerts.append(f"Critical path planning {metric_name} violation")

        # Check trajectory optimization
        for metric_name, status in (
            results.get("trajectory_optimization", {})
            .get("performance_status", {})
            .items()
        ):
            if not status.get("passed", True) and status.get("critical", False):
                alerts.append(f"Critical trajectory {metric_name} violation")

        # Check decision making
        for metric_name, status in (
            results.get("decision_making", {}).get("performance_status", {}).items()
        ):
            if not status.get("passed", True) and status.get("critical", False):
                alerts.append(f"Critical decision making {metric_name} violation")

        # Check safety (all safety violations are critical)
        for metric_name, status in (
            results.get("safety_analysis", {}).get("performance_status", {}).items()
        ):
            if not status.get("passed", True):
                alerts.append(f"Safety violation: {metric_name}")

        return alerts

    def _generate_planning_recommendations(self, results: dict[str, Any]) -> list[str]:
        """Generate recommendations for planning improvements"""
        recommendations = []

        # Analyze path planning
        path_score = results.get("path_planning", {}).get("overall_score", 0.0)
        if path_score < 0.8:
            recommendations.append(
                f"Improve path planning performance - current score: {path_score:.2f}"
            )

        # Analyze trajectory optimization
        trajectory_score = results.get("trajectory_optimization", {}).get(
            "overall_score", 0.0
        )
        if trajectory_score < 0.8:
            recommendations.append(
                f"Improve trajectory optimization - current score: {trajectory_score:.2f}"
            )

        # Analyze decision making
        decision_score = results.get("decision_making", {}).get("overall_score", 0.0)
        if decision_score < 0.8:
            recommendations.append(
                f"Improve decision making performance - current score: {decision_score:.2f}"
            )

        # Analyze safety
        safety_score = results.get("safety_analysis", {}).get("overall_score", 0.0)
        if safety_score < 0.9:  # Higher threshold for safety
            recommendations.append(
                f"Improve safety performance - current score: {safety_score:.2f}"
            )

        return recommendations
