"""NiceGUI integration setup."""

from fastapi import FastAPI
from nicegui import app as nicegui_app

def setup_nicegui_integration(fastapi_app: FastAPI):
    """Setup NiceGUI integration with FastAPI."""
    # Mount NiceGUI app on FastAPI
    nicegui_app.include_router(fastapi_app)

__all__ = ["setup_nicegui_integration"]