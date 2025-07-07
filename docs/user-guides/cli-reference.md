# CLI Reference

This document provides a complete reference for all command-line interface (CLI) commands available in the ML Systems Evaluation Framework.

## Command Overview

```bash
ml-eval [COMMAND] [OPTIONS]
```

## Global Options

```bash
--config, -c FILE          Configuration file path
--verbose, -v              Enable verbose output
--quiet, -q                Suppress output
--log-level LEVEL          Set log level (DEBUG, INFO, WARNING, ERROR)
--output-dir DIR           Output directory for reports
--format FORMAT            Output format (json, yaml, html, pdf)
```

## Main Commands

### Evaluate Command

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

### Collect Command

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

### Report Command

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

## Configuration Commands

### Config Validate

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

### Config Test

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

### Config Template

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
# Generate basic template
ml-eval config template basic --output my_config.yaml

# Generate industry-specific template
ml-eval config template manufacturing --output manufacturing_config.yaml

# Interactive customization
ml-eval config template aviation --customize
```

## Template Commands

### Templates List

List available templates.

```bash
ml-eval templates list [OPTIONS]
```

**Options:**
```bash
--industry TYPE           Filter by industry
--format FORMAT           Output format (table, json, yaml)
--details                 Show detailed information
```

**Examples:**
```bash
# List all templates
ml-eval templates list

# List manufacturing templates
ml-eval templates list --industry manufacturing

# Show detailed information
ml-eval templates list --details
```

### Templates Use

Use a specific template.

```bash
ml-eval templates use [OPTIONS] TEMPLATE
```

**Options:**
```bash
--output FILE             Output file path
--customize               Interactive customization
--overwrite               Overwrite existing file
--validate                Validate after creation
```

**Examples:**
```bash
# Use manufacturing template
ml-eval templates use manufacturing-basic --output config.yaml

# Use with customization
ml-eval templates use aviation-safety --customize

# Use and validate
ml-eval templates use energy-grid --validate
```

### Templates Customize

Customize an existing template.

```bash
ml-eval templates customize [OPTIONS] TEMPLATE
```

**Options:**
```bash
--output FILE             Output file path
--interactive             Interactive mode
--preset PRESET           Use preset customization
--validate                Validate after customization
```

**Examples:**
```bash
# Customize template
ml-eval templates customize manufacturing-basic --output my_config.yaml

# Interactive customization
ml-eval templates customize aviation-safety --interactive

# Use preset customization
ml-eval templates customize energy-grid --preset production
```

### Templates Create

Create a new template.

```bash
ml-eval templates create [OPTIONS] NAME
```

**Options:**
```bash
--base TEMPLATE           Base template to extend
--industry TYPE           Industry classification
--description TEXT        Template description
--output FILE             Output file path
```

**Examples:**
```bash
# Create new template
ml-eval templates create my-industry --output my_template.yaml

# Create based on existing template
ml-eval templates create my-manufacturing --base manufacturing-basic

# Create with description
ml-eval templates create my-aviation --industry aviation --description "Custom aviation template"
```

### Templates Edit

Edit an existing template.

```bash
ml-eval templates edit [OPTIONS] TEMPLATE
```

**Options:**
```bash
--editor EDITOR           Use specific editor
--backup                 Create backup before editing
--validate               Validate after editing
```

**Examples:**
```bash
# Edit template
ml-eval templates edit manufacturing-basic

# Edit with specific editor
ml-eval templates edit aviation-safety --editor vim

# Edit with backup
ml-eval templates edit energy-grid --backup
```

### Templates Validate

Validate template files.

```bash
ml-eval templates validate [OPTIONS] TEMPLATE
```

**Options:**
```bash
--strict                 Strict validation mode
--fix                    Auto-fix validation issues
--output FILE            Output validation results
```

**Examples:**
```bash
# Validate template
ml-eval templates validate manufacturing-basic

# Strict validation
ml-eval templates validate aviation-safety --strict

# Auto-fix issues
ml-eval templates validate energy-grid --fix
```

### Templates Test

Test template with sample data.

```bash
ml-eval templates test [OPTIONS] TEMPLATE
```

**Options:**
```bash
--sample-data            Use sample data
--data-file FILE         Use specific data file
--dry-run               Show what would be tested
--timeout SECONDS       Set test timeout
```

**Examples:**
```bash
# Test with sample data
ml-eval templates test manufacturing-basic --sample-data

# Test with specific data
ml-eval templates test aviation-safety --data-file test_data.csv

# Dry run test
ml-eval templates test energy-grid --dry-run
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

## Monitoring Commands

### Monitor

Start monitoring mode.

```bash
ml-eval monitor [OPTIONS]
```

**Options:**
```bash
--config, -c FILE         Configuration file path
--interval SECONDS        Monitoring interval
--duration SECONDS        Monitoring duration
--alerts                 Enable alerts
--dashboard              Start web dashboard
--port PORT              Dashboard port
```

**Examples:**
```bash
# Start monitoring
ml-eval monitor --config config.yaml

# Monitor with alerts
ml-eval monitor --config config.yaml --alerts

# Start with dashboard
ml-eval monitor --config config.yaml --dashboard --port 8080
```

### Alerts

Manage alerts.

```bash
ml-eval alerts [COMMAND] [OPTIONS]
```

**Subcommands:**
```bash
list                     List active alerts
acknowledge              Acknowledge alert
resolve                  Resolve alert
history                  Show alert history
configure                Configure alert settings
```

**Examples:**
```bash
# List alerts
ml-eval alerts list --config config.yaml

# Acknowledge alert
ml-eval alerts acknowledge ALERT_ID

# Show history
ml-eval alerts history --config config.yaml
```

## Utility Commands

### Version

Show version information.

```bash
ml-eval version [OPTIONS]
```

**Options:**
```bash
--verbose                Show detailed version information
--json                   Output in JSON format
```

**Examples:**
```bash
# Show version
ml-eval version

# Detailed version info
ml-eval version --verbose
```

### Info

Show system information.

```bash
ml-eval info [OPTIONS]
```

**Options:**
```bash
--config FILE            Configuration file path
--detailed              Show detailed information
--json                  Output in JSON format
```

**Examples:**
```bash
# Show system info
ml-eval info

# Show with config
ml-eval info --config config.yaml

# Detailed info
ml-eval info --detailed
```

### Help

Show help information.

```bash
ml-eval help [COMMAND]
```

**Examples:**
```bash
# Show general help
ml-eval help

# Show command help
ml-eval help evaluate

# Show subcommand help
ml-eval help templates list
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
# 1. Create configuration from template
ml-eval templates use manufacturing-basic --output config.yaml

# 2. Customize configuration
ml-eval config template manufacturing --customize

# 3. Validate configuration
ml-eval config validate config.yaml

# 4. Test configuration
ml-eval config test config.yaml --sample-data

# 5. Run evaluation
ml-eval evaluate --config config.yaml

# 6. Generate reports
ml-eval report --config config.yaml --format html

# 7. Start monitoring
ml-eval monitor --config config.yaml --dashboard
```

### Batch Processing

```bash
# Run multiple evaluations
for config in configs/*.yaml; do
    ml-eval evaluate --config "$config" --output-dir "./results/$(basename "$config" .yaml)"
done
```

### Automated Monitoring

```bash
# Start continuous monitoring with alerts
ml-eval monitor --config config.yaml --alerts --interval 300
```

For more detailed information about specific commands, use the `--help` option:

```bash
ml-eval [COMMAND] --help
``` 