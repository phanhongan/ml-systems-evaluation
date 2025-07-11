# 🖥️ CLI Reference

This document provides a complete reference for all command-line interface (CLI) commands available in the ML Systems Evaluation Framework.

## 📋 Command Overview

```bash
ml-eval [COMMAND] [OPTIONS]
```

## 🌍 Global Options

```bash
--config, -c FILE          Configuration file path
--verbose, -v              Enable verbose output
--quiet, -q                Suppress output
--log-level LEVEL          Set log level (DEBUG, INFO, WARNING, ERROR)
--output-dir DIR           Output directory for reports
--format FORMAT            Output format (json, yaml, html, pdf)
```

## 🎯 Main Commands

### 🔍 Evaluate Command

Run a complete evaluation of your ML system.

```bash
ml-eval evaluate [OPTIONS]
```

**Options:**
```bash
--config, -c FILE          Configuration file path
--evaluator NAME           Run specific evaluator only
--collector NAME           Run specific collector only
--report NAME              Generate specific report only
--dry-run                  Show what would be executed without running
--force                    Force execution even if warnings exist
--parallel                 Run evaluators in parallel
--timeout SECONDS          Set execution timeout
```

**Examples:**
```bash
# Run complete evaluation
ml-eval evaluate --config config.yaml

# Run specific evaluator
ml-eval evaluate --config config.yaml --evaluator performance

# Run with custom output
ml-eval evaluate --config config.yaml --output-dir ./my_reports/

# Dry run to see what would happen
ml-eval evaluate --config config.yaml --dry-run
```

### 📊 Collect Command

Collect data from configured sources.

```bash
ml-eval collect [OPTIONS]
```

**Options:**
```bash
--config, -c FILE          Configuration file path
--collector NAME           Run specific collector only
--data-source NAME         Collect from specific data source
--start-date DATE          Start date for data collection (YYYY-MM-DD)
--end-date DATE            End date for data collection (YYYY-MM-DD)
--batch-size SIZE          Set batch size for collection
--force                    Force collection even if data exists
--validate                 Validate collected data
```

**Examples:**
```bash
# Collect all data
ml-eval collect --config config.yaml

# Collect specific data source
ml-eval collect --config config.yaml --data-source quality_database

# Collect with date range
ml-eval collect --config config.yaml --start-date 2024-01-01 --end-date 2024-01-31

# Validate collected data
ml-eval collect --config config.yaml --validate
```

### 📊 Report Command

Generate reports from evaluation results.

```bash
ml-eval report [OPTIONS]
```

**Options:**
```bash
--config, -c FILE          Configuration file path
--report NAME              Generate specific report type
--format FORMAT            Output format (html, pdf, json, csv)
--output-path PATH         Output file path
--template TEMPLATE        Use custom report template
--include-charts           Include charts in reports
--include-recommendations  Include recommendations
--executive-summary        Include executive summary
```

**Examples:**
```bash
# Generate all reports
ml-eval report --config config.yaml

# Generate specific report
ml-eval report --config config.yaml --report business

# Generate with custom format
ml-eval report --config config.yaml --format pdf

# Generate with custom template
ml-eval report --config config.yaml --template custom_template.html
```

## 🔧 Configuration Commands

### ✅ Config Validate

Validate configuration files.

```bash
ml-eval config validate [OPTIONS] FILE
```

**Options:**
```bash
--schema SCHEMA           Use custom schema file
--strict                  Strict validation mode
--fix                     Auto-fix validation issues
--output FILE             Output validation results
```

**Examples:**
```bash
# Validate configuration
ml-eval config validate config.yaml

# Validate with custom schema
ml-eval config validate config.yaml --schema custom_schema.json

# Auto-fix issues
ml-eval config validate config.yaml --fix
```

### 🧪 Config Test

Test configuration with sample data.

```bash
ml-eval config test [OPTIONS] FILE
```

**Options:**
```bash
--sample-data             Use sample data for testing
--data-file FILE          Use specific data file
--dry-run                 Show what would be tested
--timeout SECONDS         Set test timeout
```

**Examples:**
```bash
# Test with sample data
ml-eval config test config.yaml --sample-data

# Test with specific data
ml-eval config test config.yaml --data-file test_data.csv

# Dry run test
ml-eval config test config.yaml --dry-run
```

### 📋 Config Template

Generate configuration templates.

```bash
ml-eval config template [OPTIONS] TYPE
```

**Options:**
```bash
--output FILE             Output file path
--industry TYPE           Industry-specific template
--customize               Interactive customization
--include-examples        Include example configurations
```

**Examples:**
```bash
# Generate predictive maintenance template
ml-eval config template predictive_maintenance --output my_config.yaml

# Generate industry-specific template
ml-eval config template manufacturing --output manufacturing_config.yaml

# Interactive customization
ml-eval config template aviation --customize
```

## Core Commands

### Run

Run complete evaluation pipeline.

```bash
ml-eval run CONFIG [OPTIONS]
```

**Options:**
```bash
--output FILE             Output file for results (default: stdout)
```

**Examples:**
```bash
# Run complete evaluation
ml-eval run config.yaml --output results.json

# Run with existing example
ml-eval run examples/industries/manufacturing/predictive-maintenance.yaml --output manufacturing-results.json
```

### Validate

Validate configuration file.

```bash
ml-eval validate CONFIG
```

**Examples:**
```bash
# Validate configuration
ml-eval validate config.yaml

# Validate example configuration
ml-eval validate examples/industries/aviation/aircraft-landing.yaml
```

### List Components

List configured components.

```bash
ml-eval list-collectors CONFIG
ml-eval list-evaluators CONFIG
ml-eval list-reports CONFIG
```

**Examples:**
```bash
# List collectors in configuration
ml-eval list-collectors config.yaml

# List evaluators in aviation example
ml-eval list-evaluators examples/industries/aviation/aircraft-landing.yaml

# List reports in manufacturing example
ml-eval list-reports examples/industries/manufacturing/predictive-maintenance.yaml
```

### Health Check

Perform health check on configured components.

```bash
ml-eval health CONFIG [OPTIONS]
```

**Options:**
```bash
--output FILE             Output file for health check results (default: stdout)
```

**Examples:**
```bash
# Run health check
ml-eval health config.yaml

# Save health check results
ml-eval health config.yaml --output health-report.json
```

### Create Configuration

Create a new configuration file.

```bash
ml-eval create-config [OPTIONS]
```

**Options:**
```bash
--output FILE             Output file path (required)
--system-name NAME        System name (required)
--system-type TYPE        System type (single_model, workflow, ensemble)
--criticality LEVEL       Criticality level (operational, business_critical, safety_critical)
--industry TYPE           Industry type
```

**Examples:**
```bash
# Create basic configuration
ml-eval create-config --output my-system.yaml --system-name "My ML System"

# Create business-critical manufacturing system
ml-eval create-config --output manufacturing-system.yaml --system-name "Production Line QC" --industry manufacturing --criticality business_critical

# Create safety-critical aviation system
ml-eval create-config --output aviation-system.yaml --system-name "Flight Control" --industry aviation --criticality safety_critical
```

## Data Commands

### Data Sources

Manage data sources.

```bash
ml-eval data sources [COMMAND] [OPTIONS]
```

**Subcommands:**
```bash
list                     List configured data sources
test                     Test data source connections
validate                 Validate data source configuration
```

**Examples:**
```bash
# List data sources
ml-eval data sources list --config config.yaml

# Test connections
ml-eval data sources test --config config.yaml

# Validate configuration
ml-eval data sources validate --config config.yaml
```

### Data Collectors

Manage data collectors.

```bash
ml-eval data collectors [COMMAND] [OPTIONS]
```

**Subcommands:**
```bash
list                     List configured collectors
run                      Run specific collector
status                   Show collector status
logs                     Show collector logs
```

**Examples:**
```bash
# List collectors
ml-eval data collectors list --config config.yaml

# Run specific collector
ml-eval data collectors run quality_collector --config config.yaml

# Show status
ml-eval data collectors status --config config.yaml
```

## Evaluation Commands

### Evaluators

Manage evaluators.

```bash
ml-eval evaluators [COMMAND] [OPTIONS]
```

**Subcommands:**
```bash
list                     List configured evaluators
run                      Run specific evaluator
status                   Show evaluator status
results                  Show evaluator results
```

**Examples:**
```bash
# List evaluators
ml-eval evaluators list --config config.yaml

# Run specific evaluator
ml-eval evaluators run performance --config config.yaml

# Show results
ml-eval evaluators results --config config.yaml
```

### Reports

Manage reports.

```bash
ml-eval reports [COMMAND] [OPTIONS]
```

**Subcommands:**
```bash
list                     List configured reports
generate                 Generate specific report
status                   Show report generation status
schedule                 Manage report scheduling
```

**Examples:**
```bash
# List reports
ml-eval reports list --config config.yaml

# Generate specific report
ml-eval reports generate business --config config.yaml

# Show status
ml-eval reports status --config config.yaml
```

## Data Pipeline Commands

### Collect

Collect data using configured collectors.

```bash
ml-eval collect CONFIG [OPTIONS]
```

**Options:**
```bash
--output FILE             Output file for collected data (default: stdout)
```

**Examples:**
```bash
# Collect data
ml-eval collect config.yaml --output data.json

# Collect from manufacturing example
ml-eval collect examples/industries/manufacturing/predictive-maintenance.yaml --output manufacturing-data.json
```

### Evaluate

Evaluate metrics using configured evaluators.

```bash
ml-eval evaluate CONFIG [OPTIONS]
```

**Options:**
```bash
--data FILE              Input data file (optional)
--output FILE            Output file for results (default: stdout)
```

**Examples:**
```bash
# Evaluate metrics
ml-eval evaluate config.yaml --output evaluation.json

# Evaluate with specific data
ml-eval evaluate config.yaml --data collected-data.json --output results.json
```

### Report

Generate reports using configured report generators.

```bash
ml-eval report CONFIG [OPTIONS]
```

**Options:**
```bash
--results FILE           Input results file (optional)
--output FILE            Output file for reports (default: stdout)
```

**Examples:**
```bash
# Generate reports
ml-eval report config.yaml --output reports.json

# Generate reports from specific results
ml-eval report config.yaml --results evaluation-results.json --output final-reports.json
```

## Utility Commands

### Help

Show help information.

```bash
ml-eval --help
ml-eval [COMMAND] --help
```

**Examples:**
```bash
# Show general help
ml-eval --help

# Show command help
ml-eval run --help

# Show create-config help
ml-eval create-config --help
```

## Environment Variables

The CLI supports the following environment variables:

```bash
ML_EVAL_CONFIG_FILE      Default configuration file path
ML_EVAL_LOG_LEVEL        Default log level
ML_EVAL_OUTPUT_DIR       Default output directory
ML_EVAL_TEMPLATE_DIR     Template directory path
ML_EVAL_CACHE_DIR        Cache directory path
ML_EVAL_DEBUG            Enable debug mode
```

## Exit Codes

The CLI uses the following exit codes:

- `0`: Success
- `1`: General error
- `2`: Configuration error
- `3`: Validation error
- `4`: Connection error
- `5`: Timeout error
- `6`: Permission error

## Examples

### Complete Workflow

```bash
# 1. Create configuration
ml-eval create-config --output config.yaml --system-name "My System" --industry manufacturing

# 2. Validate configuration
ml-eval validate config.yaml

# 3. Run health check
ml-eval health config.yaml

# 4. Collect data
ml-eval collect config.yaml --output data.json

# 5. Evaluate metrics
ml-eval evaluate config.yaml --data data.json --output results.json

# 6. Generate reports
ml-eval report config.yaml --results results.json --output reports.json

# 7. Run complete pipeline
ml-eval run config.yaml --output complete-results.json
```

### Using Example Configurations

```bash
# Copy and use existing examples
cp examples/industries/manufacturing/predictive-maintenance.yaml my-config.yaml
ml-eval validate my-config.yaml
ml-eval run my-config.yaml --output manufacturing-results.json

# Use aviation example
ml-eval run examples/industries/aviation/aircraft-landing.yaml --output aviation-results.json

# Use cybersecurity example
ml-eval run examples/industries/cybersecurity/security-operations.yaml --output security-results.json
```

### Batch Processing

```bash
# Run multiple evaluations
for config in examples/industries/*/*.yaml; do
    output_name=$(basename "$config" .yaml)
    ml-eval run "$config" --output "./results/${output_name}-results.json"
done
```

For more detailed information about specific commands, use the `--help` option:

```bash
ml-eval [COMMAND] --help
``` 