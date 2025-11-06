import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { XCircle, ArrowRight, Mail } from 'lucide-react';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';

/**
 * Checkout Cancel Page
 * 
 * Displayed when user cancels Stripe checkout.
 * Provides reassurance and options to retry or get support.
 * 
 * Features:
 * - Cancel icon with animation
 * - Reassuring message (no charge)
 * - Return to subscriptions button
 * - Contact support link
 * - Clean, professional design
 * 
 * @component
 * @example
 * ```tsx
 * // Stripe redirects here on cancel
 * <Route path="/checkout/cancel" element={<CheckoutCancelPage />} />
 * ```
 */
export const CheckoutCancelPage: React.FC = () => {
  const navigate = useNavigate();

  const handleReturnToSubscriptions = () => {
    navigate('/subscriptions');
  };

  const handleContactSupport = () => {
    window.location.href = 'mailto:support@tiktax.co.il?subject=עזרה בתהליך התשלום';
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        <Card className="p-8 md:p-12 text-center">
          {/* Cancel Icon */}
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
              <div className="w-24 h-24 bg-orange-100 rounded-full flex items-center justify-center">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.2 }}
                >
                  <XCircle size={56} className="text-orange-600" />
                </motion.div>
              </div>
            </div>
          </motion.div>

          {/* Cancel Message */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <div className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              התשלום בוטל
            </div>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <div className="text-lg text-gray-600 mb-8">
              לא חויבת. תוכל לנסות שוב בכל עת.
            </div>
          </motion.p>

          {/* Info Box */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            <div className="bg-blue-50 border border-blue-200 rounded-xl p-6 mb-8 text-right">
              <h2 className="text-lg font-semibold text-blue-900 mb-3">
                למה לשדרג?
              </h2>
              <ul className="space-y-2 text-blue-800">
                <li className="flex items-start gap-2">
                  <span className="text-blue-600 mt-1">•</span>
                  <span>יותר קבלות בחודש</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-600 mt-1">•</span>
                  <span>תכונות מתקדמות לניהול עסק</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-600 mt-1">•</span>
                  <span>יצוא לאקסל ו-PDF</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-600 mt-1">•</span>
                  <span>חתימה דיגיטלית מאושרת</span>
                </li>
              </ul>
            </div>
          </motion.div>

          {/* Action Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
          >
            <div className="flex flex-col gap-4">
              <Button
                onClick={handleReturnToSubscriptions}
                size="lg"
                className="w-full"
                icon={<ArrowRight size={20} />}
                iconPosition="left"
              >
                חזור למנויים
              </Button>

              <Button
                onClick={handleContactSupport}
                variant="secondary"
                size="lg"
                className="w-full"
                icon={<Mail size={20} />}
                iconPosition="left"
              >
                צור קשר עם תמיכה
              </Button>
            </div>
          </motion.div>
        </Card>

        {/* Additional Info */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
        >
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              נתקלת בבעיה? אנחנו כאן לעזור!
              <br />
              <a
                href="mailto:support@tiktax.co.il"
                className="text-primary-600 hover:underline font-medium"
              >
                support@tiktax.co.il
              </a>
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default CheckoutCancelPage;
