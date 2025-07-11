# Getting Started Tutorial

This tutorial will guide you through creating your first ML system evaluation configuration.

## Prerequisites

- Python 3.11+
- ML Systems Evaluation framework installed
- Basic understanding of YAML configuration

## Step 1: Choose Your Template

Start with one of the templates based on your system's criticality:

- **basic-system.yaml**: For general ML systems
- **safety-critical.yaml**: For systems with high reliability requirements
- **business-critical.yaml**: For systems with high business impact

## Step 2: Define Your System

```yaml
system:
  name: "My ML System"
  persona: "ML Engineer"
  criticality: "business_critical"
  description: "Description of your ML system"
```

## Step 3: Set Your SLOs

Define Service Level Objectives that matter for your system:

```yaml
slos:
  accuracy:
    target: 0.90
    window: "24h"
    description: "Model accuracy for primary task"
  
  latency:
    target: 0.95
    window: "1h"
    description: "Proportion of predictions within 1 second"
```

## Step 4: Configure Collectors

Set up data collection from your system:

```yaml
collectors:
  - type: "online"
    endpoints: ["http://your-system:8080/metrics"]
    metrics: ["accuracy", "latency", "throughput"]
    polling_interval: 30
```

## Step 5: Set Up Evaluators

Configure how your system will be evaluated:

```yaml
evaluators:
  - type: "performance"
    metrics: ["accuracy", "latency"]
    thresholds:
      latency_ms: 1000
      accuracy: 0.85
```

## Step 6: Define Alerts

Set up alerts for important events:

```yaml
alerts:
  critical:
    - "accuracy_below_threshold"
    - "latency_above_threshold"
  warning:
    - "performance_degrading"
```

## Step 7: Configure Reports

Set up reporting for stakeholders:

```yaml
reports:
  - type: "business"
    format: "html"
    schedule: "0 9 * * *"
    recipients: ["team@company.com"]
```

## Next Steps

1. **Customize**: Adapt the configuration to your specific needs
2. **Test**: Run the evaluation framework with your configuration
3. **Monitor**: Set up continuous monitoring and alerting
4. **Iterate**: Refine your SLOs and thresholds based on results

## Example Walkthrough

See the industry-specific examples for detailed configurations:

- Aviation: `industries/aviation/aircraft-landing.yaml`
- Manufacturing: `industries/manufacturing/predictive-maintenance.yaml`
- Maritime: `industries/maritime/collision-avoidance.yaml`

## Common Patterns

### Safety-Critical Systems
- High accuracy requirements (99.9%+)
- Low latency requirements (<500ms)
- Failure mode analysis
- Regulatory compliance integration

### Business-Critical Systems
- ROI-focused metrics
- Customer satisfaction tracking
- Cost optimization
- Market condition monitoring

### General ML Systems
- Standard performance metrics
- Basic drift detection
- Regular retraining schedules
- Standard reporting
