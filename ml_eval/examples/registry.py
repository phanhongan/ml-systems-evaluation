"""Example registry for ML Systems Evaluation"""

import logging
from typing import Any


class ExampleRegistry:
    """Registry for example configurations and use cases"""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.examples = self._load_examples()

    def _load_examples(self) -> dict[str, dict[str, Any]]:
        """Load all available examples"""
        return {
            "aviation": {
                "name": "Autonomous Flight Guidance System",
                "type": "safety_critical",
                "criticality": "safety_critical",
                "slos": {
                    "flight_path_accuracy": {
                        "target": 0.9999,
                        "window": "24h",
                        "description": "Accuracy of autonomous flight path predictions",
                    },
                    "runway_identification": {
                        "target": 0.9995,
                        "window": "24h",
                        "description": "Accuracy of runway detection and classification",
                    },
                    "landing_decision_confidence": {
                        "target": 0.99999,
                        "window": "24h",
                        "description": "Confidence level in autonomous landing decisions",
                    },
                },
            },
            "energy": {
                "name": "Grid Stability Management System",
                "type": "safety_critical",
                "criticality": "safety_critical",
                "slos": {
                    "grid_stability": {
                        "target": 0.9995,
                        "window": "24h",
                        "description": "Grid stability maintenance",
                    },
                    "demand_forecast": {
                        "target": 0.95,
                        "window": "24h",
                        "description": "Energy demand prediction accuracy",
                    },
                },
            },
        }

    def get_example(self, example_id: str) -> dict[str, Any] | None:
        """Get a specific example"""
        try:
            return self.examples[example_id]
        except KeyError:
            self.logger.error(f"Example not found: {example_id}")
            return None

    def list_examples(self) -> list[str]:
        """List all available examples"""
        return list(self.examples.keys())

    def get_example_config(self, example_id: str) -> dict[str, Any] | None:
        """Get configuration for a specific example"""
        example = self.get_example(example_id)
        if example:
            return example.get("config", {})
        return None
