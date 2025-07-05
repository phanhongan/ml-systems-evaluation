"""Abstract metric collection interfaces"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
from datetime import datetime

from .core import MetricData


class BaseCollector(ABC):
    """Abstract base for all metric collectors"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def collect(self) -> Dict[str, List[MetricData]]:
        """Collect and return metrics"""
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check collector health"""
        pass


class OnlineCollector(BaseCollector):
    """Real-time metric collection"""

    def collect(self) -> Dict[str, List[MetricData]]:
        """Collect real-time metrics from endpoints"""
        # Implementation depends on specific collector type
        # (Prometheus, custom APIs, etc.)
        return self._fetch_from_source()

    def health_check(self) -> bool:
        """Check if source is reachable"""
        return self._check_source_health()

    def _fetch_from_source(self) -> Dict[str, List[MetricData]]:
        """Abstract method for source-specific collection"""
        raise NotImplementedError("Implement for specific collector type")

    def _check_source_health(self) -> bool:
        """Abstract method for source-specific health check"""
        raise NotImplementedError("Implement for specific collector type")


class OfflineCollector(BaseCollector):
    """Historical data collection"""

    def collect(self) -> Dict[str, List[MetricData]]:
        """Collect historical metrics from logs/databases"""
        return self._parse_historical_data()

    def health_check(self) -> bool:
        """Check if data sources are accessible"""
        return self._check_data_sources()

    def _parse_historical_data(self) -> Dict[str, List[MetricData]]:
        """Abstract method for parsing historical data"""
        raise NotImplementedError("Implement for specific data source")

    def _check_data_sources(self) -> bool:
        """Abstract method for checking data source health"""
        raise NotImplementedError("Implement for specific data source")
