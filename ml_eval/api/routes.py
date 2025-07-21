"""FastAPI routes for ML Systems Evaluation Framework API"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from .models import (
    CollectionRequest,
    CollectionResponse,
    ConfigRequest,
    ConfigResponse,
    EvaluationRequest,
    EvaluationResponse,
    HealthResponse,
    ReportRequest,
    ReportResponse,
    ValidationRequest,
    ValidationResponse,
)
from .service import APIService

# Create router
router = APIRouter(prefix="/api/v1")

# Initialize service
service = APIService()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    health_data = service.get_health()
    return HealthResponse(**health_data)


@router.post("/config", response_model=ConfigResponse, tags=["Configuration"])
async def create_config(request: ConfigRequest):
    """Create a new configuration"""
    try:
        # Merge request data with config_data
        config_data = request.config_data.copy()
        config_data.update(
            {
                "system": {
                    "name": request.name,
                    "type": request.system_type,
                    "criticality": request.criticality,
                    "industry": request.industry,
                }
            }
        )

        config_info = service.create_config(config_data)
        return ConfigResponse(**config_info)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {e!s}"
        ) from e


@router.get(
    "/config/{config_id}", response_model=ConfigResponse, tags=["Configuration"]
)
async def get_config(config_id: str):
    """Get configuration by ID"""
    config_info = service.get_config(config_id)
    if not config_info:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return ConfigResponse(**config_info)


@router.get("/config", response_model=list[ConfigResponse], tags=["Configuration"])
async def list_configs():
    """List all configurations"""
    configs = service.list_configs()
    return [ConfigResponse(**config) for config in configs]


@router.post(
    "/config/validate", response_model=ValidationResponse, tags=["Configuration"]
)
async def validate_config(request: ValidationRequest):
    """Validate configuration data"""
    try:
        validation_result = service.validate_config(request.config_data)
        return ValidationResponse(**validation_result)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {e!s}"
        ) from e


@router.post("/evaluate", response_model=EvaluationResponse, tags=["Evaluation"])
async def start_evaluation(request: EvaluationRequest):
    """Start an evaluation"""
    try:
        evaluation_info = service.start_evaluation(request.config_id, request.options)
        return EvaluationResponse(**evaluation_info)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {e!s}"
        ) from e


@router.get(
    "/evaluate/{evaluation_id}", response_model=EvaluationResponse, tags=["Evaluation"]
)
async def get_evaluation(evaluation_id: str):
    """Get evaluation by ID"""
    evaluation_info = service.get_evaluation(evaluation_id)
    if not evaluation_info:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return EvaluationResponse(**evaluation_info)


@router.get("/evaluate", response_model=list[EvaluationResponse], tags=["Evaluation"])
async def list_evaluations():
    """List all evaluations"""
    evaluations = service.list_evaluations()
    return [EvaluationResponse(**evaluation) for evaluation in evaluations]


@router.post("/collect", response_model=CollectionResponse, tags=["Collection"])
async def start_collection(request: CollectionRequest):
    """Start data collection"""
    try:
        collection_info = service.start_collection(
            request.config_id, request.collector_name, request.options
        )
        return CollectionResponse(**collection_info)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {e!s}"
        ) from e


@router.get(
    "/collect/{collection_id}", response_model=CollectionResponse, tags=["Collection"]
)
async def get_collection(collection_id: str):
    """Get collection by ID"""
    collection_info = service.get_collection(collection_id)
    if not collection_info:
        raise HTTPException(status_code=404, detail="Collection not found")
    return CollectionResponse(**collection_info)


@router.get("/collect", response_model=list[CollectionResponse], tags=["Collection"])
async def list_collections():
    """List all collections"""
    collections = service.list_collections()
    return [CollectionResponse(**collection) for collection in collections]


@router.post("/reports", response_model=ReportResponse, tags=["Reports"])
async def generate_report(request: ReportRequest):
    """Generate a report"""
    try:
        report_info = service.generate_report(
            request.config_id,
            request.evaluation_id,
            request.report_type,
            request.format,
            request.options,
        )
        return ReportResponse(**report_info)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {e!s}"
        ) from e


@router.get("/reports/{report_id}", response_model=ReportResponse, tags=["Reports"])
async def get_report(report_id: str):
    """Get report by ID"""
    report_info = service.get_report(report_id)
    if not report_info:
        raise HTTPException(status_code=404, detail="Report not found")
    return ReportResponse(**report_info)


@router.get("/reports", response_model=list[ReportResponse], tags=["Reports"])
async def list_reports():
    """List all reports"""
    reports = service.list_reports()
    return [ReportResponse(**report) for report in reports]


@router.get("/reports/{report_id}/download", tags=["Reports"])
async def download_report(report_id: str):
    """Download report file"""
    report_info = service.get_report(report_id)
    if not report_info:
        raise HTTPException(status_code=404, detail="Report not found")

    # For MVP, return a mock report
    mock_report = {
        "report_id": report_id,
        "type": report_info.get("report_type", "business"),
        "format": report_info.get("format", "json"),
        "content": "Mock report content for MVP",
        "generated_at": report_info.get("created_at").isoformat(),
    }

    return JSONResponse(content=mock_report)
