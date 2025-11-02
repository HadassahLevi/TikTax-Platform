import React, { useState, useEffect } from 'react';
import OtpInput from 'react-otp-input';
import { Phone, RotateCcw } from 'lucide-react';
import Button from '@/components/ui/Button';

interface SMSVerificationProps {
  phone: string;
  onVerify: (code: string) => Promise<void>;
  onResend: () => Promise<void>;
  isLoading?: boolean;
}

/**
 * SMS Verification Component
 * 
 * Features:
 * - 6-digit OTP input with auto-focus and auto-advance
 * - Countdown timer for resend (60 seconds)
 * - Clear all button
 * - Auto-submit when all 6 digits entered
 * - Phone number masking for privacy
 * 
 * @component
 * @example
 * ```tsx
 * <SMSVerification
 *   phone="0501234567"
 *   onVerify={handleVerify}
 *   onResend={handleResend}
 * />
 * ```
 */
export const SMSVerification: React.FC<SMSVerificationProps> = ({
  phone,
  onVerify,
  onResend,
  isLoading = false
}) => {
  const [otp, setOtp] = useState('');
  const [countdown, setCountdown] = useState(60);
  const [isResending, setIsResending] = useState(false);

  // Format phone number for display (mask middle digits)
  const formatPhoneForDisplay = (phoneNumber: string): string => {
    // Remove all non-digits
    const cleaned = phoneNumber.replace(/\D/g, '');
    
    if (cleaned.length === 10) {
      // Format: 050-XXX-4567 (mask middle 3 digits)
      return `${cleaned.slice(0, 3)}-XXX-${cleaned.slice(6)}`;
    }
    
    return phoneNumber;
  };

  // Countdown timer effect
  useEffect(() => {
    if (countdown > 0) {
      const timer = setTimeout(() => {
        setCountdown(countdown - 1);
      }, 1000);
      
      return () => clearTimeout(timer);
    }
  }, [countdown]);

  // Auto-submit when OTP is complete
  useEffect(() => {
    if (otp.length === 6) {
      handleVerify();
    }
  }, [otp]);

  // Handle OTP verification
  const handleVerify = async () => {
    if (otp.length === 6) {
      await onVerify(otp);
    }
  };

  // Handle resend code
  const handleResend = async () => {
    setIsResending(true);
    try {
      await onResend();
      setCountdown(60); // Reset countdown
      setOtp(''); // Clear OTP input
    } finally {
      setIsResending(false);
    }
  };

  // Clear OTP input
  const handleClear = () => {
    setOtp('');
  };

  // Format countdown as MM:SS
  const formatCountdown = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <div className="flex justify-center">
          <div className="w-16 h-16 bg-primary-light rounded-full flex items-center justify-center">
            <Phone className="w-8 h-8 text-primary" />
          </div>
        </div>
        
        <h3 className="text-lg font-semibold text-gray-900">
          אימות מספר טלפון
        </h3>
        
        <p className="text-sm text-gray-600">
          קוד אימות נשלח למספר:
        </p>
        
        <p className="text-base font-mono font-semibold text-gray-900" dir="ltr">
          {formatPhoneForDisplay(phone)}
        </p>
      </div>

      {/* OTP Input */}
      <div className="flex justify-center">
        <OtpInput
          value={otp}
          onChange={setOtp}
          numInputs={6}
          renderSeparator={<span className="mx-1"></span>}
          renderInput={(props) => (
            <input
              {...props}
              className="
                !w-12 !h-14 
                text-center text-xl font-semibold
                border-2 border-gray-300 rounded-lg
                focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20
                transition-all
                disabled:bg-gray-100 disabled:cursor-not-allowed
              "
              disabled={isLoading}
            />
          )}
          inputType="tel"
          shouldAutoFocus
        />
      </div>

      {/* Clear button (only show when OTP has value) */}
      {otp.length > 0 && (
        <div className="flex justify-center">
          <button
            type="button"
            onClick={handleClear}
            className="text-sm text-gray-500 hover:text-gray-700 underline"
            disabled={isLoading}
          >
            נקה הכל
          </button>
        </div>
      )}

      {/* Resend code section */}
      <div className="text-center space-y-3">
        {countdown > 0 ? (
          <p className="text-sm text-gray-600">
            שלח קוד מחדש בעוד{' '}
            <span className="font-mono font-semibold text-primary">
              {formatCountdown(countdown)}
            </span>
          </p>
        ) : (
          <Button
            variant="ghost"
            onClick={handleResend}
            disabled={isResending}
            className="text-primary hover:text-primary-hover"
          >
            <RotateCcw className={`w-4 h-4 ml-2 ${isResending ? 'animate-spin' : ''}`} />
            שלח קוד מחדש
          </Button>
        )}
      </div>

      {/* Helper text */}
      <div className="text-center">
        <p className="text-xs text-gray-500">
          לא קיבלת קוד? בדוק שהמספר נכון או נסה לשלוח שוב
        </p>
      </div>
    </div>
  );
};

export default SMSVerification;
