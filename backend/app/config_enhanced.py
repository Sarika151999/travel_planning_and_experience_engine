"""
Enhanced configuration module with Google Cloud integration.
Handles environment variables, Google Cloud logging, and monitoring.
"""

from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings
import os


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
    
    # Database Configuration
    database_url: str = "postgresql://postgres:postgres@localhost:5432/travel_agent"
    
    # Vector Database (Pinecone)
    pinecone_api_key: str = ""
    pinecone_environment: str = ""
    pinecone_index_name: str = "travel-itineraries"
    
    # Secret Key
    secret_key: str = "your-secret-key-for-jwt"
    
    # Cloud Run
    port: int = int(os.getenv("PORT", 8000))
    
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


def setup_google_cloud():
    """
    Setup Google Cloud integration (Logging, Monitoring).
    Call this in app startup.
    """
    settings = get_settings()
    
    if settings.environment == "production":
        try:
            from google.cloud import logging as cloud_logging
            import logging
            
            # Create a Cloud Logging handler
            client = cloud_logging.Client(project=settings.google_cloud_project_id)
            handler = client.logging_handler(name="travel-agent")
            
            # Get root logger and add the handler
            cloud_logger = logging.getLogger()
            cloud_logger.addHandler(handler)
            
            # Set structured logging
            cloud_logger.setLevel(logging.INFO)
            
            return True
        except Exception as e:
            print(f"Warning: Could not setup Google Cloud Logging: {e}")
            return False
    
    return False
