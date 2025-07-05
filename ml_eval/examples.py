"""Example configurations and implementations"""

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
