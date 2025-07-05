"""Core framework abstractions"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

import logging


@dataclass
class SLOConfig:
    """Service Level Objective configuration"""

    name: str
    target: float
    window: str
    error_budget: float
    description: str = ""


@dataclass
class ErrorBudget:
    """Error budget tracking for SRE principles"""

    slo_name: str
    budget_remaining: float
    burn_rate: float
    alerts: List[str] = field(default_factory=list)

    @property
    def is_exhausted(self) -> bool:
        return self.budget_remaining <= 0


@dataclass
class MetricData:
    """Container for metric data"""

    timestamp: datetime
    value: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationResult:
    """Result of an evaluation run"""

    system_name: str
    evaluation_time: datetime
    slo_compliance: Dict[str, bool]
    error_budgets: Dict[str, ErrorBudget]
    incidents: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


class EvaluationFramework:
    """Main framework orchestrating evaluation process"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.system_name = config.get("system", {}).get("name", "Unknown")
        self.system_type = config.get("system", {}).get("type", "single_model")
        self.slos = self._parse_slos(config.get("slos", {}))
        self.collectors = []
        self.evaluators = []
        self.logger = logging.getLogger(__name__)

    def _parse_slos(self, slos_config: Dict[str, Any]) -> List[SLOConfig]:
        """Parse SLO configuration into objects"""
        return [
            SLOConfig(
                name=name,
                target=config.get("target", 0.95),
                window=config.get("window", "30d"),
                error_budget=config.get("error_budget", 0.05),
            )
            for name, config in slos_config.items()
        ]

    def add_collector(self, collector):
        self.collectors.append(collector)

    def add_evaluator(self, evaluator):
        self.evaluators.append(evaluator)

    def evaluate(self) -> EvaluationResult:
        """Run complete evaluation pipeline"""
        metrics = self._collect_all_metrics()
        results = self._run_all_evaluations(metrics)
        return self._build_result(results)

    def _collect_all_metrics(self) -> Dict[str, List[MetricData]]:
        """Collect metrics from all collectors"""
        all_metrics = {}
        for collector in self.collectors:
            metrics = collector.collect()
            all_metrics.update(metrics)
        return all_metrics

    def _run_all_evaluations(
        self, metrics: Dict[str, List[MetricData]]
    ) -> List[Dict[str, Any]]:
        """Run all evaluators"""
        return [evaluator.evaluate(metrics, self.slos) for evaluator in self.evaluators]

    def _build_result(
        self, evaluation_results: List[Dict[str, Any]]
    ) -> EvaluationResult:
        """Build final evaluation result"""
        # Aggregate results from all evaluators
        slo_compliance = {}
        error_budgets = {}
        incidents = []
        recommendations = []

        for result in evaluation_results:
            slo_compliance.update(result.get("slo_compliance", {}))
            error_budgets.update(result.get("error_budgets", {}))
            incidents.extend(result.get("incidents", []))
            recommendations.extend(result.get("recommendations", []))

        return EvaluationResult(
            system_name=self.system_name,
            evaluation_time=datetime.now(),
            slo_compliance=slo_compliance,
            error_budgets=error_budgets,
            incidents=incidents,
            recommendations=recommendations,
        )
