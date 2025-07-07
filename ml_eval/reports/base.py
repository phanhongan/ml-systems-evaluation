"""Base report interface for ML Systems Evaluation"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class ReportData:
    """Data structure for report information"""

    title: str
    generated_at: datetime
    period: str
    metrics: dict[str, Any]
    summary: dict[str, Any]
    recommendations: list[str]
    alerts: list[str] | None = None


class BaseReport(ABC):
    """Base class for all report types"""

    def __init__(self, config: dict[str, Any]):
        self.config = config

    @abstractmethod
    def generate(self, data: dict[str, Any]) -> ReportData:
        """Generate report from evaluation data"""

    @abstractmethod
    def format_report(self, report_data: ReportData) -> str:
        """Format report data for output"""

    def save_report(self, report_data: ReportData, output_path: str) -> bool:
        """Save report to file"""
        try:
            formatted_report = self.format_report(report_data)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(formatted_report)

            return True

        except Exception:
            return False
