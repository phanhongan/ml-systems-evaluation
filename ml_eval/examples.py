"""Example configurations and implementations for Industrial ML Systems"""

from typing import Dict, Any

# Fish Species Classification Workflow Configuration
FISH_CLASSIFICATION_WORKFLOW = {
    "system": {
        "name": "Fish Species Classification Pipeline",
        "type": "workflow",
        "stages": [
            "preprocessing",
            "feature_extraction",
            "classification",
            "postprocessing",
        ],
    },
    "slos": {
        "pipeline_accuracy": {"target": 0.95, "window": "24h", "error_budget": 0.05},
        "end_to_end_latency": {"target": 500, "window": "1h", "error_budget": 0.1},
        "data_quality_score": {"target": 0.98, "window": "12h", "error_budget": 0.02},
    },
    "collectors": [
        {"type": "online", "endpoint": "http://pipeline-metrics:9090"},
        {"type": "offline", "log_paths": ["/var/log/fish-pipeline/"]},
    ],
    "evaluators": [
        {"type": "reliability", "error_budget_window": "30d"},
        {"type": "performance", "metrics": ["accuracy", "latency", "throughput"]},
    ],
}

# Aircraft Landing Model Configuration
AIRCRAFT_LANDING_MODEL = {
    "system": {
        "name": "Aircraft Landing Decision Model",
        "type": "single_model",
        "criticality": "safety_critical",
    },
    "slos": {
        "decision_accuracy": {
            "target": 0.9999,
            "window": "24h",
            "error_budget": 0.0001,
        },
        "response_time": {"target": 50, "window": "1h", "error_budget": 0.01},
        "availability": {"target": 0.99999, "window": "30d", "error_budget": 0.00001},
    },
    "safety_thresholds": {
        "false_positive_rate": {"max": 0.001},
        "response_time_p99": {"max": 100},
    },
    "collectors": [
        {"type": "online", "endpoint": "http://aircraft-system:8080/metrics"}
    ],
    "evaluators": [
        {"type": "reliability", "error_budget_window": "7d"},
        {"type": "safety", "compliance_standards": ["DO-178C"]},
    ],
}

# Manufacturing Quality Control Example
MANUFACTURING_QUALITY_CONTROL = {
    "system": {
        "name": "Automotive Quality Control System",
        "type": "workflow",
        "stages": ["image_capture", "defect_detection", "quality_classification", "alert_system"],
        "criticality": "business_critical"
    },
    "slos": {
        "defect_detection_accuracy": {
            "target": 0.98,
            "window": "24h",
            "error_budget": 0.02,
            "description": "Accuracy in detecting manufacturing defects"
        },
        "inspection_speed": {
            "target": 500,
            "window": "1h",
            "error_budget": 0.05,
            "description": "Time to inspect one component (ms)"
        },
        "false_positive_rate": {
            "target": 0.01,
            "window": "24h",
            "error_budget": 0.01,
            "description": "Rate of false defect alerts"
        }
    },
    "collectors": [
        {"type": "online", "endpoint": "http://production-line:9090"},
        {"type": "offline", "log_paths": ["/var/log/quality-control/"]}
    ],
    "evaluators": [
        {"type": "reliability", "error_budget_window": "30d"},
        {"type": "performance", "metrics": ["accuracy", "throughput"]}
    ]
}



# Example registry with descriptions
EXAMPLE_REGISTRY = {
    "fish-workflow": {
        "config": FISH_CLASSIFICATION_WORKFLOW,
        "title": "🐟 Fish Species Classification Workflow",
        "description": "Multi-stage ML pipeline for commercial fishing operations",
        "challenges": [
            "Real-time processing during active fishing",
            "Environmental conditions affect data quality",
            "Regulatory compliance for bycatch prevention"
        ],
        "key_features": [
            "End-to-end pipeline monitoring",
            "Environmental adaptation",
            "Business impact metrics"
        ]
    },
    "aircraft-model": {
        "config": AIRCRAFT_LANDING_MODEL,
        "title": "✈️ Aircraft Landing Decision Model",
        "description": "Safety-critical decision system for aviation",
        "challenges": [
            "Zero tolerance for false positives",
            "Regulatory compliance (DO-178C)",
            "Real-time decision making"
        ],
        "key_features": [
            "Safety validation",
            "Regulatory compliance",
            "Real-time alerting"
        ]
    },
    "manufacturing": {
        "config": MANUFACTURING_QUALITY_CONTROL,
        "title": "🏭 Manufacturing Quality Control",
        "description": "Quality control system for automotive manufacturing",
        "challenges": [
            "High throughput requirements",
            "Defect detection accuracy",
            "Production line integration"
        ],
        "key_features": [
            "High-speed inspection",
            "Defect classification",
            "Production metrics"
        ]
    },

}

def get_example(example_type: str) -> Dict[str, Any]:
    """Get example configuration with metadata"""
    if example_type not in EXAMPLE_REGISTRY:
        available = list(EXAMPLE_REGISTRY.keys())
        raise ValueError(f"Example type '{example_type}' not found. Available: {available}")
    
    return EXAMPLE_REGISTRY[example_type]

def list_available_examples() -> Dict[str, str]:
    """List all available examples with titles"""
    return {key: example["title"] for key, example in EXAMPLE_REGISTRY.items()}

def print_example_details(example_type: str) -> None:
    """Print detailed example information"""
    example = get_example(example_type)
    
    print(example["title"])
    print("=" * len(example["title"]))
    print(f"Description: {example['description']}")
    print()
    
    print("Challenges:")
    for challenge in example["challenges"]:
        print(f"  • {challenge}")
    print()
    
    print("Key Features:")
    for feature in example["key_features"]:
        print(f"  • {feature}")
    print()
    
    print("Configuration:")
    import yaml
    print(yaml.dump(example["config"], default_flow_style=False, indent=2))
