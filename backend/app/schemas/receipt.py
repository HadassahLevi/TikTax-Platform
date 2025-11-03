"""
Receipt Pydantic Schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ReceiptBase(BaseModel):
    """Base receipt schema"""
    business_name: Optional[str] = None
    business_id: Optional[str] = None
    total_amount: float
    vat_amount: Optional[float] = None
    receipt_date: datetime
    receipt_number: Optional[str] = None
    category_id: Optional[str] = None


class ReceiptCreate(ReceiptBase):
    """Receipt creation schema"""
    pass


class ReceiptUpdate(BaseModel):
    """Receipt update schema"""
    business_name: Optional[str] = None
    business_id: Optional[str] = None
    total_amount: Optional[float] = None
    vat_amount: Optional[float] = None
    receipt_date: Optional[datetime] = None
    receipt_number: Optional[str] = None
    category_id: Optional[str] = None
    is_verified: Optional[bool] = None


class ReceiptResponse(ReceiptBase):
    """Receipt response schema"""
    id: str
    user_id: str
    image_url: str
    thumbnail_url: Optional[str] = None
    ocr_text: Optional[str] = None
    confidence_score: Optional[float] = None
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
