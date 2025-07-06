"""Reliability evaluator for ML Systems Evaluation"""

from datetime import datetime
from typing import Any, Dict, List

from .base import BaseEvaluator


class ReliabilityEvaluator(BaseEvaluator):
    """Evaluate system reliability using SLOs and error budgets"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.error_budget_window = config.get("error_budget_window", "30d")
        self.slos = config.get("slos", {})

    def get_required_metrics(self) -> List[str]:
        """Get required metrics for reliability evaluation"""
        return list(self.slos.keys())

    def evaluate(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate reliability metrics against SLOs"""
        if not self.validate_metrics(metrics):
            return {"error": "Missing required metrics"}

        results: Dict[str, Any] = {
            "slos": {},
            "error_budgets": {},
            "overall_reliability": 0.0,
            "alerts": [],
        }

        # Evaluate each SLO
        for slo_name, slo_config in self.slos.items():
            if slo_name in metrics:
                slo_result = self._evaluate_slo(slo_name, slo_config, metrics[slo_name])
                results["slos"][slo_name] = slo_result

                # Calculate error budget
                budget_result = self._calculate_error_budget(
                    slo_name, slo_config, slo_result
                )
                results["error_budgets"][slo_name] = budget_result

        # Calculate overall reliability
        if isinstance(results["slos"], dict) and results["slos"]:
            compliant_slos = sum(
                1
                for slo in results["slos"].values()
                if isinstance(slo, dict) and slo.get("compliant", False)
            )
            results["overall_reliability"] = compliant_slos / len(results["slos"])

        # Generate alerts
        results["alerts"] = self._generate_alerts(results)

        return results

    def _evaluate_slo(
        self, slo_name: str, slo_config: Dict[str, Any], current_value: float
    ) -> Dict[str, Any]:
        """Evaluate a single SLO"""
        target = slo_config.get("target", 0)
        window = slo_config.get("window", "24h")

        # Determine if SLO is met based on type
        if "accuracy" in slo_name.lower() or "precision" in slo_name.lower():
            compliant = current_value >= target
        elif "latency" in slo_name.lower() or "response_time" in slo_name.lower():
            compliant = current_value <= target
        else:
            # Default to greater than or equal
            compliant = current_value >= target

        return {
            "current_value": current_value,
            "target": target,
            "compliant": compliant,
            "window": window,
            "timestamp": datetime.now().isoformat(),
        }

    def _calculate_error_budget(
        self, slo_name: str, slo_config: Dict[str, Any], slo_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate error budget for an SLO"""
        error_budget = slo_config.get("error_budget", 0.01)
        current_value = slo_result["current_value"]
        target = slo_result["target"]

        # Calculate budget burn rate
        if slo_result["compliant"]:
            burn_rate = 0.0
        else:
            # Calculate how much budget is burned
            if "accuracy" in slo_name.lower():
                burn_rate = max(0, target - current_value) / target
            elif "latency" in slo_name.lower():
                burn_rate = max(0, current_value - target) / target
            else:
                burn_rate = max(0, target - current_value) / target

        remaining_budget = max(0, error_budget - burn_rate)
        exhausted = remaining_budget <= 0

        return {
            "remaining": remaining_budget,
            "burn_rate": burn_rate,
            "exhausted": exhausted,
            "safety_violation": slo_config.get("safety_critical", False)
            and not slo_result["compliant"],
            "regulatory_violation": slo_config.get("compliance_standard")
            and not slo_result["compliant"],
        }

    def _generate_alerts(self, results: Dict[str, Any]) -> List[str]:
        """Generate alerts based on evaluation results"""
        alerts = []

        # Check for exhausted error budgets
        for budget_name, budget_data in results["error_budgets"].items():
            if budget_data["exhausted"]:
                alerts.append(f"Error budget exhausted for {budget_name}")

        # Check for safety violations
        for budget_name, budget_data in results["error_budgets"].items():
            if budget_data["safety_violation"]:
                alerts.append(f"SAFETY VIOLATION: {budget_name} SLO not met")

        # Check for regulatory violations
        for budget_name, budget_data in results["error_budgets"].items():
            if budget_data["regulatory_violation"]:
                alerts.append(
                    f"REGULATORY VIOLATION: {budget_name} compliance standard not met"
                )

        # Check overall reliability
        if results["overall_reliability"] < 0.95:
            alerts.append(
                f"Overall reliability below 95%: {results['overall_reliability']:.2%}"
            )

        return alerts
