"""Pydantic models for API request/response schemas"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response"""

    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = Field(..., description="API version")


class ConfigRequest(BaseModel):
    """Configuration creation request"""

    name: str = Field(..., description="Configuration name")
    system_type: str = Field(default="single_model", description="System type")
    criticality: str = Field(
        default="business_critical", description="Criticality level"
    )
    industry: str | None = Field(None, description="Industry type")
    config_data: dict[str, Any] = Field(
        default_factory=dict, description="Configuration data"
    )


class ConfigResponse(BaseModel):
    """Configuration response"""

    id: str = Field(..., description="Configuration ID")
    name: str = Field(..., description="Configuration name")
    system_type: str = Field(..., description="System type")
    criticality: str = Field(..., description="Criticality level")
    industry: str | None = Field(None, description="Industry type")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class ValidationRequest(BaseModel):
    """Configuration validation request"""

    config_data: dict[str, Any] = Field(
        ..., description="Configuration data to validate"
    )


class ValidationResponse(BaseModel):
    """Configuration validation response"""

    valid: bool = Field(..., description="Whether configuration is valid")
    errors: list[str] = Field(default_factory=list, description="Validation errors")
    warnings: list[str] = Field(default_factory=list, description="Validation warnings")


class EvaluationRequest(BaseModel):
    """Evaluation request"""

    config_id: str = Field(..., description="Configuration ID")
    options: dict[str, Any] = Field(
        default_factory=dict, description="Evaluation options"
    )


class EvaluationResponse(BaseModel):
    """Evaluation response"""

    id: str = Field(..., description="Evaluation ID")
    config_id: str = Field(..., description="Configuration ID")
    status: str = Field(..., description="Evaluation status")
    progress: float = Field(..., description="Progress percentage")
    started_at: datetime = Field(..., description="Start timestamp")
    completed_at: datetime | None = Field(None, description="Completion timestamp")
    results: dict[str, Any] | None = Field(None, description="Evaluation results")


class CollectionRequest(BaseModel):
    """Data collection request"""

    config_id: str = Field(..., description="Configuration ID")
    collector_name: str = Field(..., description="Collector name")
    options: dict[str, Any] = Field(
        default_factory=dict, description="Collection options"
    )


class CollectionResponse(BaseModel):
    """Data collection response"""

    id: str = Field(..., description="Collection ID")
    config_id: str = Field(..., description="Configuration ID")
    status: str = Field(..., description="Collection status")
    progress: float = Field(..., description="Progress percentage")
    records_collected: int = Field(..., description="Number of records collected")
    started_at: datetime = Field(..., description="Start timestamp")
    completed_at: datetime | None = Field(None, description="Completion timestamp")


class ReportRequest(BaseModel):
    """Report generation request"""

    config_id: str = Field(..., description="Configuration ID")
    evaluation_id: str = Field(..., description="Evaluation ID")
    report_type: str = Field(..., description="Report type")
    format: str = Field(default="json", description="Report format")
    options: dict[str, Any] = Field(default_factory=dict, description="Report options")


class ReportResponse(BaseModel):
    """Report generation response"""

    id: str = Field(..., description="Report ID")
    config_id: str = Field(..., description="Configuration ID")
    evaluation_id: str = Field(..., description="Evaluation ID")
    status: str = Field(..., description="Report status")
    download_url: str | None = Field(None, description="Download URL")
    created_at: datetime = Field(..., description="Creation timestamp")


class ErrorResponse(BaseModel):
    """Error response"""

    error: dict[str, Any] = Field(..., description="Error details")
