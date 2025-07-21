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

### Evaluation Management

#### Start Evaluation
```http
POST /evaluation
```

**Request Body:**
```json
{
  "config_id": "config_123",
  "evaluation_type": "full",
  "options": {
    "skip_collection": false,
    "sample_data": false
  }
}
```

#### Get Evaluation Status
```http
GET /evaluation/{evaluation_id}
```

#### Get Evaluation Results
```http
GET /evaluation/{evaluation_id}/results
```

#### Download Report
```http
GET /evaluation/{evaluation_id}/report
```

### Data Collection

#### Start Data Collection
```http
POST /collection
```

**Request Body:**
```json
{
  "config_id": "config_123",
  "collection_options": {
    "time_range": "last_24h",
    "sample_size": 1000
  }
}
```

#### Monitor Collection Progress
```http
GET /collection/{collection_id}/progress
```

#### Get Collection Results
```http
GET /collection/{collection_id}/results
```

### Monitoring & Alerts

#### Get Alerts
```http
GET /alerts
```

**Query Parameters:**
- `status`: active, resolved, acknowledged
- `severity`: critical, warning, info
- `time_range`: last_hour, last_day, last_week

#### Acknowledge Alert
```http
POST /alerts/{alert_id}/acknowledge
```

#### Get Metrics
```http
GET /metrics
```

**Query Parameters:**
- `metric_name`: accuracy, precision, recall, drift_score
- `time_range`: last_hour, last_day, last_week, last_month

## Python SDK

### Initialize Client
```python
from ml_eval.api import MLSystemsEvaluationClient

# Initialize with API key
client = MLSystemsEvaluationClient(
    base_url="http://localhost:8000/api/v1",
    api_key="your_api_key"
)

# Initialize with OAuth2 token
client = MLSystemsEvaluationClient(
    base_url="http://localhost:8000/api/v1",
    oauth_token="your_oauth_token"
)
```

### Configuration Operations
```python
# Create configuration
config = client.create_configuration({
    "name": "Production Quality Control",
    "type": "manufacturing",
    "criticality": "business-critical",
    "data_sources": [...],
    "collectors": [...],
    "evaluators": [...],
    "reports": [...],
    "slo": {...}
})

# Get configuration
config = client.get_configuration("config_123")

# Update configuration
updated_config = client.update_configuration("config_123", {
    "name": "Updated Quality Control"
})

# Validate configuration
validation = client.validate_configuration("config_123")
```

### Evaluation Operations
```python
# Start evaluation
evaluation = client.start_evaluation("config_123")

# Wait for completion
results = client.wait_for_evaluation(evaluation["id"])

# Get results
results = client.get_evaluation_results(evaluation["id"])

# Download report
report = client.download_report(evaluation["id"])
```

### Data Collection
```python
# Start collection
collection = client.start_collection("config_123")

# Monitor progress
progress = client.get_collection_progress(collection["id"])

# Get results
results = client.get_collection_results(collection["id"])
```

### Monitoring
```python
# Get metrics
metrics = client.get_metrics(
    metric_names=["accuracy", "precision", "recall"],
    time_range="last_24h"
)

# Check thresholds
threshold_check = client.check_metrics_thresholds(
    metrics=metrics,
    thresholds={"accuracy": 0.95, "precision": 0.90}
)

# Get alerts
alerts = client.get_alerts(status="active", severity="critical")

# Acknowledge alert
client.acknowledge_alert("alert_123")
```

## Error Handling

### HTTP Status Codes
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation errors
- `500 Internal Server Error`: Server error

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid configuration parameters",
    "details": {
      "field": "data_sources",
      "issue": "Missing required connection string"
    }
  }
}
```

## Rate Limiting

The API implements rate limiting to ensure fair usage:
- **Standard Plan**: 100 requests per minute
- **Professional Plan**: 1000 requests per minute
- **Enterprise Plan**: Custom limits

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## SDK Installation

```bash
# Install Python SDK
pip install ml-systems-evaluation-sdk

# Or with UV
uv add ml-systems-evaluation-sdk
```

## SDK Documentation

For detailed SDK documentation, see the [Python SDK Reference](../sdk/README.md). 