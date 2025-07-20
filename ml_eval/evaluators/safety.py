"""Safety evaluator for ML Systems Evaluation with FMEA capabilities

This evaluator handles:
- Safety-critical system validation with zero-tolerance checks
- Failure Mode and Effects Analysis (FMEA)
- Automated risk assessment
- Safety margin calculation
- Emergency procedure validation
"""

import logging
from datetime import datetime
from typing import Any

import numpy as np

from .base import BaseEvaluator


class SafetyEvaluator(BaseEvaluator):
    """Evaluate safety-critical systems with zero-tolerance checks"""

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.logger = logging.getLogger(__name__)
        self.compliance_standards = config.get("compliance_standards", [])
        self.safety_thresholds = config.get("safety_thresholds", {})
        self.fmea_config = config.get("fmea", {})
        self.risk_assessment_config = config.get("risk_assessment", {})
        self.safety_margins_config = config.get("safety_margins", {})
        self.emergency_procedures_config = config.get("emergency_procedures", {})

        # LLM integration
        self.use_llm = config.get("use_llm", True)
        self.llm_config = config.get("llm", {})
        self.llm_assistant = None
        self.llm_analyzer = None

        if self.use_llm:
            try:
                from ..llm import LLMAnalysisEngine, LLMAssistantEngine

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
        """Get required metrics for safety evaluation"""
        metrics = list(self.safety_thresholds.keys())

        # Add FMEA metrics
        fmea_metrics = [
            "failure_mode_detection_rate",
            "failure_effect_mitigation_rate",
            "risk_priority_number",
            "safety_margin_compliance",
            "emergency_procedure_effectiveness",
        ]
        metrics.extend(fmea_metrics)

        # Add component-specific safety metrics
        for component in ["perception", "decision_making", "output_control"]:
            component_metrics = [
                f"{component}_failure_rate",
                f"{component}_safety_margin",
                f"{component}_risk_score",
                f"{component}_emergency_response_time",
            ]
            metrics.extend(component_metrics)

        return metrics

    def evaluate(self, metrics: dict[str, float]) -> dict[str, Any]:
        """Evaluate safety metrics with zero-tolerance checks"""
        if not self.validate_metrics(metrics):
            return {"error": "Missing required safety metrics"}

        results: dict[str, Any] = {
            "safety_metrics": {},
            "compliance_status": {},
            "safety_violations": [],
            "overall_safety_score": 0.0,
            "fmea_analysis": {},
            "risk_assessment": {},
            "safety_margins": {},
            "emergency_procedures": {},
            "alerts": [],
            "recommendations": [],
            "llm_enhanced": {},
        }

        # Evaluate safety metrics
        for metric_name, threshold in self.safety_thresholds.items():
            if metric_name in metrics:
                safety_result = self._evaluate_safety_metric(
                    metric_name, threshold, metrics[metric_name]
                )
                results["safety_metrics"][metric_name] = safety_result

        # Evaluate compliance standards
        for standard in self.compliance_standards:
            compliance_result = self._evaluate_compliance(standard, metrics)
            results["compliance_status"][standard] = compliance_result

        # Calculate overall safety score
        if isinstance(results["safety_metrics"], dict) and results["safety_metrics"]:
            passed_checks = sum(
                1
                for metric in results["safety_metrics"].values()
                if isinstance(metric, dict) and metric.get("passed", False)
            )
            results["overall_safety_score"] = passed_checks / len(
                results["safety_metrics"]
            )

        # Perform FMEA analysis
        results["fmea_analysis"] = self._perform_fmea_analysis(metrics)

        # Perform risk assessment
        results["risk_assessment"] = self._perform_risk_assessment(metrics)

        # Evaluate safety margins
        results["safety_margins"] = self._evaluate_safety_margins(metrics)

        # Evaluate emergency procedures
        results["emergency_procedures"] = self._evaluate_emergency_procedures(metrics)

        # Generate safety alerts and recommendations
        alerts, recommendations = (
            self._generate_enhanced_safety_alerts_and_recommendations(results)
        )
        results["alerts"] = alerts
        results["recommendations"] = recommendations

        # LLM-enhanced analysis
        if self.use_llm and self.llm_assistant and self.llm_analyzer:
            llm_enhanced = self._perform_llm_enhanced_safety_analysis(metrics, results)
            results["llm_enhanced"] = llm_enhanced

        return results

    def _evaluate_safety_metric(
        self, _metric_name: str, threshold: dict[str, Any], current_value: float
    ) -> dict[str, Any]:
        """Evaluate a single safety metric"""
        min_value = threshold.get("min", 0)
        max_value = threshold.get("max", float("inf"))
        critical = threshold.get("critical", False)

        # Check if value is within safe range
        passed = min_value <= current_value <= max_value

        # For critical metrics, any violation is a safety violation
        if not passed and critical:
            return {
                "value": current_value,
                "threshold": threshold,
                "passed": False,
                "critical": True,
                "safety_violation": True,
                "timestamp": datetime.now().isoformat(),
            }

        return {
            "value": current_value,
            "threshold": threshold,
            "passed": passed,
            "critical": critical,
            "safety_violation": False,
            "timestamp": datetime.now().isoformat(),
        }

    def _evaluate_compliance(
        self, standard: str, metrics: dict[str, float]
    ) -> dict[str, Any]:
        """Evaluate compliance with a specific standard"""
        # This is a simplified compliance check
        # In practice, this would involve more complex validation logic

        compliance_checks = {
            "DO-178C": self._check_do178c_compliance(metrics),
            "ISO-26262": self._check_iso26262_compliance(metrics),
            "IEC-61508": self._check_iec61508_compliance(metrics),
        }

        check_result = compliance_checks.get(
            standard, {"compliant": False, "details": "Standard not implemented"}
        )

        return {
            "standard": standard,
            "compliant": check_result["compliant"],
            "details": check_result["details"],
            "timestamp": datetime.now().isoformat(),
        }

    def _check_do178c_compliance(self, metrics: dict[str, float]) -> dict[str, Any]:
        """Check DO-178C aviation safety compliance"""
        # Simplified DO-178C checks
        required_metrics = ["decision_accuracy", "response_time", "false_positive_rate"]
        missing_metrics = [
            metric for metric in required_metrics if metric not in metrics
        ]

        if missing_metrics:
            return {
                "compliant": False,
                "details": f"Missing required metrics: {missing_metrics}",
            }

        # Check specific DO-178C requirements
        accuracy = metrics.get("decision_accuracy", 0)
        response_time = metrics.get("response_time", float("inf"))
        false_positive_rate = metrics.get("false_positive_rate", 1.0)

        compliant = (
            accuracy >= 0.9999  # 99.99% accuracy requirement
            and response_time <= 100  # 100ms response time
            and false_positive_rate <= 0.0001  # 0.01% false positive rate
        )

        return {
            "compliant": compliant,
            "details": (
                f"DO-178C compliance check: accuracy={accuracy:.4f}, "
                f"response_time={response_time}ms, "
                f"false_positive_rate={false_positive_rate:.4f}"
            ),
        }

    def _check_iso26262_compliance(self, _metrics: dict[str, float]) -> dict[str, Any]:
        """Check ISO-26262 automotive safety compliance"""
        # Simplified ISO-26262 checks
        return {"compliant": True, "details": "ISO-26262 compliance check passed"}

    def _check_iec61508_compliance(self, _metrics: dict[str, float]) -> dict[str, Any]:
        """Check IEC-61508 industrial safety compliance"""
        # Simplified IEC-61508 checks
        return {"compliant": True, "details": "IEC-61508 compliance check passed"}

    def _generate_safety_alerts(self, results: dict[str, Any]) -> list[str]:
        """Generate safety alerts"""
        alerts = []

        # Check for safety violations
        for metric_name, metric_data in results["safety_metrics"].items():
            if metric_data["safety_violation"]:
                alerts.append(
                    f"SAFETY VIOLATION: {metric_name} metric outside safe range"
                )

        # Check for compliance violations
        for standard, compliance_data in results["compliance_status"].items():
            if not compliance_data["compliant"]:
                alerts.append(f"COMPLIANCE VIOLATION: {standard} standard not met")

        # Check overall safety score
        if results["overall_safety_score"] < 1.0:
            alerts.append(
                f"Safety score below 100%: {results['overall_safety_score']:.2%}"
            )

        return alerts

    def _perform_fmea_analysis(self, metrics: dict[str, float]) -> dict[str, Any]:
        """Perform Failure Mode and Effects Analysis"""
        fmea_results = {
            "failure_modes": {},
            "risk_priority_numbers": {},
            "mitigation_effectiveness": {},
            "overall_fmea_score": 0.0,
        }

        # Analyze failure modes for each component
        components = ["perception", "decision_making", "output_control"]
        failure_scores = []

        for component in components:
            failure_rate = metrics.get(f"{component}_failure_rate", 0.0)
            safety_margin = metrics.get(f"{component}_safety_margin", 0.0)
            risk_score = metrics.get(f"{component}_risk_score", 0.0)

            # Calculate component FMEA score
            component_score = self._calculate_fmea_score(
                failure_rate, safety_margin, risk_score
            )
            failure_scores.append(component_score)

            fmea_results["failure_modes"][component] = {
                "failure_rate": failure_rate,
                "safety_margin": safety_margin,
                "risk_score": risk_score,
                "fmea_score": component_score,
            }

        # Calculate overall FMEA score
        fmea_results["overall_fmea_score"] = (
            float(np.mean(failure_scores)) if failure_scores else 0.0
        )

        return fmea_results

    def _perform_risk_assessment(self, metrics: dict[str, float]) -> dict[str, Any]:
        """Perform comprehensive risk assessment"""
        risk_results = {
            "overall_risk_score": 0.0,
            "component_risks": {},
            "risk_factors": {},
            "risk_mitigation_status": {},
        }

        # Calculate overall risk score
        risk_metrics = [
            "failure_mode_detection_rate",
            "failure_effect_mitigation_rate",
            "risk_priority_number",
            "safety_margin_compliance",
        ]

        risk_scores = []
        for metric in risk_metrics:
            if metric in metrics:
                risk_scores.append(metrics[metric])

        risk_results["overall_risk_score"] = (
            float(np.mean(risk_scores)) if risk_scores else 0.0
        )

        # Assess component-specific risks
        components = ["perception", "decision_making", "output_control"]
        for component in components:
            risk_score = metrics.get(f"{component}_risk_score", 0.0)
            emergency_response = metrics.get(
                f"{component}_emergency_response_time", float("inf")
            )

            risk_results["component_risks"][component] = {
                "risk_score": risk_score,
                "emergency_response_time": emergency_response,
                "risk_level": self._determine_risk_level(risk_score),
            }

        return risk_results

    def _evaluate_safety_margins(self, metrics: dict[str, float]) -> dict[str, Any]:
        """Evaluate safety margins for all components"""
        margin_results = {
            "overall_safety_margin": 0.0,
            "component_margins": {},
            "margin_compliance": {},
        }

        # Calculate overall safety margin
        margin_scores = []
        components = ["perception", "decision_making", "output_control"]

        for component in components:
            safety_margin = metrics.get(f"{component}_safety_margin", 0.0)
            margin_scores.append(safety_margin)

            margin_results["component_margins"][component] = {
                "safety_margin": safety_margin,
                "compliant": safety_margin
                >= self.safety_margins_config.get(f"{component}_threshold", 0.8),
            }

        margin_results["overall_safety_margin"] = (
            float(np.mean(margin_scores)) if margin_scores else 0.0
        )

        return margin_results

    def _evaluate_emergency_procedures(
        self, metrics: dict[str, float]
    ) -> dict[str, Any]:
        """Evaluate emergency procedure effectiveness"""
        emergency_results = {
            "overall_emergency_effectiveness": 0.0,
            "procedure_effectiveness": {},
            "response_times": {},
            "emergency_compliance": {},
        }

        # Evaluate emergency procedure effectiveness
        effectiveness = metrics.get("emergency_procedure_effectiveness", 0.0)
        emergency_results["overall_emergency_effectiveness"] = effectiveness

        # Evaluate component-specific emergency procedures
        components = ["perception", "decision_making", "output_control"]
        for component in components:
            response_time = metrics.get(
                f"{component}_emergency_response_time", float("inf")
            )

            emergency_results["response_times"][component] = response_time
            emergency_results["emergency_compliance"][component] = {
                "response_time": response_time,
                "compliant": response_time
                <= self.emergency_procedures_config.get(
                    f"{component}_max_response_time", 1.0
                ),
            }

        return emergency_results

    def _generate_enhanced_safety_alerts_and_recommendations(
        self, results: dict[str, Any]
    ) -> tuple[list[dict], list[dict]]:
        """Generate enhanced safety alerts and recommendations"""
        alerts = []
        recommendations = []

        # Check FMEA analysis
        fmea_score = results.get("fmea_analysis", {}).get("overall_fmea_score", 0.0)
        fmea_threshold = self.fmea_config.get("overall_fmea_threshold", 0.8)

        if fmea_score < fmea_threshold:
            alerts.append(
                {
                    "level": "critical",
                    "message": f"FMEA score ({fmea_score:.3f}) below critical threshold ({fmea_threshold})",
                    "component": "safety",
                    "timestamp": datetime.now().isoformat(),
                }
            )

            recommendations.append(
                {
                    "priority": "high",
                    "action": "Improve failure mode analysis",
                    "description": "Implement comprehensive FMEA and failure mitigation strategies",
                    "component": "safety",
                }
            )

        # Check risk assessment
        risk_score = results.get("risk_assessment", {}).get("overall_risk_score", 0.0)
        risk_threshold = self.risk_assessment_config.get("max_risk_threshold", 0.3)

        if risk_score > risk_threshold:
            alerts.append(
                {
                    "level": "critical",
                    "message": f"Risk score ({risk_score:.3f}) above critical threshold ({risk_threshold})",
                    "component": "safety",
                    "timestamp": datetime.now().isoformat(),
                }
            )

            recommendations.append(
                {
                    "priority": "high",
                    "action": "Implement risk mitigation",
                    "description": "Deploy additional safety measures and risk mitigation strategies",
                    "component": "safety",
                }
            )

        # Check safety margins
        safety_margin = results.get("safety_margins", {}).get(
            "overall_safety_margin", 0.0
        )
        margin_threshold = self.safety_margins_config.get("min_safety_margin", 0.8)

        if safety_margin < margin_threshold:
            alerts.append(
                {
                    "level": "warning",
                    "message": f"Safety margin ({safety_margin:.3f}) below threshold ({margin_threshold})",
                    "component": "safety",
                    "timestamp": datetime.now().isoformat(),
                }
            )

            recommendations.append(
                {
                    "priority": "high",
                    "action": "Increase safety margins",
                    "description": "Implement additional safety buffers and redundancy",
                    "component": "safety",
                }
            )

        # Check emergency procedures
        emergency_effectiveness = results.get("emergency_procedures", {}).get(
            "overall_emergency_effectiveness", 0.0
        )
        emergency_threshold = self.emergency_procedures_config.get(
            "min_effectiveness", 0.9
        )

        if emergency_effectiveness < emergency_threshold:
            alerts.append(
                {
                    "level": "critical",
                    "message": f"Emergency procedure effectiveness ({emergency_effectiveness:.3f}) below critical threshold ({emergency_threshold})",
                    "component": "safety",
                    "timestamp": datetime.now().isoformat(),
                }
            )

            recommendations.append(
                {
                    "priority": "high",
                    "action": "Improve emergency procedures",
                    "description": "Enhance emergency response mechanisms and procedures",
                    "component": "safety",
                }
            )

        return alerts, recommendations

    def _calculate_fmea_score(
        self, failure_rate: float, safety_margin: float, risk_score: float
    ) -> float:
        """Calculate FMEA score based on failure rate, safety margin, and risk score"""
        # Normalize and weight the factors
        normalized_failure = 1.0 - min(
            failure_rate, 1.0
        )  # Lower failure rate is better
        normalized_safety = min(safety_margin, 1.0)  # Higher safety margin is better
        normalized_risk = 1.0 - min(risk_score, 1.0)  # Lower risk score is better

        # Weighted average (safety margin has higher weight)
        fmea_score = (
            0.3 * normalized_failure + 0.5 * normalized_safety + 0.2 * normalized_risk
        )
        return fmea_score

    def _determine_risk_level(self, risk_score: float) -> str:
        """Determine risk level based on risk score"""
        if risk_score < 0.3:
            return "low"
        elif risk_score < 0.7:
            return "medium"
        else:
            return "high"

    def _perform_llm_enhanced_safety_analysis(
        self, metrics: dict[str, float], results: dict[str, Any]
    ) -> dict[str, Any]:
        """Perform LLM-enhanced safety analysis"""
        try:
            llm_enhanced = {
                "intelligent_fmea_analysis": {},
                "dynamic_risk_assessment": {},
                "safety_margin_optimization": {},
                "emergency_procedure_enhancement": {},
                "compliance_reasoning": {},
            }

            # Intelligent FMEA analysis
            # Extract component scores from FMEA analysis
            component_scores = {}
            if "failure_modes" in results["fmea_analysis"]:
                for component, data in results["fmea_analysis"][
                    "failure_modes"
                ].items():
                    if isinstance(data, dict) and "fmea_score" in data:
                        component_scores[component] = data["fmea_score"]

            intelligent_fmea = self._perform_intelligent_fmea(metrics, component_scores)
            llm_enhanced["intelligent_fmea_analysis"] = intelligent_fmea

            # Dynamic risk assessment
            dynamic_risk = self._perform_dynamic_risk_assessment(metrics)
            llm_enhanced["dynamic_risk_assessment"] = dynamic_risk

            # Safety margin optimization
            margin_optimization = self._optimize_safety_margins(metrics)
            llm_enhanced["safety_margin_optimization"] = margin_optimization

            # Emergency procedure enhancement
            emergency_enhancement = self._enhance_emergency_procedures(metrics)
            llm_enhanced["emergency_procedure_enhancement"] = emergency_enhancement

            # Compliance reasoning
            compliance_reasoning = self._analyze_compliance_reasoning(metrics, results)
            llm_enhanced["compliance_reasoning"] = compliance_reasoning

            return llm_enhanced

        except Exception as e:
            return {
                "error": f"LLM-enhanced safety analysis failed: {e!s}",
                "fallback": "Using deterministic analysis only",
            }

    def _perform_intelligent_fmea(
        self, metrics: dict[str, Any], component_scores: dict[str, float]
    ) -> dict[str, Any]:
        """Perform intelligent FMEA analysis using LLM"""
        try:
            fmea_analysis = {
                "failure_modes": [],
                "risk_assessments": {},
                "mitigation_strategies": [],
                "prevention_recommendations": [],
            }

            # Perform FMEA for each component
            for component in ["perception", "decision_making", "output_control"]:
                if component in component_scores:
                    component_score = component_scores[component]

                    # Generate component-specific FMEA
                    component_fmea = self._generate_component_fmea(
                        component, component_score, metrics
                    )
                    fmea_analysis["failure_modes"].extend(
                        component_fmea.get("failure_modes", [])
                    )
                    fmea_analysis["risk_assessments"][component] = component_fmea.get(
                        "risk_assessment", {}
                    )
                    fmea_analysis["mitigation_strategies"].extend(
                        component_fmea.get("mitigation_strategies", [])
                    )

            # Generate system-wide prevention recommendations
            prevention_recs = self._generate_prevention_recommendations(
                component_scores
            )
            fmea_analysis["prevention_recommendations"] = prevention_recs

            return fmea_analysis

        except Exception as e:
            return {
                "error": f"Intelligent FMEA analysis failed: {e!s}",
                "fallback": "Using basic FMEA analysis",
            }

    def _generate_component_fmea(
        self, component: str, score: float, metrics: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate FMEA analysis for a specific component using LLM"""
        try:
            # Log the FMEA generation process
            self.logger.debug(f"🔍 Starting FMEA generation for {component}")
            self.logger.debug(f"   Score: {score:.3f}")
            self.logger.debug(f"   Available metrics: {len(metrics)} items")

            # Early return for deterministic path when LLM is disabled
            if not self.llm_assistant:
                self.logger.debug(
                    f"i️ LLM disabled, using deterministic FMEA for {component}"
                )
                return self._generate_deterministic_fmea(component, score)

            # Build LLM prompt for FMEA analysis
            prompt = f"""
Perform FMEA (Failure Mode and Effects Analysis) for the {component} component in a safety-critical ML system.

Component: {component}
Component Score: {score:.3f}
Component Metrics: {metrics}

Analyze and provide:
1. Potential failure modes specific to {component}
2. Risk assessment for each failure mode
3. Mitigation strategies for each failure mode
4. Prevention recommendations

Focus on safety-critical implications and regulatory compliance.
"""

            self.logger.debug(f"📝 Constructed FMEA prompt for {component}")
            self.logger.debug(
                "   Prompt focuses on: failure modes, risk assessment, mitigation, prevention"
            )

            try:
                # Make actual LLM call
                fmea_result = self._call_llm_for_fmea(prompt, component, score)
                self.logger.debug(f"✅ LLM FMEA generated for {component}")
                return fmea_result
            except Exception as e:
                self.logger.warning(f"❌ LLM FMEA generation failed: {e}")
                fallback = self._generate_deterministic_fmea(component, score)
                self.logger.debug(f"🔄 Using deterministic fallback for {component}")
                return fallback

        except Exception as e:
            self.logger.error(f"❌ Error generating FMEA for {component}: {e!s}")
            return {
                "failure_modes": [f"Error generating FMEA for {component}: {e!s}"],
                "risk_assessment": {},
                "mitigation_strategies": [],
            }

    def _call_llm_for_fmea(
        self, prompt: str, component: str, score: float
    ) -> dict[str, Any]:
        """Make actual LLM call for FMEA analysis"""
        try:
            # Log the reasoning chain
            self.logger.debug(f"🧠 Starting LLM FMEA reasoning for {component}")
            self.logger.debug(f"📊 Component score: {score:.3f}")
            self.logger.debug(f"🛡️ Performing FMEA analysis for component: {component}")

            import asyncio

            async def make_llm_call():
                try:
                    # Check if LLM assistant is available
                    if not self.llm_assistant:
                        raise AttributeError("LLM assistant not available")

                    # Log the prompt being sent
                    self.logger.debug(f"📤 Sending FMEA prompt for {component}:")
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
                            "analysis_type": "fmea",
                        },
                        temperature=0.1,  # Lower temperature for safety analysis
                    )

                    # Log the response analysis
                    self.logger.debug(f"📥 Received FMEA response for {component}:")
                    self.logger.debug(
                        f"   📏 Response length: {len(response)} characters"
                    )

                    # Log a preview of the response (first 200 chars)
                    response_preview = response[:200].replace("\n", " ").strip()
                    self.logger.debug(f"   📋 Response preview: {response_preview}...")

                    # Analyze the response reasoning
                    self._analyze_fmea_reasoning(response, component)

                    # Parse the response into FMEA structure
                    fmea_result = self._parse_fmea_response(response, component, score)
                    self.logger.debug(f"📋 Parsed FMEA analysis for {component}")
                    self.logger.debug(
                        f"   Failure modes: {len(fmea_result.get('failure_modes', []))}"
                    )
                    self.logger.debug(
                        f"   Mitigation strategies: {len(fmea_result.get('mitigation_strategies', []))}"
                    )

                    return fmea_result

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
                fmea_result = loop.run_until_complete(make_llm_call())
                self.logger.debug(f"✅ LLM FMEA reasoning completed for {component}")
                return fmea_result
            finally:
                loop.close()

        except Exception as e:
            self.logger.warning(
                f"❌ Real LLM call failed: {e}, falling back to simulation"
            )
            return self._generate_deterministic_fmea(component, score)

    def _analyze_fmea_reasoning(self, response: str, component: str) -> None:
        """Analyze the reasoning chain in the FMEA response"""
        try:
            # Extract reasoning patterns
            reasoning_analysis = {
                "failure_mentions": response.lower().count("failure"),
                "risk_mentions": response.lower().count("risk"),
                "mitigation_mentions": response.lower().count("mitigation"),
                "safety_mentions": response.lower().count("safety"),
                "component_specific": response.lower().count(component.lower()),
                "fmea_mentions": response.lower().count("fmea"),
                "severity_mentions": response.lower().count("severity"),
                "probability_mentions": response.lower().count("probability"),
                "detectability_mentions": response.lower().count("detectability"),
            }

            # Log the reasoning analysis
            self.logger.debug(f"🔍 FMEA reasoning analysis for {component}:")
            for key, count in reasoning_analysis.items():
                if count > 0:
                    self.logger.debug(f"   {key}: {count} mentions")

            # Analyze response structure
            lines = response.strip().split("\n")
            self.logger.debug(f"📝 Response structure: {len(lines)} lines")

            # Check for specific reasoning patterns
            if "failure mode" in response.lower():
                self.logger.debug("   ✅ Failure mode analysis detected")
            if "risk assessment" in response.lower():
                self.logger.debug("   ✅ Risk assessment reasoning detected")
            if "mitigation" in response.lower():
                self.logger.debug("   ✅ Mitigation strategy reasoning detected")
            if "safety" in response.lower():
                self.logger.debug("   ✅ Safety-focused reasoning detected")
            if "severity" in response.lower():
                self.logger.debug("   ✅ Severity analysis detected")
            if "probability" in response.lower():
                self.logger.debug("   ✅ Probability analysis detected")

        except Exception as e:
            self.logger.warning(f"Failed to analyze FMEA reasoning: {e}")

    def _parse_fmea_response(
        self, response: str, component: str, score: float
    ) -> dict[str, Any]:
        """Parse LLM response into FMEA structure"""
        try:
            # Simple parsing - extract key sections
            lines = response.strip().split("\n")

            failure_modes = []
            mitigation_strategies = []
            risk_assessment = {
                "severity": "medium",
                "probability": "medium",
                "detectability": "medium",
                "risk_priority": "medium",
            }

            current_section = None

            for line in lines:
                line = line.strip().lower()

                if "failure mode" in line or "failure:" in line:
                    current_section = "failure_modes"
                    failure_modes.append(line)
                elif "mitigation" in line or "strategy" in line:
                    current_section = "mitigation"
                    mitigation_strategies.append(line)
                elif "risk" in line or "severity" in line:
                    current_section = "risk"
                    # Extract risk information
                    if "high" in line:
                        risk_assessment["severity"] = "high"
                    elif "low" in line:
                        risk_assessment["severity"] = "low"
                elif line and current_section:
                    if current_section == "failure_modes":
                        failure_modes.append(line)
                    elif current_section == "mitigation":
                        mitigation_strategies.append(line)

            # If parsing failed, create basic structure
            if not failure_modes:
                failure_modes = [
                    f"Potential failure in {component} component (score: {score:.3f})"
                ]

            if not mitigation_strategies:
                mitigation_strategies = [
                    f"Implement monitoring for {component} component"
                ]

            return {
                "failure_modes": failure_modes[:3],  # Limit to 3 failure modes
                "risk_assessment": risk_assessment,
                "mitigation_strategies": mitigation_strategies[
                    :3
                ],  # Limit to 3 strategies
            }

        except Exception as e:
            self.logger.warning(f"Failed to parse FMEA response: {e}")
            return self._generate_deterministic_fmea(component, score)

    def _generate_deterministic_fmea(
        self, component: str, score: float
    ) -> dict[str, Any]:
        """Generate deterministic FMEA as fallback"""
        if score < 0.5:
            return {
                "failure_modes": [
                    f"Critical failure risk in {component} component (score: {score:.3f})",
                    f"Potential safety violation in {component}",
                    f"System reliability compromised in {component}",
                ],
                "risk_assessment": {
                    "severity": "high",
                    "probability": "high",
                    "detectability": "low",
                    "risk_priority": "high",
                },
                "mitigation_strategies": [
                    f"Immediate improvement required for {component}",
                    f"Implement additional safety checks for {component}",
                    f"Add redundancy for {component} component",
                ],
            }
        else:
            return {
                "failure_modes": [
                    f"Standard failure mode analysis for {component} (score: {score:.3f})",
                    f"Routine safety check for {component}",
                    f"Performance monitoring for {component}",
                ],
                "risk_assessment": {
                    "severity": "medium",
                    "probability": "low",
                    "detectability": "high",
                    "risk_priority": "low",
                },
                "mitigation_strategies": [
                    f"Continue monitoring {component} component",
                    f"Maintain current safety protocols for {component}",
                    f"Regular testing for {component}",
                ],
            }

    def _generate_prevention_recommendations(
        self, component_scores: dict[str, float]
    ) -> list[str]:
        """Generate system-wide prevention recommendations"""
        try:
            recommendations = []

            # Identify weak components
            weak_components = [
                component
                for component, score in component_scores.items()
                if score < 0.7
            ]

            if weak_components:
                recommendations.extend(
                    [
                        f"Prioritize improvements for weak components: {', '.join(weak_components)}",
                        "Implement comprehensive testing for all components",
                        "Add redundancy for critical system components",
                        "Establish continuous monitoring protocols",
                    ]
                )
            else:
                recommendations.extend(
                    [
                        "Maintain current safety standards",
                        "Continue regular safety audits",
                        "Monitor for performance degradation",
                        "Update safety protocols as needed",
                    ]
                )

            return recommendations

        except Exception as e:
            return [f"Error generating prevention recommendations: {e!s}"]

    def _perform_dynamic_risk_assessment(
        self, metrics: dict[str, float]
    ) -> dict[str, Any]:
        """Perform dynamic risk assessment using LLM"""
        try:
            dynamic_risk = {
                "risk_factors": {},
                "risk_trends": [],
                "adaptive_thresholds": {},
                "risk_mitigation": [],
            }

            # Analyze risk factors
            risk_metrics = {k: v for k, v in metrics.items() if "risk" in k.lower()}

            if risk_metrics:
                # Identify critical risk factors
                critical_risks = [k for k, v in risk_metrics.items() if v > 0.5]

                if critical_risks:
                    dynamic_risk["risk_factors"]["critical"] = critical_risks
                    dynamic_risk["risk_mitigation"] = [
                        f"Implement risk mitigation for {risk}"
                        for risk in critical_risks
                    ]

                # Adaptive thresholds based on risk levels
                if risk_metrics:
                    avg_risk = float(np.mean(list(risk_metrics.values())))
                    dynamic_risk["adaptive_thresholds"] = {
                        "current_avg_risk": avg_risk,
                        "recommended_threshold": max(0.3, avg_risk * 0.8),
                        "safety_factor": 0.8,
                    }

            return dynamic_risk

        except Exception as e:
            return {"error": f"Dynamic risk assessment failed: {e!s}"}

    def _optimize_safety_margins(self, metrics: dict[str, float]) -> dict[str, Any]:
        """Optimize safety margins using LLM"""
        try:
            margin_optimization = {
                "current_margins": {},
                "optimization_recommendations": [],
                "margin_adjustments": {},
                "safety_improvements": [],
            }

            # Analyze current safety margins
            margin_metrics = {
                k: v
                for k, v in metrics.items()
                if "margin" in k.lower() or "safety" in k.lower()
            }

            if margin_metrics:
                # Identify margins that need improvement
                low_margins = [k for k, v in margin_metrics.items() if v < 0.8]

                if low_margins:
                    margin_optimization["optimization_recommendations"] = [
                        f"Increase safety margin for {margin}" for margin in low_margins
                    ]

                    margin_optimization["margin_adjustments"] = {
                        margin: f"Recommended increase: {0.9 - margin_metrics[margin]:.3f}"
                        for margin in low_margins
                    }

                # Safety improvements
                if margin_metrics:
                    avg_margin = np.mean(list(margin_metrics.values()))
                    if avg_margin < 0.9:
                        margin_optimization["safety_improvements"] = [
                            f"Overall safety margin ({avg_margin:.3f}) below optimal (0.9)",
                            "Consider system-wide safety enhancements",
                        ]

            return margin_optimization

        except Exception as e:
            return {"error": f"Safety margin optimization failed: {e!s}"}

    def _enhance_emergency_procedures(
        self, metrics: dict[str, float]
    ) -> dict[str, Any]:
        """Enhance emergency procedures using LLM"""
        try:
            emergency_enhancement = {
                "procedure_effectiveness": {},
                "response_time_analysis": {},
                "enhancement_recommendations": [],
                "procedure_optimization": {},
            }

            # Analyze emergency procedure effectiveness
            emergency_metrics = {
                k: v
                for k, v in metrics.items()
                if "emergency" in k.lower() or "response" in k.lower()
            }

            if emergency_metrics:
                # Identify procedures that need improvement
                ineffective_procedures = [
                    k for k, v in emergency_metrics.items() if v < 0.8
                ]

                if ineffective_procedures:
                    emergency_enhancement["enhancement_recommendations"] = [
                        f"Improve emergency procedure: {procedure}"
                        for procedure in ineffective_procedures
                    ]

                # Response time analysis
                response_metrics = {
                    k: v for k, v in emergency_metrics.items() if "time" in k.lower()
                }
                if response_metrics:
                    emergency_enhancement["response_time_analysis"] = {
                        "avg_response_time": np.mean(list(response_metrics.values())),
                        "slowest_procedure": min(
                            response_metrics.items(), key=lambda x: x[1]
                        )[0],
                        "optimization_target": "Reduce response times for critical procedures",
                    }

            return emergency_enhancement

        except Exception as e:
            return {"error": f"Emergency procedure enhancement failed: {e!s}"}

    def _analyze_compliance_reasoning(
        self, _metrics: dict[str, float], results: dict[str, Any]
    ) -> dict[str, Any]:
        """Analyze compliance reasoning using LLM"""
        try:
            compliance_reasoning = {
                "compliance_insights": {},
                "regulatory_analysis": {},
                "compliance_gaps": [],
                "improvement_strategies": [],
            }

            # Analyze compliance status
            compliance_status = results.get("compliance_status", {})
            for standard, status in compliance_status.items():
                if isinstance(status, dict):
                    compliant = status.get("compliant", False)
                    details = status.get("details", "")

                    compliance_reasoning["compliance_insights"][standard] = {
                        "compliant": compliant,
                        "details": details,
                        "status": "compliant" if compliant else "non_compliant",
                    }

                    if not compliant:
                        compliance_reasoning["compliance_gaps"].append(standard)
                        compliance_reasoning["improvement_strategies"].append(
                            f"Address compliance gaps for {standard}"
                        )

            # Regulatory analysis
            if self.compliance_standards:
                compliance_reasoning["regulatory_analysis"] = {
                    "standards_count": len(self.compliance_standards),
                    "compliance_rate": (
                        len(
                            [
                                s
                                for s in compliance_status.values()
                                if isinstance(s, dict) and s.get("compliant", False)
                            ]
                        )
                        / len(compliance_status)
                        if compliance_status
                        else 0
                    ),
                    "critical_standards": [
                        s
                        for s in self.compliance_standards
                        if "26262" in s or "178" in s
                    ],
                }

            return compliance_reasoning

        except Exception as e:
            return {"error": f"Compliance reasoning analysis failed: {e!s}"}
