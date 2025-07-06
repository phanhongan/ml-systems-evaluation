"""Safety reports for ML Systems Evaluation"""

from datetime import datetime
from typing import Dict, List, Any

from .base import BaseReport, ReportData


class SafetyReport(BaseReport):
    """Generate safety reports for safety-critical systems"""
    
    def generate(self, data: Dict[str, Any]) -> ReportData:
        """Generate safety report from evaluation data"""
        safety_metrics = data.get("safety_metrics", {})
        compliance_status = data.get("compliance_status", {})
        safety_violations = data.get("safety_violations", [])
        
        # Calculate safety summary
        total_safety_checks = len(safety_metrics)
        passed_safety_checks = sum(1 for metric in safety_metrics.values() if metric.get("passed", False))
        safety_score = passed_safety_checks / total_safety_checks if total_safety_checks > 0 else 0
        
        summary = {
            "total_safety_checks": total_safety_checks,
            "passed_safety_checks": passed_safety_checks,
            "safety_score": safety_score,
            "safety_violations": len(safety_violations),
            "compliance_status": compliance_status
        }
        
        # Generate safety recommendations
        recommendations = []
        if safety_score < 1.0:
            recommendations.append("Safety score below 100%. Immediate safety review required.")
        if safety_violations:
            recommendations.append(f"{len(safety_violations)} safety violations detected. System shutdown may be required.")
        if not compliance_status.get("compliant", False):
            recommendations.append("System not compliant with safety standards. Regulatory review required.")
            
        return ReportData(
            title="Safety Report",
            generated_at=datetime.now(),
            period=data.get("period", "24h"),
            metrics={"safety_metrics": safety_metrics, "compliance_status": compliance_status, "violations": safety_violations},
            summary=summary,
            recommendations=recommendations,
            alerts=data.get("alerts", [])
        )
        
    def format_report(self, report_data: ReportData) -> str:
        """Format safety report for output"""
        report = []
        report.append("=" * 60)
        report.append(f"SAFETY REPORT - {report_data.title}")
        report.append("=" * 60)
        report.append(f"Generated: {report_data.generated_at}")
        report.append(f"Period: {report_data.period}")
        report.append("")
        
        # Safety Summary
        report.append("SAFETY SUMMARY:")
        report.append("-" * 20)
        summary = report_data.summary
        report.append(f"Total Safety Checks: {summary['total_safety_checks']}")
        report.append(f"Passed Safety Checks: {summary['passed_safety_checks']}")
        report.append(f"Safety Score: {summary['safety_score']:.2%}")
        report.append(f"Safety Violations: {summary['safety_violations']}")
        report.append(f"Compliance Status: {'✓ Compliant' if summary['compliance_status'].get('compliant', False) else '✗ Non-Compliant'}")
        report.append("")
        
        # Safety Metrics
        if report_data.metrics.get("safety_metrics"):
            report.append("SAFETY METRICS:")
            report.append("-" * 20)
            for metric_name, metric_data in report_data.metrics["safety_metrics"].items():
                status = "✓ PASS" if metric_data.get("passed", False) else "✗ FAIL"
                report.append(f"{status} {metric_name}: {metric_data.get('value', 'N/A')}")
            report.append("")
            
        # Safety Violations
        if report_data.metrics.get("violations"):
            report.append("SAFETY VIOLATIONS:")
            report.append("-" * 20)
            for violation in report_data.metrics["violations"]:
                report.append(f"🚨 {violation.get('description', 'Unknown violation')}")
                report.append(f"   Severity: {violation.get('severity', 'Unknown')}")
                report.append(f"   Time: {violation.get('timestamp', 'Unknown')}")
                report.append("")
                
        # Recommendations
        if report_data.recommendations:
            report.append("SAFETY RECOMMENDATIONS:")
            report.append("-" * 20)
            for rec in report_data.recommendations:
                report.append(f"• {rec}")
            report.append("")
            
        # Alerts
        if report_data.alerts:
            report.append("SAFETY ALERTS:")
            report.append("-" * 20)
            for alert in report_data.alerts:
                report.append(f"⚠ {alert}")
            report.append("")
            
        return "\n".join(report) 