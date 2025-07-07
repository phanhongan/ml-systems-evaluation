# 📋 Industry Templates

This directory contains pre-configured templates for different industries, designed to help you quickly set up evaluations for your specific domain.

## 📁 Available Templates

### 🏭 Manufacturing Templates

#### 🔧 Manufacturing Predictive Maintenance
**📄 File**: `manufacturing-predictive_maintenance.yaml`
**🎯 Use Case**: Equipment monitoring and predictive maintenance systems
**📊 Key Metrics**: Failure prediction accuracy, maintenance cost reduction, downtime reduction

```yaml
system:
  name: "Manufacturing Predictive Maintenance"
  criticality: "business-critical"

data_sources:
  - name: "equipment_data"
    type: "database"
    connection: "postgresql://user:pass@localhost/equipment_db"
    tables: ["sensor_readings", "maintenance_history", "failure_events"]

collectors:
  - name: "equipment_metrics"
    type: "offline"
    data_source: "equipment_data"
    metrics: ["vibration", "temperature", "pressure", "current", "voltage"]

evaluators:
  - name: "maintenance_performance"
    type: "performance"
    thresholds:
      failure_prediction_accuracy: 0.92
      maintenance_cost_reduction: 0.15
      downtime_reduction: 0.20

  - name: "equipment_drift"
    type: "drift"
    detection_method: "statistical"
    sensitivity: 0.05

reports:
  - name: "maintenance_report"
    type: "business"
    format: "html"
    output_path: "./reports/"

slo:
  availability: 0.999
  failure_prediction_accuracy: 0.92
  maintenance_cost_reduction: 0.15
```

#### 📊 Manufacturing Demand Forecasting
**📄 File**: `manufacturing-demand_forecasting.yaml`
**🎯 Use Case**: Demand forecasting and supply chain optimization
**📊 Key Metrics**: Forecast accuracy, inventory optimization, supply chain efficiency

### ✈️ Aviation Templates

#### 🛡️ Aviation Safety Decision System
**📄 File**: `aviation-safety_decision.yaml`
**🎯 Use Case**: Safety-critical decision systems for aviation operations
**📊 Key Metrics**: Safety margins, failure probability, response time

```yaml
system:
  name: "Flight Control System"
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

#### ✈️ Aviation Flight Control System
**📄 File**: `aviation-flight_control.yaml`
**🎯 Use Case**: Advanced flight control and navigation systems
**📊 Key Metrics**: Flight path accuracy, weather assessment, obstacle detection

### ⚡ Energy Templates

#### ⚡ Energy Grid Optimization
**📄 File**: `energy-grid_optimization.yaml`
**🎯 Use Case**: Power grid optimization and load balancing
**📊 Key Metrics**: Grid stability, demand accuracy, efficiency

```yaml
system:
  name: "Grid Optimization System"
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

#### 📊 Energy Demand Prediction
**📄 File**: `energy-demand_prediction.yaml`
**🎯 Use Case**: Energy demand forecasting and capacity planning
**📊 Key Metrics**: Forecast accuracy, energy production, cost optimization

### 🚢 Maritime Templates

#### 🚢 Maritime Collision Avoidance
**📄 File**: `maritime-collision_avoidance.yaml`
**🎯 Use Case**: Ship collision avoidance and navigational safety
**📊 Key Metrics**: Collision avoidance accuracy, alert latency, false alarm rate, STW/SOG discrepancy, system availability

> **Note:** error_budget is always inferred from target and should not be specified in your configuration.

```yaml
system:
  name: "Maritime Collision Avoidance System"
  persona: "Officer of the Watch"
  criticality: "safety_critical"

slos:
  collision_avoidance_accuracy:
    target: 0.999
    window: "24h"
    description: "Accuracy of collision risk detection and avoidance recommendations, considering COLREGs and advanced navigation parameters (TCPA, DCPA, BCR, STW, SOG)"
  alert_latency:
    target: 0.95
    window: "1h"
    description: "Proportion of alerts delivered within 1000ms target time"
  false_alarm_rate:
    target: 0.01
    window: "7d"
    description: "Proportion of false positive collision alerts"
  system_availability:
    target: 0.9999
    window: "30d"
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

## 📋 Configuration Examples

#### **📁 Available Example Configurations**

The framework includes several complete example configurations in the [`examples/`](./examples/) directory:

- **[✈️ aircraft-landing.yaml](./examples/aircraft-landing.yaml)**: Comprehensive aircraft landing system with safety-critical compliance (DO-178C, DO-254, ARP4754A)
- **[🐟 fish-species-classification.yaml](./examples/fish-species-classification.yaml)**: Multi-stage workflow for underwater fish species classification
- **[🚢 maritime-collision-avoidance.yaml](./examples/maritime-collision-avoidance.yaml)**: Maritime safety system with COLREGs compliance
- **[🔧 predictive-maintenance.yaml](./examples/predictive-maintenance.yaml)**: Industrial equipment predictive maintenance with failure prediction and cost optimization

#### **📋 Using Industry Templates (Recommended)**

```bash
# List available templates
ml-eval templates list

# Use a specific template
ml-eval templates use manufacturing-predictive_maintenance

# Customize the template
ml-eval templates customize manufacturing-predictive_maintenance --output my-config.yaml
```

#### **🏭 Manufacturing Predictive Maintenance Example**

See [examples/fish-species-classification.yaml](./examples/fish-species-classification.yaml) for a complete workflow example with similar structure.

#### **✈️ Aviation Safety System Example**

See [examples/aircraft-landing.yaml](./examples/aircraft-landing.yaml) for a comprehensive aircraft landing system with multiple evaluators, collectors, and safety thresholds.

#### **🔧 Predictive Maintenance Example**

See [examples/predictive-maintenance.yaml](./examples/predictive-maintenance.yaml) for a comprehensive predictive maintenance system with:

- **Equipment Monitoring**: Vibration, temperature, pressure, current, voltage sensors
- **Failure Prediction**: Random Forest classification for failure prediction within 48 hours
- **Remaining Life Estimation**: Gradient Boosting regression for days-to-failure prediction
- **Cost Optimization**: Maintenance cost reduction and downtime minimization
- **Regulatory Compliance**: ISO-10816, ISO-7919, API-670 standards
- **Business Metrics**: Maintenance cost reduction, equipment lifetime optimization
- **Alert System**: Critical failure alerts, maintenance scheduling, performance degradation warnings

**Key Features:**
- Real-time equipment monitoring with multiple sensor types
- Dual ML models for classification and regression tasks
- Comprehensive SLOs for prediction accuracy and business impact
- Regulatory compliance for industrial equipment standards
- Automated alerting and maintenance scheduling
- Cost optimization and downtime reduction tracking

## Using Templates

### 1. List Available Templates

```bash
ml-eval templates list
```

### 2. Use a Template

```bash
# Use a specific template
ml-eval templates use manufacturing-predictive_maintenance

# Customize the template
ml-eval templates customize manufacturing-predictive_maintenance --output my-config.yaml
```

### 3. Create Custom Template

```bash
# Create a new template based on existing one
ml-eval templates create my-industry --base manufacturing-predictive_maintenance

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
- Focus on predictive maintenance metrics
- Include equipment failure prediction
- Monitor maintenance efficiency
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
ml-eval templates validate manufacturing-predictive_maintenance

# Test a template with sample data
ml-eval templates test manufacturing-predictive_maintenance --sample-data
```

## Contributing Templates

To contribute new templates:

1. Create a new YAML file in the templates directory
2. Follow the standard template structure
3. Include comprehensive documentation
4. Add industry-specific examples
5. Submit a pull request

For more information on creating custom templates, see the [Extending the Framework](extending.md) guide. 