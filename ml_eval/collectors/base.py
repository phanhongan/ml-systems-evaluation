"""Base collector interface for ML Systems Evaluation"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
from datetime import datetime
import logging

from ..core.config import MetricData


class BaseCollector(ABC):
    """Abstract base for all metric collectors in Industrial AI systems"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.name = config.get("name", self.__class__.__name__)

    @abstractmethod
    def collect(self) -> Dict[str, List[MetricData]]:
        """Collect and return metrics with industrial context"""
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check collector health and operational status"""
        pass

    def validate_config(self) -> bool:
        """Validate collector configuration"""
        required_fields = self.get_required_config_fields()
        missing_fields = [field for field in required_fields if field not in self.config]
        
        if missing_fields:
            self.logger.error(f"Missing required configuration fields: {missing_fields}")
            return False
            
        return True

    def get_required_config_fields(self) -> List[str]:
        """Get list of required configuration fields"""
        return []

    def get_collector_info(self) -> Dict[str, Any]:
        """Get information about this collector"""
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "config": self.config,
            "healthy": self.health_check(),
        }

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name})"

    def __repr__(self):
        return f"{self.__class__.__name__}(config={self.config})" 