"""
User SQLAlchemy Model
Manages user accounts, authentication, business information, and subscription tracking
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum, Index
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base, TimestampMixin


class SubscriptionPlan(enum.Enum):
    """User subscription tiers with receipt limits"""
    FREE = "free"           # 50 receipts/month
    STARTER = "starter"     # 200 receipts/month
    PRO = "pro"            # 1000 receipts/month
    BUSINESS = "business"   # Unlimited receipts


class User(Base, TimestampMixin):
    """
    User model with authentication, business info, and subscription management.
    
    Includes:
    - Authentication (email, password, phone verification)
    - Business details (Israeli business number, type)
    - Subscription tracking (plan, limits, usage)
    - Account status (active, verified, last login)
    """
    __tablename__ = "users"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Authentication
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    id_number = Column(String(9), unique=True, nullable=False)  # Israeli ID (9 digits)
    phone_number = Column(String(15), nullable=False)
    is_phone_verified = Column(Boolean, default=False)
    
    # Business Information
    business_name = Column(String, nullable=True)
    business_number = Column(String(9), nullable=True)  # Israeli business number (ח.פ/ע.מ)
    business_type = Column(String, nullable=True)  # e.g., "עוסק מורשה", "חברה בע״מ"
    
    # Subscription & Limits
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.FREE, nullable=False)
    subscription_start_date = Column(DateTime, nullable=True)
    subscription_end_date = Column(DateTime, nullable=True)
    receipt_limit = Column(Integer, default=50, nullable=False)  # Monthly limit
    receipts_used_this_month = Column(Integer, default=0, nullable=False)
    
    # Account Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_email_verified = Column(Boolean, default=False, nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    receipts = relationship("Receipt", back_populates="user", cascade="all, delete-orphan")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_user_email', 'email'),
        Index('idx_user_id_number', 'id_number'),
        Index('idx_user_phone', 'phone_number'),
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', plan={self.subscription_plan.value})>"

