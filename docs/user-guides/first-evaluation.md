# Your First Evaluation

This guide walks you through running your first evaluation using the ML Systems Evaluation Framework.

## Prerequisites

- Framework installed (see [Installation Guide](installation.md))
- Access to your ML system's data
- Basic understanding of your system's architecture

## Step 1: Choose Your Industry Template

Start with a template that matches your industry:

```bash
# List available templates
ml-eval templates list

# Use a template for your industry
ml-eval templates use manufacturing-basic
```

## Step 2: Configure Your Data Sources

Edit the generated configuration file to point to your data:

```yaml
# config.yaml
data_sources:
  - name: "my_data"
    type: "database"  # or "file", "api", etc.
    connection: "postgresql://user:pass@localhost/my_db"
    tables: ["predictions", "actuals", "metadata"]
```

## Step 3: Define Your Metrics

Configure what metrics to collect:

```yaml
collectors:
  - name: "performance_metrics"
    type: "offline"
    data_source: "my_data"
    metrics: ["accuracy", "precision", "recall", "f1_score"]
    
  - name: "drift_metrics"
    type: "offline"
    data_source: "my_data"
    features: ["feature_1", "feature_2", "feature_3"]
```

## Step 4: Set Up Evaluators

Configure how to evaluate your system:

```yaml
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
```

## Step 5: Define SLOs

Set your Service Level Objectives:

```yaml
slo:
  availability: 0.999
  accuracy: 0.95
  latency_p95: 100  # milliseconds
```

## Step 6: Run Your Evaluation

Execute the evaluation:

```bash
# Run complete evaluation
ml-eval evaluate --config config.yaml

# Run specific components
ml-eval collect --config config.yaml
ml-eval evaluate --config config.yaml --evaluator performance
```

## Step 7: Review Results

Check the generated reports:

```bash
# Generate reports
ml-eval report --config config.yaml

# View reports in browser
open reports/business_report.html
```

## Understanding Your Results

### Key Metrics

1. **Accuracy**: Overall prediction accuracy
2. **Precision**: True positive rate
3. **Recall**: Sensitivity of the model
4. **Drift Score**: Data distribution changes
5. **Latency**: Response time percentiles

### Alert Thresholds

The framework alerts you when:
- Performance metrics fall below thresholds
- Data drift is detected
- System availability drops
- Compliance violations occur

## Next Steps

1. **Customize Configuration**: Adapt to your specific needs
2. **Set Up Monitoring**: Configure continuous monitoring
3. **Define SLOs**: Establish Service Level Objectives
4. **Create Dashboards**: Visualize your metrics
5. **Set Up Alerts**: Configure notification systems

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
```

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