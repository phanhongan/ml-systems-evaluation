"""Abstract reporting interfaces"""

from abc import ABC, abstractmethod
from typing import Dict, Any

from .core import EvaluationResult


class BaseReport(ABC):
    """Abstract base for all reports"""

    def __init__(self, evaluation_result: EvaluationResult):
        self.result = evaluation_result

    @abstractmethod
    def generate(self) -> str:
        """Generate report content"""
        pass

    @abstractmethod
    def export(self, format_type: str) -> Dict[str, Any]:
        """Export report in specified format"""
        pass


class ReliabilityReport(BaseReport):
    """SRE-focused reliability report"""

    def generate(self) -> str:
        """Generate human-readable reliability report"""
        sections = [
            self._header(),
            self._slo_summary(),
            self._error_budget_status(),
            self._incident_summary(),
            self._recommendations(),
        ]
        return "\n\n".join(sections)

    def export(self, format_type: str) -> Dict[str, Any]:
        """Export in JSON/YAML format"""
        return {
            "system": self.result.system_name,
            "timestamp": self.result.evaluation_time.isoformat(),
            "slo_compliance": self.result.slo_compliance,
            "error_budgets": {
                name: budget.__dict__
                for name, budget in self.result.error_budgets.items()
            },
            "incidents": self.result.incidents,
            "recommendations": self.result.recommendations,
        }

    def _header(self) -> str:
        """Generate report header"""
        return f"# Reliability Report: {self.result.system_name}\nGenerated: {self.result.evaluation_time}"

    def _slo_summary(self) -> str:
        """Generate SLO compliance summary"""
        total = len(self.result.slo_compliance)
        passed = sum(
            1 for compliant in self.result.slo_compliance.values() if compliant
        )
        return f"## SLO Compliance\nOverall: {passed}/{total} ({passed/total*100:.1f}%)"

    def _error_budget_status(self) -> str:
        """Generate error budget status"""
        lines = ["## Error Budget Status"]
        for name, budget in self.result.error_budgets.items():
            status = "🔴 CRITICAL" if budget.is_exhausted else "🟢 HEALTHY"
            lines.append(
                f"- {name}: {budget.budget_remaining*100:.1f}% remaining {status}"
            )
        return "\n".join(lines)

    def _incident_summary(self) -> str:
        """Generate incident summary"""
        if not self.result.incidents:
            return "## Incidents\nNo incidents detected"

        lines = ["## Incidents"]
        for incident in self.result.incidents:
            lines.append(
                f"- {incident.get('type', 'Unknown')}: {incident.get('severity', 'Unknown')}"
            )
        return "\n".join(lines)

    def _recommendations(self) -> str:
        """Generate recommendations"""
        if not self.result.recommendations:
            return "## Recommendations\nNo recommendations"

        lines = ["## Recommendations"]
        for rec in self.result.recommendations:
            lines.append(f"- {rec}")
        return "\n".join(lines)
