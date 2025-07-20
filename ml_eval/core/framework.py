"""Main evaluation framework for Industrial AI systems"""

from datetime import datetime
from typing import Any

from .config import EvaluationResult, MetricData, SLOConfig
from .types import CriticalityLevel
from .workflow import EvaluationWorkflow
from .workflow_templates import WorkflowTemplateFactory


class EvaluationFramework:
    """Main framework orchestrating evaluation process for Industrial AI systems"""

    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.system_name = config.get("system", {}).get("name", "Unknown")
        self.criticality = CriticalityLevel(
            config.get("system", {}).get("criticality", "operational")
        )
        self.slos = self._parse_slos(config.get("slos", {}))
        self.collectors: list[Any] = []
        self.evaluators: list[Any] = []

        # Workflow configuration
        self.use_workflow = config.get("workflow", {}).get("enabled", False)
        self.workflow_type = config.get("workflow", {}).get("type", "standard")
        self.workflow_engine = None

        if self.use_workflow:
            self._setup_workflow_engine()

        # Automatically create collectors and evaluators from config
        self._create_components_from_config()

    def _setup_workflow_engine(self):
        """Setup workflow engine based on configuration"""
        industry = self.config.get("system", {}).get("industry", "custom")

        if self.workflow_type == "standard":
            self.workflow_engine = EvaluationWorkflow(self.config)
        else:
            # Use industry-specific workflow templates
            self.workflow_engine = WorkflowTemplateFactory.create_workflow(
                industry=industry, workflow_type=self.workflow_type, config=self.config
            )

    def _parse_slos(self, slos_config: dict[str, Any]) -> list[SLOConfig]:
        """Parse SLO configuration into objects for Industrial AI systems"""
        slos = []
        for name, config in slos_config.items():
            try:
                # Convert target to float, handle invalid values gracefully
                target = config.get("target", 0.95)
                if isinstance(target, str):
                    try:
                        target = float(target)
                    except ValueError:
                        continue  # Skip this SLO instead of raising

                slo = SLOConfig(
                    name=name,
                    target=target,
                    window=config.get("window", "30d"),
                    description=config.get("description", ""),
                    safety_critical=config.get("safety_critical", False),
                )
                slos.append(slo)
            except ValueError:
                # Continue with other SLOs instead of raising
                pass

        return slos

    def _create_components_from_config(self) -> None:
        """Create collectors and evaluators from configuration"""
        # Create collectors
        collectors_config = self.config.get("collectors", [])
        print(f"Creating {len(collectors_config)} collectors from config")
        for i, collector_config in enumerate(collectors_config):
            try:
                collector = self._create_collector(collector_config)
                if collector:
                    self.collectors.append(collector)
                    print(f"Created collector {i + 1}: {collector.__class__.__name__}")
                else:
                    print(
                        f"Failed to create collector {i + 1}: "
                        f"{collector_config.get('type', 'unknown')}"
                    )
            except Exception:
                print(
                    f"Failed to create collector {i + 1}: "
                    f"{collector_config.get('type', 'unknown')}"
                )

        # Create evaluators
        evaluators_config = self.config.get("evaluators", [])
        print(f"Creating {len(evaluators_config)} evaluators from config")
        for i, evaluator_config in enumerate(evaluators_config):
            try:
                evaluator = self._create_evaluator(evaluator_config)
                if evaluator:
                    self.evaluators.append(evaluator)
                    print(f"Created evaluator {i + 1}: {evaluator.__class__.__name__}")
                else:
                    print(
                        f"Failed to create evaluator {i + 1}: "
                        f"{evaluator_config.get('type', 'unknown')}"
                    )
            except Exception as e:
                print(
                    f"Failed to create evaluator {i + 1}: "
                    f"{evaluator_config.get('type', 'unknown')} - Error: {e}"
                )

    def _create_collector(self, config: dict[str, Any]) -> Any | None:
        """Create a collector instance from configuration"""
        collector_type = config.get("type", "")

        if collector_type == "online":
            from ..collectors.online import OnlineCollector

            return OnlineCollector(config)
        elif collector_type == "offline":
            from ..collectors.offline import OfflineCollector

            return OfflineCollector(config)
        elif collector_type == "environmental":
            from ..collectors.environmental import EnvironmentalCollector

            return EnvironmentalCollector(config)
        elif collector_type == "regulatory":
            from ..collectors.regulatory import RegulatoryCollector

            return RegulatoryCollector(config)
        else:
            print(f"Unknown collector type: {collector_type}")
            return None

    def _create_evaluator(self, config: dict[str, Any]) -> Any | None:
        """Create an evaluator instance from configuration"""
        evaluator_type = config.get("type", "")
        evaluator_config = config.get(
            "config", config
        )  # Use config field or fallback to entire config

        if evaluator_type == "reliability":
            from ..evaluators.reliability import ReliabilityEvaluator

            return ReliabilityEvaluator(evaluator_config)
        elif evaluator_type == "performance":
            from ..evaluators.performance import PerformanceEvaluator

            return PerformanceEvaluator(evaluator_config)
        elif evaluator_type == "safety":
            from ..evaluators.safety import SafetyEvaluator

            return SafetyEvaluator(evaluator_config)
        elif evaluator_type == "compliance":
            from ..evaluators.compliance import ComplianceEvaluator

            return ComplianceEvaluator(evaluator_config)
        elif evaluator_type == "drift":
            from ..evaluators.drift import DriftEvaluator

            return DriftEvaluator(evaluator_config)
        elif evaluator_type == "interpretability":
            from ..evaluators.interpretability import InterpretabilityEvaluator

            return InterpretabilityEvaluator(evaluator_config)
        elif evaluator_type == "edge_case":
            from ..evaluators.edge_case import EdgeCaseEvaluator

            return EdgeCaseEvaluator(evaluator_config)
        else:
            print(f"Unknown evaluator type: {evaluator_type}")
            return None

    def add_collector(self, collector: Any) -> None:
        """Add a metric collector to the framework"""
        self.collectors.append(collector)

    def add_evaluator(self, evaluator: Any) -> None:
        """Add an evaluator to the framework"""
        self.evaluators.append(evaluator)

    def evaluate(self) -> EvaluationResult:
        """Run complete evaluation pipeline for Industrial AI systems"""

        if self.use_workflow and self.workflow_engine:
            return self._evaluate_with_workflow()
        else:
            return self._evaluate_simple()

    async def evaluate_async(self) -> EvaluationResult:
        """Run complete evaluation pipeline asynchronously"""

        if self.use_workflow and self.workflow_engine:
            return await self._evaluate_with_workflow_async()
        else:
            return self._evaluate_simple()

    def _evaluate_simple(self) -> EvaluationResult:
        """Run simple evaluation pipeline (backward compatibility)"""
        try:
            metrics = self._collect_all_metrics()
            results = self._run_all_evaluations(metrics)
            evaluation_result = self._build_result(results)

            return evaluation_result

        except Exception:
            raise

    def _evaluate_with_workflow(self) -> EvaluationResult:
        """Run evaluation using workflow engine"""
        try:
            # Execute workflow synchronously
            import asyncio

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                if self.workflow_engine is not None:
                    workflow_result = loop.run_until_complete(
                        self.workflow_engine.execute()
                    )
                else:
                    raise RuntimeError("Workflow engine not initialized")
            finally:
                loop.close()

            # Convert workflow result to EvaluationResult
            return self._convert_workflow_result(workflow_result)

        except Exception as e:
            print(f"Workflow evaluation failed: {e}")
            # Fallback to simple evaluation
            return self._evaluate_simple()

    async def _evaluate_with_workflow_async(self) -> EvaluationResult:
        """Run evaluation using workflow engine asynchronously"""
        try:
            if self.workflow_engine is not None:
                workflow_result = await self.workflow_engine.execute()
            else:
                raise RuntimeError("Workflow engine not initialized")
            return self._convert_workflow_result(workflow_result)

        except Exception as e:
            print(f"Workflow evaluation failed: {e}")
            # Fallback to simple evaluation
            return self._evaluate_simple()

    def _convert_workflow_result(
        self, workflow_result: dict[str, Any]
    ) -> EvaluationResult:
        """Convert workflow result to EvaluationResult"""
        # Extract results from workflow context
        results = workflow_result.get("results", {})

        # Determine overall status
        has_critical_violations = any(
            result.get("critical_violations", False)
            or ("safety_violations" in result and result["safety_violations"])
            for result in results.values()
        )

        requires_emergency_shutdown = any(
            result.get("emergency_shutdown", False) for result in results.values()
        )

        # Calculate overall compliance score
        compliance_scores = [
            result.get("compliance_score", 0.0) for result in results.values()
        ]
        overall_compliance = (
            sum(compliance_scores) / len(compliance_scores)
            if compliance_scores
            else 0.0
        )

        # Build recommendations and alerts
        recommendations = []
        alerts = []
        for _evaluator_name, result in results.items():
            if result.get("recommendations"):
                recommendations.extend(result["recommendations"])
            if result.get("alerts"):
                alerts.extend(result["alerts"])

        return EvaluationResult(
            system_name=self.system_name,
            timestamp=datetime.now(),
            overall_compliance=overall_compliance,
            has_critical_violations=has_critical_violations,
            requires_emergency_shutdown=requires_emergency_shutdown,
            evaluator_results=results,
            recommendations=recommendations,
            alerts=alerts,
        )

    def _collect_all_metrics(self) -> dict[str, list[MetricData]]:
        """Collect metrics from all collectors with error handling"""
        all_metrics = {}

        for collector in self.collectors:
            try:
                metrics = collector.collect()
                all_metrics.update(metrics)
            except Exception:
                # Log error but continue with other collectors
                pass

        return all_metrics

    def _run_all_evaluations(
        self, metrics: dict[str, list[MetricData]]
    ) -> dict[str, Any]:
        """Run all evaluators on collected metrics"""
        results = {}

        for evaluator in self.evaluators:
            try:
                result = evaluator.evaluate(metrics)
                results[evaluator.__class__.__name__] = result
            except Exception:
                # Log error but continue with other evaluators
                pass

        return results

    def _build_result(self, results: dict[str, Any]) -> EvaluationResult:
        """Build final evaluation result from all evaluator results"""
        # Determine overall system status
        has_critical_violations = any(
            result.get("critical_violations", False)
            or ("safety_violations" in result and result["safety_violations"])
            for result in results.values()
        )

        requires_emergency_shutdown = any(
            result.get("emergency_shutdown", False) for result in results.values()
        )

        # Calculate overall compliance score
        compliance_scores = [
            result.get("compliance_score", 0.0) for result in results.values()
        ]
        overall_compliance = (
            sum(compliance_scores) / len(compliance_scores)
            if compliance_scores
            else 0.0
        )

        # Build recommendations
        recommendations = []
        for _evaluator_name, result in results.items():
            if result.get("recommendations"):
                recommendations.extend(result["recommendations"])

        # Build alerts
        alerts = []
        for _evaluator_name, result in results.items():
            if result.get("alerts"):
                alerts.extend(result["alerts"])

        return EvaluationResult(
            system_name=self.system_name,
            timestamp=datetime.now(),
            overall_compliance=overall_compliance,
            has_critical_violations=has_critical_violations,
            requires_emergency_shutdown=requires_emergency_shutdown,
            evaluator_results=results,
            recommendations=recommendations,
            alerts=alerts,
        )

    def get_system_info(self) -> dict[str, Any]:
        """Get information about the configured system"""
        return {
            "name": self.system_name,
            "criticality": self.criticality.value,
            "slo_count": len(self.slos),
            "collector_count": len(self.collectors),
            "evaluator_count": len(self.evaluators),
            "workflow_enabled": self.use_workflow,
            "workflow_type": self.workflow_type if self.use_workflow else None,
        }

    def get_slo_summary(self) -> list[dict[str, Any]]:
        """Get summary of all SLOs"""
        return [
            {
                "name": slo.name,
                "target": slo.target,
                "window": slo.window,
                "safety_critical": slo.safety_critical,
                "business_impact": slo.business_impact,
            }
            for slo in self.slos
        ]

    def generate_reports(self, results: dict[str, Any]) -> dict[str, Any]:
        """Generate reports from evaluation results"""
        try:
            from ..reports import (
                BusinessImpactReport,
                ComplianceReport,
                ReliabilityReport,
                SafetyReport,
            )

            reports = {}
            report_configs = self.config.get("reports", [])

            for report_config in report_configs:
                report_type = report_config.get("type", "reliability")
                report_name = report_config.get("name", f"{report_type}_report")

                # Create appropriate report instance
                report: Any
                if report_type == "business":
                    report = BusinessImpactReport(report_config)
                elif report_type == "compliance":
                    report = ComplianceReport(report_config)
                elif report_type == "safety":
                    report = SafetyReport(report_config)
                else:  # Default to reliability
                    report = ReliabilityReport(report_config)

                # Generate report data
                report_data = report.generate(results)
                reports[report_name] = {
                    "title": report_data.title,
                    "generated_at": report_data.generated_at.isoformat(),
                    "period": report_data.period,
                    "summary": report_data.summary,
                    "recommendations": report_data.recommendations,
                    "alerts": report_data.alerts,
                }

            return reports

        except Exception as e:
            return {"error": f"Failed to generate reports: {e!s}"}

    def health_check(self) -> dict[str, Any]:
        """Perform health check on all components"""
        try:
            health_status = {
                "overall_healthy": True,
                "timestamp": datetime.now().isoformat(),
                "system": self.get_system_info(),
                "collectors": [],
                "evaluators": [],
                "workflow": {},
                "errors": [],
                "evaluator_types": self._get_evaluator_types(),
            }

            # Check collectors
            for collector in self.collectors:
                try:
                    collector_health = collector.health_check()
                    collectors = health_status["collectors"]
                    if isinstance(collectors, list):
                        collectors.append(
                            {
                                "name": getattr(collector, "name", "unknown"),
                                "healthy": collector_health,
                            }
                        )
                    if not collector_health:
                        health_status["overall_healthy"] = False
                except Exception as e:
                    collectors = health_status["collectors"]
                    if isinstance(collectors, list):
                        collectors.append(
                            {
                                "name": getattr(collector, "name", "unknown"),
                                "healthy": False,
                                "error": str(e),
                            }
                        )
                    health_status["overall_healthy"] = False
                    errors = health_status["errors"]
                    if isinstance(errors, list):
                        errors.append(f"Collector error: {e!s}")

            # Check evaluators (basic check)
            for evaluator in self.evaluators:
                try:
                    evaluator_name = evaluator.__class__.__name__
                    evaluators = health_status["evaluators"]
                    if isinstance(evaluators, list):
                        evaluators.append(
                            {
                                "name": evaluator_name,
                                # Basic check - evaluators are stateless
                                "healthy": True,
                            }
                        )
                except Exception as e:
                    evaluators = health_status["evaluators"]
                    if isinstance(evaluators, list):
                        evaluators.append(
                            {
                                "name": evaluator.__class__.__name__,
                                "healthy": False,
                                "error": str(e),
                            }
                        )
                    health_status["overall_healthy"] = False
                    errors = health_status["errors"]
                    if isinstance(errors, list):
                        errors.append(f"Evaluator error: {e!s}")

            # Check workflow engine
            if self.workflow_engine:
                try:
                    try:
                        workflow_status = self.workflow_engine.get_workflow_status()
                    except AttributeError:
                        workflow_status = {"status": "unknown"}
                    health_status["workflow"] = {
                        "enabled": True,
                        "healthy": True,
                        "status": workflow_status,
                    }
                except Exception as e:
                    health_status["workflow"] = {
                        "enabled": True,
                        "healthy": False,
                        "error": str(e),
                    }
                    health_status["overall_healthy"] = False
                    errors = health_status["errors"]
                    if isinstance(errors, list):
                        errors.append(f"Workflow error: {e!s}")
            else:
                health_status["workflow"] = {
                    "enabled": False,
                    "healthy": True,
                }

            return health_status

        except Exception as e:
            return {
                "overall_healthy": False,
                "timestamp": datetime.now().isoformat(),
                "error": f"Health check failed: {e!s}",
            }

    def _get_evaluator_types(self) -> list[str]:
        """Get list of evaluator types currently loaded"""
        return [evaluator.__class__.__name__ for evaluator in self.evaluators]

    def get_evaluator_info(self) -> dict[str, Any]:
        """Get detailed information about all evaluators"""
        evaluator_info = {}

        for evaluator in self.evaluators:
            evaluator_name = evaluator.__class__.__name__
            evaluator_info[evaluator_name] = {
                "type": evaluator_name,
                "required_metrics": getattr(evaluator, "get_required_metrics", list)(),
                "config": getattr(evaluator, "config", {}),
            }

            # Add specific info for new evaluators
            if evaluator_name == "InterpretabilityEvaluator":
                evaluator_info[evaluator_name]["capabilities"] = [
                    "model_explainability",
                    "decision_transparency",
                    "feature_importance_analysis",
                    "human_readable_explanations",
                ]
            elif evaluator_name == "EdgeCaseEvaluator":
                evaluator_info[evaluator_name]["capabilities"] = [
                    "systematic_edge_case_generation",
                    "boundary_condition_testing",
                    "stress_testing",
                    "failure_scenario_simulation",
                ]
            elif evaluator_name == "SafetyEvaluator":
                evaluator_info[evaluator_name]["capabilities"] = [
                    "fmea_analysis",
                    "risk_assessment",
                    "safety_margin_evaluation",
                    "emergency_procedure_validation",
                ]

        return evaluator_info
