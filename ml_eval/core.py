"""Core framework abstractions"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

import logging


@dataclass
class SLOConfig:
    """Service Level Objective configuration for Industrial AI systems"""

    name: str
    target: float
    window: str
    error_budget: float
    description: str = ""
    compliance_standard: Optional[str] = None  # DO-178C, FDA, etc.
    safety_critical: bool = False  # Zero tolerance for failures
    business_impact: Optional[str] = None  # "catastrophic", "millions_per_hour", etc.
    environmental_conditions: Optional[List[str]] = None  # ["high_pressure", "salt_water"]


@dataclass
class ErrorBudget:
    """Error budget tracking for Industrial AI systems with safety-critical considerations"""

    slo_name: str
    budget_remaining: float
    burn_rate: float
    alerts: List[str] = field(default_factory=list)
    safety_violation: bool = False  # True if safety-critical SLO is violated
    regulatory_violation: bool = False  # True if compliance standard is violated
    business_impact_level: Optional[str] = None  # Severity of business impact

    @property
    def is_exhausted(self) -> bool:
        return self.budget_remaining <= 0

    @property
    def requires_immediate_action(self) -> bool:
        """Check if immediate action is required (safety or regulatory violation)"""
        return self.safety_violation or self.regulatory_violation or self.is_exhausted


@dataclass
class MetricData:
    """Container for metric data"""

    timestamp: datetime
    value: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationResult:
    """Result of an evaluation run for Industrial AI systems"""

    system_name: str
    evaluation_time: datetime
    slo_compliance: Dict[str, bool]
    error_budgets: Dict[str, ErrorBudget]
    incidents: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    safety_violations: List[Dict[str, Any]] = field(default_factory=list)
    regulatory_violations: List[Dict[str, Any]] = field(default_factory=list)
    environmental_alerts: List[Dict[str, Any]] = field(default_factory=list)
    business_impact_assessment: Dict[str, Any] = field(default_factory=dict)

    @property
    def has_critical_violations(self) -> bool:
        """Check if any safety or regulatory violations exist"""
        return bool(self.safety_violations or self.regulatory_violations)

    @property
    def requires_emergency_shutdown(self) -> bool:
        """Check if emergency shutdown is required"""
        return any(
            budget.requires_immediate_action 
            for budget in self.error_budgets.values()
        )


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
        """Parse SLO configuration into objects for Industrial AI systems"""
        return [
            SLOConfig(
                name=name,
                target=config.get("target", 0.95),
                window=config.get("window", "30d"),
                error_budget=config.get("error_budget", 0.05),
                description=config.get("description", ""),
                compliance_standard=config.get("compliance_standard"),
                safety_critical=config.get("safety_critical", False),
                business_impact=config.get("business_impact"),
                environmental_conditions=config.get("environmental_conditions"),
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
        """Build final evaluation result for Industrial AI systems"""
        # Aggregate results from all evaluators
        slo_compliance = {}
        error_budgets = {}
        incidents = []
        recommendations = []
        safety_violations = []
        regulatory_violations = []
        environmental_alerts = []
        business_impact_assessment = {}

        for result in evaluation_results:
            slo_compliance.update(result.get("slo_compliance", {}))
            error_budgets.update(result.get("error_budgets", {}))
            incidents.extend(result.get("incidents", []))
            recommendations.extend(result.get("recommendations", []))
            
            # Industrial AI specific aggregations
            safety_violations.extend(result.get("safety_violations", []))
            regulatory_violations.extend(result.get("regulatory_violations", []))
            environmental_alerts.extend(result.get("environmental_alerts", []))
            
            # Merge business impact assessments
            business_impact_assessment.update(result.get("business_impact_assessment", {}))

        return EvaluationResult(
            system_name=self.system_name,
            evaluation_time=datetime.now(),
            slo_compliance=slo_compliance,
            error_budgets=error_budgets,
            incidents=incidents,
            recommendations=recommendations,
            safety_violations=safety_violations,
            regulatory_violations=regulatory_violations,
            environmental_alerts=environmental_alerts,
            business_impact_assessment=business_impact_assessment,
        )
