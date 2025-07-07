"""Reliability reports for ML Systems Evaluation"""

from datetime import datetime
from typing import Any

from .base import BaseReport, ReportData


class ReliabilityReport(BaseReport):
    """Generate reliability reports with SLO compliance and error budgets"""

    def generate(self, data: dict[str, Any]) -> ReportData:
        """Generate reliability report from evaluation data"""
        slos = data.get("slos", {})
        error_budgets = data.get("error_budgets", {})
        incidents = data.get("incidents", [])

        # Calculate summary metrics
        total_slos = len(slos)
        compliant_slos = sum(1 for slo in slos.values() if slo.get("compliant", False))
        exhausted_budgets = sum(
            1 for budget in error_budgets.values() if budget.get("exhausted", False)
        )

        summary = {
            "total_slos": total_slos,
            "compliant_slos": compliant_slos,
            "compliance_rate": compliant_slos / total_slos if total_slos > 0 else 0,
            "exhausted_budgets": exhausted_budgets,
            "total_incidents": len(incidents),
        }

        # Generate recommendations
        recommendations = []
        if summary["compliance_rate"] < 0.95:
            recommendations.append(
                "SLO compliance rate is below 95%. Review system performance."
            )
        if exhausted_budgets > 0:
            recommendations.append(
                f"{exhausted_budgets} error budgets exhausted. "
                f"Immediate action required."
            )
        if len(incidents) > 0:
            recommendations.append(
                f"{len(incidents)} incidents detected. "
                f"Review incident response procedures."
            )

        return ReportData(
            title="Reliability Report",
            generated_at=datetime.now(),
            period=data.get("period", "24h"),
            metrics={
                "slos": slos,
                "error_budgets": error_budgets,
                "incidents": incidents,
            },
            summary=summary,
            recommendations=recommendations,
            alerts=data.get("alerts", []),
        )

    def format_report(self, report_data: ReportData) -> str:
        """Format reliability report for output"""
        report = []
        report.append("=" * 60)
        report.append(f"RELIABILITY REPORT - {report_data.title}")
        report.append("=" * 60)
        report.append(f"Generated: {report_data.generated_at}")
        report.append(f"Period: {report_data.period}")
        report.append("")

        # Summary
        report.append("SUMMARY:")
        report.append("-" * 20)
        summary = report_data.summary
        report.append(f"Total SLOs: {summary['total_slos']}")
        report.append(f"Compliant SLOs: {summary['compliant_slos']}")
        report.append(f"Compliance Rate: {summary['compliance_rate']:.2%}")
        report.append(f"Exhausted Error Budgets: {summary['exhausted_budgets']}")
        report.append(f"Total Incidents: {summary['total_incidents']}")
        report.append("")

        # SLO Details
        if report_data.metrics.get("slos"):
            report.append("SLO COMPLIANCE:")
            report.append("-" * 20)
            for slo_name, slo_data in report_data.metrics["slos"].items():
                status = "✓" if slo_data.get("compliant", False) else "✗"
                report.append(
                    f"{status} {slo_name}: "
                    f"{slo_data.get('current_value', 'N/A')} / "
                    f"{slo_data.get('target', 'N/A')}"
                )
            report.append("")

        # Error Budgets
        if report_data.metrics.get("error_budgets"):
            report.append("ERROR BUDGETS:")
            report.append("-" * 20)
            for budget_name, budget_data in report_data.metrics[
                "error_budgets"
            ].items():
                status = "EXHAUSTED" if budget_data.get("exhausted", False) else "OK"
                report.append(
                    f"{budget_name}: {budget_data.get('remaining', 'N/A')} "
                    f"remaining ({status})"
                )
            report.append("")

        # Recommendations
        if report_data.recommendations:
            report.append("RECOMMENDATIONS:")
            report.append("-" * 20)
            for rec in report_data.recommendations:
                report.append(f"• {rec}")
            report.append("")

        # Alerts
        if report_data.alerts:
            report.append("ALERTS:")
            report.append("-" * 20)
            for alert in report_data.alerts:
                report.append(f"⚠ {alert}")
            report.append("")

        return "\n".join(report)
