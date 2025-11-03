"""
Category SQLAlchemy Model
"""

from sqlalchemy import Column, String

from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Hebrew name
    name_en = Column(String, nullable=False)  # English name
    icon = Column(String, nullable=False)
    color = Column(String, nullable=False)
