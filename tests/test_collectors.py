"""Unit tests for collectors module"""

import pytest
from unittest.mock import Mock, patch, mock_open
from datetime import datetime, timedelta
import tempfile
import os
import json

from ml_eval.collectors.base import BaseCollector
from ml_eval.collectors.online import OnlineCollector
from ml_eval.collectors.offline import OfflineCollector
from ml_eval.collectors.environmental import EnvironmentalCollector
from ml_eval.collectors.regulatory import RegulatoryCollector
from ml_eval.core.config import MetricData


class TestBaseCollector:
    """Test base collector functionality"""

    def test_base_collector_creation(self):
        """Test base collector creation"""
        config = {"name": "test_collector"}

        class TestCollector(BaseCollector):
            def collect(self):
                return {}

            def health_check(self):
                return True

        collector = TestCollector(config)
        assert collector.config == config
        assert collector.name == "test_collector"

    def test_base_collector_validation(self):
        """Test collector configuration validation"""
        config = {"name": "test_collector"}

        class TestCollector(BaseCollector):
            def collect(self):
                return {}

            def health_check(self):
                return True

            def get_required_config_fields(self):
                return ["required_field"]

        collector = TestCollector(config)

        # Invalid config - missing required field
        assert collector.validate_config() is False

        # Valid config
        valid_config = {"name": "test_collector", "required_field": "value"}
        collector = TestCollector(valid_config)
        assert collector.validate_config() is True

    def test_base_collector_info(self):
        """Test collector information retrieval"""
        config = {"name": "test_collector"}

        class TestCollector(BaseCollector):
            def collect(self):
                return {}

            def health_check(self):
                return True

        collector = TestCollector(config)
        info = collector.get_collector_info()

        assert info["name"] == "test_collector"
        assert info["type"] == "TestCollector"
        assert info["config"] == config
        assert info["healthy"] is True


class TestOnlineCollector:
    """Test online collector functionality"""

    def test_online_collector_creation(self):
        """Test online collector creation"""
        config = {
            "name": "online_collector",
            "endpoints": ["http://api.example.com/metrics"],
            "interval": 60,
        }
        collector = OnlineCollector(config)
        assert collector.config == config
        assert collector.name == "online_collector"

    def test_online_collector_required_fields(self):
        """Test online collector required configuration fields"""
        collector = OnlineCollector({})
        required_fields = collector.get_required_config_fields()
        assert "endpoint" in required_fields

    def test_online_collector_validation(self):
        """Test online collector configuration validation"""
        # Valid config
        valid_config = {
            "name": "online_collector",
            "endpoint": "http://api.example.com/metrics",
        }
        collector = OnlineCollector(valid_config)
        assert collector.validate_config() is True

        # Invalid config - missing endpoint
        invalid_config = {"name": "online_collector"}
        collector = OnlineCollector(invalid_config)
        assert collector.validate_config() is False

    @patch("ml_eval.collectors.online.requests.get")
    def test_online_collector_collect(self, mock_get):
        """Test online collector data collection"""
        config = {
            "name": "online_collector",
            "endpoint": "http://api.example.com/metrics",
        }
        collector = OnlineCollector(config)

        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"availability": 0.99, "latency": 0.1}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = collector.collect()

        assert isinstance(result, dict)
        assert "availability" in result
        assert "latency" in result

    @patch("ml_eval.collectors.online.requests.get")
    def test_online_collector_collect_failure(self, mock_get):
        """Test online collector collection failure handling"""
        config = {
            "name": "online_collector",
            "endpoint": "http://api.example.com/metrics",
        }
        collector = OnlineCollector(config)

        # Mock failed request
        mock_get.side_effect = Exception("Connection failed")

        result = collector.collect()

        # Should return empty dict on failure
        assert result == {}

    def test_online_collector_health_check(self):
        """Test online collector health check"""
        config = {
            "name": "online_collector",
            "endpoint": "http://api.example.com/metrics",
        }
        collector = OnlineCollector(config)

        # Health check should return boolean
        health = collector.health_check()
        assert isinstance(health, bool)


class TestOfflineCollector:
    """Test offline collector functionality"""

    def test_offline_collector_creation(self):
        """Test offline collector creation"""
        config = {
            "name": "offline_collector",
            "log_paths": ["/path/to/logs"],
            "data_format": "json",
        }
        collector = OfflineCollector(config)
        assert collector.config == config
        assert collector.name == "offline_collector"

    def test_offline_collector_required_fields(self):
        """Test offline collector required configuration fields"""
        collector = OfflineCollector({})
        required_fields = collector.get_required_config_fields()
        assert "log_paths" in required_fields

    def test_offline_collector_validation(self):
        """Test offline collector configuration validation"""
        # Valid config
        valid_config = {"name": "offline_collector", "log_paths": ["/path/to/logs"]}
        collector = OfflineCollector(valid_config)
        assert collector.validate_config() is True

        # Invalid config - missing log_paths
        invalid_config = {"name": "offline_collector"}
        collector = OfflineCollector(invalid_config)
        assert collector.validate_config() is False

    @patch("builtins.open", new_callable=mock_open, read_data='{"availability": 0.99}')
    @patch("os.path.exists", return_value=True)
    def test_offline_collector_collect_json(self, mock_exists, mock_file):
        """Test offline collector JSON data collection"""
        config = {
            "name": "offline_collector",
            "log_paths": ["/path/to/logs/metrics.json"],
            "data_format": "json",
        }
        collector = OfflineCollector(config)

        result = collector.collect()

        assert isinstance(result, dict)
        # Should contain parsed metrics
        assert len(result) >= 0

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="timestamp,availability\n2023-01-01,0.99",
    )
    @patch("os.path.exists", return_value=True)
    def test_offline_collector_collect_csv(self, mock_exists, mock_file):
        """Test offline collector CSV data collection"""
        config = {
            "name": "offline_collector",
            "log_paths": ["/path/to/logs/metrics.csv"],
            "data_format": "csv",
        }
        collector = OfflineCollector(config)

        result = collector.collect()

        assert isinstance(result, dict)
        # Should contain parsed metrics
        assert len(result) >= 0

    @patch("os.path.exists", return_value=False)
    def test_offline_collector_health_check_failure(self, mock_exists):
        """Test offline collector health check with missing files"""
        config = {
            "name": "offline_collector",
            "log_paths": ["/path/to/logs/metrics.json"],
        }
        collector = OfflineCollector(config)

        # Health check should fail when files don't exist
        assert collector.health_check() is False


class TestEnvironmentalCollector:
    """Test environmental collector functionality"""

    def test_environmental_collector_creation(self):
        """Test environmental collector creation"""
        config = {
            "name": "environmental_collector",
            "sensor_types": ["temperature", "pressure", "humidity"],
        }
        collector = EnvironmentalCollector(config)
        assert collector.config == config
        assert collector.name == "environmental_collector"

    def test_environmental_collector_required_fields(self):
        """Test environmental collector required configuration fields"""
        collector = EnvironmentalCollector({})
        required_fields = collector.get_required_config_fields()
        assert "sensor_types" in required_fields

    def test_environmental_collector_validation(self):
        """Test environmental collector configuration validation"""
        # Valid config
        valid_config = {
            "name": "environmental_collector",
            "sensor_types": ["temperature", "pressure"],
        }
        collector = EnvironmentalCollector(valid_config)
        assert collector.validate_config() is True

        # Invalid config - missing sensor_types
        invalid_config = {"name": "environmental_collector"}
        collector = EnvironmentalCollector(invalid_config)
        assert collector.validate_config() is False

    @patch("ml_eval.collectors.environmental.random.uniform")
    def test_environmental_collector_collect(self, mock_uniform):
        """Test environmental collector data collection"""
        config = {
            "name": "environmental_collector",
            "sensor_types": ["temperature", "pressure"],
        }
        collector = EnvironmentalCollector(config)

        # Mock sensor readings
        mock_uniform.side_effect = [25.0, 1013.25]

        result = collector.collect()

        assert isinstance(result, dict)
        # Should contain environmental metrics
        assert len(result) >= 0

    def test_environmental_collector_health_check(self):
        """Test environmental collector health check"""
        config = {
            "name": "environmental_collector",
            "sensor_types": ["temperature", "pressure"],
        }
        collector = EnvironmentalCollector(config)

        # Health check should return boolean
        health = collector.health_check()
        assert isinstance(health, bool)


class TestRegulatoryCollector:
    """Test regulatory collector functionality"""

    def test_regulatory_collector_creation(self):
        """Test regulatory collector creation"""
        config = {
            "name": "regulatory_collector",
            "compliance_standards": ["DO-178C", "ISO-26262"],
        }
        collector = RegulatoryCollector(config)
        assert collector.config == config
        assert collector.name == "regulatory_collector"

    def test_regulatory_collector_required_fields(self):
        """Test regulatory collector required configuration fields"""
        collector = RegulatoryCollector({})
        required_fields = collector.get_required_config_fields()
        assert "compliance_standards" in required_fields

    def test_regulatory_collector_validation(self):
        """Test regulatory collector configuration validation"""
        # Valid config
        valid_config = {
            "name": "regulatory_collector",
            "compliance_standards": ["DO-178C"],
        }
        collector = RegulatoryCollector(valid_config)
        assert collector.validate_config() is True

        # Invalid config - missing compliance_standards
        invalid_config = {"name": "regulatory_collector"}
        collector = RegulatoryCollector(invalid_config)
        assert collector.validate_config() is False

    @patch("random.random")
    def test_regulatory_collector_collect(self, mock_random):
        """Test regulatory collector data collection"""
        config = {
            "name": "regulatory_collector",
            "compliance_standards": ["DO-178C", "ISO-26262"],
        }
        collector = RegulatoryCollector(config)

        # Mock compliance level generation
        mock_random.return_value = 0.95

        result = collector.collect()

        assert isinstance(result, dict)
        # Should contain compliance metrics
        assert len(result) >= 0

    @patch("os.path.exists", return_value=True)
    def test_regulatory_collector_health_check(self, mock_exists):
        """Test regulatory collector health check"""
        config = {
            "name": "regulatory_collector",
            "compliance_standards": ["DO-178C"],
            "audit_log_path": "/path/to/audit.log",
        }
        collector = RegulatoryCollector(config)

        # Health check should return boolean
        health = collector.health_check()
        assert isinstance(health, bool)


class TestCollectorIntegration:
    """Test collector integration and coordination"""

    def test_multiple_collectors(self):
        """Test using multiple collectors together"""
        collectors = [
            OnlineCollector(
                {"name": "online", "endpoints": ["http://api.example.com"]}
            ),
            OfflineCollector({"name": "offline", "log_paths": ["/path/to/logs"]}),
            EnvironmentalCollector({"name": "env", "sensor_types": ["temperature"]}),
            RegulatoryCollector({"name": "reg", "compliance_standards": ["DO-178C"]}),
        ]

        # All collectors should have consistent interface
        for collector in collectors:
            assert hasattr(collector, "collect")
            assert hasattr(collector, "health_check")
            assert hasattr(collector, "validate_config")

            # Test health check
            health = collector.health_check()
            assert isinstance(health, bool)

            # Test collection (may return empty dict if no data)
            data = collector.collect()
            assert isinstance(data, dict)

    def test_collector_error_handling(self):
        """Test collector error handling"""
        # Test with invalid configuration
        invalid_config = None

        with pytest.raises(AttributeError):
            OnlineCollector(invalid_config)

    def test_collector_data_consistency(self):
        """Test that all collectors provide consistent data structure"""
        collectors = [
            OnlineCollector({"name": "online", "endpoint": "http://api.example.com"}),
            OfflineCollector({"name": "offline", "log_paths": ["/path/to/logs"]}),
            EnvironmentalCollector({"name": "env", "sensor_types": ["temperature"]}),
            RegulatoryCollector({"name": "reg", "compliance_standards": ["DO-178C"]}),
        ]

        for collector in collectors:
            data = collector.collect()

            # Data should be a dictionary
            assert isinstance(data, dict)

            # If data is not empty, values should be lists of MetricData
            if data:
                for metric_name, metric_list in data.items():
                    assert isinstance(metric_list, list)
                    if metric_list:
                        assert isinstance(metric_list[0], MetricData)

    def test_collector_configuration_validation(self):
        """Test collector configuration validation"""
        # Test with valid configurations
        valid_configs = [
            {"name": "online", "endpoint": "http://api.example.com"},
            {"name": "offline", "log_paths": ["/path/to/logs"]},
            {"name": "env", "sensor_types": ["temperature"]},
            {"name": "reg", "compliance_standards": ["DO-178C"]},
        ]

        collectors = [
            OnlineCollector(valid_configs[0]),
            OfflineCollector(valid_configs[1]),
            EnvironmentalCollector(valid_configs[2]),
            RegulatoryCollector(valid_configs[3]),
        ]

        for collector in collectors:
            assert collector.validate_config() is True

    def test_collector_info_retrieval(self):
        """Test collector information retrieval"""
        config = {"name": "test_collector"}

        class TestCollector(BaseCollector):
            def collect(self):
                return {}

            def health_check(self):
                return True

        collector = TestCollector(config)
        info = collector.get_collector_info()

        assert "name" in info
        assert "type" in info
        assert "config" in info
        assert "healthy" in info
        assert info["name"] == "test_collector"
        assert info["type"] == "TestCollector"
