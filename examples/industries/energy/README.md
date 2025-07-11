# Energy Industry Examples

This directory contains ML systems evaluation configurations for energy industry use cases.

## Examples

### Energy Optimization Recommendations (`energy-optimization-recommendations.yaml`)

A business-critical system for generating energy optimization recommendations and cost reduction strategies.

**Use Case**: Energy managers need ML-driven recommendations to optimize facility energy consumption and reduce costs.

**Key Features**:
- Real-time energy consumption monitoring
- Optimization recommendations for HVAC, lighting, and equipment
- Cost reduction tracking and validation
- Multi-facility support (office, warehouse, manufacturing, retail)

**Getting Started**:
```bash
# Run evaluation with this configuration
uv run python -m ml_eval.cli evaluate --config examples/industries/energy/energy-optimization-recommendations.yaml

# View results
uv run python -m ml_eval.cli report --type business
```

## Configuration Highlights

- **SLO Target**: 85% recommendation accuracy, 15% cost reduction
- **Data Sources**: Real-time energy meters, historical billing data, weather data
- **Monitoring**: Energy consumption patterns, recommendation effectiveness
- **Alerts**: High energy waste detection, model performance degradation

## Prerequisites

Ensure your energy data sources are accessible and configured in the YAML file:
- Energy consumption metrics endpoint
- Historical energy data in S3 bucket
- Weather data integration (optional but recommended)

For detailed configuration options, see the [Configuration Guide](../../docs/user-guides/configuration.md). 