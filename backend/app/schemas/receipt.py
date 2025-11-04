"""
Receipt Pydantic Schemas
Request/response models for receipt operations
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum


class ReceiptStatus(str, Enum):
    """Receipt processing workflow states"""
    PROCESSING = "processing"
    REVIEW = "review"
    APPROVED = "approved"
    FAILED = "failed"
    DUPLICATE = "duplicate"


class ReceiptUploadResponse(BaseModel):
    """Response after successful receipt upload"""
    receipt_id: int
    status: ReceiptStatus
    message: str = "הקבלה הועלתה בהצלחה ונמצאת בעיבוד"
    
    class Config:
        from_attributes = True


class ReceiptProcessingStatus(BaseModel):
    """Real-time processing status for polling"""
    receipt_id: int
    status: ReceiptStatus
    progress: int = Field(..., ge=0, le=100, description="Progress percentage 0-100")
    message: str
    ocr_data: Optional[dict] = None
    
    class Config:
        from_attributes = True


class OCRConfidence(BaseModel):
    """Confidence scores for each extracted field"""
    vendor_name: Optional[float] = Field(None, ge=0.0, le=1.0)
    business_number: Optional[float] = Field(None, ge=0.0, le=1.0)
    receipt_number: Optional[float] = Field(None, ge=0.0, le=1.0)
    receipt_date: Optional[float] = Field(None, ge=0.0, le=1.0)
    total_amount: Optional[float] = Field(None, ge=0.0, le=1.0)
    vat_amount: Optional[float] = Field(None, ge=0.0, le=1.0)
    
    class Config:
        from_attributes = True


class ReceiptOCRData(BaseModel):
    """OCR extracted data from receipt"""
    vendor_name: Optional[str] = None
    business_number: Optional[str] = Field(None, max_length=9)
    receipt_number: Optional[str] = None
    receipt_date: Optional[str] = None
    total_amount: Optional[float] = Field(None, ge=0)
    vat_amount: Optional[float] = Field(None, ge=0)
    pre_vat_amount: Optional[float] = Field(None, ge=0)
    confidence: OCRConfidence = Field(default_factory=OCRConfidence)
    
    @validator('business_number')
    def validate_business_number(cls, v):
        """Validate Israeli business number format"""
        if v and not v.isdigit():
            raise ValueError('מספר עסק חייב להכיל ספרות בלבד')
        if v and len(v) != 9:
            raise ValueError('מספר עסק חייב להכיל 9 ספרות')
        return v
    
    class Config:
        from_attributes = True


class ReceiptBase(BaseModel):
    """Base receipt schema"""
    business_name: Optional[str] = None
    business_id: Optional[str] = None
    total_amount: float
    vat_amount: Optional[float] = None
    receipt_date: datetime
    receipt_number: Optional[str] = None
    category_id: Optional[int] = None


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
    category_id: Optional[int] = None
    is_verified: Optional[bool] = None
    notes: Optional[str] = None


class ReceiptResponse(BaseModel):
    """Receipt response schema with full details"""
    id: int
    user_id: int
    
    # File information
    original_filename: str
    file_url: str
    file_size: int
    mime_type: str
    
    # Receipt data
    vendor_name: Optional[str] = None
    business_number: Optional[str] = None
    receipt_number: Optional[str] = None
    receipt_date: Optional[datetime] = None
    total_amount: Optional[float] = None
    vat_amount: Optional[float] = None
    pre_vat_amount: Optional[float] = None
    
    # Classification
    category_id: Optional[int] = None
    
    # Processing status
    status: str
    confidence_score: Optional[float] = None
    ocr_data: Optional[dict] = None
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    approved_at: Optional[datetime] = None
    
    # User notes
    notes: Optional[str] = None
    
    # Digital signature
    is_digitally_signed: bool
    signature_timestamp: Optional[datetime] = None
    
    # Duplicate detection
    is_duplicate: bool
    duplicate_of_id: Optional[int] = None
    
    class Config:
        from_attributes = True
