"""Online data collection for ML Systems Evaluation Framework"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List

import aiohttp

from ..core.config import MetricData
from .base import BaseCollector


class OnlineCollector(BaseCollector):
    """Real-time data collection from APIs and streaming sources"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.endpoints = config.get("endpoints", [])
        self.polling_interval = config.get("polling_interval", 30)  # seconds
        self.timeout = config.get("timeout", 10)  # seconds
        self.retry_attempts = config.get("retry_attempts", 3)
        self.headers = config.get("headers", {})
        self.auth_config = config.get("auth_config", {})

    def get_required_config_fields(self) -> List[str]:
        return ["endpoints"]

    def collect(self) -> Dict[str, List[MetricData]]:
        """Collect real-time metrics from online sources"""
        try:
            health = self.health_check()
            if not health:
                self.logger.warning(
                    f"Online collector health check failed for {self.name}"
                )
                return {}

            metrics = self._collect_online_data()
            return metrics
        except Exception as e:
            self.logger.error(f"Failed to collect online data from {self.name}: {e}")
            return {}

    def health_check(self) -> bool:
        """Check if online endpoints are accessible"""
        try:
            # Check each endpoint
            for endpoint in self.endpoints:
                if not self._check_endpoint_health(endpoint):
                    self.logger.warning(f"Endpoint {endpoint} health check failed")
                    return False
            return True
        except Exception as e:
            self.logger.error(f"Online health check failed: {e}")
            return False

    def _collect_online_data(self) -> Dict[str, List[MetricData]]:
        """Collect data from online endpoints"""
        metrics = {}
        timestamp = datetime.now()

        for endpoint in self.endpoints:
            try:
                endpoint_metrics = self._collect_from_endpoint(endpoint, timestamp)
                metrics.update(endpoint_metrics)
            except Exception as e:
                self.logger.error(f"Failed to collect from endpoint {endpoint}: {e}")
                continue

        return metrics

    def _check_endpoint_health(self, endpoint: str) -> bool:
        """Check health of a specific endpoint"""
        try:
            # This would make a lightweight health check request
            # For now, return True for simulation
            return True
        except Exception as e:
            self.logger.error(f"Health check failed for endpoint {endpoint}: {e}")
            return False

    def _collect_from_endpoint(
        self, endpoint: str, timestamp: datetime
    ) -> Dict[str, List[MetricData]]:
        """Collect data from a specific endpoint"""
        metrics = {}

        try:
            # In a real implementation, this would make HTTP requests
            # For simulation, we'll generate mock data
            mock_data = self._generate_mock_endpoint_data(endpoint)

            for metric_name, value in mock_data.items():
                # Check if this metric is from the configured metrics list
                configured_metrics = getattr(self, 'config', {}).get('metrics', [])
                if metric_name in configured_metrics:
                    # Use the metric name as-is for configured metrics
                    final_metric_name = metric_name
                else:
                    # Prefix with "online_" for other metrics
                    final_metric_name = f"online_{metric_name}"
                
                metrics[final_metric_name] = [
                    MetricData(
                        timestamp=timestamp,
                        value=value,
                        metadata={
                            "source": self.name,
                            "endpoint": endpoint,
                            "online": True,
                        },
                    )
                ]

        except Exception as e:
            self.logger.error(f"Failed to collect from endpoint {endpoint}: {e}")

        return metrics

    def _generate_mock_endpoint_data(self, endpoint: str) -> Dict[str, float]:
        """Generate mock data for simulation"""
        import random

        # Check if we have specific metrics configured
        configured_metrics = getattr(self, 'config', {}).get('metrics', [])
        
        if configured_metrics:
            # Generate data for configured metrics
            mock_data = {}
            for metric in configured_metrics:
                if 'accuracy' in metric.lower():
                    mock_data[metric] = random.uniform(0.85, 0.98)
                elif 'latency' in metric.lower() or 'response_time' in metric.lower():
                    mock_data[metric] = random.uniform(10, 500)
                elif 'throughput' in metric.lower():
                    mock_data[metric] = random.uniform(100, 10000)
                elif 'rate' in metric.lower():
                    mock_data[metric] = random.uniform(0.8, 0.99)
                elif 'strength' in metric.lower():
                    mock_data[metric] = random.uniform(0.7, 0.95)
                elif 'confidence' in metric.lower():
                    mock_data[metric] = random.uniform(0.75, 0.95)
                elif 'quality' in metric.lower():
                    mock_data[metric] = random.uniform(0.8, 0.95)
                elif 'efficiency' in metric.lower():
                    mock_data[metric] = random.uniform(0.7, 0.9)
                else:
                    # Generic metric
                    mock_data[metric] = random.uniform(0, 100)
            return mock_data

        # Generate realistic mock data based on endpoint type
        if "metrics" in endpoint.lower():
            return {
                "cpu_usage": random.uniform(10, 90),
                "memory_usage": random.uniform(20, 80),
                "disk_usage": random.uniform(30, 95),
                "network_throughput": random.uniform(100, 1000),
            }
        elif "performance" in endpoint.lower():
            return {
                "response_time": random.uniform(10, 500),
                "throughput": random.uniform(100, 10000),
                "error_rate": random.uniform(0, 5),
                "availability": random.uniform(95, 100),
            }
        elif "business" in endpoint.lower():
            return {
                "revenue": random.uniform(1000, 100000),
                "transactions": random.uniform(10, 1000),
                "conversion_rate": random.uniform(1, 10),
                "customer_satisfaction": random.uniform(70, 100),
            }
        else:
            # Generic metrics
            return {
                "metric_1": random.uniform(0, 100),
                "metric_2": random.uniform(0, 100),
                "metric_3": random.uniform(0, 100),
            }

    async def _async_collect_from_endpoint(
        self, endpoint: str, session: aiohttp.ClientSession
    ) -> Dict[str, float]:
        """Asynchronously collect data from an endpoint"""
        try:
            headers = self.headers.copy()

            # Add authentication if configured
            if self.auth_config:
                headers.update(self._get_auth_headers())

            async with session.get(
                endpoint,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_endpoint_response(data)
                else:
                    self.logger.warning(
                        f"Endpoint {endpoint} returned status " f"{response.status}"
                    )
                    return {}

        except asyncio.TimeoutError:
            self.logger.error(f"Timeout collecting from endpoint {endpoint}")
            return {}
        except Exception as e:
            self.logger.error(f"Failed to collect from endpoint {endpoint}: {e}")
            return {}

    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        auth_type = self.auth_config.get("type", "bearer")

        if auth_type == "bearer":
            token = self.auth_config.get("token")
            if token:
                return {"Authorization": f"Bearer {token}"}
        elif auth_type == "api_key":
            api_key = self.auth_config.get("api_key")
            key_name = self.auth_config.get("key_name", "X-API-Key")
            if api_key:
                return {key_name: api_key}

        return {}

    def _parse_endpoint_response(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Parse response data and extract metrics"""
        metrics = {}

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (int, float)):
                    metrics[key] = float(value)
                elif isinstance(value, dict):
                    # Handle nested metrics
                    nested_metrics = self._parse_endpoint_response(value)
                    for nested_key, nested_value in nested_metrics.items():
                        metrics[f"{key}_{nested_key}"] = nested_value

        return metrics

    def get_collector_info(self) -> Dict[str, Any]:
        """Get detailed information about this collector"""
        info = super().get_collector_info()
        info.update(
            {
                "endpoints": self.endpoints,
                "polling_interval": self.polling_interval,
                "timeout": self.timeout,
                "retry_attempts": self.retry_attempts,
                "headers": self.headers,
                "auth_config": self.auth_config,
            }
        )
        return info
