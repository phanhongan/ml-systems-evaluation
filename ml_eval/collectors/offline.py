"""Offline data collection for ML Systems Evaluation Framework"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from ..core.config import MetricData
from .base import BaseCollector


class OfflineCollector(BaseCollector):
    """Collector for offline data sources (files, logs, databases)"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.data_sources = config.get("data_sources", [])
        self.file_patterns = config.get("file_patterns", ["*.json", "*.csv"])
        self.log_paths = config.get("log_paths", [])
        self.database_config = config.get("database_config", {})
        self.parsing_rules = config.get("parsing_rules", {})

    def get_required_config_fields(self) -> List[str]:
        return ["data_sources"]

    def collect(self) -> Dict[str, List[MetricData]]:
        """Collect metrics from offline data sources"""
        try:
            if not self.health_check():
                self.logger.warning(
                    f"Offline collector health check failed for {self.name}"
                )
                return {}

            return self._collect_offline_data()
        except Exception as e:
            self.logger.error(f"Failed to collect offline data from {self.name}: {e}")
            return {}

    def health_check(self) -> bool:
        """Check if offline data sources are accessible"""
        try:
            # Check file accessibility
            for source in self.data_sources:
                if not self._check_source_health(source):
                    self.logger.warning(f"Data source {source} health check failed")
                    return False
            return True
        except Exception as e:
            self.logger.error(f"Offline health check failed: {e}")
            return False

    def _collect_offline_data(self) -> Dict[str, List[MetricData]]:
        """Collect data from offline sources"""
        metrics = {}
        timestamp = datetime.now()

        for source in self.data_sources:
            try:
                source_metrics = self._collect_from_source(source, timestamp)
                metrics.update(source_metrics)
            except Exception as e:
                self.logger.error(f"Failed to collect from source {source}: {e}")
                continue

        return metrics

    def _check_source_health(self, source: str) -> bool:
        """Check health of a specific data source"""
        try:
            if source.startswith("file://"):
                file_path = source[7:]  # Remove 'file://' prefix
                return Path(file_path).exists()
            elif source.startswith("db://"):
                return self._check_database_health(source)
            else:
                # Assume it's a file path
                return Path(source).exists()
        except Exception as e:
            self.logger.error(f"Health check failed for source {source}: {e}")
            return False

    def _check_database_health(self, db_source: str) -> bool:
        """Check database connectivity"""
        try:
            # This would check actual database connectivity
            # For now, return True for simulation
            return True
        except Exception:
            return False

    def _collect_from_source(
        self, source: str, timestamp: datetime
    ) -> Dict[str, List[MetricData]]:
        """Collect data from a specific source"""
        metrics = {}

        if source.startswith("file://"):
            file_path = source[7:]
            metrics = self._collect_from_file(file_path, timestamp)
        elif source.startswith("db://"):
            metrics = self._collect_from_database(source, timestamp)
        else:
            # Assume it's a file path
            metrics = self._collect_from_file(source, timestamp)

        return metrics

    def _collect_from_file(
        self, file_path: str, timestamp: datetime
    ) -> Dict[str, List[MetricData]]:
        """Collect data from a file"""
        metrics = {}
        path = Path(file_path)

        if not path.exists():
            self.logger.warning(f"File not found: {file_path}")
            return metrics

        try:
            if path.suffix.lower() == ".json":
                metrics = self._parse_json_file(path, timestamp)
            elif path.suffix.lower() == ".csv":
                metrics = self._parse_csv_file(path, timestamp)
            else:
                self.logger.warning(f"Unsupported file type: {path.suffix}")

        except Exception as e:
            self.logger.error(f"Failed to parse file {file_path}: {e}")

        return metrics

    def _parse_json_file(
        self, file_path: Path, timestamp: datetime
    ) -> Dict[str, List[MetricData]]:
        """Parse JSON file and extract metrics"""
        metrics = {}

        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            # Extract metrics based on parsing rules
            for metric_name, value in data.items():
                if isinstance(value, (int, float)):
                    metrics[f"offline_{metric_name}"] = [
                        MetricData(
                            timestamp=timestamp,
                            value=float(value),
                            metadata={
                                "source": self.name,
                                "file_path": str(file_path),
                                "offline": True,
                            },
                        )
                    ]

        except Exception as e:
            self.logger.error(f"Failed to parse JSON file {file_path}: {e}")

        return metrics

    def _parse_csv_file(
        self, file_path: Path, timestamp: datetime
    ) -> Dict[str, List[MetricData]]:
        """Parse CSV file and extract metrics"""
        metrics = {}

        try:
            with open(file_path, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Extract metrics from CSV rows
                    for column, value in row.items():
                        try:
                            numeric_value = float(value)
                            metrics[f"offline_{column}"] = [
                                MetricData(
                                    timestamp=timestamp,
                                    value=numeric_value,
                                    metadata={
                                        "source": self.name,
                                        "file_path": str(file_path),
                                        "offline": True,
                                        "csv_column": column,
                                    },
                                )
                            ]
                        except (ValueError, TypeError):
                            # Skip non-numeric values
                            continue

        except Exception as e:
            self.logger.error(f"Failed to parse CSV file {file_path}: {e}")

        return metrics

    def _collect_from_database(
        self, db_source: str, timestamp: datetime
    ) -> Dict[str, List[MetricData]]:
        """Collect data from database"""
        metrics = {}

        try:
            # This would connect to database and execute queries
            # For now, return empty metrics
            self.logger.info(f"Database collection not implemented for {db_source}")

        except Exception as e:
            self.logger.error(f"Failed to collect from database {db_source}: {e}")

        return metrics

    def get_collector_info(self) -> Dict[str, Any]:
        """Get detailed information about this collector"""
        info = super().get_collector_info()
        info.update(
            {
                "data_sources": self.data_sources,
                "file_patterns": self.file_patterns,
                "log_paths": self.log_paths,
                "database_config": self.database_config,
                "parsing_rules": self.parsing_rules,
            }
        )
        return info
