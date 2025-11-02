import React, { useState, useId } from 'react';
import { AlertCircle, CheckCircle, Eye, EyeOff } from 'lucide-react';
import { cn } from '@/utils/formatters';

/**
 * Input Component Props Interface
 * 
 * @interface InputProps
 * @extends {React.InputHTMLAttributes<HTMLInputElement>}
 */
export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  /** Label text displayed above the input */
  label?: string;
  /** Error message to display (triggers error state) */
  error?: string;
  /** Helper text displayed below the input */
  helperText?: string;
  /** Icon element to display inside input */
  icon?: React.ReactNode;
  /** Position of the icon */
  iconPosition?: 'left' | 'right';
  /** Required field indicator (shows red asterisk) */
  required?: boolean;
  /** Makes input full width */
  fullWidth?: boolean;
  /** Success state (shows green border and checkmark) */
  success?: boolean;
}

/**
 * Professional, accessible Input component following Tik-Tax design system
 * 
 * Supports multiple input types, validation states, icons, and RTL layout.
 * Fully accessible with ARIA attributes and proper label associations.
 * 
 * @component
 * @example
 * // Basic text input with label
 * <Input 
 *   label="שם מלא" 
 *   placeholder="הזן שם מלא"
 *   required
 * />
 * 
 * @example
 * // Email input with error state
 * <Input 
 *   type="email"
 *   label="דוא״ל"
 *   error="כתובת דוא״ל לא תקינה"
 *   value={email}
 *   onChange={(e) => setEmail(e.target.value)}
 * />
 * 
 * @example
 * // Password input with helper text
 * <Input 
 *   type="password"
 *   label="סיסמה"
 *   helperText="לפחות 8 תווים"
 *   required
 * />
 * 
 * @example
 * // Input with icon
 * <Input 
 *   type="tel"
 *   label="טלפון"
 *   icon={<Phone size={20} />}
 *   iconPosition="right"
 * />
 * 
 * @example
 * // Success state
 * <Input 
 *   type="email"
 *   label="דוא״ל"
 *   value="user@example.com"
 *   success
 * />
 * 
 * @example
 * // With character counter
 * <Input 
 *   label="תיאור"
 *   maxLength={100}
 *   value={description}
 *   onChange={(e) => setDescription(e.target.value)}
 * />
 */
const Input = React.forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      error,
      helperText,
      icon,
      iconPosition = 'right',
      required = false,
      fullWidth = false,
      success = false,
      type = 'text',
      disabled = false,
      maxLength,
      value,
      className,
      id,
      ...props
    },
    ref
  ) => {
    const [showPassword, setShowPassword] = useState(false);
    const generatedId = useId();
    const inputId = id || generatedId;
    const errorId = `${inputId}-error`;
    const helperId = `${inputId}-helper`;

    // Determine if this is a password type input
    const isPasswordType = type === 'password';
    const actualType = isPasswordType && showPassword ? 'text' : type;

    // Determine validation state
    const hasError = !!error;
    const hasSuccess = success && !hasError;
    const hasIcon = !!icon || isPasswordType || hasError || hasSuccess;

    // Character count (only if maxLength is provided and value is controlled)
    const showCharacterCount = maxLength && value !== undefined;
    const currentLength = typeof value === 'string' ? value.length : 0;

    // Base input styles
    const inputClasses = cn(
      // Base styles
      'w-full rounded-lg border-[1.5px] bg-white px-4 py-3',
      'text-base text-gray-900 placeholder:text-gray-400',
      'transition-all duration-200 ease-in-out',
      'outline-none',
      
      // RTL support
      'rtl:text-right ltr:text-left',
      
      // Icon padding adjustments
      hasIcon && iconPosition === 'left' && 'rtl:pr-11 ltr:pl-11',
      hasIcon && iconPosition === 'right' && 'rtl:pl-11 ltr:pr-11',
      
      // Default state
      !hasError && !hasSuccess && !disabled && [
        'border-gray-300',
        'hover:border-gray-400',
        'focus:border-primary focus:shadow-[0_0_0_3px_rgba(37,99,235,0.1)]',
      ],
      
      // Error state
      hasError && [
        'border-red-500',
        'focus:border-red-500 focus:shadow-[0_0_0_3px_rgba(239,68,68,0.1)]',
      ],
      
      // Success state
      hasSuccess && [
        'border-green-500',
        'focus:border-green-500 focus:shadow-[0_0_0_3px_rgba(16,185,129,0.1)]',
      ],
      
      // Disabled state
      disabled && [
        'cursor-not-allowed bg-gray-50 text-gray-400',
        'border-gray-200',
      ],
      
      // Full width
      fullWidth && 'w-full',
      
      // Custom classes
      className
    );

    // Icon container styles
    const iconContainerClasses = cn(
      'pointer-events-none absolute top-1/2 -translate-y-1/2',
      'flex items-center justify-center',
      iconPosition === 'left' && 'rtl:right-3 ltr:left-3',
      iconPosition === 'right' && 'rtl:left-3 ltr:right-3'
    );

    // Password toggle button styles
    const passwordToggleClasses = cn(
      'absolute top-1/2 -translate-y-1/2',
      'flex items-center justify-center',
      'cursor-pointer text-gray-500 hover:text-gray-700',
      'transition-colors duration-200',
      'rtl:left-3 ltr:right-3'
    );

    // Render validation icon
    const renderValidationIcon = () => {
      if (hasError) {
        return <AlertCircle size={20} className="text-red-500" />;
      }
      if (hasSuccess) {
        return <CheckCircle size={20} className="text-green-500" />;
      }
      return null;
    };

    return (
      <div className={cn('flex flex-col gap-1.5', fullWidth && 'w-full')}>
        {/* Label */}
        {label && (
          <label
            htmlFor={inputId}
            className={cn(
              'text-sm font-medium text-gray-700',
              'rtl:text-right ltr:text-left',
              disabled && 'text-gray-400'
            )}
          >
            {label}
            {required && (
              <span className="ml-1 text-red-500" aria-label="required">
                *
              </span>
            )}
          </label>
        )}

        {/* Input Container */}
        <div className={cn('relative', fullWidth && 'w-full')}>
          {/* Input Element */}
          <input
            ref={ref}
            type={actualType}
            id={inputId}
            disabled={disabled}
            maxLength={maxLength}
            value={value}
            className={inputClasses}
            aria-invalid={hasError ? 'true' : 'false'}
            aria-describedby={cn(
              hasError && errorId,
              helperText && helperId
            )}
            {...props}
          />

          {/* Left/Right Icon */}
          {icon && !isPasswordType && !hasError && !hasSuccess && (
            <div className={iconContainerClasses}>
              <div className="text-gray-500">{icon}</div>
            </div>
          )}

          {/* Validation Icons (Error/Success) */}
          {(hasError || hasSuccess) && !isPasswordType && (
            <div className={iconContainerClasses}>
              {renderValidationIcon()}
            </div>
          )}

          {/* Password Toggle */}
          {isPasswordType && (
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className={passwordToggleClasses}
              aria-label={showPassword ? 'הסתר סיסמה' : 'הצג סיסמה'}
              tabIndex={-1}
            >
              {showPassword ? (
                <EyeOff size={20} />
              ) : (
                <Eye size={20} />
              )}
            </button>
          )}
        </div>

        {/* Bottom Section: Error, Helper Text, Character Count */}
        <div className="flex items-start justify-between gap-2">
          {/* Error Message or Helper Text */}
          <div className="flex-1">
            {hasError && error && (
              <div
                id={errorId}
                className="flex items-start gap-1.5 text-xs text-red-600"
                role="alert"
              >
                <AlertCircle size={16} className="mt-0.5 flex-shrink-0" />
                <span>{error}</span>
              </div>
            )}

            {!hasError && helperText && (
              <div
                id={helperId}
                className="text-xs text-gray-600"
              >
                {helperText}
              </div>
            )}
          </div>

          {/* Character Counter */}
          {showCharacterCount && (
            <div
              className={cn(
                'text-xs text-gray-500',
                currentLength > maxLength! && 'text-red-600'
              )}
            >
              {currentLength}/{maxLength}
            </div>
          )}
        </div>
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;
