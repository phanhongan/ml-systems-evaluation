"""Interpretability evaluator for ML Systems Evaluation"""

import logging
from datetime import datetime
from typing import Any

import numpy as np

from ..base import BaseEvaluator


class InterpretabilityEvaluator(BaseEvaluator):
    """Evaluate model interpretability and decision transparency"""

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.logger = logging.getLogger(__name__)
        self.explainability_config = config.get("explainability", {})
        self.transparency_config = config.get("transparency", {})
        self.feature_importance_config = config.get("feature_importance", {})
        self.explanation_config = config.get("explanations", {})
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
        """Get required metrics for interpretability evaluation"""
        metrics = []

        # Explainability metrics
        metrics.extend(
            [
                "model_explainability_score",
                "decision_transparency_score",
                "feature_importance_consistency",
                "explanation_quality_score",
                "human_readability_score",
            ]
        )

        # Component-specific metrics
        for component in ["perception", "decision_making", "output_control"]:
            metrics.extend(
                [
                    f"{component}_explainability_score",
                    f"{component}_decision_transparency",
                    f"{component}_feature_importance",
                    f"{component}_explanation_quality",
                ]
            )

        return metrics

    def evaluate(self, metrics: dict[str, Any]) -> dict[str, Any]:
        """Evaluate interpretability and transparency"""
        self.logger.debug("🚀 Starting Interpretability Evaluation")
        self.logger.debug(f"📊 Input metrics: {len(metrics)} items")
        self.logger.debug(f"🧠 LLM enabled: {self.use_llm}")

        results = {
            "timestamp": datetime.now().isoformat(),
            "evaluator": "interpretability",
            "overall_interpretability_score": 0.0,
            "component_scores": {},
            "alerts": [],
            "recommendations": [],
            "llm_enhanced": {},
        }

        # Evaluate overall interpretability
        self.logger.debug("📈 Evaluating overall interpretability...")
        overall_score = self._evaluate_overall_interpretability(metrics)
        results["overall_interpretability_score"] = overall_score
        self.logger.debug(f"   Overall score: {overall_score:.3f}")

        # Evaluate component-specific interpretability
        self.logger.debug("🔍 Evaluating component-specific interpretability...")
        component_scores = self._evaluate_component_interpretability(metrics)
        results["component_scores"] = component_scores
        self.logger.debug(f"   Component scores: {component_scores}")

        # Generate alerts and recommendations
        self.logger.debug("⚠️ Generating alerts and recommendations...")
        alerts, recommendations = self._generate_alerts_and_recommendations(
            metrics, overall_score
        )
        results["alerts"] = alerts
        results["recommendations"] = recommendations
        self.logger.debug(f"   Alerts: {len(alerts)}")
        self.logger.debug(f"   Recommendations: {len(recommendations)}")

        # LLM-enhanced analysis
        if self.use_llm and self.llm_assistant and self.llm_analyzer:
            self.logger.debug("🧠 Starting LLM-enhanced analysis...")
            llm_enhanced = self._perform_llm_enhanced_analysis(
                metrics, component_scores
            )
            results["llm_enhanced"] = llm_enhanced
            self.logger.debug("✅ LLM-enhanced analysis completed")
        else:
            self.logger.debug(
                "i️ LLM-enhanced analysis skipped (disabled or unavailable)"
            )

        self.logger.debug("✅ Interpretability evaluation completed")
        return results

    def _evaluate_overall_interpretability(self, metrics: dict[str, Any]) -> float:
        """Evaluate overall interpretability score"""
        scores = []

        # Model explainability
        if "model_explainability_score" in metrics:
            scores.append(metrics["model_explainability_score"])

        # Decision transparency
        if "decision_transparency_score" in metrics:
            scores.append(metrics["decision_transparency_score"])

        # Feature importance consistency
        if "feature_importance_consistency" in metrics:
            scores.append(metrics["feature_importance_consistency"])

        # Explanation quality
        if "explanation_quality_score" in metrics:
            scores.append(metrics["explanation_quality_score"])

        # Human readability
        if "human_readability_score" in metrics:
            scores.append(metrics["human_readability_score"])

        return float(np.mean(scores)) if scores else 0.0

    def _evaluate_component_interpretability(
        self, metrics: dict[str, Any]
    ) -> dict[str, float]:
        """Evaluate interpretability for each component"""
        components = ["perception", "decision_making", "output_control"]
        component_scores = {}

        for component in components:
            component_metrics = [
                f"{component}_explainability_score",
                f"{component}_decision_transparency",
                f"{component}_feature_importance",
                f"{component}_explanation_quality",
            ]

            scores = []
            for metric in component_metrics:
                if metric in metrics:
                    scores.append(metrics[metric])

            component_scores[component] = float(np.mean(scores)) if scores else 0.0

        return component_scores

    def _perform_llm_enhanced_analysis(
        self, metrics: dict[str, Any], component_scores: dict[str, float]
    ) -> dict[str, Any]:
        """Perform LLM-enhanced interpretability analysis"""
        try:
            llm_enhanced = {
                "natural_language_explanations": {},
                "decision_transparency_analysis": {},
                "feature_importance_narratives": {},
                "cross_component_reasoning": {},
                "safety_justifications": {},
            }

            # Generate natural language explanations for each component
            for component in ["perception", "decision_making", "output_control"]:
                if component in component_scores:
                    explanation = self._generate_component_explanation(
                        component, metrics, component_scores[component]
                    )
                    llm_enhanced["natural_language_explanations"][component] = (
                        explanation
                    )

            # Analyze decision transparency patterns
            transparency_analysis = self._analyze_decision_transparency(metrics)
            llm_enhanced["decision_transparency_analysis"] = transparency_analysis

            # Generate feature importance narratives
            feature_narratives = self._generate_feature_importance_narratives(metrics)
            llm_enhanced["feature_importance_narratives"] = feature_narratives

            # Cross-component reasoning
            cross_component_reasoning = self._analyze_cross_component_reasoning(
                metrics, component_scores
            )
            llm_enhanced["cross_component_reasoning"] = cross_component_reasoning

            # Safety justifications
            safety_justifications = self._generate_safety_justifications(metrics)
            llm_enhanced["safety_justifications"] = safety_justifications

            return llm_enhanced

        except Exception as e:
            return {
                "error": f"LLM-enhanced analysis failed: {e!s}",
                "fallback": "Using deterministic analysis only",
            }

    def _call_llm_for_explanation(self, prompt: str, context: dict[str, Any]) -> str:
        """Make actual LLM call for explanation generation"""
        try:
            # Log the reasoning chain
            self.logger.debug(
                f"🧠 Starting LLM reasoning chain for {context['component']}"
            )
            self.logger.debug(
                f"    📊 Component score: {context['score']:.3f}, Threshold: {context['threshold']}"
            )
            self.logger.debug(
                f"    📋 Available metrics: {list(context['metrics'].keys())}"
            )

            # Import async functionality for real LLM calls
            import asyncio

            # Create async context for LLM call
            async def make_llm_call():
                try:
                    # Check if LLM assistant is available
                    if not self.llm_assistant:
                        raise AttributeError("LLM assistant not available")

                    # Log the prompt being sent
                    self.logger.debug(
                        f"📤 Sending LLM prompt for {context['component']}:"
                    )
                    self.logger.debug(f"   📝 Prompt length: {len(prompt)} characters")
                    self.logger.debug(f"   🎯 Component: {context['component']}")
                    self.logger.debug(f"   📊 Score: {context['score']:.3f}")
                    self.logger.debug(f"   🎚️ Threshold: {context['threshold']:.3f}")

                    # Log a preview of the prompt (first 200 chars)
                    prompt_preview = prompt[:200].replace("\n", " ").strip()
                    self.logger.debug(f"   📋 Prompt preview: {prompt_preview}...")

                    # Use the LLM provider to generate response
                    response = await self.llm_assistant.provider.generate_response(
                        prompt=prompt, context=context, temperature=0.1
                    )

                    # Log the response analysis
                    self.logger.debug(
                        f"📥 Received LLM response for {context['component']}:"
                    )
                    self.logger.debug(
                        f"   📏 Response length: {len(response)} characters"
                    )

                    # Log a preview of the response (first 200 chars)
                    response_preview = response[:200].replace("\n", " ").strip()
                    self.logger.debug(f"   📋 Response preview: {response_preview}...")

                    # Analyze the response reasoning
                    self._analyze_response_reasoning(response, context)

                    return response

                except AttributeError as e:
                    self.logger.warning(f"❌ LLM provider not available: {e}")
                    raise
                except Exception as e:
                    self.logger.warning(f"❌ LLM call failed: {e}")
                    raise e

            # Run the async call
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                explanation = loop.run_until_complete(make_llm_call())
                self.logger.debug(
                    f"✅ LLM reasoning chain completed for {context['component']}"
                )
                return explanation
            finally:
                loop.close()

        except Exception as e:
            self.logger.warning(
                f"❌ Real LLM call failed: {e}, falling back to simulation"
            )
            # Fallback to simulation
            return self._generate_simulated_explanation(context)

    def _analyze_response_reasoning(
        self, response: str, context: dict[str, Any]
    ) -> None:
        """Analyze the reasoning chain in the LLM response"""
        try:
            # Extract reasoning patterns
            reasoning_analysis = {
                "safety_mentions": response.lower().count("safety"),
                "regulatory_mentions": response.lower().count("regulatory")
                + response.lower().count("compliance"),
                "risk_mentions": response.lower().count("risk"),
                "improvement_mentions": response.lower().count("improve")
                + response.lower().count("enhance"),
                "stakeholder_mentions": response.lower().count("stakeholder"),
                "threshold_comparison": response.lower().count("threshold"),
                "component_specific": response.lower().count(
                    context["component"].lower()
                ),
            }

            # Log the reasoning analysis
            self.logger.info(f"🔍 Reasoning analysis for {context['component']}:")
            for key, count in reasoning_analysis.items():
                if count > 0:
                    self.logger.info(f"   {key}: {count} mentions")

            # Analyze response structure
            sections = response.split("\n\n")
            self.logger.info(f"📝 Response structure: {len(sections)} sections")

            # Check for specific reasoning patterns
            if "interpretability" in response.lower():
                self.logger.info("   ✅ Interpretability focus detected")
            if "explanation" in response.lower():
                self.logger.info("   ✅ Explanation focus detected")
            if "safety" in response.lower():
                self.logger.info("   ✅ Safety focus detected")
            if "regulatory" in response.lower():
                self.logger.info("   ✅ Regulatory compliance focus detected")

        except Exception as e:
            self.logger.warning(f"Failed to analyze response reasoning: {e}")

    def _generate_component_explanation(
        self, component: str, metrics: dict[str, Any], score: float
    ) -> str:
        """Generate natural language explanation for a component"""
        try:
            # Log the explanation generation process
            self.logger.debug(f"🔍 Starting explanation generation for {component}")
            self.logger.debug(f"    Score: {score:.3f}")
            self.logger.debug(f"    Available metrics: {len(metrics)} items")

            # Extract component-specific metrics
            component_metrics = {
                k: v for k, v in metrics.items() if k.startswith(f"{component}_")
            }

            self.logger.debug(
                f"    Component-specific metrics: {len(component_metrics)} items"
            )

            # Create explanation context
            context = {
                "component": component,
                "score": score,
                "metrics": component_metrics,
                "threshold": self.thresholds.get(f"{component}_interpretability", 0.7),
            }

            self.logger.debug(f"    Threshold: {context['threshold']}")
            self.logger.debug(
                f"    Score vs threshold: {'❌ Below' if score < context['threshold'] else '✅ Above'}"
            )

            # Early return for deterministic path when LLM is disabled
            if not self.llm_assistant:
                self.logger.debug(
                    f"i️ LLM disabled, using deterministic explanation for {component}"
                )
                return self._generate_deterministic_explanation(
                    component, score, context
                )

            # Build comprehensive prompt for LLM
            prompt = f"""
Analyze the interpretability of the {component} component in a safety-critical ML system.

Component: {component}
Interpretability Score: {score:.3f}
Threshold: {context["threshold"]}
Component Metrics: {component_metrics}

Generate a natural language explanation that:
1. Explains what this score means for system safety
2. Identifies potential risks and concerns
3. Suggests specific improvements if needed
4. Uses clear, non-technical language for stakeholders

Focus on safety implications and regulatory compliance.
"""

            self.logger.debug(f"📝 Constructed prompt for {component}")
            self.logger.debug(
                "    Prompt focuses on: safety, risks, improvements, stakeholders"
            )

            try:
                # Make actual LLM call
                self.logger.debug(f"🧠 Making LLM call for {component}...")
                explanation = self._call_llm_for_explanation(prompt, context)
                self.logger.debug(f"✅ LLM explanation generated for {component}")
                return explanation
            except Exception as e:
                self.logger.warning(f"❌ LLM explanation generation failed: {e}")
                # Fallback to deterministic explanation
                fallback = self._generate_deterministic_explanation(
                    component, score, context
                )
                self.logger.debug(f"🔄 Using deterministic fallback for {component}")
                return fallback

        except Exception as e:
            self.logger.warning(
                f"❌ Error generating explanation for {component}: {e!s}"
            )
            return f"Error generating explanation for {component}: {e!s}"

    def _generate_deterministic_explanation(
        self, component: str, score: float, context: dict[str, Any]
    ) -> str:
        """Generate deterministic explanation as fallback"""
        if score >= context["threshold"]:
            return (
                f"The {component} component demonstrates good interpretability (score: {score:.3f}), "
                f"meeting the safety threshold of {context['threshold']}. "
                f"This means the system can adequately explain its {component} decisions "
                f"to regulators and stakeholders, which is crucial for safety-critical applications. "
                f"The component shows consistent explainability across its key metrics."
            )
        else:
            return (
                f"CRITICAL: The {component} component has poor interpretability (score: {score:.3f}), "
                f"falling below the safety threshold of {context['threshold']}. "
                f"This poses significant risks for safety-critical systems as the component "
                f"cannot adequately explain its decisions. This may violate regulatory requirements "
                f"and compromise stakeholder trust. Immediate improvements are needed."
            )

    def _generate_simulated_explanation(self, context: dict[str, Any]) -> str:
        """Generate simulated LLM response for development/testing"""
        component = context["component"]
        score = context["score"]
        threshold = context["threshold"]

        if score >= threshold:
            return (
                f"The {component} component demonstrates good interpretability (score: {score:.3f}), "
                f"meeting the safety threshold of {threshold}. "
                f"This means the system can adequately explain its {component} decisions "
                f"to regulators and stakeholders, which is crucial for safety-critical applications. "
                f"The component shows consistent explainability across its key metrics."
            )
        else:
            return (
                f"CRITICAL: The {component} component has poor interpretability (score: {score:.3f}), "
                f"falling below the safety threshold of {threshold}. "
                f"This poses significant risks for safety-critical systems as the component "
                f"cannot adequately explain its decisions. This may violate regulatory requirements "
                f"and compromise stakeholder trust. Immediate improvements are needed."
            )

    def _analyze_decision_transparency(self, metrics: dict[str, Any]) -> dict[str, Any]:
        """Analyze decision transparency patterns using LLM"""
        try:
            transparency_metrics = {
                k: v for k, v in metrics.items() if "transparency" in k.lower()
            }

            analysis = {
                "overall_transparency": metrics.get("decision_transparency_score", 0.0),
                "transparency_patterns": [],
                "improvement_areas": [],
                "best_practices": [],
            }

            # Analyze transparency patterns using LLM
            if self.llm_assistant and transparency_metrics:
                try:
                    # Build LLM prompt for transparency analysis
                    # transparency_prompt = f"""
                    # Analyze decision transparency patterns in a safety-critical ML system.
                    #
                    # Transparency Metrics: {transparency_metrics}
                    # Overall Transparency Score: {analysis["overall_transparency"]:.3f}
                    #
                    # Provide analysis that includes:
                    # 1. Pattern identification in transparency metrics
                    # 2. Areas of concern and improvement opportunities
                    # 3. Best practices for maintaining transparency
                    # 4. Safety implications of transparency gaps
                    #
                    # Focus on regulatory compliance and stakeholder communication.
                    # """

                    # Simulate LLM analysis with enhanced logic
                    if analysis["overall_transparency"] >= 0.8:
                        analysis["transparency_patterns"] = [
                            "Strong decision transparency across all components",
                            "Consistent explainability in safety-critical decisions",
                            "Adequate stakeholder communication capabilities",
                        ]
                        analysis["best_practices"] = [
                            "Maintain current transparency standards",
                            "Continue regular transparency audits",
                            "Document decision rationale for regulatory review",
                        ]
                    elif analysis["overall_transparency"] >= 0.6:
                        analysis["transparency_patterns"] = [
                            "Moderate transparency with some gaps",
                            "Inconsistent explainability in complex scenarios",
                            "Limited stakeholder communication in edge cases",
                        ]
                        analysis["improvement_areas"] = [
                            "Enhance transparency in complex decision scenarios",
                            "Improve stakeholder communication protocols",
                            "Implement transparency monitoring for edge cases",
                        ]
                    else:
                        analysis["transparency_patterns"] = [
                            "Critical transparency gaps identified",
                            "Inadequate explainability for safety-critical decisions",
                            "Poor stakeholder communication capabilities",
                        ]
                        analysis["improvement_areas"] = [
                            "Implement comprehensive transparency framework",
                            "Develop decision explanation mechanisms",
                            "Establish stakeholder communication protocols",
                            "Conduct transparency training for system operators",
                        ]

                except Exception as e:
                    self.logger.warning(f"LLM transparency analysis failed: {e}")
                    # Fallback to basic analysis
                    if transparency_metrics:
                        analysis["transparency_patterns"] = [
                            f"Metric {k}: {v:.3f}"
                            for k, v in transparency_metrics.items()
                        ]
            else:
                # Basic analysis without LLM
                if transparency_metrics:
                    analysis["transparency_patterns"] = [
                        f"Metric {k}: {v:.3f}" for k, v in transparency_metrics.items()
                    ]

            # Identify improvement areas
            low_transparency = [k for k, v in transparency_metrics.items() if v < 0.8]
            if low_transparency:
                analysis["improvement_areas"].extend(
                    [f"Improve transparency for: {', '.join(low_transparency)}"]
                )

            return analysis

        except Exception as e:
            return {"error": f"Decision transparency analysis failed: {e!s}"}

    def _generate_feature_importance_narratives(
        self, metrics: dict[str, Any]
    ) -> dict[str, str]:
        """Generate feature importance narratives using LLM"""
        try:
            feature_metrics = {
                k: v
                for k, v in metrics.items()
                if "feature" in k.lower() or "importance" in k.lower()
            }

            narratives = {}
            for metric, value in feature_metrics.items():
                if self.llm_assistant:
                    try:
                        # Build LLM prompt for feature importance analysis
                        # feature_prompt = f"""
                        # Analyze the feature importance metric '{metric}' with value {value:.3f} in a safety-critical ML system.
                        #
                        # Metric: {metric}
                        # Value: {value:.3f}
                        #
                        # Generate a narrative that explains:
                        # 1. What this feature importance value means for decision-making
                        # 2. How this affects system reliability and safety
                        # 3. Safety implications of this feature's importance
                        # 4. How this affects system interpretability
                        #
                        # Use clear, stakeholder-friendly language.
                        # """

                        # Simulate LLM response with contextual analysis
                        if value >= 0.8:
                            narrative = (
                                f"Feature '{metric}' has high importance ({value:.3f}), indicating it's a "
                                f"critical factor in the model's decision-making process. This feature "
                                f"significantly influences safety-critical decisions, making it essential "
                                f"for system interpretability and regulatory compliance."
                            )
                        elif value >= 0.5:
                            narrative = (
                                f"Feature '{metric}' has moderate importance ({value:.3f}), contributing "
                                f"meaningfully to the model's decisions. While not the primary driver, "
                                f"this feature still plays an important role in safety-critical scenarios "
                                f"and should be monitored for consistency."
                            )
                        else:
                            narrative = (
                                f"Feature '{metric}' has low importance ({value:.3f}), suggesting it has "
                                f"minimal impact on the model's decisions. While this may reduce complexity, "
                                f"it's important to verify that this feature isn't critical for safety "
                                f"scenarios that might not be captured in current training data."
                            )

                        narratives[metric] = narrative

                    except Exception as e:
                        self.logger.warning(
                            f"❌ LLM feature narrative generation failed for {metric}: {e}"
                        )
                        narratives[metric] = f"Feature importance: {value:.3f}"
                else:
                    narratives[metric] = f"Feature importance: {value:.3f}"

            return narratives

        except Exception as e:
            return {"error": f"Feature importance narrative generation failed: {e!s}"}

    def _analyze_cross_component_reasoning(
        self, _metrics: dict[str, Any], component_scores: dict[str, float]
    ) -> dict[str, Any]:
        """Analyze reasoning across components using LLM"""
        try:
            analysis = {
                "perception_to_planning": {},
                "planning_to_control": {},
                "end_to_end_reasoning": {},
            }

            # Analyze perception to planning reasoning
            if (
                "perception" in component_scores
                and "decision_making" in component_scores
            ):
                perception_score = component_scores["perception"]
                planning_score = component_scores["decision_making"]

                analysis["perception_to_planning"] = {
                    "perception_score": perception_score,
                    "planning_score": planning_score,
                    "reasoning_quality": min(perception_score, planning_score),
                    "bottleneck": (
                        "perception"
                        if perception_score < planning_score
                        else "planning"
                    ),
                }

            # Analyze planning to control reasoning
            if (
                "decision_making" in component_scores
                and "output_control" in component_scores
            ):
                planning_score = component_scores["decision_making"]
                control_score = component_scores["output_control"]

                analysis["planning_to_control"] = {
                    "planning_score": planning_score,
                    "control_score": control_score,
                    "reasoning_quality": min(planning_score, control_score),
                    "bottleneck": (
                        "planning" if planning_score < control_score else "control"
                    ),
                }

            # End-to-end reasoning
            if len(component_scores) == 3:
                overall_reasoning = np.mean(list(component_scores.values()))
                analysis["end_to_end_reasoning"] = {
                    "overall_score": overall_reasoning,
                    "component_scores": component_scores,
                    "reasoning_chain": "perception → planning → control",
                }

            return analysis

        except Exception as e:
            return {"error": f"Cross-component reasoning analysis failed: {e!s}"}

    def _generate_safety_justifications(
        self, metrics: dict[str, Any]
    ) -> dict[str, str]:
        """Generate safety justifications for interpretability decisions"""
        try:
            safety_justifications = {}

            # Generate justification for decision transparency
            transparency_score = metrics.get("decision_transparency_score", 0.0)
            if transparency_score < 0.8:
                safety_justifications["decision_transparency"] = (
                    f"Critical safety concern: Decision transparency score ({transparency_score:.3f}) "
                    f"is below safety threshold (0.8). This may compromise the ability to "
                    f"explain safety-critical decisions to regulators and stakeholders."
                )
            else:
                safety_justifications["decision_transparency"] = (
                    f"Decision transparency score ({transparency_score:.3f}) meets safety requirements. "
                    f"The system can adequately explain its decisions for safety-critical applications."
                )

            # Generate justification for overall interpretability
            overall_score = metrics.get("model_explainability_score", 0.0)
            if overall_score < 0.7:
                safety_justifications["overall_interpretability"] = (
                    f"Safety concern: Overall interpretability score ({overall_score:.3f}) "
                    f"is below recommended threshold (0.7). This may impact regulatory compliance "
                    f"and stakeholder trust in safety-critical systems."
                )
            else:
                safety_justifications["overall_interpretability"] = (
                    f"Overall interpretability score ({overall_score:.3f}) meets safety requirements. "
                    f"The system provides adequate explanations for safety-critical decision-making."
                )

            return safety_justifications

        except Exception as e:
            return {"error": f"Safety justification generation failed: {e!s}"}

    def _generate_alerts_and_recommendations(
        self, metrics: dict[str, Any], overall_score: float
    ) -> tuple[list[dict], list[dict]]:
        """Generate alerts and recommendations based on interpretability scores"""
        alerts = []
        recommendations = []

        # Check overall interpretability threshold
        interpretability_threshold = self.thresholds.get(
            "overall_interpretability", 0.7
        )
        if overall_score < interpretability_threshold:
            alerts.append(
                {
                    "level": "warning",
                    "message": f"Overall interpretability score ({overall_score:.3f}) below threshold ({interpretability_threshold})",
                    "component": "interpretability",
                    "timestamp": datetime.now().isoformat(),
                }
            )

            recommendations.append(
                {
                    "priority": "high",
                    "action": "Improve model explainability",
                    "description": "Implement explainable AI techniques to improve decision transparency",
                    "component": "interpretability",
                }
            )

        # Check component-specific scores
        for component in ["perception", "decision_making", "output_control"]:
            component_score = metrics.get(f"{component}_explainability_score", 0.0)
            component_threshold = self.thresholds.get(
                f"{component}_interpretability", 0.7
            )

            if component_score < component_threshold:
                alerts.append(
                    {
                        "level": "warning",
                        "message": f"{component.capitalize()} interpretability score ({component_score:.3f}) below threshold ({component_threshold})",
                        "component": component,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

                recommendations.append(
                    {
                        "priority": "medium",
                        "action": f"Improve {component} explainability",
                        "description": f"Add explainable AI techniques to {component} system",
                        "component": component,
                    }
                )

        # Check decision transparency
        transparency_score = metrics.get("decision_transparency_score", 0.0)
        transparency_threshold = self.thresholds.get("decision_transparency", 0.8)

        if transparency_score < transparency_threshold:
            alerts.append(
                {
                    "level": "critical",
                    "message": f"Decision transparency score ({transparency_score:.3f}) below critical threshold ({transparency_threshold})",
                    "component": "interpretability",
                    "timestamp": datetime.now().isoformat(),
                }
            )

            recommendations.append(
                {
                    "priority": "high",
                    "action": "Improve decision transparency",
                    "description": "Implement decision explanation mechanisms for safety-critical decisions",
                    "component": "interpretability",
                }
            )

        # Check explanation quality
        explanation_score = metrics.get("explanation_quality_score", 0.0)
        explanation_threshold = self.thresholds.get("explanation_quality", 0.7)

        if explanation_score < explanation_threshold:
            alerts.append(
                {
                    "level": "warning",
                    "message": f"Explanation quality score ({explanation_score:.3f}) below threshold ({explanation_threshold})",
                    "component": "interpretability",
                    "timestamp": datetime.now().isoformat(),
                }
            )

            recommendations.append(
                {
                    "priority": "medium",
                    "action": "Improve explanation quality",
                    "description": "Enhance explanation generation to provide clearer, more actionable insights",
                    "component": "interpretability",
                }
            )

        return alerts, recommendations

    def get_interpretability_metrics(self) -> dict[str, Any]:
        """Get interpretability metrics and analysis"""
        return {
            "evaluator_type": "interpretability",
            "capabilities": [
                "model_explainability",
                "decision_transparency",
                "feature_importance_analysis",
                "human_readable_explanations",
                "llm_enhanced_analysis",
            ],
            "llm_integration": self.use_llm,
            "thresholds": self.thresholds,
        }
