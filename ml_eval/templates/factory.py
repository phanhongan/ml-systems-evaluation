"""Template factory for generating industry-specific configurations"""

import logging
from typing import Dict, Any, Optional

from ..core.types import IndustryType, SystemType, CriticalityLevel


class TemplateFactory:
    """Factory for creating industry-specific configuration templates"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """Load all available templates"""
        return {
            "manufacturing": {
                "quality_control": self._manufacturing_quality_control(),
                "predictive_maintenance": self._manufacturing_predictive_maintenance()
            },
            "aviation": {
                "safety_decision": self._aviation_safety_decision(),
                "flight_control": self._aviation_flight_control()
            },
            "energy": {
                "grid_optimization": self._energy_grid_optimization(),
                "demand_prediction": self._energy_demand_prediction()
            },
            "healthcare": {
                "medical_diagnosis": self._healthcare_medical_diagnosis(),
                "patient_monitoring": self._healthcare_patient_monitoring()
            },
            "financial": {
                "fraud_detection": self._financial_fraud_detection(),
                "risk_assessment": self._financial_risk_assessment()
            },
            "automotive": {
                "autonomous_driving": self._automotive_autonomous_driving(),
                "vehicle_safety": self._automotive_vehicle_safety()
            }
        }
        
    def get_template(self, industry: str, template_type: str) -> Optional[Dict[str, Any]]:
        """Get a specific template"""
        try:
            return self.templates[industry][template_type]
        except KeyError:
            self.logger.error(f"Template not found: {industry}/{template_type}")
            return None
            
    def list_industries(self) -> list:
        """List all available industries"""
        return list(self.templates.keys())
        
    def list_templates(self, industry: str) -> list:
        """List all templates for an industry"""
        try:
            return list(self.templates[industry].keys())
        except KeyError:
            return []
            
    def _manufacturing_quality_control(self) -> Dict[str, Any]:
        """Manufacturing quality control template"""
        return {
            "system": {
                "name": "Manufacturing Quality Control System",
                "type": "workflow",
                "stages": ["data_collection", "quality_prediction", "defect_detection", "alert_generation"],
                "criticality": "business_critical"
            },
            "slos": {
                "defect_detection_accuracy": {
                    "target": 0.98,
                    "window": "24h",
                    "error_budget": 0.02,
                    "description": "Accuracy in detecting manufacturing defects"
                },
                "prediction_latency": {
                    "target": 100,
                    "window": "1h",
                    "error_budget": 0.05,
                    "description": "Time to predict quality issues (ms)"
                },
                "false_positive_rate": {
                    "target": 0.01,
                    "window": "24h",
                    "error_budget": 0.01,
                    "description": "Rate of false defect alerts"
                }
            },
            "collectors": [
                {
                    "type": "online",
                    "endpoint": "http://manufacturing-metrics:9090"
                },
                {
                    "type": "offline",
                    "log_paths": ["/var/log/quality-control/"]
                }
            ],
            "evaluators": [
                {
                    "type": "reliability",
                    "error_budget_window": "30d"
                },
                {
                    "type": "performance",
                    "metrics": ["accuracy", "latency"]
                }
            ]
        }
        
    def _aviation_safety_decision(self) -> Dict[str, Any]:
        """Aviation safety decision template"""
        return {
            "system": {
                "name": "Aviation Safety Decision System",
                "type": "single_model",
                "criticality": "safety_critical"
            },
            "slos": {
                "decision_accuracy": {
                    "target": 0.9999,
                    "window": "24h",
                    "error_budget": 0.0001,
                    "description": "Accuracy of safety-critical decisions",
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
            },
            "collectors": [
                {
                    "type": "online",
                    "endpoint": "http://aviation-system:8080/metrics"
                }
            ],
            "evaluators": [
                {
                    "type": "reliability",
                    "error_budget_window": "7d"
                },
                {
                    "type": "safety",
                    "compliance_standards": ["DO-178C"]
                }
            ]
        }
        
    def _energy_grid_optimization(self) -> Dict[str, Any]:
        """Energy grid optimization template"""
        return {
            "system": {
                "name": "Energy Grid Optimization System",
                "type": "workflow",
                "stages": ["demand_prediction", "supply_optimization", "grid_balancing"],
                "criticality": "business_critical"
            },
            "slos": {
                "prediction_accuracy": {
                    "target": 0.95,
                    "window": "24h",
                    "error_budget": 0.05,
                    "description": "Demand prediction accuracy"
                },
                "optimization_latency": {
                    "target": 300,
                    "window": "1h",
                    "error_budget": 0.02,
                    "description": "Grid optimization response time (ms)"
                }
            },
            "collectors": [
                {
                    "type": "online",
                    "endpoint": "http://energy-metrics:9090"
                }
            ],
            "evaluators": [
                {
                    "type": "reliability",
                    "error_budget_window": "30d"
                }
            ]
        }
        
    # Additional template methods would be implemented here
    def _manufacturing_predictive_maintenance(self) -> Dict[str, Any]:
        return {"system": {"name": "Predictive Maintenance System"}}
        
    def _aviation_flight_control(self) -> Dict[str, Any]:
        return {"system": {"name": "Flight Control System"}}
        
    def _energy_demand_prediction(self) -> Dict[str, Any]:
        return {"system": {"name": "Demand Prediction System"}}
        
    def _healthcare_medical_diagnosis(self) -> Dict[str, Any]:
        return {"system": {"name": "Medical Diagnosis System"}}
        
    def _healthcare_patient_monitoring(self) -> Dict[str, Any]:
        return {"system": {"name": "Patient Monitoring System"}}
        
    def _financial_fraud_detection(self) -> Dict[str, Any]:
        return {"system": {"name": "Fraud Detection System"}}
        
    def _financial_risk_assessment(self) -> Dict[str, Any]:
        return {"system": {"name": "Risk Assessment System"}}
        
    def _automotive_autonomous_driving(self) -> Dict[str, Any]:
        return {"system": {"name": "Autonomous Driving System"}}
        
    def _automotive_vehicle_safety(self) -> Dict[str, Any]:
        return {"system": {"name": "Vehicle Safety System"}} 