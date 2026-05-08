"""
Input validation utilities for Vibe-Check Travel Agent.
"""

import re
from typing import List
from app.models import EnergyLevel


def validate_destination(destination: str) -> bool:
    """
    Validate destination string.
    
    Args:
        destination: Destination name to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not destination or len(destination) < 2 or len(destination) > 100:
        return False
    
    # Allow alphanumeric, spaces, hyphens, commas
    if not re.match(r'^[a-zA-Z0-9\s,\-]*$', destination):
        return False
    
    return True


def validate_budget(budget: int) -> bool:
    """
    Validate budget amount.
    
    Args:
        budget: Budget in USD
    
    Returns:
        bool: True if valid, False otherwise
    """
    return 100 <= budget <= 100000


def validate_interests(interests: List[str]) -> bool:
    """
    Validate interests list.
    
    Args:
        interests: List of interest strings
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not interests or len(interests) > 10:
        return False
    
    for interest in interests:
        if not isinstance(interest, str) or len(interest) < 2 or len(interest) > 50:
            return False
    
    return True


def sanitize_string(value: str, max_length: int = 100) -> str:
    """
    Sanitize string input.
    
    Args:
        value: String to sanitize
        max_length: Maximum allowed length
    
    Returns:
        str: Sanitized string
    """
    return value.strip()[:max_length]
