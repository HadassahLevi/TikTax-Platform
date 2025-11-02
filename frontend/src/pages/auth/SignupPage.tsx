import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import {
  User,
  CreditCard,
  Mail,
  Lock,
  Phone,
  Briefcase,
  Hash,
  Eye,
  EyeOff
} from 'lucide-react';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Card from '@/components/ui/Card';
import { useAuth } from '@/hooks/useAuth';
import { useToast } from '@/hooks/useToast';
import { sendSMSVerification, verifySMSCode } from '@/services/auth.service';
import ProgressIndicator from '@/components/auth/ProgressIndicator';
import PasswordStrength from '@/components/auth/PasswordStrength';
import SMSVerification from '@/components/auth/SMSVerification';
import type { SignupData } from '@/types/auth.types';

/**
 * Signup form data interface (matches requirements)
 */
interface SignupFormData {
  // Step 1 - Personal Info
  fullName: string;
  idNumber: string;
  email: string;
  password: string;
  confirmPassword: string;
  phone: string;

  // Step 2 - Business Info
  businessName: string;
  businessNumber: string;
  businessType: 'licensed_dealer' | 'exempt_dealer' | 'limited_company';

  // Step 3 - Verification
  verificationCode: string;
}

/**
 * Business type options for dropdown
 */
const BUSINESS_TYPES = [
  { value: 'licensed_dealer', label: 'עוסק מורשה' },
  { value: 'exempt_dealer', label: 'עוסק פטור' },
  { value: 'limited_company', label: 'חברה בע"מ' }
] as const;

/**
 * Validate Israeli ID number (with checksum)
 */
const validateIsraeliID = (id: string): boolean => {
  if (!/^\d{9}$/.test(id)) return false;

  const digits = id.split('').map(Number);
  const sum = digits.reduce((acc, digit, index) => {
    let value = digit * ((index % 2) + 1);
    if (value > 9) value -= 9;
    return acc + value;
  }, 0);

  return sum % 10 === 0;
};

/**
 * Format Israeli phone number
 */
const formatPhone = (phone: string): string => {
  const cleaned = phone.replace(/\D/g, '');
  if (cleaned.length === 10) {
    return `${cleaned.slice(0, 3)}-${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
  }
  return phone;
};

/**
 * Comprehensive 3-Step Signup Page Component
 * 
 * Features:
 * - Progress indicator showing current step
 * - Step 1: Personal information with password strength
 * - Step 2: Business information
 * - Step 3: SMS verification with countdown timer
 * - Full form validation with react-hook-form
 * - Data persistence between steps
 * - Mobile-optimized design
 * 
 * @component
 */
export const SignupPage: React.FC = () => {
  const navigate = useNavigate();
  const { signup, isAuthenticated } = useAuth();
  const { showError, showSuccess } = useToast();

  // State management
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState<Partial<SignupFormData>>({});
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, navigate]);

  // Form setup for current step
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isSubmitting },
    reset
  } = useForm<Partial<SignupFormData>>({
    defaultValues: formData
  });

  const watchPassword = watch('password', '');

  // ============================================================================
  // STEP 1: PERSONAL INFORMATION
  // ============================================================================

  const onStep1Submit = async (data: Partial<SignupFormData>) => {
    // Save step 1 data
    setFormData(prev => ({ ...prev, ...data }));
    
    // Move to step 2
    setCurrentStep(2);
    reset(data); // Reset form with new default values
  };

  const renderStep1 = () => (
    <form onSubmit={handleSubmit(onStep1Submit)} className="space-y-5">
      <h2 className="text-2xl font-semibold text-gray-900 mb-6">
        פרטים אישיים
      </h2>

      {/* Full Name */}
      <Input
        label="שם מלא"
        icon={<User className="w-5 h-5" />}
        error={errors.fullName?.message}
        {...register('fullName', {
          required: 'שדה חובה',
          validate: (value) => {
            if (!value) return 'שדה חובה';
            const words = value.trim().split(/\s+/);
            if (words.length < 2) return 'יש להזין שם פרטי ושם משפחה';
            if (!/^[\u0590-\u05FFa-zA-Z\s]+$/.test(value)) {
              return 'ניתן להזין אותיות בעברית או אנגלית בלבד';
            }
            return true;
          }
        })}
        placeholder="דוד כהן"
      />

      {/* ID Number */}
      <Input
        label="תעודת זהות"
        icon={<CreditCard className="w-5 h-5" />}
        error={errors.idNumber?.message}
        helperText="9 ספרות"
        {...register('idNumber', {
          required: 'שדה חובה',
          validate: (value) => {
            if (!value) return 'שדה חובה';
            if (!/^\d{9}$/.test(value)) return 'תעודת זהות חייבת להכיל 9 ספרות';
            if (!validateIsraeliID(value)) return 'מספר תעודת זהות לא תקין';
            return true;
          }
        })}
        placeholder="123456789"
        maxLength={9}
        inputMode="numeric"
      />

      {/* Email */}
      <Input
        label="אימייל"
        type="email"
        icon={<Mail className="w-5 h-5" />}
        error={errors.email?.message}
        {...register('email', {
          required: 'שדה חובה',
          pattern: {
            value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            message: 'כתובת אימייל לא תקינה'
          }
        })}
        placeholder="david@example.com"
        dir="ltr"
      />

      {/* Password */}
      <div className="relative">
        <Input
          label="סיסמה"
          type={showPassword ? 'text' : 'password'}
          icon={<Lock className="w-5 h-5" />}
          error={errors.password?.message}
          {...register('password', {
            required: 'שדה חובה',
            validate: (value) => {
              if (!value) return 'שדה חובה';
              if (value.length < 8) return 'הסיסמה חייבת להכיל לפחות 8 תווים';
              if (!/[A-Z]/.test(value)) return 'הסיסמה חייבת להכיל לפחות אות גדולה אחת';
              if (!/[a-z]/.test(value)) return 'הסיסמה חייבת להכיל לפחות אות קטנה אחת';
              if (!/[0-9]/.test(value)) return 'הסיסמה חייבת להכיל לפחות ספרה אחת';
              return true;
            }
          })}
          placeholder="••••••••"
        />
        <button
          type="button"
          onClick={() => setShowPassword(!showPassword)}
          className="absolute left-3 top-9 text-gray-400 hover:text-gray-600"
        >
          {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
        </button>
      </div>

      {/* Password Strength Indicator */}
      {watchPassword && <PasswordStrength password={watchPassword} />}

      {/* Confirm Password */}
      <div className="relative">
        <Input
          label="אימות סיסמה"
          type={showConfirmPassword ? 'text' : 'password'}
          icon={<Lock className="w-5 h-5" />}
          error={errors.confirmPassword?.message}
          {...register('confirmPassword', {
            required: 'שדה חובה',
            validate: (value) => {
              if (value !== watchPassword) return 'הסיסמאות אינן תואמות';
              return true;
            }
          })}
          placeholder="••••••••"
        />
        <button
          type="button"
          onClick={() => setShowConfirmPassword(!showConfirmPassword)}
          className="absolute left-3 top-9 text-gray-400 hover:text-gray-600"
        >
          {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
        </button>
      </div>

      {/* Phone */}
      <Input
        label="טלפון"
        icon={<Phone className="w-5 h-5" />}
        error={errors.phone?.message}
        helperText="+972"
        {...register('phone', {
          required: 'שדה חובה',
          validate: (value) => {
            if (!value) return 'שדה חובה';
            const cleaned = value.replace(/\D/g, '');
            if (cleaned.length !== 10) return 'מספר טלפון חייב להכיל 10 ספרות';
            if (!cleaned.startsWith('05')) return 'מספר טלפון חייב להתחיל ב-05';
            return true;
          }
        })}
        placeholder="050-123-4567"
        inputMode="tel"
        dir="ltr"
        onBlur={(e) => {
          const formatted = formatPhone(e.target.value);
          e.target.value = formatted;
        }}
      />

      {/* Submit Button */}
      <Button
        type="submit"
        className="w-full"
        disabled={isSubmitting}
      >
        הבא
      </Button>
    </form>
  );

  // ============================================================================
  // STEP 2: BUSINESS INFORMATION
  // ============================================================================

  const onStep2Submit = async (data: Partial<SignupFormData>) => {
    // Save step 2 data
    const updatedData = { ...formData, ...data };
    setFormData(updatedData);

    // Send SMS verification
    try {
      await sendSMSVerification(updatedData.phone!);
      showSuccess('קוד אימות נשלח למספר הטלפון שלך');
      
      // Move to step 3
      setCurrentStep(3);
      reset(updatedData);
    } catch (error) {
      showError(error instanceof Error ? error.message : 'שגיאה בשליחת קוד אימות');
    }
  };

  const onStep2Back = () => {
    setCurrentStep(1);
    reset(formData);
  };

  const renderStep2 = () => (
    <form onSubmit={handleSubmit(onStep2Submit)} className="space-y-5">
      <h2 className="text-2xl font-semibold text-gray-900 mb-6">
        פרטי עסק
      </h2>

      {/* Business Name */}
      <Input
        label="שם העסק"
        icon={<Briefcase className="w-5 h-5" />}
        error={errors.businessName?.message}
        {...register('businessName', {
          required: 'שדה חובה',
          minLength: {
            value: 2,
            message: 'שם העסק חייב להכיל לפחות 2 תווים'
          }
        })}
        placeholder="דוד כהן - עיצוב גרפי"
      />

      {/* Business Number */}
      <Input
        label="מספר עוסק / ח.פ"
        icon={<Hash className="w-5 h-5" />}
        error={errors.businessNumber?.message}
        helperText="מספר עוסק מורשה או ח.פ של החברה"
        {...register('businessNumber', {
          required: 'שדה חובה',
          validate: (value) => {
            if (!value) return 'שדה חובה';
            if (!/^\d{9}$/.test(value)) return 'מספר עוסק חייב להכיל 9 ספרות';
            return true;
          }
        })}
        placeholder="123456789"
        maxLength={9}
        inputMode="numeric"
      />

      {/* Business Type */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">
          סוג עסק <span className="text-red-500">*</span>
        </label>
        
        <div className="space-y-3">
          {BUSINESS_TYPES.map((type) => (
            <label
              key={type.value}
              className="flex items-center gap-3 p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-primary transition-colors"
            >
              <input
                type="radio"
                value={type.value}
                {...register('businessType', {
                  required: 'יש לבחור סוג עסק'
                })}
                className="w-4 h-4 text-primary focus:ring-primary"
              />
              <span className="text-gray-900">{type.label}</span>
            </label>
          ))}
        </div>
        
        {errors.businessType && (
          <p className="text-sm text-red-600 mt-1">
            {errors.businessType.message}
          </p>
        )}
      </div>

      {/* Buttons */}
      <div className="flex gap-3">
        <Button
          type="button"
          variant="secondary"
          onClick={onStep2Back}
          className="flex-1"
        >
          חזור
        </Button>
        <Button
          type="submit"
          className="flex-1"
          disabled={isSubmitting}
        >
          הבא
        </Button>
      </div>
    </form>
  );

  // ============================================================================
  // STEP 3: SMS VERIFICATION
  // ============================================================================

  const handleVerifyCode = async (code: string) => {
    try {
      // Verify SMS code
      await verifySMSCode(formData.phone!, code);

      // Complete signup with all data
      const signupData: SignupData = {
        fullName: formData.fullName!,
        idNumber: formData.idNumber!,
        email: formData.email!,
        password: formData.password!,
        phone: formData.phone!,
        businessName: formData.businessName!,
        businessNumber: formData.businessNumber!,
        businessType: formData.businessType!,
        verificationCode: code
      };

      await signup(signupData);
      showSuccess('הרישום הושלם בהצלחה!');
      // Navigation handled by useAuth hook
    } catch (error) {
      showError(error instanceof Error ? error.message : 'קוד שגוי. נסה שוב.');
      throw error; // Re-throw to prevent OTP from clearing
    }
  };

  const handleResendCode = async () => {
    try {
      await sendSMSVerification(formData.phone!);
      showSuccess('קוד חדש נשלח בהצלחה');
    } catch (error) {
      showError('שגיאה בשליחת קוד מחדש');
      throw error;
    }
  };

  const onStep3Back = () => {
    setCurrentStep(2);
    reset(formData);
  };

  const renderStep3 = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold text-gray-900 text-center mb-6">
        אימות מספר טלפון
      </h2>

      <SMSVerification
        phone={formData.phone!}
        onVerify={handleVerifyCode}
        onResend={handleResendCode}
        isLoading={isSubmitting}
      />

      {/* Back Button */}
      <div className="pt-4">
        <Button
          type="button"
          variant="secondary"
          onClick={onStep3Back}
          className="w-full"
          disabled={isSubmitting}
        >
          חזור
        </Button>
      </div>
    </div>
  );

  // ============================================================================
  // RENDER
  // ============================================================================

  return (
    <div className="min-h-screen bg-off-white flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-primary">Tik-Tax</h1>
          <p className="text-gray-600 mt-2">ניהול קבלות חכם</p>
        </div>

        {/* Signup Card */}
        <Card className="p-6 md:p-8">
          {/* Progress Indicator */}
          <ProgressIndicator
            currentStep={currentStep}
            totalSteps={3}
            labels={['פרטים אישיים', 'פרטי עסק', 'אימות']}
          />

          {/* Render current step */}
          {currentStep === 1 && renderStep1()}
          {currentStep === 2 && renderStep2()}
          {currentStep === 3 && renderStep3()}
        </Card>

        {/* Login Link */}
        <div className="text-center mt-6">
          <p className="text-sm text-gray-600">
            כבר יש לך חשבון?{' '}
            <Link
              to="/login"
              className="text-primary hover:text-primary-hover font-medium"
            >
              התחבר כאן
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default SignupPage;
