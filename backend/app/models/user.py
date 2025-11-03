"""
User SQLAlchemy Model
"""

from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    
    # Personal info
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    business_name = Column(String)
    business_id = Column(String)  # Israeli business ID (ח.ב)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    receipts = relationship("Receipt", back_populates="user")
    subscription = relationship("Subscription", back_populates="user", uselist=False)
