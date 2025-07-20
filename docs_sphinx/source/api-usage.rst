API Usage Guide
==============

This guide provides practical examples of how to use the ML Systems Evaluation Framework API for common tasks.

Prerequisites
------------

1. **Install the Framework:**
   .. code-block:: bash

      pip install ml-systems-evaluation

2. **Start the API Server:**
   .. code-block:: bash

      ml-eval-api

3. **Verify the Server is Running:**
   .. code-block:: bash

      curl http://localhost:8000/api/v1/health

   Expected response:
   .. code-block:: json

      {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "0.1.0"
      }

Quick Start Example
------------------

This example demonstrates a complete workflow: creating a configuration, running an evaluation, and generating a report.

Python Example
~~~~~~~~~~~~~

.. code-block:: python

   import requests
   import time
   import json

   # API Configuration
   BASE_URL = "http://localhost:8000/api/v1"

   def create_manufacturing_config():
       """Create a manufacturing system configuration"""
       config_data = {
           "system": {
               "name": "Quality Control System",
               "type": "single_model",
               "criticality": "business_critical",
               "industry": "manufacturing"
           },
           "slos": {
               "accuracy": {
                   "target": 0.95,
                   "threshold": 0.90,
                   "window": 3600
               },
               "latency": {
                   "target": 0.1,
                   "threshold": 0.5,
                   "window": 3600
               }
           },
           "collectors": [
               {
                   "name": "quality_collector",
                   "type": "offline",
                   "data_source": "quality_metrics"
               }
           ],
           "evaluators": [
               {
                   "name": "performance_evaluator",
                   "type": "performance",
                   "metrics": ["accuracy", "precision", "recall"]
               }
           ],
           "reports": [
               {
                   "name": "business_report",
                   "type": "business",
                   "format": "json"
               }
           ]
       }

       response = requests.post(f"{BASE_URL}/config", json={
           "name": "Manufacturing Quality Control",
           "system_type": "single_model",
           "criticality": "business_critical",
           "industry": "manufacturing",
           "config_data": config_data
       })

       if response.status_code == 200:
           config = response.json()
           print(f"✅ Created configuration: {config['id']}")
           return config['id']
       else:
           print(f"❌ Failed to create configuration: {response.text}")
           return None

   def start_evaluation(config_id):
       """Start an evaluation"""
       response = requests.post(f"{BASE_URL}/evaluate", json={
           "config_id": config_id,
           "options": {
               "parallel": True,
               "timeout": 3600
           }
       })

       if response.status_code == 200:
           evaluation = response.json()
           print(f"✅ Started evaluation: {evaluation['id']}")
           return evaluation['id']
       else:
           print(f"❌ Failed to start evaluation: {response.text}")
           return None

   def wait_for_evaluation(evaluation_id, timeout=300):
       """Wait for evaluation to complete"""
       start_time = time.time()
       
       while time.time() - start_time < timeout:
           response = requests.get(f"{BASE_URL}/evaluate/{evaluation_id}")
           
           if response.status_code == 200:
               evaluation = response.json()
               status = evaluation['status']
               progress = evaluation['progress']
               
               print(f"📊 Status: {status} (Progress: {progress:.1%})")
               
               if status in ['completed', 'failed']:
                   return evaluation
           
           time.sleep(5)
       
       raise TimeoutError(f"Evaluation {evaluation_id} did not complete within {timeout} seconds")

   def generate_report(config_id, evaluation_id):
       """Generate a report"""
       response = requests.post(f"{BASE_URL}/reports", json={
           "config_id": config_id,
           "evaluation_id": evaluation_id,
           "report_type": "business",
           "format": "json",
           "options": {
               "include_charts": True,
               "include_recommendations": True
           }
       })

       if response.status_code == 200:
           report = response.json()
           print(f"✅ Generated report: {report['id']}")
           return report['id']
       else:
           print(f"❌ Failed to generate report: {response.text}")
           return None

   def download_report(report_id):
       """Download and display report"""
       response = requests.get(f"{BASE_URL}/reports/{report_id}/download")
       
       if response.status_code == 200:
           report_content = response.json()
           print("📄 Report Content:")
           print(json.dumps(report_content, indent=2))
           return report_content
       else:
           print(f"❌ Failed to download report: {response.text}")
           return None

   def main():
       """Complete workflow example"""
       print("🚀 ML Systems Evaluation Framework - Complete Workflow")
       print("=" * 60)
       
       # Step 1: Create configuration
       print("\n📝 Step 1: Creating configuration...")
       config_id = create_manufacturing_config()
       if not config_id:
           return
       
       # Step 2: Start evaluation
       print("\n🔍 Step 2: Starting evaluation...")
       evaluation_id = start_evaluation(config_id)
       if not evaluation_id:
           return
       
       # Step 3: Wait for completion
       print("\n⏳ Step 3: Waiting for evaluation to complete...")
       try:
           evaluation_result = wait_for_evaluation(evaluation_id)
           print(f"✅ Evaluation completed with status: {evaluation_result['status']}")
       except TimeoutError as e:
           print(f"❌ {e}")
           return
       
       # Step 4: Generate report
       print("\n📊 Step 4: Generating report...")
       report_id = generate_report(config_id, evaluation_id)
       if not report_id:
           return
       
       # Step 5: Download report
       print("\n📥 Step 5: Downloading report...")
       download_report(report_id)
       
       print("\n🎉 Workflow completed successfully!")

   if __name__ == "__main__":
       main()

cURL Example
~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   
   # API Configuration
   BASE_URL="http://localhost:8000/api/v1"
   
   echo "🚀 ML Systems Evaluation Framework - Complete Workflow"
   echo "======================================================"
   
   # Step 1: Create configuration
   echo -e "\n📝 Step 1: Creating configuration..."
   CONFIG_RESPONSE=$(curl -s -X POST "$BASE_URL/config" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Manufacturing Quality Control",
       "system_type": "single_model",
       "criticality": "business_critical",
       "industry": "manufacturing",
       "config_data": {
         "system": {
           "name": "Quality Control System",
           "type": "single_model",
           "criticality": "business_critical",
           "industry": "manufacturing"
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
     }')
   
   CONFIG_ID=$(echo $CONFIG_RESPONSE | jq -r '.id')
   echo "✅ Created configuration: $CONFIG_ID"
   
   # Step 2: Start evaluation
   echo -e "\n🔍 Step 2: Starting evaluation..."
   EVAL_RESPONSE=$(curl -s -X POST "$BASE_URL/evaluate" \
     -H "Content-Type: application/json" \
     -d "{
       \"config_id\": \"$CONFIG_ID\",
       \"options\": {}
     }")
   
   EVAL_ID=$(echo $EVAL_RESPONSE | jq -r '.id')
   echo "✅ Started evaluation: $EVAL_ID"
   
   # Step 3: Wait for completion
   echo -e "\n⏳ Step 3: Waiting for evaluation to complete..."
   while true; do
     EVAL_STATUS=$(curl -s "$BASE_URL/evaluate/$EVAL_ID" | jq -r '.status')
     EVAL_PROGRESS=$(curl -s "$BASE_URL/evaluate/$EVAL_ID" | jq -r '.progress')
     
     echo "📊 Status: $EVAL_STATUS (Progress: $(echo "$EVAL_PROGRESS * 100" | bc -l | cut -c1-4)%)"
     
     if [ "$EVAL_STATUS" = "completed" ] || [ "$EVAL_STATUS" = "failed" ]; then
       break
     fi
     
     sleep 5
   done
   
   # Step 4: Generate report
   echo -e "\n📊 Step 4: Generating report..."
   REPORT_RESPONSE=$(curl -s -X POST "$BASE_URL/reports" \
     -H "Content-Type: application/json" \
     -d "{
       \"config_id\": \"$CONFIG_ID\",
       \"evaluation_id\": \"$EVAL_ID\",
       \"report_type\": \"business\",
       \"format\": \"json\"
     }")
   
   REPORT_ID=$(echo $REPORT_RESPONSE | jq -r '.id')
   echo "✅ Generated report: $REPORT_ID"
   
   # Step 5: Download report
   echo -e "\n📥 Step 5: Downloading report..."
   curl -s "$BASE_URL/reports/$REPORT_ID/download" | jq '.'
   
   echo -e "\n🎉 Workflow completed successfully!"

Industry-Specific Examples
-------------------------

Aviation Safety System
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def create_aviation_config():
       """Create an aviation safety system configuration"""
       config_data = {
           "system": {
               "name": "Aircraft Landing System",
               "type": "single_model",
               "criticality": "safety_critical",
               "industry": "aviation"
           },
           "slos": {
               "accuracy": {
                   "target": 0.999,
                   "threshold": 0.999,
                   "window": 3600
               },
               "latency": {
                   "target": 0.05,
                   "threshold": 0.1,
                   "window": 3600
               }
           },
           "collectors": [
               {
                   "name": "sensor_collector",
                   "type": "online",
                   "data_source": "flight_sensors"
               }
           ],
           "evaluators": [
               {
                   "name": "safety_evaluator",
                   "type": "safety",
                   "metrics": ["reliability", "fault_tolerance"]
               }
           ],
           "reports": [
               {
                   "name": "safety_report",
                   "type": "safety",
                   "format": "json"
               }
           ]
       }

       response = requests.post(f"{BASE_URL}/config", json={
           "name": "Aviation Safety System",
           "system_type": "single_model",
           "criticality": "safety_critical",
           "industry": "aviation",
           "config_data": config_data
       })

       return response.json()['id'] if response.status_code == 200 else None

Manufacturing Quality Control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def create_manufacturing_config():
       """Create a manufacturing quality control configuration"""
       config_data = {
           "system": {
               "name": "Quality Control System",
               "type": "single_model",
               "criticality": "business_critical",
               "industry": "manufacturing"
           },
           "slos": {
               "accuracy": {
                   "target": 0.95,
                   "threshold": 0.90,
                   "window": 3600
               },
               "throughput": {
                   "target": 1000,
                   "threshold": 800,
                   "window": 3600
               }
           },
           "collectors": [
               {
                   "name": "quality_collector",
                   "type": "offline",
                   "data_source": "quality_metrics"
               }
           ],
           "evaluators": [
               {
                   "name": "performance_evaluator",
                   "type": "performance",
                   "metrics": ["accuracy", "precision", "recall"]
               }
           ],
           "reports": [
               {
                   "name": "business_report",
                   "type": "business",
                   "format": "json"
               }
           ]
       }

       response = requests.post(f"{BASE_URL}/config", json={
           "name": "Manufacturing Quality Control",
           "system_type": "single_model",
           "criticality": "business_critical",
           "industry": "manufacturing",
           "config_data": config_data
       })

       return response.json()['id'] if response.status_code == 200 else None

Error Handling
-------------

The API provides comprehensive error handling with detailed error messages.

Python Error Handling
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import requests
   from requests.exceptions import RequestException

   def safe_api_call(method, url, **kwargs):
       """Make a safe API call with error handling"""
       try:
           response = requests.request(method, url, **kwargs)
           response.raise_for_status()
           return response.json()
       except requests.exceptions.HTTPError as e:
           error_data = e.response.json() if e.response.content else {}
           print(f"HTTP Error {e.response.status_code}: {error_data.get('detail', str(e))}")
           return None
       except requests.exceptions.ConnectionError:
           print("❌ Connection Error: Could not connect to API server")
           print("Make sure the server is running with: ml-eval-api")
           return None
       except requests.exceptions.Timeout:
           print("❌ Timeout Error: Request timed out")
           return None
       except RequestException as e:
           print(f"❌ Request Error: {e}")
           return None

   # Example usage
   def create_config_safely():
       """Create configuration with error handling"""
       result = safe_api_call(
           'POST',
           f"{BASE_URL}/config",
           json={
               "name": "Test System",
               "system_type": "single_model",
               "criticality": "business_critical",
               "config_data": {
                   "system": {"name": "Test", "type": "single_model", "criticality": "business_critical"},
                   "slos": {"accuracy": {"target": 0.95, "threshold": 0.90, "window": 3600}},
                   "collectors": [],
                   "evaluators": [],
                   "reports": []
               }
           }
       )
       
       if result:
           print(f"✅ Configuration created: {result['id']}")
           return result['id']
       else:
           print("❌ Failed to create configuration")
           return None

Common Error Scenarios
~~~~~~~~~~~~~~~~~~~~~

1. **Invalid Configuration:**
   .. code-block:: json

      {
        "error": {
          "code": "VALIDATION_ERROR",
          "message": "Invalid configuration format",
          "details": {
            "field": "slos",
            "issue": "Missing required field 'window'"
          }
        }
      }

2. **Resource Not Found:**
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

3. **Server Error:**
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

Best Practices
-------------

1. **Always Check Response Status:**
   .. code-block:: python

      response = requests.post(f"{BASE_URL}/config", json=config_data)
      if response.status_code == 200:
          config = response.json()
          # Process successful response
      else:
          print(f"Error: {response.status_code} - {response.text}")

2. **Use Proper Error Handling:**
   .. code-block:: python

      try:
          response = requests.get(f"{BASE_URL}/evaluate/{evaluation_id}")
          response.raise_for_status()
          evaluation = response.json()
      except requests.exceptions.HTTPError as e:
          print(f"HTTP Error: {e.response.status_code}")
      except requests.exceptions.ConnectionError:
          print("Connection failed - check if server is running")

3. **Poll for Long-Running Operations:**
   .. code-block:: python

      def wait_for_completion(resource_type, resource_id, timeout=300):
          start_time = time.time()
          while time.time() - start_time < timeout:
              response = requests.get(f"{BASE_URL}/{resource_type}/{resource_id}")
              if response.status_code == 200:
                  data = response.json()
                  if data['status'] in ['completed', 'failed']:
                      return data
              time.sleep(5)
          raise TimeoutError(f"Operation did not complete within {timeout} seconds")

4. **Use Environment Variables for Configuration:**
   .. code-block:: python

      import os
      
      BASE_URL = os.getenv('ML_EVAL_API_URL', 'http://localhost:8000/api/v1')
      API_TIMEOUT = int(os.getenv('ML_EVAL_API_TIMEOUT', '30'))

5. **Implement Retry Logic:**
   .. code-block:: python

      from tenacity import retry, stop_after_attempt, wait_exponential
      
      @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
      def api_call_with_retry(method, url, **kwargs):
          response = requests.request(method, url, **kwargs)
          response.raise_for_status()
          return response.json()

Testing Your API Integration
---------------------------

1. **Health Check:**
   .. code-block:: bash

      curl http://localhost:8000/api/v1/health

2. **Configuration Validation:**
   .. code-block:: bash

      curl -X POST http://localhost:8000/api/v1/config/validate \
        -H "Content-Type: application/json" \
        -d @config.json

3. **Complete Workflow Test:**
   .. code-block:: bash

      # Run the complete workflow example
      python examples/api-usage-example.py

4. **Load Testing:**
   .. code-block:: python

      import concurrent.futures
      import requests
      
      def test_endpoint():
          response = requests.get(f"{BASE_URL}/health")
          return response.status_code == 200
      
      # Test with multiple concurrent requests
      with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
          results = list(executor.map(lambda _: test_endpoint(), range(100)))
      
      success_rate = sum(results) / len(results)
      print(f"Success rate: {success_rate:.2%}") 