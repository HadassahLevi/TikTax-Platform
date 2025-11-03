"""
Receipt Edit History SQLAlchemy Model
Tracks all manual edits to receipts
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class ReceiptEdit(Base):
    __tablename__ = "receipt_edits"
    
    id = Column(String, primary_key=True, index=True)
    receipt_id = Column(String, ForeignKey("receipts.id"), nullable=False)
    
    field_name = Column(String, nullable=False)
    old_value = Column(Text)
    new_value = Column(Text)
    
    edited_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    receipt = relationship("Receipt", back_populates="edits")
