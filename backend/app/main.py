"""
Main FastAPI application setup for Vibe-Check Travel Agent.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.config import get_settings
from app.api.routes import router as api_router
from app.middleware.cors import setup_cors
from app.middleware.error_handler import setup_error_handlers
from app.utils.logger import get_logger

logger = get_logger(__name__)


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        FastAPI: Configured application instance
    """
    settings = get_settings()
    
    # Create app
    app = FastAPI(
        title="Vibe-Check Travel Agent",
        description="AI-powered travel planning with Google Gemini and Google Cloud Services",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Setup middleware
    setup_cors(app)
    setup_error_handlers(app)
    
    # Include routers
    app.include_router(api_router)
    
    # Add startup event
    @app.on_event("startup")
    async def startup_event():
        """Initialize services on startup."""
        logger.info("Starting Vibe-Check Travel Agent API")
        logger.info(f"Environment: {settings.environment}")
        logger.info(f"Google Cloud Project: {settings.google_cloud_project_id}")
    
    # Add shutdown event
    @app.on_event("shutdown")
    async def shutdown_event():
        """Cleanup on shutdown."""
        logger.info("Shutting down Vibe-Check Travel Agent API")
    
    # Root endpoint
    @app.get("/", tags=["root"])
    async def root():
        """Root endpoint with API information."""
        return {
            "name": "Vibe-Check Travel Agent",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/api/v1/health"
        }
    
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
