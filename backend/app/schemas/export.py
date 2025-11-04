"""
Export Pydantic Schemas
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class ExportFormat(str, Enum):
    """Supported export formats"""
    EXCEL = "excel"
    PDF = "pdf"
    CSV = "csv"


class ExportRequest(BaseModel):
    """Export request schema"""
    format: ExportFormat = Field(default=ExportFormat.EXCEL, description="Export format")
    date_from: datetime = Field(..., description="Start date (inclusive)")
    date_to: datetime = Field(..., description="End date (inclusive)")
    category_ids: Optional[List[int]] = Field(None, description="Filter by category IDs")
    include_images: bool = Field(default=False, description="Include receipt images in export")

    class Config:
        json_schema_extra = {
            "example": {
                "format": "excel",
                "date_from": "2024-01-01T00:00:00",
                "date_to": "2024-12-31T23:59:59",
                "category_ids": [1, 2, 3],
                "include_images": False
            }
        }


class ExportResponse(BaseModel):
    """Export response schema"""
    export_id: str = Field(..., description="Unique export identifier")
    download_url: str = Field(..., description="URL to download the export file")
    expires_at: datetime = Field(..., description="Expiration time for download link")
    file_size: int = Field(..., description="File size in bytes")
    message: str = Field(..., description="Success message in Hebrew")

    class Config:
        json_schema_extra = {
            "example": {
                "export_id": "550e8400-e29b-41d4-a716-446655440000",
                "download_url": "/api/v1/export/download/550e8400-e29b-41d4-a716-446655440000",
                "expires_at": "2024-01-01T13:00:00",
                "file_size": 45678,
                "message": "הקובץ הופק בהצלחה"
            }
        }
