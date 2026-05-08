"""
Data models for Vibe-Check Travel Agent.
Defines request/response schemas using Pydantic.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class EnergyLevel(str, Enum):
    """User energy level for travel planning."""
    CHILL = "chill"
    BALANCED = "balanced"
    ADVENTUROUS = "adventurous"


class ItineraryRequest(BaseModel):
    """Request model for itinerary generation."""
    
    destination: str = Field(..., min_length=2, max_length=100, description="Travel destination")
    budget: int = Field(..., ge=100, le=100000, description="Budget in USD")
    energy_level: EnergyLevel = Field(..., description="User energy level preference")
    days: int = Field(default=3, ge=1, le=30, description="Number of days for the trip")
    interests: Optional[List[str]] = Field(default=None, description="User interests/categories")
    travelers: int = Field(default=1, ge=1, le=20, description="Number of travelers")
    
    @validator("interests")
    def validate_interests(cls, v):
        """Validate interests list."""
        if v is not None and len(v) > 10:
            raise ValueError("Maximum 10 interests allowed")
        return v


class Activity(BaseModel):
    """Model for a single activity in the itinerary."""
    
    name: str
    description: str
    location: str
    duration_hours: float
    cost_per_person: int
    energy_required: EnergyLevel
    time_of_day: str
    google_place_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ItineraryDay(BaseModel):
    """Model for a single day in the itinerary."""
    
    day_number: int
    theme: str
    activities: List[Activity]
    estimated_cost: int
    tips: List[str]


class Itinerary(BaseModel):
    """Complete itinerary model."""
    
    destination: str
    duration_days: int
    energy_level: EnergyLevel
    total_budget: int
    estimated_cost: int
    itinerary_days: List[ItineraryDay]
    highlights: List[str]
    packing_tips: List[str]
    transport_tips: List[str]
    budget_breakdown: Dict[str, int]


class ItineraryResponse(BaseModel):
    """Response model for itinerary generation."""
    
    itinerary_id: str
    itinerary: Itinerary
    shareable_url: Optional[str] = None
    generated_at: str


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str
    detail: Optional[str] = None
    status_code: int


class HealthResponse(BaseModel):
    """Health check response model."""
    
    status: str
    version: str
    timestamp: str
