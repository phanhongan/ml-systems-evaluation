"""Base evaluator interface for ML Systems Evaluation"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseEvaluator(ABC):
    """Base class for all evaluators"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def evaluate(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate metrics and return results"""
        pass

    @abstractmethod
    def get_required_metrics(self) -> List[str]:
        """Get list of required metrics for this evaluator"""
        pass

    def validate_metrics(self, metrics: Dict[str, Any]) -> bool:
        """Validate that required metrics are present"""
        required = self.get_required_metrics()
        missing = [metric for metric in required if metric not in metrics]

        if missing:
            return False

        return True
