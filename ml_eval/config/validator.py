"""Configuration validation for ML Systems Evaluation Framework"""

import logging
from typing import Any

from ..core.types import ComplianceStandard, CriticalityLevel


class ConfigValidator:
    """Configuration validator for Industrial AI systems"""

    def __init__(self) -> None:
        """Initialize validator"""
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.logger = logging.getLogger(__name__)

    def validate_config(self, config: dict[str, Any]) -> bool:
        """Validate complete configuration"""
        self.errors = []
        self.warnings = []

        # Validate basic structure
        if not self._validate_structure(config):
            return False

        # Validate system configuration
        if not self._validate_system_config(config.get("system", {})):
            return False

        # Validate SLOs
        if not self._validate_slos(config.get("slos", {})):
            return False

        # Validate collectors
        if not self._validate_collectors(config.get("collectors", [])):
            return False

        # Validate evaluators
        if not self._validate_evaluators(config.get("evaluators", [])):
            return False

        # Validate industry-specific requirements
        if not self._validate_industry_requirements(config):
            return False

        return len(self.errors) == 0

    def _validate_structure(self, config: dict[str, Any]) -> bool:
        """Validate basic configuration structure"""
        required_sections = ["system", "slos"]
        missing_sections = [
            section for section in required_sections if section not in config
        ]

        if missing_sections:
            self.errors.append(f"Missing required sections: {missing_sections}")
            return False

        return True

    def _validate_system_config(self, system: dict[str, Any]) -> bool:
        """Validate system configuration"""
        if not isinstance(system, dict):
            self.errors.append("System configuration must be a dictionary")
            return False

        # Validate system name
        if "name" not in system:
            self.errors.append("System name is required")
            return False

        # Validate criticality level
        if "criticality" in system:
            try:
                CriticalityLevel(system["criticality"])
            except ValueError:
                self.errors.append(
                    f"Invalid criticality level: {system['criticality']}"
                )
                return False

        return True

    def _validate_slos(self, slos: dict[str, Any]) -> bool:
        """Validate SLO configuration"""
        if not isinstance(slos, dict):
            self.errors.append("SLOs configuration must be a dictionary")
            return False

        for slo_name, slo_config in slos.items():
            if not self._validate_single_slo(slo_name, slo_config):
                return False

        return True

    def _validate_single_slo(self, name: str, config: dict[str, Any]) -> bool:
        """Validate a single SLO configuration"""
        # Check for required fields
        if "target" not in config:
            self.errors.append(f"SLO '{name}' missing required field: target")
            return False

        if "window" not in config:
            self.errors.append(f"SLO '{name}' missing required field: window")
            return False

        # Validate target value
        target = config.get("target")
        if not isinstance(target, int | float) or target < 0 or target > 1:
            self.errors.append(f"SLO '{name}' target must be a number between 0 and 1")
            return False

        # Validate safety-critical requirements
        if config.get("safety_critical", False) and target < 0.999:
            self.errors.append(
                f"Safety-critical SLO '{name}' must have target >= 0.999"
            )
            return False

        # Validate compliance standard
        if "compliance_standard" in config:
            try:
                ComplianceStandard(config["compliance_standard"])
            except ValueError:
                self.errors.append(
                    f"SLO '{name}' has invalid compliance standard: {config['compliance_standard']}"
                )
                return False

        return True

    def _validate_collectors(self, collectors: list[dict[str, Any]]) -> bool:
        """Validate collectors configuration"""
        if not isinstance(collectors, list):
            self.errors.append("Collectors configuration must be a list")
            return False

        for i, collector in enumerate(collectors):
            if not isinstance(collector, dict):
                self.errors.append(f"Collector {i} must be a dictionary")
                return False

            if "type" not in collector:
                self.errors.append(f"Collector {i} missing 'type' field")
                return False

        return True

    def _validate_evaluators(self, evaluators: list[dict[str, Any]]) -> bool:
        """Validate evaluators configuration"""
        if not isinstance(evaluators, list):
            self.errors.append("Evaluators configuration must be a list")
            return False

        for i, evaluator in enumerate(evaluators):
            if not isinstance(evaluator, dict):
                self.errors.append(f"Evaluator {i} must be a dictionary")
                return False

            if "type" not in evaluator:
                self.errors.append(f"Evaluator {i} missing 'type' field")
                return False

        return True

    def _validate_industry_requirements(self, config: dict[str, Any]) -> bool:
        """Validate industry-specific requirements"""
        system = config.get("system", {})
        criticality = system.get("criticality", "operational")

        # Safety-critical systems must have safety evaluators
        if criticality == "safety_critical":
            evaluators = config.get("evaluators", [])
            safety_evaluators = [e for e in evaluators if e.get("type") == "safety"]

            if not safety_evaluators:
                self.errors.append(
                    "Safety-critical systems must include safety evaluators"
                )
                return False

        # Systems with compliance standards must have compliance evaluators
        slos = config.get("slos", {})
        compliance_slos = [
            slo for slo in slos.values() if slo.get("compliance_standard")
        ]

        if compliance_slos:
            evaluators = config.get("evaluators", [])
            compliance_evaluators = [
                e for e in evaluators if e.get("type") == "compliance"
            ]

            if not compliance_evaluators:
                self.warnings.append(
                    "Systems with compliance standards should include "
                    "compliance evaluators"
                )

        return True

    def get_errors(self) -> list[str]:
        """Get validation errors"""
        return self.errors.copy()

    def get_warnings(self) -> list[str]:
        """Get validation warnings"""
        return self.warnings.copy()

    def print_validation_report(self) -> None:
        """Print validation report"""
        if self.errors:
            self.logger.error("Configuration validation failed:")
            for error in self.errors:
                self.logger.error(f"  - {error}")

        if self.warnings:
            self.logger.warning("Configuration warnings:")
            for warning in self.warnings:
                self.logger.warning(f"  - {warning}")

        if not self.errors and not self.warnings:
            self.logger.info("Configuration validation passed")
