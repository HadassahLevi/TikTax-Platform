"""
Stripe Payment Integration Service

Handles all Stripe operations:
- Checkout session creation
- Subscription management
- Webhook event processing
- Customer management
- Billing portal access

Critical Security:
- Always verify webhook signatures
- Handle events idempotently
- Never expose secret keys to frontend
"""

import stripe
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core.config import settings
from app.models.user import User, SubscriptionPlan, SubscriptionStatus
from app.services.email_service import EmailService

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Logger
logger = logging.getLogger(__name__)

# Store processed webhook event IDs (simple in-memory cache for demo)
# In production, use Redis or database
processed_events = set()


class StripeService:
    """Service for Stripe payment operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.email_service = EmailService()
    
    # ==========================================
    # CHECKOUT & SUBSCRIPTION CREATION
    # ==========================================
    
    async def create_checkout_session(
        self,
        user_id: int,
        price_id: str,
        success_url: str,
        cancel_url: str
    ) -> Dict[str, str]:
        """
        Create Stripe Checkout session for subscription
        
        Args:
            user_id: User ID
            price_id: Stripe Price ID (from dashboard)
            success_url: URL to redirect after successful payment
            cancel_url: URL to redirect if user cancels
            
        Returns:
            Dict with session_id and checkout_url
            
        Raises:
            HTTPException: If user not found or Stripe error
        """
        try:
            # Get user
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            # Create or get Stripe customer
            customer_id = await self._get_or_create_customer(user)
            
            # Validate price ID
            if not self._is_valid_price_id(price_id):
                raise HTTPException(status_code=400, detail="Invalid price ID")
            
            # Create checkout session
            session = stripe.checkout.Session.create(
                customer=customer_id,
                mode='subscription',
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=cancel_url,
                allow_promotion_codes=True,
                billing_address_collection='auto',
                metadata={
                    'user_id': user_id,
                }
            )
            
            logger.info(f"Created checkout session for user {user_id}: {session.id}")
            
            return {
                'session_id': session.id,
                'checkout_url': session.url
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating checkout: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Payment system error: {str(e)}")
        except Exception as e:
            logger.error(f"Error creating checkout session: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to create checkout session")
    
    async def _get_or_create_customer(self, user: User) -> str:
        """
        Get existing Stripe customer or create new one
        
        Args:
            user: User object
            
        Returns:
            Stripe customer ID
        """
        # Return existing customer if available
        if user.stripe_customer_id:
            return user.stripe_customer_id
        
        # Create new customer
        customer = stripe.Customer.create(
            email=user.email,
            name=user.full_name,
            phone=user.phone_number,
            metadata={
                'user_id': user.id,
                'business_name': user.business_name or ''
            }
        )
        
        # Save customer ID to database
        user.stripe_customer_id = customer.id
        self.db.commit()
        
        logger.info(f"Created Stripe customer for user {user.id}: {customer.id}")
        
        return customer.id
    
    def _is_valid_price_id(self, price_id: str) -> bool:
        """Validate that price_id matches configured price IDs"""
        valid_price_ids = [
            settings.STRIPE_STARTER_MONTHLY_PRICE_ID,
            settings.STRIPE_STARTER_YEARLY_PRICE_ID,
            settings.STRIPE_PRO_MONTHLY_PRICE_ID,
            settings.STRIPE_PRO_YEARLY_PRICE_ID,
            settings.STRIPE_BUSINESS_MONTHLY_PRICE_ID,
            settings.STRIPE_BUSINESS_YEARLY_PRICE_ID,
        ]
        return price_id in valid_price_ids
    
    def _get_plan_from_price_id(self, price_id: str) -> SubscriptionPlan:
        """Map Stripe price ID to subscription plan"""
        if price_id in [settings.STRIPE_STARTER_MONTHLY_PRICE_ID, settings.STRIPE_STARTER_YEARLY_PRICE_ID]:
            return SubscriptionPlan.STARTER
        elif price_id in [settings.STRIPE_PRO_MONTHLY_PRICE_ID, settings.STRIPE_PRO_YEARLY_PRICE_ID]:
            return SubscriptionPlan.PRO
        elif price_id in [settings.STRIPE_BUSINESS_MONTHLY_PRICE_ID, settings.STRIPE_BUSINESS_YEARLY_PRICE_ID]:
            return SubscriptionPlan.BUSINESS
        else:
            return SubscriptionPlan.FREE
    
    def _is_yearly_price(self, price_id: str) -> bool:
        """Check if price ID is for yearly billing"""
        yearly_prices = [
            settings.STRIPE_STARTER_YEARLY_PRICE_ID,
            settings.STRIPE_PRO_YEARLY_PRICE_ID,
            settings.STRIPE_BUSINESS_YEARLY_PRICE_ID,
        ]
        return price_id in yearly_prices
    
    # ==========================================
    # WEBHOOK HANDLERS
    # ==========================================
    
    async def handle_checkout_completed(self, session: Dict) -> None:
        """
        Handle successful checkout completion
        
        Updates user subscription status and sends confirmation email
        
        Args:
            session: Stripe checkout session object
        """
        try:
            customer_id = session.get('customer')
            subscription_id = session.get('subscription')
            user_id = int(session['metadata']['user_id'])
            
            # Get user
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                logger.error(f"User {user_id} not found for checkout session")
                return
            
            # Get subscription details from Stripe
            subscription = stripe.Subscription.retrieve(subscription_id)
            price_id = subscription['items']['data'][0]['price']['id']
            
            # Determine plan and billing period
            plan = self._get_plan_from_price_id(price_id)
            is_yearly = self._is_yearly_price(price_id)
            
            # Calculate end date
            start_date = datetime.now()
            end_date = start_date + timedelta(days=365 if is_yearly else 30)
            
            # Update user subscription
            user.stripe_customer_id = customer_id
            user.stripe_subscription_id = subscription_id
            user.subscription_plan = plan
            user.subscription_status = "active"
            user.subscription_start_date = start_date
            user.subscription_end_date = end_date
            
            # Update receipt limit based on plan
            user.receipt_limit = self._get_receipt_limit(plan)
            
            self.db.commit()
            
            logger.info(f"Subscription activated for user {user_id}: {plan.value}")
            
            # Send confirmation email
            await self._send_subscription_confirmation_email(user, plan, is_yearly)
            
        except Exception as e:
            logger.error(f"Error handling checkout completed: {str(e)}")
            self.db.rollback()
    
    async def handle_subscription_deleted(self, subscription: Dict) -> None:
        """
        Handle subscription cancellation
        
        Downgrades user to free plan
        
        Args:
            subscription: Stripe subscription object
        """
        try:
            subscription_id = subscription.get('id')
            
            # Find user by subscription ID
            user = self.db.query(User).filter(
                User.stripe_subscription_id == subscription_id
            ).first()
            
            if not user:
                logger.warning(f"User not found for subscription {subscription_id}")
                return
            
            # Downgrade to free plan
            user.subscription_plan = SubscriptionPlan.FREE
            user.subscription_status = "canceled"
            user.stripe_subscription_id = None
            user.receipt_limit = 50
            
            self.db.commit()
            
            logger.info(f"Subscription canceled for user {user.id}")
            
            # Send cancellation email
            await self._send_subscription_canceled_email(user)
            
        except Exception as e:
            logger.error(f"Error handling subscription deleted: {str(e)}")
            self.db.rollback()
    
    async def handle_invoice_payment_succeeded(self, invoice: Dict) -> None:
        """
        Handle successful invoice payment (renewal)
        
        Extends subscription period
        
        Args:
            invoice: Stripe invoice object
        """
        try:
            subscription_id = invoice.get('subscription')
            
            if not subscription_id:
                return
            
            # Find user
            user = self.db.query(User).filter(
                User.stripe_subscription_id == subscription_id
            ).first()
            
            if not user:
                logger.warning(f"User not found for subscription {subscription_id}")
                return
            
            # Get subscription to determine billing period
            subscription = stripe.Subscription.retrieve(subscription_id)
            price_id = subscription['items']['data'][0]['price']['id']
            is_yearly = self._is_yearly_price(price_id)
            
            # Extend subscription
            current_end = user.subscription_end_date or datetime.now()
            user.subscription_end_date = current_end + timedelta(days=365 if is_yearly else 30)
            user.subscription_status = "active"  # Clear any past_due status
            
            self.db.commit()
            
            logger.info(f"Subscription renewed for user {user.id}")
            
            # Send payment receipt email
            await self._send_payment_receipt_email(user, invoice)
            
        except Exception as e:
            logger.error(f"Error handling invoice payment succeeded: {str(e)}")
            self.db.rollback()
    
    async def handle_invoice_payment_failed(self, invoice: Dict) -> None:
        """
        Handle failed invoice payment
        
        Updates status to past_due and sends notification
        
        Args:
            invoice: Stripe invoice object
        """
        try:
            subscription_id = invoice.get('subscription')
            
            if not subscription_id:
                return
            
            # Find user
            user = self.db.query(User).filter(
                User.stripe_subscription_id == subscription_id
            ).first()
            
            if not user:
                logger.warning(f"User not found for subscription {subscription_id}")
                return
            
            # Update status
            user.subscription_status = "past_due"
            
            self.db.commit()
            
            logger.warning(f"Payment failed for user {user.id}")
            
            # Send payment failure email
            await self._send_payment_failed_email(user, invoice)
            
        except Exception as e:
            logger.error(f"Error handling invoice payment failed: {str(e)}")
            self.db.rollback()
    
    # ==========================================
    # SUBSCRIPTION MANAGEMENT
    # ==========================================
    
    async def cancel_subscription(self, user_id: int) -> Dict[str, any]:
        """
        Cancel user's subscription (at period end)
        
        Args:
            user_id: User ID
            
        Returns:
            Cancellation details
            
        Raises:
            HTTPException: If no active subscription
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            if not user.stripe_subscription_id:
                raise HTTPException(status_code=400, detail="No active subscription")
            
            # Cancel at period end (user keeps access until then)
            subscription = stripe.Subscription.modify(
                user.stripe_subscription_id,
                cancel_at_period_end=True
            )
            
            # Update status
            user.subscription_status = "canceling"
            self.db.commit()
            
            logger.info(f"Subscription set to cancel for user {user_id}")
            
            # Send confirmation email
            await self._send_cancellation_confirmation_email(user)
            
            return {
                'status': 'canceling',
                'ends_at': user.subscription_end_date,
                'message': 'Subscription will be canceled at the end of the billing period'
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error canceling subscription: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Payment system error: {str(e)}")
        except Exception as e:
            logger.error(f"Error canceling subscription: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to cancel subscription")
    
    async def get_billing_portal_url(self, user_id: int) -> str:
        """
        Create billing portal session for customer self-service
        
        Args:
            user_id: User ID
            
        Returns:
            Billing portal URL
            
        Raises:
            HTTPException: If user has no Stripe customer
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            if not user.stripe_customer_id:
                raise HTTPException(status_code=400, detail="No billing account found")
            
            # Create portal session
            session = stripe.billing_portal.Session.create(
                customer=user.stripe_customer_id,
                return_url=f"{settings.FRONTEND_URL}/profile"
            )
            
            logger.info(f"Created billing portal session for user {user_id}")
            
            return session.url
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating portal: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Payment system error: {str(e)}")
        except Exception as e:
            logger.error(f"Error creating billing portal: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to create billing portal")
    
    async def get_billing_history(self, user_id: int, limit: int = 10) -> List[Dict]:
        """
        Get user's billing history (invoices)
        
        Args:
            user_id: User ID
            limit: Number of invoices to return
            
        Returns:
            List of invoice details
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user or not user.stripe_customer_id:
                return []
            
            # Fetch invoices from Stripe
            invoices = stripe.Invoice.list(
                customer=user.stripe_customer_id,
                limit=limit
            )
            
            # Format response
            history = []
            for invoice in invoices.data:
                history.append({
                    'id': invoice.id,
                    'date': datetime.fromtimestamp(invoice.created).isoformat(),
                    'amount': invoice.amount_paid / 100,  # Convert cents to currency
                    'currency': invoice.currency.upper(),
                    'status': invoice.status,
                    'invoice_pdf': invoice.invoice_pdf,
                    'hosted_invoice_url': invoice.hosted_invoice_url
                })
            
            return history
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error fetching billing history: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error fetching billing history: {str(e)}")
            return []
    
    # ==========================================
    # HELPER METHODS
    # ==========================================
    
    def _get_receipt_limit(self, plan: SubscriptionPlan) -> int:
        """Get receipt limit for subscription plan"""
        limits = {
            SubscriptionPlan.FREE: 50,
            SubscriptionPlan.STARTER: 200,
            SubscriptionPlan.PRO: 1000,
            SubscriptionPlan.BUSINESS: -1  # Unlimited
        }
        return limits.get(plan, 50)
    
    def is_event_processed(self, event_id: str) -> bool:
        """Check if webhook event already processed (idempotency)"""
        return event_id in processed_events
    
    def mark_event_processed(self, event_id: str) -> None:
        """Mark webhook event as processed"""
        processed_events.add(event_id)
        # In production, store in Redis with expiration
    
    # ==========================================
    # EMAIL NOTIFICATIONS
    # ==========================================
    
    async def _send_subscription_confirmation_email(self, user: User, plan: SubscriptionPlan, is_yearly: bool) -> None:
        """Send subscription confirmation email"""
        try:
            plan_names = {
                SubscriptionPlan.STARTER: "Starter",
                SubscriptionPlan.PRO: "Pro",
                SubscriptionPlan.BUSINESS: "Business"
            }
            
            await self.email_service.send_email(
                to_email=user.email,
                subject="🎉 המנוי שלך הופעל בהצלחה!",
                html_content=f"""
                <h2>שלום {user.full_name},</h2>
                <p>המנוי שלך לתוכנית <strong>{plan_names.get(plan, plan.value)}</strong> הופעל בהצלחה!</p>
                <p>תקופת חיוב: <strong>{'שנתי' if is_yearly else 'חודשי'}</strong></p>
                <p>תוקף עד: <strong>{user.subscription_end_date.strftime('%d/%m/%Y')}</strong></p>
                <p>תודה שבחרת ב-Tik-Tax! 🚀</p>
                """
            )
        except Exception as e:
            logger.error(f"Failed to send confirmation email: {str(e)}")
    
    async def _send_subscription_canceled_email(self, user: User) -> None:
        """Send subscription cancellation email"""
        try:
            await self.email_service.send_email(
                to_email=user.email,
                subject="המנוי שלך בוטל",
                html_content=f"""
                <h2>שלום {user.full_name},</h2>
                <p>המנוי שלך ל-Tik-Tax בוטל.</p>
                <p>חשבונך הועבר לתוכנית החינמית (עד 50 קבלות בחודש).</p>
                <p>אנחנו מקווים לראות אותך שוב בעתיד! 💙</p>
                """
            )
        except Exception as e:
            logger.error(f"Failed to send cancellation email: {str(e)}")
    
    async def _send_payment_receipt_email(self, user: User, invoice: Dict) -> None:
        """Send payment receipt email"""
        try:
            amount = invoice['amount_paid'] / 100
            await self.email_service.send_email(
                to_email=user.email,
                subject="קבלה על תשלום - Tik-Tax",
                html_content=f"""
                <h2>שלום {user.full_name},</h2>
                <p>התשלום שלך בסך <strong>₪{amount}</strong> בוצע בהצלחה.</p>
                <p>המנוי שלך חודש עד: <strong>{user.subscription_end_date.strftime('%d/%m/%Y')}</strong></p>
                <p><a href="{invoice.get('invoice_pdf', '#')}">הורד קבלה (PDF)</a></p>
                """
            )
        except Exception as e:
            logger.error(f"Failed to send payment receipt: {str(e)}")
    
    async def _send_payment_failed_email(self, user: User, invoice: Dict) -> None:
        """Send payment failure notification"""
        try:
            await self.email_service.send_email(
                to_email=user.email,
                subject="⚠️ בעיה בתשלום - Tik-Tax",
                html_content=f"""
                <h2>שלום {user.full_name},</h2>
                <p>לא הצלחנו לחייב את אמצעי התשלום שלך.</p>
                <p>נסה שוב תוך 3 ימים כדי להמשיך ליהנות מהמנוי.</p>
                <p><a href="{settings.FRONTEND_URL}/profile">עדכן פרטי תשלום</a></p>
                """
            )
        except Exception as e:
            logger.error(f"Failed to send payment failed email: {str(e)}")
    
    async def _send_cancellation_confirmation_email(self, user: User) -> None:
        """Send cancellation confirmation email"""
        try:
            await self.email_service.send_email(
                to_email=user.email,
                subject="אישור ביטול מנוי - Tik-Tax",
                html_content=f"""
                <h2>שלום {user.full_name},</h2>
                <p>המנוי שלך יבוטל ב-<strong>{user.subscription_end_date.strftime('%d/%m/%Y')}</strong>.</p>
                <p>עד אז תמשיך ליהנות מכל התכונות של התוכנית שלך.</p>
                <p>אם שינית דעתך, תוכל לחדש את המנוי בכל עת.</p>
                """
            )
        except Exception as e:
            logger.error(f"Failed to send cancellation confirmation: {str(e)}")


# Export singleton instance factory
def get_stripe_service(db: Session) -> StripeService:
    """Factory function to create StripeService instance"""
    return StripeService(db)
