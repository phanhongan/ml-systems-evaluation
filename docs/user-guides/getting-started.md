# 🚀 Getting Started with ML Systems Evaluation Framework

This guide will help you quickly set up and run your first evaluation using the ML Systems Evaluation Framework.

## 🔧 Prerequisites

- 🐍 Python 3.11 or higher
- 📦 UV package manager (https://astral.sh/uv/)
- 📊 Access to your ML system's monitoring data
- 🏗️ Basic understanding of your system's architecture

## 📦 Installation & Setup

### Quick Installation
```bash
# Clone and setup
git clone <repository-url>
cd ml-systems-evaluation
uv sync --extra dev
uv shell

# Verify installation
ml-eval --help
```

### Production Installation
```bash
# Main dependencies only
uv sync --group main
```

## ⚡ Quick Start: Your First Evaluation

### 1. Use Example Configuration
```bash
# Copy an example configuration
cp examples/industries/manufacturing/predictive-maintenance.yaml my-config.yaml

# Or create from scratch
ml-eval create-config --output my-config.yaml --system-name "My Production System" --industry manufacturing
```

### 2. Configure Your System
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

### 3. Run Evaluation
```bash
# Run complete evaluation
ml-eval evaluate --config my-config.yaml

# Run specific components
ml-eval collect --config my-config.yaml
ml-eval evaluate --config my-config.yaml --skip-collection
ml-eval report --config my-config.yaml
```

## 🔧 Configuration Options

### Environment Overrides
```bash
# Test with sample data
ml-eval evaluate --config my-config.yaml --sample-data

# Generate template
ml-eval create-config --template manufacturing --output template.yaml
```

## 📊 Monitoring Setup

### Continuous Monitoring
```bash
# Set up cron job (every 5 minutes)
*/5 * * * * cd /path/to/project && ml-eval evaluate --config production-config.yaml

# Or use monitoring script
ml-eval monitor --config production-config.yaml --interval 300
```

## 🚀 Next Steps

1. **Review Results**: Check the generated reports in `./reports/`
2. **Adjust Configuration**: Modify thresholds and settings based on results
3. **Set Up Monitoring**: Configure continuous monitoring for production
4. **Industry Guides**: See industry-specific guides for domain expertise

For detailed configuration options, see the [Configuration Guide](configuration.md). 