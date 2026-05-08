"""
Security utilities for Vibe-Check Travel Agent.
Handles API keys, CORS, and input sanitization.
"""

import hashlib
import secrets
from typing import List
from datetime import datetime, timedelta
from functools import lru_cache


def generate_itinerary_id() -> str:
    """
    Generate a unique itinerary ID.
    
    Returns:
        str: Unique ID for itinerary
    """
    timestamp = datetime.utcnow().isoformat()
    random_suffix = secrets.token_hex(8)
    combined = f"{timestamp}{random_suffix}"
    return hashlib.sha256(combined.encode()).hexdigest()[:16]


def hash_string(value: str) -> str:
    """
    Hash a string value.
    
    Args:
        value: String to hash
    
    Returns:
        str: SHA256 hash of the value
    """
    return hashlib.sha256(value.encode()).hexdigest()


def is_valid_gcs_bucket_name(name: str) -> bool:
    """
    Validate Google Cloud Storage bucket name.
    
    Args:
        name: Bucket name to validate
    
    Returns:
        bool: True if valid bucket name format
    """
    if not name or len(name) < 3 or len(name) > 63:
        return False
    
    if not name.islower() and not name.isdigit():
        # Bucket names must be lowercase
        return False
    
    if name.startswith("-") or name.endswith("-"):
        return False
    
    if ".." in name:
        return False
    
    return True


def sanitize_gcs_path(path: str) -> str:
    """
    Sanitize Google Cloud Storage path.
    Prevents directory traversal attacks.
    
    Args:
        path: GCS path to sanitize
    
    Returns:
        str: Sanitized path
    """
    # Remove leading slashes and parent directory references
    sanitized = path.lstrip("/")
    sanitized = sanitized.replace("../", "").replace("..\\", "")
    return sanitized
