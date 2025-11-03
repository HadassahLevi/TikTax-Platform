"""
Category Pydantic Schemas
"""

from pydantic import BaseModel


class CategoryResponse(BaseModel):
    """Category response schema"""
    id: str
    name: str
    name_en: str
    icon: str
    color: str
    
    class Config:
        from_attributes = True
