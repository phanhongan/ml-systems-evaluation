"""Edge case evaluator for ML Systems Evaluation"""

import logging
from datetime import datetime
from typing import Any

import numpy as np

from ..base import BaseEvaluator


class EdgeCaseEvaluator(BaseEvaluator):
    """Evaluate system behavior under edge cases and extreme conditions"""

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.logger = logging.getLogger(__name__)
        self.edge_case_config = config.get("edge_cases", {})
        self.boundary_config = config.get("boundary_conditions", {})
        self.stress_config = config.get("stress_testing", {})
        self.failure_config = config.get("failure_scenarios", {})
        self.thresholds = config.get("thresholds", {})

        # LLM integration
        self.use_llm = config.get("use_llm", True)
        self.llm_config = config.get("llm", {})
        self.llm_assistant = None
        self.llm_analyzer = None

        if self.use_llm:
            try:
                from ...llm import LLMAnalysisEngine, LLMAssistantEngine

                self.llm_assistant = LLMAssistantEngine(self.llm_config)
                self.llm_analyzer = LLMAnalysisEngine(self.llm_config)
                self.logger.info("✅ LLM-enhanced evaluator initialized successfully")
            except ImportError:
                self.logger.warning(
                    "❌ LLM components not available, falling back to deterministic evaluation"
                )
            except Exception as e:
                self.logger.warning(
                    f"❌ LLM initialization failed: {e}, falling back to deterministic evaluation"
                )
        else:
            self.logger.info("i️ LLM disabled, using deterministic evaluation only")

    def get_required_metrics(self) -> list[str]:
        """Get required metrics for edge case evaluation"""
        metrics = []

        # Edge case metrics
        metrics.extend(
            [
                "edge_case_success_rate",
                "boundary_condition_handling",
                "stress_test_performance",
                "failure_scenario_recovery",
                "corner_case_detection_rate",
            ]
        )

        # Component-specific edge case metrics
        for component in ["perception", "decision_making", "output_control"]:
            metrics.extend(
                [
                    f"{component}_edge_case_handling",
                    f"{component}_boundary_performance",
                    f"{component}_stress_test_score",
                    f"{component}_failure_recovery_rate",
                ]
            )

        # Specific edge case scenarios
        edge_scenarios = [
            "low_visibility_handling",
            "extreme_environmental_performance",
            "sensor_failure_recovery",
            "communication_loss_handling",
            "emergency_response_success",
            "obstacle_avoidance_edge_cases",
            "rule_violation_handling",
            "system_overload_performance",
        ]

        for scenario in edge_scenarios:
            metrics.extend(
                [
                    f"{scenario}_success_rate",
                    f"{scenario}_response_time",
                    f"{scenario}_safety_margin",
                ]
            )

        return metrics

    def evaluate(self, metrics: dict[str, Any]) -> dict[str, Any]:
        """Evaluate edge case handling and stress testing"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "evaluator": "edge_case",
            "overall_edge_case_score": 0.0,
            "component_scores": {},
            "scenario_scores": {},
            "alerts": [],
            "recommendations": [],
            "llm_enhanced": {},
        }

        # Evaluate overall edge case handling
        overall_score = self._evaluate_overall_edge_case_handling(metrics)
        results["overall_edge_case_score"] = overall_score

        # Evaluate component-specific edge case handling
        component_scores = self._evaluate_component_edge_cases(metrics)
        results["component_scores"] = component_scores

        # Evaluate specific scenarios
        scenario_scores = self._evaluate_scenario_performance(metrics)
        results["scenario_scores"] = scenario_scores

        # Generate alerts and recommendations
        alerts, recommendations = self._generate_edge_case_alerts_and_recommendations(
            metrics, overall_score, scenario_scores
        )
        results["alerts"] = alerts
        results["recommendations"] = recommendations

        # LLM-enhanced analysis
        if self.use_llm and self.llm_assistant and self.llm_analyzer:
            llm_enhanced = self._perform_llm_enhanced_edge_case_analysis(
                metrics, component_scores, scenario_scores
            )
            results["llm_enhanced"] = llm_enhanced

        return results

    def _evaluate_overall_edge_case_handling(self, metrics: dict[str, Any]) -> float:
        """Evaluate overall edge case handling score"""
        scores = []

        # Edge case success rate
        if "edge_case_success_rate" in metrics:
            scores.append(metrics["edge_case_success_rate"])

        # Boundary condition handling
        if "boundary_condition_handling" in metrics:
            scores.append(metrics["boundary_condition_handling"])

        # Stress test performance
        if "stress_test_performance" in metrics:
            scores.append(metrics["stress_test_performance"])

        # Failure scenario recovery
        if "failure_scenario_recovery" in metrics:
            scores.append(metrics["failure_scenario_recovery"])

        # Corner case detection rate
        if "corner_case_detection_rate" in metrics:
            scores.append(metrics["corner_case_detection_rate"])

        return float(np.mean(scores)) if scores else 0.0

    def _evaluate_component_edge_cases(
        self, metrics: dict[str, Any]
    ) -> dict[str, float]:
        """Evaluate edge case handling for each component"""
        components = ["perception", "decision_making", "output_control"]
        component_scores = {}

        for component in components:
            component_metrics = [
                f"{component}_edge_case_handling",
                f"{component}_boundary_performance",
                f"{component}_stress_test_score",
                f"{component}_failure_recovery_rate",
            ]

            scores = []
            for metric in component_metrics:
                if metric in metrics:
                    scores.append(metrics[metric])

            component_scores[component] = float(np.mean(scores)) if scores else 0.0

        return component_scores

    def _evaluate_scenario_performance(
        self, metrics: dict[str, Any]
    ) -> dict[str, float]:
        """Evaluate performance in specific edge case scenarios"""
        scenarios = [
            "low_visibility_handling",
            "extreme_environmental_performance",
            "sensor_failure_recovery",
            "communication_loss_handling",
            "emergency_response_success",
            "obstacle_avoidance_edge_cases",
            "rule_violation_handling",
            "system_overload_performance",
        ]

        scenario_scores = {}

        for scenario in scenarios:
            scenario_metrics = [
                f"{scenario}_success_rate",
                f"{scenario}_response_time",
                f"{scenario}_safety_margin",
            ]

            scores = []
            for metric in scenario_metrics:
                if metric in metrics:
                    scores.append(metrics[metric])

            scenario_scores[scenario] = float(np.mean(scores)) if scores else 0.0

        return scenario_scores

    def _perform_llm_enhanced_edge_case_analysis(
        self,
        metrics: dict[str, Any],
        component_scores: dict[str, float],
        scenario_scores: dict[str, float],
    ) -> dict[str, Any]:
        """Perform LLM-enhanced edge case analysis"""
        try:
            llm_enhanced = {
                "intelligent_edge_case_generation": {},
                "failure_pattern_analysis": {},
                "scenario_reasoning": {},
                "adaptive_stress_testing": {},
                "safety_margin_analysis": {},
            }

            # Generate intelligent edge cases
            edge_cases = self._generate_intelligent_edge_cases(
                metrics, component_scores
            )
            llm_enhanced["intelligent_edge_case_generation"] = edge_cases

            # Analyze failure patterns
            failure_patterns = self._analyze_failure_patterns(metrics, scenario_scores)
            llm_enhanced["failure_pattern_analysis"] = failure_patterns

            # Scenario reasoning
            scenario_reasoning = self._analyze_scenario_reasoning(
                metrics, scenario_scores
            )
            llm_enhanced["scenario_reasoning"] = scenario_reasoning

            # Adaptive stress testing
            adaptive_stress = self._generate_adaptive_stress_tests(
                metrics, component_scores
            )
            llm_enhanced["adaptive_stress_testing"] = adaptive_stress

            # Safety margin analysis
            safety_margins = self._analyze_safety_margins(metrics, scenario_scores)
            llm_enhanced["safety_margin_analysis"] = safety_margins

            return llm_enhanced

        except Exception as e:
            return {
                "error": f"LLM-enhanced edge case analysis failed: {e!s}",
                "fallback": "Using deterministic analysis only",
            }

    def _generate_intelligent_edge_cases(
        self, metrics: dict[str, Any], component_scores: dict[str, float]
    ) -> dict[str, Any]:
        """Generate intelligent edge cases using LLM"""
        try:
            edge_case_analysis = {
                "generated_scenarios": [],
                "boundary_conditions": [],
                "failure_modes": [],
                "stress_conditions": [],
            }

            # Generate edge cases for each component
            for component in ["perception", "decision_making", "output_control"]:
                if component in component_scores:
                    component_score = component_scores[component]

                    # Generate component-specific edge cases
                    scenarios = self._generate_component_edge_cases(
                        component, component_score, metrics
                    )
                    edge_case_analysis["generated_scenarios"].extend(scenarios)

            # Generate boundary condition scenarios
            boundary_scenarios = self._generate_boundary_conditions(metrics)
            edge_case_analysis["boundary_conditions"] = boundary_scenarios

            # Generate failure mode scenarios
            failure_scenarios = self._generate_failure_modes(metrics)
            edge_case_analysis["failure_modes"] = failure_scenarios

            # Generate stress condition scenarios
            stress_scenarios = self._generate_stress_conditions()
            edge_case_analysis["stress_conditions"] = stress_scenarios

            return edge_case_analysis

        except Exception as e:
            return {
                "error": f"Intelligent edge case generation failed: {e!s}",
                "fallback": "Using basic edge case analysis",
            }

    def _call_llm_for_edge_cases(
        self, prompt: str, component: str, score: float
    ) -> list[str]:
        """Make actual LLM call for edge case generation"""
        try:
            # Log the reasoning chain
            self.logger.debug(f"🧠 Starting LLM edge case reasoning for {component}")
            self.logger.debug(f"📊 Component score: {score:.3f}")
            self.logger.debug(f"🎯 Targeting edge cases for component: {component}")

            import asyncio

            async def make_llm_call():
                try:
                    # Check if LLM assistant is available
                    if not self.llm_assistant:
                        raise AttributeError("LLM assistant not available")

                    # Log the prompt being sent
                    self.logger.debug(f"📤 Sending edge case prompt for {component}:")
                    self.logger.debug(f"   📝 Prompt length: {len(prompt)} characters")
                    self.logger.debug(f"   🎯 Component: {component}")
                    self.logger.debug(f"   📊 Score: {score:.3f}")

                    # Log a preview of the prompt (first 200 chars)
                    prompt_preview = prompt[:200].replace("\n", " ").strip()
                    self.logger.debug(f"   📋 Prompt preview: {prompt_preview}...")

                    # Use the LLM provider to generate response
                    response = await self.llm_assistant.provider.generate_response(
                        prompt=prompt,
                        context={
                            "component": component,
                            "score": score,
                            "edge_case_type": "component_specific",
                        },
                        temperature=0.2,  # Slightly higher for creativity
                    )

                    # Log the response analysis
                    self.logger.debug(
                        f"📥 Received edge case response for {component}:"
                    )
                    self.logger.debug(
                        f"   📏 Response length: {len(response)} characters"
                    )

                    # Log a preview of the response (first 200 chars)
                    response_preview = response[:200].replace("\n", " ").strip()
                    self.logger.debug(f"   📋 Response preview: {response_preview}...")

                    # Analyze the response reasoning
                    self._analyze_edge_case_reasoning(response, component)

                    # Parse the response into scenarios
                    scenarios = self._parse_edge_case_response(response)
                    self.logger.debug(
                        f"📋 Parsed {len(scenarios)} edge case scenarios for {component}"
                    )

                    return scenarios

                except AttributeError as e:
                    self.logger.warning(f"❌ LLM provider not available: {e}")
                    raise
                except Exception as e:
                    self.logger.error(f"❌ LLM call failed: {e}")
                    raise e

            # Run the async call
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                scenarios = loop.run_until_complete(make_llm_call())
                self.logger.debug(
                    f"✅ LLM edge case reasoning completed for {component}"
                )
                return scenarios
            finally:
                loop.close()

        except Exception as e:
            self.logger.warning(
                f"❌ Real LLM call failed: {e}, falling back to simulation"
            )
            return self._generate_deterministic_edge_cases(component, score)

    def _analyze_edge_case_reasoning(self, response: str, component: str) -> None:
        """Analyze the reasoning chain in the edge case response"""
        try:
            # Extract reasoning patterns
            reasoning_analysis = {
                "scenario_mentions": response.lower().count("scenario"),
                "failure_mentions": response.lower().count("failure"),
                "boundary_mentions": response.lower().count("boundary"),
                "stress_mentions": response.lower().count("stress"),
                "safety_mentions": response.lower().count("safety"),
                "component_specific": response.lower().count(component.lower()),
                "edge_case_mentions": response.lower().count("edge case"),
                "testing_mentions": response.lower().count("test"),
            }

            # Log the reasoning analysis
            self.logger.debug(f"🔍 Edge case reasoning analysis for {component}:")
            for key, count in reasoning_analysis.items():
                if count > 0:
                    self.logger.debug(f"   {key}: {count} mentions")

            # Analyze response structure
            lines = response.strip().split("\n")
            self.logger.debug(f"📝 Response structure: {len(lines)} lines")

            # Check for specific reasoning patterns
            if "scenario" in response.lower():
                self.logger.debug("   ✅ Scenario-based reasoning detected")
            if "failure" in response.lower():
                self.logger.debug("   ✅ Failure mode reasoning detected")
            if "boundary" in response.lower():
                self.logger.debug("   ✅ Boundary condition reasoning detected")
            if "stress" in response.lower():
                self.logger.debug("   ✅ Stress testing reasoning detected")
            if "safety" in response.lower():
                self.logger.debug("   ✅ Safety-focused reasoning detected")

        except Exception as e:
            self.logger.warning(f"Failed to analyze edge case reasoning: {e}")

    def _generate_component_edge_cases(
        self, component: str, score: float, metrics: dict[str, Any]
    ) -> list[str]:
        """Generate edge cases for a specific component using LLM"""
        try:
            # Log the edge case generation process
            self.logger.debug(f"🔍 Starting edge case generation for {component}")
            self.logger.debug(f"   Score: {score:.3f}")
            self.logger.debug(f"   Available metrics: {len(metrics)} items")

            # Early return for deterministic path when LLM is disabled
            if not self.llm_assistant:
                self.logger.debug(
                    f"i️ LLM disabled, using deterministic edge cases for {component}"
                )
                return self._generate_deterministic_edge_cases(component, score)

            # Build LLM prompt for edge case generation
            prompt = f"""
Generate edge case scenarios for the {component} component in a safety-critical ML system.

Component: {component}
Component Score: {score:.3f}
Component Metrics: {metrics}

Generate 3-5 specific edge case scenarios that:
1. Test the component's limits and boundaries
2. Challenge the component's assumptions
3. Explore failure modes and edge conditions
4. Consider safety-critical implications
5. Are specific to the {component} domain

Focus on realistic scenarios that could occur in production.
"""

            self.logger.debug(f"📝 Constructed edge case prompt for {component}")
            self.logger.debug(
                "   Prompt focuses on: limits, failure modes, decision-making, safety"
            )

            try:
                # Make actual LLM call
                scenarios = self._call_llm_for_edge_cases(prompt, component, score)
                self.logger.debug(f"✅ LLM edge cases generated for {component}")
                return scenarios
            except Exception as e:
                self.logger.warning(f"❌ LLM edge case generation failed: {e}")
                fallback = self._generate_deterministic_edge_cases(component, score)
                self.logger.debug(f"🔄 Using deterministic fallback for {component}")
                return fallback

        except Exception as e:
            self.logger.error(f"❌ Error generating edge cases for {component}: {e!s}")
            return [f"Error generating edge cases for {component}: {e!s}"]

    def _parse_edge_case_response(self, response: str) -> list[str]:
        """Parse LLM response into edge case scenarios"""
        try:
            # Simple parsing - split by newlines and filter
            lines = response.strip().split("\n")
            scenarios = []

            for line in lines:
                line = line.strip()
                # Remove numbering and common prefixes
                if line and not line.startswith(
                    ("1.", "2.", "3.", "4.", "5.", "-", "*")
                ):
                    # Clean up the scenario
                    scenario = line.strip()
                    if len(scenario) > 10:  # Minimum meaningful length
                        scenarios.append(scenario)

            # If parsing failed, return the original response as a single scenario
            if not scenarios and response.strip():
                scenarios = [response.strip()]

            return scenarios[:5]  # Limit to 5 scenarios

        except Exception as e:
            self.logger.warning(f"Failed to parse edge case response: {e}")
            return [response.strip()] if response.strip() else []

    def _generate_deterministic_edge_cases(
        self, component: str, score: float
    ) -> list[str]:
        """Generate deterministic edge cases as fallback"""
        if score < 0.5:
            return [
                f"Targeted stress test for {component} system (current score: {score:.3f})",
                f"Low performance {component} testing",
                f"Boundary condition testing for {component}",
                f"Failure mode analysis for {component}",
                f"Stress testing for {component} under load",
            ]
        else:
            return [
                f"Standard edge case testing for {component} (score: {score:.3f})",
                f"Boundary condition validation for {component}",
                f"Stress testing for {component}",
                f"Failure mode validation for {component}",
            ]

    def _generate_boundary_conditions(self, metrics: dict[str, Any]) -> list[str]:
        """Generate boundary condition scenarios"""
        try:
            boundary_scenarios = []

            # Generate boundary conditions based on metrics
            boundary_metrics = {
                k: v
                for k, v in metrics.items()
                if "boundary" in k.lower() or "limit" in k.lower()
            }

            if boundary_metrics:
                for metric, value in boundary_metrics.items():
                    boundary_scenarios.append(
                        f"Test boundary condition: {metric} = {value:.3f}"
                    )

            # Add standard boundary conditions
            boundary_scenarios.extend(
                [
                    "Test system behavior at maximum sensor range",
                    "Validate performance under minimum visibility conditions",
                    "Verify operation at maximum speed limits",
                    "Test response under minimum reaction time constraints",
                ]
            )

            return boundary_scenarios

        except Exception as e:
            return [f"Error generating boundary conditions: {e!s}"]

    def _generate_failure_modes(self, metrics: dict[str, Any]) -> list[str]:
        """Generate failure mode scenarios"""
        try:
            failure_scenarios = []

            # Generate failure modes based on metrics
            failure_metrics = {
                k: v
                for k, v in metrics.items()
                if "failure" in k.lower() or "recovery" in k.lower()
            }

            if failure_metrics:
                for metric, value in failure_metrics.items():
                    failure_scenarios.append(
                        f"Test failure mode: {metric} (current: {value:.3f})"
                    )

            # Add comprehensive failure scenarios
            failure_scenarios.extend(
                [
                    "Complete sensor failure recovery testing",
                    "Communication system failure scenarios",
                    "Power system failure recovery",
                    "Software crash recovery testing",
                    "Hardware malfunction scenarios",
                ]
            )

            return failure_scenarios

        except Exception as e:
            return [f"Error generating failure modes: {e!s}"]

    def _generate_stress_conditions(self) -> list[str]:
        """Generate stress condition scenarios"""
        try:
            stress_scenarios = [
                "Maximum computational load testing",
                "Memory exhaustion scenarios",
                "Network bandwidth limitation testing",
                "Concurrent failure mode testing",
                "Extended operation under stress conditions",
            ]

            return stress_scenarios

        except Exception as e:
            return [f"Error generating stress conditions: {e!s}"]

    def _analyze_failure_patterns(
        self, _metrics: dict[str, Any], scenario_scores: dict[str, float]
    ) -> dict[str, Any]:
        """Analyze failure patterns using LLM"""
        try:
            failure_patterns = {
                "pattern_analysis": [],
                "correlation_insights": [],
                "prevention_strategies": [],
                "risk_assessment": {},
            }

            # Analyze low-performing scenarios
            low_performing_scenarios = [
                scenario for scenario, score in scenario_scores.items() if score < 0.7
            ]

            if low_performing_scenarios:
                failure_patterns["pattern_analysis"] = [
                    f"Scenario '{scenario}' shows poor performance (score: {scenario_scores[scenario]:.3f})"
                    for scenario in low_performing_scenarios
                ]

                failure_patterns["prevention_strategies"] = [
                    f"Improve handling for: {', '.join(low_performing_scenarios)}"
                ]

            # Risk assessment
            overall_risk = (
                np.mean(list(scenario_scores.values())) if scenario_scores else 0.0
            )
            failure_patterns["risk_assessment"] = {
                "overall_risk_score": overall_risk,
                "high_risk_scenarios": low_performing_scenarios,
                "risk_level": (
                    "high"
                    if overall_risk < 0.7
                    else "medium" if overall_risk < 0.9 else "low"
                ),
            }

            return failure_patterns

        except Exception as e:
            return {"error": f"Failure pattern analysis failed: {e!s}"}

    def _analyze_scenario_reasoning(
        self, metrics: dict[str, Any], scenario_scores: dict[str, float]
    ) -> dict[str, Any]:
        """Analyze scenario reasoning using LLM"""
        try:
            scenario_reasoning = {
                "scenario_insights": {},
                "causal_analysis": {},
                "improvement_recommendations": [],
            }

            # Analyze each scenario
            for scenario, score in scenario_scores.items():
                scenario_metrics = {
                    k: v for k, v in metrics.items() if scenario in k.lower()
                }

                insight = {
                    "score": score,
                    "performance": (
                        "good" if score >= 0.8 else "poor" if score < 0.6 else "fair"
                    ),
                    "key_metrics": scenario_metrics,
                }

                if score < 0.7:
                    insight["recommendation"] = f"Improve {scenario} handling"
                    scenario_reasoning["improvement_recommendations"].append(
                        f"Enhance {scenario} scenario testing and handling"
                    )

                scenario_reasoning["scenario_insights"][scenario] = insight

            return scenario_reasoning

        except Exception as e:
            return {"error": f"Scenario reasoning analysis failed: {e!s}"}

    def _generate_adaptive_stress_tests(
        self, metrics: dict[str, Any], component_scores: dict[str, float]
    ) -> dict[str, Any]:
        """Generate adaptive stress tests using LLM"""
        try:
            adaptive_tests = {
                "targeted_stress_tests": [],
                "progressive_testing": [],
                "failure_injection": [],
                "recovery_testing": [],
            }

            # Generate targeted stress tests for weak components
            for component, score in component_scores.items():
                if score < 0.8:
                    adaptive_tests["targeted_stress_tests"].append(
                        f"Intensive stress test for {component} system (current score: {score:.3f})"
                    )

            # Progressive testing strategy
            if component_scores:
                min_score = min(component_scores.values())
                if min_score < 0.7:
                    adaptive_tests["progressive_testing"] = [
                        "Implement progressive stress testing starting with weakest components",
                        f"Focus on components with scores below {min_score:.3f}",
                    ]

            # Failure injection scenarios
            failure_metrics = {
                k: v for k, v in metrics.items() if "failure" in k.lower()
            }
            if failure_metrics:
                adaptive_tests["failure_injection"] = [
                    f"Inject failure: {k} (current: {v:.3f})"
                    for k, v in failure_metrics.items()
                ]

            return adaptive_tests

        except Exception as e:
            return {"error": f"Adaptive stress test generation failed: {e!s}"}

    def _analyze_safety_margins(
        self, metrics: dict[str, Any], scenario_scores: dict[str, float]
    ) -> dict[str, Any]:
        """Analyze safety margins using LLM"""
        try:
            safety_margins = {
                "margin_analysis": {},
                "safety_violations": [],
                "margin_recommendations": [],
            }

            # Analyze safety margins for each scenario
            for scenario, score in scenario_scores.items():
                safety_metrics = {
                    k: v
                    for k, v in metrics.items()
                    if scenario in k.lower() and "safety" in k.lower()
                }

                margin_analysis = {
                    "scenario_score": score,
                    "safety_margin": safety_metrics.get(
                        f"{scenario}_safety_margin", 0.0
                    ),
                    "safety_status": (
                        "adequate"
                        if score >= 0.8
                        else "concerning" if score >= 0.6 else "critical"
                    ),
                }

                if score < 0.7:
                    safety_margins["safety_violations"].append(
                        f"Safety concern in {scenario} scenario (score: {score:.3f})"
                    )
                    safety_margins["margin_recommendations"].append(
                        f"Increase safety margin for {scenario} scenario"
                    )

                safety_margins["margin_analysis"][scenario] = margin_analysis

            return safety_margins

        except Exception as e:
            return {"error": f"Safety margin analysis failed: {e!s}"}

    def _generate_edge_case_alerts_and_recommendations(
        self,
        metrics: dict[str, Any],
        overall_score: float,
        scenario_scores: dict[str, float],
    ) -> tuple[list[dict], list[dict]]:
        """Generate alerts and recommendations based on edge case performance"""
        alerts = []
        recommendations = []

        # Check overall edge case handling threshold
        edge_case_threshold = self.thresholds.get("overall_edge_case_handling", 0.8)
        if overall_score < edge_case_threshold:
            alerts.append(
                {
                    "level": "critical",
                    "message": f"Overall edge case handling score ({overall_score:.3f}) below critical threshold ({edge_case_threshold})",
                    "component": "edge_case",
                    "timestamp": datetime.now().isoformat(),
                }
            )

            recommendations.append(
                {
                    "priority": "high",
                    "action": "Improve edge case handling",
                    "description": "Implement comprehensive edge case testing and handling mechanisms",
                    "component": "edge_case",
                }
            )

        # Check component-specific edge case handling
        for component in ["perception", "decision_making", "output_control"]:
            component_score = metrics.get(f"{component}_edge_case_handling", 0.0)
            component_threshold = self.thresholds.get(f"{component}_edge_case", 0.8)

            if component_score < component_threshold:
                alerts.append(
                    {
                        "level": "warning",
                        "message": f"{component.capitalize()} edge case handling score ({component_score:.3f}) below threshold ({component_threshold})",
                        "component": component,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

                recommendations.append(
                    {
                        "priority": "high",
                        "action": f"Improve {component} edge case handling",
                        "description": f"Add comprehensive edge case testing for {component} system",
                        "component": component,
                    }
                )

        # Check critical scenario performance
        critical_scenarios = [
            "sensor_failure_recovery",
            "emergency_response_success",
            "communication_loss_handling",
        ]

        for scenario in critical_scenarios:
            if scenario in scenario_scores:
                scenario_score = scenario_scores[scenario]
                scenario_threshold = self.thresholds.get(f"{scenario}_threshold", 0.9)

                if scenario_score < scenario_threshold:
                    alerts.append(
                        {
                            "level": "critical",
                            "message": f"{scenario.replace('_', ' ').title()} score ({scenario_score:.3f}) below critical threshold ({scenario_threshold})",
                            "component": "edge_case",
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

                    recommendations.append(
                        {
                            "priority": "high",
                            "action": f"Improve {scenario.replace('_', ' ')} handling",
                            "description": f"Implement robust handling for {scenario.replace('_', ' ')} scenarios",
                            "component": "edge_case",
                        }
                    )

        # Check stress test performance
        stress_score = metrics.get("stress_test_performance", 0.0)
        stress_threshold = self.thresholds.get("stress_test", 0.7)

        if stress_score < stress_threshold:
            alerts.append(
                {
                    "level": "warning",
                    "message": f"Stress test performance score ({stress_score:.3f}) below threshold ({stress_threshold})",
                    "component": "edge_case",
                    "timestamp": datetime.now().isoformat(),
                }
            )

            recommendations.append(
                {
                    "priority": "medium",
                    "action": "Improve stress testing",
                    "description": "Enhance system resilience under extreme load conditions",
                    "component": "edge_case",
                }
            )

        return alerts, recommendations

    def get_edge_case_metrics(self) -> dict[str, Any]:
        """Get edge case metrics configuration"""
        return {
            "edge_case_metrics": [
                "edge_case_success_rate",
                "boundary_condition_handling",
                "stress_test_performance",
                "failure_scenario_recovery",
                "corner_case_detection_rate",
            ],
            "component_metrics": {
                "perception": [
                    "perception_edge_case_handling",
                    "perception_boundary_performance",
                    "perception_stress_test_score",
                    "perception_failure_recovery_rate",
                ],
                "decision_making": [
                    "decision_making_edge_case_handling",
                    "decision_making_boundary_performance",
                    "decision_making_stress_test_score",
                    "decision_making_failure_recovery_rate",
                ],
                "output_control": [
                    "output_control_edge_case_handling",
                    "output_control_boundary_performance",
                    "output_control_stress_test_score",
                    "output_control_failure_recovery_rate",
                ],
            },
            "scenario_metrics": [
                "low_visibility_handling",
                "extreme_weather_performance",
                "sensor_failure_recovery",
                "communication_loss_handling",
                "emergency_maneuver_success",
                "obstacle_avoidance_edge_cases",
                "traffic_rule_violation_handling",
                "system_overload_performance",
            ],
            "thresholds": self.thresholds,
        }
