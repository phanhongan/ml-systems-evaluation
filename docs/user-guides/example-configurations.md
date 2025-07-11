# 📋 Example Configurations

This guide shows you how to use the industry-specific example configurations provided with the framework to quickly set up evaluations for your domain.

## 🎯 Quick Start

The framework provides ready-to-use example configurations for 6 industries. You can copy these examples and customize them for your specific needs.

```bash
# Copy an existing example
cp examples/industries/manufacturing/predictive-maintenance.yaml my-config.yaml

# Create a new configuration from scratch
ml-eval create-config --output my-config.yaml --system-name "My System" --industry manufacturing

# Validate and run
ml-eval validate my-config.yaml
ml-eval run my-config.yaml --output results.json
```

## 📁 Available Industry Examples

### 🏭 Manufacturing

**Files Available:**
- `predictive-maintenance.yaml` - Equipment monitoring and failure prediction
- `product-demand-forecasting.yaml` - Supply chain and demand optimization

**Key Features:**
- Equipment sensor monitoring (vibration, temperature, pressure)
- Predictive maintenance with Random Forest models
- Cost optimization and downtime reduction
- ISO compliance standards

**Example Usage:**
```bash
# Copy manufacturing example
cp examples/industries/manufacturing/predictive-maintenance.yaml manufacturing-config.yaml

# Customize for your equipment
nano manufacturing-config.yaml

# Run evaluation
ml-eval run manufacturing-config.yaml --output manufacturing-results.json
```

### ✈️ Aviation

**Files Available:**
- `aircraft-landing.yaml` - Safety-critical aircraft landing systems

**Key Features:**
- DO-178C, DO-254, ARP4754A compliance
- Safety-critical thresholds with zero tolerance
- Sub-500ms response time requirements
- Environmental adaptation (weather, runway conditions)

**Example Usage:**
```bash
# Copy aviation example
cp examples/industries/aviation/aircraft-landing.yaml aviation-config.yaml

# Run safety evaluation
ml-eval run aviation-config.yaml --output aviation-results.json
```

### 🚢 Maritime

**Files Available:**
- `collision-avoidance.yaml` - Ship collision avoidance and navigation safety

**Key Features:**
- COLREGs compliance monitoring
- Real-time collision detection
- Multi-vessel tracking
- Navigation parameter monitoring (TCPA, DCPA, BCR)

**Example Usage:**
```bash
# Copy maritime example
cp examples/industries/maritime/collision-avoidance.yaml maritime-config.yaml

# Run navigation safety evaluation
ml-eval run maritime-config.yaml --output maritime-results.json
```

### 🔬 Semiconductor

**Files Available:**
- `etching-digital-twins.yaml` - Digital twin process monitoring
- `etching-digital-twins.py` - Python implementation example

**Key Features:**
- Real-time process control
- Quality metrics monitoring
- Equipment health tracking
- Yield prediction models

**Example Usage:**
```bash
# Copy semiconductor example
cp examples/industries/semiconductor/etching-digital-twins.yaml semiconductor-config.yaml

# Run process evaluation
ml-eval run semiconductor-config.yaml --output semiconductor-results.json
```

### 🐟 Aquaculture

**Files Available:**
- `fish-species-classification.yaml` - Sonar-based fish classification

**Key Features:**
- Environmental monitoring
- Species identification accuracy
- Resource optimization
- Multi-stage workflow processing

**Example Usage:**
```bash
# Copy aquaculture example
cp examples/industries/aquaculture/fish-species-classification.yaml aquaculture-config.yaml

# Run classification evaluation
ml-eval run aquaculture-config.yaml --output aquaculture-results.json
```

### 🔒 Cybersecurity

**Files Available:**
- `security-operations.yaml` - Agentic AI security operations

**Key Features:**
- Multi-agent workflows for alert triage
- Cost-optimized LLM integration
- RAG-powered threat intelligence
- Multi-TB data processing capabilities

**Example Usage:**
```bash
# Copy cybersecurity example
cp examples/industries/cybersecurity/security-operations.yaml security-config.yaml

# Run security evaluation
ml-eval run security-config.yaml --output security-results.json
```

## 🔧 Customizing Example Configurations

### 1. Copy and Modify

```bash
# Start with an example closest to your use case
cp examples/industries/manufacturing/predictive-maintenance.yaml my-system.yaml

# Edit the configuration
nano my-system.yaml
```

### 2. Key Sections to Customize

#### **System Information**
```yaml
system:
  name: "Your System Name"
  criticality: "business_critical"  # or "safety_critical"
```

#### **Data Sources**
```yaml
data_sources:
  - name: "your_data"
    type: "database"  # or "api", "file"
    connection: "your_connection_string"
    tables: ["your_table_names"]
```

#### **SLOs (Service Level Objectives)**
```yaml
slos:
  accuracy:
    target: 0.95  # Adjust to your requirements
    window: "24h"
  availability:
    target: 0.999
    window: "30d"
```

#### **Collectors (Data Collection)**
```yaml
collectors:
  - type: "offline"  # or "online", "environmental"
    data_source: "your_data"
    metrics: ["accuracy", "latency", "throughput"]
```

#### **Evaluators (Evaluation Logic)**
```yaml
evaluators:
  - type: "performance"
    thresholds:
      accuracy: 0.95
      latency_p99: 100  # milliseconds
  - type: "drift"
    detection_method: "statistical"
    sensitivity: 0.05
```

### 3. Validate Your Configuration

```bash
# Check configuration syntax and logic
ml-eval validate my-system.yaml

# List configured components
ml-eval list-collectors my-system.yaml
ml-eval list-evaluators my-system.yaml
ml-eval list-reports my-system.yaml

# Run health check
ml-eval health my-system.yaml
```

## 🎯 Creating New Configurations from Scratch

If no existing example fits your needs:

```bash
# Create a basic configuration
ml-eval create-config \
  --output my-new-system.yaml \
  --system-name "My New System" \
  --industry manufacturing \
  --criticality business_critical

# Edit the generated file
nano my-new-system.yaml

# Add your specific requirements
```

## 🏆 Best Practices

1. **Start with Examples**: Always begin with the closest existing example
2. **Validate Early**: Run `ml-eval validate` after each major change
3. **Test Incrementally**: Start with basic configuration, then add complexity
4. **Document Changes**: Keep notes on your customizations
5. **Version Control**: Store your configurations in git

## 📚 Industry-Specific Guidance

### For Manufacturing Systems
- Focus on equipment monitoring and predictive maintenance
- Include cost optimization metrics
- Consider regulatory compliance (ISO standards)
- Monitor both performance and business impact

### For Aviation Systems  
- Prioritize safety-critical metrics
- Include regulatory compliance (DO-178C, DO-254)
- Set zero-tolerance thresholds for safety violations
- Monitor response times critically

### For Maritime Systems
- Include COLREGs compliance
- Monitor collision avoidance accuracy
- Track navigation parameters (TCPA, DCPA)
- Consider weather and environmental factors

### For Security Systems
- Focus on alert triage and response times
- Include cost optimization for LLM usage
- Monitor threat detection accuracy
- Consider scalability for large data volumes

## 🤝 Contributing New Examples

To contribute new industry examples:

1. Create a new directory: `examples/industries/your-industry/`
2. Add your configuration file: `your-example.yaml`
3. Include a README.md with usage instructions
4. Follow existing naming conventions
5. Submit a pull request

For detailed guidance, see the [Extending the Framework](extending.md) guide.

## 📖 Related Documentation

- [Getting Started](getting-started.md) - Basic setup and first evaluation
- [Configuration Guide](configuration.md) - Detailed configuration options
- [CLI Reference](cli-reference.md) - Complete command reference
- [Industry Guides](../industries/) - Industry-specific documentation 