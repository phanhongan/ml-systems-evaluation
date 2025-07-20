# Autonomous Vehicle Evaluation System

This example demonstrates how to use the ML Systems Evaluation Framework for comprehensive evaluation of autonomous vehicle systems, covering perception, planning, and control components.

## Overview

The autonomous vehicle evaluation system provides:

- **Multi-modal sensor evaluation** (camera, lidar, radar)
- **Path planning and trajectory optimization assessment**
- **Control system performance monitoring**
- **Safety-critical system validation**
- **Real-time performance monitoring**
- **Simulation integration capabilities**

## Key Components

### 1. Perception Evaluation

The `PerceptionEvaluator` handles:
- **Multi-sensor fusion** (camera, lidar, radar)
- **Object detection and classification accuracy**
- **Cross-modal consistency validation**
- **Sensor-specific performance metrics**
- **Fusion algorithm evaluation**

**Supported Sensors:**
- **Camera**: RGB image processing, object detection
- **Lidar**: Point cloud processing, 3D object detection
- **Radar**: Range and velocity detection, object tracking

### 2. Planning Evaluation

The `PlanningEvaluator` covers:
- **Path planning accuracy and efficiency**
- **Trajectory optimization performance**
- **Decision-making quality and consistency**
- **Safety margin validation**
- **Planning latency monitoring**

**Key Metrics:**
- Path planning accuracy and efficiency
- Trajectory smoothness and optimality
- Decision consistency and confidence
- Safety margin compliance
- Collision avoidance rates

### 3. Control Evaluation

The `ControlEvaluator` monitors:
- **Actuator control accuracy** (steering, braking, acceleration)
- **Control system stability and performance**
- **Command execution accuracy and latency**
- **Feedback loop performance**
- **Control system safety and fault tolerance**

**Supported Actuators:**
- **Steering**: Steering angle control and response time
- **Braking**: Brake force control and emergency response
- **Acceleration**: Throttle control and smooth acceleration

### 4. Data Collection

#### Multi-Modal Collector
- **Multi-sensor data synchronization**
- **Data quality assessment**
- **Sensor health monitoring**
- **Cross-modal consistency validation**

#### Simulation Collector
- **Integration with simulation platforms** (CARLA, LGSVL)
- **Scenario-based data collection**
- **Synthetic data generation**
- **Ground truth annotation**

## Configuration

The system is configured through `autonomous-vehicle-evaluation.yaml`:

```yaml
# Sensor Configuration
collectors:
  multimodal:
    sensors:
      front_camera:
        type: "camera"
        expected_shape: [480, 640, 3]
        thresholds:
          sharpness:
            min: 0.6
            max: 1.0
            critical: true
      
      lidar_sensor:
        type: "lidar"
        expected_shape: [10000, 3]
        thresholds:
          point_density:
            min: 0.7
            max: 1.0
            critical: true

# Evaluation Configuration
evaluators:
  perception:
    sensors:
      front_camera:
        thresholds:
          detection_accuracy:
            min: 0.9
            max: 1.0
            critical: true
          latency_p95:
            min: 0.0
            max: 100.0
            critical: true
```

## Usage

### 1. Basic Evaluation

```python
from ml_eval import MLEvaluationFramework

# Load configuration
framework = MLEvaluationFramework("autonomous-vehicle-evaluation.yaml")

# Run evaluation
results = framework.evaluate()

# Get perception results
perception_score = results["perception"]["overall_perception_score"]
print(f"Perception Score: {perception_score:.3f}")

# Get planning results
planning_score = results["planning"]["overall_planning_score"]
print(f"Planning Score: {planning_score:.3f}")

# Get control results
control_score = results["control"]["overall_control_score"]
print(f"Control Score: {control_score:.3f}")
```

### 2. Real-time Monitoring

```python
# Start real-time monitoring
framework.start_monitoring()

# Monitor specific metrics
while True:
    metrics = framework.get_current_metrics()
    
    # Check perception alerts
    if "perception" in metrics["alerts"]:
        print("Perception alert detected!")
    
    # Check safety violations
    if "safety" in metrics["alerts"]:
        print("Safety violation detected!")
```

### 3. Simulation Integration

```python
# Load simulation scenario
framework.load_scenario("highway_merge")

# Start simulation
framework.start_simulation()

# Collect simulation data
sim_data = framework.collect_simulation_data()

# Evaluate with simulation data
results = framework.evaluate_with_data(sim_data)
```

## Safety Features

### 1. Safety Margins
- **Collision distance**: Minimum 2.0m, maximum 50.0m
- **Braking distance**: Minimum 5.0m, maximum 100.0m
- **Lateral clearance**: Minimum 0.5m, maximum 5.0m

### 2. Emergency Procedures
- **Emergency stop**: 0.1s response time
- **Safe parking**: 5.0s response time
- **Manual override**: 0.5s response time

### 3. Failure Mode Analysis
- **Sensor failure**: 0.001 probability
- **Communication failure**: 0.001 probability
- **Actuator failure**: 0.0001 probability
- **Software failure**: 0.01 probability

## Performance Requirements

### Latency Thresholds
- **Perception latency**: < 100ms (p95)
- **Planning latency**: < 200ms (p95)
- **Control latency**: < 100ms (p95)
- **End-to-end latency**: < 300ms (p95)

### Throughput Requirements
- **Frames per second**: 30 FPS
- **Planning updates**: 10 Hz
- **Control updates**: 100 Hz

### Resource Limits
- **CPU usage**: < 80%
- **Memory usage**: < 90%
- **GPU usage**: < 90%
- **Network bandwidth**: < 80%

## Compliance Standards

The system supports evaluation against:
- **ISO-26262**: Functional safety for road vehicles
- **DO-178C**: Software considerations in airborne systems
- **UL-4600**: Safety for the evaluation of autonomous products

## Reporting

### Safety Reports
- **Real-time alerts** for safety violations
- **Escalation levels** (warning, critical, emergency)
- **Multi-channel notifications** (email, SMS, dashboard)

### Compliance Reports
- **Daily compliance status**
- **Audit trail maintenance**
- **Standards compliance tracking**

### Business Reports
- **Weekly KPI summaries**
- **Stakeholder-specific reports**
- **Performance trend analysis**

## Integration Examples

### 1. CARLA Simulation
```python
# CARLA integration example
carla_config = {
    "host": "localhost",
    "port": 2000,
    "timeout": 10.0,
    "world": "Town01"
}

framework.connect_simulation("carla", carla_config)
```

### 2. Real Vehicle Integration
```python
# Real vehicle sensor integration
vehicle_config = {
    "camera_url": "rtsp://vehicle-camera:554/stream",
    "lidar_topic": "/lidar/points",
    "radar_topic": "/radar/detections"
}

framework.connect_vehicle_sensors(vehicle_config)
```

### 3. Cloud Integration
```python
# Cloud monitoring integration
cloud_config = {
    "endpoint": "https://api.company.com/monitoring",
    "api_key": "your-api-key",
    "update_frequency": 1.0  # seconds
}

framework.connect_cloud_monitoring(cloud_config)
```

## Customization

### Adding New Sensors
```yaml
# Add new sensor type
sensors:
  thermal_camera:
    type: "thermal"
    source: "thermal_camera_feed"
    expected_shape: [480, 640, 1]
    format: "GRAY"
    thresholds:
      temperature_range:
        min: -40.0
        max: 80.0
        critical: false
```

### Custom Evaluation Metrics
```python
# Custom perception metric
class CustomPerceptionMetric:
    def calculate(self, sensor_data):
        # Custom calculation logic
        return custom_score

# Register custom metric
framework.register_metric("custom_perception", CustomPerceptionMetric())
```

## Troubleshooting

### Common Issues

1. **Sensor Synchronization Issues**
   - Check timestamp differences
   - Verify sensor configurations
   - Monitor sync quality metrics

2. **Performance Degradation**
   - Monitor resource usage
   - Check latency thresholds
   - Review evaluation frequency

3. **Safety Violations**
   - Review safety margin configurations
   - Check sensor health status
   - Verify emergency procedures

### Debug Mode
```python
# Enable debug logging
framework.enable_debug_mode()

# Get detailed evaluation logs
logs = framework.get_evaluation_logs()
```

## Next Steps

1. **Deploy to real vehicle** for field testing
2. **Integrate with cloud monitoring** for remote oversight
3. **Add custom sensors** for specific use cases
4. **Extend evaluation metrics** for domain-specific requirements
5. **Implement advanced safety features** for production deployment

For more information, see the main framework documentation and other industry examples. 