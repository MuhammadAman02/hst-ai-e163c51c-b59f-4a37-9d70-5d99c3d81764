"""Order schemas for API validation."""

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List
from app.schemas.product import ProductResponse

class OrderItemResponse(BaseModel):
    """Schema for order item responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    product_id: int
    quantity: int
    price: float
    product: ProductResponse

class OrderCreate(BaseModel):
    """Schema for creating orders."""
    pass  # Order will be created from current cart

class OrderResponse(BaseModel):
    """Schema for order responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    total_amount: float
    status: str
    created_at: datetime
    order_items: List[OrderItemResponse]

__all__ = ["OrderCreate", "OrderResponse"]