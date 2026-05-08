"""
Vector Database Service for semantic search using Pinecone.
Enables intelligent itinerary matching and recommendations.
"""

from typing import List, Dict, Any, Optional
from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class VectorDBService:
    """Service for managing vector embeddings and semantic search."""
    
    def __init__(self):
        """Initialize Vector DB service."""
        settings = get_settings()
        self.api_key = settings.pinecone_api_key
        self.environment = settings.pinecone_environment
        self.index_name = settings.pinecone_index_name
        
        if not self.api_key or not self.environment:
            logger.warning("Pinecone not configured - semantic search disabled")
            self.client = None
            return
        
        try:
            import pinecone
            
            # Initialize Pinecone
            pinecone.init(
                api_key=self.api_key,
                environment=self.environment
            )
            
            self.client = pinecone.Index(self.index_name)
            logger.info(f"Initialized Pinecone index: {self.index_name}")
        
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {e}")
            self.client = None
    
    async def embed_text(self, text: str) -> Optional[List[float]]:
        """
        Convert text to embeddings using sentence-transformers.
        
        Args:
            text: Text to embed
        
        Returns:
            List of floats representing the embedding
        """
        try:
            from sentence_transformers import SentenceTransformer
            
            model = SentenceTransformer('all-MiniLM-L6-v2')
            embedding = model.encode(text)
            return embedding.tolist()
        
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return None
    
    async def store_itinerary_embedding(
        self,
        itinerary_id: str,
        itinerary_text: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """
        Store itinerary embedding in Pinecone.
        
        Args:
            itinerary_id: Unique ID for the itinerary
            itinerary_text: Text representation of itinerary
            metadata: Metadata dict with destination, budget, energy_level
        
        Returns:
            bool: Success status
        """
        if not self.client:
            logger.warning("Pinecone not available - skipping embedding storage")
            return False
        
        try:
            embedding = await self.embed_text(itinerary_text)
            
            if not embedding:
                return False
            
            # Upsert to Pinecone
            self.client.upsert(
                vectors=[(itinerary_id, embedding, metadata)],
                namespace="itineraries"
            )
            
            logger.info(f"Stored embedding for itinerary {itinerary_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error storing embedding: {e}")
            return False
    
    async def search_similar_itineraries(
        self,
        query_text: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for similar itineraries using semantic search.
        
        Args:
            query_text: Search query
            top_k: Number of results to return
        
        Returns:
            List of similar itineraries with scores
        """
        if not self.client:
            logger.warning("Pinecone not available - returning empty results")
            return []
        
        try:
            query_embedding = await self.embed_text(query_text)
            
            if not query_embedding:
                return []
            
            # Query Pinecone
            results = self.client.query(
                vector=query_embedding,
                top_k=top_k,
                namespace="itineraries",
                include_metadata=True
            )
            
            return [
                {
                    "id": match["id"],
                    "score": match["score"],
                    "metadata": match.get("metadata", {})
                }
                for match in results["matches"]
            ]
        
        except Exception as e:
            logger.error(f"Error searching similar itineraries: {e}")
            return []
    
    async def get_recommendations(
        self,
        destination: str,
        energy_level: str,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Get recommendations based on destination and energy level.
        
        Args:
            destination: Travel destination
            energy_level: User energy level (chill/balanced/adventurous)
            top_k: Number of recommendations
        
        Returns:
            List of recommended itineraries
        """
        query_text = f"Travel to {destination} for {energy_level} travelers"
        return await self.search_similar_itineraries(query_text, top_k)
