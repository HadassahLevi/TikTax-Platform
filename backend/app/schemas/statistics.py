"""
Statistics Schemas
Pydantic models for analytics and dashboard data aggregation
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class MonthlyStat(BaseModel):
    """Statistics for a single month"""
    month: str = Field(..., description="YYYY-MM format", example="2024-01")
    total_receipts: int = Field(..., ge=0, description="Number of receipts in month")
    total_amount: float = Field(..., ge=0, description="Total amount for month")
    average_amount: float = Field(..., ge=0, description="Average amount per receipt")

    class Config:
        json_schema_extra = {
            "example": {
                "month": "2024-01",
                "total_receipts": 15,
                "total_amount": 2450.50,
                "average_amount": 163.37
            }
        }


class CategoryBreakdown(BaseModel):
    """Category statistics breakdown"""
    category_id: int = Field(..., description="Category ID")
    category_name: str = Field(..., description="Category name (Hebrew)")
    count: int = Field(..., ge=0, description="Number of receipts")
    total_amount: float = Field(..., ge=0, description="Total amount")
    percentage: float = Field(..., ge=0, le=100, description="Percentage of total")

    class Config:
        json_schema_extra = {
            "example": {
                "category_id": 1,
                "category_name": "משרד",
                "count": 8,
                "total_amount": 1200.50,
                "percentage": 35.2
            }
        }


class RecentReceiptSummary(BaseModel):
    """Summary of recent receipt for dashboard"""
    id: int
    vendor_name: Optional[str]
    receipt_date: Optional[str]
    total_amount: Optional[float]
    category_name: Optional[str]


class ReceiptStatistics(BaseModel):
    """
    Comprehensive dashboard statistics.
    Includes overall stats, monthly comparisons, subscription usage,
    category breakdown, recent receipts, and trends.
    """
    # Overall stats
    total_receipts: int = Field(..., ge=0, description="Total receipts all time")
    approved_receipts: int = Field(..., ge=0, description="Approved receipts")
    pending_receipts: int = Field(..., ge=0, description="Pending review receipts")
    
    # Current month
    monthly_receipts: int = Field(..., ge=0, description="Receipts this month")
    monthly_amount: float = Field(..., ge=0, description="Total amount this month")
    monthly_average: float = Field(..., ge=0, description="Average amount this month")
    
    # Previous month comparison
    prev_monthly_receipts: int = Field(..., ge=0, description="Receipts last month")
    prev_monthly_amount: float = Field(..., ge=0, description="Total amount last month")
    receipts_change_percent: float = Field(..., description="Month-over-month receipts change %")
    amount_change_percent: float = Field(..., description="Month-over-month amount change %")
    
    # Subscription usage
    receipts_limit: int = Field(..., ge=0, description="Monthly receipt limit")
    receipts_used: int = Field(..., ge=0, description="Receipts used this month")
    receipts_remaining: int = Field(..., ge=0, description="Receipts remaining")
    usage_percentage: float = Field(..., ge=0, le=100, description="Usage percentage")
    
    # Category breakdown (top 5)
    categories: List[CategoryBreakdown] = Field(default_factory=list, description="Top categories")
    
    # Recent receipts (last 5)
    recent_receipts: List[Dict] = Field(default_factory=list, description="Recent receipts")
    
    # Monthly trend (last 6 months)
    monthly_trend: List[MonthlyStat] = Field(default_factory=list, description="6-month trend")

    class Config:
        json_schema_extra = {
            "example": {
                "total_receipts": 150,
                "approved_receipts": 145,
                "pending_receipts": 5,
                "monthly_receipts": 25,
                "monthly_amount": 3500.75,
                "monthly_average": 140.03,
                "prev_monthly_receipts": 20,
                "prev_monthly_amount": 2800.50,
                "receipts_change_percent": 25.0,
                "amount_change_percent": 25.0,
                "receipts_limit": 50,
                "receipts_used": 25,
                "receipts_remaining": 25,
                "usage_percentage": 50.0,
                "categories": [],
                "recent_receipts": [],
                "monthly_trend": []
            }
        }


class YearlyReport(BaseModel):
    """
    Yearly tax report with comprehensive breakdown.
    Used for annual tax filing and accountant reports.
    """
    year: int = Field(..., description="Report year", example=2024)
    total_receipts: int = Field(..., ge=0, description="Total receipts for year")
    total_amount: float = Field(..., ge=0, description="Total amount for year")
    total_vat: float = Field(..., ge=0, description="Total VAT for year")
    categories: List[CategoryBreakdown] = Field(default_factory=list, description="Category breakdown")
    monthly_breakdown: List[MonthlyStat] = Field(default_factory=list, description="Monthly breakdown")

    class Config:
        json_schema_extra = {
            "example": {
                "year": 2024,
                "total_receipts": 300,
                "total_amount": 42000.00,
                "total_vat": 7140.00,
                "categories": [],
                "monthly_breakdown": []
            }
        }
