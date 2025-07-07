"""Base evaluator interface for ML Systems Evaluation"""

from abc import ABC, abstractmethod
from typing import Any


class BaseEvaluator(ABC):
    """Base class for all evaluators"""

    def __init__(self, config: dict[str, Any]):
        self.config = config

    @abstractmethod
    def evaluate(self, metrics: dict[str, Any]) -> dict[str, Any]:
        """Evaluate metrics and return results"""

    @abstractmethod
    def get_required_metrics(self) -> list[str]:
        """Get list of required metrics for this evaluator"""

    def validate_metrics(self, metrics: dict[str, Any]) -> bool:
        """Validate that required metrics are present"""
        required = self.get_required_metrics()
        missing = [metric for metric in required if metric not in metrics]

        return not missing
