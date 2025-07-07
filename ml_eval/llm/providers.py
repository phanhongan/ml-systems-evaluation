"""LLM provider integrations for ML Systems Evaluation Framework"""

import logging
from abc import ABC, abstractmethod
from typing import Any

from openai import OpenAI


class LLMProvider(ABC):
    """Base class for LLM providers"""

    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.client = self._initialize_client()

    @abstractmethod
    def _initialize_client(self) -> Any:
        """Initialize the LLM client"""

    @abstractmethod
    async def generate_response(
        self,
        prompt: str,
        context: dict[str, Any] | None = None,
        temperature: float = 0.1,
    ) -> str:
        """Generate response from LLM"""

    @abstractmethod
    async def analyze_metrics(
        self, metrics: dict[str, Any], analysis_type: str
    ) -> dict[str, Any]:
        """Analyze metrics using LLM"""

    @abstractmethod
    async def generate_report(self, data: dict[str, Any], report_type: str) -> str:
        """Generate report using LLM"""

    def validate_response(self, response: str) -> bool:
        """Validate LLM response quality"""
        # Basic validation - can be extended
        return len(response.strip()) > 0 and not response.startswith("I'm sorry")


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider implementation"""

    def _initialize_client(self) -> OpenAI:
        """Initialize OpenAI client"""
        api_key = self.config.get("api_key")
        if not api_key:
            raise ValueError("OpenAI API key is required")

        return OpenAI(api_key=api_key)

    async def generate_response(
        self,
        prompt: str,
        context: dict[str, Any] | None = None,
        temperature: float = 0.1,
    ) -> str:
        """Generate response using OpenAI GPT"""
        try:
            # Build system message with context
            system_message = self._build_system_message(context)

            response = self.client.chat.completions.create(
                model=self.config.get("model", "gpt-4"),
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=self.config.get("max_tokens", 1000),
            )

            return response.choices[0].message.content or ""

        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            return ""

    async def analyze_metrics(
        self, metrics: dict[str, Any], analysis_type: str
    ) -> dict[str, Any]:
        """Analyze metrics using OpenAI"""
        prompt = self._build_analysis_prompt(metrics, analysis_type)
        response = await self.generate_response(prompt)

        return {
            "analysis_type": analysis_type,
            "insights": response,
            "confidence": self._calculate_confidence(response),
            "recommendations": self._extract_recommendations(response),
        }

    async def generate_report(self, data: dict[str, Any], report_type: str) -> str:
        """Generate report using OpenAI"""
        prompt = self._build_report_prompt(data, report_type)
        return await self.generate_response(prompt)

    def _build_system_message(self, context: dict[str, Any] | None) -> str:
        """Build system message with context"""
        base_message = """You are an expert ML systems evaluation analyst.
        Your role is to analyze ML system metrics and provide intelligent insights.
        Always provide actionable recommendations and explain technical concepts clearly."""

        if context:
            context_str = f"\nContext: {context}"
            base_message += context_str

        return base_message

    def _build_analysis_prompt(
        self, metrics: dict[str, Any], analysis_type: str
    ) -> str:
        """Build analysis prompt"""
        if analysis_type == "drift":
            return f"""Analyze the following ML system metrics for data drift patterns:

            Metrics: {metrics}

            Please provide:
            1. Drift detection analysis
            2. Potential root causes
            3. Business impact assessment
            4. Recommended actions
            """
        elif analysis_type == "anomaly":
            return f"""Analyze the following ML system metrics for anomalies:

            Metrics: {metrics}

            Please provide:
            1. Anomaly detection analysis
            2. Severity assessment
            3. Potential causes
            4. Recommended actions
            """
        else:
            return f"""Analyze the following ML system metrics:

            Metrics: {metrics}

            Please provide:
            1. Key insights
            2. Performance assessment
            3. Recommendations
            """

    def _build_report_prompt(self, data: dict[str, Any], report_type: str) -> str:
        """Build report generation prompt"""
        if report_type == "business":
            return f"""Generate a business impact report based on the following data:

            Data: {data}

            Please provide:
            1. Executive summary
            2. Business impact analysis
            3. Key metrics and trends
            4. Recommendations for stakeholders
            """
        elif report_type == "technical":
            return f"""Generate a technical analysis report based on the following data:

            Data: {data}

            Please provide:
            1. Technical summary
            2. Performance analysis
            3. Issues and recommendations
            4. Next steps
            """
        else:
            return f"""Generate a comprehensive report based on the following data:

            Data: {data}

            Please provide a clear, structured report with insights and recommendations.
            """

    def _calculate_confidence(self, response: str) -> float:
        """Calculate confidence score for response"""
        # Simple heuristic - can be enhanced
        if len(response) < 50:
            return 0.3
        elif "uncertain" in response.lower() or "unclear" in response.lower():
            return 0.5
        else:
            return 0.8

    def _extract_recommendations(self, response: str) -> list[str]:
        """Extract recommendations from response"""
        # Simple extraction - can be enhanced with better parsing
        recommendations = []
        lines = response.split("\n")

        for line in lines:
            if any(
                keyword in line.lower()
                for keyword in ["recommend", "suggest", "should", "action"]
            ):
                recommendations.append(line.strip())

        return recommendations


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider implementation"""

    def _initialize_client(self) -> Any:
        """Initialize Anthropic client"""
        api_key = self.config.get("api_key")
        if not api_key:
            raise ValueError("Anthropic API key is required")

        # Import here to avoid dependency issues
        try:
            import anthropic

            return anthropic.Anthropic(api_key=api_key)
        except ImportError as err:
            raise ImportError(
                "anthropic package is required for AnthropicProvider"
            ) from err

    async def generate_response(
        self,
        prompt: str,
        context: dict[str, Any] | None = None,
        temperature: float = 0.1,
    ) -> str:
        """Generate response using Anthropic Claude"""
        try:
            system_message = self._build_system_message(context)

            response = self.client.messages.create(
                model=self.config.get("model", "claude-3-sonnet-20240229"),
                max_tokens=self.config.get("max_tokens", 1000),
                temperature=temperature,
                system=system_message,
                messages=[{"role": "user", "content": prompt}],
            )

            return response.content[0].text

        except Exception as e:
            self.logger.error(f"Anthropic API error: {e}")
            return ""

    async def analyze_metrics(
        self, metrics: dict[str, Any], analysis_type: str
    ) -> dict[str, Any]:
        """Analyze metrics using Anthropic"""
        prompt = self._build_analysis_prompt(metrics, analysis_type)
        response = await self.generate_response(prompt)

        return {
            "analysis_type": analysis_type,
            "insights": response,
            "confidence": self._calculate_confidence(response),
            "recommendations": self._extract_recommendations(response),
        }

    async def generate_report(self, data: dict[str, Any], report_type: str) -> str:
        """Generate report using Anthropic"""
        prompt = self._build_report_prompt(data, report_type)
        return await self.generate_response(prompt)

    def _build_system_message(self, context: dict[str, Any] | None) -> str:
        """Build system message with context"""
        base_message = """You are an expert ML systems evaluation analyst.
        Your role is to analyze ML system metrics and provide intelligent insights.
        Always provide actionable recommendations and explain technical concepts clearly."""

        if context:
            context_str = f"\nContext: {context}"
            base_message += context_str

        return base_message

    def _build_analysis_prompt(
        self, metrics: dict[str, Any], analysis_type: str
    ) -> str:
        """Build analysis prompt"""
        if analysis_type == "drift":
            return f"""Analyze the following ML system metrics for data drift patterns:

            Metrics: {metrics}

            Please provide:
            1. Drift detection analysis
            2. Potential root causes
            3. Business impact assessment
            4. Recommended actions
            """
        elif analysis_type == "anomaly":
            return f"""Analyze the following ML system metrics for anomalies:

            Metrics: {metrics}

            Please provide:
            1. Anomaly detection analysis
            2. Severity assessment
            3. Potential causes
            4. Recommended actions
            """
        else:
            return f"""Analyze the following ML system metrics:

            Metrics: {metrics}

            Please provide:
            1. Key insights
            2. Performance assessment
            3. Recommendations
            """

    def _build_report_prompt(self, data: dict[str, Any], report_type: str) -> str:
        """Build report generation prompt"""
        if report_type == "business":
            return f"""Generate a business impact report based on the following data:

            Data: {data}

            Please provide:
            1. Executive summary
            2. Business impact analysis
            3. Key metrics and trends
            4. Recommendations for stakeholders
            """
        elif report_type == "technical":
            return f"""Generate a technical analysis report based on the following data:

            Data: {data}

            Please provide:
            1. Technical summary
            2. Performance analysis
            3. Issues and recommendations
            4. Next steps
            """
        else:
            return f"""Generate a comprehensive report based on the following data:

            Data: {data}

            Please provide a clear, structured report with insights and recommendations.
            """

    def _calculate_confidence(self, response: str) -> float:
        """Calculate confidence score for response"""
        if len(response) < 50:
            return 0.3
        elif "uncertain" in response.lower() or "unclear" in response.lower():
            return 0.5
        else:
            return 0.8

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


def create_llm_provider(provider_type: str, config: dict[str, Any]) -> LLMProvider:
    """Factory function to create LLM provider"""
    providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
    }

    if provider_type not in providers:
        raise ValueError(f"Unknown LLM provider: {provider_type}")

    return providers[provider_type](config)
