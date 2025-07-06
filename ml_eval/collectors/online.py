"""Real-time metric collection for Industrial AI systems"""

from typing import Dict, List, Any
from datetime import datetime
import logging
import requests
from urllib.parse import urljoin

from .base import BaseCollector
from ..core.config import MetricData


class OnlineCollector(BaseCollector):
    """Real-time metric collection from live systems"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.endpoint = config.get("endpoint")
        self.timeout = config.get("timeout", 30)
        self.retry_count = config.get("retry_count", 3)
        self.metrics_path = config.get("metrics_path", "/metrics")

    def get_required_config_fields(self) -> List[str]:
        return ["endpoint"]

    def collect(self) -> Dict[str, List[MetricData]]:
        """Collect real-time metrics from endpoints"""
        try:
            if not self.health_check():
                self.logger.warning(f"Health check failed for {self.name}")
                return {}

            return self._fetch_from_source()
        except Exception as e:
            self.logger.error(f"Failed to collect metrics from {self.name}: {e}")
            return {}

    def health_check(self) -> bool:
        """Check if source is reachable and responding"""
        try:
            response = requests.get(
                self.endpoint, 
                timeout=self.timeout,
                headers={"User-Agent": "ML-Eval-Framework/1.0"}
            )
            return response.status_code == 200
        except Exception as e:
            self.logger.debug(f"Health check failed for {self.name}: {e}")
            return False

    def _fetch_from_source(self) -> Dict[str, List[MetricData]]:
        """Fetch metrics from the configured endpoint"""
        try:
            url = urljoin(self.endpoint, self.metrics_path)
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse response based on format (Prometheus, JSON, etc.)
            metrics = self._parse_response(response)
            self.logger.debug(f"Collected {len(metrics)} metrics from {self.name}")
            return metrics
            
        except requests.RequestException as e:
            self.logger.error(f"Request failed for {self.name}: {e}")
            return {}
        except Exception as e:
            self.logger.error(f"Failed to parse response from {self.name}: {e}")
            return {}

    def _parse_response(self, response) -> Dict[str, List[MetricData]]:
        """Parse response into metric data format"""
        # Default implementation - override for specific formats
        metrics = {}
        
        try:
            # Try to parse as JSON first
            data = response.json()
            for metric_name, value in data.items():
                if isinstance(value, (int, float)):
                    metrics[metric_name] = [
                        MetricData(
                            timestamp=datetime.now(),
                            value=float(value),
                            metadata={"source": self.name, "endpoint": self.endpoint}
                        )
                    ]
        except ValueError:
            # Fall back to text parsing (e.g., Prometheus format)
            self._parse_text_response(response.text, metrics)
            
        return metrics

    def _parse_text_response(self, text: str, metrics: Dict[str, List[MetricData]]):
        """Parse text-based metric formats (e.g., Prometheus)"""
        for line in text.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    # Simple Prometheus-style parsing
                    if ' ' in line:
                        metric_name, value = line.rsplit(' ', 1)
                        if value.replace('.', '').replace('-', '').isdigit():
                            metrics[metric_name] = [
                                MetricData(
                                    timestamp=datetime.now(),
                                    value=float(value),
                                    metadata={"source": self.name, "format": "prometheus"}
                                )
                            ]
                except (ValueError, IndexError):
                    continue

    def get_collector_info(self) -> Dict[str, Any]:
        """Get detailed information about this collector"""
        info = super().get_collector_info()
        info.update({
            "endpoint": self.endpoint,
            "timeout": self.timeout,
            "retry_count": self.retry_count,
            "metrics_path": self.metrics_path,
        })
        return info 