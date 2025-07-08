"""Template factory for generating industry-specific configurations"""

from typing import Any


class TemplateFactory:
    """Factory for creating industry-specific configuration templates"""

    def __init__(self) -> None:
        self.templates = self._load_templates()

    def _load_templates(self) -> dict[str, dict[str, Any]]:
        """Load industry-specific templates"""
        return {
            "aviation": {
                "safety_decision": self._create_aviation_safety_decision(),
                "flight_control": self._create_aviation_flight_control(),
            },
            "energy": {
                "grid_optimization": self._create_energy_grid_optimization(),
                "demand_prediction": self._create_energy_demand_prediction(),
            },
            "manufacturing": {
                "predictive_maintenance": self._create_manufacturing_predictive_maintenance(),
                "demand_forecasting": self._create_manufacturing_demand_forecasting(),
            },
            "maritime": {
                "collision_avoidance": self._create_maritime_collision_avoidance(),
                "navigation_system": self._create_maritime_navigation_system(),
            },
            "semiconductor": {
                "digital_twins": self._create_semiconductor_digital_twins(),
                "yield_prediction": self._create_semiconductor_yield_prediction(),
            },
        }

    def get_template(self, industry: str, template_type: str) -> dict[str, Any]:
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

    def _create_aviation_safety_decision(self) -> dict[str, Any]:
        """Create aviation safety decision template"""
        return {
            "system": {
                "name": "Aircraft Safety Decision System",
                "persona": "Flight Crew",
                "criticality": "safety_critical",
                "description": "Safety-critical decision system for aircraft operations",
            },
            "slos": {
                "flight_path_accuracy": {
                    "target": 0.9999,
                    "window": "24h",
                    "description": "Accuracy of autonomous flight path predictions",
                },
                "system_response_time": {
                    "target": 0.99,
                    "window": "1h",
                    "description": "Proportion of system responses within 500ms",
                },
            },
            "collectors": [
                {
                    "type": "online",
                    "endpoints": ["http://flight-systems:8080/metrics"],
                    "metrics": ["flight_path_accuracy", "response_time"],
                },
            ],
            "evaluators": [
                {
                    "type": "safety",
                    "compliance_standards": ["DO-178C"],
                    "critical_metrics": ["flight_path_accuracy"],
                },
            ],
        }

    def _create_aviation_flight_control(self) -> dict[str, Any]:
        """Create aviation flight control template"""
        return {
            "system": {
                "name": "Advanced Aircraft Flight Control System",
                "persona": "Flight Crew",
                "criticality": "safety_critical",
                "description": "Comprehensive flight control system with safety features",
            },
            "slos": {
                "flight_path_accuracy": {
                    "target": 0.9999,
                    "window": "24h",
                    "description": "Accuracy of autonomous flight path predictions",
                },
                "system_response_time": {
                    "target": 0.99,
                    "window": "1h",
                    "description": "Proportion of system responses within 500ms",
                },
                "system_availability": {
                    "target": 0.9999,
                    "window": "30d",
                    "description": "System uptime for flight control functionality",
                },
            },
            "collectors": [
                {
                    "type": "online",
                    "endpoints": ["http://flight-systems:8080/metrics"],
                    "metrics": [
                        "flight_path_accuracy",
                        "response_time",
                        "availability",
                    ],
                },
            ],
            "evaluators": [
                {
                    "type": "safety",
                    "compliance_standards": ["DO-178C"],
                    "critical_metrics": ["flight_path_accuracy"],
                },
                {
                    "type": "reliability",
                    "error_budget_window": "30d",
                    "critical_metrics": ["system_availability"],
                },
            ],
        }

    def _create_energy_grid_optimization(self) -> dict[str, Any]:
        """Create energy grid optimization template"""
        return {
            "system": {
                "name": "Energy Grid Optimization System",
                "persona": "Grid Operator",
                "criticality": "business_critical",
                "description": "ML system for energy grid optimization and load balancing",
            },
            "slos": {
                "load_prediction_accuracy": {
                    "target": 0.95,
                    "window": "24h",
                    "description": "Accuracy of energy demand prediction",
                },
                "response_time": {
                    "target": 0.99,
                    "window": "1h",
                    "description": "Proportion of system responses within 2 seconds",
                },
            },
            "collectors": [
                {
                    "type": "online",
                    "endpoints": ["http://grid-monitor:8080/metrics"],
                    "metrics": ["load_prediction", "response_time"],
                },
            ],
            "evaluators": [
                {
                    "type": "performance",
                    "metrics": ["load_prediction_accuracy", "response_time"],
                },
            ],
        }

    def _create_energy_demand_prediction(self) -> dict[str, Any]:
        """Create energy demand prediction template"""
        return {
            "system": {
                "name": "Energy Demand Prediction System",
                "persona": "Grid Operator",
                "criticality": "business_critical",
                "description": "Energy demand prediction and grid optimization system",
            },
            "slos": {
                "load_prediction_accuracy": {
                    "target": 0.95,
                    "window": "24h",
                    "description": "Accuracy of energy demand prediction",
                },
                "system_availability": {
                    "target": 0.999,
                    "window": "30d",
                    "description": "System uptime for grid optimization",
                },
            },
            "collectors": [
                {
                    "type": "online",
                    "endpoints": ["http://grid-monitor:8080/metrics"],
                    "metrics": ["load_prediction", "availability"],
                },
            ],
            "evaluators": [
                {
                    "type": "performance",
                    "metrics": ["load_prediction_accuracy"],
                },
                {
                    "type": "reliability",
                    "error_budget_window": "30d",
                    "critical_metrics": ["system_availability"],
                },
            ],
        }

    def _create_manufacturing_predictive_maintenance(self) -> dict[str, Any]:
        """Create manufacturing predictive maintenance template"""
        return {
            "system": {
                "name": "Manufacturing Predictive Maintenance System",
                "persona": "Maintenance Engineer",
                "criticality": "business_critical",
                "description": "ML system for manufacturing equipment monitoring",
            },
            "slos": {
                "equipment_failure_prediction": {
                    "target": 0.92,
                    "window": "24h",
                    "description": "Accuracy of equipment failure prediction",
                },
                "system_availability": {
                    "target": 0.999,
                    "window": "30d",
                    "description": "System uptime for maintenance functionality",
                },
            },
            "collectors": [
                {
                    "type": "online",
                    "endpoints": ["http://equipment-monitor:8080/metrics"],
                    "metrics": ["failure_prediction", "availability"],
                },
            ],
            "evaluators": [
                {
                    "type": "performance",
                    "metrics": ["equipment_failure_prediction"],
                },
                {
                    "type": "reliability",
                    "error_budget_window": "30d",
                    "critical_metrics": ["system_availability"],
                },
            ],
        }

    def _create_manufacturing_demand_forecasting(self) -> dict[str, Any]:
        """Create manufacturing demand forecasting template"""
        return {
            "system": {
                "name": "Manufacturing Demand Forecasting System",
                "persona": "Supply Chain Manager",
                "criticality": "business_critical",
                "description": "ML system for manufacturing demand forecasting",
            },
            "slos": {
                "demand_forecast_accuracy": {
                    "target": 0.90,
                    "window": "30d",
                    "description": "Accuracy of demand forecasting",
                },
                "forecast_response_time": {
                    "target": 0.99,
                    "window": "1h",
                    "description": "Proportion of forecast requests completed within 5 minutes",
                },
            },
            "collectors": [
                {
                    "type": "online",
                    "endpoints": ["http://forecast-engine:8080/metrics"],
                    "metrics": ["demand_prediction", "response_time"],
                },
            ],
            "evaluators": [
                {
                    "type": "performance",
                    "metrics": ["demand_forecast_accuracy", "forecast_response_time"],
                },
            ],
        }

    def _create_maritime_collision_avoidance(self) -> dict[str, Any]:
        """Create maritime collision avoidance template"""
        return {
            "system": {
                "name": "Maritime Collision Avoidance System",
                "persona": "Ship Captain",
                "criticality": "safety_critical",
                "description": "Safety-critical collision avoidance system for maritime vessels",
            },
            "slos": {
                "collision_detection_accuracy": {
                    "target": 0.999,
                    "window": "24h",
                    "description": "Accuracy of collision detection and avoidance",
                },
                "response_time": {
                    "target": 0.99,
                    "window": "1h",
                    "description": "Proportion of collision alerts within 2 seconds",
                },
            },
            "collectors": [
                {
                    "type": "online",
                    "endpoints": ["http://maritime-monitor:8080/metrics"],
                    "metrics": ["collision_detection", "response_time"],
                },
            ],
            "evaluators": [
                {
                    "type": "safety",
                    "compliance_standards": ["SOLAS", "COLREGS"],
                    "critical_metrics": ["collision_detection_accuracy"],
                },
            ],
        }

    def _create_maritime_navigation_system(self) -> dict[str, Any]:
        """Create maritime navigation system template"""
        return {
            "system": {
                "name": "Maritime Navigation System",
                "persona": "Ship Captain",
                "criticality": "safety_critical",
                "description": "Maritime navigation and safety system",
            },
            "slos": {
                "collision_detection_accuracy": {
                    "target": 0.999,
                    "window": "24h",
                    "description": "Accuracy of collision detection and avoidance",
                },
                "system_availability": {
                    "target": 0.9999,
                    "window": "30d",
                    "description": "System uptime for navigation functionality",
                },
            },
            "collectors": [
                {
                    "type": "online",
                    "endpoints": ["http://maritime-monitor:8080/metrics"],
                    "metrics": ["collision_detection", "availability"],
                },
            ],
            "evaluators": [
                {
                    "type": "safety",
                    "compliance_standards": ["SOLAS", "COLREGS"],
                    "critical_metrics": ["collision_detection_accuracy"],
                },
                {
                    "type": "reliability",
                    "error_budget_window": "30d",
                    "critical_metrics": ["system_availability"],
                },
            ],
        }

    def _create_semiconductor_digital_twins(self) -> dict[str, Any]:
        """Create minimum viable semiconductor digital twins template"""
        return {
            "system": {
                "name": "Semiconductor Digital Twins System",
                "persona": "Process Engineer",
                "description": "Digital twins for semiconductor etching process monitoring",
            },
            "slos": {
                "yield_prediction_accuracy": {
                    "target": 0.95,
                    "window": "7d",
                    "description": "Accuracy of wafer yield prediction",
                },
            },
            "collectors": [
                {
                    "type": "online",
                    "metrics": ["temperature", "pressure"],
                },
            ],
            "evaluators": [
                {
                    "type": "performance",
                    "metrics": ["yield_prediction_accuracy"],
                },
            ],
        }

    def _create_semiconductor_yield_prediction(self) -> dict[str, Any]:
        """Create minimum viable semiconductor yield prediction template"""
        return {
            "system": {
                "name": "Semiconductor Yield Prediction System",
                "persona": "Process Engineer",
                "description": "ML system for wafer yield prediction",
            },
            "slos": {
                "yield_prediction_accuracy": {
                    "target": 0.95,
                    "window": "7d",
                    "description": "Accuracy of wafer yield prediction",
                },
            },
            "collectors": [
                {
                    "type": "online",
                    "metrics": ["temperature", "pressure"],
                },
            ],
            "evaluators": [
                {
                    "type": "performance",
                    "metrics": ["yield_prediction_accuracy"],
                },
            ],
        }
