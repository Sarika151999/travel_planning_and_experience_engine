"""
Error handling middleware for Vibe-Check Travel Agent.
"""

import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle exceptions and return formatted error response.
    
    Args:
        request: FastAPI request object
        exc: Exception that occurred
    
    Returns:
        JSONResponse: Formatted error response
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred. Please try again later.",
            "status_code": 500
        }
    )


def setup_error_handlers(app: FastAPI) -> None:
    """
    Configure error handlers for the application.
    
    Args:
        app: FastAPI application instance
    """
    app.add_exception_handler(Exception, exception_handler)
