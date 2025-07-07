# ⚙️ Configuration Guide

This guide provides detailed information about all configuration options available in the ML Systems Evaluation Framework.

## 📁 Configuration File Structure

The framework uses YAML configuration files with the following structure:

```yaml
system:
  name: "Your System Name"
  type: "industry_type"
  criticality: "criticality_level"

data_sources:
  - name: "data_source_name"
    type: "source_type"
    # source-specific configuration

collectors:
  - name: "collector_name"
    type: "collector_type"
    # collector-specific configuration

evaluators:
  - name: "evaluator_name"
    type: "evaluator_type"
    # evaluator-specific configuration

reports:
  - name: "report_name"
    type: "report_type"
    # report-specific configuration

slo:
  # Service Level Objectives
```

## 🏗️ System Configuration

### 🔧 Basic System Settings

```yaml
system:
  name: "Production Quality Control System"
  type: "manufacturing"  # manufacturing, aviation, energy, etc.
  criticality: "business-critical"  # business-critical, safety-critical
  description: "Optional system description"
  version: "1.0.0"
  environment: "production"  # production, staging, development
```

### 🏭 System Types

- **🏭 manufacturing**: Manufacturing and quality control systems
- **✈️ aviation**: Aviation and aerospace systems
- **⚡ energy**: Energy and utility systems
- **🏥 healthcare**: Healthcare and medical systems
- **🚗 automotive**: Automotive and transportation systems
- **🔧 custom**: Custom system type

### 🚨 Criticality Levels

- **💰 business-critical**: Systems where failures result in financial loss
- **🛡️ safety-critical**: Systems where failures can cause harm to people or environment

## 📊 Data Sources

### 🗄️ Database Sources

```yaml
data_sources:
  - name: "quality_database"
    type: "database"
    connection: "postgresql://user:pass@localhost/db_name"
    tables: ["quality_measurements", "defect_reports"]
    schema: "public"
    query_timeout: 300  # seconds
    connection_pool_size: 10
    ssl_mode: "require"
```

#### 🗄️ Supported Database Types

- **🐘 postgresql**: PostgreSQL database
- **🐬 mysql**: MySQL database
- **📱 sqlite**: SQLite database
- **🔷 oracle**: Oracle database
- **🪟 sqlserver**: Microsoft SQL Server

### 🌐 API Sources

```yaml
data_sources:
  - name: "api_endpoint"
    type: "api"
    url: "https://api.example.com/metrics"
    method: "GET"
    headers:
      Authorization: "Bearer your_token"
      Content-Type: "application/json"
    timeout: 30  # seconds
    retry_attempts: 3
    rate_limit: 100  # requests per minute
```

### 📁 File Sources

```yaml
data_sources:
  - name: "csv_data"
    type: "file"
    path: "/path/to/data.csv"
    format: "csv"
    encoding: "utf-8"
    delimiter: ","
    has_header: true
    compression: "gzip"  # optional
```

#### 📄 Supported File Formats

- **📊 csv**: Comma-separated values
- **📋 json**: JSON files
- **📦 parquet**: Apache Parquet files
- **📊 excel**: Microsoft Excel files
- **📄 xml**: XML files

### 🌊 Streaming Sources

```yaml
data_sources:
  - name: "kafka_stream"
    type: "stream"
    broker: "localhost:9092"
    topic: "metrics_topic"
    group_id: "ml_eval_consumer"
    auto_offset_reset: "latest"
    max_poll_records: 1000
    session_timeout_ms: 30000
```

## 📊 Collectors

### 📁 Offline Collectors

```yaml
collectors:
  - name: "batch_collector"
    type: "offline"
    data_source: "quality_database"
    metrics: ["accuracy", "precision", "recall", "f1_score"]
    schedule: "0 */6 * * *"  # Every 6 hours
    batch_size: 10000
    retention_days: 90
    filters:
      date_range:
        start: "2024-01-01"
        end: "2024-12-31"
      conditions:
        - field: "status"
          operator: "equals"
          value: "completed"
```

### ⚡ Online Collectors

```yaml
collectors:
  - name: "realtime_collector"
    type: "online"
    data_source: "api_endpoint"
    metrics: ["latency", "throughput", "error_rate"]
    interval: 60  # seconds
    buffer_size: 1000
    timeout: 30
    retry_on_failure: true
    max_retries: 3
```

### 🌊 Environmental Collectors

```yaml
collectors:
  - name: "system_metrics"
    type: "environmental"
    metrics: ["cpu_usage", "memory_usage", "disk_usage"]
    interval: 300  # 5 minutes
    include_process_metrics: true
    include_network_metrics: true
    include_disk_metrics: true
```

## 🔍 Evaluators

### 📊 Performance Evaluator

```yaml
evaluators:
  - name: "performance_evaluator"
    type: "performance"
    thresholds:
      accuracy: 0.95
      precision: 0.90
      recall: 0.85
      f1_score: 0.88
      latency_p95: 100  # milliseconds
      throughput: 1000  # requests per second
    comparison_method: "absolute"  # absolute, relative, percentile
    baseline_period: "last_30_days"
    alert_on_threshold_breach: true
    alert_channels: ["email", "slack"]
```

### Drift Evaluator

```yaml
evaluators:
  - name: "drift_evaluator"
    type: "drift"
    detection_method: "statistical"  # statistical, ml_based, domain_specific
    features: ["feature1", "feature2", "feature3"]
    sensitivity: 0.05
    baseline_period: "last_30_days"
    comparison_window: "last_7_days"
    statistical_tests: ["ks_test", "chi_square", "ad_test"]
    drift_threshold: 0.1
    alert_on_drift: true
```

### Safety Evaluator

```yaml
evaluators:
  - name: "safety_evaluator"
    type: "safety"
    thresholds:
      safety_margin: 0.99
      failure_probability: 0.001
      response_time_p99: 50  # milliseconds
      error_budget: 0.001
    safety_criteria:
      - name: "no_false_negatives"
        critical: true
        threshold: 0.0
      - name: "max_response_time"
        critical: true
        threshold: 100
    compliance_standards: ["DO-178C", "ISO-26262"]
```

### Compliance Evaluator

```yaml
evaluators:
  - name: "compliance_evaluator"
    type: "compliance"
    standards: ["GDPR", "SOX", "HIPAA"]
    requirements:
      - name: "data_retention"
        period_days: 2555  # 7 years
        encrypted: true
      - name: "audit_logging"
        enabled: true
        retention_days: 365
    compliance_checks:
      - name: "data_encryption"
        required: true
      - name: "access_control"
        required: true
      - name: "audit_trail"
        required: true
```

### Reliability Evaluator

```yaml
evaluators:
  - name: "reliability_evaluator"
    type: "reliability"
    failure_modes: ["hardware_failure", "software_failure", "network_failure"]
    reliability_metrics:
      - name: "mtbf"  # Mean Time Between Failures
        target: 8760  # hours (1 year)
      - name: "mttr"  # Mean Time To Repair
        target: 4  # hours
      - name: "availability"
        target: 0.9999
    redundancy_level: 2
    backup_systems: ["backup_server", "failover_system"]
```

## Reports

### Business Report

```yaml
reports:
  - name: "business_report"
    type: "business"
    format: "html"  # html, pdf, json, csv
    output_path: "./reports/"
    schedule: "0 9 * * 1"  # Every Monday at 9 AM
    recipients: ["management@company.com"]
    include_charts: true
    include_recommendations: true
    executive_summary: true
    kpi_highlights: true
```

### Compliance Report

```yaml
reports:
  - name: "compliance_report"
    type: "compliance"
    format: "pdf"
    output_path: "./compliance_reports/"
    schedule: "0 0 1 * *"  # Monthly on 1st
    standards: ["GDPR", "SOX", "HIPAA"]
    include_evidence: true
    include_remediation_plan: true
    audit_trail: true
```

### Safety Report

```yaml
reports:
  - name: "safety_report"
    type: "safety"
    format: "html"
    output_path: "./safety_reports/"
    schedule: "0 8 * * *"  # Daily at 8 AM
    recipients: ["safety_team@company.com"]
    include_risk_assessment: true
    include_mitigation_plans: true
    include_incident_history: true
    critical_alerts: true
```

### Reliability Report

```yaml
reports:
  - name: "reliability_report"
    type: "reliability"
    format: "html"
    output_path: "./reliability_reports/"
    schedule: "0 10 * * 1"  # Every Monday at 10 AM
    include_failure_analysis: true
    include_maintenance_schedule: true
    include_cost_analysis: true
    include_trends: true
```

## Service Level Objectives (SLOs)

For comprehensive SLO configuration guidance, including detailed examples and industry-specific configurations, see the [SLO Configuration Guide](./slo-configuration.md).

## Advanced Configuration

### Environment Variables

```yaml
# Use environment variables for sensitive data
data_sources:
  - name: "secure_database"
    type: "database"
    connection: "${DATABASE_URL}"
    username: "${DB_USERNAME}"
    password: "${DB_PASSWORD}"
```

### Conditional Configuration

```yaml
# Different configurations for different environments
system:
  name: "Quality Control System"
  type: "manufacturing"
  criticality: "business-critical"
  
# Environment-specific overrides
environments:
  production:
    data_sources:
      - name: "prod_database"
        connection: "postgresql://prod_user:prod_pass@prod_host/prod_db"
    
  staging:
    data_sources:
      - name: "staging_database"
        connection: "postgresql://staging_user:staging_pass@staging_host/staging_db"
    
  development:
    data_sources:
      - name: "dev_database"
        connection: "sqlite:///dev.db"
```

### Validation Rules

```yaml
# Configuration validation
validation:
  required_fields: ["system.name", "system.type", "system.criticality"]
  data_source_validation: true
  evaluator_validation: true
  report_validation: true
  
  # Custom validation rules
  custom_rules:
    - name: "safety_critical_requires_safety_evaluator"
      condition: "system.criticality == 'safety-critical'"
      requirement: "evaluators contains safety_evaluator"
      
    - name: "aviation_requires_compliance"
      condition: "system.type == 'aviation'"
      requirement: "evaluators contains compliance_evaluator"
```

## Configuration Best Practices

### 1. Security
- Use environment variables for sensitive data
- Encrypt database connections
- Use least-privilege access
- Regularly rotate credentials

### 2. Performance
- Set appropriate timeouts
- Use connection pooling
- Configure batch sizes appropriately
- Monitor resource usage

### 3. Reliability
- Use multiple data sources for redundancy
- Configure retry mechanisms
- Set up alerting for failures
- Monitor system health

### 4. Maintainability
- Use descriptive names
- Document custom configurations
- Version control your configs
- Test configurations before deployment

### 5. Compliance
- Include all required fields
- Validate against standards
- Maintain audit trails
- Regular compliance checks

## Configuration Validation

```bash
# Validate configuration file
ml-eval config validate config.yaml

# Test configuration with sample data
ml-eval config test config.yaml --sample-data

# Generate configuration template
ml-eval config template manufacturing --output my_config.yaml
```

## Troubleshooting Configuration Issues

### Common Issues

1. **Invalid YAML Syntax**
   - Use a YAML validator
   - Check indentation
   - Verify quotes and special characters

2. **Missing Required Fields**
   - Check validation errors
   - Review configuration schema
   - Use configuration templates

3. **Connection Issues**
   - Verify connection strings
   - Check network connectivity
   - Validate credentials

4. **Performance Problems**
   - Adjust batch sizes
   - Increase timeouts
   - Optimize queries

For more detailed troubleshooting, see the [Troubleshooting Guide](troubleshooting.md). 