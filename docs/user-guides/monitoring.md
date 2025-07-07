# Monitoring Setup

This guide helps you set up continuous monitoring for your ML systems using the ML Systems Evaluation Framework.

## Overview

Continuous monitoring is essential for Industrial AI systems to:
- Detect performance degradation early
- Identify data drift before it impacts predictions
- Ensure compliance with safety and business requirements
- Provide real-time alerts for critical issues

## Setting Up Continuous Monitoring

### Step 1: Configure Data Collection

Set up automated data collection from your ML system:

```yaml
# monitoring-config.yaml
data_sources:
  - name: "production_metrics"
    type: "database"
    connection: "postgresql://user:pass@localhost/prod_db"
    tables: ["predictions", "actuals", "system_metrics"]
    
  - name: "real_time_stream"
    type: "kafka"
    brokers: ["localhost:9092"]
    topics: ["ml-predictions", "ml-actuals"]

collectors:
  - name: "online_collector"
    type: "online"
    data_source: "real_time_stream"
    interval: "1m"
    metrics: ["accuracy", "latency", "throughput"]
    
  - name: "batch_collector"
    type: "offline"
    data_source: "production_metrics"
    schedule: "0 */6 * * *"  # Every 6 hours
    metrics: ["drift_score", "performance_trends"]
```

### Step 2: Define Monitoring Rules

Configure what to monitor and when to alert:

```yaml
monitoring:
  rules:
    - name: "performance_degradation"
      condition: "accuracy < 0.95"
      window: "1h"
      severity: "critical"
      
    - name: "data_drift"
      condition: "drift_score > 0.1"
      window: "24h"
      severity: "warning"
      
    - name: "high_latency"
      condition: "latency_p95 > 100"
      window: "5m"
      severity: "critical"
      
    - name: "system_unavailable"
      condition: "availability < 0.999"
      window: "1m"
      severity: "critical"
```

### Step 3: Set Up Alerting

Configure notification channels:

```yaml
alerts:
  channels:
    - name: "slack"
      type: "slack"
      webhook: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
      
    - name: "email"
      type: "email"
      recipients: ["ml-team@company.com", "oncall@company.com"]
      
    - name: "pagerduty"
      type: "pagerduty"
      service_key: "YOUR_PAGERDUTY_KEY"

  routing:
    critical: ["slack", "pagerduty"]
    warning: ["slack"]
    info: ["email"]
```

### Step 4: Start Monitoring

Run the monitoring service:

```bash
# Start continuous monitoring
ml-eval monitor --config monitoring-config.yaml

# Run in background
nohup ml-eval monitor --config monitoring-config.yaml > monitoring.log 2>&1 &

# Check status
ml-eval monitor --status
```

## Monitoring Dashboards

### Setting Up Dashboards

Create visualizations for your metrics:

```yaml
dashboards:
  - name: "ml_performance"
    type: "grafana"
    url: "http://localhost:3000"
    
  - name: "business_metrics"
    type: "custom"
    template: "business_dashboard.html"
```

### Key Dashboards

1. **Performance Dashboard**
   - Real-time accuracy, precision, recall
   - Latency percentiles
   - Throughput metrics

2. **Drift Dashboard**
   - Feature distribution changes
   - Statistical drift scores
   - Historical trends

3. **Business Dashboard**
   - Revenue impact
   - Cost savings
   - Risk metrics

4. **Compliance Dashboard**
   - Regulatory compliance status
   - Safety metrics
   - Audit trails

## Alert Management

### Alert Lifecycle

1. **Detection**: System detects violation of monitoring rules
2. **Notification**: Alerts sent to configured channels
3. **Acknowledgment**: Team acknowledges the alert
4. **Investigation**: Root cause analysis
5. **Resolution**: Fix applied and verified
6. **Post-mortem**: Document lessons learned

### Escalation Policies

```yaml
escalation:
  levels:
    - level: 1
      delay: "5m"
      channels: ["slack"]
      
    - level: 2
      delay: "15m"
      channels: ["slack", "email"]
      
    - level: 3
      delay: "30m"
      channels: ["slack", "email", "pagerduty"]
```

## Integration with Existing Systems

### Prometheus Integration

```yaml
exporters:
  - name: "prometheus"
    type: "prometheus"
    port: 9090
    metrics:
      - "ml_accuracy"
      - "ml_latency"
      - "ml_drift_score"
```

### Grafana Integration

```yaml
dashboards:
  - name: "ml_overview"
    type: "grafana"
    datasource: "prometheus"
    panels:
      - title: "ML Performance"
        query: "ml_accuracy"
        type: "graph"
```

## Best Practices

### Monitoring Strategy

1. **Start Simple**: Begin with basic performance metrics
2. **Add Gradually**: Introduce drift detection and business metrics
3. **Test Alerts**: Verify alerting works before going live
4. **Document Everything**: Keep runbooks for common issues
5. **Review Regularly**: Update thresholds based on system evolution

### Performance Considerations

1. **Sampling**: Use sampling for high-volume data
2. **Aggregation**: Pre-aggregate metrics where possible
3. **Retention**: Set appropriate data retention policies
4. **Scaling**: Plan for monitoring system scaling

### Security

1. **Access Control**: Limit access to monitoring data
2. **Encryption**: Encrypt sensitive metrics in transit
3. **Audit Logs**: Log all monitoring system access
4. **Compliance**: Ensure monitoring meets regulatory requirements

## Troubleshooting

### Common Issues

**Issue**: "No data being collected"
- **Solution**: Check data source connections and permissions

**Issue**: "Alerts not firing"
- **Solution**: Verify monitoring rules and thresholds

**Issue**: "High resource usage"
- **Solution**: Optimize collection intervals and sampling

### Getting Help

- Check the [Configuration Guide](configuration.md) for detailed options
- Review [CLI Reference](cli-reference.md) for command details
- Consult [Incident Response](../reference/incident-response.md) for handling alerts 