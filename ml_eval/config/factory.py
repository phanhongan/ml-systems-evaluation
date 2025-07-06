"""Configuration factory for ML Systems Evaluation Framework"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from .loader import ConfigLoader
from .validator import ConfigValidator


class ConfigFactory:
    """Factory for creating and managing configuration objects"""

    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = config_dir or os.getcwd()
        self.loader = ConfigLoader()
        self.validator = ConfigValidator()
        self._config_cache: Dict[str, Dict[str, Any]] = {}

    def create_config(self, config_path: str) -> Dict[str, Any]:
        """Create configuration from file or directory"""
        try:
            # Check if config is already cached
            if config_path in self._config_cache:
                return self._config_cache[config_path]

            # Load configuration
            config = self.loader.load_config(config_path)

            # Validate configuration
            validation_result = self.validator.validate_config(config)
            if not (
                isinstance(validation_result, dict)
                and validation_result.get("valid", False)
            ):
                errors = (
                    validation_result["errors"]
                    if isinstance(validation_result, dict)
                    and "errors" in validation_result
                    else str(validation_result)
                )
                raise ValueError(f"Configuration validation failed: {errors}")

            # Cache the configuration
            self._config_cache[config_path] = config

            return config

        except Exception as e:
            raise ConfigFactoryError(f"Failed to create config from {config_path}: {e}")

    def create_collector_config(self, collector_type: str, **kwargs) -> Dict[str, Any]:
        """Create configuration for a specific collector type"""
        base_config = self._get_base_collector_config(collector_type)

        # Merge with provided kwargs
        config = {**base_config, **kwargs}

        # Validate collector-specific configuration
        validation_result = self.validator.validate_config(config)
        if not (
            isinstance(validation_result, dict)
            and validation_result.get("valid", False)
        ):
            errors = (
                validation_result["errors"]
                if isinstance(validation_result, dict) and "errors" in validation_result
                else str(validation_result)
            )
            raise ValueError(f"Collector config validation failed: {errors}")

        return config

    def create_evaluator_config(self, evaluator_type: str, **kwargs) -> Dict[str, Any]:
        """Create configuration for a specific evaluator type"""
        base_config = self._get_base_evaluator_config(evaluator_type)

        # Merge with provided kwargs
        config = {**base_config, **kwargs}

        # Validate evaluator-specific configuration
        validation_result = self.validator.validate_config(config)
        if not (
            isinstance(validation_result, dict)
            and validation_result.get("valid", False)
        ):
            errors = (
                validation_result["errors"]
                if isinstance(validation_result, dict) and "errors" in validation_result
                else str(validation_result)
            )
            raise ValueError(f"Evaluator config validation failed: {errors}")

        return config

    def create_report_config(self, report_type: str, **kwargs) -> Dict[str, Any]:
        """Create configuration for a specific report type"""
        base_config = self._get_base_report_config(report_type)

        # Merge with provided kwargs
        config = {**base_config, **kwargs}

        # Validate report-specific configuration
        validation_result = self.validator.validate_config(config)
        if not (
            isinstance(validation_result, dict)
            and validation_result.get("valid", False)
        ):
            errors = (
                validation_result["errors"]
                if isinstance(validation_result, dict) and "errors" in validation_result
                else str(validation_result)
            )
            raise ValueError(f"Report config validation failed: {errors}")

        return config

    def _get_base_collector_config(self, collector_type: str) -> Dict[str, Any]:
        """Get base configuration for a collector type"""
        base_configs = {
            "environmental": {
                "type": "environmental",
                "sensor_types": ["temperature", "pressure", "humidity"],
                "sampling_interval": 60,
                "alert_thresholds": {},
            },
            "offline": {
                "type": "offline",
                "data_sources": [],
                "file_patterns": ["*.json", "*.csv"],
                "parsing_rules": {},
            },
            "online": {
                "type": "online",
                "endpoints": [],
                "polling_interval": 30,
                "timeout": 10,
                "retry_attempts": 3,
            },
            "regulatory": {
                "type": "regulatory",
                "compliance_frameworks": [],
                "audit_requirements": {},
                "reporting_frequency": "monthly",
            },
        }

        result = base_configs.get(collector_type, {"type": collector_type})
        if not isinstance(result, dict):
            result = {"type": collector_type}
        return result

    def _get_base_evaluator_config(self, evaluator_type: str) -> Dict[str, Any]:
        """Get base configuration for an evaluator type"""
        base_configs = {
            "performance": {
                "type": "performance",
                "metrics": ["accuracy", "precision", "recall", "f1"],
                "thresholds": {},
                "baseline_comparison": True,
            },
            "reliability": {
                "type": "reliability",
                "availability_threshold": 0.99,
                "error_budget": 0.01,
                "slo_targets": {},
            },
            "safety": {
                "type": "safety",
                "safety_thresholds": {},
                "risk_assessment": True,
                "incident_tracking": True,
            },
            "compliance": {
                "type": "compliance",
                "standards": [],
                "audit_requirements": {},
                "reporting_frequency": "monthly",
            },
            "drift": {
                "type": "drift",
                "detection_methods": ["statistical", "ml_based"],
                "sensitivity": 0.05,
                "window_size": 1000,
            },
        }

        result = base_configs.get(evaluator_type, {"type": evaluator_type})
        if not isinstance(result, dict):
            result = {"type": evaluator_type}
        return result

    def _get_base_report_config(self, report_type: str) -> Dict[str, Any]:
        """Get base configuration for a report type"""
        base_configs = {
            "business": {
                "type": "business",
                "metrics": ["revenue_impact", "cost_savings", "efficiency_gains"],
                "format": "html",
                "frequency": "weekly",
            },
            "compliance": {
                "type": "compliance",
                "standards": [],
                "audit_trail": True,
                "format": "pdf",
                "frequency": "monthly",
            },
            "reliability": {
                "type": "reliability",
                "slo_metrics": [],
                "error_budgets": {},
                "format": "html",
                "frequency": "daily",
            },
            "safety": {
                "type": "safety",
                "safety_metrics": [],
                "incident_reports": True,
                "format": "html",
                "frequency": "daily",
            },
        }

        result = base_configs.get(report_type, {"type": report_type})
        if not isinstance(result, dict):
            result = {"type": report_type}
        return result

    def list_available_configs(self) -> List[str]:
        """List all available configuration files"""
        config_files = []
        config_path = Path(self.config_dir)

        if config_path.exists():
            for file_path in config_path.rglob("*.yaml"):
                config_files.append(str(file_path))
            for file_path in config_path.rglob("*.yml"):
                config_files.append(str(file_path))
            for file_path in config_path.rglob("*.json"):
                config_files.append(str(file_path))

        return config_files

    def clear_cache(self):
        """Clear the configuration cache"""
        self._config_cache.clear()

    def get_cached_config(self, config_path: str) -> Optional[Dict[str, Any]]:
        """Get cached configuration if available"""
        return self._config_cache.get(config_path)


class ConfigFactoryError(Exception):
    """Exception raised by ConfigFactory"""

    pass
