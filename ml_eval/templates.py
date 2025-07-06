"""Industry-specific configuration templates for Industrial ML Systems Evaluation"""

import yaml
from typing import Dict, Any

# Manufacturing Industry Templates
MANUFACTURING_TEMPLATES = {
    "quality_control": {
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
            {"type": "online", "endpoint": "http://manufacturing-metrics:9090"},
            {"type": "offline", "log_paths": ["/var/log/quality-control/"]}
        ],
        "evaluators": [
            {"type": "reliability", "error_budget_window": "30d"},
            {"type": "performance", "metrics": ["accuracy", "latency"]}
        ]
    },
    "predictive_maintenance": {
        "system": {
            "name": "Predictive Maintenance System",
            "type": "workflow",
            "stages": ["sensor_data", "anomaly_detection", "failure_prediction", "maintenance_alert"],
            "criticality": "business_critical"
        },
        "slos": {
            "failure_prediction_accuracy": {
                "target": 0.95,
                "window": "24h",
                "error_budget": 0.05,
                "description": "Accuracy in predicting equipment failures"
            },
            "prediction_horizon": {
                "target": 72,
                "window": "24h",
                "error_budget": 0.1,
                "description": "Hours ahead of failure to predict"
            }
        },
        "collectors": [
            {"type": "online", "endpoint": "http://equipment-sensors:9090"},
            {"type": "offline", "log_paths": ["/var/log/maintenance/"]}
        ],
        "evaluators": [
            {"type": "reliability", "error_budget_window": "30d"},
            {"type": "performance", "metrics": ["accuracy", "prediction_horizon"]}
        ]
    }
}

# Aviation Industry Templates
AVIATION_TEMPLATES = {
    "safety_decision": {
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
            },
            "availability": {
                "target": 0.99999,
                "window": "30d",
                "error_budget": 0.00001,
                "description": "System availability",
                "safety_critical": True
            }
        },
        "collectors": [
            {"type": "online", "endpoint": "http://aviation-system:8080/metrics"}
        ],
        "evaluators": [
            {"type": "reliability", "error_budget_window": "7d"},
            {"type": "safety", "compliance_standards": ["DO-178C"]}
        ]
    },
    "flight_control": {
        "system": {
            "name": "Flight Control Assistance System",
            "type": "single_model",
            "criticality": "safety_critical"
        },
        "slos": {
            "control_accuracy": {
                "target": 0.9995,
                "window": "24h",
                "error_budget": 0.0005,
                "description": "Accuracy of flight control decisions",
                "compliance_standard": "DO-178C",
                "safety_critical": True
            },
            "response_latency": {
                "target": 10,
                "window": "1h",
                "error_budget": 0.001,
                "description": "Control response time (ms)",
                "safety_critical": True
            }
        },
        "collectors": [
            {"type": "online", "endpoint": "http://flight-control:8080/metrics"}
        ],
        "evaluators": [
            {"type": "reliability", "error_budget_window": "7d"},
            {"type": "safety", "compliance_standards": ["DO-178C"]}
        ]
    }
}



# Energy Industry Templates
ENERGY_TEMPLATES = {
    "grid_optimization": {
        "system": {
            "name": "Power Grid Optimization System",
            "type": "workflow",
            "stages": ["demand_prediction", "supply_optimization", "grid_balancing", "outage_prevention"],
            "criticality": "business_critical"
        },
        "slos": {
            "demand_prediction_accuracy": {
                "target": 0.95,
                "window": "24h",
                "error_budget": 0.05,
                "description": "Accuracy in predicting power demand"
            },
            "optimization_latency": {
                "target": 1000,
                "window": "1h",
                "error_budget": 0.1,
                "description": "Grid optimization response time (ms)"
            }
        },
        "collectors": [
            {"type": "online", "endpoint": "http://grid-metrics:9090"},
            {"type": "offline", "log_paths": ["/var/log/grid-operations/"]}
        ],
        "evaluators": [
            {"type": "reliability", "error_budget_window": "30d"},
            {"type": "performance", "metrics": ["accuracy", "latency"]}
        ]
    }
}





# Template registry
TEMPLATE_REGISTRY = {
    "manufacturing": MANUFACTURING_TEMPLATES,
    "aviation": AVIATION_TEMPLATES,
    "energy": ENERGY_TEMPLATES
}

def get_template(industry: str, template_type: str = None) -> Dict[str, Any]:
    """Get industry-specific template configuration"""
    if industry not in TEMPLATE_REGISTRY:
        raise ValueError(f"Industry '{industry}' not supported. Available: {list(TEMPLATE_REGISTRY.keys())}")
    
    templates = TEMPLATE_REGISTRY[industry]
    
    if template_type is None:
        # Return the first template as default
        return list(templates.values())[0]
    
    if template_type not in templates:
        available = list(templates.keys())
        raise ValueError(f"Template type '{template_type}' not found for {industry}. Available: {available}")
    
    return templates[template_type]

def list_available_templates() -> Dict[str, list]:
    """List all available templates by industry"""
    return {industry: list(templates.keys()) for industry, templates in TEMPLATE_REGISTRY.items()}

def save_template(template: Dict[str, Any], output_file: str) -> None:
    """Save template to YAML file"""
    yaml_content = yaml.dump(template, default_flow_style=False, indent=2)
    with open(output_file, 'w') as f:
        # Ensure only one newline at the end
        f.write(yaml_content.rstrip('\n') + '\n')

def print_template(template: Dict[str, Any], industry: str, template_type: str = None) -> None:
    """Print template in a formatted way"""
    title = f"{industry.title()} Configuration Template"
    if template_type:
        title += f" - {template_type.replace('_', ' ').title()}"
    
    print(title)
    print("=" * len(title))
    print(yaml.dump(template, default_flow_style=False, indent=2)) 