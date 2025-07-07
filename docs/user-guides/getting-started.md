# Getting Started with ML Systems Evaluation Framework

This guide will help you quickly set up and run your first evaluation using the ML Systems Evaluation Framework.

## Prerequisites

- Python 3.9 or higher
- Poetry package manager (https://python-poetry.org/)
- Access to your ML system's monitoring data
- Basic understanding of your system's architecture

## Installation

### 1. Install the Framework

```bash
# Clone the repository
git clone <repository-url>
cd ml-systems-evaluation

# Install dependencies and the framework
poetry install

# (Optional) Activate the Poetry-managed virtual environment
poetry shell
```

### 2. Verify Installation

```bash
ml-eval --version
```

## Quick Start: Your First Evaluation

### 1. Choose a Template

The framework provides industry-specific templates. For your first evaluation, we recommend starting with a basic template:

```bash
# List available templates
ml-eval templates list

# Use a basic template for manufacturing
ml-eval templates use manufacturing-basic
```

### 2. Configure Your System

Create a configuration file for your system:

```yaml
# config.yaml
system:
  name: "Production Line Quality Control"
  type: "manufacturing"
  criticality: "business-critical"

data_sources:
  - name: "quality_metrics"
    type: "database"
    connection: "postgresql://user:pass@localhost/quality_db"
    tables: ["quality_measurements", "defect_reports"]

collectors:
  - name: "quality_collector"
    type: "offline"
    data_source: "quality_metrics"
    metrics: ["accuracy", "precision", "recall", "f1_score"]

evaluators:
  - name: "performance_evaluator"
    type: "performance"
    thresholds:
      accuracy: 0.95
      precision: 0.90
      recall: 0.85

  - name: "drift_evaluator"
    type: "drift"
    detection_method: "statistical"
    sensitivity: 0.05

reports:
  - name: "business_report"
    type: "business"
    format: "html"
    output_path: "./reports/"

slo:
  availability: 0.999
  accuracy: 0.95
  latency_p95: 100  # milliseconds
```

### 3. Run Your First Evaluation

```bash
# Run a complete evaluation
ml-eval evaluate --config config.yaml

# Run specific components
ml-eval collect --config config.yaml
ml-eval evaluate --config config.yaml --evaluator performance
ml-eval report --config config.yaml --report business
```

### 4. Review Results

Check the generated reports in the `./reports/` directory:

- **Business Report**: High-level metrics and recommendations
- **Performance Report**: Detailed performance analysis
- **Compliance Report**: Regulatory compliance status

## Understanding Your Results

### Key Metrics to Monitor

1. **Accuracy**: Overall prediction accuracy
2. **Precision**: True positive rate
3. **Recall**: Sensitivity of the model
4. **Drift Score**: Data distribution changes
5. **Latency**: Response time percentiles

### Alert Thresholds

The framework automatically alerts you when:
- Performance metrics fall below thresholds
- Data drift is detected
- System availability drops
- Compliance violations occur

## Next Steps

1. **Customize Configuration**: Adapt the template to your specific needs
2. **Set Up Monitoring**: Configure continuous monitoring
3. **Define SLOs**: Establish Service Level Objectives
4. **Create Dashboards**: Visualize your metrics
5. **Set Up Alerts**: Configure notification systems

## Troubleshooting

### Common Issues

**Issue**: "No data found"
- **Solution**: Verify your data source configuration and connection

**Issue**: "Evaluation failed"
- **Solution**: Check your evaluator configuration and thresholds

**Issue**: "Template not found"
- **Solution**: Update to the latest version: `poetry update`

### Getting Help

- Check the [Configuration Guide](configuration.md) for detailed options
- Review [CLI Reference](cli-reference.md) for command details
- Consult [Templates Guide](templates.md) for your specific domain

## Example: Manufacturing Quality Control

Here's a complete example for a manufacturing quality control system:

```yaml
# manufacturing-quality.yaml
system:
  name: "PCB Quality Control"
  type: "manufacturing"
  criticality: "business-critical"

data_sources:
  - name: "quality_data"
    type: "database"
    connection: "postgresql://user:pass@localhost/pcb_quality"
    tables: ["inspection_results", "defect_logs"]

collectors:
  - name: "quality_metrics"
    type: "offline"
    data_source: "quality_data"
    metrics: ["accuracy", "false_positive_rate", "false_negative_rate"]

evaluators:
  - name: "quality_performance"
    type: "performance"
    thresholds:
      accuracy: 0.98
      false_positive_rate: 0.01
      false_negative_rate: 0.005

  - name: "quality_drift"
    type: "drift"
    detection_method: "ks_test"
    features: ["component_size", "solder_quality", "placement_accuracy"]

reports:
  - name: "quality_report"
    type: "business"
    format: "html"
    output_path: "./quality_reports/"

slo:
  availability: 0.9995
  accuracy: 0.98
  false_positive_rate: 0.01
  false_negative_rate: 0.005
```

Run this evaluation with:

```bash
ml-eval evaluate --config manufacturing-quality.yaml
```

This will generate comprehensive reports for your PCB quality control system, helping you maintain high quality standards and meet production targets. 