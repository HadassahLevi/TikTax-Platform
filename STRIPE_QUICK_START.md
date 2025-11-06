# Stripe Integration Quick Reference

## 🚀 Quick Start (5 Minutes)

### 1. Get Stripe Keys
```bash
# Login to Stripe Dashboard
# Go to: Developers → API Keys
# Copy: pk_test_... and sk_test_...
```

### 2. Start Webhook Listener
```bash
stripe login
stripe listen --forward-to localhost:8000/api/v1/stripe/webhook
# Copy webhook secret: whsec_...
```

### 3. Configure Backend .env
```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Get these from Stripe Dashboard → Products
STRIPE_STARTER_MONTHLY_PRICE_ID=price_...
STRIPE_STARTER_YEARLY_PRICE_ID=price_...
STRIPE_PRO_MONTHLY_PRICE_ID=price_...
STRIPE_PRO_YEARLY_PRICE_ID=price_...
STRIPE_BUSINESS_MONTHLY_PRICE_ID=price_...
STRIPE_BUSINESS_YEARLY_PRICE_ID=price_...

FRONTEND_URL=http://localhost:5173
```

### 4. Configure Frontend .env
```env
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...
VITE_STRIPE_STARTER_MONTHLY_PRICE_ID=price_...
VITE_STRIPE_STARTER_YEARLY_PRICE_ID=price_...
VITE_STRIPE_PRO_MONTHLY_PRICE_ID=price_...
VITE_STRIPE_PRO_YEARLY_PRICE_ID=price_...
VITE_STRIPE_BUSINESS_MONTHLY_PRICE_ID=price_...
VITE_STRIPE_BUSINESS_YEARLY_PRICE_ID=price_...
```

### 5. Run Migration
```bash
cd backend
alembic upgrade head
```

### 6. Start Services
```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Stripe Webhooks
stripe listen --forward-to localhost:8000/api/v1/stripe/webhook
```

### 7. Test
1. Visit http://localhost:5173
2. Click "שדרג עכשיו"
3. Use test card: `4242 4242 4242 4242`
4. Complete checkout
5. Verify redirect to success page

---

## 📁 Files Modified/Created

### Backend:
- ✅ `app/services/stripe_service.py` (NEW)
- ✅ `app/api/v1/endpoints/stripe_webhooks.py` (NEW)
- ✅ `app/api/v1/endpoints/subscriptions.py` (UPDATED)
- ✅ `app/models/user.py` (UPDATED)
- ✅ `app/core/config.py` (UPDATED)
- ✅ `app/api/v1/router.py` (UPDATED)
- ✅ `alembic_migration_stripe.py` (NEW)

### Frontend:
- ✅ `src/services/subscription.service.ts` (NEW)
- ✅ `src/services/index.ts` (UPDATED)
- ✅ `src/pages/CheckoutSuccessPage.tsx` (NEW)
- ✅ `src/pages/CheckoutCancelPage.tsx` (NEW)
- ✅ `src/pages/SubscriptionPage.tsx` (UPDATED)
- ✅ `src/pages/index.ts` (UPDATED)
- ✅ `src/App.tsx` (UPDATED)

---

## 🔑 Key API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/subscriptions/upgrade` | Create checkout |
| GET | `/api/v1/subscriptions/status` | Get subscription |
| GET | `/api/v1/subscriptions/billing-history` | Get invoices |
| POST | `/api/v1/subscriptions/cancel` | Cancel subscription |
| GET | `/api/v1/subscriptions/billing-portal` | Get portal URL |
| POST | `/api/v1/stripe/webhook` | Receive webhooks |

---

## 🧪 Test Cards

| Card | Result |
|------|--------|
| `4242 4242 4242 4242` | ✅ Success |
| `4000 0000 0000 0002` | ❌ Decline |
| `4000 0000 0000 9995` | ❌ Insufficient funds |

---

## 📊 Webhook Events Handled

- ✅ `checkout.session.completed` → Activate subscription
- ✅ `customer.subscription.deleted` → Cancel subscription
- ✅ `invoice.payment_succeeded` → Renew subscription
- ✅ `invoice.payment_failed` → Mark past_due

---

## 🔐 Security Checklist

- ✅ Webhook signature verification
- ✅ Idempotent event processing
- ✅ Secret keys not in git
- ✅ Input validation
- ✅ Price ID validation

---

## 🐛 Common Issues

**Webhook not received:**
```bash
# Restart Stripe CLI
stripe listen --forward-to localhost:8000/api/v1/stripe/webhook
```

**Invalid price ID:**
```bash
# Verify in Stripe Dashboard → Products → Prices
# Copy price_... ID exactly
```

**Checkout fails:**
```bash
# Check FRONTEND_URL in backend .env
# Verify CORS settings
```

---

## 📞 Support

- Stripe Docs: https://stripe.com/docs
- Stripe Support: https://support.stripe.com
- Test Cards: https://stripe.com/docs/testing

---

**Ready to go! 🎉**
