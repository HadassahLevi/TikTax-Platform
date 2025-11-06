# Subscription Page - Quick Reference

## Overview
Comprehensive subscription and pricing page for Tik-Tax with plan comparison, billing toggle, and upgrade flow.

## File Location
`/src/pages/SubscriptionPage.tsx`

## Route
`/subscription` or `/pricing`

## Features

### ✅ Subscription Tiers
- **Free**: ₪0/month (50 receipts)
- **Starter**: ₪49/month (200 receipts)
- **Pro**: ₪99/month (1,000 receipts) - RECOMMENDED
- **Business**: ₪199/month (unlimited receipts)

### ✅ Billing Toggle
- Monthly/yearly billing switch
- 20% discount badge on yearly
- Savings calculation displayed

### ✅ Plan Cards
- Animated entrance
- Icon-based branding
- Feature list with checkmarks
- Receipts limit highlighted
- CTA button (upgrade/current plan)
- "Popular" badge on Pro plan

### ✅ Feature Comparison Table
- Full responsive table
- Check/X icons for features
- Pro plan highlighted column
- Mobile-friendly overflow scroll

### ✅ FAQ Section
- Accordion-style expansion
- Smooth animations
- 6 common questions
- Keyboard accessible

### ✅ Trust Badges
- Security badge (bank-level encryption)
- ISO 27001 certification
- Customer count (1000+ businesses)

## Component Structure

```typescript
SubscriptionPage (main)
├── Header
│   ├── H1: "בחר את התוכנית המתאימה לך"
│   ├── Subtitle
│   └── BillingToggle (monthly/yearly)
├── Plans Grid (4 cards)
│   └── PlanCard × 4
│       ├── Icon
│       ├── Plan name
│       ├── Price
│       ├── Receipts limit
│       ├── Features list
│       └── CTA button
├── FeatureComparison (table)
├── FAQSection (accordion)
└── TrustBadges
```

## Props & State

### State
```typescript
billingPeriod: 'monthly' | 'yearly'  // Toggle state
```

### From useAuth Hook
```typescript
user.subscription_plan: 'free' | 'starter' | 'pro' | 'business'
```

## Animations

### Framer Motion Effects
- **Header**: Fade in from top
- **Billing Toggle**: Scale in with delay
- **Plan Cards**: Staggered fade-up (0.1s delay each)
- **Sections**: Scroll-triggered reveal
- **FAQ**: Height expand/collapse
- **Hover**: Card lift + shadow increase

## Pricing Logic

### Monthly
```typescript
price = plan.price
total = price (billed monthly)
```

### Yearly
```typescript
price = plan.yearlyPrice / 12  // Monthly equivalent
total = plan.yearlyPrice       // Billed annually
savings = (plan.price * 12) - plan.yearlyPrice
```

### Discount
```typescript
yearlyDiscount = 20%
yearlyPrice = monthlyPrice * 12 * 0.8
```

## Responsive Breakpoints

### Mobile (< 640px)
- 1 column grid
- Full-width cards
- Stacked comparison table
- Larger touch targets

### Tablet (640px - 1024px)
- 2 column grid
- Increased spacing

### Desktop (> 1024px)
- 4 column grid
- Hover effects enabled
- Max width: 1200px

## Accessibility

### ARIA Labels
- `aria-pressed` on billing toggle
- `aria-expanded` on FAQ buttons
- `aria-controls` links FAQs to answers
- `aria-label` on check/X icons

### Keyboard Navigation
- Tab through all interactive elements
- Enter/Space to toggle FAQ
- Focus visible on all buttons

### Screen Reader
- Semantic HTML (header, section, table)
- Descriptive button text
- Alt text on icons via aria-label

## Integration Points

### TODO: Stripe Checkout
```typescript
handleUpgrade(planId) {
  // TODO: Implement in Prompt 49
  // Navigate to Stripe checkout
  // Pass: planId, billingPeriod
}
```

### User Subscription
```typescript
const currentPlan = user?.subscription_plan || 'free';
// Used to:
// - Highlight current plan card
// - Disable upgrade button for current plan
// - Show "התוכנית הנוכחית שלך" text
```

## Design System Compliance

### Colors
- Primary: #2563EB (CTA buttons)
- Success: #10B981 (checkmarks, savings badge)
- Gray scale: Professional neutrals
- Status colors: Per plan (gray/blue/primary/purple)

### Typography
- H1: 32-40px bold
- H2: 24px bold (sections)
- H3: 18px bold (plan names)
- Body: 16px regular
- Pricing: 40-48px bold

### Spacing
- Container: max-w-7xl, px-4/6/8
- Cards: 24px padding
- Sections: 48-64px margin-bottom
- Grid gap: 24px

### Shadows
- Cards: Level 1 (resting)
- Hover: Level 2
- Toggle: Level 2

## Hebrew UI Text

### Headers
- "בחר את התוכנית המתאימה לך" (Choose your plan)
- "שדרג את החוויה שלך" (Upgrade your experience)
- "השוואת תכונות" (Feature comparison)
- "שאלות נפוצות" (FAQ)

### Buttons
- "חיוב חודשי" (Monthly billing)
- "חיוב שנתי" (Yearly billing)
- "שדרג עכשיו" (Upgrade now)
- "התחל בחינם" (Start free)
- "התוכנית הנוכחית שלך" (Your current plan)

### Other
- "חסוך 20%" (Save 20%)
- "הכי פופולרי" (Most popular)
- "קבלות בחודש" (Receipts per month)
- "ללא הגבלה" (Unlimited)

## Testing Checklist

### Visual
- [ ] All 4 plans display correctly
- [ ] Recommended badge shows on Pro
- [ ] Monthly/yearly toggle works
- [ ] Pricing updates on toggle
- [ ] Savings calculation correct
- [ ] Current plan highlighted
- [ ] Mobile responsive (320px+)

### Functionality
- [ ] Toggle switches billing period
- [ ] Plan cards are clickable
- [ ] handleUpgrade logs plan ID
- [ ] FAQ accordion expands/collapses
- [ ] Animations smooth (no jank)
- [ ] Table scrolls on mobile

### Accessibility
- [ ] Keyboard navigation works
- [ ] Screen reader announces all content
- [ ] Focus indicators visible
- [ ] Color contrast meets WCAG AA
- [ ] Touch targets 44px minimum

### Performance
- [ ] No layout shift on load
- [ ] Animations use GPU (transform/opacity)
- [ ] Images optimized (icons are SVG)
- [ ] No console errors

## Known Issues
None currently.

## Future Enhancements
1. Add custom plan builder
2. Annual/monthly chart comparison
3. Customer testimonials
4. Money-back guarantee badge
5. Live chat for plan questions
6. Plan feature tooltips
7. Currency selector (ILS/USD/EUR)
8. Volume discount calculator

## Related Files
- `/hooks/useAuth.ts` - User subscription data
- `/components/ui/Card.tsx` - Card component
- `/components/ui/Button.tsx` - Button component
- `/utils/formatters.ts` - cn() utility
- (Future) `/pages/CheckoutPage.tsx` - Stripe integration

## Example Usage

```tsx
import { SubscriptionPage } from '@/pages';

// In App.tsx routing
<Route path="/subscription" element={<SubscriptionPage />} />
<Route path="/pricing" element={<SubscriptionPage />} />
```

## Notes
- Pricing is in Israeli New Shekel (₪)
- All amounts include VAT (17%)
- Yearly discount is fixed at 20%
- Free plan has no time limit
- Receipts counter resets monthly
- Unused receipts don't roll over
- Upgrade/downgrade takes effect immediately
- Refunds are pro-rated for cancellations

---

**Last Updated**: 2025-11-06  
**Component Status**: ✅ Complete - Ready for integration  
**Stripe Integration**: 🔄 Pending (Prompt 49)
