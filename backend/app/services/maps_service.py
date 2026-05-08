"""
Google Maps service for location intelligence and place search.
"""

from typing import List, Dict, Any, Optional
import googlemaps
from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class MapsService:
    """Service for interacting with Google Maps API."""
    
    def __init__(self):
        """Initialize Maps service with API key."""
        settings = get_settings()
        self.client = googlemaps.Client(key=settings.google_maps_api_key)
    
    async def search_places(
        self, 
        query: str, 
        location: Optional[Dict[str, float]] = None,
        radius: int = 50000
    ) -> List[Dict[str, Any]]:
        """
        Search for places using Google Maps API.
        
        Args:
            query: Search query (e.g., "restaurants", "museums")
            location: Optional center point (lat/lng dict)
            radius: Search radius in meters
        
        Returns:
            List of place dictionaries with details
        """
        try:
            # This would use Google Places API
            logger.info(f"Searching places for: {query}")
            # Implementation would go here
            return []
        
        except Exception as e:
            logger.error(f"Error searching places: {str(e)}")
            raise
    
    async def geocode_address(self, address: str) -> Optional[Dict[str, Any]]:
        """
        Convert address to latitude/longitude.
        
        Args:
            address: Address to geocode
        
        Returns:
            Dict with lat/lng or None if not found
        """
        try:
            result = self.client.geocode(address=address)
            
            if result:
                location = result[0]['geometry']['location']
                return {
                    "latitude": location['lat'],
                    "longitude": location['lng'],
                    "formatted_address": result[0]['formatted_address']
                }
            return None
        
        except Exception as e:
            logger.error(f"Error geocoding address {address}: {str(e)}")
            return None
    
    async def get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a place.
        
        Args:
            place_id: Google Place ID
        
        Returns:
            Dict with place details or None
        """
        try:
            place = self.client.place(place_id)
            
            if place['status'] == 'OK':
                result = place['result']
                return {
                    "name": result.get('name'),
                    "address": result.get('formatted_address'),
                    "rating": result.get('rating'),
                    "reviews": result.get('reviews', [])[:3],
                    "phone": result.get('formatted_phone_number'),
                    "opening_hours": result.get('opening_hours'),
                    "website": result.get('website')
                }
            return None
        
        except Exception as e:
            logger.error(f"Error getting place details: {str(e)}")
            return None
    
    async def calculate_distance(
        self, 
        origin: str, 
        destination: str
    ) -> Optional[Dict[str, Any]]:
        """
        Calculate distance between two points.
        
        Args:
            origin: Starting location
            destination: Ending location
        
        Returns:
            Dict with distance and duration or None
        """
        try:
            result = self.client.distance_matrix(origins=[origin], destinations=[destination])
            
            if result['status'] == 'OK':
                element = result['rows'][0]['elements'][0]
                if element['status'] == 'OK':
                    return {
                        "distance_km": element['distance']['value'] / 1000,
                        "duration_minutes": element['duration']['value'] / 60,
                        "distance_text": element['distance']['text'],
                        "duration_text": element['duration']['text']
                    }
            return None
        
        except Exception as e:
            logger.error(f"Error calculating distance: {str(e)}")
            return None
    
    def cluster_locations(self, locations: List[Dict[str, float]]) -> List[List[Dict]]:
        """
        Cluster geographically nearby locations.
        Uses simple geographic clustering to minimize travel time.
        
        Args:
            locations: List of location dicts with lat/lng
        
        Returns:
            List of location clusters
        """
        # Simple clustering algorithm
        # In production, consider using more sophisticated approaches like K-means
        clusters = []
        used = set()
        
        for i, loc in enumerate(locations):
            if i in used:
                continue
            
            cluster = [loc]
            used.add(i)
            
            # Find nearby locations (within ~1km)
            for j, other_loc in enumerate(locations[i+1:], start=i+1):
                if j in used:
                    continue
                
                distance = self._haversine_distance(loc, other_loc)
                if distance < 1.0:  # 1 km threshold
                    cluster.append(other_loc)
                    used.add(j)
            
            clusters.append(cluster)
        
        return clusters
    
    @staticmethod
    def _haversine_distance(loc1: Dict[str, float], loc2: Dict[str, float]) -> float:
        """
        Calculate distance between two lat/lng points using Haversine formula.
        
        Args:
            loc1: Location dict with lat/lng
            loc2: Location dict with lat/lng
        
        Returns:
            float: Distance in kilometers
        """
        from math import radians, sin, cos, sqrt, atan2
        
        lat1, lon1 = radians(loc1['latitude']), radians(loc1['longitude'])
        lat2, lon2 = radians(loc2['latitude']), radians(loc2['longitude'])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        R = 6371  # Earth radius in km
        return R * c
