"""User schemas for API validation."""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username")

class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8, description="User password")

class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

class UserResponse(UserBase):
    """Schema for user responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    created_at: datetime

__all__ = ["UserCreate", "UserResponse", "UserLogin"]