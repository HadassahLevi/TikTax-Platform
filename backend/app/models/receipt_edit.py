"""
Receipt Edit History SQLAlchemy Model
Tracks all manual edits to receipts for audit trail and analytics
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class ReceiptEdit(Base):
    """
    Audit trail for receipt modifications.
    
    Tracks every manual edit users make to OCR-extracted data,
    enabling:
    - Edit history viewing
    - OCR accuracy improvement
    - Compliance audit trail
    - User behavior analytics
    """
    __tablename__ = "receipt_edits"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    receipt_id = Column(Integer, ForeignKey("receipts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Edit Details
    field_name = Column(String, nullable=False)  # e.g., "vendor_name", "total_amount"
    old_value = Column(String, nullable=True)    # Original value (JSON string if complex)
    new_value = Column(String, nullable=True)    # New value (JSON string if complex)
    
    # Timestamp
    edited_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    receipt = relationship("Receipt", back_populates="edits")
    
    def __repr__(self):
        return f"<ReceiptEdit(id={self.id}, receipt_id={self.receipt_id}, field='{self.field_name}')>"

