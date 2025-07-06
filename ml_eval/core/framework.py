"""Main evaluation framework for Industrial AI systems"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

import logging

from .config import SLOConfig, ErrorBudget, EvaluationResult, MetricData
from .types import SystemType, CriticalityLevel


class EvaluationFramework:
    """Main framework orchestrating evaluation process for Industrial AI systems"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.system_name = config.get("system", {}).get("name", "Unknown")
        self.system_type = SystemType(config.get("system", {}).get("type", "single_model"))
        self.criticality = CriticalityLevel(config.get("system", {}).get("criticality", "operational"))
        self.slos = self._parse_slos(config.get("slos", {}))
        self.collectors = []
        self.evaluators = []
        self.logger = logging.getLogger(__name__)

    def _parse_slos(self, slos_config: Dict[str, Any]) -> List[SLOConfig]:
        """Parse SLO configuration into objects for Industrial AI systems"""
        slos = []
        for name, config in slos_config.items():
            try:
                slo = SLOConfig(
                    name=name,
                    target=config.get("target", 0.95),
                    window=config.get("window", "30d"),
                    error_budget=config.get("error_budget", 0.05),
                    description=config.get("description", ""),
                    compliance_standard=config.get("compliance_standard"),
                    safety_critical=config.get("safety_critical", False),
                    business_impact=config.get("business_impact"),
                    environmental_conditions=config.get("environmental_conditions"),
                )
                slos.append(slo)
            except ValueError as e:
                self.logger.error(f"Invalid SLO configuration for '{name}': {e}")
                raise

        return slos

    def add_collector(self, collector):
        """Add a metric collector to the framework"""
        self.collectors.append(collector)
        self.logger.info(f"Added collector: {collector.__class__.__name__}")

    def add_evaluator(self, evaluator):
        """Add an evaluator to the framework"""
        self.evaluators.append(evaluator)
        self.logger.info(f"Added evaluator: {evaluator.__class__.__name__}")

    def evaluate(self) -> EvaluationResult:
        """Run complete evaluation pipeline for Industrial AI systems"""
        self.logger.info(f"Starting evaluation for system: {self.system_name}")
        
        try:
            metrics = self._collect_all_metrics()
            results = self._run_all_evaluations(metrics)
            evaluation_result = self._build_result(results)
            
            # Log critical findings
            if evaluation_result.has_critical_violations:
                self.logger.critical(
                    f"Critical violations detected in system: {self.system_name}"
                )
            
            if evaluation_result.requires_emergency_shutdown:
                self.logger.critical(
                    f"Emergency shutdown required for system: {self.system_name}"
                )
            
            return evaluation_result
            
        except Exception as e:
            self.logger.error(f"Evaluation failed for system {self.system_name}: {e}")
            raise

    def _collect_all_metrics(self) -> Dict[str, List[MetricData]]:
        """Collect metrics from all collectors with error handling"""
        all_metrics = {}
        
        for collector in self.collectors:
            try:
                metrics = collector.collect()
                all_metrics.update(metrics)
                self.logger.debug(f"Collected {len(metrics)} metrics from {collector.__class__.__name__}")
            except Exception as e:
                self.logger.error(f"Failed to collect metrics from {collector.__class__.__name__}: {e}")
                # Continue with other collectors for resilience
                continue
                
        return all_metrics

    def _run_all_evaluations(
        self, metrics: Dict[str, List[MetricData]]
    ) -> List[Dict[str, Any]]:
        """Run all evaluators with error handling"""
        results = []
        
        for evaluator in self.evaluators:
            try:
                result = evaluator.evaluate(metrics, self.slos)
                results.append(result)
                self.logger.debug(f"Completed evaluation with {evaluator.__class__.__name__}")
            except Exception as e:
                self.logger.error(f"Failed to run evaluator {evaluator.__class__.__name__}: {e}")
                # Continue with other evaluators for resilience
                continue
                
        return results

    def _build_result(
        self, evaluation_results: List[Dict[str, Any]]
    ) -> EvaluationResult:
        """Build final evaluation result for Industrial AI systems"""
        # Aggregate results from all evaluators
        slo_compliance = {}
        error_budgets = {}
        incidents = []
        recommendations = []
        safety_violations = []
        regulatory_violations = []
        environmental_alerts = []
        business_impact_assessment = {}

        for result in evaluation_results:
            slo_compliance.update(result.get("slo_compliance", {}))
            error_budgets.update(result.get("error_budgets", {}))
            incidents.extend(result.get("incidents", []))
            recommendations.extend(result.get("recommendations", []))
            
            # Industrial AI specific aggregations
            safety_violations.extend(result.get("safety_violations", []))
            regulatory_violations.extend(result.get("regulatory_violations", []))
            environmental_alerts.extend(result.get("environmental_alerts", []))
            
            # Merge business impact assessments
            business_impact_assessment.update(result.get("business_impact_assessment", {}))

        return EvaluationResult(
            system_name=self.system_name,
            evaluation_time=datetime.now(),
            slo_compliance=slo_compliance,
            error_budgets=error_budgets,
            incidents=incidents,
            recommendations=recommendations,
            safety_violations=safety_violations,
            regulatory_violations=regulatory_violations,
            environmental_alerts=environmental_alerts,
            business_impact_assessment=business_impact_assessment,
        )

    def validate_configuration(self) -> bool:
        """Validate framework configuration for industrial requirements"""
        errors = []
        
        # Check for safety-critical systems
        if self.criticality == CriticalityLevel.SAFETY_CRITICAL:
            safety_slos = [slo for slo in self.slos if slo.safety_critical]
            if not safety_slos:
                errors.append("Safety-critical system must have at least one safety-critical SLO")
        
        # Check for compliance standards
        compliance_slos = [slo for slo in self.slos if slo.compliance_standard]
        if compliance_slos and not any(collector.__class__.__name__ == "RegulatoryCollector" 
                                     for collector in self.collectors):
            errors.append("System with compliance standards should include RegulatoryCollector")
        
        # Check for environmental monitoring
        environmental_slos = [slo for slo in self.slos if slo.environmental_conditions]
        if environmental_slos and not any(collector.__class__.__name__ == "EnvironmentalCollector" 
                                        for collector in self.collectors):
            errors.append("System with environmental conditions should include EnvironmentalCollector")
        
        if errors:
            for error in errors:
                self.logger.error(f"Configuration validation error: {error}")
            return False
            
        return True

    def get_system_summary(self) -> Dict[str, Any]:
        """Get a summary of the system configuration"""
        return {
            "name": self.system_name,
            "type": self.system_type.value,
            "criticality": self.criticality.value,
            "slo_count": len(self.slos),
            "safety_critical_slos": len([slo for slo in self.slos if slo.safety_critical]),
            "compliance_standards": list(set(slo.compliance_standard for slo in self.slos if slo.compliance_standard)),
            "collector_count": len(self.collectors),
            "evaluator_count": len(self.evaluators),
        } 