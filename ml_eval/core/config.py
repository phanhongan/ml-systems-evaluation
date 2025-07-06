"""Configuration classes for ML Systems Evaluation Framework"""

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

    def __post_init__(self):
        """Validate SLO configuration for industrial systems"""
        if self.safety_critical and self.error_budget > 0.001:
            raise ValueError(
                f"Safety-critical SLO '{self.name}' must have error budget <= 0.001"
            )
        
        if self.compliance_standard and self.compliance_standard not in [
            "DO-178C", "ISO-26262", "IEC-61508", "FDA-510K", "SOX", "GDPR"
        ]:
            raise ValueError(f"Unsupported compliance standard: {self.compliance_standard}")


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

    def add_alert(self, message: str, level: str = "warning"):
        """Add an alert with severity level"""
        self.alerts.append(f"[{level.upper()}] {message}")
        
        if level == "critical":
            if "safety" in message.lower():
                self.safety_violation = True
            elif "compliance" in message.lower() or "regulatory" in message.lower():
                self.regulatory_violation = True


@dataclass
class MetricData:
    """Container for metric data with industrial context"""

    timestamp: datetime
    value: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    environmental_conditions: Optional[Dict[str, Any]] = None
    compliance_context: Optional[Dict[str, Any]] = None


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

    def add_safety_violation(self, slo_name: str, details: Dict[str, Any]):
        """Add a safety violation with details"""
        violation = {
            "slo_name": slo_name,
            "timestamp": self.evaluation_time,
            "details": details,
            "severity": "critical"
        }
        self.safety_violations.append(violation)

    def add_regulatory_violation(self, slo_name: str, standard: str, details: Dict[str, Any]):
        """Add a regulatory violation with compliance details"""
        violation = {
            "slo_name": slo_name,
            "compliance_standard": standard,
            "timestamp": self.evaluation_time,
            "details": details,
            "severity": "critical"
        }
        self.regulatory_violations.append(violation)

    def add_environmental_alert(self, condition: str, details: Dict[str, Any]):
        """Add an environmental condition alert"""
        alert = {
            "condition": condition,
            "timestamp": self.evaluation_time,
            "details": details
        }
        self.environmental_alerts.append(alert) 