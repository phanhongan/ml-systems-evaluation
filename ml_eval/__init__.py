"""ML Systems Evaluation Framework - Industrial AI Reliability Assessment"""

from .core import EvaluationFramework, SLOConfig, ErrorBudget, EvaluationResult
from .collectors import BaseCollector, OnlineCollector, OfflineCollector
from .evaluators import BaseEvaluator, ReliabilityEvaluator, PerformanceEvaluator
from .reports import BaseReport, ReliabilityReport

__version__ = "0.1.0"