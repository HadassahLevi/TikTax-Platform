import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { CheckCircle, ArrowRight, Loader2 } from 'lucide-react';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import { subscriptionService } from '@/services';

/**
 * Checkout Success Page
 * 
 * Displayed after successful Stripe checkout.
 * Shows subscription details and redirects to dashboard.
 * 
 * Features:
 * - Success animation with checkmark
 * - Subscription details display
 * - Auto-redirect after 5 seconds
 * - Manual navigation button
 * - Loading state while fetching details
 * 
 * @component
 * @example
 * ```tsx
 * // Stripe redirects here with session_id
 * <Route path="/checkout/success" element={<CheckoutSuccessPage />} />
 * ```
 */
export const CheckoutSuccessPage: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [subscriptionDetails, setSubscriptionDetails] = useState<any>(null);
  const [countdown, setCountdown] = useState(5);

  // Fetch subscription details on mount
  useEffect(() => {
    const fetchDetails = async () => {
      try {
        const details = await subscriptionService.getSubscriptionStatus();
        setSubscriptionDetails(details);
      } catch (error) {
        console.error('Failed to fetch subscription details:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDetails();
  }, []);

  // Auto-redirect countdown
  useEffect(() => {
    if (loading || countdown <= 0) return;

    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          navigate('/dashboard');
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [loading, countdown, navigate]);

  const handleNavigateToDashboard = () => {
    navigate('/dashboard');
  };

  const getPlanName = (plan: string) => {
    const names: Record<string, string> = {
      starter: 'Starter',
      pro: 'Pro',
      business: 'Business',
    };
    return names[plan] || plan;
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'לא זמין';
    const date = new Date(dateString);
    return date.toLocaleDateString('he-IL', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        <Card className="p-8 md:p-12 text-center">
          {loading ? (
            // Loading State
            <div className="flex flex-col items-center gap-4">
              <Loader2 size={48} className="text-primary-600 animate-spin" />
              <p className="text-gray-600">טוען פרטי מנוי...</p>
            </div>
          ) : (
            <>
              {/* Success Animation */}
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{
                  type: 'spring',
                  stiffness: 260,
                  damping: 20,
                }}
              >
                <div className="flex justify-center mb-6">
                  <div className="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center">
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ delay: 0.2 }}
                    >
                      <CheckCircle size={56} className="text-green-600" />
                    </motion.div>
                  </div>
                </div>
              </motion.div>

              {/* Success Message */}
              <motion.h1
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
              >
                <div className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                  התשלום בוצע בהצלחה! 🎉
                </div>
              </motion.h1>

              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
              >
                <div className="text-lg text-gray-600 mb-8">
                  המנוי שלך הופעל. ברוך הבא ל-Tik-Tax!
                </div>
              </motion.p>

              {/* Subscription Details */}
              {subscriptionDetails && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 }}
                >
                  <div className="bg-gray-50 rounded-xl p-6 mb-8 text-right">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4">
                      פרטי המנוי
                    </h2>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-gray-600">תוכנית:</span>
                        <span className="font-semibold text-primary-600">
                          {getPlanName(subscriptionDetails.subscription_plan)}
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-600">סטטוס:</span>
                        <span className="font-semibold text-green-600">פעיל</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-600">מגבלת קבלות:</span>
                        <span className="font-semibold text-gray-900">
                          {subscriptionDetails.receipt_limit === -1
                            ? 'ללא הגבלה'
                            : `${subscriptionDetails.receipt_limit} בחודש`}
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-600">תאריך התחלה:</span>
                        <span className="font-semibold text-gray-900">
                          {formatDate(subscriptionDetails.subscription_start_date)}
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-600">חידוש הבא:</span>
                        <span className="font-semibold text-gray-900">
                          {formatDate(subscriptionDetails.subscription_end_date)}
                        </span>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Action Buttons */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
              >
                <div className="flex flex-col gap-4">
                  <Button
                    onClick={handleNavigateToDashboard}
                    size="lg"
                    className="w-full"
                    icon={<ArrowRight size={20} />}
                    iconPosition="left"
                  >
                    חזור לדשבורד
                  </Button>

                  <p className="text-sm text-gray-500">
                    מועבר אוטומטית בעוד {countdown} שניות...
                  </p>
                </div>
              </motion.div>
            </>
          )}
        </Card>

        {/* Additional Info */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
        >
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              קיבלת אישור בדוא״ל עם כל הפרטים.
              <br />
              יש שאלות? צור קשר עם{' '}
              <a href="mailto:support@tiktax.co.il" className="text-primary-600 hover:underline">
                התמיכה שלנו
              </a>
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default CheckoutSuccessPage;
