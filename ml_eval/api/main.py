"""Main FastAPI application for ML Systems Evaluation Framework API"""

import argparse
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router

# Create FastAPI app
app = FastAPI(
    title="ML Systems Evaluation Framework API",
    description="REST API for ML Systems Evaluation Framework",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "ML Systems Evaluation Framework API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/v1/health",
    }


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    return app


def main(args: list[str] | None = None) -> int:
    """Main entry point for the API server"""
    parser = argparse.ArgumentParser(description="ML Systems Evaluation Framework API")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of worker processes (default: 1)",
    )

    parsed_args = parser.parse_args(args)

    try:
        uvicorn.run(
            "ml_eval.api.main:app",
            host=parsed_args.host,
            port=parsed_args.port,
            reload=parsed_args.reload,
            workers=parsed_args.workers,
        )
        return 0
    except KeyboardInterrupt:
        print("\nServer stopped.")
        return 0
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
