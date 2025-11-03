"""
Subscription SQLAlchemy Model
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Stripe data
    stripe_customer_id = Column(String)
    stripe_subscription_id = Column(String)
    
    # Plan details
    plan_type = Column(String, nullable=False)  # "basic", "premium"
    price = Column(Float, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    status = Column(String, default="active")  # active, canceled, past_due
    
    # Timestamps
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    canceled_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="subscription")
