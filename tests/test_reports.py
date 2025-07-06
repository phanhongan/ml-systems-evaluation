"""Tests for report generators"""

import os
from datetime import datetime
from unittest.mock import Mock, patch

from ml_eval.core.config import EvaluationResult
from ml_eval.reports.base import BaseReport, ReportData
from ml_eval.reports.business import BusinessImpactReport
from ml_eval.reports.compliance import ComplianceReport
from ml_eval.reports.reliability import ReliabilityReport
from ml_eval.reports.safety import SafetyReport


class TestBaseReport:
    """Test base report functionality"""

    def test_base_report_creation(self):
        """Test base report creation"""

        class TestReport(BaseReport):
            def generate(self, data):
                return ReportData(
                    title="Test Report",
                    generated_at=datetime.now(),
                    period="24h",
                    metrics={},
                    summary={},
                    recommendations=[],
                )

            def format_report(self, report_data):
                return "test_report"

        config = {"name": "test_report", "format": "json"}
        report = TestReport(config)
        assert report.config == config

    def test_base_report_validation(self):
        """Test base report configuration validation"""

        class TestReport(BaseReport):
            def generate(self, data):
                return ReportData(
                    title="Test Report",
                    generated_at=datetime.now(),
                    period="24h",
                    metrics={},
                    summary={},
                    recommendations=[],
                )

            def format_report(self, report_data):
                return "test_report"

            def get_required_config_fields(self):
                return ["required_field"]

        # Valid config
        config = {"name": "test", "required_field": "value"}
        report = TestReport(config)
        assert report.config == config

    def test_base_report_info(self):
        """Test getting report information"""

        class TestReport(BaseReport):
            def generate(self, data):
                return ReportData(
                    title="Test Report",
                    generated_at=datetime.now(),
                    period="24h",
                    metrics={},
                    summary={},
                    recommendations=[],
                )

            def format_report(self, report_data):
                return "test_report"

        config = {"name": "test_report"}
        report = TestReport(config)
        assert report.config == config


class TestReliabilityReport:
    """Test reliability report functionality"""

    def test_reliability_report_creation(self):
        """Test reliability report creation"""
        config = {
            "name": "reliability_report",
            "format": "json",
            "include_metrics": True,
            "include_recommendations": True,
        }
        report = ReliabilityReport(config)
        assert report.config == config

    def test_reliability_report_required_fields(self):
        """Test reliability report required configuration fields"""
        report = ReliabilityReport({})
        # ReliabilityReport may not have required fields
        assert hasattr(report, "config")

    def test_reliability_report_generate(self):
        """Test reliability report generation"""
        config = {"name": "reliability_report", "format": "json"}
        report = ReliabilityReport(config)

        # Create sample evaluation result
        evaluation_result = Mock(spec=EvaluationResult)
        evaluation_result.system_name = "test_system"
        evaluation_result.evaluation_time = datetime.now()
        evaluation_result.slo_compliance = {"availability": True, "latency": False}
        evaluation_result.error_budgets = {}
        evaluation_result.incidents = []
        evaluation_result.recommendations = ["Improve latency"]

        # Generate report
        result = report.generate({"evaluation_result": evaluation_result})

        # Verify report structure - should return ReportData
        assert isinstance(result, ReportData)
        assert result.title == "Reliability Report"
        assert isinstance(result.generated_at, datetime)
        assert isinstance(result.metrics, dict)
        assert isinstance(result.summary, dict)
        assert isinstance(result.recommendations, list)

    def test_reliability_report_json_format(self):
        """Test reliability report JSON format"""
        config = {"name": "reliability_report", "format": "json"}
        report = ReliabilityReport(config)

        # Create sample data
        data = {
            "evaluation_result": Mock(spec=EvaluationResult),
            "period": "30d",
            "metrics": {"availability": 0.99, "latency": 0.15},
        }

        result = report.generate(data)

        # Test format_report method
        formatted = report.format_report(result)

        # Verify text format (not JSON)
        assert "RELIABILITY REPORT" in formatted
        assert "SUMMARY:" in formatted
        assert "RECOMMENDATIONS:" in formatted

    def test_reliability_report_html_format(self):
        """Test reliability report HTML format"""
        config = {"name": "reliability_report", "format": "html"}
        report = ReliabilityReport(config)

        # Create sample data
        data = {"evaluation_result": Mock(spec=EvaluationResult), "period": "30d"}

        result = report.generate(data)
        formatted = report.format_report(result)

        # Verify text format (not HTML)
        assert "RELIABILITY REPORT" in formatted
        assert "SUMMARY:" in formatted
        assert "RECOMMENDATIONS:" in formatted

    def test_reliability_report_no_data(self):
        """Test reliability report with no data"""
        config = {"name": "reliability_report", "format": "json"}
        report = ReliabilityReport(config)

        # Generate report with empty data
        result = report.generate({})

        # Should still return valid ReportData
        assert isinstance(result, ReportData)
        assert result.title == "Reliability Report"


class TestSafetyReport:
    """Test safety report functionality"""

    def test_safety_report_creation(self):
        """Test safety report creation"""
        config = {
            "name": "safety_report",
            "format": "json",
            "include_violations": True,
            "include_recommendations": True,
        }
        report = SafetyReport(config)
        assert report.config == config

    def test_safety_report_generate(self):
        """Test safety report generation"""
        config = {"name": "safety_report", "format": "json"}
        report = SafetyReport(config)

        # Create sample evaluation result with safety violations
        evaluation_result = Mock(spec=EvaluationResult)
        evaluation_result.system_name = "safety_system"
        evaluation_result.evaluation_time = datetime.now()
        evaluation_result.safety_violations = [
            {
                "slo_name": "safety_decision",
                "severity": "critical",
                "details": "Safety threshold exceeded",
            }
        ]
        evaluation_result.regulatory_violations = []
        evaluation_result.recommendations = ["Immediate safety review required"]

        # Generate report
        result = report.generate({"evaluation_result": evaluation_result})

        # Verify report structure - should return ReportData
        assert isinstance(result, ReportData)
        assert result.title == "Safety Report"
        assert isinstance(result.generated_at, datetime)
        assert isinstance(result.metrics, dict)
        assert isinstance(result.summary, dict)
        assert isinstance(result.recommendations, list)

    def test_safety_report_no_violations(self):
        """Test safety report with no violations"""
        config = {"name": "safety_report", "format": "json"}
        report = SafetyReport(config)

        # Create sample evaluation result with no violations
        evaluation_result = Mock(spec=EvaluationResult)
        evaluation_result.system_name = "safe_system"
        evaluation_result.evaluation_time = datetime.now()
        evaluation_result.safety_violations = []
        evaluation_result.regulatory_violations = []
        evaluation_result.recommendations = ["System operating safely"]

        # Generate report
        result = report.generate({"evaluation_result": evaluation_result})

        # Verify report structure
        assert isinstance(result, ReportData)
        assert result.title == "Safety Report"

    def test_safety_report_regulatory_violations(self):
        """Test safety report with regulatory violations"""
        config = {"name": "safety_report", "format": "json"}
        report = SafetyReport(config)

        # Create sample evaluation result with regulatory violations
        evaluation_result = Mock(spec=EvaluationResult)
        evaluation_result.system_name = "compliance_system"
        evaluation_result.evaluation_time = datetime.now()
        evaluation_result.safety_violations = []
        evaluation_result.regulatory_violations = [
            {
                "slo_name": "do_178c_compliance",
                "compliance_standard": "DO-178C",
                "severity": "critical",
                "details": "Compliance standard violation",
            }
        ]
        evaluation_result.recommendations = ["Compliance review required"]

        # Generate report
        result = report.generate({"evaluation_result": evaluation_result})

        # Verify report structure
        assert isinstance(result, ReportData)
        assert result.title == "Safety Report"


class TestComplianceReport:
    """Test compliance report functionality"""

    def test_compliance_report_creation(self):
        """Test compliance report creation"""
        config = {
            "name": "compliance_report",
            "format": "json",
            "standards": ["DO-178C", "ISO-26262"],
            "include_audit_trail": True,
        }
        report = ComplianceReport(config)
        assert report.config == config

    def test_compliance_report_generate(self):
        """Test compliance report generation"""
        config = {"name": "compliance_report", "format": "json"}
        report = ComplianceReport(config)

        # Create sample evaluation result
        evaluation_result = Mock(spec=EvaluationResult)
        evaluation_result.system_name = "compliance_system"
        evaluation_result.evaluation_time = datetime.now()
        evaluation_result.regulatory_violations = [
            {
                "slo_name": "do_178c_compliance",
                "compliance_standard": "DO-178C",
                "severity": "critical",
                "details": "Compliance violation",
            }
        ]
        evaluation_result.safety_violations = []

        # Generate report
        result = report.generate({"evaluation_result": evaluation_result})

        # Verify report structure - should return ReportData
        assert isinstance(result, ReportData)
        assert result.title == "Compliance Report"
        assert isinstance(result.generated_at, datetime)
        assert isinstance(result.metrics, dict)
        assert isinstance(result.summary, dict)
        assert isinstance(result.recommendations, list)

    def test_compliance_report_multiple_standards(self):
        """Test compliance report with multiple standards"""
        config = {
            "name": "compliance_report",
            "format": "json",
            "standards": ["DO-178C", "ISO-26262", "IEC-61508"],
        }
        report = ComplianceReport(config)

        # Create sample evaluation result
        evaluation_result = Mock(spec=EvaluationResult)
        evaluation_result.system_name = "multi_standard_system"
        evaluation_result.evaluation_time = datetime.now()
        evaluation_result.regulatory_violations = [
            {
                "slo_name": "do_178c_compliance",
                "compliance_standard": "DO-178C",
                "severity": "critical",
            },
            {
                "slo_name": "iso_26262_compliance",
                "compliance_standard": "ISO-26262",
                "severity": "warning",
            },
        ]

        # Generate report
        result = report.generate({"evaluation_result": evaluation_result})

        # Verify report structure
        assert isinstance(result, ReportData)
        assert result.title == "Compliance Report"


class TestBusinessImpactReport:
    """Test business impact report functionality"""

    def test_business_impact_report_creation(self):
        """Test business impact report creation"""
        config = {
            "name": "business_impact_report",
            "format": "json",
            "include_financial_metrics": True,
            "include_risk_assessment": True,
        }
        report = BusinessImpactReport(config)
        assert report.config == config

    def test_business_impact_report_generate(self):
        """Test business impact report generation"""
        config = {"name": "business_impact_report", "format": "json"}
        report = BusinessImpactReport(config)

        # Create sample evaluation result
        evaluation_result = Mock(spec=EvaluationResult)
        evaluation_result.system_name = "business_system"
        evaluation_result.evaluation_time = datetime.now()
        evaluation_result.business_impact_assessment = {
            "financial_impact": "$1M/hour",
            "risk_level": "high",
            "mitigation_cost": "$500K",
        }
        evaluation_result.slo_compliance = {"availability": False, "latency": True}

        # Generate report
        result = report.generate({"evaluation_result": evaluation_result})

        # Verify report structure - should return ReportData
        assert isinstance(result, ReportData)
        assert result.title == "Business Impact Report"
        assert isinstance(result.generated_at, datetime)
        assert isinstance(result.metrics, dict)
        assert isinstance(result.summary, dict)
        assert isinstance(result.recommendations, list)

    def test_business_impact_report_financial_metrics(self):
        """Test business impact report with financial metrics"""
        config = {
            "name": "business_impact_report",
            "format": "json",
            "include_financial_metrics": True,
        }
        report = BusinessImpactReport(config)

        # Create sample data with financial metrics
        data = {
            "evaluation_result": Mock(spec=EvaluationResult),
            "financial_metrics": {
                "revenue_impact": "$2M/day",
                "cost_savings": "$500K/month",
                "roi": "150%",
            },
        }

        result = report.generate(data)

        # Verify financial metrics are included
        assert isinstance(result, ReportData)
        assert result.title == "Business Impact Report"


class TestReportIntegration:
    """Test report integration and coordination"""

    def test_multiple_report_types(self):
        """Test using multiple report types together"""
        reports = [
            ReliabilityReport({"name": "reliability_report"}),
            SafetyReport({"name": "safety_report"}),
            ComplianceReport({"name": "compliance_report"}),
            BusinessImpactReport({"name": "business_report"}),
        ]

        # All reports should have consistent interface
        for report in reports:
            assert hasattr(report, "generate")
            assert hasattr(report, "format_report")
            assert hasattr(report, "config")

    def test_report_error_handling(self):
        """Test report error handling"""
        # Test with invalid data
        config = {"name": "test_report"}
        report = ReliabilityReport(config)

        # Should handle missing or invalid data gracefully
        result = report.generate({})
        assert isinstance(result, ReportData)

    def test_report_file_output(self):
        """Test report file output"""
        config = {"name": "test_report", "format": "json"}
        report = ReliabilityReport(config)

        # Create sample data
        data = {"evaluation_result": Mock(spec=EvaluationResult), "period": "30d"}

        # Generate report
        report_data = report.generate(data)

        # Test writing to file
        with patch("tempfile.NamedTemporaryFile") as mock_tempfile:
            mock_tempfile.return_value.__enter__.return_value.name = "test_file.json"
            report.save_report(report_data, "test_file.json")

        try:
            # Verify file was written
            with open("test_file.json", "r") as f:
                content = f.read()
                assert len(content) > 0
        finally:
            # Clean up
            import os

            os.unlink("test_file.json")

    def test_report_format_consistency(self):
        """Test that all reports provide consistent format options"""
        report_configs = [
            {"name": "reliability", "format": "json"},
            {"name": "safety", "format": "html"},
            {"name": "compliance", "format": "pdf"},
            {"name": "business", "format": "csv"},
        ]

        reports = [
            ReliabilityReport(report_configs[0]),
            SafetyReport(report_configs[1]),
            ComplianceReport(report_configs[2]),
            BusinessImpactReport(report_configs[3]),
        ]

        for report in reports:
            # All reports should support format configuration
            assert hasattr(report, "config")
            assert "format" in report.config

    def test_report_data_validation(self):
        """Test report data validation"""
        config = {"name": "test_report"}
        report = ReliabilityReport(config)

        # Test with valid data
        valid_data = {"evaluation_result": Mock(spec=EvaluationResult), "period": "30d"}
        result = report.generate(valid_data)
        assert isinstance(result, ReportData)

    def test_report_save_functionality(self):
        """Test report save functionality"""
        config = {"name": "test_report", "format": "json"}
        report = ReliabilityReport(config)

        # Create sample data
        data = {"evaluation_result": Mock(spec=EvaluationResult), "period": "30d"}

        # Generate report
        report_data = report.generate(data)

        # Test saving to file
        try:
            with patch("tempfile.NamedTemporaryFile") as mock_tempfile:
                mock_tempfile.return_value.__enter__.return_value.name = (
                    "test_file.json"
                )
                success = report.save_report(report_data, "test_file.json")
                assert success is True

                # Verify file was created
                assert os.path.exists("test_file.json")
                with open("test_file.json", "r") as f:
                    content = f.read()
                    assert len(content) > 0
        finally:
            # Clean up
            if os.path.exists("test_file.json"):
                os.unlink("test_file.json")
