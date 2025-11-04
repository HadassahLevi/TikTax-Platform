"""
Category SQLAlchemy Model
Receipt categorization system with Hebrew and English names
"""

from sqlalchemy import Column, String, Integer, Boolean

from app.db.base import Base


class Category(Base):
    """
    Receipt category model for expense classification.
    
    Includes system default categories and supports custom user categories.
    Used for organizing and filtering receipts in the archive.
    """
    __tablename__ = "categories"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Category Names (Bilingual)
    name_hebrew = Column(String, unique=True, nullable=False)  # e.g., "משרד"
    name_english = Column(String, unique=True, nullable=False)  # e.g., "Office"
    
    # Visual Properties
    icon = Column(String, nullable=False)  # Lucide icon name (e.g., "briefcase")
    color = Column(String, nullable=False)  # Hex color code (e.g., "#2563EB")
    
    # Category Type
    is_default = Column(Boolean, default=True, nullable=False)  # System category vs user-created
    sort_order = Column(Integer, default=0, nullable=False)  # Display order in UI
    
    def __repr__(self):
        return f"<Category(id={self.id}, name_he='{self.name_hebrew}', name_en='{self.name_english}')>"

