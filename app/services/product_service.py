"""Product service for catalog management."""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from typing import List, Optional
from app.models.product import Product, Category

class ProductService:
    """Service for product operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_products(self, category_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get products with optional category filtering."""
        stmt = select(Product).options(joinedload(Product.category))
        
        if category_id:
            stmt = stmt.where(Product.category_id == category_id)
        
        stmt = stmt.offset(skip).limit(limit)
        return list(self.db.execute(stmt).scalars().all())
    
    def get_product(self, product_id: int) -> Optional[Product]:
        """Get product by ID with category."""
        stmt = select(Product).options(joinedload(Product.category)).where(Product.id == product_id)
        return self.db.execute(stmt).scalar_one_or_none()
    
    def get_categories(self) -> List[Category]:
        """Get all categories."""
        stmt = select(Category)
        return list(self.db.execute(stmt).scalars().all())
    
    def search_products(self, query: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """Search products by name or description."""
        stmt = select(Product).options(joinedload(Product.category)).where(
            Product.name.ilike(f"%{query}%") | Product.description.ilike(f"%{query}%")
        ).offset(skip).limit(limit)
        return list(self.db.execute(stmt).scalars().all())

__all__ = ["ProductService"]