"""Main API router for the Apple Store application."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.health import HealthCheck
from app.services import UserService, ProductService, CartService, OrderService
from app.schemas import (
    UserCreate, UserResponse, UserLogin,
    ProductResponse, CategoryResponse,
    CartItemCreate, CartResponse,
    OrderResponse
)
from app.core.security import create_access_token, verify_token

api_router = APIRouter()

# Health check
@api_router.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return HealthCheck.check_all()

# Authentication endpoints
@api_router.post("/auth/register", response_model=UserResponse, tags=["auth"])
async def register(user_create: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    user_service = UserService(db)
    
    # Check if user already exists
    if user_service.get_user_by_email(user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    return user_service.create_user(user_create)

@api_router.post("/auth/login", tags=["auth"])
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token."""
    user_service = UserService(db)
    user = user_service.authenticate_user(user_login.email, user_login.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer", "user": user}

# Product endpoints
@api_router.get("/categories", response_model=List[CategoryResponse], tags=["products"])
async def get_categories(db: Session = Depends(get_db)):
    """Get all product categories."""
    product_service = ProductService(db)
    return product_service.get_categories()

@api_router.get("/products", response_model=List[ProductResponse], tags=["products"])
async def get_products(
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get products with optional filtering."""
    product_service = ProductService(db)
    
    if search:
        return product_service.search_products(search, skip, limit)
    else:
        return product_service.get_products(category_id, skip, limit)

@api_router.get("/products/{product_id}", response_model=ProductResponse, tags=["products"])
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product by ID."""
    product_service = ProductService(db)
    product = product_service.get_product(product_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product

# Cart endpoints (simplified without authentication for demo)
@api_router.post("/cart/add", tags=["cart"])
async def add_to_cart(
    cart_item: CartItemCreate,
    user_id: int = 1,  # Simplified: using default user
    db: Session = Depends(get_db)
):
    """Add item to cart."""
    cart_service = CartService(db)
    return cart_service.add_to_cart(user_id, cart_item)

@api_router.get("/cart", response_model=CartResponse, tags=["cart"])
async def get_cart(user_id: int = 1, db: Session = Depends(get_db)):
    """Get cart contents."""
    cart_service = CartService(db)
    cart_items = cart_service.get_cart_items(user_id)
    total_amount = cart_service.get_cart_total(user_id)
    total_items = sum(item.quantity for item in cart_items)
    
    return CartResponse(
        items=cart_items,
        total_amount=total_amount,
        total_items=total_items
    )

@api_router.delete("/cart/{cart_item_id}", tags=["cart"])
async def remove_from_cart(
    cart_item_id: int,
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """Remove item from cart."""
    cart_service = CartService(db)
    success = cart_service.remove_from_cart(user_id, cart_item_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    return {"message": "Item removed from cart"}

# Order endpoints
@api_router.post("/orders", response_model=OrderResponse, tags=["orders"])
async def create_order(user_id: int = 1, db: Session = Depends(get_db)):
    """Create order from cart."""
    order_service = OrderService(db)
    order = order_service.create_order_from_cart(user_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    return order

@api_router.get("/orders", response_model=List[OrderResponse], tags=["orders"])
async def get_orders(user_id: int = 1, db: Session = Depends(get_db)):
    """Get user orders."""
    order_service = OrderService(db)
    return order_service.get_user_orders(user_id)

__all__ = ["api_router"]