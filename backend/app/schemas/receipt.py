"""
Receipt Pydantic Schemas
Request/response models for receipt operations
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
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


class ReceiptUpdate(BaseModel):
    """Receipt update schema for review process"""
    vendor_name: Optional[str] = Field(None, min_length=1, max_length=200)
    business_number: Optional[str] = Field(None, min_length=9, max_length=9)
    receipt_number: Optional[str] = Field(None, max_length=50)
    receipt_date: Optional[datetime] = None
    total_amount: Optional[float] = Field(None, gt=0)
    vat_amount: Optional[float] = Field(None, ge=0)
    pre_vat_amount: Optional[float] = Field(None, ge=0)
    category_id: Optional[int] = None
    notes: Optional[str] = Field(None, max_length=500)
    
    @validator('business_number')
    def validate_business_number(cls, v):
        """Validate Israeli business number format"""
        if v and not v.isdigit():
            raise ValueError('מספר עסק חייב להכיל ספרות בלבד')
        if v and len(v) != 9:
            raise ValueError('מספר עסק חייב להכיל 9 ספרות')
        return v


class ReceiptApprove(BaseModel):
    """Data for final approval"""
    vendor_name: str = Field(..., min_length=1, max_length=200)
    business_number: Optional[str] = Field(None, min_length=9, max_length=9)
    receipt_number: Optional[str] = Field(None, max_length=50)
    receipt_date: datetime
    total_amount: float = Field(..., gt=0)
    category_id: int
    notes: Optional[str] = Field(None, max_length=500)
    
    @validator('business_number')
    def validate_business_number(cls, v):
        """Validate Israeli business number format"""
        if v and not v.isdigit():
            raise ValueError('מספר עסק חייב להכיל ספרות בלבד')
        if v and len(v) != 9:
            raise ValueError('מספר עסק חייב להכיל 9 ספרות')
        return v


class ReceiptDetail(BaseModel):
    """Detailed receipt data with joined category name"""
    id: int
    user_id: int
    original_filename: str
    file_url: str
    file_size: int
    
    vendor_name: Optional[str]
    business_number: Optional[str]
    receipt_number: Optional[str]
    receipt_date: Optional[datetime]
    
    total_amount: Optional[float]
    vat_amount: Optional[float]
    pre_vat_amount: Optional[float]
    
    category_id: Optional[int]
    category_name: Optional[str]  # Joined from Category
    
    status: ReceiptStatus
    confidence_score: Optional[float]
    
    is_digitally_signed: bool
    is_duplicate: bool
    duplicate_of_id: Optional[int]
    
    notes: Optional[str]
    
    created_at: datetime
    updated_at: datetime
    approved_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ReceiptListItem(BaseModel):
    """Minimal receipt data for list views"""
    id: int
    vendor_name: Optional[str]
    receipt_date: Optional[datetime]
    total_amount: Optional[float]
    category_name: Optional[str]
    status: ReceiptStatus
    is_duplicate: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ReceiptListResponse(BaseModel):
    """Paginated receipt list response"""
    receipts: List[ReceiptListItem]
    total: int
    page: int
    page_size: int
    pages: int


class ReceiptFilterParams(BaseModel):
    """Filter parameters for receipt listing"""
    # Date range
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    
    # Categories (comma-separated IDs)
    category_ids: Optional[str] = None
    
    # Amount range
    amount_min: Optional[float] = None
    amount_max: Optional[float] = None
    
    # Status
    status: Optional[ReceiptStatus] = None
    
    # Search
    search_query: Optional[str] = None


class ReceiptSortParams(BaseModel):
    """Sort parameters for receipt listing"""
    sort_by: str = Field(default="created_at", pattern="^(created_at|receipt_date|total_amount|vendor_name)$")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")


class DuplicateCheckRequest(BaseModel):
    """Request to check if receipt is a duplicate"""
    vendor_name: str = Field(..., min_length=1, max_length=200)
    receipt_date: datetime
    total_amount: float = Field(..., gt=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "vendor_name": "סופר מרקט",
                "receipt_date": "2024-11-01T10:30:00",
                "total_amount": 150.50
            }
        }


class DuplicateCheckResponse(BaseModel):
    """Response from duplicate check"""
    is_duplicate: bool
    duplicate_receipt_id: Optional[int] = None
    similarity_score: float = Field(..., ge=0, le=100, description="Similarity percentage 0-100")
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "is_duplicate": True,
                "duplicate_receipt_id": 123,
                "similarity_score": 95.5,
                "message": "נמצאה קבלה דומה (95% דמיון)"
            }
        }


class SearchResult(BaseModel):
    """Single search result"""
    receipt_id: int
    vendor_name: Optional[str]
    receipt_date: Optional[datetime]
    total_amount: Optional[float]
    category_name: Optional[str]
    relevance_score: float = Field(..., ge=0, description="Relevance score (higher is better)")
    matched_field: Optional[str] = Field(None, description="Field that matched the query")
    
    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    """Response from receipt search"""
    results: List[SearchResult]
    total: int
    query: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "results": [
                    {
                        "receipt_id": 123,
                        "vendor_name": "סופר מרקט",
                        "receipt_date": "2024-11-01T10:30:00",
                        "total_amount": 150.50,
                        "category_name": "מזון",
                        "relevance_score": 100.0,
                        "matched_field": "vendor_name"
                    }
                ],
                "total": 1,
                "query": "סופר"
            }
        }


class ReceiptEditHistory(BaseModel):
    """Edit history entry for a receipt field"""
    id: int
    field_name: str
    field_name_hebrew: Optional[str] = None
    old_value: Optional[str]
    new_value: Optional[str]
    edited_at: datetime
    
    class Config:
        from_attributes = True


class ReceiptHistoryResponse(BaseModel):
    """Complete edit history for a receipt"""
    receipt_id: int
    edits: List[ReceiptEditHistory]
    total_edits: int


