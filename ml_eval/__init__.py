"""ML Systems Evaluation Framework - Industrial AI Reliability Assessment

A reliability-focused evaluation framework for Industrial AI systems, applying 
Site Reliability Engineering (SRE) principles to machine learning evaluation.

This framework is designed for system engineers working with safety-critical
and business-critical ML systems in industrial environments.
"""

# Core framework components
from .core.framework import EvaluationFramework
from .core.config import SLOConfig, ErrorBudget, EvaluationResult
from .core.types import SystemType, CriticalityLevel, ComplianceStandard

# Data collection
from .collectors.base import BaseCollector
from .collectors.online import OnlineCollector
from .collectors.offline import OfflineCollector
from .collectors.environmental import EnvironmentalCollector
from .collectors.regulatory import RegulatoryCollector

# Evaluation engines
from .evaluators.base import BaseEvaluator
from .evaluators.reliability import ReliabilityEvaluator
from .evaluators.safety import SafetyEvaluator
from .evaluators.performance import PerformanceEvaluator
from .evaluators.compliance import ComplianceEvaluator
from .evaluators.drift import DriftEvaluator

# Reporting
from .reports.base import BaseReport
from .reports.reliability import ReliabilityReport
from .reports.safety import SafetyReport
from .reports.compliance import ComplianceReport
from .reports.business import BusinessImpactReport

# Templates and examples
from .templates.factory import TemplateFactory
from .examples.registry import ExampleRegistry

# CLI interface
from .cli.main import main as cli_main

__version__ = "0.1.0"
__author__ = "ML Systems Evaluation Team"
__description__ = "Industrial AI Reliability Assessment Framework"

# Public API for system engineers
__all__ = [
    # Core framework
    "EvaluationFramework",
    "SLOConfig", 
    "ErrorBudget",
    "EvaluationResult",
    "SystemType",
    "CriticalityLevel", 
    "ComplianceStandard",
    
    # Collectors
    "BaseCollector",
    "OnlineCollector",
    "OfflineCollector", 
    "EnvironmentalCollector",
    "RegulatoryCollector",
    
    # Evaluators
    "BaseEvaluator",
    "ReliabilityEvaluator",
    "SafetyEvaluator",
    "PerformanceEvaluator", 
    "ComplianceEvaluator",
    "DriftEvaluator",
    
    # Reports
    "BaseReport",
    "ReliabilityReport",
    "SafetyReport",
    "ComplianceReport",
    "BusinessImpactReport",
    
    # Utilities
    "TemplateFactory",
    "ExampleRegistry",
    "cli_main",
]