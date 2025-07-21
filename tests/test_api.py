"""Tests for the API component"""

from fastapi.testclient import TestClient

from ml_eval.api.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "version" in data
    assert data["status"] == "healthy"


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data
    assert "health" in data


def test_create_config():
    """Test configuration creation"""
    config_data = {
        "system": {
            "name": "Test System",
            "type": "single_model",
            "criticality": "business_critical",
        },
        "slos": {
            "accuracy": {
                "target": 0.95,
                "threshold": 0.90,
                "window": 3600,  # 1 hour window
            }
        },
        "collectors": [],
        "evaluators": [],
        "reports": [],
    }

    request_data = {
        "name": "Test Config",
        "system_type": "single_model",
        "criticality": "business_critical",
        "config_data": config_data,
    }

    response = client.post("/api/v1/config", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "Test Config"
    assert data["system_type"] == "single_model"
    assert data["criticality"] == "business_critical"


def test_validate_config():
    """Test configuration validation"""
    config_data = {
        "system": {
            "name": "Test System",
            "type": "single_model",
            "criticality": "business_critical",
        },
        "slos": {
            "accuracy": {
                "target": 0.95,
                "threshold": 0.90,
                "window": 3600,  # 1 hour window
            }
        },
        "collectors": [],
        "evaluators": [],
        "reports": [],
    }

    request_data = {"config_data": config_data}

    response = client.post("/api/v1/config/validate", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "valid" in data
    assert "errors" in data
    assert "warnings" in data


def test_list_configs():
    """Test listing configurations"""
    response = client.get("/api/v1/config")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_nonexistent_config():
    """Test getting non-existent configuration"""
    response = client.get("/api/v1/config/nonexistent-id")
    assert response.status_code == 404


def test_start_evaluation():
    """Test starting evaluation"""
    # First create a config
    config_data = {
        "system": {
            "name": "Test System",
            "type": "single_model",
            "criticality": "business_critical",
        },
        "slos": {
            "accuracy": {
                "target": 0.95,
                "threshold": 0.90,
                "window": 3600,  # 1 hour window
            }
        },
        "collectors": [],
        "evaluators": [],
        "reports": [],
    }

    create_request = {
        "name": "Test Config",
        "system_type": "single_model",
        "criticality": "business_critical",
        "config_data": config_data,
    }

    create_response = client.post("/api/v1/config", json=create_request)
    assert create_response.status_code == 200
    config_id = create_response.json()["id"]

    # Start evaluation
    eval_request = {
        "config_id": config_id,
        "options": {},
    }

    response = client.post("/api/v1/evaluate", json=eval_request)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["config_id"] == config_id
    assert "status" in data
    assert "progress" in data


def test_list_evaluations():
    """Test listing evaluations"""
    response = client.get("/api/v1/evaluate")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_start_collection():
    """Test starting data collection"""
    # First create a config
    config_data = {
        "system": {
            "name": "Test System",
            "type": "single_model",
            "criticality": "business_critical",
        },
        "slos": {
            "accuracy": {
                "target": 0.95,
                "threshold": 0.90,
                "window": 3600,  # 1 hour window
            }
        },
        "collectors": [],
        "evaluators": [],
        "reports": [],
    }

    create_request = {
        "name": "Test Config",
        "system_type": "single_model",
        "criticality": "business_critical",
        "config_data": config_data,
    }

    create_response = client.post("/api/v1/config", json=create_request)
    assert create_response.status_code == 200
    config_id = create_response.json()["id"]

    # Start collection
    collection_request = {
        "config_id": config_id,
        "collector_name": "test_collector",
        "options": {},
    }

    response = client.post("/api/v1/collect", json=collection_request)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["config_id"] == config_id
    assert "status" in data
    assert "progress" in data


def test_list_collections():
    """Test listing collections"""
    response = client.get("/api/v1/collect")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_generate_report():
    """Test report generation"""
    # First create a config and evaluation
    config_data = {
        "system": {
            "name": "Test System",
            "type": "single_model",
            "criticality": "business_critical",
        },
        "slos": {
            "accuracy": {
                "target": 0.95,
                "threshold": 0.90,
                "window": 3600,  # 1 hour window
            }
        },
        "collectors": [],
        "evaluators": [],
        "reports": [],
    }

    create_request = {
        "name": "Test Config",
        "system_type": "single_model",
        "criticality": "business_critical",
        "config_data": config_data,
    }

    create_response = client.post("/api/v1/config", json=create_request)
    assert create_response.status_code == 200
    config_id = create_response.json()["id"]

    eval_request = {
        "config_id": config_id,
        "options": {},
    }

    eval_response = client.post("/api/v1/evaluate", json=eval_request)
    assert eval_response.status_code == 200
    evaluation_id = eval_response.json()["id"]

    # Generate report
    report_request = {
        "config_id": config_id,
        "evaluation_id": evaluation_id,
        "report_type": "business",
        "format": "json",
        "options": {},
    }

    response = client.post("/api/v1/reports", json=report_request)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["config_id"] == config_id
    assert data["evaluation_id"] == evaluation_id
    assert "status" in data


def test_list_reports():
    """Test listing reports"""
    response = client.get("/api/v1/reports")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_download_report():
    """Test report download"""
    # First create a report
    config_data = {
        "system": {
            "name": "Test System",
            "type": "single_model",
            "criticality": "business_critical",
        },
        "slos": {
            "accuracy": {
                "target": 0.95,
                "threshold": 0.90,
                "window": 3600,  # 1 hour window
            }
        },
        "collectors": [],
        "evaluators": [],
        "reports": [],
    }

    create_request = {
        "name": "Test Config",
        "system_type": "single_model",
        "criticality": "business_critical",
        "config_data": config_data,
    }

    create_response = client.post("/api/v1/config", json=create_request)
    assert create_response.status_code == 200
    config_id = create_response.json()["id"]

    eval_request = {
        "config_id": config_id,
        "options": {},
    }

    eval_response = client.post("/api/v1/evaluate", json=eval_request)
    assert eval_response.status_code == 200
    evaluation_id = eval_response.json()["id"]

    report_request = {
        "config_id": config_id,
        "evaluation_id": evaluation_id,
        "report_type": "business",
        "format": "json",
        "options": {},
    }

    report_response = client.post("/api/v1/reports", json=report_request)
    assert report_response.status_code == 200
    report_id = report_response.json()["id"]

    # Download report
    response = client.get(f"/api/v1/reports/{report_id}/download")
    assert response.status_code == 200
    data = response.json()
    assert "report_id" in data
    assert "type" in data
    assert "format" in data
    assert "content" in data
