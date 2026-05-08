"""
Initialization file for backend app package.
"""

from app.config import get_settings
from app.main import app

__version__ = "1.0.0"
__all__ = ["app", "get_settings"]
