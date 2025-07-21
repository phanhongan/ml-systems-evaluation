# 🏭 ML Systems Evaluation Framework

An evaluation framework for Industrial AI systems, applying Site Reliability Engineering (SRE) principles to machine learning evaluation.

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
This framework treats Industrial AI systems as critical infrastructure, applying SRE concepts:
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
- **🤖 LLM-Powered Intelligence**: Pattern recognition, natural language configuration, and report enhancement
- **🤖 Autonomous Agents**: Future-ready architecture for proactive monitoring, alerting, and scheduling
- **🔌 Extensible Architecture**: Plugin-based collectors and evaluators for domain-specific requirements
- **⚡ Real-time & Batch**: Online and offline evaluation for continuous monitoring
- **📋 Standards Enforcement**: Configurable quality gates with regulatory compliance checks

## 🎯 Supported Industries

The framework supports multiple industrial sectors with ready-to-use configurations and industry-specific requirements. Each industry has its own directory with detailed examples and documentation:

### **🐟 Aquaculture**
- **Species Classification**: Sonar-based fish species identification and environmental hazard detection
- **Key Features**: Environmental monitoring, regulatory compliance, resource optimization
- **Examples**: [`examples/industries/aquaculture/`](./examples/industries/aquaculture/)

### **✈️ Aviation**  
- **Safety-Critical Systems**: Aircraft landing and flight control assistance
- **Key Features**: DO-178C compliance, sub-500ms response times, environmental adaptation
- **Examples**: [`examples/industries/aviation/`](./examples/industries/aviation/)

### **🔒 Cybersecurity**
- **Agentic Security Operations**: Multi-agent AI workflows for alert triage, investigation, and response
- **Key Features**: Cost-optimized LLM integration, RAG-powered threat intelligence, explainable AI decisions, multi-TB data processing
- **Examples**: [`examples/industries/cybersecurity/`](./examples/industries/cybersecurity/)

### **⚡ Energy**
- **Energy Optimization Recommendations**: ML-driven recommendations for facility energy consumption and cost reduction
- **Key Features**: Real-time energy monitoring, cost reduction tracking, multi-facility support
- **Examples**: [`examples/industries/energy/`](./examples/industries/energy/)

### **🏭 Manufacturing**
- **Predictive Maintenance**: Equipment failure prediction with VAE anomaly detection
- **Demand Forecasting**: Supply chain optimization and production planning
- **Key Features**: ISO compliance, cost optimization, real-time monitoring
- **Examples**: [`examples/industries/manufacturing/`](./examples/industries/manufacturing/)

### **🚢 Maritime**
- **Collision Avoidance**: Vessel collision detection and navigation safety
- **Key Features**: COLREGs compliance, real-time alerts, multi-vessel tracking
- **Examples**: [`examples/industries/maritime/`](./examples/industries/maritime/)

### **🔬 Semiconductor**
- **Digital Twins**: Manufacturing process monitoring and yield prediction
- **Key Features**: Real-time process control, quality metrics, equipment monitoring
- **Examples**: [`examples/industries/semiconductor/`](./examples/industries/semiconductor/)

### 📋 Additional Examples

See the [`examples/industries/`](./examples/industries/) directory for complete configuration files covering all scenarios. Each industry directory contains detailed README files with specific use cases, requirements, and implementation guidance.

For an overview of all examples, templates, and tutorials, see the [examples/](./examples/).

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
                                              │     Agents      │
                                              │                 │
                                              │ • RL Agent      │
                                              │ • Monitoring*   │
                                              │ • Alerting*     │
                                              └─────────────────┘
```

> **📋 Architecture Details**: For detailed technical architecture information, component interactions, and implementation specifics, see [Architecture Overview](./docs/developer/architecture.md).

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
# 1. Create a new configuration file
ml-eval create-config --output my-system.yaml --system-name "My ML System" --industry manufacturing

# 2. Validate your configuration
ml-eval validate my-system.yaml

# 3. Run health check on your system
ml-eval health my-system.yaml

# 4. Collect data from your system
ml-eval collect my-system.yaml --output collected-data.json

# 5. Evaluate your system metrics
ml-eval evaluate my-system.yaml --data collected-data.json --output results.json

# 6. Generate reports
ml-eval report my-system.yaml --results results.json --output reports.json

# 7. Run complete evaluation pipeline
ml-eval run my-system.yaml --output complete-results.json
```

### ⚡ Quick Commands

```bash
# Show all available commands
ml-eval --help

# Create new configurations for different industries
ml-eval create-config --output aviation-system.yaml --system-name "Aircraft Landing System" --industry aviation --criticality safety_critical
ml-eval create-config --output security-system.yaml --system-name "Security Operations" --industry cybersecurity --criticality business_critical

# Validate configurations (use existing example files)
ml-eval validate examples/industries/aviation/aircraft-landing.yaml
ml-eval validate examples/industries/maritime/collision-avoidance.yaml
ml-eval validate examples/industries/manufacturing/predictive-maintenance.yaml
ml-eval validate examples/industries/semiconductor/etching-digital-twins.yaml
ml-eval validate examples/industries/cybersecurity/security-operations.yaml

# Run health checks
ml-eval health examples/industries/aviation/aircraft-landing.yaml

# List configured components
ml-eval list-collectors examples/industries/manufacturing/predictive-maintenance.yaml
ml-eval list-evaluators examples/industries/cybersecurity/security-operations.yaml
ml-eval list-reports examples/industries/aviation/aircraft-landing.yaml

# Run evaluations
ml-eval run examples/industries/aviation/aircraft-landing.yaml --output aviation-results.json
ml-eval run examples/industries/cybersecurity/security-operations.yaml --output security-results.json
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
- **🤖 LLMAnalysisEngine**: Pattern recognition and drift detection
- **🤖 LLMAssistantEngine**: Natural language configuration and troubleshooting assistance
- **🤖 LLMEnhancementEngine**: Report enhancement and business impact translation

### 🤖 Autonomous Agents
- **🤖 RLAgent**: Adaptive decision-making with LLM integration and safety constraints
- **🤖 MonitoringAgent** 🚧: Autonomous real-time monitoring and health checks _(planned)_
- **🤖 AlertingAgent** 🚧: Alert prioritization and routing _(planned)_

> **📋 Agent Details**: For comprehensive agent implementation details, RL loop architecture, and usage examples, see [Architecture Overview](./docs/developer/architecture.md#agent-implementation-status).

### 📊 Reports
- **🛡️ ReliabilityReport**: Error budgets, SLO compliance, incident analysis
- **🚨 SafetyReport**: Safety-critical metrics and compliance status
- **📋 RegulatoryReport**: Compliance validation and audit trails
- **💰 BusinessImpactReport**: Technical metrics connected to business outcomes

## 🔧 SRE Integration

### 📋 Service Level Objectives (SLOs)

For SLO configuration guidance, see the [SLO Configuration Guide](./docs/reference/slo-configuration.md). The framework supports:

- **🛡️ Safety-Critical SLOs**: Zero-tolerance thresholds for catastrophic failures
- **💰 Business-Critical SLOs**: Performance targets with immediate financial impact
- **🌊 Environmental SLOs**: Adaptation to harsh operating conditions
- **📋 Regulatory SLOs**: Compliance with industry standards (DO-178C, COLREGs, etc.)

### 🚨 Error Budget Policies
- **🛡️ Safety-First Alerts**: Immediate notification for safety-critical budget violations
- **📋 Regulatory Compliance**: Automatic audit trail for compliance violations
- **💰 Business Impact Assessment**: Connect budget exhaustion to financial impact
- **🌊 Environmental Adaptation**: Adjust thresholds based on operating conditions

## 🔧 Additional Features

### 🛡️ Safety-Critical Development
The framework enables Industrial AI development with built-in safety and compliance:
- **Safety-First SLOs**: Zero-tolerance thresholds for catastrophic failures  
- **Real-time Validation**: Continuous safety validation during development
- **Regulatory Compliance**: Built-in validation against industry standards (DO-178C, etc.)
- **Emergency Protocols**: Automatic system shutdown for safety violations

### 🤖 LLM-Powered Intelligence
Enhanced analysis and decision support capabilities:
- **Pattern Recognition**: Drift detection and anomaly identification
- **Natural Language Configuration**: Generate configurations from plain English requirements
- **Report Enhancement**: Add business context and insights to technical reports
- **Smart Troubleshooting**: AI-powered problem diagnosis and solution recommendations

### 🤖 Autonomous Agents
**Currently Available:**
- **🤖 RL Agent**: Adaptive decision-making, resource allocation, and threshold optimization with LLM integration

**Planned Capabilities:**
- **Proactive Monitoring**: Autonomous system health monitoring and issue detection
- **Alert Management**: Smart alert prioritization and context-aware notifications
- **Dynamic Scheduling**: Autonomous task scheduling and resource optimization

### 🔌 Extensibility
- **Custom Collectors**: Domain-specific data collection interfaces
- **Custom Evaluators**: Specialized evaluation logic for industry requirements
- **Custom Reports**: Tailored reporting formats and outputs
- **LLM Integration**: Support for multiple LLM providers and custom models

> **📋 Code Examples**: For detailed code examples, usage patterns, and implementation guides, see [Architecture Overview](./docs/developer/architecture.md) and [Getting Started Guide](./docs/user-guides/getting-started.md).

## 🛠️ Development

### 📚 Documentation
The project includes comprehensive documentation in a simplified format:

- **[📖 Markdown Documentation](./docs/README.md)**: Primary documentation with user guides, developer guides, and industry-specific examples
- **[🔧 Sphinx Documentation](./docs_sphinx/)**: Auto-generated API documentation and navigation
- **[🔧 Development Guide](./docs/developer/development.md)**: Development setup and contribution guidelines

**Quick Start with Documentation:**
```bash
# Build Sphinx documentation
make docs-sphinx

# Serve documentation locally
make docs-sphinx-serve

# View built documentation
open docs_sphinx/build/html/index.html
```

### 📁 Project Structure
See [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) for the most up-to-date and detailed project structure.

### 🔧 Modular Architecture

The framework is designed with a modular architecture for easy maintenance and extension:

- **`core/`**: Central framework components with type safety and validation
- **`collectors/`**: Modular data collection with industrial focus
- **`evaluators/`**: Specialized evaluation engines for different aspects
- **`reports/`**: Reporting for different stakeholders
- **`llm/`**: LLM integration layer with analysis, assistant, and enhancement engines
- **`agents/`**: Autonomous agents (RL Agent implemented, monitoring/alerting planned)
- **`cli/`**: User-friendly command-line interface for system engineers
- **`config/`**: Configuration management for complex systems

> **📋 Technical Details**: For component interfaces, data flow diagrams, and extension points, see [Architecture Overview](./docs/developer/architecture.md).

### 👨‍💻 Developer-Friendly Features

The refactored framework provides several developer-friendly features:

#### **🏭 Industry-Specific Templates**
- Ready-to-use configurations for 6 industrial sectors
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
# Using Makefile (recommended)
make test
make test-verbose
make test-coverage

# Or manually
pytest tests/ -v
pytest tests/safety/ -v  # Safety-critical tests
pytest tests/industry/ -v  # Industry-specific tests
```

**Note**: For detailed testing instructions, see [docs/developer/testing.md](./docs/developer/testing.md)

## 🤝 Contributing

We welcome contributions! Please see our [Development Guide](docs/developer/development.md) for information about:

- **🔧 Code Quality Tools**: Ruff
- **🧪 Testing Practices**: Unit, integration, and end-to-end tests
- **🔄 Development Workflow**: Setup, coding standards, and CI/CD
- **📝 Code Style Guidelines**: Python style, naming conventions, documentation

### ⚡ Quick Development Setup

```bash
# Using Makefile (recommended)
make install-dev
make check
make test
make build

# Or manually
uv sync --extra dev
uv run ruff check .
uv run ruff format .
uv run pytest
uv build
```

### 📝 Code Quality Standards

The project enforces strict code quality standards:

- **🦊 Ruff**: Fast linting, formatting, type checking, and import sorting with Black-compatible settings

All code must pass these checks before merging.

## 📄 License

MIT License - see [LICENSE](./LICENSE) file for details.
