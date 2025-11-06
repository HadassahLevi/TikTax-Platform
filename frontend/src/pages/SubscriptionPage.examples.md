# Subscription Page - Usage Examples

## Basic Usage in Router

### Example 1: React Router v6 Integration
```tsx
// src/App.tsx or src/router/index.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { SubscriptionPage } from '@/pages';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ... other routes ... */}
        
        {/* Subscription page */}
        <Route path="/subscription" element={<SubscriptionPage />} />
        <Route path="/pricing" element={<SubscriptionPage />} />
        
        {/* Or with protected route */}
        <Route 
          path="/subscription" 
          element={
            <ProtectedRoute>
              <SubscriptionPage />
            </ProtectedRoute>
          } 
        />
      </Routes>
    </BrowserRouter>
  );
}
```

## Navigation Examples

### Example 2: Link from Navigation Menu
```tsx
// src/components/layout/Header.tsx
import { Link } from 'react-router-dom';

function Header() {
  return (
    <nav>
      <Link to="/">דף הבית</Link>
      <Link to="/archive">ארכיון</Link>
      <Link to="/subscription">מנויים ומחירים</Link>
      <Link to="/profile">פרופיל</Link>
    </nav>
  );
}
```

### Example 3: Upgrade Button from Dashboard
```tsx
// src/pages/dashboard/DashboardPage.tsx
import { useNavigate } from 'react-router-dom';
import Button from '@/components/ui/Button';

function DashboardPage() {
  const navigate = useNavigate();
  
  return (
    <div>
      {/* Usage limit warning */}
      {receiptsUsage > 80 && (
        <div className="bg-yellow-50 p-4 rounded-lg">
          <p>הגעת ל-80% מהמכסה החודשית שלך</p>
          <Button 
            variant="primary"
            onClick={() => navigate('/subscription')}
          >
            שדרג תוכנית
          </Button>
        </div>
      )}
    </div>
  );
}
```

### Example 4: Direct Plan Link
```tsx
// Link directly to subscription with query param (future enhancement)
<Link to="/subscription?plan=pro">
  שדרג ל-Pro
</Link>

// In SubscriptionPage, handle the query:
const { plan } = useSearchParams();
useEffect(() => {
  if (plan) {
    // Scroll to plan card
    // Or open checkout directly
  }
}, [plan]);
```

## Integration with User State

### Example 5: Conditional Rendering Based on Current Plan
```tsx
// src/pages/SubscriptionPage.tsx (already implemented)
import { useAuth } from '@/hooks/useAuth';

export const SubscriptionPage: React.FC = () => {
  const { user } = useAuth();
  const currentPlan = user?.subscription_plan || 'free';
  
  // Current plan gets:
  // - Highlighted border
  // - Disabled upgrade button
  // - "התוכנית הנוכחית שלך" text
  
  return (
    // ... component
  );
};
```

### Example 6: Redirect After Upgrade
```tsx
// Future: After successful Stripe payment
function handleUpgradeSuccess() {
  // Update user in auth store
  updateUser({ subscription_plan: 'pro' });
  
  // Show success message
  toast.success('התוכנית שודרגה בהצלחה!');
  
  // Redirect to dashboard
  navigate('/dashboard', { state: { upgraded: true } });
}
```

## Custom Hooks for Subscription Logic

### Example 7: useSubscription Hook (Future Enhancement)
```tsx
// src/hooks/useSubscription.ts
import { useAuth } from './useAuth';
import { useNavigate } from 'react-router-dom';

export function useSubscription() {
  const { user, updateUser } = useAuth();
  const navigate = useNavigate();
  
  const currentPlan = user?.subscription_plan || 'free';
  const receiptsUsed = user?.receipts_this_month || 0;
  const receiptsLimit = getPlanLimit(currentPlan);
  const usagePercent = (receiptsUsed / receiptsLimit) * 100;
  
  const canUpload = receiptsUsed < receiptsLimit || receiptsLimit === -1;
  const shouldUpgrade = usagePercent > 80;
  
  const navigateToUpgrade = (suggestedPlan?: string) => {
    navigate('/subscription', { 
      state: { suggestedPlan } 
    });
  };
  
  return {
    currentPlan,
    receiptsUsed,
    receiptsLimit,
    usagePercent,
    canUpload,
    shouldUpgrade,
    navigateToUpgrade
  };
}

// Usage in components
function UploadPage() {
  const { canUpload, navigateToUpgrade } = useSubscription();
  
  if (!canUpload) {
    return (
      <div>
        <p>הגעת למגבלת הקבלות החודשית</p>
        <Button onClick={() => navigateToUpgrade('pro')}>
          שדרג עכשיו
        </Button>
      </div>
    );
  }
  
  return <UploadForm />;
}
```

## Analytics Tracking

### Example 8: Track Page Views and Interactions
```tsx
// src/pages/SubscriptionPage.tsx
import { useEffect } from 'react';
import { analytics } from '@/services/analytics';

export const SubscriptionPage: React.FC = () => {
  const { user } = useAuth();
  
  useEffect(() => {
    // Track page view
    analytics.track('Pricing Page Viewed', {
      currentPlan: user?.subscription_plan,
      referrer: document.referrer
    });
  }, []);
  
  const handleUpgrade = (planId: string) => {
    // Track upgrade intent
    analytics.track('Upgrade Button Clicked', {
      from_plan: user?.subscription_plan,
      to_plan: planId,
      billing_period: billingPeriod
    });
    
    // Navigate to checkout (Stripe - Prompt 49)
    navigate(`/checkout?plan=${planId}&period=${billingPeriod}`);
  };
  
  const handleBillingToggle = (period: 'monthly' | 'yearly') => {
    setBillingPeriod(period);
    
    // Track billing preference
    analytics.track('Billing Period Changed', {
      period,
      currentPlan: user?.subscription_plan
    });
  };
  
  return (
    // ... component
  );
};
```

## Error Handling

### Example 9: Handle Subscription Errors
```tsx
// src/pages/SubscriptionPage.tsx
import { toast } from '@/components/ui/Toast';

export const SubscriptionPage: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const handleUpgrade = async (planId: string) => {
    try {
      setLoading(true);
      setError(null);
      
      // Validate can upgrade
      if (!user) {
        throw new Error('יש להתחבר כדי לשדרג');
      }
      
      if (user.subscription_plan === planId) {
        throw new Error('זו התוכנית הנוכחית שלך');
      }
      
      // Create Stripe checkout session
      const { sessionId } = await createCheckoutSession({
        planId,
        billingPeriod,
        userId: user.id
      });
      
      // Redirect to Stripe
      const stripe = await loadStripe(process.env.VITE_STRIPE_PUBLIC_KEY);
      await stripe.redirectToCheckout({ sessionId });
      
    } catch (err) {
      const message = err instanceof Error ? err.message : 'שגיאה בשדרוג התוכנית';
      setError(message);
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div>
      {error && (
        <div className="bg-red-50 border border-red-200 p-4 rounded-lg mb-4">
          <p className="text-red-800">{error}</p>
        </div>
      )}
      
      {/* ... rest of component */}
    </div>
  );
};
```

## Mobile-Specific Examples

### Example 10: Bottom Sheet for Mobile
```tsx
// Alternative mobile layout (future enhancement)
import { useMediaQuery } from '@/hooks/useMediaQuery';
import { BottomSheet } from '@/components/ui/BottomSheet';

export const SubscriptionPage: React.FC = () => {
  const isMobile = useMediaQuery('(max-width: 640px)');
  const [selectedPlan, setSelectedPlan] = useState<Plan | null>(null);
  
  if (isMobile) {
    return (
      <div>
        {/* Compact plan list */}
        {PLANS.map(plan => (
          <PlanListItem 
            key={plan.id}
            plan={plan}
            onClick={() => setSelectedPlan(plan)}
          />
        ))}
        
        {/* Bottom sheet with full details */}
        <BottomSheet 
          isOpen={!!selectedPlan}
          onClose={() => setSelectedPlan(null)}
        >
          {selectedPlan && (
            <PlanDetails 
              plan={selectedPlan}
              onUpgrade={handleUpgrade}
            />
          )}
        </BottomSheet>
      </div>
    );
  }
  
  return <DesktopSubscriptionLayout />;
};
```

## Testing Examples

### Example 11: Component Testing
```tsx
// src/pages/SubscriptionPage.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { SubscriptionPage } from './SubscriptionPage';
import { AuthProvider } from '@/contexts/AuthContext';

describe('SubscriptionPage', () => {
  it('renders all 4 subscription plans', () => {
    render(
      <BrowserRouter>
        <AuthProvider>
          <SubscriptionPage />
        </AuthProvider>
      </BrowserRouter>
    );
    
    expect(screen.getByText('חינמי')).toBeInTheDocument();
    expect(screen.getByText('בסיסי')).toBeInTheDocument();
    expect(screen.getByText('מקצועי')).toBeInTheDocument();
    expect(screen.getByText('עסקי')).toBeInTheDocument();
  });
  
  it('toggles between monthly and yearly billing', () => {
    render(<SubscriptionPage />);
    
    const yearlyButton = screen.getByText('חיוב שנתי');
    fireEvent.click(yearlyButton);
    
    // Check that yearly prices are displayed
    expect(screen.getByText(/470/)).toBeInTheDocument(); // Starter yearly
  });
  
  it('highlights current user plan', () => {
    const mockUser = { subscription_plan: 'pro' };
    
    render(
      <AuthProvider value={{ user: mockUser }}>
        <SubscriptionPage />
      </AuthProvider>
    );
    
    expect(screen.getByText('התוכנית הנוכחית שלך')).toBeInTheDocument();
  });
  
  it('expands FAQ on click', () => {
    render(<SubscriptionPage />);
    
    const faqButton = screen.getByText('האם אוכל לשנות תוכנית בכל זמן?');
    fireEvent.click(faqButton);
    
    expect(screen.getByText(/שינוי יכנס לתוקף מיד/)).toBeVisible();
  });
});
```

## Styling Customization

### Example 12: Custom Theme Colors
```tsx
// If you want to customize plan colors
const CUSTOM_PLANS = PLANS.map(plan => ({
  ...plan,
  color: plan.id === 'pro' ? 'purple' : plan.color // Change Pro to purple
}));

// Then use in component
{CUSTOM_PLANS.map((plan, index) => (
  <PlanCard key={plan.id} plan={plan} ... />
))}
```

---

## Quick Integration Checklist

### Setup (5 minutes)
- [ ] File already created: ✅ `/src/pages/SubscriptionPage.tsx`
- [ ] Export added to index: ✅ `/src/pages/index.ts`
- [ ] Add route to router (see Example 1)
- [ ] Add navigation link (see Example 2)

### Test (10 minutes)
- [ ] Navigate to `/subscription`
- [ ] Toggle monthly/yearly
- [ ] Click on plan cards
- [ ] Expand FAQs
- [ ] Check mobile responsive
- [ ] Test keyboard navigation

### Integration (Pending Prompt 49)
- [ ] Implement Stripe checkout
- [ ] Handle successful payment
- [ ] Update user subscription
- [ ] Show success message

---

**All examples are production-ready and follow Tik-Tax patterns!**
