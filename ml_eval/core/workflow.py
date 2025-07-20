"""Workflow engine for complex evaluation orchestration"""

import asyncio
import logging
from collections.abc import Callable
from datetime import datetime
from enum import Enum
from typing import Any

from .config import EvaluationResult


class WorkflowStatus(Enum):
    """Workflow execution status"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StepStatus(Enum):
    """Individual step status"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowStep:
    """Individual workflow step with conditional logic"""

    def __init__(
        self,
        name: str,
        function: Callable,
        dependencies: list[str] | None = None,
        condition: Callable | None = None,
        timeout: int = 300,
        retries: int = 3,
        critical: bool = False,
        parallel: bool = False,
    ):
        self.name = name
        self.function = function
        self.dependencies = dependencies or []
        self.condition = condition
        self.timeout = timeout
        self.retries = retries
        self.critical = critical
        self.parallel = parallel
        self.status = StepStatus.PENDING
        self.result = None
        self.error = None
        self.start_time = None
        self.end_time = None


class WorkflowEngine:
    """Advanced workflow engine for complex evaluation orchestration"""

    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.steps: list[WorkflowStep] = []
        self.context: dict[str, Any] = {}
        self.status = WorkflowStatus.PENDING
        self.results: dict[str, Any] = {}
        self.errors: list[str] = []

    def add_step(
        self,
        name: str,
        function: Callable,
        dependencies: list[str] | None = None,
        condition: Callable | None = None,
        timeout: int = 300,
        retries: int = 3,
        critical: bool = False,
        parallel: bool = False,
    ) -> "WorkflowEngine":
        """Add a workflow step"""
        step = WorkflowStep(
            name=name,
            function=function,
            dependencies=dependencies or [],
            condition=condition,
            timeout=timeout,
            retries=retries,
            critical=critical,
            parallel=parallel,
        )
        self.steps.append(step)
        return self

    def add_conditional_step(
        self,
        name: str,
        function: Callable,
        condition: Callable,
        dependencies: list[str] | None = None,
        **kwargs,
    ) -> "WorkflowEngine":
        """Add a step that only executes if condition is met"""
        return self.add_step(
            name=name,
            function=function,
            condition=condition,
            dependencies=dependencies,
            **kwargs,
        )

    def add_parallel_steps(self, steps: list[dict[str, Any]]) -> "WorkflowEngine":
        """Add multiple steps that can run in parallel"""
        for step_config in steps:
            self.add_step(
                name=step_config["name"],
                function=step_config["function"],
                dependencies=step_config.get("dependencies", []),
                parallel=True,
                **step_config.get("kwargs", {}),
            )
        return self

    async def execute(self) -> dict[str, Any]:
        """Execute the workflow with dependency resolution and error handling"""
        self.status = WorkflowStatus.RUNNING
        self.logger.info(f"Starting workflow execution with {len(self.steps)} steps")

        try:
            # Execute steps in dependency order
            executed_steps = set()
            failed_steps = set()

            while len(executed_steps) < len(self.steps):
                # Find steps ready to execute
                ready_steps = self._get_ready_steps(executed_steps, failed_steps)

                if not ready_steps:
                    # Check for circular dependencies or unreachable steps
                    remaining_steps = [
                        s
                        for s in self.steps
                        if s.name not in executed_steps and s.name not in failed_steps
                    ]
                    if remaining_steps:
                        self.logger.error(
                            f"Circular dependency detected or unreachable steps: {[s.name for s in remaining_steps]}"
                        )
                        raise RuntimeError(
                            "Workflow has circular dependencies or unreachable steps"
                        )
                    break

                # Execute ready steps (parallel if possible)
                parallel_steps = [s for s in ready_steps if s.parallel]
                sequential_steps = [s for s in ready_steps if not s.parallel]

                # Execute parallel steps
                if parallel_steps:
                    parallel_results = await asyncio.gather(
                        *[self._execute_step(step) for step in parallel_steps],
                        return_exceptions=True,
                    )
                    for step, result in zip(
                        parallel_steps, parallel_results, strict=False
                    ):
                        if isinstance(result, Exception):
                            self._handle_step_failure(step, result)
                            failed_steps.add(step.name)
                        else:
                            executed_steps.add(step.name)

                # Execute sequential steps
                for step in sequential_steps:
                    try:
                        await self._execute_step(step)
                        executed_steps.add(step.name)
                    except Exception as e:
                        self._handle_step_failure(step, e)
                        failed_steps.add(step.name)
                        if step.critical:
                            self.status = WorkflowStatus.FAILED
                            raise e

            # Check final status
            if failed_steps:
                self.status = WorkflowStatus.FAILED
            else:
                self.status = WorkflowStatus.COMPLETED

            return {
                "status": self.status.value,
                "results": self.results,
                "errors": self.errors,
                "executed_steps": list(executed_steps),
                "failed_steps": list(failed_steps),
            }

        except Exception as e:
            self.status = WorkflowStatus.FAILED
            self.logger.error(f"Workflow execution failed: {e}")
            raise

    def _get_ready_steps(
        self, executed_steps: set, failed_steps: set
    ) -> list[WorkflowStep]:
        """Get steps that are ready to execute (dependencies satisfied)"""
        ready_steps = []

        for step in self.steps:
            if step.name in executed_steps or step.name in failed_steps:
                continue

            # Check if dependencies are satisfied
            dependencies_satisfied = all(
                dep in executed_steps for dep in step.dependencies
            )

            # Check if condition is met
            condition_met = True
            if step.condition:
                try:
                    condition_met = step.condition(self.context)
                except Exception as e:
                    self.logger.warning(
                        f"Condition check failed for step {step.name}: {e}"
                    )
                    condition_met = False

            if dependencies_satisfied and condition_met:
                ready_steps.append(step)

        return ready_steps

    async def _execute_step(self, step: WorkflowStep) -> Any:
        """Execute a single workflow step"""
        step.status = StepStatus.RUNNING
        step.start_time = datetime.now()

        self.logger.info(f"Executing step: {step.name}")

        for attempt in range(step.retries + 1):
            try:
                # Execute with timeout
                if asyncio.iscoroutinefunction(step.function):
                    result = await asyncio.wait_for(
                        step.function(self.context), timeout=step.timeout
                    )
                else:
                    result = step.function(self.context)

                step.status = StepStatus.COMPLETED
                step.result = result
                step.end_time = datetime.now()

                # Store result in context
                self.context[step.name] = result
                self.results[step.name] = result

                self.logger.info(f"Step {step.name} completed successfully")
                return result

            except Exception as e:
                if attempt < step.retries:
                    self.logger.warning(
                        f"Step {step.name} failed (attempt {attempt + 1}/{step.retries + 1}): {e}"
                    )
                    await asyncio.sleep(1)  # Brief delay before retry
                else:
                    step.status = StepStatus.FAILED
                    step.error = str(e)
                    step.end_time = datetime.now()
                    self.logger.error(
                        f"Step {step.name} failed after {step.retries + 1} attempts: {e}"
                    )
                    raise e

    def _handle_step_failure(self, step: WorkflowStep, error: Exception):
        """Handle step failure"""
        step.status = StepStatus.FAILED
        step.error = str(error)
        step.end_time = datetime.now()
        self.errors.append(f"Step {step.name} failed: {error}")

        if step.critical:
            self.logger.error(f"Critical step {step.name} failed, stopping workflow")
        else:
            self.logger.warning(
                f"Non-critical step {step.name} failed, continuing workflow"
            )

    def get_workflow_status(self) -> dict[str, Any]:
        """Get current workflow status"""
        return {
            "status": self.status.value,
            "total_steps": len(self.steps),
            "completed_steps": len(
                [s for s in self.steps if s.status == StepStatus.COMPLETED]
            ),
            "failed_steps": len(
                [s for s in self.steps if s.status == StepStatus.FAILED]
            ),
            "pending_steps": len(
                [s for s in self.steps if s.status == StepStatus.PENDING]
            ),
            "errors": self.errors,
        }


class EvaluationWorkflow:
    """Specialized workflow for ML system evaluation"""

    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.workflow_engine = WorkflowEngine(config)
        self._setup_evaluation_workflow()

    def _setup_evaluation_workflow(self):
        """Setup the evaluation workflow steps"""
        # Data collection phase
        self.workflow_engine.add_step(
            name="validate_config", function=self._validate_configuration, critical=True
        )

        self.workflow_engine.add_step(
            name="collect_metrics",
            function=self._collect_metrics,
            dependencies=["validate_config"],
            critical=True,
        )

        # Parallel evaluation phase
        self.workflow_engine.add_parallel_steps(
            [
                {
                    "name": "evaluate_performance",
                    "function": self._evaluate_performance,
                    "dependencies": ["collect_metrics"],
                    "kwargs": {"critical": False},
                },
                {
                    "name": "evaluate_reliability",
                    "function": self._evaluate_reliability,
                    "dependencies": ["collect_metrics"],
                    "kwargs": {"critical": False},
                },
                {
                    "name": "evaluate_safety",
                    "function": self._evaluate_safety,
                    "dependencies": ["collect_metrics"],
                    "kwargs": {"critical": True},
                },
            ]
        )

        # Conditional evaluation steps
        self.workflow_engine.add_conditional_step(
            name="evaluate_drift",
            function=self._evaluate_drift,
            condition=self._should_evaluate_drift,
            dependencies=["collect_metrics"],
        )

        self.workflow_engine.add_conditional_step(
            name="evaluate_compliance",
            function=self._evaluate_compliance,
            condition=self._should_evaluate_compliance,
            dependencies=["collect_metrics"],
        )

        # Reporting phase
        self.workflow_engine.add_step(
            name="generate_reports",
            function=self._generate_reports,
            dependencies=[
                "evaluate_performance",
                "evaluate_reliability",
                "evaluate_safety",
            ],
            critical=False,
        )

        self.workflow_engine.add_step(
            name="build_final_result",
            function=self._build_final_result,
            dependencies=["generate_reports"],
            critical=True,
        )

    def _validate_configuration(self, _context: dict[str, Any]) -> dict[str, Any]:
        """Validate configuration before execution"""
        # Implementation would validate config structure, required fields, etc.
        return {"valid": True, "validation_errors": []}

    def _collect_metrics(self, _context: dict[str, Any]) -> dict[str, Any]:
        """Collect metrics from all sources"""
        # Implementation would collect from all configured collectors
        return {"metrics": {}, "collection_errors": []}

    def _evaluate_performance(self, _context: dict[str, Any]) -> dict[str, Any]:
        """Evaluate performance metrics"""
        # Implementation would run performance evaluators
        return {"performance_score": 0.95, "alerts": []}

    def _evaluate_reliability(self, _context: dict[str, Any]) -> dict[str, Any]:
        """Evaluate reliability metrics"""
        # Implementation would run reliability evaluators
        return {"reliability_score": 0.98, "slo_violations": []}

    def _evaluate_safety(self, _context: dict[str, Any]) -> dict[str, Any]:
        """Evaluate safety-critical metrics"""
        # Implementation would run safety evaluators
        return {"safety_score": 0.99, "safety_violations": []}

    def _evaluate_drift(self, _context: dict[str, Any]) -> dict[str, Any]:
        """Evaluate data/model drift"""
        # Implementation would run drift evaluators
        return {"drift_score": 0.02, "drift_detected": False}

    def _evaluate_compliance(self, _context: dict[str, Any]) -> dict[str, Any]:
        """Evaluate compliance requirements"""
        # Implementation would run compliance evaluators
        return {"compliance_score": 0.97, "compliance_violations": []}

    def _generate_reports(self, _context: dict[str, Any]) -> dict[str, Any]:
        """Generate evaluation reports"""
        # Implementation would generate various reports
        return {"reports": {"business": {}, "compliance": {}, "safety": {}}}

    def _build_final_result(self, _context: dict[str, Any]) -> dict[str, Any]:
        """Build final evaluation result"""
        # Implementation would combine all results into final evaluation
        return {"final_result": EvaluationResult(...)}

    def _should_evaluate_drift(self, _context: dict[str, Any]) -> bool:
        """Determine if drift evaluation should run"""
        config = self.config.get("evaluators", [])
        return any(e.get("type") == "drift" for e in config)

    def _should_evaluate_compliance(self, _context: dict[str, Any]) -> bool:
        """Determine if compliance evaluation should run"""
        config = self.config.get("evaluators", [])
        return any(e.get("type") == "compliance" for e in config)

    async def execute(self) -> dict[str, Any]:
        """Execute the evaluation workflow"""
        return await self.workflow_engine.execute()

    def get_workflow_status(self) -> dict[str, Any]:
        """Get current workflow status"""
        return self.workflow_engine.get_workflow_status()
