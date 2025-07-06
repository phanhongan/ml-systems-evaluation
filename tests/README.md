# Testing Guide for ML Systems Evaluation Framework

This directory contains comprehensive tests for the ML Systems Evaluation Framework, designed to ensure reliability and safety for Industrial AI systems.

## Test Structure

### 🧪 Unit Tests
- **Core Framework**: Tests for core evaluation logic (`test_core.py`)
- **Collectors**: Tests for data collection components (`test_collectors.py`)
- **Evaluators**: Tests for evaluation engines (`test_evaluators.py`)
- **Reports**: Tests for report generation (`test_reports.py`)
- **CLI**: Tests for command-line interface (`test_cli.py`)

### 🔄 Integration Tests
- **End-to-End**: Complete evaluation pipeline tests (`test_integration.py`)
- **Industry Templates**: Tests for industry-specific configurations
- **CLI Commands**: Tests for command-line interface
- **Error Handling**: Tests for error scenarios and recovery

### 🏭 Industry-Specific Tests
- **Manufacturing**: Quality control and predictive maintenance scenarios
- **Aviation**: Safety-critical system validation
- **Energy**: Grid optimization and demand prediction
- **Healthcare**: Medical diagnostics and patient monitoring
- **Financial**: Fraud detection and risk assessment
- **Automotive**: Autonomous driving and vehicle safety

### 🔒 Safety and Compliance Tests
- **Safety Validation**: Tests for safety-critical requirements
- **Compliance Verification**: Tests for regulatory compliance
- **Error Budget Management**: Tests for error budget calculations
- **Incident Response**: Tests for incident handling procedures

## Running Tests

### Prerequisites
```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock

# Install the framework in development mode
pip install -e .
```

### Basic Test Execution
```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run with coverage report
python -m pytest --cov=ml_eval --cov-report=html --cov-report=term
```

### Using the Test Runner
```bash
# Run all tests
python tests/run_tests.py

# Run specific test types
python tests/run_tests.py --type unit
python tests/run_tests.py --type integration
python tests/run_tests.py --type core
python tests/run_tests.py --type collectors
python tests/run_tests.py --type evaluators
python tests/run_tests.py --type cli
python tests/run_tests.py --type reports

# Run with verbose output
python tests/run_tests.py --verbose

# Run with coverage
python tests/run_tests.py --coverage
```

### Running Specific Test Files
```bash
# Run core tests only
python -m pytest tests/test_core.py

# Run collectors tests only
python -m pytest tests/test_collectors.py

# Run integration tests only
python -m pytest tests/test_integration.py
```

### Running Specific Test Classes
```bash
# Run specific test class
python -m pytest tests/test_core.py::TestEvaluationFramework

# Run specific test method
python -m pytest tests/test_core.py::TestEvaluationFramework::test_framework_creation
```

## Test Categories

### Core Framework Tests (`test_core.py`)
- **SystemType**: Enum validation and string conversion
- **CriticalityLevel**: Criticality level validation
- **ComplianceStandard**: Compliance standard validation
- **SLOConfig**: Service Level Objective configuration
- **ErrorBudget**: Error budget tracking and alerts
- **MetricData**: Metric data container
- **EvaluationResult**: Evaluation result aggregation
- **EvaluationFramework**: Main framework orchestration

### Collector Tests (`test_collectors.py`)
- **BaseCollector**: Abstract collector interface
- **OnlineCollector**: Real-time metric collection
- **OfflineCollector**: Historical data collection
- **EnvironmentalCollector**: Environmental condition monitoring
- **RegulatoryCollector**: Compliance data collection
- **Integration**: Multiple collector coordination

### Evaluator Tests (`test_evaluators.py`)
- **BaseEvaluator**: Abstract evaluator interface
- **ReliabilityEvaluator**: System reliability assessment
- **SafetyEvaluator**: Safety-critical system evaluation
- **PerformanceEvaluator**: Performance metrics evaluation
- **ComplianceEvaluator**: Regulatory compliance assessment
- **DriftEvaluator**: Data and concept drift detection
- **Integration**: Multiple evaluator coordination

### CLI Tests (`test_cli.py`)
- **Parser**: Command-line argument parsing
- **Commands**: Individual command execution
- **Error Handling**: Error scenarios and recovery
- **Integration**: End-to-end CLI workflows

### Report Tests (`test_reports.py`)
- **BaseReport**: Abstract report interface
- **ReliabilityReport**: Reliability assessment reports
- **SafetyReport**: Safety violation reports
- **ComplianceReport**: Regulatory compliance reports
- **BusinessImpactReport**: Business impact assessment
- **Integration**: Multiple report type coordination

### Integration Tests (`test_integration.py`)
- **End-to-End**: Complete evaluation pipeline
- **Industry Scenarios**: Industry-specific workflows
- **Error Handling**: System failure recovery
- **Configuration**: Configuration management
- **Performance**: Scalability and performance

## Test Fixtures

The test suite includes comprehensive fixtures in `conftest.py`:

### Configuration Fixtures
- `sample_config`: Basic system configuration
- `safety_critical_config`: Safety-critical system configuration
- `manufacturing_config`: Manufacturing industry configuration
- `aviation_config`: Aviation industry configuration

### Data Fixtures
- `sample_metrics`: Sample metric data
- `sample_slos`: Sample SLO configurations
- `safety_slos`: Safety-critical SLO configurations
- `error_budget`: Sample error budget
- `evaluation_result`: Sample evaluation result

### Mock Fixtures
- `mock_collector`: Mock collector for testing
- `mock_evaluator`: Mock evaluator for testing
- `temp_config_file`: Temporary configuration file creator

### Environmental Fixtures
- `sample_environmental_conditions`: Environmental sensor data
- `sample_compliance_data`: Compliance standard data

## Test Coverage

The test suite provides comprehensive coverage for:

### Core Components
- ✅ Type definitions and enums
- ✅ Configuration classes
- ✅ Framework orchestration
- ✅ Error handling and validation

### Data Collection
- ✅ Online metric collection
- ✅ Offline data processing
- ✅ Environmental monitoring
- ✅ Regulatory compliance data

### Evaluation Engines
- ✅ Reliability assessment
- ✅ Safety validation
- ✅ Performance evaluation
- ✅ Compliance verification
- ✅ Drift detection

### Reporting
- ✅ Multiple report formats (JSON, HTML, PDF, CSV)
- ✅ Industry-specific reports
- ✅ Business impact assessment
- ✅ Compliance documentation

### CLI Interface
- ✅ Command parsing
- ✅ Argument validation
- ✅ Error handling
- ✅ Integration workflows

## Industry-Specific Testing

### Manufacturing
- Quality control defect detection
- Predictive maintenance scenarios
- Real-time monitoring workflows
- Business impact assessment

### Aviation
- Safety-critical decision validation
- Flight control system evaluation
- Environmental condition monitoring
- Regulatory compliance (DO-178C)

### Energy
- Grid optimization scenarios
- Demand prediction workflows
- Real-time monitoring
- Business impact assessment

### Healthcare
- Medical diagnostics validation
- Patient monitoring scenarios
- Regulatory compliance (FDA)
- Safety-critical workflows

### Financial
- Fraud detection scenarios
- Risk assessment workflows
- Regulatory compliance (SOX)
- Business impact evaluation

### Automotive
- Autonomous driving validation
- Vehicle safety assessment
- Environmental monitoring
- Regulatory compliance (ISO-26262)

## Continuous Integration

The test suite is designed for continuous integration with:

### Automated Testing
- Unit test execution
- Integration test validation
- Coverage reporting
- Performance benchmarking

### Quality Gates
- Minimum coverage thresholds
- Performance benchmarks
- Safety validation requirements
- Compliance verification

### Reporting
- Test result aggregation
- Coverage reports
- Performance metrics
- Quality indicators

## Best Practices

### Test Organization
- Group related tests in classes
- Use descriptive test names
- Include docstrings for complex tests
- Follow AAA pattern (Arrange, Act, Assert)

### Mock Usage
- Mock external dependencies
- Use realistic test data
- Verify mock interactions
- Clean up after tests

### Error Testing
- Test error conditions
- Verify error messages
- Test recovery scenarios
- Validate error handling

### Performance Testing
- Test with large datasets
- Measure execution time
- Test memory usage
- Validate scalability

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure the framework is installed in development mode
2. **Mock Failures**: Check mock setup and verification
3. **Configuration Errors**: Validate test configuration files
4. **Performance Issues**: Check test data size and complexity

### Debugging
```bash
# Run tests with debug output
python -m pytest -v -s

# Run specific failing test
python -m pytest tests/test_core.py::TestEvaluationFramework::test_framework_creation -v -s

# Run with coverage and debug
python -m pytest --cov=ml_eval --cov-report=term-missing -v
```

### Test Data
- Test data is generated dynamically
- Use realistic but safe test values
- Avoid hardcoded test data
- Use fixtures for reusable data

## Contributing

When adding new tests:

1. **Follow existing patterns**: Use similar structure and naming
2. **Add comprehensive coverage**: Test all code paths
3. **Include edge cases**: Test error conditions and boundaries
4. **Update documentation**: Keep this README current
5. **Run full test suite**: Ensure no regressions

### Test Naming Convention
- Test classes: `Test<ComponentName>`
- Test methods: `test_<description>`
- Integration tests: `test_<scenario>_<outcome>`

### Test Data Convention
- Use fixtures for reusable data
- Generate realistic test data
- Avoid hardcoded values
- Include edge cases and error conditions
