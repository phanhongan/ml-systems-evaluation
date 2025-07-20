"""API service layer for ML Systems Evaluation Framework"""

import uuid
from datetime import datetime
from typing import Any

from ..config.factory import ConfigFactory
from ..config.validator import ConfigValidator
from ..core.framework import EvaluationFramework


class APIService:
    """Service layer for API operations"""

    def __init__(self):
        self.config_factory = ConfigFactory()
        self.validator = ConfigValidator()
        self.configs: dict[str, dict[str, Any]] = {}
        self.evaluations: dict[str, dict[str, Any]] = {}
        self.collections: dict[str, dict[str, Any]] = {}
        self.reports: dict[str, dict[str, Any]] = {}

    def get_health(self) -> dict[str, Any]:
        """Get service health status"""
        return {
            "status": "healthy",
            "timestamp": datetime.now(),
            "version": "0.1.0",
        }

    def create_config(self, config_data: dict[str, Any]) -> dict[str, Any]:
        """Create a new configuration"""
        config_id = str(uuid.uuid4())

        # Validate configuration
        self.validator.validate_config(config_data)
        errors = self.validator.get_errors()

        if errors:
            raise ValueError(f"Invalid configuration: {', '.join(errors)}")

        # Store configuration
        config_info = {
            "id": config_id,
            "name": config_data.get("system", {}).get("name", "Unnamed Config"),
            "system_type": config_data.get("system", {}).get("type", "single_model"),
            "criticality": config_data.get("system", {}).get(
                "criticality", "business_critical"
            ),
            "industry": config_data.get("system", {}).get("industry"),
            "config_data": config_data,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        self.configs[config_id] = config_info
        return config_info

    def get_config(self, config_id: str) -> dict[str, Any] | None:
        """Get configuration by ID"""
        return self.configs.get(config_id)

    def list_configs(self) -> list[dict[str, Any]]:
        """List all configurations"""
        return list(self.configs.values())

    def validate_config(self, config_data: dict[str, Any]) -> dict[str, Any]:
        """Validate configuration data"""
        self.validator.validate_config(config_data)
        errors = self.validator.get_errors()
        warnings = self.validator.get_warnings()

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    def start_evaluation(
        self, config_id: str, options: dict[str, Any]
    ) -> dict[str, Any]:
        """Start an evaluation"""
        config_info = self.configs.get(config_id)
        if not config_info:
            raise ValueError(f"Configuration {config_id} not found")

        evaluation_id = str(uuid.uuid4())

        # Create evaluation record
        evaluation_info = {
            "id": evaluation_id,
            "config_id": config_id,
            "status": "running",
            "progress": 0.0,
            "started_at": datetime.now(),
            "completed_at": None,
            "results": None,
            "options": options,
        }

        self.evaluations[evaluation_id] = evaluation_info

        # Run evaluation in background (simplified for MVP)
        try:
            framework = EvaluationFramework(config_info["config_data"])
            results = framework.evaluate()

            # Convert results to dict for JSON serialization
            results_dict = self._convert_to_dict(results)

            evaluation_info.update(
                {
                    "status": "completed",
                    "progress": 1.0,
                    "completed_at": datetime.now(),
                    "results": results_dict,
                }
            )

        except Exception as e:
            evaluation_info.update(
                {
                    "status": "failed",
                    "progress": 0.0,
                    "error": str(e),
                }
            )

        return evaluation_info

    def get_evaluation(self, evaluation_id: str) -> dict[str, Any] | None:
        """Get evaluation by ID"""
        return self.evaluations.get(evaluation_id)

    def list_evaluations(self) -> list[dict[str, Any]]:
        """List all evaluations"""
        return list(self.evaluations.values())

    def start_collection(
        self, config_id: str, collector_name: str, options: dict[str, Any]
    ) -> dict[str, Any]:
        """Start data collection"""
        config_info = self.configs.get(config_id)
        if not config_info:
            raise ValueError(f"Configuration {config_id} not found")

        collection_id = str(uuid.uuid4())

        # Create collection record
        collection_info = {
            "id": collection_id,
            "config_id": config_id,
            "collector_name": collector_name,
            "status": "running",
            "progress": 0.0,
            "records_collected": 0,
            "started_at": datetime.now(),
            "completed_at": None,
            "options": options,
        }

        self.collections[collection_id] = collection_info

        # Simulate collection (simplified for MVP)
        collection_info.update(
            {
                "status": "completed",
                "progress": 1.0,
                "records_collected": 1000,  # Mock data
                "completed_at": datetime.now(),
            }
        )

        return collection_info

    def get_collection(self, collection_id: str) -> dict[str, Any] | None:
        """Get collection by ID"""
        return self.collections.get(collection_id)

    def list_collections(self) -> list[dict[str, Any]]:
        """List all collections"""
        return list(self.collections.values())

    def generate_report(
        self,
        config_id: str,
        evaluation_id: str,
        report_type: str,
        format: str,
        options: dict[str, Any],
    ) -> dict[str, Any]:
        """Generate a report"""
        config_info = self.configs.get(config_id)
        if not config_info:
            raise ValueError(f"Configuration {config_id} not found")

        evaluation_info = self.evaluations.get(evaluation_id)
        if not evaluation_info:
            raise ValueError(f"Evaluation {evaluation_id} not found")

        report_id = str(uuid.uuid4())

        # Create report record
        report_info = {
            "id": report_id,
            "config_id": config_id,
            "evaluation_id": evaluation_id,
            "report_type": report_type,
            "format": format,
            "status": "completed",
            "download_url": f"/api/v1/reports/{report_id}/download",
            "created_at": datetime.now(),
            "options": options,
        }

        self.reports[report_id] = report_info
        return report_info

    def get_report(self, report_id: str) -> dict[str, Any] | None:
        """Get report by ID"""
        return self.reports.get(report_id)

    def list_reports(self) -> list[dict[str, Any]]:
        """List all reports"""
        return list(self.reports.values())

    def _convert_to_dict(self, obj: Any) -> Any:
        """Recursively convert objects to dictionaries for JSON serialization"""
        if hasattr(obj, "__dict__"):
            result = {}
            for key, value in obj.__dict__.items():
                if key.startswith("_"):  # Skip private attributes
                    continue
                result[key] = self._convert_to_dict(value)
            return result
        elif isinstance(obj, list | tuple):
            return [self._convert_to_dict(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self._convert_to_dict(value) for key, value in obj.items()}
        elif hasattr(obj, "isoformat"):  # Handle datetime objects
            return obj.isoformat()
        else:
            return obj
