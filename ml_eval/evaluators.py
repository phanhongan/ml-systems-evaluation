"""Abstract evaluation interfaces"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any

from .core import SLOConfig, ErrorBudget, MetricData


class BaseEvaluator(ABC):
    """Abstract base for all evaluators"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def evaluate(
        self, metrics: Dict[str, List[MetricData]], slos: List[SLOConfig]
    ) -> Dict[str, Any]:
        """Evaluate metrics and return assessment"""
        pass


class ReliabilityEvaluator(BaseEvaluator):
    """SRE-focused reliability evaluation"""

    def evaluate(
        self, metrics: Dict[str, List[MetricData]], slos: List[SLOConfig]
    ) -> Dict[str, Any]:
        """Evaluate system reliability using SRE principles"""
        return {
            "slo_compliance": self._assess_slo_compliance(metrics, slos),
            "error_budgets": self._calculate_error_budgets(metrics, slos),
            "incidents": self._detect_incidents(metrics, slos),
            "recommendations": self._generate_recommendations(metrics, slos),
        }

    def _assess_slo_compliance(
        self, metrics: Dict[str, List[MetricData]], slos: List[SLOConfig]
    ) -> Dict[str, bool]:
        """Abstract SLO compliance assessment"""
        # Implementation varies by metric type and SLO definition
        return {}

    def _calculate_error_budgets(
        self, metrics: Dict[str, List[MetricData]], slos: List[SLOConfig]
    ) -> Dict[str, ErrorBudget]:
        """Abstract error budget calculation"""
        # Implementation depends on SLO configuration
        return {}

    def _detect_incidents(
        self, metrics: Dict[str, List[MetricData]], slos: List[SLOConfig]
    ) -> List[Dict[str, Any]]:
        """Abstract incident detection"""
        return []

    def _generate_recommendations(
        self, metrics: Dict[str, List[MetricData]], slos: List[SLOConfig]
    ) -> List[str]:
        """Abstract recommendation generation"""
        return []


class PerformanceEvaluator(BaseEvaluator):
    """ML performance evaluation"""

    def evaluate(
        self, metrics: Dict[str, List[MetricData]], slos: List[SLOConfig]
    ) -> Dict[str, Any]:
        """Evaluate ML model/workflow performance"""
        return {
            "performance_metrics": self._analyze_performance(metrics),
            "trend_analysis": self._analyze_trends(metrics),
            "anomaly_detection": self._detect_anomalies(metrics),
        }

    def _analyze_performance(
        self, metrics: Dict[str, List[MetricData]]
    ) -> Dict[str, Any]:
        """Abstract performance analysis"""
        return {}

    def _analyze_trends(self, metrics: Dict[str, List[MetricData]]) -> Dict[str, str]:
        """Abstract trend analysis"""
        return {}

    def _detect_anomalies(
        self, metrics: Dict[str, List[MetricData]]
    ) -> List[Dict[str, Any]]:
        """Abstract anomaly detection"""
        return []
