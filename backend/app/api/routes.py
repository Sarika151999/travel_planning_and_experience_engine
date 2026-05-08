"""
API routes for Vibe-Check Travel Agent.
Defines all REST endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from app.models import ItineraryRequest, ItineraryResponse, HealthResponse, ErrorResponse
from app.services.itinerary_service import ItineraryService
from app.api.dependencies import get_itinerary_service
from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1", tags=["travel-planning"])


@router.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Application health status
    """
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.utcnow().isoformat()
    )


@router.post(
    "/itineraries/generate",
    response_model=ItineraryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate travel itinerary",
    description="Generate a personalized travel itinerary based on destination, budget, and energy level",
    tags=["itineraries"]
)
async def generate_itinerary(
    request: ItineraryRequest,
    service: ItineraryService = Depends(get_itinerary_service)
):
    """
    Generate a personalized travel itinerary.
    
    Request body should include:
    - destination: Travel destination (string)
    - budget: Budget in USD (100-100,000)
    - energy_level: "chill", "balanced", or "adventurous"
    - days: Number of days (1-30, default: 3)
    - interests: List of interests/categories (optional)
    - travelers: Number of travelers (1-20, default: 1)
    
    Returns:
        ItineraryResponse: Generated itinerary with shareable URL
    
    Raises:
        HTTPException: If generation fails
    """
    try:
        logger.info(f"Generating itinerary for {request.destination} with budget ${request.budget}")
        
        response = await service.generate_and_save_itinerary(request)
        
        return response
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error generating itinerary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate itinerary"
        )


@router.get(
    "/itineraries/{itinerary_id}",
    response_model=dict,
    summary="Retrieve itinerary",
    description="Retrieve a previously generated itinerary by ID",
    tags=["itineraries"]
)
async def get_itinerary(
    itinerary_id: str,
    service: ItineraryService = Depends(get_itinerary_service)
):
    """
    Retrieve a saved itinerary.
    
    Args:
        itinerary_id: ID of the itinerary to retrieve
    
    Returns:
        dict: Itinerary data
    
    Raises:
        HTTPException: If itinerary not found
    """
    try:
        logger.info(f"Retrieving itinerary {itinerary_id}")
        
        itinerary = await service.retrieve_itinerary(itinerary_id)
        
        if not itinerary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Itinerary {itinerary_id} not found"
            )
        
        return itinerary
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving itinerary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve itinerary"
        )


@router.get(
    "/itineraries",
    response_model=list,
    summary="List recent itineraries",
    description="List recently generated itineraries",
    tags=["itineraries"]
)
async def list_itineraries(
    limit: int = 10,
    service: ItineraryService = Depends(get_itinerary_service)
):
    """
    List recent itineraries.
    
    Args:
        limit: Maximum number to return (default: 10)
    
    Returns:
        list: List of itinerary metadata
    """
    try:
        logger.info(f"Listing recent itineraries (limit: {limit})")
        
        itineraries = await service.list_recent_itineraries(limit)
        
        return itineraries
    
    except Exception as e:
        logger.error(f"Error listing itineraries: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list itineraries"
        )
