API Reference
============

The ML Systems Evaluation Framework provides a REST API for programmatic access to all framework capabilities.

Base URL
--------

All API endpoints are prefixed with ``/api/v1``:

.. code-block:: text

   http://localhost:8000/api/v1

Authentication
-------------

Currently, the API does not require authentication for the MVP version. All endpoints are publicly accessible.

.. note::
   Future versions will include API key authentication and role-based access control.

Response Format
--------------

All API responses are returned in JSON format with the following structure:

**Success Response:**
.. code-block:: json

   {
     "id": "resource-id",
     "status": "success",
     "data": {...}
   }

**Error Response:**
.. code-block:: json

   {
     "error": {
       "code": "ERROR_CODE",
       "message": "Human-readable error message",
       "details": {...}
     }
   }

HTTP Status Codes
----------------

* ``200 OK`` - Request successful
* ``201 Created`` - Resource created successfully
* ``400 Bad Request`` - Invalid request data
* ``404 Not Found`` - Resource not found
* ``500 Internal Server Error`` - Server error

Health Check
-----------

Check API server health and version information.

**GET** ``/api/v1/health``

**Response:**
.. code-block:: json

   {
     "status": "healthy",
     "timestamp": "2024-01-01T00:00:00Z",
     "version": "0.1.0"
   }

Configuration Management
----------------------

Create, validate, and manage evaluation configurations.

Create Configuration
~~~~~~~~~~~~~~~~~~~

**POST** ``/api/v1/config``

**Request Body:**
.. code-block:: json

   {
     "name": "My ML System",
     "system_type": "single_model",
     "criticality": "business_critical",
     "industry": "manufacturing",
     "config_data": {
       "system": {
         "name": "My ML System",
         "type": "single_model",
         "criticality": "business_critical"
       },
       "slos": {
         "accuracy": {
           "target": 0.95,
           "threshold": 0.90,
           "window": 3600
         }
       },
       "collectors": [],
       "evaluators": [],
       "reports": []
     }
   }

**Response:**
.. code-block:: json

   {
     "id": "config-uuid",
     "name": "My ML System",
     "system_type": "single_model",
     "criticality": "business_critical",
     "industry": "manufacturing",
     "created_at": "2024-01-01T00:00:00Z",
     "updated_at": "2024-01-01T00:00:00Z"
   }

Get Configuration
~~~~~~~~~~~~~~~~

**GET** ``/api/v1/config/{config_id}``

**Response:**
.. code-block:: json

   {
     "id": "config-uuid",
     "name": "My ML System",
     "system_type": "single_model",
     "criticality": "business_critical",
     "industry": "manufacturing",
     "created_at": "2024-01-01T00:00:00Z",
     "updated_at": "2024-01-01T00:00:00Z"
   }

List Configurations
~~~~~~~~~~~~~~~~~~

**GET** ``/api/v1/config``

**Response:**
.. code-block:: json

   [
     {
       "id": "config-uuid-1",
       "name": "System 1",
       "system_type": "single_model",
       "criticality": "business_critical",
       "created_at": "2024-01-01T00:00:00Z",
       "updated_at": "2024-01-01T00:00:00Z"
     },
     {
       "id": "config-uuid-2",
       "name": "System 2",
       "system_type": "workflow",
       "criticality": "safety_critical",
       "created_at": "2024-01-01T00:00:00Z",
       "updated_at": "2024-01-01T00:00:00Z"
     }
   ]

Validate Configuration
~~~~~~~~~~~~~~~~~~~~~

**POST** ``/api/v1/config/validate``

**Request Body:**
.. code-block:: json

   {
     "config_data": {
       "system": {
         "name": "My ML System",
         "type": "single_model",
         "criticality": "business_critical"
       },
       "slos": {
         "accuracy": {
           "target": 0.95,
           "threshold": 0.90,
           "window": 3600
         }
       },
       "collectors": [],
       "evaluators": [],
       "reports": []
     }
   }

**Response:**
.. code-block:: json

   {
     "valid": true,
     "errors": [],
     "warnings": []
   }

Evaluation Management
--------------------

Start, monitor, and manage evaluation processes.

Start Evaluation
~~~~~~~~~~~~~~~

**POST** ``/api/v1/evaluate``

**Request Body:**
.. code-block:: json

   {
     "config_id": "config-uuid",
     "options": {
       "parallel": true,
       "timeout": 3600
     }
   }

**Response:**
.. code-block:: json

   {
     "id": "eval-uuid",
     "config_id": "config-uuid",
     "status": "running",
     "progress": 0.0,
     "started_at": "2024-01-01T00:00:00Z",
     "completed_at": null,
     "results": null
   }

Get Evaluation
~~~~~~~~~~~~~

**GET** ``/api/v1/evaluate/{evaluation_id}``

**Response:**
.. code-block:: json

   {
     "id": "eval-uuid",
     "config_id": "config-uuid",
     "status": "completed",
     "progress": 1.0,
     "started_at": "2024-01-01T00:00:00Z",
     "completed_at": "2024-01-01T01:00:00Z",
     "results": {
       "accuracy": 0.95,
       "precision": 0.92,
       "recall": 0.88
     }
   }

List Evaluations
~~~~~~~~~~~~~~~

**GET** ``/api/v1/evaluate``

**Response:**
.. code-block:: json

   [
     {
       "id": "eval-uuid-1",
       "config_id": "config-uuid-1",
       "status": "completed",
       "progress": 1.0,
       "started_at": "2024-01-01T00:00:00Z",
       "completed_at": "2024-01-01T01:00:00Z"
     },
     {
       "id": "eval-uuid-2",
       "config_id": "config-uuid-2",
       "status": "running",
       "progress": 0.5,
       "started_at": "2024-01-01T02:00:00Z",
       "completed_at": null
     }
   ]

Data Collection Management
-------------------------

Start and monitor data collection processes.

Start Collection
~~~~~~~~~~~~~~~

**POST** ``/api/v1/collect``

**Request Body:**
.. code-block:: json

   {
     "config_id": "config-uuid",
     "collector_name": "quality_collector",
     "options": {
       "batch_size": 10000,
       "timeout": 1800
     }
   }

**Response:**
.. code-block:: json

   {
     "id": "collection-uuid",
     "config_id": "config-uuid",
     "status": "running",
     "progress": 0.0,
     "records_collected": 0,
     "started_at": "2024-01-01T00:00:00Z",
     "completed_at": null
   }

Get Collection
~~~~~~~~~~~~~

**GET** ``/api/v1/collect/{collection_id}``

**Response:**
.. code-block:: json

   {
     "id": "collection-uuid",
     "config_id": "config-uuid",
     "status": "completed",
     "progress": 1.0,
     "records_collected": 50000,
     "started_at": "2024-01-01T00:00:00Z",
     "completed_at": "2024-01-01T00:30:00Z"
   }

List Collections
~~~~~~~~~~~~~~~

**GET** ``/api/v1/collect``

**Response:**
.. code-block:: json

   [
     {
       "id": "collection-uuid-1",
       "config_id": "config-uuid-1",
       "status": "completed",
       "progress": 1.0,
       "records_collected": 50000,
       "started_at": "2024-01-01T00:00:00Z",
       "completed_at": "2024-01-01T00:30:00Z"
     },
     {
       "id": "collection-uuid-2",
       "config_id": "config-uuid-2",
       "status": "running",
       "progress": 0.75,
       "records_collected": 37500,
       "started_at": "2024-01-01T01:00:00Z",
       "completed_at": null
     }
   ]

Report Management
----------------

Generate and download evaluation reports.

Generate Report
~~~~~~~~~~~~~~

**POST** ``/api/v1/reports``

**Request Body:**
.. code-block:: json

   {
     "config_id": "config-uuid",
     "evaluation_id": "eval-uuid",
     "report_type": "business",
     "format": "json",
     "options": {
       "include_charts": true,
       "include_recommendations": true
     }
   }

**Response:**
.. code-block:: json

   {
     "id": "report-uuid",
     "config_id": "config-uuid",
     "evaluation_id": "eval-uuid",
     "status": "completed",
     "download_url": "/api/v1/reports/report-uuid/download",
     "created_at": "2024-01-01T00:00:00Z"
   }

Get Report
~~~~~~~~~~

**GET** ``/api/v1/reports/{report_id}``

**Response:**
.. code-block:: json

   {
     "id": "report-uuid",
     "config_id": "config-uuid",
     "evaluation_id": "eval-uuid",
     "status": "completed",
     "download_url": "/api/v1/reports/report-uuid/download",
     "created_at": "2024-01-01T00:00:00Z"
   }

List Reports
~~~~~~~~~~~

**GET** ``/api/v1/reports``

**Response:**
.. code-block:: json

   [
     {
       "id": "report-uuid-1",
       "config_id": "config-uuid-1",
       "evaluation_id": "eval-uuid-1",
       "status": "completed",
       "download_url": "/api/v1/reports/report-uuid-1/download",
       "created_at": "2024-01-01T00:00:00Z"
     },
     {
       "id": "report-uuid-2",
       "config_id": "config-uuid-2",
       "evaluation_id": "eval-uuid-2",
       "status": "completed",
       "download_url": "/api/v1/reports/report-uuid-2/download",
       "created_at": "2024-01-01T01:00:00Z"
     }
   ]

Download Report
~~~~~~~~~~~~~~

**GET** ``/api/v1/reports/{report_id}/download``

**Response:**
.. code-block:: json

   {
     "report_id": "report-uuid",
     "type": "business",
     "format": "json",
     "content": "Report content...",
     "generated_at": "2024-01-01T00:00:00Z"
   }

Error Handling
-------------

The API uses standard HTTP status codes and returns detailed error messages.

**400 Bad Request:**
.. code-block:: json

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

**404 Not Found:**
.. code-block:: json

   {
     "error": {
       "code": "NOT_FOUND",
       "message": "Configuration not found",
       "details": {
         "resource": "config",
         "id": "nonexistent-id"
       }
     }
   }

**500 Internal Server Error:**
.. code-block:: json

   {
     "error": {
       "code": "INTERNAL_ERROR",
       "message": "Internal server error",
       "details": {
         "traceback": "..."
       }
     }
   }

Common Error Codes
~~~~~~~~~~~~~~~~~

* ``AUTHENTICATION_ERROR`` - Invalid API key or token
* ``AUTHORIZATION_ERROR`` - Insufficient permissions
* ``VALIDATION_ERROR`` - Invalid request data
* ``NOT_FOUND`` - Resource not found
* ``CONFLICT`` - Resource conflict
* ``RATE_LIMIT_EXCEEDED`` - Too many requests
* ``INTERNAL_ERROR`` - Server error

Rate Limiting
-------------

Currently, the API does not implement rate limiting for the MVP version.

.. note::
   Future versions will include configurable rate limiting based on API plan tiers.

API Versioning
--------------

The API uses URL versioning with the format ``/api/v1/``.

.. note::
   Future API versions will be available at ``/api/v2/``, etc., with backward compatibility maintained.

Interactive Documentation
-----------------------

The API provides interactive documentation when the server is running:

* **Swagger UI**: http://localhost:8000/docs
* **ReDoc**: http://localhost:8000/redoc

These provide interactive documentation with:
* Request/response examples
* Schema validation
* Try-it-out functionality
* Authentication information

SDK Examples
-----------

Python SDK Example
~~~~~~~~~~~~~~~~~

.. code-block:: python

   import requests

   # Base URL
   BASE_URL = "http://localhost:8000/api/v1"

   # Create configuration
   config_data = {
       "system": {
           "name": "My ML System",
           "type": "single_model",
           "criticality": "business_critical"
       },
       "slos": {
           "accuracy": {
               "target": 0.95,
               "threshold": 0.90,
               "window": 3600
           }
       },
       "collectors": [],
       "evaluators": [],
       "reports": []
   }

   response = requests.post(f"{BASE_URL}/config", json={
       "name": "My Config",
       "system_type": "single_model",
       "criticality": "business_critical",
       "config_data": config_data
   })

   config_id = response.json()["id"]

   # Start evaluation
   eval_response = requests.post(f"{BASE_URL}/evaluate", json={
       "config_id": config_id,
       "options": {}
   })

   evaluation_id = eval_response.json()["id"]

   # Generate report
   report_response = requests.post(f"{BASE_URL}/reports", json={
       "config_id": config_id,
       "evaluation_id": evaluation_id,
       "report_type": "business",
       "format": "json"
   })

   report_id = report_response.json()["id"]

   # Download report
   download_response = requests.get(f"{BASE_URL}/reports/{report_id}/download")
   report_content = download_response.json()

cURL Examples
~~~~~~~~~~~~

Create Configuration:
.. code-block:: bash

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
         "slos": {
           "accuracy": {
             "target": 0.95,
             "threshold": 0.90,
             "window": 3600
           }
         },
         "collectors": [],
         "evaluators": [],
         "reports": []
       }
     }'

Start Evaluation:
.. code-block:: bash

   curl -X POST "http://localhost:8000/api/v1/evaluate" \
     -H "Content-Type: application/json" \
     -d '{
       "config_id": "your-config-id",
       "options": {}
     }'

Get Evaluation Status:
.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/evaluate/your-evaluation-id"

Generate Report:
.. code-block:: bash

   curl -X POST "http://localhost:8000/api/v1/reports" \
     -H "Content-Type: application/json" \
     -d '{
       "config_id": "your-config-id",
       "evaluation_id": "your-evaluation-id",
       "report_type": "business",
       "format": "json"
     }'

Download Report:
.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/reports/your-report-id/download" 