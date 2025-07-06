# ML Systems Evaluation Framework - Project Structure

This document provides a comprehensive overview of the refactored project structure, designed specifically for system engineers working with Industrial AI systems.

## 📁 Root Directory Structure

```
ml-systems-evaluation/
├── ml_eval/                    # Main package directory
│   ├── __init__.py            # Package initialization with clean API
│   ├── core/                  # Core framework components
│   ├── collectors/            # Data collection modules
│   ├── evaluators/            # Evaluation engines
│   ├── reports/               # Report generation
│   ├── templates/             # Industry-specific templates
│   ├── examples/              # Example configurations
│   ├── cli/                   # Command-line interface
│   ├── config/                # Configuration management
│   └── utils/                 # Utility functions
├── docs/                      # Comprehensive documentation
├── tests/                     # Test suite
├── examples/                  # Example configuration files
├── scripts/                   # Utility scripts
├── requirements.txt           # Python dependencies
├── requirements-test.txt      # Test dependencies
├── setup.py                  # Package installation
├── README.md                 # Main project documentation
├── PROJECT_STRUCTURE.md      # This file
└── LICENSE                   # MIT License
```

## 🏗️ Core Package Structure (`ml_eval/`)

### Core Framework (`core/`)
```
core/
├── __init__.py               # Core module exports
├── types.py                  # Type definitions and enums
├── config.py                 # Configuration classes (SLO, ErrorBudget, etc.)
└── framework.py              # Main evaluation framework
```

**Purpose**: Central framework components that define the evaluation system architecture.

**Key Components**:
- `SystemType`, `CriticalityLevel`, `ComplianceStandard` enums
- `SLOConfig`, `ErrorBudget`, `EvaluationResult` data classes
- `EvaluationFramework` main orchestrator class

### Data Collection (`collectors/`)
```
collectors/
├── __init__.py               # Collector module exports
├── base.py                   # Base collector interface
├── online.py                 # Real-time metric collection
├── offline.py                # Historical data collection
├── environmental.py          # Environmental condition monitoring
└── regulatory.py             # Compliance monitoring
```

**Purpose**: Modular data collection from various sources with industrial focus.

**Key Features**:
- Pluggable collector architecture
- Support for harsh environmental conditions
- Regulatory compliance monitoring
- Health checking and error handling

### Evaluation Engines (`evaluators/`)
```
evaluators/
├── __init__.py               # Evaluator module exports
├── base.py                   # Base evaluator interface
├── reliability.py            # Reliability and SLO evaluation
├── safety.py                 # Safety-critical system evaluation
├── performance.py            # Performance metrics evaluation
├── compliance.py             # Regulatory compliance evaluation
└── drift.py                  # Data and model drift detection
```

**Purpose**: Specialized evaluation engines for different aspects of Industrial AI systems.

**Key Features**:
- Safety-critical evaluation with zero-tolerance checks
- Regulatory compliance validation
- Business impact assessment
- Environmental adaptation

### Reporting (`reports/`)
```
reports/
├── __init__.py               # Report module exports
├── base.py                   # Base report interface
├── reliability.py            # Reliability reports
├── safety.py                 # Safety reports
├── compliance.py             # Compliance reports
└── business.py               # Business impact reports
```

**Purpose**: Generate comprehensive reports for different stakeholders.

**Key Features**:
- Industry-specific report formats
- Compliance audit trails
- Business impact quantification
- Trend analysis and forecasting

### Command-Line Interface (`cli/`)
```
cli/
├── __init__.py               # CLI module exports
├── main.py                   # Main CLI entry point
└── commands.py               # Command implementations
```

**Purpose**: User-friendly command-line interface for system engineers.

**Key Features**:
- Industry-specific commands
- Template generation
- Configuration validation
- Real-time monitoring

### Configuration Management (`config/`)
```
config/
├── __init__.py               # Config module exports
├── loader.py                 # Configuration loading utilities
├── validator.py              # Configuration validation
└── factory.py                # Configuration factory patterns
```

**Purpose**: Robust configuration management for complex industrial systems.

**Key Features**:
- Multi-format support (YAML, JSON)
- Industry-specific validation
- Template-based configuration
- Error handling and recovery

## 📚 Documentation Structure (`docs/`)

```
docs/
├── README.md                 # Documentation overview
├── getting-started.md        # Quick start guide
├── configuration.md          # Configuration guide
├── cli-reference.md         # CLI documentation
├── architecture.md           # System architecture
├── api-reference.md         # API documentation
├── extending.md             # Extension guide
├── testing.md               # Testing guide
├── templates/               # Template documentation
│   └── README.md
└── industries/              # Industry-specific guides
    ├── manufacturing.md
    ├── aviation.md
    ├── energy.md
    ├── healthcare.md
    ├── financial.md
    └── automotive.md
```

**Purpose**: Comprehensive documentation tailored for system engineers.

**Key Features**:
- Industry-specific examples
- Step-by-step tutorials
- Troubleshooting guides
- Best practices

## 🧪 Test Structure (`tests/`)

```
tests/
├── README.md                 # Testing guide
├── unit/                     # Unit tests
│   ├── core/
│   ├── collectors/
│   ├── evaluators/
│   ├── reports/
│   └── config/
├── integration/              # Integration tests
│   ├── e2e/
│   ├── cli/
│   ├── templates/
│   └── errors/
├── industry/                 # Industry-specific tests
│   ├── manufacturing/
│   ├── aviation/
│   ├── energy/
│   ├── healthcare/
│   ├── financial/
│   └── automotive/
├── safety/                   # Safety-critical tests
├── compliance/               # Compliance tests
└── data/                     # Test data
    ├── configs/
    ├── metrics/
    ├── expected/
    └── templates/
```

**Purpose**: Comprehensive testing for reliability and safety.

**Key Features**:
- Safety-critical test scenarios
- Industry-specific test cases
- Compliance validation tests
- Error handling tests

## 🏭 Industry-Specific Structure

### Template System
- **Manufacturing**: Quality control, predictive maintenance
- **Aviation**: Safety-critical decisions, flight control
- **Energy**: Grid optimization, demand prediction
- **Healthcare**: Medical diagnostics, patient monitoring
- **Financial**: Fraud detection, risk assessment
- **Automotive**: Autonomous driving, vehicle safety

### Configuration Examples
- Pre-configured SLOs for each industry
- Compliance standards integration
- Environmental monitoring setup
- Business impact metrics

## 🔧 Development Workflow

### For System Engineers
1. **Start with Templates**: Use industry-specific templates
2. **Configure SLOs**: Define safety and business requirements
3. **Add Collectors**: Configure data sources
4. **Run Evaluations**: Execute evaluation pipeline
5. **Monitor Continuously**: Set up ongoing monitoring

### For Developers
1. **Understand Architecture**: Review core framework design
2. **Extend Components**: Add custom collectors/evaluators
3. **Add Tests**: Write comprehensive tests
4. **Update Documentation**: Keep docs current

### For Quality Assurance
1. **Safety Testing**: Focus on safety-critical scenarios
2. **Compliance Testing**: Verify regulatory requirements
3. **Integration Testing**: Test complete workflows
4. **Performance Testing**: Validate under load

## 🚀 Key Benefits of Refactored Structure

### For System Engineers
- **Clear Separation**: Easy to understand component boundaries
- **Industry Focus**: Pre-configured for specific industries
- **Safety First**: Built-in safety-critical considerations
- **Compliance Ready**: Regulatory standards integration

### For Developers
- **Modular Design**: Easy to extend and maintain
- **Type Safety**: Strong typing with enums and dataclasses
- **Error Handling**: Comprehensive error management
- **Testing Support**: Extensive test infrastructure

### For Organizations
- **Scalability**: Modular architecture supports growth
- **Maintainability**: Clear structure reduces technical debt
- **Reliability**: Comprehensive testing ensures quality
- **Compliance**: Built-in regulatory support

## 📋 File Naming Conventions

### Python Files
- **Modules**: `snake_case.py`
- **Classes**: `PascalCase` within files
- **Functions**: `snake_case` within classes
- **Constants**: `UPPER_SNAKE_CASE`

### Configuration Files
- **Templates**: `industry_type.yaml`
- **Examples**: `example_name.yaml`
- **Tests**: `test_<category>_<name>.py`

### Documentation Files
- **Guides**: `topic_name.md`
- **API Docs**: `module_name.md`
- **Industry Docs**: `industry_name.md`

## 🔍 Navigation Tips

### Finding Components
- **Core Logic**: Look in `ml_eval/core/`
- **Data Collection**: Check `ml_eval/collectors/`
- **Evaluation**: See `ml_eval/evaluators/`
- **Industry Templates**: Browse `ml_eval/templates/`

### Understanding Configuration
- **SLOs**: Defined in `core/config.py`
- **Types**: See `core/types.py`
- **Validation**: Check `config/validator.py`

### Adding Features
- **New Collectors**: Add to `collectors/` directory
- **New Evaluators**: Add to `evaluators/` directory
- **New Reports**: Add to `reports/` directory
- **New Templates**: Add to `templates/` directory

This refactored structure provides a clear, maintainable, and extensible foundation for Industrial AI system evaluation, with strong focus on safety, compliance, and system engineering best practices.
