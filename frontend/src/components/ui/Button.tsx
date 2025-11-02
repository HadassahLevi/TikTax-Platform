import React from 'react';
import { Loader2 } from 'lucide-react';
import { cn } from '@/utils/formatters';

/**
 * Button Component Props Interface
 * 
 * @interface ButtonProps
 * @extends {React.ButtonHTMLAttributes<HTMLButtonElement>}
 */
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /** Visual style variant of the button */
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  /** Size of the button */
  size?: 'sm' | 'md' | 'lg';
  /** Loading state - shows spinner and disables interaction */
  loading?: boolean;
  /** Disabled state */
  disabled?: boolean;
  /** Makes button full width */
  fullWidth?: boolean;
  /** Icon element to display */
  icon?: React.ReactNode;
  /** Position of the icon relative to text */
  iconPosition?: 'left' | 'right';
  /** Button content */
  children: React.ReactNode;
}

/**
 * Professional, accessible Button component following Tik-Tax design system
 * 
 * @component
 * @example
 * // Primary button (default)
 * <Button>שמור</Button>
 * 
 * @example
 * // Secondary button with icon
 * <Button variant="secondary" icon={<PlusIcon />} iconPosition="left">
 *   הוסף קבלה
 * </Button>
 * 
 * @example
 * // Loading state
 * <Button loading variant="primary">
 *   שומר...
 * </Button>
 * 
 * @example
 * // Danger button (destructive action)
 * <Button variant="danger" size="sm">
 *   מחק
 * </Button>
 * 
 * @example
 * // Ghost button with full width
 * <Button variant="ghost" fullWidth>
 *   ביטול
 * </Button>
 */
const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      loading = false,
      disabled = false,
      fullWidth = false,
      icon,
      iconPosition = 'left',
      children,
      className,
      type = 'button',
      ...props
    },
    ref
  ) => {
    const isDisabled = disabled || loading;

    // Base styles - applied to all buttons
    const baseStyles = [
      'inline-flex',
      'items-center',
      'justify-center',
      'gap-2',
      'font-medium',
      'rounded-lg',
      'transition-all',
      'duration-200',
      'ease-in-out',
      'focus:outline-none',
      'focus:ring-2',
      'focus:ring-offset-2',
      'focus-visible:ring-2',
      'focus-visible:ring-offset-2',
      'disabled:cursor-not-allowed',
      'relative',
      'overflow-hidden',
    ].join(' ');

    // Variant styles
    const variantStyles = {
      primary: [
        'bg-primary-500',
        'text-white',
        'shadow-sm',
        'hover:bg-primary-600',
        'hover:shadow-md',
        'active:bg-primary-700',
        'active:translate-y-px',
        'focus:ring-primary-500',
        'disabled:bg-gray-200',
        'disabled:text-gray-400',
        'disabled:shadow-none',
        'disabled:hover:bg-gray-200',
        'disabled:active:translate-y-0',
      ].join(' '),
      secondary: [
        'bg-white',
        'text-gray-700',
        'border',
        'border-gray-300',
        'shadow-sm',
        'hover:bg-gray-50',
        'hover:border-gray-400',
        'active:bg-gray-100',
        'active:translate-y-px',
        'focus:ring-primary-500',
        'disabled:bg-gray-100',
        'disabled:text-gray-400',
        'disabled:border-gray-200',
        'disabled:shadow-none',
        'disabled:hover:bg-gray-100',
        'disabled:active:translate-y-0',
      ].join(' '),
      ghost: [
        'bg-transparent',
        'text-primary-600',
        'hover:bg-blue-50',
        'active:bg-blue-100',
        'active:translate-y-px',
        'focus:ring-primary-500',
        'disabled:bg-transparent',
        'disabled:text-gray-400',
        'disabled:hover:bg-transparent',
        'disabled:active:translate-y-0',
      ].join(' '),
      danger: [
        'bg-error-500',
        'text-white',
        'shadow-sm',
        'hover:bg-error-600',
        'hover:shadow-md',
        'active:bg-error-700',
        'active:translate-y-px',
        'focus:ring-error-500',
        'disabled:bg-gray-200',
        'disabled:text-gray-400',
        'disabled:shadow-none',
        'disabled:hover:bg-gray-200',
        'disabled:active:translate-y-0',
      ].join(' '),
    };

    // Size styles
    const sizeStyles = {
      sm: 'px-4 py-2 text-sm h-9 min-h-[36px]',
      md: 'px-6 py-3 text-[15px] h-11 min-h-[44px]',
      lg: 'px-7 py-3.5 text-base h-[52px] min-h-[52px]',
    };

    // Full width style
    const widthStyle = fullWidth ? 'w-full' : '';

    // Icon size based on button size
    const iconSizeClass = {
      sm: 'w-4 h-4',
      md: 'w-5 h-5',
      lg: 'w-5 h-5',
    };

    // Combine all styles
    const buttonClasses = cn(
      baseStyles,
      variantStyles[variant],
      sizeStyles[size],
      widthStyle,
      className
    );

    // Render icon with proper sizing
    const renderIcon = (iconElement: React.ReactNode) => {
      if (!iconElement) return null;
      
      return (
        <span className={cn('inline-flex shrink-0', iconSizeClass[size])}>
          {iconElement}
        </span>
      );
    };

    // Loading spinner
    const renderSpinner = () => (
      <Loader2 
        className={cn('animate-spin', iconSizeClass[size])} 
        aria-hidden="true"
      />
    );

    return (
      <button
        ref={ref}
        type={type}
        className={buttonClasses}
        disabled={isDisabled}
        aria-disabled={isDisabled}
        aria-busy={loading}
        {...props}
      >
        {/* Left icon or spinner */}
        {loading && <span className="inline-flex">{renderSpinner()}</span>}
        {!loading && icon && iconPosition === 'left' && renderIcon(icon)}
        
        {/* Button text */}
        <span className={cn('inline-flex items-center', loading && 'opacity-70')}>
          {children}
        </span>
        
        {/* Right icon */}
        {!loading && icon && iconPosition === 'right' && renderIcon(icon)}
      </button>
    );
  }
);

Button.displayName = 'Button';

export default Button;
export type { ButtonProps };

/**
 * USAGE EXAMPLES (Storybook-style)
 * 
 * ============================================
 * BASIC USAGE
 * ============================================
 * 
 * import { Button } from '@/components/ui';
 * 
 * // Primary button (most common actions)
 * <Button>שמור</Button>
 * <Button variant="primary">אישור</Button>
 * 
 * // Secondary button (alternative actions)
 * <Button variant="secondary">ביטול</Button>
 * 
 * // Ghost button (tertiary actions)
 * <Button variant="ghost">עוד פרטים</Button>
 * 
 * // Danger button (destructive actions)
 * <Button variant="danger">מחק</Button>
 * 
 * ============================================
 * SIZES
 * ============================================
 * 
 * <Button size="sm">קטן</Button>
 * <Button size="md">בינוני</Button> // default
 * <Button size="lg">גדול</Button>
 * 
 * ============================================
 * WITH ICONS
 * ============================================
 * 
 * import { Upload, Download, Trash2, Plus } from 'lucide-react';
 * 
 * // Icon on left (default)
 * <Button icon={<Upload />}>העלה קבלה</Button>
 * 
 * // Icon on right
 * <Button icon={<Download />} iconPosition="right">
 *   הורד דוח
 * </Button>
 * 
 * // Icon only button (no text)
 * <Button icon={<Plus />} aria-label="הוסף קבלה" />
 * 
 * ============================================
 * STATES
 * ============================================
 * 
 * // Loading state
 * <Button loading>שומר...</Button>
 * <Button loading variant="primary">מעבד קבלה...</Button>
 * 
 * // Disabled state
 * <Button disabled>לא זמין</Button>
 * <Button disabled variant="secondary">לא ניתן ללחוץ</Button>
 * 
 * ============================================
 * FULL WIDTH
 * ============================================
 * 
 * <Button fullWidth>שמור</Button>
 * <Button fullWidth variant="secondary">ביטול</Button>
 * 
 * ============================================
 * FORM INTEGRATION
 * ============================================
 * 
 * <form onSubmit={handleSubmit}>
 *   <Button type="submit" loading={isSubmitting}>
 *     שלח טופס
 *   </Button>
 *   <Button type="button" variant="ghost" onClick={handleCancel}>
 *     ביטול
 *   </Button>
 * </form>
 * 
 * ============================================
 * COMMON PATTERNS
 * ============================================
 * 
 * // Action buttons group
 * <div className="flex gap-3">
 *   <Button variant="primary">שמור</Button>
 *   <Button variant="secondary">ביטול</Button>
 * </div>
 * 
 * // Stacked mobile buttons
 * <div className="flex flex-col gap-2">
 *   <Button fullWidth>פעולה ראשית</Button>
 *   <Button fullWidth variant="secondary">פעולה משנית</Button>
 * </div>
 * 
 * // Upload receipt button (primary use case)
 * <Button 
 *   variant="primary" 
 *   size="lg" 
 *   icon={<Upload />}
 *   fullWidth
 *   onClick={handleUpload}
 * >
 *   העלה קבלה חדשה
 * </Button>
 * 
 * // Delete confirmation
 * <Button 
 *   variant="danger" 
 *   size="sm"
 *   icon={<Trash2 />}
 *   onClick={handleDelete}
 *   disabled={!canDelete}
 * >
 *   מחק קבלה
 * </Button>
 * 
 * ============================================
 * ACCESSIBILITY EXAMPLES
 * ============================================
 * 
 * // Icon-only button (must have aria-label)
 * <Button 
 *   icon={<Plus />} 
 *   aria-label="הוסף קבלה חדשה"
 *   variant="ghost"
 * />
 * 
 * // Loading button (automatically has aria-busy)
 * <Button loading>
 *   מעבד...
 * </Button>
 * // Renders: <button aria-busy="true" aria-disabled="true">
 * 
 * // Disabled button (automatically has aria-disabled)
 * <Button disabled>
 *   לא זמין
 * </Button>
 * // Renders: <button aria-disabled="true" disabled>
 * 
 * ============================================
 * ADVANCED USAGE
 * ============================================
 * 
 * // With custom className (extends styles)
 * <Button className="mt-4 shadow-xl">
 *   כפתור מותאם
 * </Button>
 * 
 * // With ref (for focus management)
 * const buttonRef = useRef<HTMLButtonElement>(null);
 * <Button ref={buttonRef}>התמקד כאן</Button>
 * 
 * // With all HTML button attributes
 * <Button
 *   type="submit"
 *   form="my-form"
 *   name="action"
 *   value="save"
 *   onClick={handleClick}
 *   onFocus={handleFocus}
 *   onBlur={handleBlur}
 * >
 *   שמור
 * </Button>
 */
