"""Historical data collection for Industrial AI systems"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
import logging
import os
import json
import csv
from pathlib import Path

from .base import BaseCollector
from ..core.config import MetricData


class OfflineCollector(BaseCollector):
    """Historical data collection from logs and databases"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.log_paths = config.get("log_paths", [])
        self.data_format = config.get("data_format", "json")  # json, csv, log
        self.time_window = config.get("time_window", "24h")
        self.encoding = config.get("encoding", "utf-8")

    def get_required_config_fields(self) -> List[str]:
        return ["log_paths"]

    def collect(self) -> Dict[str, List[MetricData]]:
        """Collect historical metrics from logs/databases"""
        try:
            if not self.health_check():
                self.logger.warning(f"Health check failed for {self.name}")
                return {}

            return self._parse_historical_data()
        except Exception as e:
            self.logger.error(f"Failed to collect historical data from {self.name}: {e}")
            return {}

    def health_check(self) -> bool:
        """Check if data sources are accessible"""
        for path in self.log_paths:
            if not os.path.exists(path):
                self.logger.warning(f"Data source path does not exist: {path}")
                return False
        return True

    def _parse_historical_data(self) -> Dict[str, List[MetricData]]:
        """Parse historical data from configured sources"""
        all_metrics = {}
        
        for path in self.log_paths:
            try:
                metrics = self._parse_single_source(path)
                all_metrics.update(metrics)
            except Exception as e:
                self.logger.error(f"Failed to parse data from {path}: {e}")
                continue
                
        return all_metrics

    def _parse_single_source(self, path: str) -> Dict[str, List[MetricData]]:
        """Parse a single data source"""
        if self.data_format == "json":
            return self._parse_json_file(path)
        elif self.data_format == "csv":
            return self._parse_csv_file(path)
        elif self.data_format == "log":
            return self._parse_log_file(path)
        else:
            self.logger.warning(f"Unsupported data format: {self.data_format}")
            return {}

    def _parse_json_file(self, path: str) -> Dict[str, List[MetricData]]:
        """Parse JSON-formatted historical data"""
        metrics = {}
        
        try:
            with open(path, 'r', encoding=self.encoding) as f:
                data = json.load(f)
                
            # Handle different JSON structures
            if isinstance(data, list):
                # List of metric records
                for record in data:
                    self._process_metric_record(record, metrics)
            elif isinstance(data, dict):
                # Single record or nested structure
                self._process_metric_record(data, metrics)
                
        except Exception as e:
            self.logger.error(f"Failed to parse JSON file {path}: {e}")
            
        return metrics

    def _parse_csv_file(self, path: str) -> Dict[str, List[MetricData]]:
        """Parse CSV-formatted historical data"""
        metrics = {}
        
        try:
            with open(path, 'r', encoding=self.encoding) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self._process_csv_row(row, metrics)
                    
        except Exception as e:
            self.logger.error(f"Failed to parse CSV file {path}: {e}")
            
        return metrics

    def _parse_log_file(self, path: str) -> Dict[str, List[MetricData]]:
        """Parse log-formatted historical data"""
        metrics = {}
        
        try:
            with open(path, 'r', encoding=self.encoding) as f:
                for line in f:
                    self._process_log_line(line, metrics)
                    
        except Exception as e:
            self.logger.error(f"Failed to parse log file {path}: {e}")
            
        return metrics

    def _process_metric_record(self, record: Dict[str, Any], metrics: Dict[str, List[MetricData]]):
        """Process a single metric record"""
        if not isinstance(record, dict):
            return
            
        # Extract timestamp and value
        timestamp_str = record.get("timestamp")
        if timestamp_str:
            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            except ValueError:
                timestamp = datetime.now()
        else:
            timestamp = datetime.now()
            
        # Process all numeric fields as metrics
        for key, value in record.items():
            if key != "timestamp" and isinstance(value, (int, float)):
                if key not in metrics:
                    metrics[key] = []
                    
                metrics[key].append(
                    MetricData(
                        timestamp=timestamp,
                        value=float(value),
                        metadata={
                            "source": self.name,
                            "file": str(Path(record.get("file", ""))),
                            "format": "json"
                        }
                    )
                )

    def _process_csv_row(self, row: Dict[str, str], metrics: Dict[str, List[MetricData]]):
        """Process a single CSV row"""
        # Look for timestamp column
        timestamp_col = None
        for col in row.keys():
            if "time" in col.lower() or "date" in col.lower():
                timestamp_col = col
                break
                
        timestamp = datetime.now()
        if timestamp_col:
            try:
                timestamp = datetime.fromisoformat(row[timestamp_col].replace('Z', '+00:00'))
            except ValueError:
                pass
                
        # Process all numeric columns as metrics
        for key, value in row.items():
            if key != timestamp_col:
                try:
                    float_val = float(value)
                    if key not in metrics:
                        metrics[key] = []
                        
                    metrics[key].append(
                        MetricData(
                            timestamp=timestamp,
                            value=float_val,
                            metadata={
                                "source": self.name,
                                "format": "csv"
                            }
                        )
                    )
                except (ValueError, TypeError):
                    continue

    def _process_log_line(self, line: str, metrics: Dict[str, List[MetricData]]):
        """Process a single log line"""
        # Simple log parsing - extract metrics from structured logs
        # This is a basic implementation - can be extended for specific log formats
        
        # Look for metric patterns like "metric_name=value"
        import re
        metric_pattern = r'(\w+)=([0-9]+\.?[0-9]*)'
        matches = re.findall(metric_pattern, line)
        
        timestamp = datetime.now()
        
        for metric_name, value in matches:
            try:
                float_val = float(value)
                if metric_name not in metrics:
                    metrics[metric_name] = []
                    
                metrics[metric_name].append(
                    MetricData(
                        timestamp=timestamp,
                        value=float_val,
                        metadata={
                            "source": self.name,
                            "format": "log",
                            "line": line.strip()
                        }
                    )
                )
            except ValueError:
                continue

    def get_collector_info(self) -> Dict[str, Any]:
        """Get detailed information about this collector"""
        info = super().get_collector_info()
        info.update({
            "log_paths": self.log_paths,
            "data_format": self.data_format,
            "time_window": self.time_window,
            "encoding": self.encoding,
        })
        return info 