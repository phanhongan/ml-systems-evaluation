"""Performance evaluator for ML Systems Evaluation"""

from datetime import datetime
from typing import Any

from ..base import BaseEvaluator


class PerformanceEvaluator(BaseEvaluator):
    """Evaluate system performance metrics"""

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.performance_metrics = config.get("metrics", [])
        self.thresholds = config.get("thresholds", {})

    def get_required_metrics(self) -> list[str]:
        """Get required metrics for performance evaluation"""
        return self.performance_metrics

    def evaluate(self, metrics: dict[str, Any]) -> dict[str, Any]:
        """Evaluate performance metrics"""
        if not self.validate_metrics(metrics):
            return {"error": "Missing required performance metrics"}

        results: dict[str, Any] = {
            "performance_metrics": {},
            "overall_performance_score": 0.0,
            "bottlenecks": [],
            "alerts": [],
        }

        # Evaluate each performance metric
        for metric_name in self.performance_metrics:
            if metric_name in metrics:
                perf_result = self._evaluate_performance_metric(
                    metric_name, metrics[metric_name]
                )
                results["performance_metrics"][metric_name] = perf_result

        # Calculate overall performance score
        if (
            isinstance(results["performance_metrics"], dict)
            and results["performance_metrics"]
        ):
            total_score = sum(
                metric.get("score", 0)
                for metric in results["performance_metrics"].values()
                if isinstance(metric, dict)
            )
            results["overall_performance_score"] = total_score / len(
                results["performance_metrics"]
            )

        # Identify bottlenecks
        if isinstance(results["performance_metrics"], dict):
            results["bottlenecks"] = self._identify_bottlenecks(
                results["performance_metrics"]
            )
        else:
            results["bottlenecks"] = []

        # Generate alerts
        results["alerts"] = self._generate_performance_alerts(results)

        return results

    def _evaluate_performance_metric(
        self, metric_name: str, current_value: Any
    ) -> dict[str, Any]:
        """Evaluate a single performance metric"""
        # Get target from thresholds - thresholds can be direct values or dictionaries
        threshold_config = self.thresholds.get(metric_name, {})
        if isinstance(threshold_config, dict):
            target = threshold_config.get("target", 0)
        else:
            # Direct value
            target = threshold_config

        # Extract value from MetricData if it's a list
        if isinstance(current_value, list) and len(current_value) > 0:
            # Take the first MetricData object and get its value
            current_value = current_value[0].value
        elif hasattr(current_value, "value"):
            # It's a single MetricData object
            current_value = current_value.value

        # Calculate performance score (0-1)
        if "accuracy" in metric_name.lower() or "precision" in metric_name.lower():
            # Higher is better for accuracy metrics
            score = min(1.0, current_value / target) if target > 0 else 0.0
        elif "latency" in metric_name.lower() or "response_time" in metric_name.lower():
            # Lower is better for latency metrics
            score = (
                max(0.0, 1.0 - (current_value - target) / target) if target > 0 else 0.0
            )
        else:
            # Default: higher is better
            score = min(1.0, current_value / target) if target > 0 else 0.0

        # Determine status
        if score >= 0.9:
            status = "excellent"
        elif score >= 0.7:
            status = "good"
        elif score >= 0.5:
            status = "acceptable"
        else:
            status = "poor"

        return {
            "value": current_value,
            "target": target,
            "score": score,
            "status": status,
            "timestamp": datetime.now().isoformat(),
        }

    def _identify_bottlenecks(self, performance_metrics: dict[str, Any]) -> list[str]:
        """Identify performance bottlenecks"""
        bottlenecks = []

        for metric_name, metric_data in performance_metrics.items():
            score = metric_data.get("score", 0)
            if score < 0.7:  # Below 70% performance
                bottlenecks.append(
                    f"{metric_name}: {score:.2%} performance "
                    f"(target: {metric_data.get('target', 'N/A')})"
                )

        return bottlenecks

    def _generate_performance_alerts(self, results: dict[str, Any]) -> list[str]:
        """Generate performance alerts"""
        alerts = []

        # Check overall performance
        overall_score = results["overall_performance_score"]
        if overall_score < 0.8:
            alerts.append(f"Overall performance below 80%: {overall_score:.2%}")

        # Check for bottlenecks
        bottlenecks = results["bottlenecks"]
        if bottlenecks:
            alerts.append(
                f"Performance bottlenecks detected: {len(bottlenecks)} issues"
            )

        # Check individual metrics
        for metric_name, metric_data in results["performance_metrics"].items():
            score = metric_data.get("score", 0)
            if score < 0.5:
                alerts.append(
                    f"Critical performance issue: {metric_name} at {score:.2%}"
                )

        return alerts
