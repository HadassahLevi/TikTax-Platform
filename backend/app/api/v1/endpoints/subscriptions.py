"""
Subscription management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from app.core.dependencies import get_db, get_current_user
from app.schemas.user import SubscriptionResponse
from app.services.stripe_service import get_stripe_service
from app.core.config import settings

router = APIRouter()


# ==========================================
# REQUEST/RESPONSE MODELS
# ==========================================

class CheckoutRequest(BaseModel):
    """Request model for creating checkout session"""
    price_id: str
    billing_cycle: str  # 'monthly' or 'yearly'


class CheckoutResponse(BaseModel):
    """Response model for checkout session"""
    session_id: str
    checkout_url: str


class BillingHistoryItem(BaseModel):
    """Single billing history entry"""
    id: str
    date: str
    amount: float
    currency: str
    status: str
    invoice_pdf: Optional[str]
    hosted_invoice_url: Optional[str]


class CancellationResponse(BaseModel):
    """Response model for subscription cancellation"""
    status: str
    ends_at: Optional[str]
    message: str


class BillingPortalResponse(BaseModel):
    """Response model for billing portal"""
    portal_url: str


# ==========================================
# ENDPOINTS
# ==========================================

@router.get("/status", response_model=SubscriptionResponse)
async def get_subscription_status(
    current_user = Depends(get_current_user)
):
    """
    Get current subscription status
    
    Returns:
        Subscription details including plan, status, and dates
    """
    return SubscriptionResponse(
        user_id=current_user.id,
        subscription_plan=current_user.subscription_plan.value,
        subscription_status=current_user.subscription_status,
        subscription_start_date=current_user.subscription_start_date,
        subscription_end_date=current_user.subscription_end_date,
        receipt_limit=current_user.receipt_limit,
        receipts_used_this_month=current_user.receipts_used_this_month
    )


@router.post("/upgrade", response_model=CheckoutResponse)
async def create_checkout_session(
    request: CheckoutRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create Stripe checkout session for subscription upgrade
    
    Args:
        request: Contains price_id and billing_cycle
        
    Returns:
        Checkout session ID and URL for redirect
        
    Raises:
        400: Invalid price_id
        500: Stripe API error
    """
    stripe_service = get_stripe_service(db)
    
    # Build success and cancel URLs
    success_url = f"{settings.FRONTEND_URL}/checkout/success"
    cancel_url = f"{settings.FRONTEND_URL}/checkout/cancel"
    
    # Create checkout session
    result = await stripe_service.create_checkout_session(
        user_id=current_user.id,
        price_id=request.price_id,
        success_url=success_url,
        cancel_url=cancel_url
    )
    
    return CheckoutResponse(
        session_id=result['session_id'],
        checkout_url=result['checkout_url']
    )


@router.get("/billing-history", response_model=List[BillingHistoryItem])
async def get_billing_history(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    limit: int = 10
):
    """
    Get user's billing history (past invoices)
    
    Args:
        limit: Number of invoices to return (default: 10)
        
    Returns:
        List of invoice details with dates, amounts, and PDF links
    """
    stripe_service = get_stripe_service(db)
    
    history = await stripe_service.get_billing_history(
        user_id=current_user.id,
        limit=limit
    )
    
    return [BillingHistoryItem(**item) for item in history]


@router.post("/cancel", response_model=CancellationResponse)
async def cancel_subscription(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Cancel user's subscription (at period end)
    
    Subscription remains active until the end of the current billing period.
    
    Returns:
        Cancellation status and effective date
        
    Raises:
        400: No active subscription
        500: Stripe API error
    """
    stripe_service = get_stripe_service(db)
    
    result = await stripe_service.cancel_subscription(user_id=current_user.id)
    
    return CancellationResponse(
        status=result['status'],
        ends_at=result['ends_at'].isoformat() if result.get('ends_at') else None,
        message=result['message']
    )


@router.get("/billing-portal", response_model=BillingPortalResponse)
async def get_billing_portal(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get Stripe billing portal URL for customer self-service
    
    Allows users to:
    - Update payment methods
    - View billing history
    - Download invoices
    - Update billing information
    
    Returns:
        URL to Stripe-hosted billing portal
        
    Raises:
        400: No billing account found
        500: Stripe API error
    """
    stripe_service = get_stripe_service(db)
    
    portal_url = await stripe_service.get_billing_portal_url(user_id=current_user.id)
    
    return BillingPortalResponse(portal_url=portal_url)

