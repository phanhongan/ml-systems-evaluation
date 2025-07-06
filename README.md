# ML Systems Evaluation Framework

A reliability-focused evaluation framework for Industrial AI systems, applying Site Reliability Engineering (SRE) principles to machine learning evaluation.

## The Problem

Industrial AI systems face unique challenges that traditional ML evaluation approaches don't address:

### **Safety-Critical Requirements**
- **Zero Tolerance Failures**: Aircraft landing systems, medical diagnostics, autonomous vehicles where errors can be catastrophic
- **Regulatory Standards**: Aviation (DO-178C), healthcare, financial services require continuous compliance validation
- **Environmental Constraints**: Underwater devices, extreme temperatures, harsh conditions that affect system reliability

### **Business-Critical Operations**
- **Immediate Financial Impact**: Manufacturing quality control, fraud detection where failures cost millions instantly
- **Real-time Decision Making**: Supply chain optimization, trading systems where delays cause cascading failures
- **Public Safety**: Systems where failures affect public safety, requiring continuous monitoring and rapid response

### **Traditional ML Evaluation Gaps**
- **No Safety Validation**: Standard ML evaluation doesn't assess catastrophic failure scenarios
- **Missing Regulatory Compliance**: No built-in validation against industry-specific standards
- **Inadequate Environmental Monitoring**: Doesn't account for harsh operating conditions
- **No Business Impact Metrics**: Technical metrics don't connect to business outcomes

## Why This Framework Matters

### **SRE Principles for Industrial AI**
This framework treats Industrial AI systems as critical infrastructure, applying proven SRE concepts:
- **Safety-First Error Budgets**: Acceptable failure rates with zero tolerance for catastrophic failures
- **Regulatory SLOs**: Service Level Objectives that include compliance requirements
- **Environmental Observability**: Monitoring that accounts for harsh operating conditions
- **Business-Critical Reliability**: Focus on preventing immediate financial and safety impacts
- **Rapid Incident Response**: Structured approach to handling safety-critical and business-critical failures

### **Continuous Evaluation Lifecycle**
Evaluation isn't just a final checkpoint—it's a continuous feedback mechanism that informs every stage of the ML lifecycle:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Development   │    │   Deployment    │    │   Production    │
│                 │    │                 │    │                 │
│ • Model Design  │───▶│ • A/B Testing   │───▶│ • Real-time     │
│ • Data Pipeline │    │ • Canary Deploy │    │ • Monitoring    │
│ • Architecture  │    │ • Rollback Plan │    │ • Alerting      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲                       │
         │                       │                       ▼
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Evaluation    │
                    │                 │
                    │ • Performance   │
                    │ • Reliability   │
                    │ • Safety        │
                    │ • Compliance    │
                    └─────────────────┘
```

## How Evaluation Informs the ML Lifecycle

### **Development Phase Insights**
- **Model Architecture**: Performance bottlenecks reveal design flaws
- **Data Quality**: Drift detection identifies training data issues
- **Feature Engineering**: Model degradation points to feature relevance changes
- **Hyperparameter Tuning**: Real-world performance guides optimization

### **Deployment Phase Validation**
- **A/B Testing**: Structured comparison of model versions
- **Canary Deployments**: Gradual rollout with continuous evaluation
- **Rollback Triggers**: Automatic reversion based on SLO violations
- **Infrastructure Scaling**: Performance metrics guide resource allocation

### **Production Phase Monitoring**
- **Real-time Alerts**: Immediate notification of SLO violations
- **Trend Analysis**: Long-term performance degradation detection
- **Incident Response**: Structured approach to ML system failures
- **Capacity Planning**: Resource needs based on usage patterns

### **Feedback Loop Benefits**
- **Model Retraining**: Triggered by drift detection and performance degradation
- **Data Pipeline Updates**: Informed by data quality issues
- **Architecture Evolution**: Driven by scalability and reliability needs
- **Process Improvement**: Continuous refinement of ML operations

## Business Impact

### **Risk Mitigation**
- **Prevent Catastrophic Failures**: Early detection of safety-critical system issues
- **Regulatory Compliance**: Continuous validation for regulated industries
- **Brand Protection**: Avoid public incidents that damage reputation
- **Financial Loss Prevention**: Catch issues before they impact revenue

### **Operational Excellence**
- **Proactive Maintenance**: Fix issues before they become incidents
- **Resource Optimization**: Right-size infrastructure based on actual usage
- **Team Efficiency**: Automated monitoring reduces manual oversight
- **Data-Driven Decisions**: Metrics guide strategic ML investments

### **Competitive Advantage**
- **Faster Iteration**: Rapid feedback enables quick model improvements
- **Higher Quality**: Continuous evaluation maintains performance standards
- **Customer Trust**: Reliable ML systems build user confidence
- **Innovation Velocity**: Safe experimentation with new ML approaches

## Key Features

- **Safety-Critical Evaluation**: Zero tolerance for catastrophic failures with specialized safety metrics
- **Regulatory Compliance**: Built-in validation against industry standards (DO-178C for aviation)
- **Environmental Monitoring**: Specialized collectors for harsh operating conditions
- **Business-Critical Reliability**: SRE principles applied to systems with immediate financial impact
- **Extensible Architecture**: Plugin-based collectors and evaluators for domain-specific requirements
- **Real-time & Batch**: Online and offline evaluation for continuous monitoring
- **Standards Enforcement**: Configurable quality gates with regulatory compliance checks

## Supported Scenarios

### Fish Species Classification AI (Workflow Example)
**Problem**: Multi-stage ML pipeline processing echogram images from underwater devices for real-time fish species identification in commercial fishing operations.

**Challenges**:
- **Data Quality**: Echogram images from underwater devices vary in clarity, depth, and environmental conditions
- **Pipeline Reliability**: Any stage failure breaks the entire classification process during active fishing operations
- **Business Impact**: Incorrect species identification affects catch management, regulatory compliance, and fishing efficiency
- **Real-time Constraints**: Decisions must be made quickly during active fishing to optimize catch and avoid bycatch

**Framework Solution**:
- **End-to-end monitoring**: Track performance across echogram preprocessing → feature extraction → species classification → catch optimization
- **Data quality validation**: Detect drift in echogram characteristics and underwater conditions
- **Reliability assessment**: Ensure 99.9% pipeline availability with automatic failover during fishing operations
- **Business metrics**: Connect technical performance to fishing efficiency and regulatory compliance
- **Environmental adaptation**: Monitor water conditions and adjust model behavior for different fishing environments

### Aircraft Landing Systems (Single Model Example)
**Problem**: Safety-critical decision model with zero tolerance for false positives.

**Challenges**:
- **Safety Requirements**: 99.99% accuracy with sub-100ms response time
- **Regulatory Compliance**: Must meet aviation safety standards (DO-178C)
- **Real-time Constraints**: Decisions must be made within strict time limits
- **Failure Consequences**: Incorrect decisions can lead to catastrophic outcomes

**Framework Solution**:
- **Safety validation**: Continuous monitoring of false positive rates and response times
- **Regulatory compliance**: Automated validation against aviation safety standards
- **Real-time alerting**: Immediate notification of any performance degradation
- **Incident response**: Structured approach to handling safety-critical failures

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │    │   Collectors    │    │   Evaluators    │
│                 │    │                 │    │                 │
│ • Logs          │───▶│ • Online        │───▶│ • Reliability   │
│ • Metrics       │    │ • Offline       │    │ • Performance   │
│ • Telemetry     │    │ • Custom        │    │ • Safety        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                              ┌─────────────────┐
                                              │    Reports      │
                                              │                 │
                                              │ • SLI/SLO       │
                                              │ • Incidents     │
                                              │ • Trends        │
                                              └─────────────────┘
```

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd ml-systems-evaluation

# Install in development mode
pip install -e .

# Install with industry-specific dependencies
pip install -e .[manufacturing]  # For manufacturing systems
pip install -e .[aviation]       # For aviation systems
pip install -e .[energy]         # For energy systems
```

### Getting Started (For Industrial ML Engineers)

```bash
# 1. List available templates for your industry
ml-eval template --industry manufacturing --type list

# 2. Get a specific template for your industry
ml-eval template --industry manufacturing --type quality_control > quality-system.yaml

# 3. Customize your configuration
# Edit the generated .yaml file with your specific requirements

# 4. Test your configuration
ml-eval dev --config quality-system.yaml --mode validation

# 5. Evaluate your production system
ml-eval evaluate --config quality-system.yaml --mode single

# 6. Set up continuous monitoring
ml-eval monitor --config quality-system.yaml --interval 300

# 7. Generate reports
ml-eval report --type reliability --period 30d
```

### Available Industries and Templates

The framework provides ready-to-use templates for these industrial sectors:

#### **Manufacturing Industry**
- **quality_control**: Quality control system for defect detection and inspection
- **predictive_maintenance**: Predictive maintenance system for equipment monitoring

#### **Aviation Industry**  
- **safety_decision**: Safety-critical decision system for aviation safety
- **flight_control**: Flight control assistance system for aircraft control

#### **Energy Industry**
- **grid_optimization**: Power grid optimization system for demand prediction and supply management
- **demand_prediction**: Energy demand forecasting system

### Quick Commands

```bash
# Get help and examples
ml-eval quickstart --industry aviation
ml-eval example --type aircraft-model --detailed

# Show all available commands
ml-eval --help

# Additional template examples
ml-eval template --industry aviation --type safety_decision --output safety-system.yaml
ml-eval template --industry energy --type grid_optimization --output grid-system.yaml

# Advanced development and production
ml-eval dev --config production-system.yaml --mode validation --strict
ml-eval evaluate --config production-system.yaml --mode single
ml-eval monitor --config production-system.yaml --interval 60

# Additional reporting
ml-eval report --type safety --period 30d
```

### Configuration Examples

#### **Using Industry Templates (Recommended)**

```bash
# List available templates
ml-eval template --industry manufacturing --type list

# Get a specific template
ml-eval template --industry manufacturing --type quality_control > quality-control.yaml
```

#### **Manufacturing Quality Control Example**

```yaml
# quality-control.yaml (generated from template)
system:
  name: "Manufacturing Quality Control System"
  type: "workflow"
  stages: ["data_collection", "quality_prediction", "defect_detection", "alert_generation"]
  criticality: "business_critical"
  
slos:
  defect_detection_accuracy:
    target: 0.98
    window: "24h"
    error_budget: 0.02
    description: "Accuracy in detecting manufacturing defects"
  
  prediction_latency:
    target: 100
    window: "1h"
    error_budget: 0.05
    description: "Time to predict quality issues (ms)"
  
  false_positive_rate:
    target: 0.01
    window: "24h"
    error_budget: 0.01
    description: "Rate of false defect alerts"

collectors:
  - type: "online"
    endpoint: "http://manufacturing-metrics:9090"
  - type: "offline"
    log_paths: ["/var/log/quality-control/"]

evaluators:
  - type: "reliability"
    error_budget_window: "30d"
  - type: "performance"
    metrics: ["accuracy", "latency"]
```

#### **Aviation Safety System Example**

```yaml
# safety-system.yaml (generated from template)
system:
  name: "Aviation Safety Decision System"
  type: "single_model"
  criticality: "safety_critical"
  
slos:
  decision_accuracy:
    target: 0.9999
    window: "24h"
    error_budget: 0.0001
    description: "Accuracy of safety-critical decisions"
    compliance_standard: "DO-178C"
    safety_critical: True
  
  response_time:
    target: 50
    window: "1h"
    error_budget: 0.01
    description: "Decision response time (ms)"
    safety_critical: True

collectors:
  - type: "online"
    endpoint: "http://aviation-system:8080/metrics"

evaluators:
  - type: "reliability"
    error_budget_window: "7d"
  - type: "safety"
    compliance_standards: ["DO-178C"]
```

## Core Components

### Collectors
- **OnlineCollector**: Real-time metrics from running systems
- **OfflineCollector**: Historical data from logs and databases
- **EnvironmentalCollector**: Specialized monitoring for harsh conditions (temperature, pressure, etc.)
- **RegulatoryCollector**: Compliance metrics for industry standards
- **CustomCollector**: Extensible interface for domain-specific metrics

### Evaluators
- **ReliabilityEvaluator**: SLI/SLO compliance and error budgets with safety thresholds
- **SafetyEvaluator**: Critical system safety validation with zero-tolerance checks
- **RegulatoryEvaluator**: Compliance validation against industry standards
- **EnvironmentalEvaluator**: Performance assessment under harsh conditions
- **DriftEvaluator**: Data and model drift detection with business impact assessment

### Reports
- **ReliabilityReport**: Error budgets, SLO compliance, incident analysis
- **SafetyReport**: Safety-critical metrics and compliance status
- **RegulatoryReport**: Compliance validation and audit trails
- **BusinessImpactReport**: Technical metrics connected to business outcomes

## SRE Integration

### Service Level Objectives (SLOs)
```yaml
slos:
  # Safety-Critical SLOs
  false_positive_rate:
    target: 0.0001  # 0.01% for safety-critical systems
    window: "24h"
    error_budget: 0.0001
    compliance: "DO-178C"
  
  # Business-Critical SLOs
  fraud_detection_accuracy:
    target: 0.999
    window: "1h"
    error_budget: 0.001
    business_impact: "millions_per_hour"
  
  # Environmental SLOs
  underwater_device_uptime:
    target: 0.9999
    window: "30d"
    error_budget: 0.0001
    environmental_conditions: "high_pressure, salt_water"
```

### Error Budget Policies
- **Safety-First Alerts**: Immediate notification for safety-critical budget violations
- **Regulatory Compliance**: Automatic audit trail for compliance violations
- **Business Impact Assessment**: Connect budget exhaustion to financial impact
- **Environmental Adaptation**: Adjust thresholds based on operating conditions

## Advanced Features

### Safety-Critical Development
This framework enables a new approach to Industrial AI development where safety and compliance are built-in:

```python
# Define safety-critical SLOs before model development
slos = {
    "false_positive_rate": SLOConfig(target=0.0001, error_budget=0.0001, compliance="DO-178C"),
    "response_time": SLOConfig(target=50, error_budget=0.001, safety_critical=True),
    "availability": SLOConfig(target=0.99999, error_budget=0.00001, business_impact="catastrophic")
}

# Continuous evaluation during development
from ml_eval import EvaluationFramework
from ml_eval.collectors import OnlineCollector
from ml_eval.evaluators import SafetyEvaluator

framework = EvaluationFramework({"system": {"name": "Safety System"}})
framework.add_collector(OnlineCollector({"endpoint": "http://safety-metrics:8080"}))
framework.add_evaluator(SafetyEvaluator({"compliance_standards": ["DO-178C"]}))

# Real-time safety validation during training
while training:
    result = framework.evaluate()
    if result.safety_violations:
        # Halt development if safety thresholds are violated
        raise Exception("Model violates safety requirements")
```

### Workflow Evaluation
```python
from ml_eval import EvaluationFramework

# Create framework for workflow evaluation
config = {
    "system": {
        "name": "Workflow System",
        "type": "workflow",
        "stages": ["preprocessing", "inference", "postprocessing"]
    },
    "slos": slo_config
}
framework = EvaluationFramework(config)
result = framework.evaluate()
```

### Custom Metrics
```python
from ml_eval.collectors import BaseCollector

class DomainSpecificCollector(BaseCollector):
    def collect(self) -> Dict[str, float]:
        # Custom metric collection logic
        return {"custom_metric": value}
```

### Safety-Critical Continuous Improvement
```python
# Automated safety validation and retraining for Industrial AI
class SafetyCriticalImprovement:
    def __init__(self, evaluation_framework):
        self.framework = evaluation_framework
    
    def check_safety_compliance(self):
        result = self.framework.evaluate()
        
        if result.safety_violation_detected:
            # Immediate system shutdown for safety
            self.emergency_shutdown()
            self.create_safety_incident(result)
            
        if result.regulatory_compliance_violated:
            # Halt operations until compliance restored
            self.halt_operations()
            self.notify_regulatory_authorities(result)
            
        if result.environmental_conditions_changed:
            # Adapt model for new environmental conditions
            self.adapt_to_environment(result.environmental_data)
```

## Development

### Project Structure
```
ml-systems-evaluation/
├── ml_eval/                 # Main package
│   ├── __init__.py         # Package initialization with clean API
│   ├── core/               # Core framework components
│   │   ├── __init__.py     # Core module exports
│   │   ├── types.py        # Type definitions and enums
│   │   ├── config.py       # Configuration classes
│   │   └── framework.py    # Main evaluation framework
│   ├── collectors/         # Data collection modules
│   │   ├── __init__.py     # Collector module exports
│   │   ├── base.py         # Base collector interface
│   │   ├── online.py       # Real-time metric collection
│   │   ├── offline.py      # Historical data collection
│   │   ├── environmental.py # Environmental condition monitoring
│   │   └── regulatory.py   # Compliance monitoring
│   ├── evaluators/         # Evaluation engines
│   │   ├── __init__.py     # Evaluator module exports
│   │   ├── base.py         # Base evaluator interface
│   │   ├── reliability.py  # Reliability and SLO evaluation
│   │   ├── safety.py       # Safety-critical evaluation
│   │   ├── performance.py  # Performance metrics evaluation
│   │   ├── compliance.py   # Regulatory compliance evaluation
│   │   └── drift.py        # Data and model drift detection
│   ├── reports/            # Report generation
│   │   ├── __init__.py     # Report module exports
│   │   ├── base.py         # Base report interface
│   │   ├── reliability.py  # Reliability reports
│   │   ├── safety.py       # Safety reports
│   │   ├── compliance.py   # Compliance reports
│   │   └── business.py     # Business impact reports
│   ├── cli/                # Command-line interface
│   │   ├── __init__.py     # CLI module exports
│   │   ├── main.py         # Main CLI entry point
│   │   └── commands.py     # Command implementations
│   ├── config/             # Configuration management
│   │   ├── __init__.py     # Config module exports
│   │   ├── loader.py       # Configuration loading utilities
│   │   ├── validator.py    # Configuration validation
│   │   └── factory.py      # Configuration factory patterns
│   ├── templates/          # Industry-specific templates
│   │   ├── __init__.py     # Template module exports
│   │   └── factory.py      # Template factory patterns
│   ├── examples/           # Example configurations
│   │   ├── __init__.py     # Examples module exports
│   │   └── registry.py     # Example registry
│   └── utils/              # Utility functions
├── docs/                   # Comprehensive documentation
├── tests/                  # Test suite
├── examples/               # Example configuration files
├── setup.py               # Package installation
├── requirements.txt        # Dependencies
└── README.md              # This file
```

### Modular Architecture

The framework is designed with a modular architecture for easy maintenance and extension:

- **`core/`**: Central framework components with type safety and validation
- **`collectors/`**: Modular data collection with industrial focus
- **`evaluators/`**: Specialized evaluation engines for different aspects
- **`reports/`**: Comprehensive reporting for different stakeholders
- **`cli/`**: User-friendly command-line interface for system engineers
- **`config/`**: Robust configuration management for complex systems

### Developer-Friendly Features

The refactored framework provides several developer-friendly features:

#### **Industry-Specific Templates**
- Ready-to-use configurations for 6 industrial sectors
- Multiple template types per industry
- Industry-specific SLOs with appropriate safety and compliance standards

#### **Industrial-Focused CLI**
- Clear, industry-specific help messages
- Step-by-step guidance tailored for ML engineers in industrial sectors
- Detailed examples with explanations for each industry use case
- Error messages with actionable suggestions

#### **Modular Design**
- Easy to add new commands or templates
- Clear separation of concerns
- Maintainable codebase with modular CLI architecture
- Extensible architecture for custom requirements

#### **Industrial Focus**
- Safety-critical and business-critical system support
- Regulatory compliance templates (DO-178C for aviation safety systems)
- Environmental monitoring for harsh conditions
- Business impact assessment and reporting

### Running Tests
```bash
# Basic functionality test
python -c "
from ml_eval import EvaluationFramework, SLOConfig, ReliabilityReport
print('✅ Framework imports successfully')
"

# Test CLI functionality
python -m ml_eval.cli.main --help
python -m ml_eval.cli.main template --industry manufacturing
python -m ml_eval.cli.main quickstart --industry aviation

# Run comprehensive tests
pytest tests/ -v
pytest tests/safety/ -v  # Safety-critical tests
pytest tests/industry/ -v  # Industry-specific tests
```

## Dependencies

### Core Dependencies
- **PyYAML>=6.0.1**: Configuration file parsing
- **requests>=2.31.0**: HTTP client for metric collection
- **pydantic>=2.0.0**: Data validation and settings management
- **structlog>=23.1.0**: Structured logging
- **click>=8.1.0**: CLI framework

### Development Dependencies
- **pytest>=7.4.0**: Testing framework
- **black>=23.7.0**: Code formatting
- **flake8>=6.0.0**: Linting
- **mypy>=1.5.0**: Type checking
- **sphinx>=7.0.0**: Documentation generation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.
