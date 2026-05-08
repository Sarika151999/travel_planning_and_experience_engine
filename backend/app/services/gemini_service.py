"""
Google Gemini AI service for itinerary generation.
"""

import json
from typing import Dict, Any
import google.generativeai as genai
from app.config import get_settings
from app.models import Itinerary, EnergyLevel, ItineraryRequest
from app.utils.logger import get_logger

logger = get_logger(__name__)


class GeminiService:
    """Service for interacting with Google Gemini API."""
    
    def __init__(self):
        """Initialize Gemini service with API key."""
        settings = get_settings()
        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    async def generate_itinerary(self, request: ItineraryRequest) -> Dict[str, Any]:
        """
        Generate a personalized travel itinerary using Gemini AI.
        
        Args:
            request: ItineraryRequest with destination, budget, and preferences
        
        Returns:
            Dict containing the generated itinerary data
        
        Raises:
            ValueError: If API returns invalid data
            Exception: If API call fails
        """
        try:
            # Build the prompt for Gemini
            prompt = self._build_itinerary_prompt(request)
            
            # Call Gemini API
            response = self.model.generate_content(prompt)
            
            # Parse the response
            itinerary_data = self._parse_gemini_response(response.text)
            
            logger.info(f"Successfully generated itinerary for {request.destination}")
            return itinerary_data
        
        except Exception as e:
            logger.error(f"Error generating itinerary: {str(e)}")
            raise
    
    def _build_itinerary_prompt(self, request: ItineraryRequest) -> str:
        """
        Build the prompt for Gemini API.
        
        Args:
            request: ItineraryRequest object
        
        Returns:
            str: Formatted prompt for Gemini
        """
        interests_text = ", ".join(request.interests) if request.interests else "general"
        energy_description = self._get_energy_description(request.energy_level)
        
        prompt = f"""
        Generate a detailed {request.days}-day travel itinerary for {request.destination}.
        
        Constraints:
        - Total budget: ${request.budget}
        - Energy level: {request.energy_level.value} ({energy_description})
        - Number of travelers: {request.travelers}
        - Interests: {interests_text}
        
        Requirements:
        1. Create activities that match the energy level
        2. Ensure geographically clustered activities to minimize travel time
        3. Include realistic costs per person
        4. Provide time of day recommendations
        5. Include location names, descriptions, and estimated durations
        
        Format the response as a valid JSON object with this exact structure:
        {{
            "destination": "{request.destination}",
            "duration_days": {request.days},
            "energy_level": "{request.energy_level.value}",
            "total_budget": {request.budget},
            "estimated_cost": <calculated based on activities>,
            "highlights": ["highlight1", "highlight2", ...],
            "packing_tips": ["tip1", "tip2", ...],
            "transport_tips": ["tip1", "tip2", ...],
            "budget_breakdown": {{"activities": <amount>, "food": <amount>, "transport": <amount>, "accommodation": <amount>}},
            "itinerary_days": [
                {{
                    "day_number": 1,
                    "theme": "day theme",
                    "tips": ["tip1", "tip2"],
                    "estimated_cost": <cost>,
                    "activities": [
                        {{
                            "name": "activity name",
                            "description": "brief description",
                            "location": "location name",
                            "duration_hours": <number>,
                            "cost_per_person": <cost>,
                            "energy_required": "{request.energy_level.value}",
                            "time_of_day": "morning/afternoon/evening"
                        }}
                    ]
                }}
            ]
        }}
        
        Only return the JSON object, no additional text.
        """
        
        return prompt
    
    def _get_energy_description(self, energy_level: EnergyLevel) -> str:
        """Get description for energy level."""
        descriptions = {
            EnergyLevel.CHILL: "relaxing, cultural, and leisurely activities",
            EnergyLevel.BALANCED: "mix of relaxation and moderate activities",
            EnergyLevel.ADVENTUROUS: "high-energy, adventure-based activities"
        }
        return descriptions.get(energy_level, "balanced activities")
    
    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse JSON response from Gemini.
        
        Args:
            response_text: Raw text response from Gemini
        
        Returns:
            Dict: Parsed itinerary data
        
        Raises:
            ValueError: If response is not valid JSON
        """
        try:
            # Try to find JSON in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response_text[start_idx:end_idx]
            data = json.loads(json_str)
            
            return data
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response: {str(e)}")
            raise ValueError(f"Invalid JSON in Gemini response: {str(e)}")
