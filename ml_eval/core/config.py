"""Configuration types and structures for ML Systems Evaluation Framework"""

from datetime import datetime
from typing import Any, Dict, List, Optional


class MetricData:
    """Data structure for metric measurements"""

    def __init__(
        self,
        timestamp: datetime,
        value: float,
        metadata: Optional[Dict[str, Any]] = None,
        environmental_conditions: Optional[Dict[str, Any]] = None,
        compliance_info: Optional[Dict[str, Any]] = None,
    ):
        self.timestamp = timestamp
        self.value = value
        self.metadata = metadata or {}
        self.environmental_conditions = environmental_conditions or {}
        self.compliance_info = compliance_info or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "metadata": self.metadata,
            "environmental_conditions": self.environmental_conditions,
            "compliance_info": self.compliance_info,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MetricData":
        """Create MetricData from dictionary"""
        timestamp = datetime.fromisoformat(data["timestamp"])
        return cls(
            timestamp=timestamp,
            value=data["value"],
            metadata=data.get("metadata", {}),
            environmental_conditions=data.get("environmental_conditions", {}),
            compliance_info=data.get("compliance_info", {}),
        )


class SystemConfig:
    """Configuration for ML system under evaluation"""

    def __init__(
        self,
        name: str,
        system_type: str = "single_model",
        criticality: str = "operational",
        description: Optional[str] = None,
        industry: Optional[str] = None,
        compliance_standards: Optional[List[str]] = None,
    ):
        self.name = name
        self.system_type = system_type
        self.criticality = criticality
        self.description = description
        self.industry = industry
        self.compliance_standards = compliance_standards or []

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "name": self.name,
            "system_type": self.system_type,
            "criticality": self.criticality,
            "description": self.description,
            "industry": self.industry,
            "compliance_standards": self.compliance_standards,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SystemConfig":
        """Create SystemConfig from dictionary"""
        return cls(
            name=data["name"],
            system_type=data.get("system_type", "single_model"),
            criticality=data.get("criticality", "operational"),
            description=data.get("description"),
            industry=data.get("industry"),
            compliance_standards=data.get("compliance_standards", []),
        )


class SLOConfig:
    """Service Level Objective configuration"""

    def __init__(
        self,
        name: str,
        target: float,
        window: str,
        error_budget: Optional[float] = None,
        description: Optional[str] = None,
        safety_critical: bool = False,
        business_impact: Optional[str] = None,
    ):
        self.name = name
        self.target = target
        self.window = window
        # Infer error_budget from target if not provided
        self.error_budget = error_budget if error_budget is not None else (1.0 - target)
        self.description = description
        self.safety_critical = safety_critical
        self.business_impact = business_impact

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "name": self.name,
            "target": self.target,
            "window": self.window,
            "error_budget": self.error_budget,
            "description": self.description,
            "safety_critical": self.safety_critical,
            "business_impact": self.business_impact,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SLOConfig":
        """Create SLOConfig from dictionary"""
        return cls(
            name=data["name"],
            target=data["target"],
            window=data["window"],
            error_budget=data.get("error_budget"),  # Optional now
            description=data.get("description"),
            safety_critical=data.get("safety_critical", False),
            business_impact=data.get("business_impact"),
        )


class EvaluationConfig:
    """Configuration for evaluation framework"""

    def __init__(
        self,
        system_config: SystemConfig,
        slos: Optional[Dict[str, SLOConfig]] = None,
        collectors: Optional[List[Dict[str, Any]]] = None,
        evaluators: Optional[List[Dict[str, Any]]] = None,
        reports: Optional[List[Dict[str, Any]]] = None,
    ):
        self.system_config = system_config
        self.slos = slos or {}
        self.collectors = collectors or []
        self.evaluators = evaluators or []
        self.reports = reports or []

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "system": self.system_config.to_dict(),
            "slos": {name: slo.to_dict() for name, slo in self.slos.items()},
            "collectors": self.collectors,
            "evaluators": self.evaluators,
            "reports": self.reports,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EvaluationConfig":
        """Create EvaluationConfig from dictionary"""
        system_config = SystemConfig.from_dict(data["system"])

        slos = {}
        for name, slo_data in data.get("slos", {}).items():
            slos[name] = SLOConfig.from_dict(slo_data)

        return cls(
            system_config=system_config,
            slos=slos,
            collectors=data.get("collectors", []),
            evaluators=data.get("evaluators", []),
            reports=data.get("reports", []),
        )


class EvaluationResult:
    def __init__(
        self,
        system_name: str,
        timestamp: datetime,
        overall_compliance: float,
        has_critical_violations: bool,
        requires_emergency_shutdown: bool,
        evaluator_results: dict,
        recommendations: list,
        alerts: list,
    ):
        self.system_name = system_name
        self.timestamp = timestamp
        self.overall_compliance = overall_compliance
        self.has_critical_violations = has_critical_violations
        self.requires_emergency_shutdown = requires_emergency_shutdown
        self.evaluator_results = evaluator_results
        self.recommendations = recommendations
        self.alerts = alerts

    def to_dict(self) -> dict:
        return {
            "system_name": self.system_name,
            "timestamp": self.timestamp.isoformat(),
            "overall_compliance": self.overall_compliance,
            "has_critical_violations": self.has_critical_violations,
            "requires_emergency_shutdown": self.requires_emergency_shutdown,
            "evaluator_results": self.evaluator_results,
            "recommendations": self.recommendations,
            "alerts": self.alerts,
        }

    @property
    def safety_violations(self):
        violations = []
        for result in self.evaluator_results.values():
            if "safety_violations" in result and result["safety_violations"]:
                violations.extend(result["safety_violations"])
        return violations


class ErrorBudget:
    def __init__(
        self, slo_name: str, budget_remaining: float, burn_rate: float, alerts=None
    ):
        self.slo_name = slo_name
        self.budget_remaining = budget_remaining
        self.burn_rate = burn_rate
        self.alerts = alerts or []

    def to_dict(self) -> dict:
        return {
            "slo_name": self.slo_name,
            "budget_remaining": self.budget_remaining,
            "burn_rate": self.burn_rate,
            "alerts": self.alerts,
        }
