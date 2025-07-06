"""Main evaluation framework for Industrial AI systems"""

from datetime import datetime
from typing import Any, Dict, List

from .config import EvaluationResult, MetricData, SLOConfig
from .types import CriticalityLevel, SystemType


class EvaluationFramework:
    """Main framework orchestrating evaluation process for Industrial AI systems"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.system_name = config.get("system", {}).get("name", "Unknown")
        self.system_type = SystemType(
            config.get("system", {}).get("type", "single_model")
        )
        self.criticality = CriticalityLevel(
            config.get("system", {}).get("criticality", "operational")
        )
        self.slos = self._parse_slos(config.get("slos", {}))
        self.collectors = []
        self.evaluators = []

    def _parse_slos(self, slos_config: Dict[str, Any]) -> List[SLOConfig]:
        """Parse SLO configuration into objects for Industrial AI systems"""
        slos = []
        for name, config in slos_config.items():
            try:
                # Convert target to float, handle invalid values gracefully
                target = config.get("target", 0.95)
                if isinstance(target, str):
                    try:
                        target = float(target)
                    except ValueError:
                        continue  # Skip this SLO instead of raising

                slo = SLOConfig(
                    name=name,
                    target=target,
                    window=config.get("window", "30d"),
                    error_budget=config.get("error_budget", 0.05),
                    description=config.get("description", ""),
                    safety_critical=config.get("safety_critical", False),
                )
                slos.append(slo)
            except ValueError:
                # Continue with other SLOs instead of raising
                pass

        return slos

    def add_collector(self, collector):
        """Add a metric collector to the framework"""
        self.collectors.append(collector)

    def add_evaluator(self, evaluator):
        """Add an evaluator to the framework"""
        self.evaluators.append(evaluator)

    def evaluate(self) -> EvaluationResult:
        """Run complete evaluation pipeline for Industrial AI systems"""

        try:
            metrics = self._collect_all_metrics()
            results = self._run_all_evaluations(metrics)
            evaluation_result = self._build_result(results)

            return evaluation_result

        except Exception:
            raise

    def _collect_all_metrics(self) -> Dict[str, List[MetricData]]:
        """Collect metrics from all collectors with error handling"""
        all_metrics = {}

        for collector in self.collectors:
            try:
                metrics = collector.collect()
                all_metrics.update(metrics)
            except Exception:
                # Log error but continue with other collectors
                pass

        return all_metrics

    def _run_all_evaluations(
        self, metrics: Dict[str, List[MetricData]]
    ) -> Dict[str, Any]:
        """Run all evaluators on collected metrics"""
        results = {}

        for evaluator in self.evaluators:
            try:
                result = evaluator.evaluate(metrics)
                results[evaluator.__class__.__name__] = result
            except Exception:
                # Log error but continue with other evaluators
                pass

        return results

    def _build_result(self, results: Dict[str, Any]) -> EvaluationResult:
        """Build final evaluation result from all evaluator results"""
        # Determine overall system status
        has_critical_violations = any(
            result.get("critical_violations", False)
            or ("safety_violations" in result and result["safety_violations"])
            for result in results.values()
        )

        requires_emergency_shutdown = any(
            result.get("emergency_shutdown", False) for result in results.values()
        )

        # Calculate overall compliance score
        compliance_scores = [
            result.get("compliance_score", 0.0) for result in results.values()
        ]
        overall_compliance = (
            sum(compliance_scores) / len(compliance_scores)
            if compliance_scores
            else 0.0
        )

        # Build recommendations
        recommendations = []
        for evaluator_name, result in results.items():
            if result.get("recommendations"):
                recommendations.extend(result["recommendations"])

        # Build alerts
        alerts = []
        for evaluator_name, result in results.items():
            if result.get("alerts"):
                alerts.extend(result["alerts"])

        return EvaluationResult(
            system_name=self.system_name,
            timestamp=datetime.now(),
            overall_compliance=overall_compliance,
            has_critical_violations=has_critical_violations,
            requires_emergency_shutdown=requires_emergency_shutdown,
            evaluator_results=results,
            recommendations=recommendations,
            alerts=alerts,
        )

    def get_system_info(self) -> Dict[str, Any]:
        """Get information about the configured system"""
        return {
            "name": self.system_name,
            "type": self.system_type.value,
            "criticality": self.criticality.value,
            "slo_count": len(self.slos),
            "collector_count": len(self.collectors),
            "evaluator_count": len(self.evaluators),
        }

    def get_slo_summary(self) -> List[Dict[str, Any]]:
        """Get summary of all SLOs"""
        return [
            {
                "name": slo.name,
                "target": slo.target,
                "window": slo.window,
                "safety_critical": slo.safety_critical,
                "compliance_standard": slo.compliance_standard,
            }
            for slo in self.slos
        ]
