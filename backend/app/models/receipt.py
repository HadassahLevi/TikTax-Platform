"""
Receipt SQLAlchemy Model
"""

from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Receipt(Base):
    __tablename__ = "receipts"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    category_id = Column(String, ForeignKey("categories.id"))
    
    # Receipt data
    business_name = Column(String)
    business_id = Column(String)  # מספר עוסק
    total_amount = Column(Float, nullable=False)
    vat_amount = Column(Float)
    receipt_date = Column(DateTime, nullable=False)
    receipt_number = Column(String)
    
    # OCR data
    ocr_text = Column(Text)
    confidence_score = Column(Float)
    
    # File storage
    image_url = Column(String, nullable=False)
    thumbnail_url = Column(String)
    
    # Status
    is_verified = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="receipts")
    category = relationship("Category")
    edits = relationship("ReceiptEdit", back_populates="receipt")
