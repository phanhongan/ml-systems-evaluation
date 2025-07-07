"""LLM Assistant Engine for ML Systems Evaluation Framework"""

import logging
from datetime import datetime
from typing import Any

from .providers import create_llm_provider


class LLMAssistantEngine:
    """LLM-powered assistant engine for configuration and troubleshooting"""

    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.provider = create_llm_provider(
            config.get("provider", "openai"), config.get("provider_config", {})
        )
        self.assistance_cache: dict[str, Any] = {}

    async def generate_configuration(
        self,
        requirements: str,
        industry: str | None = None,
        system_type: str | None = None,
    ) -> dict[str, Any]:
        """Generate configuration from natural language requirements"""
        try:
            # Prepare context
            context = {
                "assistance_type": "configuration_generation",
                "timestamp": datetime.now().isoformat(),
                "industry": industry,
                "system_type": system_type,
            }

            # Generate prompt
            prompt = self._build_configuration_prompt(
                requirements, industry, system_type
            )

            # Get LLM response
            response = await self.provider.generate_response(prompt, context)

            # Parse configuration
            config_result = {
                "assistance_type": "configuration_generation",
                "timestamp": datetime.now().isoformat(),
                "requirements": requirements,
                "generated_config": self._parse_configuration(response),
                "explanations": self._extract_explanations(response),
                "recommendations": self._extract_recommendations(response),
            }

            # Cache result
            cache_key = f"config_{hash(requirements)}"
            self.assistance_cache[cache_key] = config_result

            return config_result

        except Exception as e:
            self.logger.error(f"Configuration generation failed: {e}")
            return {
                "assistance_type": "configuration_generation",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    async def optimize_configuration(
        self, current_config: dict[str, Any], optimization_goals: str
    ) -> dict[str, Any]:
        """Optimize existing configuration based on goals"""
        try:
            # Prepare context
            context = {
                "assistance_type": "configuration_optimization",
                "timestamp": datetime.now().isoformat(),
                "current_config": current_config,
                "optimization_goals": optimization_goals,
            }

            # Generate prompt
            prompt = self._build_optimization_prompt(current_config, optimization_goals)

            # Get LLM response
            response = await self.provider.generate_response(prompt, context)

            # Parse optimization
            optimization_result = {
                "assistance_type": "configuration_optimization",
                "timestamp": datetime.now().isoformat(),
                "optimized_config": self._parse_configuration(response),
                "changes": self._extract_changes(current_config, response),
                "rationale": self._extract_rationale(response),
                "recommendations": self._extract_recommendations(response),
            }

            return optimization_result

        except Exception as e:
            self.logger.error(f"Configuration optimization failed: {e}")
            return {
                "assistance_type": "configuration_optimization",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    async def troubleshoot_issues(
        self, error_logs: list[str], system_metrics: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Troubleshoot issues using LLM analysis"""
        try:
            # Prepare context
            context = {
                "assistance_type": "troubleshooting",
                "timestamp": datetime.now().isoformat(),
                "error_count": len(error_logs),
                "system_metrics": system_metrics,
            }

            # Generate prompt
            prompt = self._build_troubleshooting_prompt(error_logs, system_metrics)

            # Get LLM response
            response = await self.provider.generate_response(prompt, context)

            # Parse troubleshooting
            troubleshooting_result = {
                "assistance_type": "troubleshooting",
                "timestamp": datetime.now().isoformat(),
                "diagnosis": self._extract_diagnosis(response),
                "root_causes": self._extract_root_causes(response),
                "solutions": self._extract_solutions(response),
                "prevention": self._extract_prevention_tips(response),
                "severity": self._assess_issue_severity(error_logs, response),
            }

            return troubleshooting_result

        except Exception as e:
            self.logger.error(f"Troubleshooting failed: {e}")
            return {
                "assistance_type": "troubleshooting",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    async def generate_documentation(
        self, config: dict[str, Any], doc_type: str = "user_guide"
    ) -> dict[str, Any]:
        """Generate documentation from configuration"""
        try:
            # Prepare context
            context = {
                "assistance_type": "documentation_generation",
                "timestamp": datetime.now().isoformat(),
                "doc_type": doc_type,
                "config_complexity": len(str(config)),
            }

            # Generate prompt
            prompt = self._build_documentation_prompt(config, doc_type)

            # Get LLM response
            response = await self.provider.generate_response(prompt, context)

            # Parse documentation
            doc_result = {
                "assistance_type": "documentation_generation",
                "timestamp": datetime.now().isoformat(),
                "doc_type": doc_type,
                "documentation": response,
                "sections": self._extract_doc_sections(response),
                "recommendations": self._extract_recommendations(response),
            }

            return doc_result

        except Exception as e:
            self.logger.error(f"Documentation generation failed: {e}")
            return {
                "assistance_type": "documentation_generation",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def _build_configuration_prompt(
        self, requirements: str, industry: str | None, system_type: str | None
    ) -> str:
        """Build prompt for configuration generation"""
        prompt = f"""Generate a configuration for an ML Systems Evaluation Framework based on the following requirements:

Requirements: {requirements}

"""
        if industry:
            prompt += f"Industry: {industry}\n"
        if system_type:
            prompt += f"System Type: {system_type}\n"

        prompt += """
Please generate a complete YAML configuration that includes:

1. System Configuration:
   - System name and description
   - Criticality level
   - Industry-specific requirements

2. SLOs (Service Level Objectives):
   - Performance SLOs
   - Reliability SLOs
   - Safety SLOs (if applicable)
   - Compliance SLOs (if applicable)

3. Collectors:
   - Data collection configuration
   - Endpoints and data sources
   - Collection intervals

4. Evaluators:
   - Performance evaluators
   - Safety evaluators (if safety-critical)
   - Compliance evaluators (if applicable)
   - Drift evaluators

5. Reports:
   - Business impact reports
   - Technical reports
   - Compliance reports

Please provide:
- A complete, valid YAML configuration
- Explanations for key configuration choices
- Industry-specific best practices
- Recommendations for monitoring and maintenance

Format the response as:
CONFIGURATION:
[YAML configuration here]

EXPLANATIONS:
[Explanations for key choices]

RECOMMENDATIONS:
[Additional recommendations]
"""

        return prompt

    def _build_optimization_prompt(
        self, current_config: dict[str, Any], optimization_goals: str
    ) -> str:
        """Build prompt for configuration optimization"""
        prompt = f"""Optimize the following ML Systems Evaluation Framework configuration based on these goals:

Current Configuration: {current_config}

Optimization Goals: {optimization_goals}

Please provide:
1. Optimized Configuration:
   - Improved YAML configuration
   - Better performance settings
   - Enhanced monitoring capabilities
   - Industry best practices

2. Changes Made:
   - Specific changes and their rationale
   - Performance improvements
   - Risk mitigations

3. Recommendations:
   - Additional optimizations
   - Monitoring strategies
   - Maintenance procedures

Format the response as:
OPTIMIZED_CONFIGURATION:
[Optimized YAML configuration]

CHANGES:
[Detailed list of changes with rationale]

RECOMMENDATIONS:
[Additional recommendations]
"""

        return prompt

    def _build_troubleshooting_prompt(
        self, error_logs: list[str], system_metrics: dict[str, Any] | None
    ) -> str:
        """Build prompt for troubleshooting"""
        prompt = f"""Analyze the following error logs and system metrics to diagnose issues:

Error Logs:
{chr(10).join(error_logs)}

"""
        if system_metrics:
            prompt += f"System Metrics: {system_metrics}\n\n"

        prompt += """Please provide:
1. Diagnosis:
   - Primary issue identification
   - Contributing factors
   - Impact assessment

2. Root Causes:
   - Technical root causes
   - Configuration issues
   - Environmental factors

3. Solutions:
   - Immediate fixes
   - Long-term solutions
   - Preventive measures

4. Prevention:
   - Monitoring improvements
   - Alert configurations
   - Best practices

Format the response as:
DIAGNOSIS:
[Primary diagnosis]

ROOT_CAUSES:
[List of root causes]

SOLUTIONS:
[Immediate and long-term solutions]

PREVENTION:
[Preventive measures]
"""

        return prompt

    def _build_documentation_prompt(self, config: dict[str, Any], doc_type: str) -> str:
        """Build prompt for documentation generation"""
        prompt = f"""Generate {doc_type} documentation for the following ML Systems Evaluation Framework configuration:

Configuration: {config}

Please provide comprehensive documentation that includes:

1. Overview:
   - System purpose and scope
   - Key components and their roles
   - Architecture overview

2. Configuration Guide:
   - Step-by-step setup instructions
   - Configuration options explanation
   - Best practices

3. Monitoring Guide:
   - Key metrics to monitor
   - Alert configurations
   - Troubleshooting procedures

4. Maintenance:
   - Regular maintenance tasks
   - Performance optimization
   - Security considerations

Please provide clear, actionable documentation suitable for the target audience.
"""

        return prompt

    def _parse_configuration(self, response: str) -> dict[str, Any]:
        """Parse configuration from LLM response"""
        # Simple parsing - can be enhanced
        try:
            import yaml

            # Extract YAML configuration from response
            lines = response.split("\n")
            yaml_start = -1
            yaml_end = -1

            for i, line in enumerate(lines):
                if "CONFIGURATION:" in line or "---" in line:
                    yaml_start = i + 1
                elif yaml_start > 0 and (
                    line.strip() == "" or line.startswith("EXPLANATIONS:")
                ):
                    yaml_end = i
                    break

            if yaml_start > 0 and yaml_end > yaml_start:
                yaml_content = "\n".join(lines[yaml_start:yaml_end])
                return yaml.safe_load(yaml_content)
            else:
                # Fallback: try to parse the entire response
                return yaml.safe_load(response)

        except Exception as e:
            self.logger.error(f"Failed to parse configuration: {e}")
            return {}

    def _extract_explanations(self, response: str) -> list[str]:
        """Extract explanations from response"""
        explanations = []
        lines = response.split("\n")
        in_explanations = False

        for line in lines:
            if "EXPLANATIONS:" in line:
                in_explanations = True
                continue
            elif in_explanations and line.strip() == "":
                break
            elif in_explanations:
                explanations.append(line.strip())

        return explanations

    def _extract_changes(
        self, _current_config: dict[str, Any], response: str
    ) -> list[str]:
        """Extract changes from optimization response"""
        changes = []
        lines = response.split("\n")
        in_changes = False

        for line in lines:
            if "CHANGES:" in line:
                in_changes = True
                continue
            elif in_changes and line.strip() == "":
                break
            elif in_changes:
                changes.append(line.strip())

        return changes

    def _extract_rationale(self, response: str) -> str:
        """Extract rationale from response"""
        # Simple extraction - can be enhanced
        lines = response.split("\n")
        for line in lines:
            if "rationale" in line.lower() or "reason" in line.lower():
                return line.strip()
        return "Optimization based on best practices and performance requirements"

    def _extract_diagnosis(self, response: str) -> str:
        """Extract diagnosis from response"""
        lines = response.split("\n")
        in_diagnosis = False
        diagnosis = []

        for line in lines:
            if "DIAGNOSIS:" in line:
                in_diagnosis = True
                continue
            elif in_diagnosis and line.strip() == "":
                break
            elif in_diagnosis:
                diagnosis.append(line.strip())

        return " ".join(diagnosis)

    def _extract_root_causes(self, response: str) -> list[str]:
        """Extract root causes from response"""
        root_causes = []
        lines = response.split("\n")
        in_root_causes = False

        for line in lines:
            if "ROOT_CAUSES:" in line:
                in_root_causes = True
                continue
            elif in_root_causes and line.strip() == "":
                break
            elif in_root_causes:
                root_causes.append(line.strip())

        return root_causes

    def _extract_solutions(self, response: str) -> list[str]:
        """Extract solutions from response"""
        solutions = []
        lines = response.split("\n")
        in_solutions = False

        for line in lines:
            if "SOLUTIONS:" in line:
                in_solutions = True
                continue
            elif in_solutions and line.strip() == "":
                break
            elif in_solutions:
                solutions.append(line.strip())

        return solutions

    def _extract_prevention_tips(self, response: str) -> list[str]:
        """Extract prevention tips from response"""
        prevention = []
        lines = response.split("\n")
        in_prevention = False

        for line in lines:
            if "PREVENTION:" in line:
                in_prevention = True
                continue
            elif in_prevention and line.strip() == "":
                break
            elif in_prevention:
                prevention.append(line.strip())

        return prevention

    def _extract_doc_sections(self, response: str) -> dict[str, str]:
        """Extract documentation sections"""
        sections = {}
        lines = response.split("\n")
        current_section = ""
        current_content = []

        for line in lines:
            if line.strip().endswith(":") and len(line.strip()) < 50:
                if current_section and current_content:
                    sections[current_section] = "\n".join(current_content).strip()
                current_section = line.strip()[:-1]
                current_content = []
            elif current_section:
                current_content.append(line)

        if current_section and current_content:
            sections[current_section] = "\n".join(current_content).strip()

        return sections

    def _extract_recommendations(self, response: str) -> list[str]:
        """Extract recommendations from response"""
        recommendations = []
        lines = response.split("\n")

        for line in lines:
            if any(
                keyword in line.lower()
                for keyword in ["recommend", "suggest", "should", "action"]
            ):
                recommendations.append(line.strip())

        return recommendations

    def _assess_issue_severity(self, _error_logs: list[str], response: str) -> str:
        """Assess issue severity"""
        # Simple assessment - can be enhanced
        if any(
            keyword in response.lower()
            for keyword in ["critical", "severe", "emergency"]
        ):
            return "critical"
        elif any(keyword in response.lower() for keyword in ["high", "serious"]):
            return "high"
        elif any(keyword in response.lower() for keyword in ["medium", "moderate"]):
            return "medium"
        else:
            return "low"

    def get_cached_assistance(self, cache_key: str) -> dict[str, Any] | None:
        """Get cached assistance result"""
        return self.assistance_cache.get(cache_key)

    def clear_cache(self) -> None:
        """Clear assistance cache"""
        self.assistance_cache.clear()
