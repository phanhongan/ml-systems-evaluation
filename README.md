# ML Systems Evaluation Framework

A reliability-focused evaluation framework for Industrial AI systems, applying Site Reliability Engineering (SRE) principles to machine learning evaluation.

## Philosophy

This framework treats ML systems as critical infrastructure, applying SRE concepts:
- **Error Budgets**: Acceptable failure rates for different system components
- **SLIs/SLOs**: Service Level Indicators and Objectives for ML performance
- **Observability**: Comprehensive monitoring and alerting
- **Reliability**: Focus on system uptime and consistent performance
- **Incident Response**: Structured approach to handling ML system failures

## Key Features

- **Multi-Modal Evaluation**: Support for single models and orchestrated workflows
- **Industrial AI Focus**: Specialized metrics for production environments
- **Reliability-First**: SRE principles applied to ML systems
- **Extensible Architecture**: Plugin-based metric collectors and evaluators
- **Real-time & Batch**: Online and offline evaluation capabilities
- **Standards Enforcement**: Configurable quality gates and requirements

## Supported Scenarios

### Fish Species Classification AI (Workflow Example)
- End-to-end pipeline evaluation: preprocessing → feature extraction → classification → post-processing
- Multi-stage reliability assessment
- Workflow orchestration monitoring
- Data quality validation across pipeline stages

### Aircraft Landing Systems (Single Model Example)
- Critical decision model evaluation
- Real-time safety validation
- Model performance under constraints
- Regulatory compliance verification

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │    │   Collectors    │    │   Evaluators    │
│                 │    │                 │    │                 │
│ • Logs          │───▶│ • Online        │───▶│ • Reliability   │
│ • Metrics       │    │ • Offline       │    │ • Performance   │
│ • Telemetry     │    │ • Custom        │    │ • Safety        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                              ┌─────────────────┐
                                              │    Reports      │
                                              │                 │
                                              │ • SLI/SLO       │
                                              │ • Incidents     │
                                              │ • Trends        │
                                              └─────────────────┘
```

## Quick Start

### Installation
```bash
pip install ml-eval
```

### Basic Usage
```bash
# Evaluate workflow (Fish Species Classification)
ml-eval evaluate --config fish-classification-workflow.yaml --mode workflow

# Evaluate single model (Aircraft Landing)
ml-eval evaluate --config aircraft-landing-model.yaml --mode single

# Generate reliability report
ml-eval report --type reliability --period 30d
```

### Configuration Example
```yaml
# fish-classification-workflow.yaml
system:
  name: "Fish Species Classification Pipeline"
  type: "workflow"
  stages: ["preprocessing", "feature_extraction", "classification", "postprocessing"]
  
slos:
  accuracy: 0.95
  latency_p99: 100ms
  availability: 99.9%

collectors:
  - type: "prometheus"
    endpoint: "http://metrics:9090"
  - type: "logs"
    path: "/var/log/ml-system/"

evaluators:
  - type: "reliability"
    error_budget: 0.1%
  - type: "performance"
    metrics: ["accuracy", "precision", "recall"]
  - type: "drift"
    baseline_period: "7d"
```

## Core Components

### Collectors
- **OnlineCollector**: Real-time metrics from running systems
- **OfflineCollector**: Historical data from logs and databases
- **CustomCollector**: Extensible interface for specialized metrics

### Evaluators
- **ReliabilityEvaluator**: SLI/SLO compliance and error budgets
- **PerformanceEvaluator**: ML-specific performance metrics
- **SafetyEvaluator**: Critical system safety validation
- **DriftEvaluator**: Data and model drift detection

### Reports
- **ReliabilityReport**: Error budgets, SLO compliance, incident analysis
- **PerformanceReport**: Model accuracy, latency, throughput trends
- **SafetyReport**: Safety-critical metrics and compliance status

## SRE Integration

### Service Level Objectives (SLOs)
```yaml
slos:
  model_accuracy:
    target: 0.95
    window: "30d"
    error_budget: 0.05
  
  inference_latency:
    target: "p99 < 100ms"
    window: "24h"
    error_budget: 0.01
    
  system_availability:
    target: 0.999
    window: "30d"
    error_budget: 0.001
```

### Error Budget Policies
- **Burn Rate Alerts**: Fast/slow burn rate detection
- **Budget Exhaustion**: Automatic incident creation
- **Quality Gates**: Deployment blocking on budget violations

## Advanced Features

### Workflow Evaluation
```python
from ml_eval import WorkflowEvaluator

evaluator = WorkflowEvaluator()
evaluator.add_stage("preprocessing", slo_config)
evaluator.add_stage("inference", slo_config)
evaluator.add_stage("postprocessing", slo_config)
result = evaluator.evaluate()
```

### Custom Metrics
```python
from ml_eval.collectors import CustomCollector

class DomainSpecificCollector(CustomCollector):
    def collect(self) -> Dict[str, float]:
        # Custom metric collection logic
        return {"custom_metric": value}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.
