"""
API dependencies and common functions.
"""

from app.services.itinerary_service import ItineraryService


async def get_itinerary_service() -> ItineraryService:
    """
    Dependency for getting itinerary service.
    
    Returns:
        ItineraryService: Service instance for itinerary operations
    """
    return ItineraryService()
