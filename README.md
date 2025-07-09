# 🚀 ML Systems Evaluation Framework

A reliability-focused evaluation framework for Industrial AI systems, applying Site Reliability Engineering (SRE) principles to machine learning evaluation.

## 🎯 The Problem

Industrial AI systems face unique challenges that traditional ML evaluation approaches don't address:

### **🛡️ Safety-Critical Requirements**
- **🚨 Zero Tolerance Failures**: Aircraft landing systems, medical diagnostics, autonomous vehicles where errors can be catastrophic
- **📋 Regulatory Standards**: Aviation (DO-178C), healthcare, financial services require continuous compliance validation
- **🌊 Environmental Constraints**: Underwater devices, extreme temperatures, harsh conditions that affect system reliability

### **💰 Business-Critical Operations**
- **💸 Immediate Financial Impact**: Manufacturing quality control, fraud detection where failures cost millions instantly
- **⚡ Real-time Decision Making**: Supply chain optimization, trading systems where delays cause cascading failures
- **👥 Public Safety**: Systems where failures affect public safety, requiring continuous monitoring and rapid response

### **❌ Traditional ML Evaluation Gaps**
- **🚫 No Safety Validation**: Standard ML evaluation doesn't assess catastrophic failure scenarios
- **📜 Missing Regulatory Compliance**: No built-in validation against industry-specific standards
- **🌡️ Inadequate Environmental Monitoring**: Doesn't account for harsh operating conditions
- **📊 No Business Impact Metrics**: Technical metrics don't connect to business outcomes

## 🎯 Why This Framework Matters

### **🔧 SRE Principles for Industrial AI**
This framework treats Industrial AI systems as critical infrastructure, applying proven SRE concepts:
- **🛡️ Safety-First Error Budgets**: Acceptable failure rates with zero tolerance for catastrophic failures
- **📋 Regulatory SLOs**: Service Level Objectives that include compliance requirements
- **🌊 Environmental Observability**: Monitoring that accounts for harsh operating conditions
- **💰 Business-Critical Reliability**: Focus on preventing immediate financial and safety impacts
- **🚨 Rapid Incident Response**: Structured approach to handling safety-critical and business-critical failures

### **🔄 Continuous Evaluation Lifecycle**
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

## 🔍 How Evaluation Informs the ML Lifecycle

### **🔬 Development Phase Insights**
- **🏗️ Model Architecture**: Performance bottlenecks reveal design flaws
- **📊 Data Quality**: Drift detection identifies training data issues
- **🔧 Feature Engineering**: Model degradation points to feature relevance changes
- **⚙️ Hyperparameter Tuning**: Real-world performance guides optimization

### **🚀 Deployment Phase Validation**
- **🧪 A/B Testing**: Structured comparison of model versions
- **🐦 Canary Deployments**: Gradual rollout with continuous evaluation
- **🔄 Rollback Triggers**: Automatic reversion based on SLO violations
- **📈 Infrastructure Scaling**: Performance metrics guide resource allocation

### **🏭 Production Phase Monitoring**
- **🚨 Real-time Alerts**: Immediate notification of SLO violations
- **📈 Trend Analysis**: Long-term performance degradation detection
- **🚨 Incident Response**: Structured approach to ML system failures
- **📊 Capacity Planning**: Resource needs based on usage patterns

### **🔄 Feedback Loop Benefits**
- **🔄 Model Retraining**: Triggered by drift detection and performance degradation
- **📊 Data Pipeline Updates**: Informed by data quality issues
- **🏗️ Architecture Evolution**: Driven by scalability and reliability needs
- **📈 Process Improvement**: Continuous refinement of ML operations

## 💼 Business Impact

### **🛡️ Risk Mitigation**
- **🚨 Prevent Catastrophic Failures**: Early detection of safety-critical system issues
- **📋 Regulatory Compliance**: Continuous validation for regulated industries
- **🛡️ Brand Protection**: Avoid public incidents that damage reputation
- **💰 Financial Loss Prevention**: Catch issues before they impact revenue

### **🏆 Operational Excellence**
- **🔧 Proactive Maintenance**: Fix issues before they become incidents
- **⚡ Resource Optimization**: Right-size infrastructure based on actual usage
- **👥 Team Efficiency**: Automated monitoring reduces manual oversight
- **📊 Data-Driven Decisions**: Metrics guide strategic ML investments

### **🚀 Competitive Advantage**
- **⚡ Faster Iteration**: Rapid feedback enables quick model improvements
- **🏆 Higher Quality**: Continuous evaluation maintains performance standards
- **🤝 Customer Trust**: Reliable ML systems build user confidence
- **💡 Innovation Velocity**: Safe experimentation with new ML approaches

## ✨ Key Features

- **🛡️ Safety-Critical Evaluation**: Zero tolerance for catastrophic failures with specialized safety metrics
- **📋 Regulatory Compliance**: Built-in validation against industry standards (DO-178C for aviation)
- **🌊 Environmental Monitoring**: Specialized collectors for harsh operating conditions
- **💰 Business-Critical Reliability**: SRE principles applied to systems with immediate financial impact
- **🤖 LLM-Powered Intelligence**: Advanced pattern recognition, natural language configuration, and intelligent report enhancement
- **🤖 Autonomous Agents**: Future-ready architecture for proactive monitoring, alerting, and scheduling
- **🔌 Extensible Architecture**: Plugin-based collectors and evaluators for domain-specific requirements
- **⚡ Real-time & Batch**: Online and offline evaluation for continuous monitoring
- **📋 Standards Enforcement**: Configurable quality gates with regulatory compliance checks

## 🎯 Supported Industries

The framework supports multiple industrial sectors with ready-to-use configurations and industry-specific requirements. Each industry has its own directory with detailed examples and documentation:

### **🏭 Manufacturing**
- **Predictive Maintenance**: Equipment failure prediction with VAE anomaly detection
- **Demand Forecasting**: Supply chain optimization and production planning
- **Key Features**: ISO compliance, cost optimization, real-time monitoring
- **Examples**: [`examples/industries/manufacturing/`](./examples/industries/manufacturing/)

### **✈️ Aviation**  
- **Safety-Critical Systems**: Aircraft landing and flight control assistance
- **Key Features**: DO-178C compliance, sub-500ms response times, environmental adaptation
- **Examples**: [`examples/industries/aviation/`](./examples/industries/aviation/)

### **🚢 Maritime**
- **Collision Avoidance**: Vessel collision detection and navigation safety
- **Key Features**: COLREGs compliance, real-time alerts, multi-vessel tracking
- **Examples**: [`examples/industries/maritime/`](./examples/industries/maritime/)

### **🔬 Semiconductor**
- **Digital Twins**: Manufacturing process monitoring and yield prediction
- **Key Features**: Real-time process control, quality metrics, equipment monitoring
- **Examples**: [`examples/industries/semiconductor/`](./examples/industries/semiconductor/)

### **🐟 Aquaculture**
- **Species Classification**: Sonar-based fish species identification and environmental hazard detection
- **Key Features**: Environmental monitoring, regulatory compliance, resource optimization
- **Examples**: [`examples/industries/aquaculture/`](./examples/industries/aquaculture/)

### 📋 Additional Examples

See the [`examples/industries/`](./examples/industries/) directory for complete configuration files covering all scenarios. Each industry directory contains detailed README files with specific use cases, requirements, and implementation guidance.

For a comprehensive overview of all examples, templates, and tutorials, see the [examples/](./examples/).

## 🏗️ Architecture

The framework follows a hybrid architecture that combines deterministic components with LLM-powered intelligence:

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
                                                        │
                                                        ▼
                                              ┌─────────────────┐
                                              │   LLM Layer     │
                                              │                 │
                                              │ • Analysis      │
                                              │ • Assistant     │
                                              │ • Enhancement   │
                                              └─────────────────┘
                                                        │
                                                        ▼
                                              ┌─────────────────┐
                                              │  Agents (Future)│
                                              │                 │
                                              │ • Monitoring    │
                                              │ • Alerting      │
                                              │ • Scheduling    │
                                              └─────────────────┘
```

## 🚀 Quick Start

### 📦 Installation

```bash
# Clone the repository
git clone <repository-url>
cd ml-systems-evaluation

# Install in development mode
uv sync --group dev

# (Optional) Activate the virtual environment managed by UV
uv shell

# For production installs (main dependencies only)
# uv sync --group main

```

**Note**: This project uses UV for dependency management and packaging. 
See [pyproject.toml](./pyproject.toml) for the full, up-to-date list of dependencies.
For detailed installation instructions, see [docs/user-guides/installation.md](./docs/user-guides/installation.md).

### 🎯 Getting Started (For Industrial ML Engineers)

```bash
# 1. List available templates for your industry
ml-eval template --industry manufacturing --type list

# 2. Get a specific template for your industry
ml-eval template --industry manufacturing --type predictive_maintenance > maintenance-system.yaml

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

### ⚡ Quick Commands

```bash
# Get help and examples
ml-eval quickstart --industry aviation
ml-eval example --type aircraft-model --detailed

# Show all available commands
ml-eval --help

# Additional template examples
ml-eval template --industry aviation --type safety_decision --output safety-system.yaml
ml-eval template --industry semiconductor --type digital_twins --output digital-twins-system.yaml

# Using example configurations
ml-eval dev --config examples/industries/aviation/aircraft-landing.yaml --mode validation --strict
ml-eval evaluate --config examples/industries/maritime/collision-avoidance.yaml --mode single
ml-eval monitor --config examples/industries/manufacturing/predictive-maintenance.yaml --interval 60
ml-eval evaluate --config examples/industries/semiconductor/etching-digital-twins.yaml --mode single

# Additional reporting
ml-eval report --type safety --period 30d
```

## 🔧 Core Components

### 📊 Collectors
- **⚡ OnlineCollector**: Real-time metrics from running systems
- **📁 OfflineCollector**: Historical data from logs and databases
- **🌊 EnvironmentalCollector**: Specialized monitoring for harsh conditions (temperature, pressure, etc.)
- **📋 RegulatoryCollector**: Compliance metrics for industry standards
- **🔌 CustomCollector**: Extensible interface for domain-specific metrics

### 🔍 Evaluators
- **🛡️ ReliabilityEvaluator**: SLI/SLO compliance and error budgets with safety thresholds
- **🚨 SafetyEvaluator**: Critical system safety validation with zero-tolerance checks
- **📋 RegulatoryEvaluator**: Compliance validation against industry standards
- **🌊 EnvironmentalEvaluator**: Performance assessment under harsh conditions
- **📈 DriftEvaluator**: Data and model drift detection with business impact assessment

### 🤖 LLM Integration Layer
- **🤖 LLMAnalysisEngine**: Advanced pattern recognition and intelligent drift detection
- **🤖 LLMAssistantEngine**: Natural language configuration and troubleshooting assistance
- **🤖 LLMEnhancementEngine**: Intelligent report enhancement and business impact translation

### 🤖 Autonomous Agents (Future)
- **🤖 MonitoringAgent**: Autonomous real-time monitoring and health checks
- **🤖 AlertingAgent**: Intelligent alert prioritization and routing
- **🤖 RLAgent**: Adaptive decision-making and scheduling

### 📊 Reports
- **🛡️ ReliabilityReport**: Error budgets, SLO compliance, incident analysis
- **🚨 SafetyReport**: Safety-critical metrics and compliance status
- **📋 RegulatoryReport**: Compliance validation and audit trails
- **💰 BusinessImpactReport**: Technical metrics connected to business outcomes

## 🔧 SRE Integration

### 📋 Service Level Objectives (SLOs)

For comprehensive SLO configuration guidance, see the [SLO Configuration Guide](./docs/reference/slo-configuration.md). The framework supports:

- **🛡️ Safety-Critical SLOs**: Zero-tolerance thresholds for catastrophic failures
- **💰 Business-Critical SLOs**: Performance targets with immediate financial impact
- **🌊 Environmental SLOs**: Adaptation to harsh operating conditions
- **📋 Regulatory SLOs**: Compliance with industry standards (DO-178C, COLREGs, etc.)

### 🚨 Error Budget Policies
- **🛡️ Safety-First Alerts**: Immediate notification for safety-critical budget violations
- **📋 Regulatory Compliance**: Automatic audit trail for compliance violations
- **💰 Business Impact Assessment**: Connect budget exhaustion to financial impact
- **🌊 Environmental Adaptation**: Adjust thresholds based on operating conditions

## 🚀 Advanced Features

### 🛡️ Safety-Critical Development
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

### 🤖 LLM-Powered Intelligence
The framework integrates LLM capabilities for enhanced analysis and decision support:

- **Advanced Pattern Recognition**: Intelligent drift detection and anomaly identification
- **Natural Language Configuration**: Generate configurations from plain English requirements
- **Intelligent Report Enhancement**: Add business context and insights to technical reports
- **Smart Troubleshooting**: AI-powered problem diagnosis and solution recommendations

### 🤖 Autonomous Agents (Future)
The framework is designed for future autonomous capabilities:

- **Proactive Monitoring**: Autonomous system health monitoring and issue detection
- **Intelligent Alerting**: Smart alert prioritization and context-aware notifications
- **Dynamic Scheduling**: Autonomous task scheduling and resource optimization

### 🔄 Workflow Evaluation
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

### 🔌 Custom Metrics
```python
from ml_eval.collectors import BaseCollector

class DomainSpecificCollector(BaseCollector):
    def collect(self) -> Dict[str, float]:
        # Custom metric collection logic
        return {"custom_metric": value}
```



### 🛡️ Safety-Critical Continuous Improvement
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

## 🛠️ Development

### 📚 Documentation
For comprehensive documentation including user guides, developer guides, and industry-specific guides, see the [Documentation Index](./docs/README.md).

### 📁 Project Structure
See [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) for the most up-to-date and detailed project structure.

### 🔧 Modular Architecture

The framework is designed with a modular architecture for easy maintenance and extension:

- **`core/`**: Central framework components with type safety and validation
- **`collectors/`**: Modular data collection with industrial focus
- **`evaluators/`**: Specialized evaluation engines for different aspects
- **`reports/`**: Comprehensive reporting for different stakeholders
- **`llm/`**: LLM integration layer with analysis, assistant, and enhancement engines
- **`agents/`**: Future autonomous agents for monitoring, alerting, and scheduling
- **`cli/`**: User-friendly command-line interface for system engineers
- **`config/`**: Robust configuration management for complex systems

### 👨‍💻 Developer-Friendly Features

The refactored framework provides several developer-friendly features:

#### **🏭 Industry-Specific Templates**
- Ready-to-use configurations for 5 industrial sectors
- Multiple template types per industry
- Industry-specific SLOs with appropriate safety and compliance standards

#### **🖥️ Industrial-Focused CLI**
- Clear, industry-specific help messages
- Step-by-step guidance tailored for ML engineers in industrial sectors
- Detailed examples with explanations for each industry use case
- Error messages with actionable suggestions

#### **🔧 Modular Design**
- Easy to add new commands or templates
- Clear separation of concerns
- Maintainable codebase with modular CLI architecture
- Extensible architecture for custom requirements

#### **🏭 Industrial Focus**
- Safety-critical and business-critical system support
- Regulatory compliance templates (DO-178C for aviation safety systems)
- Environmental monitoring for harsh conditions
- Business impact assessment and reporting

### 🧪 Running Tests
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

**Note**: For detailed testing instructions, see [docs/developer/testing.md](./docs/developer/testing.md)

## 🤝 Contributing

We welcome contributions! Please see our [Development Guide](docs/developer/development.md) for comprehensive information about:

- **🔧 Code Quality Tools**: Black, Ruff
- **🧪 Testing Practices**: Unit, integration, and end-to-end tests
- **🔄 Development Workflow**: Setup, coding standards, and CI/CD
- **📝 Code Style Guidelines**: Python style, naming conventions, documentation

### ⚡ Quick Development Setup

```bash
# Install dependencies
uv sync --group dev

# Run code quality checks
uv run black .          # Format code
uv run ruff check .     # Lint, type check, and sort imports
uv run ruff format .    # Format code

# Run tests
uv run pytest

# Build package
uv build
```

### 📝 Code Quality Standards

The project enforces strict code quality standards:

- **⚫ Black**: 88-character line length, opinionated formatting
- **🦊 Ruff**: Fast linting, type checking, and import sorting

All code must pass these checks before merging.

## 📄 License

MIT License - see [LICENSE](./LICENSE) file for details.
