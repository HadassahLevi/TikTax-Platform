# ✅ Stripe Integration Setup Checklist

Use this checklist to set up and test the Stripe integration step by step.

---

## 📋 Pre-Setup (Do These First)

### Stripe Account Setup
- [ ] Create Stripe account at https://stripe.com
- [ ] Complete business verification
- [ ] Enable test mode (toggle in top-right of dashboard)

### Create Products in Stripe Dashboard
Go to: **Products** → **Add Product**

- [ ] **Product 1: Starter**
  - Name: `Tik-Tax Starter`
  - Description: `200 receipts per month`
  - Price (Monthly): `₪49/month` (recurring)
  - Price (Yearly): `₪470/year` (recurring)
  - Copy both Price IDs (starts with `price_...`)

- [ ] **Product 2: Pro**
  - Name: `Tik-Tax Pro`  
  - Description: `1,000 receipts per month`
  - Price (Monthly): `₪99/month` (recurring)
  - Price (Yearly): `₪950/year` (recurring)
  - Copy both Price IDs

- [ ] **Product 3: Business**
  - Name: `Tik-Tax Business`
  - Description: `Unlimited receipts`
  - Price (Monthly): `₪199/month` (recurring)
  - Price (Yearly): `₪1,910/year` (recurring)
  - Copy both Price IDs

### Get API Keys
Go to: **Developers** → **API Keys**

- [ ] Copy **Publishable key** (starts with `pk_test_...`)
- [ ] Reveal and copy **Secret key** (starts with `sk_test_...`)
- [ ] ⚠️ NEVER commit these keys to git!

### Install Stripe CLI
- [ ] Windows: `scoop install stripe`
- [ ] Mac: `brew install stripe/stripe-cli/stripe`
- [ ] Linux: See https://stripe.com/docs/stripe-cli#install

---

## 🔧 Backend Configuration

### 1. Environment Variables
- [ ] Create/Edit `backend/.env`
- [ ] Add Stripe secret key
- [ ] Add Stripe publishable key
- [ ] Add all 6 price IDs (3 plans × 2 billing periods)
- [ ] Set FRONTEND_URL to `http://localhost:5173`

**Template:**
```env
STRIPE_SECRET_KEY=sk_test_YOUR_KEY_HERE
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY_HERE
STRIPE_WEBHOOK_SECRET=whsec_WILL_GET_THIS_NEXT
STRIPE_STARTER_MONTHLY_PRICE_ID=price_...
STRIPE_STARTER_YEARLY_PRICE_ID=price_...
STRIPE_PRO_MONTHLY_PRICE_ID=price_...
STRIPE_PRO_YEARLY_PRICE_ID=price_...
STRIPE_BUSINESS_MONTHLY_PRICE_ID=price_...
STRIPE_BUSINESS_YEARLY_PRICE_ID=price_...
FRONTEND_URL=http://localhost:5173
```

### 2. Start Webhook Listener
- [ ] Open terminal
- [ ] Run: `stripe login`
- [ ] Run: `stripe listen --forward-to localhost:8000/api/v1/stripe/webhook`
- [ ] Copy webhook signing secret (starts with `whsec_...`)
- [ ] Add to `backend/.env` as `STRIPE_WEBHOOK_SECRET`
- [ ] **Keep this terminal running!**

### 3. Database Migration
- [ ] Open terminal in `backend/` folder
- [ ] Run: `alembic upgrade head`
- [ ] Verify no errors
- [ ] Check database has new columns: `stripe_customer_id`, `stripe_subscription_id`, `subscription_status`

### 4. Install Dependencies
- [ ] Run: `pip install stripe==7.5.0`
- [ ] Verify installation: `pip show stripe`

---

## 🎨 Frontend Configuration

### 1. Environment Variables
- [ ] Create/Edit `frontend/.env`
- [ ] Add Stripe publishable key
- [ ] Add all 6 price IDs (same as backend)

**Template:**
```env
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY_HERE
VITE_STRIPE_STARTER_MONTHLY_PRICE_ID=price_...
VITE_STRIPE_STARTER_YEARLY_PRICE_ID=price_...
VITE_STRIPE_PRO_MONTHLY_PRICE_ID=price_...
VITE_STRIPE_PRO_YEARLY_PRICE_ID=price_...
VITE_STRIPE_BUSINESS_MONTHLY_PRICE_ID=price_...
VITE_STRIPE_BUSINESS_YEARLY_PRICE_ID=price_...
```

### 2. Verify Files Exist
- [ ] `src/services/subscription.service.ts` exists
- [ ] `src/pages/CheckoutSuccessPage.tsx` exists
- [ ] `src/pages/CheckoutCancelPage.tsx` exists
- [ ] `src/pages/SubscriptionPage.tsx` updated
- [ ] `src/App.tsx` has new routes

---

## 🚀 Start All Services

### Terminal 1: Backend
```bash
cd backend
uvicorn app.main:app --reload
```
- [ ] Backend running on http://localhost:8000
- [ ] No startup errors
- [ ] Check logs for "Application startup complete"

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```
- [ ] Frontend running on http://localhost:5173
- [ ] No compile errors
- [ ] Browser opens automatically

### Terminal 3: Stripe Webhooks (Already Running)
```bash
stripe listen --forward-to localhost:8000/api/v1/stripe/webhook
```
- [ ] Shows "Ready! Your webhook signing secret is whsec_..."
- [ ] Shows "Webhooks are being forwarded to..."

---

## 🧪 Testing Checklist

### Test 1: Basic Checkout Flow
- [ ] Open http://localhost:5173
- [ ] See 4 subscription plans (Free, Starter, Pro, Business)
- [ ] Toggle between Monthly/Yearly billing
- [ ] Click "שדרג עכשיו" on **Starter** plan
- [ ] Loading spinner appears on button
- [ ] Redirected to Stripe Checkout page
- [ ] See "Tik-Tax Starter" product
- [ ] See correct price (₪49 or ₪470)

### Test 2: Complete Payment
- [ ] On Stripe Checkout, use test card: `4242 4242 4242 4242`
- [ ] Expiry: Any future date (e.g., 12/25)
- [ ] CVC: Any 3 digits (e.g., 123)
- [ ] ZIP: Any 5 digits (e.g., 12345)
- [ ] Click "Subscribe"
- [ ] Redirected to `/checkout/success`
- [ ] See green checkmark animation
- [ ] See "התשלום בוצע בהצלחה!"
- [ ] See subscription details (plan, status, limits)
- [ ] Countdown from 5 seconds
- [ ] Auto-redirect to dashboard OR click "חזור לדשבורד"

### Test 3: Verify Backend
- [ ] Check **Terminal 3** (Stripe webhooks)
- [ ] See: `checkout.session.completed` event received
- [ ] Check **Terminal 1** (Backend logs)
- [ ] See: "Subscription activated for user..."
- [ ] See: "Checkout completed: cs_..."
- [ ] No errors in logs

### Test 4: Verify Database
- [ ] Open database client (e.g., DBeaver, pgAdmin)
- [ ] Query: `SELECT * FROM users WHERE email = 'your@email.com'`
- [ ] Verify:
  - [ ] `stripe_customer_id` is populated (starts with `cus_...`)
  - [ ] `stripe_subscription_id` is populated (starts with `sub_...`)
  - [ ] `subscription_plan` = `starter`
  - [ ] `subscription_status` = `active`
  - [ ] `subscription_start_date` is set
  - [ ] `subscription_end_date` is set (30 or 365 days from now)
  - [ ] `receipt_limit` = 200

### Test 5: Cancel Checkout
- [ ] Click upgrade again
- [ ] On Stripe Checkout, click browser "Back" button
- [ ] Redirected to `/checkout/cancel`
- [ ] See "התשלום בוטל"
- [ ] See "לא חויבת"
- [ ] Click "חזור למנויים" → Back to subscription page
- [ ] Click "צור קשר עם תמיכה" → Opens email client

### Test 6: Test Other Plans
Repeat Test 2 & 3 for:
- [ ] **Pro** plan (₪99/month or ₪950/year)
- [ ] **Business** plan (₪199/month or ₪1,910/year)
- [ ] Verify correct `receipt_limit` in database:
  - Pro: 1000
  - Business: -1 (unlimited)

### Test 7: Yearly Billing
- [ ] Toggle to "חיוב שנתי"
- [ ] See prices change
- [ ] See savings badge
- [ ] Click upgrade
- [ ] Verify correct yearly price on Stripe Checkout
- [ ] Complete payment
- [ ] Verify `subscription_end_date` is ~365 days from now

### Test 8: Subscription Cancellation
- [ ] Make API call (or create UI):
  ```bash
  curl -X POST http://localhost:8000/api/v1/subscriptions/cancel \
    -H "Authorization: Bearer YOUR_TOKEN"
  ```
- [ ] Verify response: `"status": "canceling"`
- [ ] Check database: `subscription_status` = `canceling`
- [ ] Verify access continues until `subscription_end_date`

### Test 9: Billing History
- [ ] Make API call:
  ```bash
  curl http://localhost:8000/api/v1/subscriptions/billing-history \
    -H "Authorization: Bearer YOUR_TOKEN"
  ```
- [ ] Verify returns array of invoices
- [ ] Check: date, amount, status, invoice_pdf

### Test 10: Billing Portal
- [ ] Make API call:
  ```bash
  curl http://localhost:8000/api/v1/subscriptions/billing-portal \
    -H "Authorization: Bearer YOUR_TOKEN"
  ```
- [ ] Verify returns `portal_url`
- [ ] Open URL in browser
- [ ] See Stripe billing portal
- [ ] Can update payment method
- [ ] Can view billing history
- [ ] Can download invoices

---

## 🐛 Troubleshooting

### Issue: Webhook not received
- [ ] Check Stripe CLI is running (Terminal 3)
- [ ] Restart: `stripe listen --forward-to localhost:8000/api/v1/stripe/webhook`
- [ ] Copy new webhook secret to `.env`
- [ ] Restart backend

### Issue: Invalid price ID
- [ ] Go to Stripe Dashboard → Products
- [ ] Click on product → Pricing
- [ ] Copy exact Price ID (including `price_` prefix)
- [ ] Update `.env` file
- [ ] Restart backend and frontend

### Issue: Checkout redirect fails
- [ ] Check `FRONTEND_URL` in backend `.env` = `http://localhost:5173`
- [ ] Check CORS settings in backend allow frontend origin
- [ ] Check browser console for errors

### Issue: Success page doesn't show subscription
- [ ] Check browser console for API errors
- [ ] Verify user is authenticated (has JWT token)
- [ ] Check backend logs for `/subscriptions/status` call
- [ ] Verify database has subscription data

### Issue: Payment succeeds but subscription not activated
- [ ] Check Terminal 3 for webhook event
- [ ] Check Terminal 1 for processing logs
- [ ] Check database for `stripe_subscription_id`
- [ ] Manually trigger webhook: `stripe trigger checkout.session.completed`

---

## ✅ Final Verification

After completing all tests:

- [ ] All 10 tests passed
- [ ] No errors in any terminal
- [ ] Database updated correctly
- [ ] Webhooks received and processed
- [ ] Success page works perfectly
- [ ] Cancel page works perfectly
- [ ] Can upgrade to all 3 plans
- [ ] Monthly and yearly billing both work
- [ ] Subscription status tracked correctly
- [ ] Email notifications sent (check email service logs)

---

## 📊 Production Checklist

Before deploying to production:

- [ ] **Switch to Live Mode in Stripe**
- [ ] Get live API keys (`pk_live_...`, `sk_live_...`)
- [ ] Recreate products in live mode
- [ ] Update all environment variables with live keys
- [ ] Set up production webhook endpoint in Stripe Dashboard
- [ ] Update `FRONTEND_URL` to production domain
- [ ] Enable HTTPS (required by Stripe)
- [ ] Test with real credit card (your own)
- [ ] Cancel test subscription immediately
- [ ] Monitor Stripe Dashboard for first 24 hours
- [ ] Set up error alerts (Sentry, etc.)
- [ ] Review Stripe security best practices

---

## 📞 Support

**Issues with Setup:**
- Read `STRIPE_INTEGRATION_COMPLETE.md`
- Check troubleshooting section above
- Review Stripe logs in Dashboard

**Stripe-Specific Help:**
- Stripe Docs: https://stripe.com/docs
- Stripe Testing Guide: https://stripe.com/docs/testing
- Stripe Support: https://support.stripe.com

**Code Issues:**
- Check implementation files
- Review error logs carefully
- Verify environment variables match exactly

---

## 🎉 Success!

If all checkboxes are ✅, your Stripe integration is working perfectly!

**Next Steps:**
1. Test with team members
2. Prepare for production launch
3. Monitor first few transactions closely
4. Collect user feedback

**Congratulations! 🚀**
