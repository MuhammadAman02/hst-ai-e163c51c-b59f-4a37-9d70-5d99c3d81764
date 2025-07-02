from nicegui import ui, app as nicegui_app
from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import app_logger

def setup_nicegui(fastapi_app: FastAPI, ui_instance=None, settings_instance=None):
    """Sets up NiceGUI integration with FastAPI.
    
    Args:
        fastapi_app: The FastAPI application instance
        ui_instance: Optional NiceGUI UI instance (if not provided, uses imported ui)
        settings_instance: Optional settings instance (if not provided, uses imported settings)
    """
    app_logger.info("Setting up NiceGUI integration...")
    
    # Use provided instances or fall back to imports
    ui_obj = ui_instance or ui
    config = settings_instance or settings
    
    # Default mount path if not specified
    mount_path = getattr(config, 'NICEGUI_MOUNT_PATH', '/')
    
    # Mount NiceGUI to FastAPI
    ui_obj.run_with(fastapi_app, 
                mount_path=mount_path, 
                storage_secret=config.SECRET_KEY)
    
    app_logger.info(f"NiceGUI mounted at {mount_path}")
    app_logger.info("NiceGUI setup complete.")
    
    # Return the UI instance for convenience
    return ui_obj