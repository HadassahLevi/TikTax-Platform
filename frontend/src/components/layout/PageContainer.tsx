import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Loader2 } from 'lucide-react';
import { cn } from '@/utils/formatters';

/**
 * PageContainer Component Props Interface
 * 
 * @interface PageContainerProps
 */
export interface PageContainerProps {
  /** Page content */
  children: React.ReactNode;
  /** Loading state - shows skeleton and spinner overlay */
  loading?: boolean;
  /** Page title (optional) */
  title?: string;
  /** Page subtitle/description (optional) */
  subtitle?: string;
  /** Action button(s) or other elements to display in header */
  action?: React.ReactNode;
  /** Maximum width constraint */
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  /** Disable default padding */
  noPadding?: boolean;
  /** Additional CSS classes */
  className?: string;
}

/**
 * Skeleton loader for page title area
 */
const TitleSkeleton: React.FC = () => (
  <div className="space-y-2">
    <div className="h-8 bg-gray-200 rounded w-1/3 animate-pulse" />
    <div className="h-4 bg-gray-200 rounded w-1/2 animate-pulse" />
  </div>
);

/**
 * Skeleton loader for page content
 */
const ContentSkeleton: React.FC = () => (
  <div className="grid gap-4 mt-8">
    {[1, 2, 3].map((i) => (
      <div 
        key={i} 
        className="h-32 bg-gray-200 rounded-lg animate-pulse"
        style={{ animationDelay: `${i * 100}ms` }}
      />
    ))}
  </div>
);

/**
 * PageContainer wrapper component for consistent page layouts
 * 
 * Provides:
 * - Consistent max-width and padding across pages
 * - Optional title/subtitle header with action buttons
 * - Loading state with skeleton loaders
 * - Responsive padding that adjusts by breakpoint
 * - Smooth fade-in animation
 * - Automatic scroll to top on mount
 * 
 * Following Tik-Tax design system specifications:
 * - Professional FinTech aesthetic
 * - Mobile-first responsive design
 * - RTL support for Hebrew
 * - Accessible and semantic HTML
 * 
 * @component
 * @example
 * // Basic dashboard container
 * <PageContainer title="לוח בקרה" maxWidth="xl">
 *   <DashboardContent />
 * </PageContainer>
 * 
 * @example
 * // Archive with search action
 * <PageContainer 
 *   title="ארכיון קבלות" 
 *   subtitle="כל הקבלות שלך במקום אחד"
 *   action={<SearchBar />}
 *   maxWidth="lg"
 * >
 *   <ReceiptGrid />
 * </PageContainer>
 * 
 * @example
 * // Loading state
 * ```tsx
 * <PageContainer title="טוען..." loading>
 *   <Content />
 * </PageContainer>
 * ```
 * 
 * @example
 * // Full width with no padding (for custom layouts)
 * ```tsx
 * <PageContainer maxWidth="full" noPadding>
 *   <CustomFullWidthLayout />
 * </PageContainer>
 * ```
 */
export const PageContainer: React.FC<PageContainerProps> = ({
  children,
  loading = false,
  title,
  subtitle,
  action,
  maxWidth = 'md',
  noPadding = false,
  className,
}) => {
  // Scroll to top when component mounts
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  // Max width classes mapping
  const maxWidthClasses = {
    sm: 'max-w-[640px]',
    md: 'max-w-[880px]',
    lg: 'max-w-[1200px]',
    xl: 'max-w-[1440px]',
    full: 'max-w-full',
  };

  // Padding classes (responsive)
  const paddingClasses = noPadding 
    ? '' 
    : 'px-4 sm:px-6 md:px-8';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      style={{ width: '100%' }}
    >
      <div
        className={cn(
          'w-full mx-auto',
          'min-h-[calc(100vh-128px)]', // 64px header + 64px bottom nav
          maxWidthClasses[maxWidth],
          paddingClasses,
          'py-6 sm:py-8 md:py-10',
          className
        )}
      >
      {/* Header Section (if title provided) */}
      {title && (
        <div 
          className={cn(
            'mb-6 sm:mb-8 pb-4 sm:pb-6',
            'border-b border-gray-200',
            'flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4'
          )}
        >
          {loading ? (
            <TitleSkeleton />
          ) : (
            <div className="flex-1">
              <h1 className={cn(
                'text-2xl sm:text-3xl font-semibold',
                'text-gray-900',
                'leading-tight tracking-tight'
              )}>
                {title}
              </h1>
              {subtitle && (
                <p className={cn(
                  'mt-2 text-base',
                  'text-gray-600',
                  'leading-relaxed'
                )}>
                  {subtitle}
                </p>
              )}
            </div>
          )}
          
          {/* Action Button Area */}
          {action && !loading && (
            <div className="flex items-center gap-3 flex-shrink-0">
              {action}
            </div>
          )}
        </div>
      )}

      {/* Content Area */}
      <div className="relative">
        {loading ? (
          <>
            {/* Skeleton Content */}
            <div className="opacity-60">
              <ContentSkeleton />
            </div>
            
            {/* Spinner Overlay */}
            <div 
              className={cn(
                'absolute inset-0',
                'flex items-center justify-center',
                'bg-white/50 backdrop-blur-sm',
                'rounded-lg'
              )}
              role="status"
              aria-live="polite"
              aria-label="טוען תוכן..."
            >
              <div className="flex flex-col items-center gap-3">
                <Loader2 
                  className="w-8 h-8 text-primary-600 animate-spin" 
                  aria-hidden="true"
                />
                <p className="text-sm text-gray-600 font-medium">
                  טוען...
                </p>
              </div>
            </div>
          </>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.2, delay: 0.1 }}
          >
            {children}
          </motion.div>
        )}
      </div>
      </div>
    </motion.div>
  );
};

/**
 * Alternative skeleton patterns for different page types
 */

/**
 * Grid skeleton for card-based layouts
 */
export const GridSkeleton: React.FC<{ count?: number }> = ({ count = 6 }) => (
  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
    {Array.from({ length: count }).map((_, i) => (
      <div 
        key={i} 
        className="h-48 bg-gray-200 rounded-lg animate-pulse"
        style={{ animationDelay: `${i * 50}ms` }}
      />
    ))}
  </div>
);

/**
 * List skeleton for row-based layouts
 */
export const ListSkeleton: React.FC<{ count?: number }> = ({ count = 5 }) => (
  <div className="space-y-3">
    {Array.from({ length: count }).map((_, i) => (
      <div 
        key={i} 
        className="flex items-center gap-4 p-4 bg-gray-100 rounded-lg"
        style={{ animationDelay: `${i * 50}ms` }}
      >
        <div className="w-12 h-12 bg-gray-200 rounded-lg animate-pulse" />
        <div className="flex-1 space-y-2">
          <div className="h-4 bg-gray-200 rounded w-3/4 animate-pulse" />
          <div className="h-3 bg-gray-200 rounded w-1/2 animate-pulse" />
        </div>
        <div className="w-20 h-8 bg-gray-200 rounded animate-pulse" />
      </div>
    ))}
  </div>
);

/**
 * Stats skeleton for dashboard metrics
 */
export const StatsSkeleton: React.FC = () => (
  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
    {[1, 2, 3, 4].map((i) => (
      <div 
        key={i} 
        className="bg-white border border-gray-200 rounded-lg p-6"
        style={{ animationDelay: `${i * 50}ms` }}
      >
        <div className="h-4 bg-gray-200 rounded w-1/2 animate-pulse mb-4" />
        <div className="h-8 bg-gray-200 rounded w-3/4 animate-pulse mb-2" />
        <div className="h-3 bg-gray-200 rounded w-1/3 animate-pulse" />
      </div>
    ))}
  </div>
);

/**
 * Form skeleton for input-heavy pages
 */
export const FormSkeleton: React.FC = () => (
  <div className="space-y-6 max-w-xl">
    {[1, 2, 3, 4].map((i) => (
      <div key={i} className="space-y-2">
        <div className="h-4 bg-gray-200 rounded w-1/4 animate-pulse" />
        <div className="h-12 bg-gray-200 rounded w-full animate-pulse" />
      </div>
    ))}
    <div className="flex gap-3 pt-4">
      <div className="h-12 bg-gray-200 rounded w-32 animate-pulse" />
      <div className="h-12 bg-gray-200 rounded w-32 animate-pulse" />
    </div>
  </div>
);

export default PageContainer;
