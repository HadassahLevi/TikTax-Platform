"""
Database session management
Creates SQLAlchemy engine and session factory with connection pooling
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings

# Create database engine with optimized connection pool
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=10,           # Number of permanent connections
    max_overflow=20,        # Max additional connections beyond pool_size
    pool_pre_ping=True,     # Verifyxxxxxxctions before using (prevents stale connections)
    pool_recycle=3600,      # Recycle connections after 1 hour
    echo=False,             # Set to True for SQL logging in development
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    Database dependency for FastAPI endpoints.
    
    Usage:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
