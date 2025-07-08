"""Configuration factory for ML Systems Evaluation Framework"""

import os
from pathlib import Path
from typing import Any

from ..templates import TemplateManager
from .loader import ConfigLoader
from .validator import ConfigValidator


class ConfigFactory:
    """Factory for creating and managing configuration objects"""

    def __init__(self, config_dir: str | None = None):
        self.config_dir = config_dir or os.getcwd()
        self.loader = ConfigLoader()
        self.validator = ConfigValidator()
        self.template_manager = TemplateManager()
        self._config_cache: dict[str, dict[str, Any]] = {}

    def create_config(self, config_path: str) -> dict[str, Any]:
        """Create configuration from file or directory"""
        try:
            # Check if config is already cached
            if config_path in self._config_cache:
                return self._config_cache[config_path]

            # Load configuration
            config = self.loader.load_config(config_path)

            # Validate configuration
            if not self.validator.validate_config(config):
                errors = self.validator.get_errors()
                raise ValueError(f"Configuration validation failed: {errors}")

            # Cache the configuration
            self._config_cache[config_path] = config

            return config

        except Exception as e:
            raise ConfigFactoryError(
                f"Failed to create config from {config_path}: {e}"
            ) from e

    def create_collector_config(self, collector_type: str, **kwargs) -> dict[str, Any]:
        """Create configuration for a specific collector type"""
        # Try to get from template first
        try:
            base_config = self.template_manager.get_template(
                "base", f"collector_{collector_type}"
            )
        except ValueError:
            # Fallback to hardcoded config
            base_config = self._get_base_collector_config(collector_type)

        # Merge with provided kwargs
        config = {**base_config, **kwargs}

        # Validate collector-specific configuration
        if not self.validator.validate_config(config):
            errors = self.validator.get_errors()
            raise ValueError(f"Collector config validation failed: {errors}")

        return config

    def create_evaluator_config(self, evaluator_type: str, **kwargs) -> dict[str, Any]:
        """Create configuration for a specific evaluator type"""
        # Try to get from template first
        try:
            base_config = self.template_manager.get_template(
                "base", f"evaluator_{evaluator_type}"
            )
        except ValueError:
            # Fallback to hardcoded config
            base_config = self._get_base_evaluator_config(evaluator_type)

        # Merge with provided kwargs
        config = {**base_config, **kwargs}

        # Validate evaluator-specific configuration
        if not self.validator.validate_config(config):
            errors = self.validator.get_errors()
            raise ValueError(f"Evaluator config validation failed: {errors}")

        return config

    def create_report_config(self, report_type: str, **kwargs) -> dict[str, Any]:
        """Create configuration for a specific report type"""
        # Try to get from template first
        try:
            base_config = self.template_manager.get_template(
                "base", f"report_{report_type}"
            )
        except ValueError:
            # Fallback to hardcoded config
            base_config = self._get_base_report_config(report_type)

        # Merge with provided kwargs
        config = {**base_config, **kwargs}

        # Validate report-specific configuration
        if not self.validator.validate_config(config):
            errors = self.validator.get_errors()
            raise ValueError(f"Report config validation failed: {errors}")

        return config

    def _get_base_collector_config(self, collector_type: str) -> dict[str, Any]:
        """Get base configuration for a collector type from template"""
        try:
            return self.template_manager.get_template(
                "base", f"collector_{collector_type}"
            )
        except Exception as e:
            raise ValueError(
                f"No template found for collector type '{collector_type}': {e}"
            ) from e

    def _get_base_evaluator_config(self, evaluator_type: str) -> dict[str, Any]:
        """Get base configuration for an evaluator type from template"""
        try:
            return self.template_manager.get_template(
                "base", f"evaluator_{evaluator_type}"
            )
        except Exception as e:
            raise ValueError(
                f"No template found for evaluator type '{evaluator_type}': {e}"
            ) from e

    def _get_base_report_config(self, report_type: str) -> dict[str, Any]:
        """Get base configuration for a report type from template"""
        try:
            return self.template_manager.get_template("base", f"report_{report_type}")
        except Exception as e:
            raise ValueError(
                f"No template found for report type '{report_type}': {e}"
            ) from e

    def list_available_configs(self) -> list[str]:
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

    def clear_cache(self) -> None:
        """Clear the configuration cache"""
        self._config_cache.clear()

    def get_cached_config(self, config_path: str) -> dict[str, Any] | None:
        """Get cached configuration if available"""
        return self._config_cache.get(config_path)

    def create_template_files(self, output_dir: str | None = None) -> list[str]:
        """Create external template files from hardcoded configurations"""
        created_files = []

        # Create base collector templates
        collector_types = ["environmental", "offline", "online", "regulatory"]
        for collector_type in collector_types:
            self._get_base_collector_config(collector_type)
            file_path = self.template_manager.create_template_file(
                "base",
                f"collector_{collector_type}",
                output_dir and f"{output_dir}/base-collector_{collector_type}.yaml",
            )
            created_files.append(file_path)

        # Create base evaluator templates
        evaluator_types = [
            "performance",
            "reliability",
            "safety",
            "compliance",
            "drift",
        ]
        for evaluator_type in evaluator_types:
            self._get_base_evaluator_config(evaluator_type)
            file_path = self.template_manager.create_template_file(
                "base",
                f"evaluator_{evaluator_type}",
                output_dir and f"{output_dir}/base-evaluator_{evaluator_type}.yaml",
            )
            created_files.append(file_path)

        # Create base report templates
        report_types = ["business", "compliance", "reliability", "safety"]
        for report_type in report_types:
            self._get_base_report_config(report_type)
            file_path = self.template_manager.create_template_file(
                "base",
                f"report_{report_type}",
                output_dir and f"{output_dir}/base-report_{report_type}.yaml",
            )
            created_files.append(file_path)

        return created_files

    def _validate_collector(self, collector: dict[str, Any]) -> bool:
        """Validate a collector configuration"""
        return isinstance(collector, dict)

    def _validate_evaluator(self, evaluator: dict[str, Any]) -> bool:
        """Validate an evaluator configuration"""
        return isinstance(evaluator, dict)

    def _validate_report(self, report: dict[str, Any]) -> bool:
        """Validate a report configuration"""
        return isinstance(report, dict)


class ConfigFactoryError(Exception):
    """Exception raised by ConfigFactory"""
