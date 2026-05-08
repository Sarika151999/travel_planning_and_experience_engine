"""
Google Cloud Storage service for saving and retrieving itineraries.
"""

import json
from typing import Optional
from datetime import datetime, timedelta
from google.cloud import storage
from google.oauth2 import service_account
from app.config import get_settings
from app.utils.logger import get_logger
from app.utils.security import generate_itinerary_id, sanitize_gcs_path

logger = get_logger(__name__)


class StorageService:
    """Service for interacting with Google Cloud Storage."""
    
    def __init__(self):
        """Initialize Cloud Storage service."""
        settings = get_settings()
        self.bucket_name = settings.gcs_bucket_name
        self.project_id = settings.google_cloud_project_id
        
        try:
            # Initialize GCS client
            self.client = storage.Client(project=self.project_id)
            self.bucket = self.client.bucket(self.bucket_name)
            logger.info(f"Initialized Cloud Storage service for bucket: {self.bucket_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Cloud Storage: {str(e)}")
            raise
    
    async def save_itinerary(self, itinerary_data: dict, itinerary_id: Optional[str] = None) -> str:
        """
        Save itinerary to Google Cloud Storage.
        
        Args:
            itinerary_data: Dictionary containing itinerary data
            itinerary_id: Optional custom ID, generates one if not provided
        
        Returns:
            str: Public shareable URL for the itinerary
        
        Raises:
            Exception: If storage operation fails
        """
        try:
            # Generate ID if not provided
            if not itinerary_id:
                itinerary_id = generate_itinerary_id()
            
            # Create storage path
            timestamp = datetime.utcnow().strftime("%Y/%m/%d")
            storage_path = f"itineraries/{timestamp}/{itinerary_id}.json"
            storage_path = sanitize_gcs_path(storage_path)
            
            # Create blob and upload data
            blob = self.bucket.blob(storage_path)
            blob.content_type = "application/json"
            
            # Make the blob publicly readable
            blob.upload_from_string(
                json.dumps(itinerary_data),
                content_type="application/json"
            )
            
            # Make blob public
            blob.make_public()
            
            # Generate public URL
            public_url = blob.public_url
            
            logger.info(f"Saved itinerary {itinerary_id} to Cloud Storage")
            return public_url
        
        except Exception as e:
            logger.error(f"Error saving itinerary to Cloud Storage: {str(e)}")
            raise
    
    async def retrieve_itinerary(self, itinerary_id: str) -> Optional[dict]:
        """
        Retrieve itinerary from Google Cloud Storage.
        
        Args:
            itinerary_id: ID of itinerary to retrieve
        
        Returns:
            dict: Itinerary data or None if not found
        """
        try:
            # Search for the blob
            blobs = self.client.list_blobs(
                self.bucket_name,
                prefix=f"itineraries/",
                delimiter="/"
            )
            
            for blob in blobs:
                if itinerary_id in blob.name:
                    data = blob.download_as_string().decode('utf-8')
                    return json.loads(data)
            
            logger.warning(f"Itinerary {itinerary_id} not found in Cloud Storage")
            return None
        
        except Exception as e:
            logger.error(f"Error retrieving itinerary from Cloud Storage: {str(e)}")
            return None
    
    async def delete_itinerary(self, itinerary_id: str) -> bool:
        """
        Delete itinerary from Google Cloud Storage.
        
        Args:
            itinerary_id: ID of itinerary to delete
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Search for the blob
            blobs = list(self.client.list_blobs(
                self.bucket_name,
                prefix=f"itineraries/"
            ))
            
            for blob in blobs:
                if itinerary_id in blob.name:
                    blob.delete()
                    logger.info(f"Deleted itinerary {itinerary_id} from Cloud Storage")
                    return True
            
            logger.warning(f"Itinerary {itinerary_id} not found for deletion")
            return False
        
        except Exception as e:
            logger.error(f"Error deleting itinerary from Cloud Storage: {str(e)}")
            return False
    
    async def generate_signed_url(self, itinerary_id: str, expiration_hours: int = 24) -> Optional[str]:
        """
        Generate a signed URL for temporary access to itinerary.
        
        Args:
            itinerary_id: ID of itinerary
            expiration_hours: URL expiration time in hours
        
        Returns:
            str: Signed URL or None if not found
        """
        try:
            # Search for the blob
            blobs = list(self.client.list_blobs(
                self.bucket_name,
                prefix=f"itineraries/"
            ))
            
            for blob in blobs:
                if itinerary_id in blob.name:
                    url = blob.generate_signed_url(
                        version="v4",
                        expiration=timedelta(hours=expiration_hours),
                        method="GET"
                    )
                    logger.info(f"Generated signed URL for itinerary {itinerary_id}")
                    return url
            
            return None
        
        except Exception as e:
            logger.error(f"Error generating signed URL: {str(e)}")
            return None
    
    async def list_itineraries(self, limit: int = 10) -> list:
        """
        List recent itineraries.
        
        Args:
            limit: Maximum number of itineraries to return
        
        Returns:
            list: List of itinerary metadata
        """
        try:
            blobs = list(self.client.list_blobs(
                self.bucket_name,
                prefix="itineraries/",
                max_results=limit
            ))
            
            itineraries = []
            for blob in blobs:
                itineraries.append({
                    "id": blob.name.split('/')[-1].replace('.json', ''),
                    "created": blob.time_created,
                    "size": blob.size
                })
            
            return itineraries
        
        except Exception as e:
            logger.error(f"Error listing itineraries: {str(e)}")
            return []
