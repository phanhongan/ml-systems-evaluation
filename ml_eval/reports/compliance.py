"""Compliance reports for ML Systems Evaluation"""

from datetime import datetime
from typing import Any

from .base import BaseReport, ReportData


class ComplianceReport(BaseReport):
    """Generate compliance reports for regulatory standards"""

    def generate(self, data: dict[str, Any]) -> ReportData:
        """Generate compliance report from evaluation data"""
        compliance_metrics = data.get("compliance_metrics", {})
        audit_trail = data.get("audit_trail", [])
        regulatory_standards = data.get("regulatory_standards", [])

        # Calculate compliance summary
        total_standards = len(regulatory_standards)
        compliant_standards = sum(
            1
            for standard in regulatory_standards
            if compliance_metrics.get(standard, {}).get("compliant", False)
        )
        compliance_rate = (
            compliant_standards / total_standards if total_standards > 0 else 0
        )

        summary = {
            "total_standards": total_standards,
            "compliant_standards": compliant_standards,
            "compliance_rate": compliance_rate,
            "audit_entries": len(audit_trail),
            "last_audit": audit_trail[-1].get("timestamp") if audit_trail else None,
        }

        # Generate compliance recommendations
        recommendations = []
        if compliance_rate < 1.0:
            recommendations.append(
                "Not all regulatory standards are compliant. Review required."
            )
        if not audit_trail:
            recommendations.append("No audit trail available. Implement audit logging.")
        if len(audit_trail) < 10:
            recommendations.append("Limited audit trail. Increase audit frequency.")

        return ReportData(
            title="Compliance Report",
            generated_at=datetime.now(),
            period=data.get("period", "30d"),
            metrics={
                "compliance_metrics": compliance_metrics,
                "audit_trail": audit_trail,
                "standards": regulatory_standards,
            },
            summary=summary,
            recommendations=recommendations,
            alerts=data.get("alerts", []),
        )

    def format_report(self, report_data: ReportData) -> str:
        """Format compliance report for output"""
        report = []
        report.append("=" * 60)
        report.append(f"COMPLIANCE REPORT - {report_data.title}")
        report.append("=" * 60)
        report.append(f"Generated: {report_data.generated_at}")
        report.append(f"Period: {report_data.period}")
        report.append("")

        # Compliance Summary
        report.append("COMPLIANCE SUMMARY:")
        report.append("-" * 20)
        summary = report_data.summary
        report.append(f"Total Standards: {summary['total_standards']}")
        report.append(f"Compliant Standards: {summary['compliant_standards']}")
        report.append(f"Compliance Rate: {summary['compliance_rate']:.2%}")
        report.append(f"Audit Entries: {summary['audit_entries']}")
        if summary["last_audit"]:
            report.append(f"Last Audit: {summary['last_audit']}")
        report.append("")

        # Compliance by Standard
        if report_data.metrics.get("compliance_metrics"):
            report.append("COMPLIANCE BY STANDARD:")
            report.append("-" * 20)
            for standard, metrics in report_data.metrics["compliance_metrics"].items():
                status = (
                    "✓ COMPLIANT"
                    if metrics.get("compliant", False)
                    else "✗ NON-COMPLIANT"
                )
                report.append(f"{status} {standard}")
                if metrics.get("details"):
                    report.append(f"   Details: {metrics['details']}")
            report.append("")

        # Recent Audit Trail
        if report_data.metrics.get("audit_trail"):
            report.append("RECENT AUDIT TRAIL:")
            report.append("-" * 20)
            for entry in report_data.metrics["audit_trail"][-5:]:  # Show last 5 entries
                report.append(
                    f"[{entry.get('timestamp', 'Unknown')}] "
                    f"{entry.get('action', 'Unknown action')}"
                )
                if entry.get("details"):
                    report.append(f"   {entry['details']}")
            report.append("")

        # Recommendations
        if report_data.recommendations:
            report.append("COMPLIANCE RECOMMENDATIONS:")
            report.append("-" * 20)
            for rec in report_data.recommendations:
                report.append(f"• {rec}")
            report.append("")

        # Alerts
        if report_data.alerts:
            report.append("COMPLIANCE ALERTS:")
            report.append("-" * 20)
            for alert in report_data.alerts:
                report.append(f"⚠ {alert}")
            report.append("")

        return "\n".join(report)
