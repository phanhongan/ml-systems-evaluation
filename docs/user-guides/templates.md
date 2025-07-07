# 📋 Industry Templates

This directory contains pre-configured templates for different industries, designed to help you quickly set up evaluations for your specific domain.

## 📁 Available Templates

### 🏭 Manufacturing Templates

#### 🔍 Basic Manufacturing Quality Control
**📄 File**: `manufacturing-basic.yaml`
**🎯 Use Case**: General quality control systems
**📊 Key Metrics**: Accuracy, precision, recall, defect rate

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

#### 🔧 Advanced Manufacturing with Predictive Maintenance
**📄 File**: `manufacturing-advanced.yaml`
**🎯 Use Case**: Predictive maintenance and quality control
**📊 Key Metrics**: Equipment health, failure prediction, maintenance costs

### ✈️ Aviation Templates

#### 🛡️ Safety-Critical Flight Systems
**📄 File**: `aviation-safety.yaml`
**🎯 Use Case**: Flight control and safety systems
**📊 Key Metrics**: Safety margins, failure probability, response time

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

#### 🔧 Aircraft Maintenance Prediction
**📄 File**: `aviation-maintenance.yaml`
**🎯 Use Case**: Predictive maintenance for aircraft components
**📊 Key Metrics**: Component health, maintenance scheduling, cost optimization

### ⚡ Energy Templates

#### ⚡ Grid Optimization Systems
**📄 File**: `energy-grid.yaml`
**🎯 Use Case**: Power grid optimization and demand prediction
**📊 Key Metrics**: Grid stability, demand accuracy, efficiency

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

#### 🌞 Renewable Energy Forecasting
**📄 File**: `energy-renewable.yaml`
**🎯 Use Case**: Solar and wind power forecasting
**📊 Key Metrics**: Forecast accuracy, energy production, cost optimization

### 🚢 Maritime Templates

#### 🚢 Maritime Collision Avoidance
**📄 File**: `maritime-collision-avoidance.yaml`
**🎯 Use Case**: Ship collision avoidance and navigational safety
**📊 Key Metrics**: Collision avoidance accuracy, alert latency, false alarm rate, STW/SOG discrepancy, system availability

```yaml
system:
  name: "Maritime Collision Avoidance System"
  type: "workflow"
  persona: "Officer of the Watch"
  criticality: "safety_critical"

slos:
  collision_avoidance_accuracy:
    target: 0.999
    window: "24h"
    error_budget: 0.001
    description: "Accuracy of collision risk detection and avoidance recommendations, considering COLREGs and advanced navigation parameters (TCPA, DCPA, BCR, STW, SOG)"
  alert_latency:
    target: 1000
    window: "1h"
    error_budget: 0.05
    description: "Maximum time to alert Officer of the Watch after risk detected (ms)"
  false_alarm_rate:
    target: 0.01
    window: "7d"
    error_budget: 0.005
    description: "Proportion of false positive collision alerts"
  system_availability:
    target: 0.9999
    window: "30d"
    error_budget: 0.0001
    description: "System uptime for collision avoidance functionality"

safety_thresholds:
  stw_sog_discrepancy:
    max: 2  # knots
    description: "Maximum allowed difference between Speed Through Water (STW) and Speed Over Ground (SOG) before triggering a safety alert. Discrepancies can lead to misclassification of collision scenarios (e.g., crossing vs head-on)."

operating_conditions:
  vessel_types: ["cargo", "tanker", "passenger", "fishing"]
  weather_conditions: ["clear", "fog", "storm", "rain"]
  traffic_density: ["low", "medium", "high"]
  navigation_parameters:
    stw: "Speed Through Water (knots)"
    sog: "Speed Over Ground (knots)"
    tcpa: "Time to Closest Point of Approach (minutes)"
    dcpa: "Distance at Closest Point of Approach (nautical miles)"
    bcr: "Bow Crossing Range (nautical miles)"

collectors:
  - type: "online"
    endpoint: "http://bridge-systems:9000/metrics"
    metrics: ["proximity_alerts", "collision_predictions", "alert_latency"]
  - type: "offline"
    log_paths: ["/var/log/bridge-systems/", "/var/log/navigation/alerts/"]
  - type: "environmental"
    sources: ["weather_station", "radar", "ais_receiver"]

evaluators:
  - type: "safety"
    compliance_standards: ["COLREGs", "IMO Guidelines"]
    critical_metrics: ["collision_avoidance_accuracy", "false_alarm_rate", "stw_sog_discrepancy"]
  - type: "reliability"
    error_budget_window: "30d"
    critical_metrics: ["system_availability"]
  - type: "performance"
    metrics: ["alert_latency"]
    real_time_threshold: 2000  # ms
```

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