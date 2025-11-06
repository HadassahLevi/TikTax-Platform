import React, { useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import { motion, AnimatePresence } from 'framer-motion';
import { subscriptionService } from '@/services';
import { 
  Check, 
  X, 
  Zap, 
  Building2, 
  Sparkles,
  TrendingUp,
  Shield,
  ChevronDown,
  Star,
  Users,
  Lock
} from 'lucide-react';
import { cn } from '@/utils/formatters';

/**
 * Plan Interface
 * Defines structure for subscription plans
 */
interface Plan {
  id: string;
  name: string;
  nameHe: string;
  price: number;
  yearlyPrice: number;
  receiptsLimit: number;
  features: string[];
  recommended?: boolean;
  color: string;
  icon: React.ReactNode;
}

/**
 * Subscription Plans Configuration
 * All pricing and features for Tik-Tax plans
 */
const PLANS: Plan[] = [
  {
    id: 'free',
    name: 'Free',
    nameHe: 'חינמי',
    price: 0,
    yearlyPrice: 0,
    receiptsLimit: 50,
    features: [
      '50 קבלות בחודש',
      'OCR אוטומטי',
      'אחסון בענן',
      'ייצוא לאקסל',
      'תמיכה במייל'
    ],
    color: 'gray',
    icon: <Sparkles size={24} />
  },
  {
    id: 'starter',
    name: 'Starter',
    nameHe: 'בסיסי',
    price: 49,
    yearlyPrice: 470,
    receiptsLimit: 200,
    features: [
      '200 קבלות בחודש',
      'כל התכונות של Free',
      'חיפוש מתקדם',
      'קטגוריות מותאמות',
      'דוחות חודשיים',
      'תמיכה מועדפת'
    ],
    color: 'blue',
    icon: <TrendingUp size={24} />
  },
  {
    id: 'pro',
    name: 'Pro',
    nameHe: 'מקצועי',
    price: 99,
    yearlyPrice: 950,
    receiptsLimit: 1000,
    recommended: true,
    features: [
      '1,000 קבלות בחודש',
      'כל התכונות של Starter',
      'AI מתקדם לזיהוי',
      'אינטגרציה עם רואה חשבון',
      'ייצוא אוטומטי',
      'דוחות מתקדמים',
      'תמיכה טלפונית'
    ],
    color: 'primary',
    icon: <Zap size={24} />
  },
  {
    id: 'business',
    name: 'Business',
    nameHe: 'עסקי',
    price: 199,
    yearlyPrice: 1910,
    receiptsLimit: -1, // Unlimited
    features: [
      'קבלות ללא הגבלה',
      'כל התכונות של Pro',
      'ניהול צוות',
      'API מלא',
      'חתימה דיגיטלית',
      'אינטגרציה עם מערכות חשבונאות',
      'מנהל חשבון ייעודי',
      'SLA מובטח'
    ],
    color: 'purple',
    icon: <Building2 size={24} />
  }
];

/**
 * Subscription Page Component
 * 
 * Displays all subscription plans with comparison, billing toggle, and upgrade flow
 * Follows Tik-Tax design system with professional FinTech aesthetic
 * 
 * Features:
 * - 4 subscription tiers (Free, Starter, Pro, Business)
 * - Monthly/yearly billing toggle with 20% discount
 * - Animated plan cards with hover effects
 * - Feature comparison table
 * - FAQ accordion section
 * - Trust badges
 * - Full RTL support
 * - Mobile-responsive
 * 
 * @component
 * @example
 * ```tsx
 * <SubscriptionPage />
 * ```
 */
export const SubscriptionPage: React.FC = () => {
  const { user } = useAuth();
  const [billingPeriod, setBillingPeriod] = useState<'monthly' | 'yearly'>('monthly');
  const [loadingPlan, setLoadingPlan] = useState<string | null>(null);
  
  const currentPlan = user?.subscription_plan || 'free';
  
  /**
   * Map plan ID and billing period to Stripe Price ID
   * These must match the environment variables in .env
   */
  const getPriceId = (planId: string, billing: 'monthly' | 'yearly'): string => {
    // Note: These are placeholder price IDs
    // Replace with actual Stripe Price IDs from your dashboard
    const priceMap: Record<string, { monthly: string; yearly: string }> = {
      starter: {
        monthly: import.meta.env.VITE_STRIPE_STARTER_MONTHLY_PRICE_ID || 'price_starter_monthly',
        yearly: import.meta.env.VITE_STRIPE_STARTER_YEARLY_PRICE_ID || 'price_starter_yearly',
      },
      pro: {
        monthly: import.meta.env.VITE_STRIPE_PRO_MONTHLY_PRICE_ID || 'price_pro_monthly',
        yearly: import.meta.env.VITE_STRIPE_PRO_YEARLY_PRICE_ID || 'price_pro_yearly',
      },
      business: {
        monthly: import.meta.env.VITE_STRIPE_BUSINESS_MONTHLY_PRICE_ID || 'price_business_monthly',
        yearly: import.meta.env.VITE_STRIPE_BUSINESS_YEARLY_PRICE_ID || 'price_business_yearly',
      },
    };

    return priceMap[planId]?.[billing] || '';
  };
  
  /**
   * Handle plan upgrade - Create Stripe checkout session
   */
  const handleUpgrade = async (planId: string) => {
    // Skip for free plan
    if (planId === 'free') return;
    
    try {
      setLoadingPlan(planId);
      
      // Get Stripe Price ID for selected plan and billing period
      const priceId = getPriceId(planId, billingPeriod);
      
      if (!priceId) {
        throw new Error('Invalid plan or billing period');
      }
      
      // Create checkout session
      const { checkout_url } = await subscriptionService.createCheckout({
        price_id: priceId,
        billing_cycle: billingPeriod,
      });
      
      // Redirect to Stripe Checkout
      window.location.href = checkout_url;
      
    } catch (error) {
      console.error('Failed to create checkout session:', error);
      alert('לא ניתן להפעיל את תהליך התשלום. נסה שוב מאוחר יותר.');
      setLoadingPlan(null);
    }
  };
  
  return (
    <div className="min-h-screen bg-gray-50 pb-24 md:pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        
        {/* Header */}
        <header className="text-center mb-12">
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <span className="text-4xl md:text-5xl font-bold text-gray-900 mb-4 block">
              בחר את התוכנית המתאימה לך
            </span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <span className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto block">
              שדרג את החוויה שלך עם תכונות מתקדמות יותר
            </span>
          </motion.p>
          
          {/* Billing Period Toggle */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <div className="inline-flex items-center gap-3 bg-white rounded-full p-2 shadow-md border border-gray-200">
            <button
              onClick={() => setBillingPeriod('monthly')}
              className={cn(
                'px-6 py-2 rounded-full font-medium transition-all duration-200',
                billingPeriod === 'monthly'
                  ? 'bg-primary-600 text-white shadow-lg'
                  : 'text-gray-600 hover:text-gray-900'
              )}
              aria-pressed={billingPeriod === 'monthly'}
            >
              חיוב חודשי
            </button>
            <button
              onClick={() => setBillingPeriod('yearly')}
              className={cn(
                'px-6 py-2 rounded-full font-medium transition-all duration-200 relative',
                billingPeriod === 'yearly'
                  ? 'bg-primary-600 text-white shadow-lg'
                  : 'text-gray-600 hover:text-gray-900'
              )}
              aria-pressed={billingPeriod === 'yearly'}
            >
              חיוב שנתי
              <span className="absolute -top-2 -left-2 bg-green-500 text-white text-xs font-bold px-2 py-0.5 rounded-full shadow-sm">
                חסוך 20%
              </span>
            </button>
            </div>
          </motion.div>
        </header>
        
        {/* Plans Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {PLANS.map((plan, index) => (
            <PlanCard
              key={plan.id}
              plan={plan}
              billingPeriod={billingPeriod}
              isCurrentPlan={currentPlan === plan.id}
              onSelect={handleUpgrade}
              delay={index * 0.1}
              isLoading={loadingPlan === plan.id}
            />
          ))}
        </div>
        
        {/* Feature Comparison */}
        <FeatureComparison />
        
        {/* FAQ Section */}
        <FAQSection />
        
        {/* Trust Badges */}
        <TrustBadges />
      </div>
    </div>
  );
};

/**
 * Plan Card Component
 * Individual subscription plan card with pricing and features
 * 
 * @component
 */
interface PlanCardProps {
  plan: Plan;
  billingPeriod: 'monthly' | 'yearly';
  isCurrentPlan: boolean;
  onSelect: (planId: string) => void;
  delay: number;
  isLoading?: boolean;
}

const PlanCard: React.FC<PlanCardProps> = ({ 
  plan, 
  billingPeriod, 
  isCurrentPlan, 
  onSelect, 
  delay,
  isLoading = false
}) => {
  const price = billingPeriod === 'monthly' ? plan.price : plan.yearlyPrice / 12;
  const totalYearly = billingPeriod === 'yearly' ? plan.yearlyPrice : plan.price * 12;
  const savings = plan.price > 0 ? plan.price * 12 - plan.yearlyPrice : 0;
  
  const colorClasses = {
    gray: 'from-gray-50 to-gray-100',
    blue: 'from-blue-50 to-blue-100',
    primary: 'from-primary-50 to-primary-100',
    purple: 'from-purple-50 to-purple-100'
  };
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
    >
      <div className="relative">
      {plan.recommended && (
        <div className="absolute -top-4 left-1/2 -translate-x-1/2 z-10">
          <div className="bg-gradient-to-r from-amber-500 to-orange-500 text-white px-4 py-1.5 rounded-full shadow-lg flex items-center gap-1.5 font-semibold text-sm">
            <Star size={14} fill="currentColor" />
            הכי פופולרי
          </div>
        </div>
      )}
      
      <Card 
        className={cn(
          'h-full flex flex-col transition-all duration-300',
          plan.recommended && 'ring-2 ring-primary-500 shadow-xl',
          !isCurrentPlan && 'hover:shadow-2xl hover:-translate-y-1'
        )}
        padding="lg"
      >
        {/* Plan Header */}
        <div className="text-center mb-6">
          <div className={cn(
            'w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br flex items-center justify-center',
            `${colorClasses[plan.color as keyof typeof colorClasses]}`,
            plan.recommended && 'ring-4 ring-primary-200'
          )}>
            <div className={cn(
              plan.color === 'primary' ? 'text-primary-600' :
              plan.color === 'blue' ? 'text-blue-600' :
              plan.color === 'purple' ? 'text-purple-600' :
              'text-gray-600'
            )}>
              {plan.icon}
            </div>
          </div>
          
          <h3 className="text-2xl font-bold text-gray-900 mb-1">
            {plan.nameHe}
          </h3>
          <p className="text-sm text-gray-500 font-medium">
            {plan.name}
          </p>
        </div>
        
        {/* Price */}
        <div className="text-center mb-6 pb-6 border-b border-gray-200">
          {plan.price === 0 ? (
            <div className="text-4xl font-bold text-gray-900">
              חינמי
            </div>
          ) : (
            <>
              <div className="flex items-baseline justify-center gap-2 mb-2">
                <span className="text-5xl font-bold text-gray-900" dir="ltr">
                  ₪{Math.round(price)}
                </span>
                <span className="text-gray-500 font-medium">
                  /חודש
                </span>
              </div>
              {billingPeriod === 'yearly' && savings > 0 && (
                <div className="text-sm text-green-600 font-medium" dir="ltr">
                  ₪{totalYearly} לשנה (חיסכון של ₪{savings})
                </div>
              )}
            </>
          )}
        </div>
        
        {/* Receipts Limit */}
        <div className="text-center mb-6 pb-6 border-b border-gray-200">
          <div className="text-sm text-gray-600 mb-1">
            קבלות בחודש
          </div>
          <div className="text-2xl font-bold text-primary-600">
            {plan.receiptsLimit === -1 ? 'ללא הגבלה' : plan.receiptsLimit.toLocaleString('he-IL')}
          </div>
        </div>
        
        {/* Features List */}
        <ul className="space-y-3 mb-8 flex-grow" role="list">
          {plan.features.map((feature, idx) => (
            <li key={idx} className="flex items-start gap-3">
              <div className="flex-shrink-0 w-5 h-5 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                <Check size={14} className="text-green-600" />
              </div>
              <span className="text-gray-700 text-sm leading-relaxed">
                {feature}
              </span>
            </li>
          ))}
        </ul>
        
        {/* CTA Button */}
        <Button
          fullWidth
          variant={plan.recommended ? 'primary' : 'secondary'}
          size="lg"
          onClick={() => onSelect(plan.id)}
          disabled={isCurrentPlan || isLoading}
          loading={isLoading}
          className="mt-auto"
        >
          {isCurrentPlan ? (
            <>
              <Check size={18} />
              התוכנית הנוכחית שלך
            </>
          ) : plan.id === 'free' ? (
            'התחל בחינם'
          ) : (
            'שדרג עכשיו'
          )}
        </Button>
      </Card>
      </div>
    </motion.div>
  );
};

/**
 * Feature Comparison Table Component
 * Detailed comparison of features across all plans
 * 
 * @component
 */
const FeatureComparison: React.FC = () => {
  const features = [
    { name: 'קבלות בחודש', free: '50', starter: '200', pro: '1,000', business: 'ללא הגבלה' },
    { name: 'OCR אוטומטי', free: true, starter: true, pro: true, business: true },
    { name: 'אחסון בענן', free: true, starter: true, pro: true, business: true },
    { name: 'ייצוא לאקסל', free: true, starter: true, pro: true, business: true },
    { name: 'חיפוש מתקדם', free: false, starter: true, pro: true, business: true },
    { name: 'קטגוריות מותאמות', free: false, starter: true, pro: true, business: true },
    { name: 'דוחות חודשיים', free: false, starter: true, pro: true, business: true },
    { name: 'AI מתקדם', free: false, starter: false, pro: true, business: true },
    { name: 'דוחות מתקדמים', free: false, starter: false, pro: true, business: true },
    { name: 'אינטגרציה עם רואה חשבון', free: false, starter: false, pro: true, business: true },
    { name: 'ניהול צוות', free: false, starter: false, pro: false, business: true },
    { name: 'API מלא', free: false, starter: false, pro: false, business: true },
    { name: 'חתימה דיגיטלית', free: false, starter: false, pro: false, business: true },
    { name: 'מנהל חשבון ייעודי', free: false, starter: false, pro: false, business: true },
  ];
  
  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
    >
      <div className="mb-16">
      <h2 className="text-3xl font-bold text-gray-900 text-center mb-8">
        השוואת תכונות
      </h2>
      
      <Card padding="none" className="overflow-x-auto">
        <div className="min-w-[800px]">
          <table className="w-full" role="table">
            <thead>
              <tr className="bg-gray-50 border-b border-gray-200">
                <th className="text-right py-4 px-6 font-semibold text-gray-900" scope="col">
                  תכונה
                </th>
                <th className="text-center py-4 px-6 font-semibold text-gray-900" scope="col">
                  חינמי
                </th>
                <th className="text-center py-4 px-6 font-semibold text-gray-900" scope="col">
                  בסיסי
                </th>
                <th className="text-center py-4 px-6 font-semibold text-gray-900 bg-primary-50" scope="col">
                  מקצועי
                  <div className="text-xs font-normal text-primary-600 mt-1">
                    מומלץ
                  </div>
                </th>
                <th className="text-center py-4 px-6 font-semibold text-gray-900" scope="col">
                  עסקי
                </th>
              </tr>
            </thead>
            <tbody>
              {features.map((feature, idx) => (
                <tr 
                  key={idx} 
                  className={cn(
                    'border-b border-gray-200 hover:bg-gray-50 transition-colors',
                    idx % 2 === 0 ? 'bg-white' : 'bg-gray-50/50'
                  )}
                >
                  <td className="py-4 px-6 text-gray-900 font-medium">
                    {feature.name}
                  </td>
                  <td className="py-4 px-6 text-center">
                    {typeof feature.free === 'boolean' ? (
                      feature.free ? (
                        <Check size={20} className="text-green-600 mx-auto" aria-label="כלול" />
                      ) : (
                        <X size={20} className="text-gray-300 mx-auto" aria-label="לא כלול" />
                      )
                    ) : (
                      <span className="text-gray-900 font-semibold">{feature.free}</span>
                    )}
                  </td>
                  <td className="py-4 px-6 text-center">
                    {typeof feature.starter === 'boolean' ? (
                      feature.starter ? (
                        <Check size={20} className="text-green-600 mx-auto" aria-label="כלול" />
                      ) : (
                        <X size={20} className="text-gray-300 mx-auto" aria-label="לא כלול" />
                      )
                    ) : (
                      <span className="text-gray-900 font-semibold">{feature.starter}</span>
                    )}
                  </td>
                  <td className="py-4 px-6 text-center bg-primary-50/30">
                    {typeof feature.pro === 'boolean' ? (
                      feature.pro ? (
                        <Check size={20} className="text-green-600 mx-auto" aria-label="כלול" />
                      ) : (
                        <X size={20} className="text-gray-300 mx-auto" aria-label="לא כלול" />
                      )
                    ) : (
                      <span className="text-gray-900 font-semibold">{feature.pro}</span>
                    )}
                  </td>
                  <td className="py-4 px-6 text-center">
                    {typeof feature.business === 'boolean' ? (
                      feature.business ? (
                        <Check size={20} className="text-green-600 mx-auto" aria-label="כלול" />
                      ) : (
                        <X size={20} className="text-gray-300 mx-auto" aria-label="לא כלול" />
                      )
                    ) : (
                      <span className="text-gray-900 font-semibold">{feature.business}</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
      </div>
    </motion.section>
  );
};

/**
 * FAQ Section Component
 * Accordion-style frequently asked questions
 * 
 * @component
 */
const FAQSection: React.FC = () => {
  const [openFaq, setOpenFaq] = useState<number | null>(null);
  
  const faqs = [
    {
      question: 'האם אוכל לשנות תוכנית בכל זמן?',
      answer: 'כן, אפשר לשדרג או להוריד תוכנית בכל עת. שינוי יכנס לתוקף מיד והחיוב יותאם באופן יחסי.'
    },
    {
      question: 'מה קורה אם אחרוג ממגבלת הקבלות?',
      answer: 'המערכת תודיע לך כשתגיע ל-80% מהמכסה. אם תחרוג, תוכל לשדרג תוכנית או לחכות לחודש הבא.'
    },
    {
      question: 'האם יש תקופת ניסיון חינם?',
      answer: 'כן! התוכנית החינמית מאפשרת לך לנסות את המערכת עם 50 קבלות בחודש ללא מגבלת זמן.'
    },
    {
      question: 'איך מבטלים מנוי?',
      answer: 'אפשר לבטל את המנוי בכל עת דרך הגדרות החשבון. המנוי יישאר פעיל עד סוף התקופה המשולמת.'
    },
    {
      question: 'האם הנתונים שלי מאובטחים?',
      answer: 'כן, אנחנו משתמשים בהצפנה ברמה בנקאית (AES-256) ואחסון מפוזר ב-AWS. כל הנתונים מוגנים ומגובים.'
    },
    {
      question: 'מה כולל החיוב השנתי?',
      answer: 'בחיוב שנתי אתם משלמים מראש עבור 12 חודשים ומקבלים 20% הנחה. אפשר לבטל בכל עת עם החזר יחסי.'
    }
  ];
  
  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
    >
      <div className="mb-16">
      <h2 className="text-3xl font-bold text-gray-900 text-center mb-8">
        שאלות נפוצות
      </h2>
      
      <Card padding="none" className="max-w-3xl mx-auto overflow-hidden">
        {faqs.map((faq, idx) => (
          <div 
            key={idx} 
            className="border-b border-gray-200 last:border-b-0"
          >
            <button
              onClick={() => setOpenFaq(openFaq === idx ? null : idx)}
              className="w-full px-6 py-4 text-right flex items-center justify-between hover:bg-gray-50 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-inset"
              aria-expanded={openFaq === idx}
              aria-controls={`faq-answer-${idx}`}
            >
              <span className="text-gray-900 font-semibold text-lg">
                {faq.question}
              </span>
              <ChevronDown 
                size={20}
                className={cn(
                  'text-primary-600 transition-transform duration-200 flex-shrink-0 mr-3',
                  openFaq === idx && 'rotate-180'
                )}
              />
            </button>
            
            <AnimatePresence>
              {openFaq === idx && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <div className="overflow-hidden">
                  <p id={`faq-answer-${idx}`} className="px-6 pb-4 text-gray-600 leading-relaxed">
                    {faq.answer}
                  </p>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        ))}
      </Card>
      </div>
    </motion.section>
  );
};

/**
 * Trust Badges Component
 * Display security and trust indicators
 * 
 * @component
 */
const TrustBadges: React.FC = () => (
  <motion.section
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true }}
    transition={{ duration: 0.5 }}
  >
    <div className="text-center">
    <div className="flex flex-wrap justify-center gap-8 items-center">
      {/* Security Badge */}
      <div className="flex flex-col items-center gap-2 text-gray-600">
        <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center">
          <Shield size={24} className="text-green-600" />
        </div>
        <span className="text-sm font-medium">
          אבטחה ברמה בנקאית
        </span>
      </div>
      
      {/* ISO Badge */}
      <div className="flex flex-col items-center gap-2 text-gray-600">
        <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
          <Lock size={24} className="text-blue-600" />
        </div>
        <span className="text-sm font-medium">
          תקן ISO 27001
        </span>
      </div>
      
      {/* Users Badge */}
      <div className="flex flex-col items-center gap-2 text-gray-600">
        <div className="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center">
          <Users size={24} className="text-purple-600" />
        </div>
        <span className="text-sm font-medium">
          1000+ עסקים מרוצים
        </span>
      </div>
    </div>
    
    {/* Support Text */}
    <p className="text-gray-500 text-sm mt-8 max-w-2xl mx-auto">
      כל התוכניות כוללות תמיכה טכנית בעברית, גיבוי אוטומטי, והתאמה לדרישות רשות המסים בישראל
    </p>
    </div>
  </motion.section>
);

export default SubscriptionPage;
