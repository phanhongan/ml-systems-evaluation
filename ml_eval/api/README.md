# ML Systems Evaluation Framework API

A minimum viable REST API for the ML Systems Evaluation Framework.

## Features

- **Health Check**: Service status and version information
- **Configuration Management**: Create, validate, and manage configurations
- **Evaluation**: Start and monitor evaluations
- **Data Collection**: Start and monitor data collection processes
- **Reporting**: Generate and download reports
- **Interactive Documentation**: Auto-generated API docs with Swagger UI

## Quick Start

### Start the API Server

```bash
# Start the API server
ml-eval-api

# Start with custom host/port
ml-eval-api --host 0.0.0.0 --port 8080

# Start in development mode with auto-reload
ml-eval-api --reload
```

### Access API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

**Note**: The API server uses port 8000 by default. The Sphinx documentation server uses port 8080 to avoid conflicts.

## API Endpoints

### Health Check
- `GET /api/v1/health` - Service health status

### Configuration Management
- `POST /api/v1/config` - Create new configuration
- `GET /api/v1/config/{config_id}` - Get configuration by ID
- `GET /api/v1/config` - List all configurations
- `POST /api/v1/config/validate` - Validate configuration data

### Evaluation
- `POST /api/v1/evaluate` - Start evaluation
- `GET /api/v1/evaluate/{evaluation_id}` - Get evaluation by ID
- `GET /api/v1/evaluate` - List all evaluations

### Data Collection
- `POST /api/v1/collect` - Start data collection
- `GET /api/v1/collect/{collection_id}` - Get collection by ID
- `GET /api/v1/collect` - List all collections

### Reports
- `POST /api/v1/reports` - Generate report
- `GET /api/v1/reports/{report_id}` - Get report by ID
- `GET /api/v1/reports` - List all reports
- `GET /api/v1/reports/{report_id}/download` - Download report

## Example Usage

### Create Configuration

```bash
curl -X POST "http://localhost:8000/api/v1/config" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My ML System",
    "system_type": "single_model",
    "criticality": "business_critical",
    "config_data": {
      "system": {
        "name": "My ML System",
        "type": "single_model",
        "criticality": "business_critical"
      },
      "collectors": [],
      "evaluators": [],
      "reports": []
    }
  }'
```

### Start Evaluation

```bash
curl -X POST "http://localhost:8000/api/v1/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "config_id": "your-config-id",
    "options": {}
  }'
```

### Generate Report

```bash
curl -X POST "http://localhost:8000/api/v1/reports" \
  -H "Content-Type: application/json" \
  -d '{
    "config_id": "your-config-id",
    "evaluation_id": "your-evaluation-id",
    "report_type": "business",
    "format": "json",
    "options": {}
  }'
```

## Development

### Running Tests

```bash
# Run API tests
pytest tests/test_api.py -v

# Run all tests
pytest
```

### API Structure

```
ml_eval/api/
├── __init__.py      # Package initialization
├── main.py          # FastAPI application entry point
├── models.py        # Pydantic request/response models
├── routes.py        # API route definitions
├── service.py       # Business logic service layer
└── README.md        # This file
```

## MVP Limitations

This is a minimum viable implementation with the following limitations:

1. **In-Memory Storage**: All data is stored in memory and lost on restart
2. **Synchronous Operations**: Evaluations run synchronously (not background jobs)
3. **Mock Data**: Some operations return mock data for demonstration
4. **No Authentication**: No authentication or authorization implemented
5. **No Persistence**: No database or file storage for configurations/results

## Future Enhancements

- [ ] Background job processing with Celery
- [ ] Database persistence with SQLAlchemy
- [ ] Authentication and authorization
- [ ] File upload/download for configurations and reports
- [ ] Real-time status updates with WebSockets
- [ ] Rate limiting and API key management
- [ ] Metrics and monitoring endpoints 