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

    def _create_aviation_basic(self) -> dict[str, Any]:
        """Create basic aviation template"""
        return {
            "system": {
                "name": "Aircraft Landing System",
                "persona": "Flight Crew",
                "criticality": "safety_critical",
                "description": "Advanced system for aircraft landing assistance and safety-critical landing decisions",
            },
            "slos": {
                "flight_path_accuracy": {
                    "target": 0.9999,
                    "window": "24h",
                    "description": "Accuracy of autonomous flight path predictions and trajectory optimization",
                },
                "runway_identification": {
                    "target": 0.9995,
                    "window": "24h",
                    "description": "Accuracy of runway detection, classification, and approach path identification",
                },
                "landing_decision_confidence": {
                    "target": 0.99999,
                    "window": "24h",
                    "description": "Confidence level in autonomous landing decisions and safety assessments",
                },
                "system_response_time": {
                    "target": 0.99,
                    "window": "1h",
                    "description": "Proportion of system responses within 500ms for critical flight decisions",
                },
            },
            "safety_thresholds": {
                "decision_confidence_threshold": {
                    "min": 0.95,
                    "description": "Minimum confidence threshold required for autonomous decisions",
                },
                "response_time_p99": {
                    "max": 500,
                    "description": "99th percentile response time for critical flight decisions",
                },
            },
            "collectors": [
                {
                    "type": "online",
                    "endpoints": ["http://flight-systems:8080/metrics"],
                    "metrics": [
                        "flight_path_accuracy",
                        "runway_detection",
                        "weather_assessment",
                    ],
                },
                {
                    "type": "environmental",
                    "sources": ["weather_station", "radar", "gps", "altimeter"],
                },
            ],
            "evaluators": [
                {
                    "type": "safety",
                    "compliance_standards": ["DO-178C"],
                    "critical_metrics": [
                        "landing_decision_confidence",
                        "false_positive_rate",
                    ],
                },
                {
                    "type": "reliability",
                    "error_budget_window": "30d",
                    "critical_metrics": ["system_availability", "flight_path_accuracy"],
                },
            ],
        }

    def _create_aviation_advanced(self) -> dict[str, Any]:
        """Create advanced aviation template"""
        basic = self._create_aviation_basic()
        basic["system"]["name"] = "Advanced Aircraft Landing System"

        # Add more comprehensive SLOs
        basic["slos"].update(
            {
                "weather_condition_assessment": {
                    "target": 0.995,
                    "window": "24h",
                    "description": "Accuracy of weather condition evaluation and impact assessment on landing",
                },
                "obstacle_detection": {
                    "target": 0.9999,
                    "window": "24h",
                    "description": "Accuracy of obstacle detection and avoidance recommendations",
                },
                "false_positive_rate": {
                    "target": 0.001,
                    "window": "7d",
                    "description": "Rate of false positive alerts for safety-critical scenarios",
                },
                "system_availability": {
                    "target": 0.9999,
                    "window": "30d",
                    "description": "System uptime for aircraft landing functionality",
                },
            }
        )

        # Add operating conditions
        basic["operating_conditions"] = {
            "flight_phases": ["approach", "final_approach", "landing", "rollout"],
            "weather_conditions": [
                "clear",
                "fog",
                "rain",
                "crosswind",
                "low_visibility",
            ],
            "runway_types": [
                "asphalt",
                "concrete",
                "grass",
                "short_field",
                "contaminated",
            ],
        }

        # Add more collectors
        basic["collectors"].extend(
            [
                {
                    "type": "offline",
                    "log_paths": ["/var/log/flight-systems/", "/var/log/navigation/"],
                },
                {
                    "type": "regulatory",
                    "standards": ["FAA", "EASA", "ICAO"],
                    "compliance_metrics": ["safety_margins", "operational_limits"],
                },
            ]
        )

        # Add more evaluators
        basic["evaluators"].extend(
            [
                {
                    "type": "performance",
                    "metrics": ["system_response_time", "decision_confidence"],
                    "real_time_threshold": 500,
                },
                {
                    "type": "drift",
                    "detection_methods": ["statistical", "ml_model"],
                    "drift_metrics": [
                        "flight_path_accuracy",
                        "weather_assessment",
                        "runway_identification",
                    ],
                },
            ]
        )

        # Add reports
        basic["reports"] = [
            {
                "type": "safety",
                "frequency": "daily",
                "stakeholders": [
                    "flight_crew",
                    "safety_officer",
                    "regulatory_authority",
                ],
            },
            {
                "type": "reliability",
                "frequency": "weekly",
                "stakeholders": ["maintenance_crew", "operations_manager"],
            },
        ]

        return basic

    def _create_energy_basic(self) -> dict[str, Any]:
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
                    "description": "Grid stability prediction accuracy",
                    "safety_critical": True,
                    "compliance_standard": "IEC-61508",
                },
                "response_time": {
                    "target": 50,
                    "window": "5m",
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
                    "slos": {
                        "grid_stability": {
                            "target": 0.995,
                            "window": "1h",
                            "description": "Grid stability prediction accuracy",
                        },
                        "emergency_response": {
                            "target": 50,
                            "window": "5m",
                            "description": "Emergency response time (ms)",
                        },
                    },
                },
            ],
        }

    def _create_energy_advanced(self) -> dict[str, Any]:
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

    def _create_manufacturing_basic(self) -> dict[str, Any]:
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
                    "description": "Quality control accuracy",
                    "safety_critical": False,
                    "compliance_standard": "ISO-13485",
                },
                "throughput": {
                    "target": 1000,
                    "window": "1h",
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
                },
            ],
        }

    def _create_manufacturing_advanced(self) -> dict[str, Any]:
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

    def _create_maritime_basic(self) -> dict[str, Any]:
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
                    "description": "Collision avoidance accuracy",
                    "safety_critical": True,
                    "compliance_standard": "SOLAS",
                },
                "navigation_accuracy": {
                    "target": 0.98,
                    "window": "24h",
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
                    "error_budget_window": "30d",
                    "slos": {
                        "collision_avoidance": {
                            "target": 0.99,
                            "window": "1h",
                            "description": "Collision avoidance accuracy",
                        },
                        "navigation_accuracy": {
                            "target": 0.98,
                            "window": "24h",
                            "description": "Navigation system accuracy",
                        },
                    },
                },
            ],
        }

    def _create_maritime_advanced(self) -> dict[str, Any]:
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
