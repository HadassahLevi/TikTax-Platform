"""
Receipt SQLAlchemy Model
Manages receipt data, OCR processing, digital signatures, and user workflow
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, Text, JSON, Enum, Index
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base, TimestampMixin


class ReceiptStatus(enum.Enum):
    """Receipt processing workflow states"""
    PROCESSING = "processing"    # OCR in progress
    REVIEW = "review"           # Awaiting user approval
    APPROVED = "approved"       # User approved and archived
    FAILED = "failed"          # Processing failed
    DUPLICATE = "duplicate"     # Detected as duplicate


class Receipt(Base, TimestampMixin):
    """
    Receipt model with OCR data, digital signatures, and audit trail.
    
    Workflow:
    1. Upload → PROCESSING (OCR starts)
    2. OCR complete → REVIEW (user reviews)
    3. User approves → APPROVED (digitally signed + archived)
    
    Includes:
    - File storage (S3 URLs)
    - OCR extracted data (vendor, amounts, dates)
    - Processing metadata (confidence, status, timing)
    - Digital signature (Israeli CA compliance)
    - Duplicate detection
    - Edit history tracking
    """
    __tablename__ = "receipts"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # File Information
    original_filename = Column(String, nullable=False)
    file_url = Column(String, nullable=False)  # S3 URL to original image
    file_size = Column(Integer, nullable=False)  # bytes
    mime_type = Column(String, nullable=False)  # e.g., "image/jpeg"
    
    # Receipt Data (Extracted by OCR)
    vendor_name = Column(String, nullable=True)  # Business name
    business_number = Column(String(9), nullable=True)  # Israeli business number (ח.פ/ע.מ)
    receipt_number = Column(String, nullable=True)  # Receipt/invoice number
    receipt_date = Column(DateTime, nullable=True)  # Transaction date
    
    # Financial Data
    total_amount = Column(Float, nullable=True)  # Total including VAT
    vat_amount = Column(Float, nullable=True)  # VAT amount
    pre_vat_amount = Column(Float, nullable=True)  # Amount before VAT
    
    # Classification
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    # OCR Metadata
    ocr_data = Column(JSON, nullable=True)  # Full OCR response from Google Vision
    confidence_score = Column(Float, nullable=True)  # Overall confidence 0-100
    
    # Status & Workflow
    status = Column(Enum(ReceiptStatus), default=ReceiptStatus.PROCESSING, nullable=False)
    processing_started_at = Column(DateTime, nullable=True)
    processing_completed_at = Column(DateTime, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    
    # User Input
    notes = Column(Text, nullable=True)  # User notes/comments
    
    # Digital Signature (Israeli Compliance)
    is_digitally_signed = Column(Boolean, default=False, nullable=False)
    signature_timestamp = Column(DateTime, nullable=True)
    signature_certificate_id = Column(String, nullable=True)  # CA certificate ID
    
    # Duplicate Detection
    is_duplicate = Column(Boolean, default=False, nullable=False)
    duplicate_of_id = Column(Integer, ForeignKey("receipts.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="receipts")
    category = relationship("Category")
    edits = relationship("ReceiptEdit", back_populates="receipt", cascade="all, delete-orphan")
    
    # Performance Indexes
    __table_args__ = (
        Index('idx_receipt_user_id', 'user_id'),
        Index('idx_receipt_status', 'status'),
        Index('idx_receipt_date', 'receipt_date'),
        Index('idx_receipt_vendor', 'vendor_name'),
        Index('idx_receipt_business_number', 'business_number'),
        Index('idx_receipt_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Receipt(id={self.id}, vendor='{self.vendor_name}', amount={self.total_amount}, status={self.status.value})>"

