import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { Mail, Lock, Eye, EyeOff } from 'lucide-react';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import { useAuth } from '@/hooks/useAuth';
import { useToast } from '@/hooks/useToast';

/**
 * Login form data interface
 */
interface LoginFormData {
  email: string;
  password: string;
  rememberMe: boolean;
}

/**
 * Professional Login Page Component
 * 
 * Features:
 * - Form validation with react-hook-form
 * - Hebrew error messages
 * - Password visibility toggle
 * - Google OAuth integration (UI only, Phase 2)
 * - Remember me checkbox
 * - Responsive design
 * - RTL support
 * - Accessibility compliant
 * 
 * @component
 * @example
 * ```tsx
 * <Route path="/login" element={<LoginPage />} />
 * ```
 */
export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login, isAuthenticated } = useAuth();
  const { showError, showSuccess } = useToast();
  const [showPassword, setShowPassword] = useState(false);

  // Form setup with react-hook-form
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm<LoginFormData>({
    defaultValues: {
      email: '',
      password: '',
      rememberMe: false
    }
  });

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, navigate]);

  /**
   * Handle form submission
   */
  const onSubmit = async (data: LoginFormData) => {
    try {
      await login({ email: data.email, password: data.password });
      showSuccess('התחברת בהצלחה!');
      // Navigation handled by useAuth hook
    } catch (error) {
      showError(error instanceof Error ? error.message : 'שגיאה בהתחברות');
    }
  };

  /**
   * Handle Google OAuth login (Phase 2)
   */
  const handleGoogleLogin = () => {
    // TODO: Implement Google OAuth in Phase 2
    showError('התחברות עם Google תהיה זמינה בקרוב');
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-[440px]">
        {/* Card Container */}
        <div className="bg-white rounded-2xl shadow-lg p-10">
          {/* Logo */}
          <div className="flex justify-center mb-8">
            <div className="h-12 flex items-center">
              <svg
                width="48"
                height="48"
                viewBox="0 0 48 48"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                aria-label="Tik-Tax Logo"
              >
                {/* Simplified logo - checkmark in circle */}
                <circle cx="24" cy="24" r="22" fill="#2563EB" />
                <path
                  d="M14 24L20 30L34 16"
                  stroke="white"
                  strokeWidth="3"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <span className="mr-3 text-2xl font-bold text-gray-900">Tik-Tax</span>
            </div>
          </div>

          {/* Page Title */}
          <div className="text-center mb-8">
            <h1 className="text-2xl font-semibold text-gray-900 mb-2">
              התחברות
            </h1>
            <p className="text-sm text-gray-600">
              ברוכים השבים! נשמח לראותכם שוב
            </p>
          </div>

          {/* Login Form */}
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            {/* Email Field */}
            <div>
              <Input
                {...register('email', {
                  required: 'אימייל הוא שדה חובה',
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: 'כתובת אימייל לא תקינה'
                  }
                })}
                type="email"
                label="אימייל"
                placeholder="name@example.com"
                icon={<Mail size={20} />}
                iconPosition="right"
                error={errors.email?.message}
                fullWidth
                required
                autoFocus
                autoComplete="email"
                dir="ltr"
              />
            </div>

            {/* Password Field */}
            <div>
              <Input
                {...register('password', {
                  required: 'סיסמה היא שדה חובה',
                  minLength: {
                    value: 8,
                    message: 'סיסמה חייבת להכיל לפחות 8 תווים'
                  }
                })}
                type={showPassword ? 'text' : 'password'}
                label="סיסמה"
                placeholder="••••••••"
                icon={<Lock size={20} />}
                iconPosition="right"
                error={errors.password?.message}
                fullWidth
                required
                autoComplete="current-password"
                dir="ltr"
              />
              
              {/* Password Toggle Button */}
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute left-3 top-[38px] text-gray-500 hover:text-gray-700 transition-colors"
                aria-label={showPassword ? 'הסתר סיסמה' : 'הצג סיסמה'}
                style={{ position: 'relative', float: 'left', marginTop: '-42px', marginLeft: '12px' }}
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>

            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between">
              {/* Remember Me Checkbox */}
              <label className="flex items-center cursor-pointer">
                <input
                  {...register('rememberMe')}
                  type="checkbox"
                  className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500 focus:ring-offset-0 focus:ring-2 ml-2"
                />
                <span className="text-sm text-gray-700">זכור אותי</span>
              </label>

              {/* Forgot Password Link */}
              <Link
                to="/forgot-password"
                className="text-sm text-blue-600 hover:text-blue-700 font-medium transition-colors"
              >
                שכחת סיסמה?
              </Link>
            </div>

            {/* Submit Button */}
            <Button
              type="submit"
              variant="primary"
              fullWidth
              loading={isSubmitting}
              disabled={isSubmitting}
              className="mt-6"
            >
              {isSubmitting ? 'מתחבר...' : 'התחבר'}
            </Button>

            {/* Divider */}
            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-200"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-4 bg-white text-gray-500">או</span>
              </div>
            </div>

            {/* Google OAuth Button */}
            <Button
              type="button"
              variant="secondary"
              fullWidth
              onClick={handleGoogleLogin}
              disabled={isSubmitting}
              icon={
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M19.8 10.2273C19.8 9.51818 19.7364 8.83636 19.6182 8.18182H10.2V12.05H15.6091C15.3727 13.3 14.6455 14.3591 13.5636 15.0682V17.5773H16.8182C18.7091 15.8364 19.8 13.2727 19.8 10.2273Z" fill="#4285F4"/>
                  <path d="M10.2 20C12.9 20 15.1727 19.1045 16.8182 17.5773L13.5636 15.0682C12.6545 15.6682 11.5091 16.0227 10.2 16.0227C7.59545 16.0227 5.38182 14.2636 4.58182 11.9H1.22727V14.4909C2.86364 17.7591 6.27273 20 10.2 20Z" fill="#34A853"/>
                  <path d="M4.58182 11.9C4.38182 11.3 4.26364 10.6591 4.26364 10C4.26364 9.34091 4.38182 8.7 4.58182 8.1V5.50909H1.22727C0.554545 6.85909 0.181818 8.38636 0.181818 10C0.181818 11.6136 0.554545 13.1409 1.22727 14.4909L4.58182 11.9Z" fill="#FBBC04"/>
                  <path d="M10.2 3.97727C11.6227 3.97727 12.8864 4.48182 13.8773 5.43636L16.7682 2.54545C15.1682 0.954545 12.8955 0 10.2 0C6.27273 0 2.86364 2.24091 1.22727 5.50909L4.58182 8.1C5.38182 5.73636 7.59545 3.97727 10.2 3.97727Z" fill="#EA4335"/>
                </svg>
              }
              iconPosition="right"
            >
              התחבר עם Google
            </Button>
          </form>

          {/* Footer - Signup Link */}
          <div className="mt-8 text-center">
            <p className="text-sm text-gray-600">
              אין לך חשבון?{' '}
              <Link
                to="/signup"
                className="text-blue-600 hover:text-blue-700 font-medium transition-colors"
              >
                הירשם עכשיו
              </Link>
            </p>
          </div>
        </div>

        {/* Footer Text */}
        <div className="mt-6 text-center">
          <p className="text-xs text-gray-500">
            על ידי התחברות, אתה מסכים ל
            <a href="/terms" className="text-blue-600 hover:text-blue-700 mx-1">
              תנאי השימוש
            </a>
            ו
            <a href="/privacy" className="text-blue-600 hover:text-blue-700 mx-1">
              מדיניות הפרטיות
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
