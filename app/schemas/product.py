"""Product schemas for API validation."""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class CategoryResponse(BaseModel):
    """Schema for category responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None

class ProductResponse(BaseModel):
    """Schema for product responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    stock_quantity: int
    category_id: int
    category: Optional[CategoryResponse] = None
    created_at: datetime

__all__ = ["ProductResponse", "CategoryResponse"]