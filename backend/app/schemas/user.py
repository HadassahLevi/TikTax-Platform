"""
User Pydantic Schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    first_name: str
    last_name: str
    phone: str
    business_name: Optional[str] = None
    business_id: Optional[str] = None


class UserResponse(UserBase):
    """User response schema"""
    id: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """User update schema"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    business_name: Optional[str] = None
    business_id: Optional[str] = None


class SubscriptionResponse(BaseModel):
    """Subscription response schema"""
    id: str
    plan_type: str
    price: float
    is_active: bool
    status: str
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    
    class Config:
        from_attributes = True
