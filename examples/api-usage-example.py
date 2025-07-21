#!/usr/bin/env python3
"""
Example script demonstrating API usage for ML Systems Evaluation Framework.

This script shows how to:
1. Start the API server
2. Create a configuration
3. Start an evaluation
4. Generate a report
5. Download the report

Run this script after starting the API server with: ml-eval-api
"""

import json
import time
from typing import Any

import requests

# API base URL
# Note: API server runs on port 8000, Sphinx docs on port 8080
BASE_URL = "http://localhost:8000/api/v1"


def create_config() -> str:
    """Create a new configuration via API"""
    config_data = {
        "system": {
            "name": "Example ML System",
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
        "name": "Example Configuration",
        "system_type": "single_model",
        "criticality": "business_critical",
        "config_data": config_data,
    }

    response = requests.post(f"{BASE_URL}/config", json=request_data)
    response.raise_for_status()

    config_info = response.json()
    print(f"✅ Created configuration: {config_info['id']}")
    return config_info["id"]


def start_evaluation(config_id: str) -> str:
    """Start an evaluation via API"""
    request_data = {
        "config_id": config_id,
        "options": {},
    }

    response = requests.post(f"{BASE_URL}/evaluate", json=request_data)
    response.raise_for_status()

    evaluation_info = response.json()
    print(f"✅ Started evaluation: {evaluation_info['id']}")
    return evaluation_info["id"]


def wait_for_evaluation(evaluation_id: str, timeout: int = 60) -> dict[str, Any]:
    """Wait for evaluation to complete"""
    start_time = time.time()

    while time.time() - start_time < timeout:
        response = requests.get(f"{BASE_URL}/evaluate/{evaluation_id}")
        response.raise_for_status()

        evaluation_info = response.json()
        status = evaluation_info["status"]

        print(
            f"📊 Evaluation status: {status} (progress: {evaluation_info['progress']:.1%})"
        )

        if status in ["completed", "failed"]:
            return evaluation_info

        time.sleep(2)

    raise TimeoutError(
        f"Evaluation {evaluation_id} did not complete within {timeout} seconds"
    )


def generate_report(config_id: str, evaluation_id: str) -> str:
    """Generate a report via API"""
    request_data = {
        "config_id": config_id,
        "evaluation_id": evaluation_id,
        "report_type": "business",
        "format": "json",
        "options": {},
    }

    response = requests.post(f"{BASE_URL}/reports", json=request_data)
    response.raise_for_status()

    report_info = response.json()
    print(f"✅ Generated report: {report_info['id']}")
    return report_info["id"]


def download_report(report_id: str) -> dict[str, Any]:
    """Download a report via API"""
    response = requests.get(f"{BASE_URL}/reports/{report_id}/download")
    response.raise_for_status()

    report_data = response.json()
    print(f"📄 Downloaded report: {report_id}")
    return report_data


def main():
    """Main example function"""
    print("🚀 ML Systems Evaluation Framework API Example")
    print("=" * 50)

    try:
        # Check API health
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        health_info = response.json()
        print(f"✅ API is healthy: {health_info['status']}")
        print()

        # Step 1: Create configuration
        print("📝 Step 1: Creating configuration...")
        config_id = create_config()
        print()

        # Step 2: Start evaluation
        print("🔍 Step 2: Starting evaluation...")
        evaluation_id = start_evaluation(config_id)
        print()

        # Step 3: Wait for evaluation to complete
        print("⏳ Step 3: Waiting for evaluation to complete...")
        wait_for_evaluation(evaluation_id)
        print()

        # Step 4: Generate report
        print("📊 Step 4: Generating report...")
        report_id = generate_report(config_id, evaluation_id)
        print()

        # Step 5: Download report
        print("📥 Step 5: Downloading report...")
        report_data = download_report(report_id)
        print()

        # Display results
        print("🎉 Example completed successfully!")
        print(f"Configuration ID: {config_id}")
        print(f"Evaluation ID: {evaluation_id}")
        print(f"Report ID: {report_id}")
        print()
        print("📋 Report Summary:")
        print(json.dumps(report_data, indent=2))

    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API server.")
        print("Make sure the API server is running with: ml-eval-api")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
