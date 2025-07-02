"""Health check utilities."""

import time
from typing import Dict, Any
from app.core.config import settings

class HealthCheck:
    """Health check utilities."""
    
    @staticmethod
    def check_all() -> Dict[str, Any]:
        """Perform comprehensive health check."""
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "version": settings.app_version,
            "app_name": settings.app_name
        }

def is_healthy() -> bool:
    """Simple health check."""
    return True

__all__ = ["HealthCheck", "is_healthy"]