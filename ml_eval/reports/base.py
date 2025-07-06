"""Base report interface for ML Systems Evaluation"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Any, Optional

import logging


@dataclass
class ReportData:
    """Data structure for report information"""
    title: str
    generated_at: datetime
    period: str
    metrics: Dict[str, Any]
    summary: Dict[str, Any]
    recommendations: List[str]
    alerts: List[str] = None


class BaseReport(ABC):
    """Base class for all report types"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    @abstractmethod
    def generate(self, data: Dict[str, Any]) -> ReportData:
        """Generate report from evaluation data"""
        pass
        
    @abstractmethod
    def format_report(self, report_data: ReportData) -> str:
        """Format report data for output"""
        pass
        
    def save_report(self, report_data: ReportData, output_path: str) -> bool:
        """Save report to file"""
        try:
            formatted_report = self.format_report(report_data)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(formatted_report)
                
            self.logger.info(f"Report saved to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save report to {output_path}: {e}")
            return False 