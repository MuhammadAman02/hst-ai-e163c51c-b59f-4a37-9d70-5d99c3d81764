"""Order service for purchase processing."""

from sqlalchemy.orm import Session
from typing import Optional
from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app.services.cart_service import CartService

class OrderService:
    """Service for order operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.cart_service = CartService(db)
    
    def create_order_from_cart(self, user_id: int) -> Optional[Order]:
        """Create order from current cart items."""
        cart_items = self.cart_service.get_cart_items(user_id)
        
        if not cart_items:
            return None
        
        # Calculate total
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        
        # Create order
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            status="confirmed"
        )
        self.db.add(order)
        self.db.flush()  # Get order ID
        
        # Create order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            self.db.add(order_item)
        
        # Clear cart
        self.cart_service.clear_cart(user_id)
        
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def get_user_orders(self, user_id: int) -> list[Order]:
        """Get all orders for a user."""
        from sqlalchemy import select
        from sqlalchemy.orm import joinedload
        
        stmt = select(Order).options(
            joinedload(Order.order_items).joinedload(OrderItem.product)
        ).where(Order.user_id == user_id).order_by(Order.created_at.desc())
        
        return list(self.db.execute(stmt).scalars().all())

__all__ = ["OrderService"]