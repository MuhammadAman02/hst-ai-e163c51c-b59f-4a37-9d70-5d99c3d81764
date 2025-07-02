"""Database configuration using SQLAlchemy V2."""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from app.core.config import settings

# Create engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_recycle=300
)

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass

def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)

def get_db() -> Session:
    """Database session dependency."""
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()

__all__ = ["Base", "engine", "create_tables", "get_db"]