"""Template factory for generating industry-specific configurations"""

from typing import Any, Dict


class TemplateFactory:
    """Factory for creating industry-specific configuration templates"""

    def __init__(self):
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load industry-specific templates"""
        return {
            "aviation": {
                "basic": self._create_aviation_basic(),
                "advanced": self._create_aviation_advanced(),
            },
            "energy": {
                "basic": self._create_energy_basic(),
                "advanced": self._create_energy_advanced(),
            },
            "manufacturing": {
                "basic": self._create_manufacturing_basic(),
                "advanced": self._create_manufacturing_advanced(),
            },
            "maritime": {
                "basic": self._create_maritime_basic(),
                "advanced": self._create_maritime_advanced(),
            },
        }

    def get_template(self, industry: str, template_type: str) -> Dict[str, Any]:
        """Get a specific template"""
        if industry not in self.templates:
            raise ValueError(f"Unknown industry: {industry}")

        if template_type not in self.templates[industry]:
            raise ValueError(f"Unknown template type: {template_type}")

        return self.templates[industry][template_type]

    def list_industries(self) -> list:
        """List available industries"""
        return list(self.templates.keys())

    def list_template_types(self, industry: str) -> list:
        """List available template types for an industry"""
        if industry not in self.templates:
            return []
        return list(self.templates[industry].keys())

    def _create_aviation_basic(self) -> Dict[str, Any]:
        """Create basic aviation template"""
        return {
            "system": {
                "name": "Aviation ML System",
                "type": "single_model",
                "criticality": "safety_critical",
            },
            "slos": {
                "accuracy": {
                    "target": 0.99,
                    "window": "24h",
                    "error_budget": 0.001,
                    "description": "Model accuracy for flight safety",
                    "safety_critical": True,
                    "compliance_standard": "DO-178C",
                },
                "latency": {
                    "target": 100,
                    "window": "1h",
                    "error_budget": 0.01,
                    "description": "Inference latency (ms)",
                    "safety_critical": True,
                },
            },
            "collectors": [
                {
                    "type": "online",
                    "endpoint": "http://aviation-system:8080/metrics",
                },
                {
                    "type": "environmental",
                    "sensor_types": ["temperature", "pressure", "humidity"],
                },
            ],
            "evaluators": [
                {
                    "type": "safety",
                    "compliance_standards": ["DO-178C"],
                },
                {
                    "type": "reliability",
                    "error_budget_window": "7d",
                },
            ],
        }

    def _create_aviation_advanced(self) -> Dict[str, Any]:
        """Create advanced aviation template"""
        basic = self._create_aviation_basic()
        basic["system"]["name"] = "Advanced Aviation ML System"
        basic["collectors"].append(
            {
                "type": "regulatory",
                "compliance_standards": ["DO-178C", "ISO-26262"],
            }
        )
        return basic

    def _create_energy_basic(self) -> Dict[str, Any]:
        """Create basic energy template"""
        return {
            "system": {
                "name": "Energy Grid ML System",
                "type": "workflow",
                "criticality": "safety_critical",
            },
            "slos": {
                "grid_stability": {
                    "target": 0.995,
                    "window": "1h",
                    "error_budget": 0.005,
                    "description": "Grid stability prediction accuracy",
                    "safety_critical": True,
                    "compliance_standard": "IEC-61508",
                },
                "response_time": {
                    "target": 50,
                    "window": "5m",
                    "error_budget": 0.001,
                    "description": "Emergency response time (ms)",
                    "safety_critical": True,
                },
            },
            "collectors": [
                {
                    "type": "online",
                    "endpoint": "http://energy-grid:9090",
                },
                {
                    "type": "environmental",
                    "sensor_types": ["temperature", "pressure"],
                },
            ],
            "evaluators": [
                {
                    "type": "safety",
                    "compliance_standards": ["IEC-61508"],
                },
                {
                    "type": "reliability",
                    "error_budget_window": "30d",
                },
            ],
        }

    def _create_energy_advanced(self) -> Dict[str, Any]:
        """Create advanced energy template"""
        basic = self._create_energy_basic()
        basic["system"]["name"] = "Advanced Energy Grid ML System"
        basic["collectors"].append(
            {
                "type": "regulatory",
                "compliance_standards": ["IEC-61508", "ISO-13849"],
            }
        )
        return basic

    def _create_manufacturing_basic(self) -> Dict[str, Any]:
        """Create basic manufacturing template"""
        return {
            "system": {
                "name": "Manufacturing ML System",
                "type": "workflow",
                "criticality": "business_critical",
            },
            "slos": {
                "quality_control": {
                    "target": 0.95,
                    "window": "8h",
                    "error_budget": 0.05,
                    "description": "Quality control accuracy",
                    "safety_critical": False,
                    "compliance_standard": "ISO-13485",
                },
                "throughput": {
                    "target": 1000,
                    "window": "1h",
                    "error_budget": 0.1,
                    "description": "Production throughput (units/hour)",
                    "safety_critical": False,
                },
            },
            "collectors": [
                {
                    "type": "online",
                    "endpoint": "http://manufacturing-metrics:9090",
                },
                {
                    "type": "environmental",
                    "sensor_types": ["temperature", "humidity", "vibration"],
                },
            ],
            "evaluators": [
                {
                    "type": "performance",
                    "thresholds": {
                        "quality_control": {"target": 0.95, "warning": 0.90},
                        "throughput": {"target": 1000, "warning": 900},
                    },
                },
                {
                    "type": "reliability",
                    "error_budget_window": "30d",
                },
            ],
        }

    def _create_manufacturing_advanced(self) -> Dict[str, Any]:
        """Create advanced manufacturing template"""
        basic = self._create_manufacturing_basic()
        basic["system"]["name"] = "Advanced Manufacturing ML System"
        basic["collectors"].append(
            {
                "type": "regulatory",
                "compliance_standards": ["ISO-13485", "FDA-510K"],
            }
        )
        return basic

    def _create_maritime_basic(self) -> Dict[str, Any]:
        """Create basic maritime template"""
        return {
            "system": {
                "name": "Maritime ML System",
                "type": "workflow",
                "criticality": "safety_critical",
            },
            "slos": {
                "collision_avoidance": {
                    "target": 0.99,
                    "window": "1h",
                    "error_budget": 0.001,
                    "description": "Collision avoidance accuracy",
                    "safety_critical": True,
                    "compliance_standard": "SOLAS",
                },
                "navigation_accuracy": {
                    "target": 0.98,
                    "window": "24h",
                    "error_budget": 0.02,
                    "description": "Navigation system accuracy",
                    "safety_critical": True,
                },
            },
            "collectors": [
                {
                    "type": "online",
                    "endpoint": "http://maritime-system:8080/metrics",
                },
                {
                    "type": "environmental",
                    "sensor_types": ["temperature", "humidity", "pressure"],
                },
            ],
            "evaluators": [
                {
                    "type": "safety",
                    "compliance_standards": ["SOLAS", "MARPOL"],
                },
                {
                    "type": "reliability",
                    "error_budget_window": "7d",
                },
            ],
        }

    def _create_maritime_advanced(self) -> Dict[str, Any]:
        """Create advanced maritime template"""
        basic = self._create_maritime_basic()
        basic["system"]["name"] = "Advanced Maritime ML System"
        basic["collectors"].append(
            {
                "type": "regulatory",
                "compliance_standards": ["SOLAS", "MARPOL"],
            }
        )
        return basic
