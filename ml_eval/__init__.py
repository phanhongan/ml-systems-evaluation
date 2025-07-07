"""ML Systems Evaluation Framework - Industrial AI Reliability Assessment

A reliability-focused evaluation framework for Industrial AI systems, applying
Site Reliability Engineering (SRE) principles to machine learning evaluation.

This framework is designed for system engineers working with safety-critical
and business-critical ML systems in industrial environments.
"""

# CLI interface
# Autonomous agents (future implementation)
from .agents.alerting import AlertingAgent
from .agents.monitoring import MonitoringAgent
from .agents.scheduling import SchedulingAgent
from .cli.main import cli as cli_main

# Data collection
from .collectors.base import BaseCollector
from .collectors.environmental import EnvironmentalCollector
from .collectors.offline import OfflineCollector
from .collectors.online import OnlineCollector
from .collectors.regulatory import RegulatoryCollector
from .core.config import ErrorBudget, EvaluationResult, SLOConfig

# Core framework components
from .core.framework import EvaluationFramework
from .core.types import ComplianceStandard, CriticalityLevel

# Evaluation engines
from .evaluators.base import BaseEvaluator
from .evaluators.compliance import ComplianceEvaluator
from .evaluators.drift import DriftEvaluator
from .evaluators.performance import PerformanceEvaluator
from .evaluators.reliability import ReliabilityEvaluator
from .evaluators.safety import SafetyEvaluator
from .examples.registry import ExampleRegistry

# LLM integration layer
from .llm.analysis import LLMAnalysisEngine
from .llm.assistant import LLMAssistantEngine
from .llm.enhancement import LLMEnhancementEngine
from .llm.providers import LLMProvider

# Reporting
from .reports.base import BaseReport
from .reports.business import BusinessImpactReport
from .reports.compliance import ComplianceReport
from .reports.reliability import ReliabilityReport
from .reports.safety import SafetyReport

# Templates and examples
from .templates.factory import TemplateFactory

__version__ = "0.1.0"
__author__ = "ML Systems Evaluation Team"
__description__ = "Industrial AI Reliability Assessment Framework"

# Public API for system engineers
__all__ = [
    "AlertingAgent",
    "BaseCollector",
    "BaseEvaluator",
    "BaseReport",
    "BusinessImpactReport",
    "ComplianceEvaluator",
    "ComplianceReport",
    "ComplianceStandard",
    "CriticalityLevel",
    "DriftEvaluator",
    "EnvironmentalCollector",
    "ErrorBudget",
    "EvaluationFramework",
    "EvaluationResult",
    "ExampleRegistry",
    "LLMAnalysisEngine",
    "LLMAssistantEngine",
    "LLMEnhancementEngine",
    "LLMProvider",
    "MonitoringAgent",
    "OfflineCollector",
    "OnlineCollector",
    "PerformanceEvaluator",
    "RegulatoryCollector",
    "ReliabilityEvaluator",
    "ReliabilityReport",
    "SLOConfig",
    "SafetyEvaluator",
    "SafetyReport",
    "SchedulingAgent",
    "TemplateFactory",
    "cli_main",
]
