"""Main application entry point for Apple Store."""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed, skipping .env loading")

# Import NiceGUI and FastAPI
from nicegui import ui
from fastapi import FastAPI

# Import application components
try:
    import app.main  # This registers the NiceGUI pages
    from app.core import (
        settings, app_logger, setup_middleware, setup_routers,
        setup_error_handlers, validate_environment, setup_database
    )
except ImportError as e:
    print(f"Failed to import application modules: {e}")
    sys.exit(1)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url=f"{settings.api_prefix}/docs",
    redoc_url=f"{settings.api_prefix}/redoc",
)

# Setup FastAPI components
setup_error_handlers(app)
setup_middleware(app)
setup_routers(app, api_prefix=settings.api_prefix)

# Validate environment
errors = validate_environment()
if errors:
    for error in errors:
        app_logger.error(f"Environment validation error: {error}")

# Setup database
try:
    setup_database()
    app_logger.info("Database setup completed")
except Exception as e:
    app_logger.error(f"Database setup failed: {e}")

# Mount FastAPI on NiceGUI
ui.run_with(app, mount_path='/api')

if __name__ in {"__main__", "__mp_main__"}:
    try:
        app_logger.info(f"Starting Apple Store at {settings.host}:{settings.port}")
        ui.run(
            host=settings.host,
            port=settings.port,
            title=settings.app_name,
            favicon='🍎',
            reload=settings.debug,
            show=True,
            storage_secret=settings.secret_key
        )
    except Exception as e:
        app_logger.critical(f"Failed to start application: {e}")
        sys.exit(1)