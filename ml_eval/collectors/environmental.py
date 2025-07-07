"""Environmental condition monitoring for harsh industrial environments"""

import random
from datetime import datetime
from typing import Any

from ..core.config import MetricData
from .base import BaseCollector


class EnvironmentalCollector(BaseCollector):
    """Environmental condition monitoring for harsh industrial environments"""

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.sensor_types = config.get(
            "sensor_types", ["temperature", "pressure", "humidity"]
        )
        self.sampling_interval = config.get("sampling_interval", 60)  # seconds
        self.alert_thresholds = config.get("alert_thresholds", {})
        self.sensor_endpoints = config.get("sensor_endpoints", {})

    def get_required_config_fields(self) -> list[str]:
        return ["sensor_types"]

    def collect(self) -> dict[str, list[MetricData]]:
        """Collect environmental metrics from sensors and monitoring systems"""
        try:
            if not self.health_check():
                self.logger.warning(
                    f"Environmental sensors health check failed for {self.name}"
                )
                return {}

            return self._collect_environmental_data()
        except Exception as e:
            self.logger.error(
                f"Failed to collect environmental data from {self.name}: {e}"
            )
            return {}

    def health_check(self) -> bool:
        """Check if environmental collector is healthy"""
        try:
            # Basic health check - verify we can access environmental data
            test_data = self._collect_environmental_data()
            return len(test_data) > 0
        except Exception as e:
            self.logger.error(f"Environmental collector health check failed: {e}")
            return False

    def _collect_environmental_data(self) -> dict[str, list[MetricData]]:
        """Collect environmental data (temperature, pressure, humidity, etc.)"""
        metrics = {}
        timestamp = datetime.now()

        for sensor_type in self.sensor_types:
            try:
                value = self._read_sensor(sensor_type)
                if value is not None:
                    metrics[f"environmental_{sensor_type}"] = [
                        MetricData(
                            timestamp=timestamp,
                            value=value,
                            metadata={
                                "source": self.name,
                                "sensor_type": sensor_type,
                                "environmental": True,
                            },
                            environmental_conditions={
                                "sensor_type": sensor_type,
                                "location": self.config.get("location", "unknown"),
                                "alert_threshold": self.alert_thresholds.get(
                                    sensor_type
                                ),
                            },
                        )
                    ]

                    # Check for environmental alerts
                    self._check_environmental_alerts(sensor_type, value)

            except Exception as e:
                self.logger.error(f"Failed to read sensor {sensor_type}: {e}")
                continue

        return metrics

    def _check_sensor_health(self, sensor_type: str) -> bool:
        """Check health of a specific environmental sensor"""
        try:
            # In a real implementation, this would check actual sensor connectivity
            # For now, we'll simulate sensor health checks

            if sensor_type in self.sensor_endpoints:
                # Check if sensor endpoint is reachable
                return self._check_endpoint_health(self.sensor_endpoints[sensor_type])
            else:
                # Simulate sensor health (replace with actual sensor library calls)
                return True  # Always healthy for simulation

        except Exception as e:
            self.logger.error(f"Health check failed for sensor {sensor_type}: {e}")
            return False

    def _check_endpoint_health(self, endpoint: str) -> bool:
        """Check if sensor endpoint is reachable"""
        try:
            import requests

            response = requests.get(endpoint, timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def _read_sensor(self, sensor_type: str) -> float | None:
        """Read value from a specific environmental sensor"""
        try:
            if sensor_type in self.sensor_endpoints:
                return self._read_from_endpoint(
                    sensor_type, self.sensor_endpoints[sensor_type]
                )
            else:
                # For simulation - replace with actual sensor libraries
                return self._simulate_sensor_reading(sensor_type)

        except Exception as e:
            self.logger.error(f"Failed to read sensor {sensor_type}: {e}")
            return None

    def _read_from_endpoint(self, _sensor_type: str, endpoint: str) -> float | None:
        """Read sensor data from configured endpoint"""
        try:
            import requests

            response = requests.get(endpoint, timeout=10)
            response.raise_for_status()

            data = response.json()
            return float(data.get("value", 0))

        except Exception as e:
            self.logger.error(f"Failed to read from endpoint {endpoint}: {e}")
            return None

    def _simulate_sensor_reading(self, sensor_type: str) -> float:
        """Simulate sensor readings for development/testing"""
        # Real implementation would use actual sensor libraries
        # These are realistic ranges for industrial environments

        if sensor_type == "temperature":
            # Industrial temperature range: -40 to 85°C
            return random.uniform(-20, 60)
        elif sensor_type == "pressure":
            # Pressure range: 0 to 1000 hPa
            return random.uniform(900, 1100)
        elif sensor_type == "humidity":
            # Humidity range: 0 to 100%
            return random.uniform(20, 80)
        elif sensor_type == "vibration":
            # Vibration range: 0 to 10 g
            return random.uniform(0, 2)
        elif sensor_type == "noise":
            # Noise level range: 30 to 120 dB
            return random.uniform(40, 90)
        else:
            # Generic sensor reading
            return random.uniform(0, 100)

    def _check_environmental_alerts(self, sensor_type: str, value: float) -> None:
        """Check for environmental condition alerts"""
        threshold = self.alert_thresholds.get(sensor_type)
        if threshold:
            min_val = threshold.get("min")
            max_val = threshold.get("max")

            if min_val is not None and value < min_val:
                self.logger.warning(
                    f"Environmental alert: {sensor_type} = {value} "
                    f"below minimum {min_val}"
                )

            if max_val is not None and value > max_val:
                self.logger.warning(
                    f"Environmental alert: {sensor_type} = {value} "
                    f"above maximum {max_val}"
                )

    def get_collector_info(self) -> dict[str, Any]:
        """Get detailed information about this collector"""
        info = super().get_collector_info()
        info.update(
            {
                "sensor_types": self.sensor_types,
                "sampling_interval": self.sampling_interval,
                "alert_thresholds": self.alert_thresholds,
                "sensor_endpoints": self.sensor_endpoints,
            }
        )
        return info
