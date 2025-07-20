"""Perception evaluator for multi-modal sensor data evaluation

This evaluator handles perception system evaluation including:
- Multi-modal sensor fusion (camera, lidar, radar, etc.)
- Object detection and classification accuracy
- Sensor-specific performance metrics
- Cross-modal consistency validation
"""

from datetime import datetime
from typing import Any

from ..base import BaseEvaluator


class PerceptionEvaluator(BaseEvaluator):
    """Evaluate perception system performance with multi-modal sensor support"""

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.sensor_configs = config.get("sensors", {})
        self.fusion_config = config.get("fusion", {})
        self.detection_thresholds = config.get("detection_thresholds", {})
        self.classification_thresholds = config.get("classification_thresholds", {})
        self.consistency_thresholds = config.get("consistency_thresholds", {})

    def get_required_metrics(self) -> list[str]:
        """Get required metrics for perception evaluation"""
        metrics = []

        # Sensor-specific metrics
        for sensor_name, _sensor_config in self.sensor_configs.items():
            metrics.extend(
                [
                    f"{sensor_name}_detection_accuracy",
                    f"{sensor_name}_classification_accuracy",
                    f"{sensor_name}_false_positive_rate",
                    f"{sensor_name}_false_negative_rate",
                    f"{sensor_name}_latency_p95",
                ]
            )

        # Fusion metrics
        if self.fusion_config:
            metrics.extend(
                ["fusion_accuracy", "cross_modal_consistency", "fusion_latency_p95"]
            )

        return metrics

    def evaluate(self, metrics: dict[str, float]) -> dict[str, Any]:
        """Evaluate perception metrics with multi-modal support"""
        if not self.validate_metrics(metrics):
            return {"error": "Missing required perception metrics"}

        results: dict[str, Any] = {
            "sensor_performance": {},
            "fusion_performance": {},
            "cross_modal_analysis": {},
            "overall_perception_score": 0.0,
            "alerts": [],
            "recommendations": [],
        }

        # Evaluate individual sensor performance
        for sensor_name, sensor_config in self.sensor_configs.items():
            sensor_results = self._evaluate_sensor_performance(
                sensor_name, sensor_config, metrics
            )
            results["sensor_performance"][sensor_name] = sensor_results

        # Evaluate sensor fusion performance
        if self.fusion_config:
            fusion_results = self._evaluate_fusion_performance(metrics)
            results["fusion_performance"] = fusion_results

        # Evaluate cross-modal consistency
        if len(self.sensor_configs) > 1:
            consistency_results = self._evaluate_cross_modal_consistency(metrics)
            results["cross_modal_analysis"] = consistency_results

        # Calculate overall perception score
        results["overall_perception_score"] = self._calculate_overall_score(results)

        # Generate alerts and recommendations
        results["alerts"] = self._generate_perception_alerts(results)
        results["recommendations"] = self._generate_perception_recommendations(results)

        return results

    def _evaluate_sensor_performance(
        self, sensor_name: str, sensor_config: dict[str, Any], metrics: dict[str, float]
    ) -> dict[str, Any]:
        """Evaluate performance of a specific sensor"""
        sensor_metrics = {
            "detection_accuracy": metrics.get(f"{sensor_name}_detection_accuracy", 0.0),
            "classification_accuracy": metrics.get(
                f"{sensor_name}_classification_accuracy", 0.0
            ),
            "false_positive_rate": metrics.get(
                f"{sensor_name}_false_positive_rate", 1.0
            ),
            "false_negative_rate": metrics.get(
                f"{sensor_name}_false_negative_rate", 1.0
            ),
            "latency_p95": metrics.get(f"{sensor_name}_latency_p95", float("inf")),
        }

        # Check against thresholds
        thresholds = sensor_config.get("thresholds", {})
        performance_status = {}

        for metric_name, value in sensor_metrics.items():
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
            "metrics": sensor_metrics,
            "performance_status": performance_status,
            "overall_score": self._calculate_sensor_score(sensor_metrics, thresholds),
        }

    def _evaluate_fusion_performance(self, metrics: dict[str, float]) -> dict[str, Any]:
        """Evaluate sensor fusion performance"""
        fusion_metrics = {
            "accuracy": metrics.get("fusion_accuracy", 0.0),
            "consistency": metrics.get("cross_modal_consistency", 0.0),
            "latency_p95": metrics.get("fusion_latency_p95", float("inf")),
        }

        # Check fusion thresholds
        fusion_status = {}
        for metric_name, value in fusion_metrics.items():
            threshold = self.fusion_config.get("thresholds", {}).get(metric_name, {})
            min_value = threshold.get("min", 0.0)
            max_value = threshold.get("max", float("inf"))

            passed = min_value <= value <= max_value
            fusion_status[metric_name] = {
                "value": value,
                "threshold": threshold,
                "passed": passed,
                "timestamp": datetime.now().isoformat(),
            }

        return {
            "metrics": fusion_metrics,
            "performance_status": fusion_status,
            "overall_score": self._calculate_fusion_score(fusion_metrics),
        }

    def _evaluate_cross_modal_consistency(
        self, metrics: dict[str, float]
    ) -> dict[str, Any]:
        """Evaluate consistency across different sensor modalities"""
        consistency_metrics = {
            "cross_modal_consistency": metrics.get("cross_modal_consistency", 0.0),
            "sensor_agreement_rate": metrics.get("sensor_agreement_rate", 0.0),
            "fusion_confidence": metrics.get("fusion_confidence", 0.0),
        }

        # Check consistency thresholds
        consistency_status = {}
        for metric_name, value in consistency_metrics.items():
            threshold = self.consistency_thresholds.get(metric_name, {})
            min_value = threshold.get("min", 0.0)
            max_value = threshold.get("max", 1.0)

            passed = min_value <= value <= max_value
            consistency_status[metric_name] = {
                "value": value,
                "threshold": threshold,
                "passed": passed,
                "timestamp": datetime.now().isoformat(),
            }

        return {
            "metrics": consistency_metrics,
            "performance_status": consistency_status,
            "overall_score": self._calculate_consistency_score(consistency_metrics),
        }

    def _calculate_sensor_score(
        self, metrics: dict[str, float], thresholds: dict[str, Any]
    ) -> float:
        """Calculate overall score for a sensor"""
        weights = {
            "detection_accuracy": 0.3,
            "classification_accuracy": 0.3,
            "false_positive_rate": 0.2,
            "false_negative_rate": 0.2,
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

    def _calculate_fusion_score(self, metrics: dict[str, float]) -> float:
        """Calculate overall fusion score"""
        weights = {"accuracy": 0.5, "consistency": 0.3, "latency_p95": 0.2}

        score = 0.0
        for metric_name, weight in weights.items():
            if metric_name in metrics:
                value = metrics[metric_name]
                if metric_name == "latency_p95":
                    # Lower latency is better
                    normalized_score = max(
                        0, 1 - (value / 1000)
                    )  # Normalize to 1 second
                else:
                    normalized_score = min(value, 1.0)
                score += normalized_score * weight

        return min(score, 1.0)

    def _calculate_consistency_score(self, metrics: dict[str, float]) -> float:
        """Calculate consistency score"""
        weights = {
            "cross_modal_consistency": 0.4,
            "sensor_agreement_rate": 0.4,
            "fusion_confidence": 0.2,
        }

        score = 0.0
        for metric_name, weight in weights.items():
            if metric_name in metrics:
                value = metrics[metric_name]
                normalized_score = min(value, 1.0)
                score += normalized_score * weight

        return min(score, 1.0)

    def _calculate_overall_score(self, results: dict[str, Any]) -> float:
        """Calculate overall perception score"""
        sensor_scores = []
        for sensor_results in results.get("sensor_performance", {}).values():
            if "overall_score" in sensor_results:
                sensor_scores.append(sensor_results["overall_score"])

        fusion_score = 0.0
        if results.get("fusion_performance"):
            fusion_score = results["fusion_performance"].get("overall_score", 0.0)

        consistency_score = 0.0
        if results.get("cross_modal_analysis"):
            consistency_score = results["cross_modal_analysis"].get(
                "overall_score", 0.0
            )

        # Weighted average
        if sensor_scores:
            avg_sensor_score = sum(sensor_scores) / len(sensor_scores)
            if fusion_score > 0:
                return (
                    avg_sensor_score * 0.6
                    + fusion_score * 0.3
                    + consistency_score * 0.1
                )
            else:
                return avg_sensor_score

        return 0.0

    def _generate_perception_alerts(self, results: dict[str, Any]) -> list[str]:
        """Generate alerts for perception issues"""
        alerts = []

        # Check sensor performance
        for sensor_name, sensor_results in results.get(
            "sensor_performance", {}
        ).items():
            for metric_name, status in sensor_results.get(
                "performance_status", {}
            ).items():
                if not status.get("passed", True) and status.get("critical", False):
                    alerts.append(f"Critical {sensor_name} {metric_name} violation")

        # Check fusion performance
        if results.get("fusion_performance"):
            for metric_name, status in (
                results["fusion_performance"].get("performance_status", {}).items()
            ):
                if not status.get("passed", True):
                    alerts.append(f"Fusion {metric_name} threshold violation")

        # Check consistency
        if results.get("cross_modal_analysis"):
            for metric_name, status in (
                results["cross_modal_analysis"].get("performance_status", {}).items()
            ):
                if not status.get("passed", True):
                    alerts.append(f"Cross-modal {metric_name} threshold violation")

        return alerts

    def _generate_perception_recommendations(
        self, results: dict[str, Any]
    ) -> list[str]:
        """Generate recommendations for perception improvements"""
        recommendations = []

        # Analyze sensor performance
        for sensor_name, sensor_results in results.get(
            "sensor_performance", {}
        ).items():
            score = sensor_results.get("overall_score", 0.0)
            if score < 0.8:
                recommendations.append(
                    f"Improve {sensor_name} performance - current score: {score:.2f}"
                )

        # Analyze fusion performance
        if results.get("fusion_performance"):
            fusion_score = results["fusion_performance"].get("overall_score", 0.0)
            if fusion_score < 0.8:
                recommendations.append(
                    f"Improve sensor fusion performance - current score: {fusion_score:.2f}"
                )

        # Analyze consistency
        if results.get("cross_modal_analysis"):
            consistency_score = results["cross_modal_analysis"].get(
                "overall_score", 0.0
            )
            if consistency_score < 0.8:
                recommendations.append(
                    f"Improve cross-modal consistency - current score: {consistency_score:.2f}"
                )

        return recommendations
