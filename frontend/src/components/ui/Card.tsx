import React from 'react';
import { cn } from '@/utils/formatters';

/**
 * Card Component Props Interface
 * 
 * @interface CardProps
 */
export interface CardProps {
  /** Card content */
  children: React.ReactNode;
  /** Shadow elevation level */
  shadow?: 'none' | 'sm' | 'md' | 'lg';
  /** Internal padding size */
  padding?: 'none' | 'sm' | 'md' | 'lg';
  /** Enable hover effect (lift + shadow increase) */
  hoverable?: boolean;
  /** Click handler - makes card interactive */
  onClick?: () => void;
  /** Additional CSS classes */
  className?: string;
  /** HTML element to render as (default: div) */
  as?: 'div' | 'article' | 'section';
}

/**
 * Flexible Card component for displaying content containers
 * 
 * Following Tik-Tax design system specifications:
 * - Professional FinTech aesthetic
 * - Consistent elevation system
 * - Smooth hover interactions
 * - Accessible and semantic HTML
 * 
 * @component
 * @example
 * // Basic card with default styling
 * <Card>
 *   <h3>כותרת כרטיס</h3>
 *   <p>תוכן הכרטיס</p>
 * </Card>
 * 
 * @example
 * // Hoverable card with custom shadow
 * <Card shadow="lg" hoverable onClick={() => console.log('clicked')}>
 *   <p>לחץ עלי</p>
 * </Card>
 * 
 * @example
 * // Card with no padding (for images)
 * <Card padding="none">
 *   <img src="/image.jpg" alt="תמונה" />
 * </Card>
 */
const Card: React.FC<CardProps> = ({
  children,
  shadow = 'md',
  padding = 'md',
  hoverable = false,
  onClick,
  className,
  as: Component = 'div',
}) => {
  // Shadow variant classes matching design system elevation levels
  const shadowClasses = {
    none: '',
    sm: 'shadow-sm', // Level 1: 0 1px 3px 0 rgba(0,0,0,0.08)
    md: 'shadow-md', // Level 2: 0 4px 6px -1px rgba(0,0,0,0.1)
    lg: 'shadow-lg', // Level 3: 0 10px 15px -3px rgba(0,0,0,0.15)
  };

  // Padding variant classes following 8-point grid
  const paddingClasses = {
    none: 'p-0',
    sm: 'p-4',   // 16px
    md: 'p-6',   // 24px
    lg: 'p-8',   // 32px
  };

  // Hover shadow mapping (increase to next level)
  const hoverShadowClasses = {
    none: 'hover:shadow-sm',
    sm: 'hover:shadow-md',
    md: 'hover:shadow-lg',
    lg: 'hover:shadow-xl',
  };

  // Base card styles from design system
  const baseClasses = cn(
    // Background and structure
    'bg-white',
    'border border-gray-200', // #E5E7EB
    'rounded-xl', // 12px - comfortable radius for cards
    'overflow-hidden', // For image cards
    
    // Shadow
    shadowClasses[shadow],
    
    // Padding
    paddingClasses[padding],
    
    // Transitions (0.2s ease per design system)
    'transition-all duration-200 ease-in-out',
    
    // Hoverable state
    hoverable && [
      'cursor-pointer',
      '-translate-y-0 hover:-translate-y-0.5', // translateY(-2px)
      hoverShadowClasses[shadow],
    ],
    
    // Focus state for accessibility (when clickable)
    onClick && [
      'focus-visible:outline-none',
      'focus-visible:ring-2',
      'focus-visible:ring-primary', // #2563EB
      'focus-visible:ring-offset-2',
    ],
  );

  const cardClasses = cn(baseClasses, className);

  return (
    <Component
      className={cardClasses}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={
        onClick
          ? (e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                onClick();
              }
            }
          : undefined
      }
    >
      {children}
    </Component>
  );
};

// Export type for external use
export type { CardProps as CardComponentProps };

export default Card;
