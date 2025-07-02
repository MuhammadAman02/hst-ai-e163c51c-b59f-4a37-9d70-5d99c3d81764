"""Cart schemas for API validation."""

from pydantic import BaseModel, Field, ConfigDict
from typing import List
from app.schemas.product import ProductResponse

class CartItemCreate(BaseModel):
    """Schema for adding items to cart."""
    product_id: int = Field(..., description="Product ID")
    quantity: int = Field(default=1, ge=1, description="Quantity")

class CartItemResponse(BaseModel):
    """Schema for cart item responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    product_id: int
    quantity: int
    product: ProductResponse

class CartResponse(BaseModel):
    """Schema for cart responses."""
    items: List[CartItemResponse]
    total_amount: float
    total_items: int

__all__ = ["CartItemCreate", "CartItemResponse", "CartResponse"]