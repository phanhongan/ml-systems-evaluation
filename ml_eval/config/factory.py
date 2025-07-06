"""Configuration factory patterns for ML Systems Evaluation Framework"""

import logging
from typing import Dict, Any, Optional
from pathlib import Path

from .loader import ConfigLoader
from .validator import ConfigValidator


class ConfigFactory:
    """Factory for creating and managing configurations"""
    
    def __init__(self):
        self.loader = ConfigLoader()
        self.validator = ConfigValidator()
        self.logger = logging.getLogger(__name__)
        
    def create_config(self, 
                     system_name: str,
                     system_type: str = "single_model",
                     criticality: str = "operational",
                     industry: Optional[str] = None) -> Dict[str, Any]:
        """Create a new configuration with basic structure"""
        
        config = {
            "system": {
                "name": system_name,
                "type": system_type,
                "criticality": criticality
            },
            "slos": {},
            "collectors": [],
            "evaluators": []
        }
        
        # Add industry-specific defaults
        if industry:
            config = self._add_industry_defaults(config, industry)
            
        return config
        
    def create_from_template(self, industry: str, template_type: str) -> Dict[str, Any]:
        """Create configuration from industry template"""
        try:
            template = self.loader.load_template(industry, template_type)
            
            # Validate the template
            if not self.validator.validate_config(template):
                self.logger.error("Template validation failed")
                return {}
                
            return template
            
        except Exception as e:
            self.logger.error(f"Failed to create config from template {industry}/{template_type}: {e}")
            return {}
            
    def create_safety_critical_config(self, system_name: str) -> Dict[str, Any]:
        """Create a safety-critical system configuration"""
        
        config = self.create_config(
            system_name=system_name,
            system_type="single_model",
            criticality="safety_critical"
        )
        
        # Add safety-critical SLOs
        config["slos"].update({
            "safety_accuracy": {
                "target": 0.9999,
                "window": "24h",
                "error_budget": 0.0001,
                "description": "Safety-critical decision accuracy",
                "safety_critical": True,
                "compliance_standard": "DO-178C"
            },
            "response_time": {
                "target": 50,
                "window": "1h",
                "error_budget": 0.01,
                "description": "Decision response time (ms)",
                "safety_critical": True
            }
        })
        
        # Add safety evaluators
        config["evaluators"].extend([
            {
                "type": "safety",
                "compliance_standards": ["DO-178C"]
            },
            {
                "type": "reliability",
                "error_budget_window": "7d"
            }
        ])
        
        return config
        
    def create_business_critical_config(self, system_name: str) -> Dict[str, Any]:
        """Create a business-critical system configuration"""
        
        config = self.create_config(
            system_name=system_name,
            system_type="workflow",
            criticality="business_critical"
        )
        
        # Add business-critical SLOs
        config["slos"].update({
            "accuracy": {
                "target": 0.98,
                "window": "24h",
                "error_budget": 0.02,
                "description": "System accuracy",
                "business_impact": "millions_per_hour"
            },
            "availability": {
                "target": 0.999,
                "window": "30d",
                "error_budget": 0.001,
                "description": "System availability",
                "business_impact": "operational_disruption"
            }
        })
        
        # Add business evaluators
        config["evaluators"].extend([
            {
                "type": "reliability",
                "error_budget_window": "30d"
            },
            {
                "type": "performance",
                "metrics": ["accuracy", "latency"]
            }
        ])
        
        return config
        
    def create_operational_config(self, system_name: str) -> Dict[str, Any]:
        """Create an operational system configuration"""
        
        config = self.create_config(
            system_name=system_name,
            system_type="single_model",
            criticality="operational"
        )
        
        # Add operational SLOs
        config["slos"].update({
            "accuracy": {
                "target": 0.95,
                "window": "24h",
                "error_budget": 0.05,
                "description": "System accuracy"
            },
            "latency": {
                "target": 1000,
                "window": "1h",
                "error_budget": 0.1,
                "description": "Response time (ms)"
            }
        })
        
        # Add operational evaluators
        config["evaluators"].extend([
            {
                "type": "reliability",
                "error_budget_window": "30d"
            }
        ])
        
        return config
        
    def _add_industry_defaults(self, config: Dict[str, Any], industry: str) -> Dict[str, Any]:
        """Add industry-specific defaults to configuration"""
        
        industry_defaults = {
            "manufacturing": {
                "collectors": [
                    {
                        "type": "online",
                        "endpoint": "http://manufacturing-metrics:9090"
                    }
                ],
                "evaluators": [
                    {
                        "type": "reliability",
                        "error_budget_window": "30d"
                    }
                ]
            },
            "aviation": {
                "collectors": [
                    {
                        "type": "online",
                        "endpoint": "http://aviation-system:8080/metrics"
                    }
                ],
                "evaluators": [
                    {
                        "type": "safety",
                        "compliance_standards": ["DO-178C"]
                    },
                    {
                        "type": "reliability",
                        "error_budget_window": "7d"
                    }
                ]
            },
            "energy": {
                "collectors": [
                    {
                        "type": "online",
                        "endpoint": "http://energy-grid:9090"
                    }
                ],
                "evaluators": [
                    {
                        "type": "reliability",
                        "error_budget_window": "30d"
                    }
                ]
            }
        }
        
        if industry in industry_defaults:
            defaults = industry_defaults[industry]
            config["collectors"].extend(defaults.get("collectors", []))
            config["evaluators"].extend(defaults.get("evaluators", []))
            
        return config
        
    def validate_and_save(self, config: Dict[str, Any], output_path: str) -> bool:
        """Validate configuration and save to file"""
        
        # Validate configuration
        if not self.validator.validate_config(config):
            self.validator.print_validation_report()
            return False
            
        # Save configuration
        try:
            self.loader.save_config(config, output_path)
            self.logger.info(f"Configuration saved to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            return False 