"""Example registry for ML Systems Evaluation"""

import logging
from typing import Dict, Any, Optional


class ExampleRegistry:
    """Registry for example configurations and use cases"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.examples = self._load_examples()
        
    def _load_examples(self) -> Dict[str, Dict[str, Any]]:
        """Load all available examples"""
        return {
            "aircraft-model": {
                "title": "Aircraft Landing Model",
                "description": "Safety-critical decision model for aircraft landing systems",
                "industry": "aviation",
                "criticality": "safety_critical",
                "config": {
                    "system": {
                        "name": "Aircraft Landing Decision System",
                        "type": "single_model",
                        "criticality": "safety_critical"
                    },
                    "slos": {
                        "decision_accuracy": {
                            "target": 0.9999,
                            "window": "24h",
                            "error_budget": 0.0001,
                            "description": "Accuracy of landing decisions",
                            "compliance_standard": "DO-178C",
                            "safety_critical": True
                        },
                        "response_time": {
                            "target": 50,
                            "window": "1h",
                            "error_budget": 0.01,
                            "description": "Decision response time (ms)",
                            "safety_critical": True
                        }
                    }
                }
            },
            "fish-classification": {
                "title": "Fish Species Classification",
                "description": "Multi-stage ML pipeline for real-time fish species identification",
                "industry": "manufacturing",
                "criticality": "business_critical",
                "config": {
                    "system": {
                        "name": "Fish Species Classification System",
                        "type": "workflow",
                        "stages": ["preprocessing", "feature_extraction", "classification", "optimization"],
                        "criticality": "business_critical"
                    },
                    "slos": {
                        "classification_accuracy": {
                            "target": 0.95,
                            "window": "24h",
                            "error_budget": 0.05,
                            "description": "Accuracy in fish species classification"
                        },
                        "pipeline_latency": {
                            "target": 200,
                            "window": "1h",
                            "error_budget": 0.02,
                            "description": "End-to-end processing time (ms)"
                        }
                    }
                }
            }
        }
        
    def get_example(self, example_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific example"""
        try:
            return self.examples[example_id]
        except KeyError:
            self.logger.error(f"Example not found: {example_id}")
            return None
            
    def list_examples(self) -> list:
        """List all available examples"""
        return list(self.examples.keys())
        
    def get_example_config(self, example_id: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific example"""
        example = self.get_example(example_id)
        if example:
            return example.get("config", {})
        return None 