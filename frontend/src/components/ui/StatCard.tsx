import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { cn } from '@/utils/formatters';
import Card from './Card';

/**
 * StatCard Component Props Interface
 * 
 * @interface StatCardProps
 */
export interface StatCardProps {
  /** Main statistic label */
  label: string;
  /** Large number/value to display */
  value: string | number;
  /** Optional icon component */
  icon?: LucideIcon;
  /** Icon color class (e.g., 'text-blue-500') */
  iconColor?: string;
  /** Percentage change from previous period */
  change?: number;
  /** Comparison period label (e.g., 'vs last month') */
  changeLabel?: string;
  /** Enable gradient background */
  gradient?: boolean;
  /** Custom gradient colors (from -> to) */
  gradientColors?: { from: string; to: string };
  /** Click handler */
  onClick?: () => void;
  /** Additional CSS classes */
  className?: string;
}

/**
 * Dashboard Statistics Card Component
 * 
 * Specialized card for displaying key metrics with:
 * - Large number displays
 * - Optional icons
 * - Percentage change indicators
 * - Gradient background support
 * 
 * Following design system:
 * - Currency formatting for financial data
 * - Monospace fonts for numbers
 * - Color-coded change indicators
 * 
 * @component
 * @example
 * // Basic stat card
 * <StatCard
 *   label="סך הוצאות החודש"
 *   value="₪12,345.67"
 * />
 * 
 * @example
 * // With percentage change and icon
 * <StatCard
 *   label="קבלות החודש"
 *   value={42}
 *   icon={ReceiptIcon}
 *   iconColor="text-blue-500"
 *   change={12.5}
 *   changeLabel="לעומת חודש קודם"
 * />
 * 
 * @example
 * // Gradient background variant
 * <StatCard
 *   label="יתרה"
 *   value="₪98,765.43"
 *   gradient
 *   gradientColors={{ from: 'from-blue-500', to: 'to-blue-700' }}
 * />
 */
const StatCard: React.FC<StatCardProps> = ({
  label,
  value,
  icon: Icon,
  iconColor = 'text-gray-400',
  change,
  changeLabel,
  gradient = false,
  gradientColors = { from: 'from-primary', to: 'to-primary-dark' },
  onClick,
  className,
}) => {
  // Determine if change is positive or negative
  const isPositive = change !== undefined && change >= 0;
  const hasChange = change !== undefined;

  return (
    <Card
      shadow="md"
      padding="lg"
      hoverable={!!onClick}
      onClick={onClick}
      className={cn(
        'relative',
        gradient && [
          'bg-gradient-to-br',
          gradientColors.from,
          gradientColors.to,
          'text-white',
          'border-none',
        ],
        className
      )}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          {/* Label */}
          <p
            className={cn(
              'text-sm font-medium mb-2',
              gradient ? 'text-white/90' : 'text-gray-600'
            )}
          >
            {label}
          </p>

          {/* Main Value - Large display with monospace font for numbers */}
          <p
            className={cn(
              'text-3xl font-semibold mb-3',
              'font-mono', // IBM Plex Mono for financial data
              gradient ? 'text-white' : 'text-gray-900'
            )}
            dir="ltr" // Numbers always LTR
          >
            {value}
          </p>

          {/* Percentage Change Indicator */}
          {hasChange && (
            <div className="flex items-center gap-1.5">
              {isPositive ? (
                <TrendingUp
                  className={cn(
                    'w-4 h-4',
                    gradient ? 'text-white/80' : 'text-emerald-600'
                  )}
                />
              ) : (
                <TrendingDown
                  className={cn(
                    'w-4 h-4',
                    gradient ? 'text-white/80' : 'text-red-600'
                  )}
                />
              )}
              <span
                className={cn(
                  'text-sm font-medium',
                  gradient
                    ? 'text-white/90'
                    : isPositive
                    ? 'text-emerald-600'
                    : 'text-red-600'
                )}
              >
                {isPositive ? '+' : ''}
                {change}%
              </span>
              {changeLabel && (
                <span
                  className={cn(
                    'text-xs',
                    gradient ? 'text-white/70' : 'text-gray-500'
                  )}
                >
                  {changeLabel}
                </span>
              )}
            </div>
          )}
        </div>

        {/* Icon */}
        {Icon && (
          <div
            className={cn(
              'p-3 rounded-lg',
              gradient
                ? 'bg-white/20 text-white'
                : 'bg-gray-50',
              !gradient && iconColor
            )}
          >
            <Icon className="w-6 h-6" />
          </div>
        )}
      </div>
    </Card>
  );
};

export default StatCard;
