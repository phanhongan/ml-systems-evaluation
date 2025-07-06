"""Business impact reports for ML Systems Evaluation"""

from datetime import datetime
from typing import Any, Dict

from .base import BaseReport, ReportData


class BusinessImpactReport(BaseReport):
    """Generate business impact reports connecting technical metrics to
    business outcomes"""

    def generate(self, data: Dict[str, Any]) -> ReportData:
        """Generate business impact report from evaluation data"""
        business_metrics = data.get("business_metrics", {})
        technical_metrics = data.get("technical_metrics", {})
        financial_impact = data.get("financial_impact", {})

        # Calculate business impact summary
        total_incidents = len(data.get("incidents", []))
        financial_loss = financial_impact.get("total_loss", 0)
        downtime_hours = business_metrics.get("downtime_hours", 0)
        customer_impact = business_metrics.get("customer_impact_score", 0)

        summary = {
            "total_incidents": total_incidents,
            "financial_loss": financial_loss,
            "downtime_hours": downtime_hours,
            "customer_impact_score": customer_impact,
            "roi_impact": financial_impact.get("roi_impact", 0),
        }

        # Generate business recommendations
        recommendations = []
        if financial_loss > 0:
            recommendations.append(
                f"Financial loss of ${financial_loss:,.2f} detected. "
                f"Review system reliability."
            )
        if downtime_hours > 1:
            recommendations.append(
                f"{downtime_hours} hours of downtime. Implement redundancy."
            )
        if customer_impact < 0.8:
            recommendations.append(
                "Customer impact score below 80%. Improve system performance."
            )
        if total_incidents > 5:
            recommendations.append(
                f"{total_incidents} incidents detected. Review incident response."
            )

        return ReportData(
            title="Business Impact Report",
            generated_at=datetime.now(),
            period=data.get("period", "30d"),
            metrics={
                "business_metrics": business_metrics,
                "technical_metrics": technical_metrics,
                "financial_impact": financial_impact,
            },
            summary=summary,
            recommendations=recommendations,
            alerts=data.get("alerts", []),
        )

    def format_report(self, report_data: ReportData) -> str:
        """Format business impact report for output"""
        report = []
        report.append("=" * 60)
        report.append(f"BUSINESS IMPACT REPORT - {report_data.title}")
        report.append("=" * 60)
        report.append(f"Generated: {report_data.generated_at}")
        report.append(f"Period: {report_data.period}")
        report.append("")

        # Business Impact Summary
        report.append("BUSINESS IMPACT SUMMARY:")
        report.append("-" * 20)
        summary = report_data.summary
        report.append(f"Total Incidents: {summary['total_incidents']}")
        report.append(f"Financial Loss: ${summary['financial_loss']:,.2f}")
        report.append(f"Downtime Hours: {summary['downtime_hours']:.1f}")
        report.append(f"Customer Impact Score: {summary['customer_impact_score']:.1%}")
        report.append(f"ROI Impact: {summary['roi_impact']:.2%}")
        report.append("")

        # Business Metrics
        if report_data.metrics.get("business_metrics"):
            report.append("BUSINESS METRICS:")
            report.append("-" * 20)
            for metric_name, metric_value in report_data.metrics[
                "business_metrics"
            ].items():
                if isinstance(metric_value, float):
                    report.append(f"{metric_name}: {metric_value:.2f}")
                else:
                    report.append(f"{metric_name}: {metric_value}")
            report.append("")

        # Technical to Business Correlation
        if report_data.metrics.get("technical_metrics") and report_data.metrics.get(
            "business_metrics"
        ):
            report.append("TECHNICAL TO BUSINESS CORRELATION:")
            report.append("-" * 20)
            tech_metrics = report_data.metrics["technical_metrics"]
            biz_metrics = report_data.metrics["business_metrics"]

            if "availability" in tech_metrics and "downtime_hours" in biz_metrics:
                availability = tech_metrics["availability"]
                downtime = biz_metrics["downtime_hours"]
                report.append(
                    f"System Availability: {availability:.2%} → "
                    f"Downtime: {downtime:.1f} hours"
                )

            if "error_rate" in tech_metrics and "customer_impact_score" in biz_metrics:
                error_rate = tech_metrics["error_rate"]
                customer_impact = biz_metrics["customer_impact_score"]
                report.append(
                    f"Error Rate: {error_rate:.2%} → "
                    f"Customer Impact: {customer_impact:.1%}"
                )
            report.append("")

        # Financial Impact
        if report_data.metrics.get("financial_impact"):
            report.append("FINANCIAL IMPACT:")
            report.append("-" * 20)
            financial = report_data.metrics["financial_impact"]
            for impact_type, value in financial.items():
                if isinstance(value, float):
                    report.append(f"{impact_type}: ${value:,.2f}")
                else:
                    report.append(f"{impact_type}: {value}")
            report.append("")

        # Recommendations
        if report_data.recommendations:
            report.append("BUSINESS RECOMMENDATIONS:")
            report.append("-" * 20)
            for rec in report_data.recommendations:
                report.append(f"• {rec}")
            report.append("")

        # Alerts
        if report_data.alerts:
            report.append("BUSINESS ALERTS:")
            report.append("-" * 20)
            for alert in report_data.alerts:
                report.append(f"⚠ {alert}")
            report.append("")

        return "\n".join(report)
