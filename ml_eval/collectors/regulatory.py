"""Regulatory compliance monitoring for Industrial AI systems"""

from typing import Dict, List, Any
from datetime import datetime
import logging
import json
import os

from .base import BaseCollector
from ..core.config import MetricData


class RegulatoryCollector(BaseCollector):
    """Regulatory compliance monitoring for Industrial AI systems"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.compliance_standards = config.get("compliance_standards", [])
        self.audit_log_path = config.get("audit_log_path")
        self.compliance_endpoints = config.get("compliance_endpoints", {})
        self.audit_interval = config.get("audit_interval", 3600)  # seconds

    def get_required_config_fields(self) -> List[str]:
        return ["compliance_standards"]

    def collect(self) -> Dict[str, List[MetricData]]:
        """Collect compliance-related metrics and audit data"""
        try:
            if not self.health_check():
                self.logger.warning(f"Compliance monitoring health check failed for {self.name}")
                return {}

            return self._collect_compliance_data()
        except Exception as e:
            self.logger.error(f"Failed to collect compliance data from {self.name}: {e}")
            return {}

    def health_check(self) -> bool:
        """Check if compliance monitoring systems are operational"""
        try:
            # Check audit log accessibility
            if self.audit_log_path and not os.path.exists(self.audit_log_path):
                self.logger.warning(f"Audit log path does not exist: {self.audit_log_path}")
                return False
                
            # Check compliance endpoints
            for standard, endpoint in self.compliance_endpoints.items():
                if not self._check_compliance_endpoint(endpoint):
                    self.logger.warning(f"Compliance endpoint not reachable: {endpoint}")
                    return False
                    
            return True
        except Exception as e:
            self.logger.error(f"Compliance health check failed: {e}")
            return False

    def _collect_compliance_data(self) -> Dict[str, List[MetricData]]:
        """Collect compliance metrics and audit trail data"""
        metrics = {}
        timestamp = datetime.now()
        
        # Collect compliance metrics for each standard
        for standard in self.compliance_standards:
            try:
                compliance_metrics = self._collect_standard_metrics(standard)
                metrics.update(compliance_metrics)
            except Exception as e:
                self.logger.error(f"Failed to collect metrics for standard {standard}: {e}")
                continue
                
        # Collect audit trail data
        audit_metrics = self._collect_audit_data()
        metrics.update(audit_metrics)
        
        return metrics

    def _collect_standard_metrics(self, standard: str) -> Dict[str, List[MetricData]]:
        """Collect metrics for a specific compliance standard"""
        metrics = {}
        timestamp = datetime.now()
        
        if standard in self.compliance_endpoints:
            # Collect from compliance endpoint
            endpoint_metrics = self._collect_from_endpoint(standard, self.compliance_endpoints[standard])
            metrics.update(endpoint_metrics)
        else:
            # Generate compliance metrics based on standard requirements
            standard_metrics = self._generate_standard_metrics(standard)
            metrics.update(standard_metrics)
            
        return metrics

    def _collect_from_endpoint(self, standard: str, endpoint: str) -> Dict[str, List[MetricData]]:
        """Collect compliance data from configured endpoint"""
        metrics = {}
        timestamp = datetime.now()
        
        try:
            import requests
            response = requests.get(endpoint, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Process compliance metrics
            for metric_name, value in data.items():
                if isinstance(value, (int, float)):
                    metrics[f"compliance_{standard}_{metric_name}"] = [
                        MetricData(
                            timestamp=timestamp,
                            value=float(value),
                            metadata={
                                "source": self.name,
                                "compliance_standard": standard,
                                "endpoint": endpoint
                            },
                            compliance_context={
                                "standard": standard,
                                "metric_type": metric_name,
                                "compliance_level": self._assess_compliance_level(standard, metric_name, value)
                            }
                        )
                    ]
                    
        except Exception as e:
            self.logger.error(f"Failed to collect from compliance endpoint {endpoint}: {e}")
            
        return metrics

    def _generate_standard_metrics(self, standard: str) -> Dict[str, List[MetricData]]:
        """Generate compliance metrics based on standard requirements"""
        metrics = {}
        timestamp = datetime.now()
        
        # Define compliance metrics for different standards
        standard_requirements = {
            "DO-178C": {
                "safety_level": 1.0,
                "documentation_completeness": 0.95,
                "test_coverage": 0.90,
                "code_quality": 0.85
            },
            "ISO-26262": {
                "asil_level": 1.0,
                "safety_mechanisms": 0.95,
                "fault_tolerance": 0.90
            },
            "IEC-61508": {
                "sil_level": 1.0,
                "safety_integrity": 0.95,
                "reliability": 0.90
            },
            "FDA-510K": {
                "clinical_validation": 0.95,
                "safety_assessment": 0.90,
                "regulatory_compliance": 0.85
            },
            "SOX": {
                "financial_accuracy": 0.99,
                "audit_trail": 0.95,
                "data_integrity": 0.90
            },
            "GDPR": {
                "data_protection": 0.95,
                "privacy_compliance": 0.90,
                "consent_management": 0.85
            }
        }
        
        if standard in standard_requirements:
            requirements = standard_requirements[standard]
            for metric_name, target_value in requirements.items():
                # Simulate compliance level (replace with actual compliance assessment)
                compliance_level = self._simulate_compliance_level(target_value)
                
                metrics[f"compliance_{standard}_{metric_name}"] = [
                    MetricData(
                        timestamp=timestamp,
                        value=compliance_level,
                        metadata={
                            "source": self.name,
                            "compliance_standard": standard,
                            "target": target_value
                        },
                        compliance_context={
                            "standard": standard,
                            "metric_type": metric_name,
                            "target_value": target_value,
                            "compliance_level": self._assess_compliance_level(standard, metric_name, compliance_level)
                        }
                    )
                ]
                
        return metrics

    def _simulate_compliance_level(self, target_value: float) -> float:
        """Simulate compliance level for development/testing"""
        import random
        
        # Generate compliance level around target value with some variance
        variance = 0.05  # 5% variance
        min_val = max(0.0, target_value - variance)
        max_val = min(1.0, target_value + variance)
        
        return random.uniform(min_val, max_val)

    def _assess_compliance_level(self, standard: str, metric_name: str, value: float) -> str:
        """Assess compliance level based on metric value"""
        if value >= 0.95:
            return "compliant"
        elif value >= 0.85:
            return "warning"
        else:
            return "non_compliant"

    def _collect_audit_data(self) -> Dict[str, List[MetricData]]:
        """Collect audit trail data"""
        metrics = {}
        timestamp = datetime.now()
        
        if self.audit_log_path and os.path.exists(self.audit_log_path):
            try:
                audit_metrics = self._parse_audit_log()
                metrics.update(audit_metrics)
            except Exception as e:
                self.logger.error(f"Failed to parse audit log: {e}")
                
        return metrics

    def _parse_audit_log(self) -> Dict[str, List[MetricData]]:
        """Parse audit log for compliance metrics"""
        metrics = {}
        timestamp = datetime.now()
        
        try:
            with open(self.audit_log_path, 'r') as f:
                audit_entries = f.readlines()
                
            # Count different types of audit events
            event_counts = {}
            for entry in audit_entries:
                if "compliance" in entry.lower():
                    event_type = "compliance_check"
                elif "audit" in entry.lower():
                    event_type = "audit_event"
                elif "violation" in entry.lower():
                    event_type = "compliance_violation"
                else:
                    event_type = "other"
                    
                event_counts[event_type] = event_counts.get(event_type, 0) + 1
                
            # Create metrics from audit data
            for event_type, count in event_counts.items():
                metrics[f"audit_{event_type}_count"] = [
                    MetricData(
                        timestamp=timestamp,
                        value=float(count),
                        metadata={
                            "source": self.name,
                            "audit_log": self.audit_log_path
                        },
                        compliance_context={
                            "audit_event_type": event_type,
                            "total_events": len(audit_entries)
                        }
                    )
                ]
                
        except Exception as e:
            self.logger.error(f"Failed to parse audit log {self.audit_log_path}: {e}")
            
        return metrics

    def _check_compliance_endpoint(self, endpoint: str) -> bool:
        """Check if compliance endpoint is reachable"""
        try:
            import requests
            response = requests.get(endpoint, timeout=10)
            return response.status_code == 200
        except Exception:
            return False

    def get_collector_info(self) -> Dict[str, Any]:
        """Get detailed information about this collector"""
        info = super().get_collector_info()
        info.update({
            "compliance_standards": self.compliance_standards,
            "audit_log_path": self.audit_log_path,
            "compliance_endpoints": self.compliance_endpoints,
            "audit_interval": self.audit_interval,
        })
        return info 