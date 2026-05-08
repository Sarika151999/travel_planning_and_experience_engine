"""
Configuration module for Vibe-Check Travel Agent backend.
Handles environment variables and app configuration.
"""

from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Google Cloud Configuration
    google_cloud_project_id: str
    google_api_key: str
    google_maps_api_key: str
    gcs_bucket_name: str
    gcs_json_key_path: str = "./gcs-key.json"
    
    # Application Configuration
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"
    api_version: str = "v1"
    
    # CORS Configuration
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # API Configuration
    max_itinerary_requests_per_hour: int = 30
    
    # Security
    allowed_hosts: List[str] = ["localhost", "127.0.0.1"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached application settings.
    
    Returns:
        Settings: Application configuration object.
    """
    return Settings()
