# 🚀 Getting Started with ML Systems Evaluation Framework

This guide will help you quickly set up and run your first evaluation using the ML Systems Evaluation Framework.

## 🔧 Prerequisites

- 🐍 Python 3.11 or higher
- 📦 UV package manager (https://astral.sh/uv/)
- 📊 Access to your ML system's monitoring data
- 🏗️ Basic understanding of your system's architecture

## 📦 Installation

### 1️⃣ Install the Framework

```bash
# Clone the repository
git clone <repository-url>
cd ml-systems-evaluation

# Install dependencies and the framework
uv sync --group dev

# (Optional) Activate the UV-managed virtual environment
uv shell

# For production installs (main dependencies only)
uv sync --group main
```

### 2️⃣ Verify Installation

```bash
ml-eval --help
```

## ⚡ Quick Start: Your First Evaluation

### 1️⃣ Use an Example Configuration

The framework provides industry-specific example configurations. For your first evaluation, we recommend starting with an existing example:

```bash
# Copy an example configuration for manufacturing
cp examples/industries/manufacturing/predictive-maintenance.yaml my-config.yaml

# Or create a new configuration from scratch
ml-eval create-config --output my-config.yaml --system-name "My Production System" --industry manufacturing
```

### 2️⃣ Configure Your System

Create a configuration file for your system:

```yaml
# config.yaml
system:
  name: "Production Line Quality Control"
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

### 3️⃣ Run Your First Evaluation

```bash
# Validate your configuration first
ml-eval validate config.yaml

# Run a complete evaluation
ml-eval run config.yaml --output results.json

# Run specific components
ml-eval collect config.yaml --output data.json
ml-eval evaluate config.yaml --data data.json --output evaluation.json
ml-eval report config.yaml --results evaluation.json --output reports.json
```

### 4️⃣ Review Results

Check the generated reports in the `./reports/` directory:

- **📊 Business Report**: High-level metrics and recommendations
- **📈 Performance Report**: Detailed performance analysis
- **📋 Compliance Report**: Regulatory compliance status

## 📊 Understanding Your Results

### 🎯 Key Metrics to Monitor

1. **📊 Accuracy**: Overall prediction accuracy
2. **🎯 Precision**: True positive rate
3. **🔍 Recall**: Sensitivity of the model
4. **📈 Drift Score**: Data distribution changes
5. **⚡ Latency**: Response time percentiles

### 🚨 Alert Thresholds

The framework automatically alerts you when:
- 📉 Performance metrics fall below thresholds
- 📊 Data drift is detected
- 🔴 System availability drops
- 📋 Compliance violations occur

## 🎯 Next Steps

1. **⚙️ Customize Configuration**: Adapt the template to your specific needs
2. **📊 Set Up Monitoring**: Configure continuous monitoring
3. **📋 Define SLOs**: Establish Service Level Objectives
4. **📈 Create Dashboards**: Visualize your metrics
5. **🚨 Set Up Alerts**: Configure notification systems

## 🔧 Troubleshooting

### ❌ Common Issues

**🚨 Issue**: "No data found"
- **✅ Solution**: Verify your data source configuration and connection

**🚨 Issue**: "Evaluation failed"
- **✅ Solution**: Check your evaluator configuration and thresholds

**🚨 Issue**: "Template not found"
- **✅ Solution**: Update to the latest version: `uv update`

### 🆘 Getting Help

- ⚙️ Check the [Configuration Guide](configuration.md) for detailed options
- 🖥️ Review [CLI Reference](cli-reference.md) for command details
- 📋 Consult [Example Configurations Guide](example-configurations.md) for your specific domain

## 💡 Example: Manufacturing Quality Control

Here's a complete example for a manufacturing quality control system:

```yaml
# manufacturing-quality.yaml
system:
  name: "PCB Quality Control"
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
ml-eval run manufacturing-quality.yaml --output quality-results.json
```

This will generate reports for your PCB quality control system, helping you maintain high quality standards and meet production targets. 