# Industry Templates

This directory contains pre-configured templates for different industries, designed to help you quickly set up evaluations for your specific domain.

## Available Templates

### Manufacturing Templates

#### Basic Manufacturing Quality Control
**File**: `manufacturing-basic.yaml`
**Use Case**: General quality control systems
**Key Metrics**: Accuracy, precision, recall, defect rate

```yaml
system:
  name: "Manufacturing Quality Control"
  type: "manufacturing"
  criticality: "business-critical"

data_sources:
  - name: "quality_data"
    type: "database"
    connection: "postgresql://user:pass@localhost/quality_db"
    tables: ["quality_measurements", "defect_reports"]

collectors:
  - name: "quality_metrics"
    type: "offline"
    data_source: "quality_data"
    metrics: ["accuracy", "precision", "recall", "f1_score"]

evaluators:
  - name: "quality_performance"
    type: "performance"
    thresholds:
      accuracy: 0.95
      precision: 0.90
      recall: 0.85

  - name: "quality_drift"
    type: "drift"
    detection_method: "statistical"
    sensitivity: 0.05

reports:
  - name: "quality_report"
    type: "business"
    format: "html"
    output_path: "./reports/"

slo:
  availability: 0.999
  accuracy: 0.95
  latency_p95: 100
```

#### Advanced Manufacturing with Predictive Maintenance
**File**: `manufacturing-advanced.yaml`
**Use Case**: Predictive maintenance and quality control
**Key Metrics**: Equipment health, failure prediction, maintenance costs

### Aviation Templates

#### Safety-Critical Flight Systems
**File**: `aviation-safety.yaml`
**Use Case**: Flight control and safety systems
**Key Metrics**: Safety margins, failure probability, response time

```yaml
system:
  name: "Flight Control System"
  type: "aviation"
  criticality: "safety-critical"

data_sources:
  - name: "flight_data"
    type: "database"
    connection: "postgresql://user:pass@localhost/flight_db"
    tables: ["flight_telemetry", "safety_events"]

collectors:
  - name: "safety_metrics"
    type: "offline"
    data_source: "flight_data"
    metrics: ["safety_margin", "failure_probability", "response_time"]

evaluators:
  - name: "safety_evaluator"
    type: "safety"
    thresholds:
      safety_margin: 0.99
      failure_probability: 0.001
      response_time_p99: 50

  - name: "compliance_evaluator"
    type: "compliance"
    standards: ["DO-178C", "DO-254"]

reports:
  - name: "safety_report"
    type: "safety"
    format: "html"
    output_path: "./reports/"

slo:
  availability: 0.9999
  safety_margin: 0.99
  response_time_p99: 50
```

#### Aircraft Maintenance Prediction
**File**: `aviation-maintenance.yaml`
**Use Case**: Predictive maintenance for aircraft components
**Key Metrics**: Component health, maintenance scheduling, cost optimization

### Energy Templates

#### Grid Optimization Systems
**File**: `energy-grid.yaml`
**Use Case**: Power grid optimization and demand prediction
**Key Metrics**: Grid stability, demand accuracy, efficiency

```yaml
system:
  name: "Grid Optimization System"
  type: "energy"
  criticality: "business-critical"

data_sources:
  - name: "grid_data"
    type: "database"
    connection: "postgresql://user:pass@localhost/grid_db"
    tables: ["power_consumption", "grid_stability", "demand_forecasts"]

collectors:
  - name: "grid_metrics"
    type: "offline"
    data_source: "grid_data"
    metrics: ["demand_accuracy", "grid_stability", "efficiency"]

evaluators:
  - name: "grid_performance"
    type: "performance"
    thresholds:
      demand_accuracy: 0.95
      grid_stability: 0.99
      efficiency: 0.85

  - name: "grid_reliability"
    type: "reliability"
    failure_modes: ["voltage_drop", "frequency_deviation"]

reports:
  - name: "grid_report"
    type: "business"
    format: "html"
    output_path: "./reports/"

slo:
  availability: 0.9995
  demand_accuracy: 0.95
  grid_stability: 0.99
```

#### Renewable Energy Forecasting
**File**: `energy-renewable.yaml`
**Use Case**: Solar and wind power forecasting
**Key Metrics**: Forecast accuracy, energy production, cost optimization

## Using Templates

### 1. List Available Templates

```bash
ml-eval templates list
```

### 2. Use a Template

```bash
# Use a specific template
ml-eval templates use manufacturing-basic

# Customize the template
ml-eval templates customize manufacturing-basic --output my-config.yaml
```

### 3. Create Custom Template

```bash
# Create a new template based on existing one
ml-eval templates create my-industry --base manufacturing-basic

# Edit the template
ml-eval templates edit my-industry
```

## Template Structure

Each template contains:

### System Configuration
- **Name**: System identifier
- **Type**: Industry classification
- **Criticality**: Safety-critical or business-critical

### Data Sources
- Database connections
- API endpoints
- File paths
- Authentication details

### Collectors
- **Offline**: Batch data collection
- **Online**: Real-time data collection
- **Environmental**: System environment metrics

### Evaluators
- **Performance**: Accuracy, precision, recall
- **Drift**: Data distribution changes
- **Safety**: Safety-critical metrics
- **Compliance**: Regulatory requirements
- **Reliability**: System reliability metrics

### Reports
- **Business**: High-level business metrics
- **Compliance**: Regulatory compliance status
- **Safety**: Safety-critical system reports
- **Reliability**: System reliability analysis

### SLOs (Service Level Objectives)
- Availability targets
- Performance thresholds
- Safety requirements
- Compliance standards

## Customizing Templates

### 1. Modify Data Sources

```yaml
data_sources:
  - name: "my_data"
    type: "database"
    connection: "your_connection_string"
    tables: ["your_tables"]
```

### 2. Adjust Thresholds

```yaml
evaluators:
  - name: "performance_evaluator"
    type: "performance"
    thresholds:
      accuracy: 0.98  # Your custom threshold
      precision: 0.95
```

### 3. Add Custom Metrics

```yaml
collectors:
  - name: "custom_metrics"
    type: "offline"
    data_source: "my_data"
    metrics: ["your_custom_metric"]
```

## Industry-Specific Considerations

### Manufacturing
- Focus on quality control metrics
- Include defect detection rates
- Monitor production efficiency
- Track cost implications

### Aviation
- Emphasize safety-critical metrics
- Include regulatory compliance
- Monitor failure probabilities
- Track response times

### Energy
- Focus on grid stability
- Monitor demand forecasting accuracy
- Include efficiency metrics
- Track cost optimization

## Best Practices

1. **Start with a Template**: Use industry-specific templates as starting points
2. **Customize Gradually**: Modify templates incrementally
3. **Validate Configuration**: Test configurations before production use
4. **Document Changes**: Keep track of customizations
5. **Review Regularly**: Update templates based on system evolution

## Template Validation

```bash
# Validate a template
ml-eval templates validate manufacturing-basic

# Test a template with sample data
ml-eval templates test manufacturing-basic --sample-data
```

## Contributing Templates

To contribute new templates:

1. Create a new YAML file in the templates directory
2. Follow the standard template structure
3. Include comprehensive documentation
4. Add industry-specific examples
5. Submit a pull request

For more information on creating custom templates, see the [Extending the Framework](extending.md) guide. 