"""
Tests for Vibe-Check Travel Agent backend.
Unit tests for validators, security, and services.
"""

import pytest
from app.models import ItineraryRequest, EnergyLevel
from app.utils.validators import (
    validate_destination,
    validate_budget,
    validate_interests,
    sanitize_string
)
from app.utils.security import (
    generate_itinerary_id,
    hash_string,
    is_valid_gcs_bucket_name,
    sanitize_gcs_path
)


class TestValidators:
    """Test input validators."""
    
    def test_validate_destination_valid(self):
        """Test validation of valid destinations."""
        assert validate_destination("Paris") is True
        assert validate_destination("New York") is True
        assert validate_destination("Tokyo, Japan") is True
    
    def test_validate_destination_invalid(self):
        """Test validation of invalid destinations."""
        assert validate_destination("") is False
        assert validate_destination("A") is False
        assert validate_destination("Paris@#$") is False
    
    def test_validate_budget_valid(self):
        """Test budget validation."""
        assert validate_budget(500) is True
        assert validate_budget(5000) is True
        assert validate_budget(100) is True
    
    def test_validate_budget_invalid(self):
        """Test invalid budget amounts."""
        assert validate_budget(50) is False
        assert validate_budget(100001) is False
        assert validate_budget(0) is False
    
    def test_validate_interests(self):
        """Test interests validation."""
        assert validate_interests(["hiking", "museums"]) is True
        assert validate_interests([]) is False
        assert validate_interests(["a" * 100]) is False


class TestSecurity:
    """Test security utilities."""
    
    def test_generate_itinerary_id(self):
        """Test itinerary ID generation."""
        id1 = generate_itinerary_id()
        id2 = generate_itinerary_id()
        
        assert len(id1) == 16
        assert id1 != id2
    
    def test_hash_string(self):
        """Test string hashing."""
        hash1 = hash_string("test")
        hash2 = hash_string("test")
        hash3 = hash_string("different")
        
        assert hash1 == hash2
        assert hash1 != hash3
        assert len(hash1) == 64  # SHA256 hex length
    
    def test_valid_gcs_bucket_name(self):
        """Test GCS bucket name validation."""
        assert is_valid_gcs_bucket_name("valid-bucket-name") is True
        assert is_valid_gcs_bucket_name("bucket123") is True
    
    def test_invalid_gcs_bucket_name(self):
        """Test invalid bucket names."""
        assert is_valid_gcs_bucket_name("") is False
        assert is_valid_gcs_bucket_name("bucket-") is False
        assert is_valid_gcs_bucket_name("-bucket") is False
    
    def test_sanitize_gcs_path(self):
        """Test GCS path sanitization."""
        assert sanitize_gcs_path("../../../etc/passwd") == "etc/passwd"
        assert sanitize_gcs_path("/file.json") == "file.json"
        assert sanitize_gcs_path("valid/path/file.json") == "valid/path/file.json"


class TestItineraryRequest:
    """Test itinerary request model."""
    
    def test_valid_request(self):
        """Test creating valid itinerary request."""
        request = ItineraryRequest(
            destination="Paris",
            budget=2000,
            energy_level=EnergyLevel.BALANCED,
            days=5
        )
        
        assert request.destination == "Paris"
        assert request.budget == 2000
        assert request.energy_level == EnergyLevel.BALANCED
    
    def test_invalid_budget(self):
        """Test request validation with invalid budget."""
        with pytest.raises(ValueError):
            ItineraryRequest(
                destination="Paris",
                budget=50,  # Too low
                energy_level=EnergyLevel.CHILL
            )
    
    def test_invalid_days(self):
        """Test request validation with invalid days."""
        with pytest.raises(ValueError):
            ItineraryRequest(
                destination="Paris",
                budget=2000,
                energy_level=EnergyLevel.CHILL,
                days=50  # Too many
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
