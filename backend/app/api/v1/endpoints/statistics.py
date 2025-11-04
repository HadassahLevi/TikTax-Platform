"""
Statistics API Endpoints
Dashboard analytics and reporting endpoints with optimized queries
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_
from datetime import datetime, timedelta
from typing import Optional
import logging

from app.db.session import get_db
from app.models.user import User
from app.models.receipt import Receipt, ReceiptStatus
from app.models.category import Category
from app.schemas.statistics import (
    ReceiptStatistics, CategoryBreakdown, MonthlyStat, YearlyReport
)
from app.core.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/dashboard", response_model=ReceiptStatistics)
async def get_dashboard_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive statistics for dashboard.
    
    Includes:
    - Overall receipt counts (total, approved, pending)
    - Current month stats with previous month comparison
    - Subscription usage tracking
    - Top 5 categories by spending
    - 5 most recent receipts
    - 6-month trend analysis
    
    **Performance:** Optimized with indexed queries and batch operations.
    **Caching:** Consider caching this endpoint for 5-10 minutes.
    """
    try:
        now = datetime.utcnow()
        current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        prev_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
        prev_month_end = current_month_start - timedelta(seconds=1)
        
        # ===== OVERALL STATS =====
        # Single query for all overall counts
        overall_counts = db.query(
            func.count(Receipt.id).label('total'),
            func.sum(func.cast(Receipt.status == ReceiptStatus.APPROVED, Integer)).label('approved'),
            func.sum(func.cast(
                Receipt.status.in_([ReceiptStatus.PROCESSING, ReceiptStatus.REVIEW]), 
                Integer
            )).label('pending')
        ).filter(
            Receipt.user_id == current_user.id
        ).first()
        
        total_receipts = overall_counts.total or 0
        approved_receipts = overall_counts.approved or 0
        pending_receipts = overall_counts.pending or 0
        
        # ===== CURRENT MONTH STATS =====
        current_month_stats = db.query(
            func.count(Receipt.id).label('count'),
            func.coalesce(func.sum(Receipt.total_amount), 0).label('amount')
        ).filter(
            Receipt.user_id == current_user.id,
            Receipt.receipt_date >= current_month_start,
            Receipt.status == ReceiptStatus.APPROVED
        ).first()
        
        monthly_receipts = current_month_stats.count or 0
        monthly_amount = float(current_month_stats.amount or 0)
        monthly_average = monthly_amount / monthly_receipts if monthly_receipts > 0 else 0.0
        
        # ===== PREVIOUS MONTH STATS =====
        prev_month_stats = db.query(
            func.count(Receipt.id).label('count'),
            func.coalesce(func.sum(Receipt.total_amount), 0).label('amount')
        ).filter(
            Receipt.user_id == current_user.id,
            Receipt.receipt_date >= prev_month_start,
            Receipt.receipt_date <= prev_month_end,
            Receipt.status == ReceiptStatus.APPROVED
        ).first()
        
        prev_monthly_receipts = prev_month_stats.count or 0
        prev_monthly_amount = float(prev_month_stats.amount or 0)
        
        # Calculate change percentages (handle division by zero)
        receipts_change = (
            ((monthly_receipts - prev_monthly_receipts) / prev_monthly_receipts * 100)
            if prev_monthly_receipts > 0 else 0.0
        )
        amount_change = (
            ((monthly_amount - prev_monthly_amount) / prev_monthly_amount * 100)
            if prev_monthly_amount > 0 else 0.0
        )
        
        # ===== SUBSCRIPTION USAGE =====
        receipts_used = current_user.receipts_used_this_month or 0
        receipts_limit = current_user.receipt_limit or 50
        receipts_remaining = max(0, receipts_limit - receipts_used)
        usage_percentage = (receipts_used / receipts_limit * 100) if receipts_limit > 0 else 0.0
        
        # ===== CATEGORY BREAKDOWN (TOP 5) =====
        category_stats = db.query(
            Receipt.category_id,
            Category.name_hebrew,
            func.count(Receipt.id).label('count'),
            func.sum(Receipt.total_amount).label('total')
        ).join(
            Category, Receipt.category_id == Category.id
        ).filter(
            Receipt.user_id == current_user.id,
            Receipt.status == ReceiptStatus.APPROVED,
            Receipt.category_id.isnot(None)
        ).group_by(
            Receipt.category_id,
            Category.name_hebrew
        ).order_by(
            func.sum(Receipt.total_amount).desc()
        ).limit(5).all()
        
        # Calculate total for percentage calculation
        total_categorized_amount = sum([stat.total for stat in category_stats]) or 1.0  # Avoid division by zero
        
        categories = [
            CategoryBreakdown(
                category_id=stat.category_id,
                category_name=stat.name_hebrew,
                count=stat.count,
                total_amount=float(stat.total or 0),
                percentage=float(stat.total or 0) / total_categorized_amount * 100
            )
            for stat in category_stats
        ]
        
        # ===== RECENT RECEIPTS (LAST 5 APPROVED) =====
        recent_receipts_query = db.query(
            Receipt.id,
            Receipt.vendor_name,
            Receipt.receipt_date,
            Receipt.total_amount,
            Category.name_hebrew.label('category_name')
        ).outerjoin(
            Category, Receipt.category_id == Category.id
        ).filter(
            Receipt.user_id == current_user.id,
            Receipt.status == ReceiptStatus.APPROVED
        ).order_by(
            Receipt.approved_at.desc()
        ).limit(5).all()
        
        recent_receipts = [
            {
                "id": receipt.id,
                "vendor_name": receipt.vendor_name,
                "receipt_date": receipt.receipt_date.isoformat() if receipt.receipt_date else None,
                "total_amount": receipt.total_amount,
                "category_name": receipt.category_name
            }
            for receipt in recent_receipts_query
        ]
        
        # ===== MONTHLY TREND (LAST 6 MONTHS) =====
        six_months_ago = current_month_start - timedelta(days=180)
        
        monthly_data = db.query(
            func.date_trunc('month', Receipt.receipt_date).label('month'),
            func.count(Receipt.id).label('count'),
            func.coalesce(func.sum(Receipt.total_amount), 0).label('total')
        ).filter(
            Receipt.user_id == current_user.id,
            Receipt.receipt_date >= six_months_ago,
            Receipt.status == ReceiptStatus.APPROVED
        ).group_by(
            func.date_trunc('month', Receipt.receipt_date)
        ).order_by('month').all()
        
        monthly_trend = [
            MonthlyStat(
                month=data.month.strftime('%Y-%m'),
                total_receipts=data.count,
                total_amount=float(data.total or 0),
                average_amount=float(data.total or 0) / data.count if data.count > 0 else 0.0
            )
            for data in monthly_data
        ]
        
        # ===== BUILD RESPONSE =====
        return ReceiptStatistics(
            # Overall
            total_receipts=total_receipts,
            approved_receipts=approved_receipts,
            pending_receipts=pending_receipts,
            # Current month
            monthly_receipts=monthly_receipts,
            monthly_amount=monthly_amount,
            monthly_average=monthly_average,
            # Previous month
            prev_monthly_receipts=prev_monthly_receipts,
            prev_monthly_amount=prev_monthly_amount,
            receipts_change_percent=round(receipts_change, 2),
            amount_change_percent=round(amount_change, 2),
            # Subscription
            receipts_limit=receipts_limit,
            receipts_used=receipts_used,
            receipts_remaining=receipts_remaining,
            usage_percentage=round(usage_percentage, 2),
            # Data
            categories=categories,
            recent_receipts=recent_receipts,
            monthly_trend=monthly_trend
        )
        
    except Exception as e:
        logger.error(f"Error fetching dashboard statistics: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch dashboard statistics"
        )


@router.get("/yearly", response_model=YearlyReport)
async def get_yearly_report(
    year: Optional[int] = Query(None, description="Year for report (defaults to current year)", ge=2000, le=2100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get yearly report for tax purposes.
    
    Includes:
    - Total receipts, amounts, and VAT for the year
    - Category breakdown with percentages
    - Monthly breakdown for trend analysis
    
    **Use Case:** Annual tax filing, accountant reports, business analysis.
    **Performance:** Optimized for year-end reporting.
    """
    try:
        # Default to current year if not specified
        if year is None:
            year = datetime.utcnow().year
        
        # Validate year range
        current_year = datetime.utcnow().year
        if year < 2000 or year > current_year + 1:
            raise HTTPException(
                status_code=400,
                detail=f"Year must be between 2000 and {current_year + 1}"
            )
        
        year_start = datetime(year, 1, 1, 0, 0, 0)
        year_end = datetime(year, 12, 31, 23, 59, 59)
        
        # ===== TOTAL STATS FOR YEAR =====
        year_stats = db.query(
            func.count(Receipt.id).label('count'),
            func.coalesce(func.sum(Receipt.total_amount), 0).label('total_amount'),
            func.coalesce(func.sum(Receipt.vat_amount), 0).label('total_vat')
        ).filter(
            Receipt.user_id == current_user.id,
            Receipt.receipt_date >= year_start,
            Receipt.receipt_date <= year_end,
            Receipt.status == ReceiptStatus.APPROVED
        ).first()
        
        total_receipts = year_stats.count or 0
        total_amount = float(year_stats.total_amount or 0)
        total_vat = float(year_stats.total_vat or 0)
        
        # ===== CATEGORY BREAKDOWN =====
        category_stats = db.query(
            Receipt.category_id,
            Category.name_hebrew,
            func.count(Receipt.id).label('count'),
            func.sum(Receipt.total_amount).label('total')
        ).join(
            Category, Receipt.category_id == Category.id
        ).filter(
            Receipt.user_id == current_user.id,
            Receipt.receipt_date >= year_start,
            Receipt.receipt_date <= year_end,
            Receipt.status == ReceiptStatus.APPROVED,
            Receipt.category_id.isnot(None)
        ).group_by(
            Receipt.category_id,
            Category.name_hebrew
        ).order_by(
            func.sum(Receipt.total_amount).desc()
        ).all()
        
        categories = [
            CategoryBreakdown(
                category_id=stat.category_id,
                category_name=stat.name_hebrew,
                count=stat.count,
                total_amount=float(stat.total or 0),
                percentage=float(stat.total or 0) / total_amount * 100 if total_amount > 0 else 0.0
            )
            for stat in category_stats
        ]
        
        # ===== MONTHLY BREAKDOWN =====
        monthly_data = db.query(
            extract('month', Receipt.receipt_date).label('month'),
            func.count(Receipt.id).label('count'),
            func.coalesce(func.sum(Receipt.total_amount), 0).label('total')
        ).filter(
            Receipt.user_id == current_user.id,
            Receipt.receipt_date >= year_start,
            Receipt.receipt_date <= year_end,
            Receipt.status == ReceiptStatus.APPROVED
        ).group_by(
            extract('month', Receipt.receipt_date)
        ).order_by('month').all()
        
        monthly_breakdown = [
            MonthlyStat(
                month=f"{year}-{int(data.month):02d}",
                total_receipts=data.count,
                total_amount=float(data.total or 0),
                average_amount=float(data.total or 0) / data.count if data.count > 0 else 0.0
            )
            for data in monthly_data
        ]
        
        # ===== BUILD RESPONSE =====
        return YearlyReport(
            year=year,
            total_receipts=total_receipts,
            total_amount=round(total_amount, 2),
            total_vat=round(total_vat, 2),
            categories=categories,
            monthly_breakdown=monthly_breakdown
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching yearly report: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch yearly report"
        )


@router.get("/category/{category_id}", response_model=CategoryBreakdown)
async def get_category_statistics(
    category_id: int,
    year: Optional[int] = Query(None, description="Filter by year"),
    month: Optional[int] = Query(None, description="Filter by month (1-12)", ge=1, le=12),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed statistics for a specific category.
    
    Optionally filter by year and/or month.
    """
    try:
        # Verify category exists
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        # Build date filter
        filters = [
            Receipt.user_id == current_user.id,
            Receipt.category_id == category_id,
            Receipt.status == ReceiptStatus.APPROVED
        ]
        
        if year:
            if month:
                # Specific month
                start_date = datetime(year, month, 1)
                if month == 12:
                    end_date = datetime(year + 1, 1, 1) - timedelta(seconds=1)
                else:
                    end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)
            else:
                # Whole year
                start_date = datetime(year, 1, 1)
                end_date = datetime(year, 12, 31, 23, 59, 59)
            
            filters.extend([
                Receipt.receipt_date >= start_date,
                Receipt.receipt_date <= end_date
            ])
        
        # Query category stats
        stats = db.query(
            func.count(Receipt.id).label('count'),
            func.coalesce(func.sum(Receipt.total_amount), 0).label('total')
        ).filter(and_(*filters)).first()
        
        # Get total for all categories in same period for percentage
        total_filters = [
            Receipt.user_id == current_user.id,
            Receipt.status == ReceiptStatus.APPROVED,
            Receipt.category_id.isnot(None)
        ]
        if year:
            total_filters.extend([
                Receipt.receipt_date >= start_date,
                Receipt.receipt_date <= end_date
            ])
        
        total_amount_all = db.query(
            func.coalesce(func.sum(Receipt.total_amount), 0)
        ).filter(and_(*total_filters)).scalar() or 1.0
        
        return CategoryBreakdown(
            category_id=category.id,
            category_name=category.name_hebrew,
            count=stats.count or 0,
            total_amount=float(stats.total or 0),
            percentage=float(stats.total or 0) / total_amount_all * 100 if total_amount_all > 0 else 0.0
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching category statistics: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch category statistics"
        )
