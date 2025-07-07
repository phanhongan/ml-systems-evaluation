# API Reference

> **Note**: This API is currently in the design phase and has not been implemented yet.

This document provides the design specification for the REST API and Python SDK interfaces for the ML Systems Evaluation Framework.

## API Overview

The framework provides both REST API and Python SDK interfaces for programmatic access to all functionality.

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication
All API requests require authentication using API keys or OAuth2 tokens.

```bash
# Using API Key
Authorization: Bearer YOUR_API_KEY

# Using OAuth2 Token
Authorization: Bearer YOUR_OAUTH_TOKEN
```

## REST API Endpoints

### Configuration Management

#### Get Configuration
```http
GET /config/{config_id}
```

**Parameters:**
- `config_id` (string): Configuration identifier

**Response:**
```json
{
  "id": "config_123",
  "name": "Production Quality Control",
  "type": "manufacturing",
  "criticality": "business-critical",
  "data_sources": [...],
  "collectors": [...],
  "evaluators": [...],
  "reports": [...],
  "slo": {...},
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### Create Configuration
```http
POST /config
```

**Request Body:**
```json
{
  "name": "New Configuration",
  "type": "manufacturing",
  "criticality": "business-critical",
  "data_sources": [...],
  "collectors": [...],
  "evaluators": [...],
  "reports": [...],
  "slo": {...}
}
```

#### Update Configuration
```http
PUT /config/{config_id}
```

#### Delete Configuration
```http
DELETE /config/{config_id}
```

#### Validate Configuration
```http
POST /config/{config_id}/validate
```

**Response:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": []
}
```

### Template Management

#### List Templates
```http
GET /templates
```

**Query Parameters:**
- `industry` (string): Filter by industry
- `type` (string): Filter by template type
- `limit` (integer): Number of results to return
- `offset` (integer): Number of results to skip

**Response:**
```json
{
  "templates": [
    {
      "id": "manufacturing-predictive_maintenance",
      "name": "Manufacturing Predictive Maintenance",
      "industry": "manufacturing",
      "description": "Manufacturing predictive maintenance template",
      "version": "1.0.0"
    }
  ],
  "total": 10,
  "limit": 20,
  "offset": 0
}
```

#### Get Template
```http
GET /templates/{template_id}
```

#### Use Template
```http
POST /templates/{template_id}/use
```

**Request Body:**
```json
{
  "customizations": {
    "system.name": "My System",
    "data_sources.0.connection": "postgresql://user:pass@localhost/db"
  }
}
```

### Data Collection

#### Start Collection
```http
POST /collect
```

**Request Body:**
```json
{
  "config_id": "config_123",
  "collector_name": "quality_collector",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "batch_size": 10000
}
```

#### Get Collection Status
```http
GET /collect/{collection_id}
```

**Response:**
```json
{
  "id": "collection_123",
  "status": "running",
  "progress": 0.75,
  "records_collected": 75000,
  "started_at": "2024-01-01T00:00:00Z",
  "estimated_completion": "2024-01-01T02:00:00Z"
}
```

#### List Collections
```http
GET /collect
```

**Query Parameters:**
- `config_id` (string): Filter by configuration
- `status` (string): Filter by status
- `start_date` (string): Filter by start date
- `end_date` (string): Filter by end date

### Evaluation

#### Start Evaluation
```http
POST /evaluate
```

**Request Body:**
```json
{
  "config_id": "config_123",
  "evaluator_name": "performance_evaluator",
  "data_collection_id": "collection_123",
  "options": {
    "parallel": true,
    "timeout": 3600
  }
}
```

#### Get Evaluation Status
```http
GET /evaluate/{evaluation_id}
```

**Response:**
```json
{
  "id": "evaluation_123",
  "status": "completed",
  "progress": 1.0,
  "results": {
    "accuracy": 0.95,
    "precision": 0.92,
    "recall": 0.88
  },
  "started_at": "2024-01-01T00:00:00Z",
  "completed_at": "2024-01-01T01:00:00Z"
}
```

#### Get Evaluation Results
```http
GET /evaluate/{evaluation_id}/results
```

**Response:**
```json
{
  "evaluation_id": "evaluation_123",
  "metrics": {
    "accuracy": {
      "value": 0.95,
      "threshold": 0.90,
      "status": "pass"
    },
    "precision": {
      "value": 0.92,
      "threshold": 0.85,
      "status": "pass"
    }
  },
  "drift_analysis": {
    "detected": false,
    "score": 0.05
  },
  "recommendations": [
    "Consider retraining model due to slight performance degradation"
  ]
}
```

#### List Evaluations
```http
GET /evaluate
```

### Reporting

#### Generate Report
```http
POST /reports
```

**Request Body:**
```json
{
  "config_id": "config_123",
  "evaluation_id": "evaluation_123",
  "report_type": "business",
  "format": "html",
  "options": {
    "include_charts": true,
    "include_recommendations": true
  }
}
```

#### Get Report Status
```http
GET /reports/{report_id}
```

**Response:**
```json
{
  "id": "report_123",
  "status": "completed",
  "download_url": "https://api.ml-eval.com/reports/report_123/download",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Download Report
```http
GET /reports/{report_id}/download
```

#### List Reports
```http
GET /reports
```

### Monitoring

#### Get System Status
```http
GET /monitor/status
```

**Response:**
```json
{
  "status": "healthy",
  "components": {
    "database": "healthy",
    "evaluation_engine": "healthy",
    "reporting_engine": "healthy"
  },
  "metrics": {
    "cpu_usage": 0.25,
    "memory_usage": 0.40,
    "disk_usage": 0.60
  }
}
```

#### Get Alerts
```http
GET /monitor/alerts
```

**Query Parameters:**
- `status` (string): Filter by alert status
- `severity` (string): Filter by severity level
- `start_date` (string): Filter by start date
- `end_date` (string): Filter by end date

**Response:**
```json
{
  "alerts": [
    {
      "id": "alert_123",
      "type": "threshold_breach",
      "severity": "warning",
      "message": "Accuracy below threshold",
      "created_at": "2024-01-01T00:00:00Z",
      "acknowledged": false
    }
  ]
}
```

#### Acknowledge Alert
```http
POST /monitor/alerts/{alert_id}/acknowledge
```

#### Resolve Alert
```http
POST /monitor/alerts/{alert_id}/resolve
```

### Data Sources

#### Test Connection
```http
POST /data-sources/test
```

**Request Body:**
```json
{
  "type": "database",
  "connection": "postgresql://user:pass@localhost/db",
  "options": {
    "timeout": 30,
    "ssl_mode": "require"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Connection successful",
  "tables": ["quality_measurements", "defect_reports"]
}
```

#### Get Data Source Schema
```http
GET /data-sources/{source_id}/schema
```

## Python SDK

### Installation

```bash
pip install ml-eval-sdk
```

### Basic Usage

```python
from ml_eval import MLEvalClient

# Initialize client
client = MLEvalClient(api_key="your_api_key")

# Create configuration
config = client.create_configuration({
    "name": "My System",
    "type": "manufacturing",
    "criticality": "business-critical",
    "data_sources": [...],
    "collectors": [...],
    "evaluators": [...],
    "reports": [...],
    "slo": {...}
})

# Start data collection
collection = client.start_collection(
    config_id=config["id"],
    collector_name="quality_collector"
)

# Wait for collection to complete
client.wait_for_collection(collection["id"])

# Start evaluation
evaluation = client.start_evaluation(
    config_id=config["id"],
    evaluation_id=collection["id"]
)

# Wait for evaluation to complete
client.wait_for_evaluation(evaluation["id"])

# Generate report
report = client.generate_report(
    config_id=config["id"],
    evaluation_id=evaluation["id"],
    report_type="business"
)

# Download report
client.download_report(report["id"], "report.html")
```

### Configuration Management

```python
# List configurations
configs = client.list_configurations()

# Get configuration
config = client.get_configuration("config_123")

# Update configuration
updated_config = client.update_configuration("config_123", {
    "name": "Updated Name"
})

# Validate configuration
validation = client.validate_configuration("config_123")
```

### Template Management

```python
# List templates
templates = client.list_templates(industry="manufacturing")

# Use template
config = client.use_template("manufacturing-predictive_maintenance", {
    "system.name": "My System",
    "data_sources.0.connection": "postgresql://user:pass@localhost/db"
})
```

### Data Collection

```python
# Start collection
collection = client.start_collection(
    config_id="config_123",
    collector_name="quality_collector",
    start_date="2024-01-01",
    end_date="2024-01-31"
)

# Monitor collection progress
while True:
    status = client.get_collection_status(collection["id"])
    if status["status"] == "completed":
        break
    time.sleep(10)
```

### Evaluation

```python
# Start evaluation
evaluation = client.start_evaluation(
    config_id="config_123",
    evaluator_name="performance_evaluator"
)

# Get results
results = client.get_evaluation_results(evaluation["id"])

# Check if metrics meet thresholds
for metric, data in results["metrics"].items():
    if data["status"] == "fail":
        print(f"Metric {metric} failed: {data['value']} < {data['threshold']}")
```

### Reporting

```python
# Generate report
report = client.generate_report(
    config_id="config_123",
    evaluation_id="evaluation_123",
    report_type="business",
    format="html"
)

# Download report
client.download_report(report["id"], "business_report.html")
```

### Monitoring

```python
# Get system status
status = client.get_system_status()

# Get alerts
alerts = client.get_alerts(status="active")

# Acknowledge alert
client.acknowledge_alert("alert_123")
```

## Webhook Integration

### Configure Webhooks

```http
POST /webhooks
```

**Request Body:**
```json
{
  "url": "https://your-app.com/webhook",
  "events": ["evaluation.completed", "alert.created"],
  "secret": "your_webhook_secret"
}
```

### Webhook Events

#### Evaluation Completed
```json
{
  "event": "evaluation.completed",
  "timestamp": "2024-01-01T00:00:00Z",
  "data": {
    "evaluation_id": "evaluation_123",
    "config_id": "config_123",
    "status": "completed",
    "results": {...}
  }
}
```

#### Alert Created
```json
{
  "event": "alert.created",
  "timestamp": "2024-01-01T00:00:00Z",
  "data": {
    "alert_id": "alert_123",
    "type": "threshold_breach",
    "severity": "warning",
    "message": "Accuracy below threshold"
  }
}
```

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid configuration format",
    "details": {
      "field": "data_sources",
      "issue": "Missing required field 'connection'"
    }
  }
}
```

### Common Error Codes

- `AUTHENTICATION_ERROR`: Invalid API key or token
- `AUTHORIZATION_ERROR`: Insufficient permissions
- `VALIDATION_ERROR`: Invalid request data
- `NOT_FOUND`: Resource not found
- `CONFLICT`: Resource conflict
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_ERROR`: Server error

### Rate Limiting

- **Standard Plan**: 1000 requests per hour
- **Professional Plan**: 10000 requests per hour
- **Enterprise Plan**: Custom limits

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## SDK Reference

### MLEvalClient

#### Constructor
```python
MLEvalClient(api_key=None, base_url=None, timeout=30)
```

#### Methods

##### Configuration
- `create_configuration(config_data)`
- `get_configuration(config_id)`
- `update_configuration(config_id, updates)`
- `delete_configuration(config_id)`
- `list_configurations(**filters)`
- `validate_configuration(config_id)`

##### Templates
- `list_templates(**filters)`
- `get_template(template_id)`
- `use_template(template_id, customizations=None)`

##### Data Collection
- `start_collection(config_id, collector_name, **options)`
- `get_collection_status(collection_id)`
- `list_collections(**filters)`
- `wait_for_collection(collection_id, timeout=None)`

##### Evaluation
- `start_evaluation(config_id, **options)`
- `get_evaluation_status(evaluation_id)`
- `get_evaluation_results(evaluation_id)`
- `list_evaluations(**filters)`
- `wait_for_evaluation(evaluation_id, timeout=None)`

##### Reporting
- `generate_report(config_id, evaluation_id, report_type, **options)`
- `get_report_status(report_id)`
- `download_report(report_id, file_path)`
- `list_reports(**filters)`

##### Monitoring
- `get_system_status()`
- `get_alerts(**filters)`
- `acknowledge_alert(alert_id)`
- `resolve_alert(alert_id)`

##### Data Sources
- `test_connection(connection_data)`
- `get_data_source_schema(source_id)`

This API reference provides comprehensive access to all framework functionality through both REST API and Python SDK interfaces, enabling seamless integration with existing systems and workflows. 