import React from 'react';
import type { LucideIcon } from 'lucide-react';
import Button from '@/components/ui/Button';

/**
 * EmptyState Component Props
 */
interface EmptyStateProps {
  /** Icon component from lucide-react */
  icon: LucideIcon;
  /** Main heading text */
  title: string;
  /** Supporting description text */
  description: string;
  /** Primary action button label */
  actionLabel?: string;
  /** Primary action button callback */
  onAction?: () => void;
  /** Secondary action button label */
  secondaryLabel?: string;
  /** Secondary action button callback */
  onSecondaryAction?: () => void;
  /** Additional CSS classes */
  className?: string;
}

/**
 * Generic Empty State Component
 * 
 * Used to display helpful messages when there's no content to show.
 * Follows Tik-Tax design system for consistency.
 * 
 * @component
 * @example
 * // No receipts in archive
 * <EmptyState
 *   icon={Receipt}
 *   title="הארכיון ריק"
 *   description="לאחר שתאשר קבלות, הן יופיעו כאן"
 *   actionLabel="העלה קבלה"
 *   onAction={() => navigate('/upload')}
 * />
 * 
 * @example
 * // No search results
 * <EmptyState
 *   icon={Search}
 *   title="לא נמצאו תוצאות"
 *   description="נסה מילות חיפוש אחרות"
 *   actionLabel="נקה חיפוש"
 *   onAction={() => setSearch('')}
 * />
 */
export const EmptyState: React.FC<EmptyStateProps> = ({
  icon: Icon,
  title,
  description,
  actionLabel,
  onAction,
  secondaryLabel,
  onSecondaryAction,
  className = ''
}) => {
  return (
    <div className={`flex flex-col items-center justify-center py-12 px-4 text-center ${className}`}>
      {/* Icon Container */}
      <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
        <Icon className="w-8 h-8 text-gray-400" />
      </div>
      
      {/* Text Content */}
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600 max-w-md mb-6">{description}</p>
      
      {/* Action Buttons */}
      <div className="flex items-center gap-3 flex-wrap justify-center">
        {actionLabel && onAction && (
          <Button onClick={onAction} size="lg">
            {actionLabel}
          </Button>
        )}
        {secondaryLabel && onSecondaryAction && (
          <Button onClick={onSecondaryAction} variant="secondary" size="lg">
            {secondaryLabel}
          </Button>
        )}
      </div>
    </div>
  );
};
