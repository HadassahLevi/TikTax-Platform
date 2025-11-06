# 🚀 Stripe Payment Integration - Complete Setup Guide

## ✅ Implementation Summary

Complete Stripe payment integration for Tik-Tax subscription management.

### 📦 What Was Implemented

#### Backend (Python/FastAPI):
1. **✅ Stripe Service** (`app/services/stripe_service.py`)
   - Checkout session creation
   - Customer management
   - Subscription lifecycle handling
   - Webhook event processing
   - Billing history retrieval
   - Billing portal access

2. **✅ Webhook Handler** (`app/api/v1/endpoints/stripe_webhooks.py`)
   - Signature verification (CRITICAL for security)
   - Idempotent event processing
   - Support for: checkout.session.completed, customer.subscription.deleted, invoice.payment_succeeded, invoice.payment_failed

3. **✅ Subscription Endpoints** (`app/api/v1/endpoints/subscriptions.py`)
   - POST /subscriptions/upgrade - Create checkout session
   - GET /subscriptions/billing-history - Fetch invoices
   - POST /subscriptions/cancel - Cancel subscription
   - GET /subscriptions/billing-portal - Get portal URL
   - GET /subscriptions/status - Get current subscription

4. **✅ User Model Updates** (`app/models/user.py`)
   - stripe_customer_id
   - stripe_subscription_id
   - subscription_status (active, canceled, past_due, canceling)

5. **✅ Configuration** (`app/core/config.py`)
   - All Stripe settings added
   - Price ID configurations

#### Frontend (React/TypeScript):
1. **✅ Subscription Service** (`src/services/subscription.service.ts`)
   - createCheckout()
   - getSubscriptionStatus()
   - getBillingHistory()
   - cancelSubscription()
   - getBillingPortal()

2. **✅ Checkout Success Page** (`src/pages/CheckoutSuccessPage.tsx`)
   - Success animation
   - Subscription details display
   - Auto-redirect to dashboard

3. **✅ Checkout Cancel Page** (`src/pages/CheckoutCancelPage.tsx`)
   - Cancel message
   - Return to subscriptions
   - Contact support

4. **✅ Updated Subscription Page** (`src/pages/SubscriptionPage.tsx`)
   - Real Stripe checkout integration
   - Loading states
   - Price ID mapping

5. **✅ Routes** (`src/App.tsx`)
   - /checkout/success
   - /checkout/cancel

---

## 🔧 Environment Setup

### Step 1: Create Stripe Account
1. Go to https://stripe.com
2. Sign up for a new account
3. Complete business verification

### Step 2: Create Products in Stripe Dashboard

Go to **Products** → **Add Product** and create:

#### Product 1: Starter
- **Name:** Tik-Tax Starter
- **Description:** 200 receipts per month
- **Pricing:**
  - Monthly: ₪49/month (recurring)
  - Yearly: ₪470/year (recurring, save ₪118)

#### Product 2: Pro (Recommended)
- **Name:** Tik-Tax Pro
- **Description:** 1,000 receipts per month
- **Pricing:**
  - Monthly: ₪99/month (recurring)
  - Yearly: ₪950/year (recurring, save ₪238)

#### Product 3: Business
- **Name:** Tik-Tax Business
- **Description:** Unlimited receipts
- **Pricing:**
  - Monthly: ₪199/month (recurring)
  - Yearly: ₪1,910/year (recurring, save ₪478)

**Important:** After creating each price, copy the **Price ID** (starts with `price_...`)

### Step 3: Get API Keys

1. Go to **Developers** → **API Keys**
2. Copy **Publishable key** (starts with `pk_test_...`)
3. Reveal and copy **Secret key** (starts with `sk_test_...`)

⚠️ **NEVER commit secret keys to git!**

### Step 4: Set Up Webhook Endpoint

1. Install Stripe CLI:
   ```bash
   # Windows (using Scoop)
   scoop install stripe
   
   # Or download from: https://stripe.com/docs/stripe-cli
   ```

2. Login to Stripe:
   ```bash
   stripe login
   ```

3. Forward webhooks to local server:
   ```bash
   stripe listen --forward-to localhost:8000/api/v1/stripe/webhook
   ```

4. Copy the **webhook signing secret** (starts with `whsec_...`)

---

## 📝 Backend Environment Variables

Create/Update `backend/.env`:

```env
# =====================================================
# STRIPE CONFIGURATION
# =====================================================

# Stripe API Keys (from Stripe Dashboard → Developers → API Keys)
STRIPE_SECRET_KEY=sk_test_YOUR_SECRET_KEY_HERE
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_PUBLISHABLE_KEY_HERE

# Webhook Secret (from Stripe CLI: stripe listen --forward-to ...)
STRIPE_WEBHOOK_SECRET=whsec_YOUR_WEBHOOK_SECRET_HERE

# =====================================================
# STRIPE PRICE IDs (from Stripe Dashboard → Products)
# =====================================================

# Starter Plan Price IDs
STRIPE_STARTER_MONTHLY_PRICE_ID=price_STARTER_MONTHLY_ID_HERE
STRIPE_STARTER_YEARLY_PRICE_ID=price_STARTER_YEARLY_ID_HERE

# Pro Plan Price IDs
STRIPE_PRO_MONTHLY_PRICE_ID=price_PRO_MONTHLY_ID_HERE
STRIPE_PRO_YEARLY_PRICE_ID=price_PRO_YEARLY_ID_HERE

# Business Plan Price IDs
STRIPE_BUSINESS_MONTHLY_PRICE_ID=price_BUSINESS_MONTHLY_ID_HERE
STRIPE_BUSINESS_YEARLY_PRICE_ID=price_BUSINESS_YEARLY_ID_HERE

# Frontend URL (for redirects after checkout)
FRONTEND_URL=http://localhost:5173
```

---

## 📝 Frontend Environment Variables

Create/Update `frontend/.env`:

```env
# =====================================================
# STRIPE CONFIGURATION (Frontend)
# =====================================================

# Stripe Publishable Key (safe to expose in frontend)
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_PUBLISHABLE_KEY_HERE

# Stripe Price IDs (same as backend)
VITE_STRIPE_STARTER_MONTHLY_PRICE_ID=price_STARTER_MONTHLY_ID_HERE
VITE_STRIPE_STARTER_YEARLY_PRICE_ID=price_STARTER_YEARLY_ID_HERE
VITE_STRIPE_PRO_MONTHLY_PRICE_ID=price_PRO_MONTHLY_ID_HERE
VITE_STRIPE_PRO_YEARLY_PRICE_ID=price_PRO_YEARLY_ID_HERE
VITE_STRIPE_BUSINESS_MONTHLY_PRICE_ID=price_BUSINESS_MONTHLY_ID_HERE
VITE_STRIPE_BUSINESS_YEARLY_PRICE_ID=price_BUSINESS_YEARLY_ID_HERE
```

---

## 🗄️ Database Migration

Run the migration to add Stripe fields to users table:

```bash
cd backend
alembic upgrade head
```

If migration file doesn't exist, create it:

```bash
alembic revision -m "add_stripe_fields_to_user"
```

Then edit the migration file with the SQL from `alembic_migration_stripe.py`.

---

## 🧪 Testing Guide

### Test 1: Checkout Flow

1. **Start backend:**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Start frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Start Stripe webhook forwarding:**
   ```bash
   stripe listen --forward-to localhost:8000/api/v1/stripe/webhook
   ```

4. **Test checkout:**
   - Navigate to http://localhost:5173
   - Click "שדרג עכשיו" on any paid plan
   - Use Stripe test card: `4242 4242 4242 4242`
   - Expiry: Any future date
   - CVC: Any 3 digits
   - Complete checkout

5. **Verify:**
   - ✅ Redirected to /checkout/success
   - ✅ Subscription details shown
   - ✅ Auto-redirect after 5 seconds
   - ✅ User subscription updated in database
   - ✅ Webhook received and processed (check logs)

### Test 2: Cancel Checkout

1. Click upgrade
2. Click "Back" or close checkout
3. Verify redirected to /checkout/cancel
4. Verify message shows "no charge"

### Test 3: Webhook Events

Trigger test webhooks manually:

```bash
stripe trigger checkout.session.completed
stripe trigger customer.subscription.deleted
stripe trigger invoice.payment_succeeded
stripe trigger invoice.payment_failed
```

Check backend logs to verify processing.

### Test 4: Subscription Cancellation

```bash
curl -X POST http://localhost:8000/api/v1/subscriptions/cancel \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Verify:
- ✅ Subscription marked as "canceling"
- ✅ Access continues until period end
- ✅ Email notification sent

### Test 5: Billing Portal

```bash
curl http://localhost:8000/api/v1/subscriptions/billing-portal \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Verify:
- ✅ Returns portal URL
- ✅ Can update payment method
- ✅ Can view billing history

---

## 🎯 Test Cards (Stripe Test Mode)

| Scenario | Card Number | Behavior |
|----------|-------------|----------|
| Success | 4242 4242 4242 4242 | Payment succeeds |
| Decline | 4000 0000 0000 0002 | Generic decline |
| Insufficient Funds | 4000 0000 0000 9995 | Insufficient funds |
| 3D Secure | 4000 0027 6000 3184 | Requires authentication |

Expiry: Any future date  
CVC: Any 3 digits  
ZIP: Any 5 digits

---

## 🔐 Security Checklist

✅ **Webhook Signature Verification**
- ALWAYS verify webhook signatures
- Reject requests with invalid signatures
- Implemented in `stripe_webhooks.py`

✅ **Secret Keys Protection**
- NEVER commit .env files
- Secret keys stored server-side only
- Publishable keys safe for frontend

✅ **Idempotent Webhook Handling**
- Check event IDs before processing
- Prevent duplicate processing
- Implemented with `processed_events` set

✅ **Input Validation**
- Validate price IDs before checkout
- Check user permissions
- Sanitize all inputs

✅ **HTTPS in Production**
- Required for Stripe webhooks
- Required for checkout redirects

---

## 🚀 Production Deployment

### Before Going Live:

1. **Switch to Live Mode:**
   - Get live API keys (start with `pk_live_...` and `sk_live_...`)
   - Update all environment variables

2. **Create Live Products:**
   - Recreate all products in live mode
   - Update price IDs in .env

3. **Set Up Production Webhook:**
   - Go to Stripe Dashboard → Developers → Webhooks
   - Add endpoint: `https://api.tiktax.co.il/api/v1/stripe/webhook`
   - Select events:
     - checkout.session.completed
     - customer.subscription.deleted
     - invoice.payment_succeeded
     - invoice.payment_failed
   - Copy webhook signing secret

4. **Test in Production:**
   - Use real credit card (your own)
   - Complete full checkout flow
   - Cancel immediately if needed
   - Verify webhooks received

5. **Monitor:**
   - Check Stripe Dashboard daily
   - Review webhook logs
   - Monitor subscription metrics

---

## 📊 API Endpoints Reference

### Create Checkout Session
```http
POST /api/v1/subscriptions/upgrade
Content-Type: application/json
Authorization: Bearer {token}

{
  "price_id": "price_...",
  "billing_cycle": "monthly"
}

Response:
{
  "session_id": "cs_...",
  "checkout_url": "https://checkout.stripe.com/..."
}
```

### Get Billing History
```http
GET /api/v1/subscriptions/billing-history?limit=10
Authorization: Bearer {token}

Response:
[
  {
    "id": "in_...",
    "date": "2025-11-07T10:00:00",
    "amount": 99.0,
    "currency": "ILS",
    "status": "paid",
    "invoice_pdf": "https://...",
    "hosted_invoice_url": "https://..."
  }
]
```

### Cancel Subscription
```http
POST /api/v1/subscriptions/cancel
Authorization: Bearer {token}

Response:
{
  "status": "canceling",
  "ends_at": "2025-12-07T10:00:00",
  "message": "Subscription will be canceled at the end of the billing period"
}
```

### Get Billing Portal
```http
GET /api/v1/subscriptions/billing-portal
Authorization: Bearer {token}

Response:
{
  "portal_url": "https://billing.stripe.com/..."
}
```

---

## 🐛 Troubleshooting

### Issue: Webhook not received

**Solution:**
1. Check Stripe CLI is running: `stripe listen --forward-to ...`
2. Verify webhook secret in .env matches CLI output
3. Check backend logs for errors
4. Test manually: `stripe trigger checkout.session.completed`

### Issue: Checkout redirect fails

**Solution:**
1. Verify FRONTEND_URL in backend .env
2. Check CORS settings allow frontend origin
3. Verify success_url and cancel_url are correct

### Issue: Payment succeeds but subscription not activated

**Solution:**
1. Check webhook was received (backend logs)
2. Verify user_id in session metadata
3. Check database for subscription update
4. Review webhook event processing logs

### Issue: Invalid price ID error

**Solution:**
1. Verify price IDs in .env match Stripe Dashboard
2. Check price belongs to correct product
3. Ensure price is active in Stripe
4. Verify test/live mode consistency

---

## 📚 Documentation Links

- **Stripe Documentation:** https://stripe.com/docs
- **Stripe Testing:** https://stripe.com/docs/testing
- **Stripe Webhooks:** https://stripe.com/docs/webhooks
- **Stripe Checkout:** https://stripe.com/docs/payments/checkout
- **Stripe CLI:** https://stripe.com/docs/stripe-cli

---

## ✨ Features Implemented

✅ Subscription checkout with Stripe  
✅ Multiple billing periods (monthly/yearly)  
✅ Webhook handling (secure signature verification)  
✅ Subscription lifecycle management  
✅ Billing history retrieval  
✅ Customer billing portal  
✅ Subscription cancellation  
✅ Email notifications  
✅ Success/cancel pages  
✅ Loading states  
✅ Error handling  
✅ Hebrew UI support  
✅ Mobile-responsive design  

---

## 🎉 You're All Set!

Follow the steps above to complete your Stripe integration. If you run into issues, refer to the troubleshooting section or contact Stripe support.

**Happy coding! 🚀**
