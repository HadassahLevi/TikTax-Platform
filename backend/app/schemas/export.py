"""
Export Pydantic Schemas
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class ExportRequest(BaseModel):
    """Export request schema"""
    start_date: datetime
    end_date: datetime
    category_ids: Optional[List[str]] = None
    format: str = "excel"  # "excel" or "pdf"
