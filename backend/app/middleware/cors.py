"""
CORS middleware configuration for Vibe-Check Travel Agent.
"""

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.config import get_settings


def setup_cors(app: FastAPI) -> None:
    """
    Configure CORS middleware for the application.
    
    Args:
        app: FastAPI application instance
    """
    settings = get_settings()
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Type", "X-Itinerary-ID"],
    )
