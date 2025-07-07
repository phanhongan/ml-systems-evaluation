"""Base collector interface for ML Systems Evaluation"""

import logging
from abc import ABC, abstractmethod
from typing import Any

from ..core.config import MetricData


class BaseCollector(ABC):
    """Abstract base for all metric collectors in Industrial AI systems"""

    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.name = config.get("name", self.__class__.__name__)
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def collect(self) -> dict[str, list[MetricData]]:
        """Collect and return metrics with industrial context"""

    @abstractmethod
    def health_check(self) -> bool:
        """Check collector health and operational status"""

    def validate_config(self) -> bool:
        """Validate collector configuration"""
        required_fields = self.get_required_config_fields()
        missing_fields = [
            field for field in required_fields if field not in self.config
        ]

        if missing_fields:
            self.logger.error(
                f"Missing required configuration fields: {missing_fields}"
            )
            return False

        return True

    def get_required_config_fields(self) -> list[str]:
        """Get list of required configuration fields"""
        return []

    def get_collector_info(self) -> dict[str, Any]:
        """Get information about this collector"""
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "config": self.config,
            "healthy": self.health_check(),
        }

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(config={self.config})"
