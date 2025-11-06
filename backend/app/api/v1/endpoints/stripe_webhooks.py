"""
Stripe Webhook Handler

Receives and processes webhook events from Stripe.
CRITICAL: Always verify webhook signatures for security!

Supported Events:
- checkout.session.completed: Subscription created
- customer.subscription.deleted: Subscription canceled
- invoice.payment_succeeded: Payment succeeded (renewal)
- invoice.payment_failed: Payment failed
"""

from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
import stripe
import logging

from app.core.config import settings
from app.core.dependencies import get_db
from app.services.stripe_service import get_stripe_service

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Handle Stripe webhook events
    
    Security:
    - Verifies webhook signature (CRITICAL!)
    - Validates event structure
    - Handles events idempotently
    
    Returns:
        200 OK on success (Stripe retries on failure)
    """
    # Get raw payload and signature
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    if not sig_header:
        logger.warning("Webhook received without signature")
        raise HTTPException(status_code=400, detail="Missing signature")
    
    # Verify webhook signature
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f"Invalid webhook payload: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid webhook signature: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Get event details
    event_type = event['type']
    event_id = event['id']
    event_data = event['data']['object']
    
    logger.info(f"Received webhook event: {event_type} ({event_id})")
    
    # Get Stripe service
    stripe_service = get_stripe_service(db)
    
    # Check if event already processed (idempotency)
    if stripe_service.is_event_processed(event_id):
        logger.info(f"Event {event_id} already processed, skipping")
        return {"status": "success", "message": "Event already processed"}
    
    # Handle different event types
    try:
        if event_type == 'checkout.session.completed':
            await _handle_checkout_completed(event_data, stripe_service)
            
        elif event_type == 'customer.subscription.deleted':
            await _handle_subscription_deleted(event_data, stripe_service)
            
        elif event_type == 'invoice.payment_succeeded':
            await _handle_invoice_payment_succeeded(event_data, stripe_service)
            
        elif event_type == 'invoice.payment_failed':
            await _handle_invoice_payment_failed(event_data, stripe_service)
            
        else:
            logger.info(f"Unhandled event type: {event_type}")
        
        # Mark event as processed
        stripe_service.mark_event_processed(event_id)
        
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Error processing webhook {event_type}: {str(e)}")
        # Return 200 to prevent Stripe retries for unrecoverable errors
        # For recoverable errors, raise HTTPException(500) to trigger retry
        return {"status": "error", "message": str(e)}


async def _handle_checkout_completed(session: dict, stripe_service) -> None:
    """Handle successful checkout"""
    try:
        # Only process subscription checkouts
        if session.get('mode') != 'subscription':
            logger.info("Skipping non-subscription checkout")
            return
        
        await stripe_service.handle_checkout_completed(session)
        logger.info(f"Checkout completed: {session['id']}")
        
    except Exception as e:
        logger.error(f"Error handling checkout completed: {str(e)}")
        raise


async def _handle_subscription_deleted(subscription: dict, stripe_service) -> None:
    """Handle subscription cancellation"""
    try:
        await stripe_service.handle_subscription_deleted(subscription)
        logger.info(f"Subscription deleted: {subscription['id']}")
        
    except Exception as e:
        logger.error(f"Error handling subscription deleted: {str(e)}")
        raise


async def _handle_invoice_payment_succeeded(invoice: dict, stripe_service) -> None:
    """Handle successful payment"""
    try:
        await stripe_service.handle_invoice_payment_succeeded(invoice)
        logger.info(f"Invoice payment succeeded: {invoice['id']}")
        
    except Exception as e:
        logger.error(f"Error handling invoice payment succeeded: {str(e)}")
        raise


async def _handle_invoice_payment_failed(invoice: dict, stripe_service) -> None:
    """Handle failed payment"""
    try:
        await stripe_service.handle_invoice_payment_failed(invoice)
        logger.warning(f"Invoice payment failed: {invoice['id']}")
        
    except Exception as e:
        logger.error(f"Error handling invoice payment failed: {str(e)}")
        raise
