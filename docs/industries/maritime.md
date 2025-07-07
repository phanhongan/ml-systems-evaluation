# Maritime Industry Guide

This guide provides comprehensive information for implementing the ML Systems Evaluation Framework in maritime environments, with a focus on collision avoidance, navigational safety, and regulatory compliance.

## Maritime Overview

Maritime systems require high levels of safety, reliability, and compliance with international regulations. The framework provides specialized components for maritime-specific needs, including collision avoidance, navigational decision support, and compliance with standards such as COLREGs.

## Key Maritime Challenges

### 1. Collision Avoidance
- **Risk Detection**: Identifying potential collision scenarios in real time
- **Alerting**: Timely and accurate alerts to the Officer of the Watch (OOW)
- **Scenario Classification**: Correctly distinguishing between crossing, head-on, and overtaking situations, considering both STW (Speed Through Water) and SOG (Speed Over Ground)

### 2. Regulatory Compliance
- **COLREGs**: Adhering to International Regulations for Preventing Collisions at Sea
- **IMO Guidelines**: Meeting International Maritime Organization safety standards
- **Record Keeping**: Logging compliance-relevant events and actions

### 3. Navigation Complexity
- **Environmental Factors**: Handling fog, storms, and high-traffic conditions
- **Parameter Monitoring**: Tracking TCPA, DCPA, BCR, STW, SOG, and other navigation metrics
- **Sensor Fusion**: Integrating radar, AIS, and environmental data

## Maritime-Specific Configuration

### Maritime Collision Avoidance System Example

See the full template in [`docs/user-guides/templates.md`](../user-guides/templates.md) for a complete, ready-to-use configuration example.

Key configuration highlights:
- **Persona**: Officer of the Watch (OOW)
- **Critical SLOs**: Collision avoidance accuracy, alert latency, false alarm rate, system availability
- **Safety Parameter**: STW vs SOG discrepancy threshold
- **Navigation Parameters**: TCPA, DCPA, BCR, STW, SOG
- **Regulatory Compliance**: COLREGs, IMO Guidelines

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

## Maritime Best Practices

### 1. Collision Avoidance Best Practices
- Use sensor fusion (radar, AIS, environmental) for robust risk detection
- Monitor both STW and SOG to avoid scenario misclassification
- Set safety thresholds for navigation parameter discrepancies
- Provide clear, timely alerts to the OOW

### 2. Regulatory Compliance Best Practices
- Log all compliance-relevant events and actions
- Regularly review system recommendations against COLREGs and IMO guidelines
- Maintain audit trails for incident investigations

### 3. Navigation and Environmental Monitoring
- Continuously monitor TCPA, DCPA, BCR, and other key parameters
- Adapt alerting and recommendations to changing weather and traffic conditions
- Test system performance in simulated adverse conditions
