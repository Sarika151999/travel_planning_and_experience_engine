"""
Main itinerary business logic service.
Orchestrates Gemini, Maps, and Storage services.
"""

from typing import Dict, Any
from datetime import datetime
from app.models import ItineraryRequest, Itinerary, ItineraryResponse
from app.services.gemini_service import GeminiService
from app.services.maps_service import MapsService
from app.services.storage_service import StorageService
from app.utils.logger import get_logger
from app.utils.security import generate_itinerary_id

logger = get_logger(__name__)


class ItineraryService:
    """Main service orchestrating itinerary generation."""
    
    def __init__(self):
        """Initialize itinerary service with dependent services."""
        self.gemini_service = GeminiService()
        self.maps_service = MapsService()
        self.storage_service = StorageService()
    
    async def generate_and_save_itinerary(
        self, 
        request: ItineraryRequest
    ) -> ItineraryResponse:
        """
        Generate itinerary using Gemini and save to Cloud Storage.
        
        Args:
            request: ItineraryRequest with travel preferences
        
        Returns:
            ItineraryResponse with generated itinerary and shareable URL
        
        Raises:
            Exception: If generation or storage fails
        """
        try:
            logger.info(f"Starting itinerary generation for {request.destination}")
            
            # Step 1: Generate itinerary using Gemini
            itinerary_id = generate_itinerary_id()
            gemini_data = await self.gemini_service.generate_itinerary(request)
            
            # Step 2: Enrich with geographic clustering
            enriched_data = await self._enrich_with_geographic_data(gemini_data, request.destination)
            
            # Step 3: Save to Cloud Storage
            shareable_url = await self.storage_service.save_itinerary(enriched_data, itinerary_id)
            
            # Step 4: Build response
            response = ItineraryResponse(
                itinerary_id=itinerary_id,
                itinerary=Itinerary(**enriched_data),
                shareable_url=shareable_url,
                generated_at=datetime.utcnow().isoformat()
            )
            
            logger.info(f"Successfully generated and saved itinerary {itinerary_id}")
            return response
        
        except Exception as e:
            logger.error(f"Error in itinerary generation: {str(e)}")
            raise
    
    async def _enrich_with_geographic_data(self, itinerary_data: Dict[str, Any], destination: str) -> Dict[str, Any]:
        """
        Enrich itinerary with geographic coordinates and clustered locations.
        
        Args:
            itinerary_data: Base itinerary data from Gemini
            destination: Travel destination
        
        Returns:
            Dict: Enriched itinerary with geographic data
        """
        try:
            # Geocode destination
            destination_location = await self.maps_service.geocode_address(destination)
            
            if destination_location:
                logger.info(f"Geocoded destination: {destination}")
            
            # For each activity, geocode and add location data
            for day in itinerary_data.get("itinerary_days", []):
                for activity in day.get("activities", []):
                    # Try to geocode the activity location
                    location = await self.maps_service.geocode_address(activity.get("location", ""))
                    
                    if location:
                        activity["latitude"] = location["latitude"]
                        activity["longitude"] = location["longitude"]
            
            return itinerary_data
        
        except Exception as e:
            logger.warning(f"Error enriching geographic data: {str(e)}")
            # Return original data if enrichment fails
            return itinerary_data
    
    async def retrieve_itinerary(self, itinerary_id: str) -> Dict[str, Any]:
        """
        Retrieve a saved itinerary from Cloud Storage.
        
        Args:
            itinerary_id: ID of itinerary to retrieve
        
        Returns:
            Dict: Itinerary data
        """
        return await self.storage_service.retrieve_itinerary(itinerary_id)
    
    async def list_recent_itineraries(self, limit: int = 10) -> list:
        """
        List recent itineraries.
        
        Args:
            limit: Maximum number to return
        
        Returns:
            list: List of itinerary metadata
        """
        return await self.storage_service.list_itineraries(limit)
