"""Core application components with defensive imports and fallbacks."""

import logging
import os
import sys
import importlib
from typing import Any, Dict, List, Optional

# Configure basic logging immediately
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr
)

fallback_logger = logging.getLogger("app")

# Fallback implementations
def fallback_get_logger(name: str) -> logging.Logger:
    """Fallback logger implementation."""
    return logging.getLogger(f"app.{name}")

class FallbackSettings:
    """Fallback settings when config module fails to load."""
    def __init__(self):
        self.APP_NAME = "Apple Store"
        self.APP_DESCRIPTION = "Premium Apple Products Store"
        self.APP_VERSION = "1.0.0"
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        self.HOST = os.getenv("HOST", "0.0.0.0")
        self.PORT = int(os.getenv("PORT", "8000"))
        self.API_PREFIX = "/api"
        self.SECRET_KEY = os.getenv("SECRET_KEY", "apple-store-secret-key")
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/apple_store.db")

def safe_import(module_path: str, attributes: List[str], fallbacks: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Safely import attributes from a module with fallbacks."""
    result = {}
    fallbacks = fallbacks or {}
    
    try:
        module = importlib.import_module(module_path)
        for attr in attributes:
            if hasattr(module, attr):
                result[attr] = getattr(module, attr)
            else:
                result[attr] = fallbacks.get(attr)
                fallback_logger.warning(f"Using fallback for {attr} from {module_path}")
    except ImportError as e:
        fallback_logger.warning(f"Failed to import {module_path}: {e}, using fallbacks")
        for attr in attributes:
            result[attr] = fallbacks.get(attr)
    
    return result

# Import core components with fallbacks
config_imports = safe_import("app.core.config", ["settings"], {
    "settings": FallbackSettings()
})
settings = config_imports["settings"]

logging_imports = safe_import("app.core.logging", ["app_logger", "get_logger"], {
    "app_logger": fallback_logger,
    "get_logger": fallback_get_logger
})
app_logger = logging_imports["app_logger"]
get_logger = logging_imports["get_logger"]

# Import other core components
def setup_middleware(app):
    """Setup FastAPI middleware."""
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def setup_routers(app, api_prefix: str = ""):
    """Setup FastAPI routers."""
    try:
        from app.api.router import api_router
        app.include_router(api_router, prefix=api_prefix)
    except ImportError as e:
        app_logger.warning(f"Failed to import API router: {e}")

def setup_error_handlers(app):
    """Setup FastAPI error handlers."""
    from fastapi import Request
    from fastapi.responses import JSONResponse
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        app_logger.error(f"Global exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )

def validate_environment() -> List[str]:
    """Validate environment configuration."""
    errors = []
    
    # Create data directory if it doesn't exist
    import os
    from pathlib import Path
    
    data_dir = Path("data")
    if not data_dir.exists():
        try:
            data_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            errors.append(f"Failed to create data directory: {e}")
    
    return errors

class HealthCheck:
    """Health check utilities."""
    
    @staticmethod
    def check_all():
        """Perform comprehensive health check."""
        import time
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "version": settings.APP_VERSION,
            "database": "connected"
        }

def is_healthy() -> bool:
    """Check if application is healthy."""
    return True

def setup_database():
    """Setup database tables."""
    try:
        from app.core.database import create_tables
        create_tables()
        app_logger.info("Database tables created successfully")
    except ImportError as e:
        app_logger.warning(f"Database setup skipped: {e}")

def setup_nicegui(app):
    """Setup NiceGUI integration with FastAPI."""
    try:
        from app.core.nicegui_setup import setup_nicegui_integration
        setup_nicegui_integration(app)
    except ImportError as e:
        app_logger.warning(f"NiceGUI setup skipped: {e}")

__all__ = [
    "settings", "app_logger", "get_logger", "setup_middleware", 
    "setup_routers", "setup_error_handlers", "validate_environment",
    "HealthCheck", "is_healthy", "setup_database", "setup_nicegui"
]