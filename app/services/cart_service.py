"""Cart service for shopping cart management."""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, delete
from typing import List, Optional
from app.models.cart import CartItem
from app.models.product import Product
from app.schemas.cart import CartItemCreate

class CartService:
    """Service for cart operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_cart_items(self, user_id: int) -> List[CartItem]:
        """Get all cart items for a user."""
        stmt = select(CartItem).options(
            joinedload(CartItem.product).joinedload(Product.category)
        ).where(CartItem.user_id == user_id)
        return list(self.db.execute(stmt).scalars().all())
    
    def add_to_cart(self, user_id: int, cart_item: CartItemCreate) -> CartItem:
        """Add item to cart or update quantity if exists."""
        # Check if item already in cart
        stmt = select(CartItem).where(
            CartItem.user_id == user_id,
            CartItem.product_id == cart_item.product_id
        )
        existing_item = self.db.execute(stmt).scalar_one_or_none()
        
        if existing_item:
            existing_item.quantity += cart_item.quantity
            self.db.commit()
            self.db.refresh(existing_item)
            return existing_item
        else:
            db_cart_item = CartItem(
                user_id=user_id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity
            )
            self.db.add(db_cart_item)
            self.db.commit()
            self.db.refresh(db_cart_item)
            return db_cart_item
    
    def update_cart_item(self, user_id: int, cart_item_id: int, quantity: int) -> Optional[CartItem]:
        """Update cart item quantity."""
        stmt = select(CartItem).where(
            CartItem.id == cart_item_id,
            CartItem.user_id == user_id
        )
        cart_item = self.db.execute(stmt).scalar_one_or_none()
        
        if cart_item:
            if quantity <= 0:
                self.db.delete(cart_item)
            else:
                cart_item.quantity = quantity
            self.db.commit()
            return cart_item
        return None
    
    def remove_from_cart(self, user_id: int, cart_item_id: int) -> bool:
        """Remove item from cart."""
        stmt = delete(CartItem).where(
            CartItem.id == cart_item_id,
            CartItem.user_id == user_id
        )
        result = self.db.execute(stmt)
        self.db.commit()
        return result.rowcount > 0
    
    def clear_cart(self, user_id: int) -> bool:
        """Clear all items from cart."""
        stmt = delete(CartItem).where(CartItem.user_id == user_id)
        result = self.db.execute(stmt)
        self.db.commit()
        return result.rowcount > 0
    
    def get_cart_total(self, user_id: int) -> float:
        """Calculate total cart value."""
        cart_items = self.get_cart_items(user_id)
        return sum(item.product.price * item.quantity for item in cart_items)

__all__ = ["CartService"]