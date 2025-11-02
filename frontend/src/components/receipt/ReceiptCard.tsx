import React from 'react';
import { Clock, CheckCircle2, AlertCircle, XCircle } from 'lucide-react';
import { cn } from '@/utils/formatters';
import { formatCurrency, formatDate } from '@/utils/formatters';
import { RECEIPT_CATEGORIES } from '@/constants';
import Card from '@/components/ui/Card';
import type { Receipt, ReceiptStatus } from '@/types';

/**
 * ReceiptCard Component Props Interface
 * 
 * @interface ReceiptCardProps
 */
export interface ReceiptCardProps {
  /** Receipt data object */
  receipt: Receipt;
  /** Click handler for card interaction */
  onClick?: (receipt: Receipt) => void;
  /** Show selection state */
  selected?: boolean;
  /** Additional CSS classes */
  className?: string;
}

/**
 * Receipt Archive Card Component
 * 
 * Displays receipt summary in grid/list views with:
 * - Image thumbnail (16:9 aspect ratio)
 * - Vendor name (truncated)
 * - Amount (large, monospace)
 * - Date
 * - Category badge
 * - Status indicator
 * 
 * Following design system:
 * - Receipt card specifications
 * - Hebrew RTL support
 * - Status color coding
 * - Hover interactions
 * 
 * @component
 * @example
 * <ReceiptCard
 *   receipt={receiptData}
 *   onClick={(receipt) => viewDetails(receipt)}
 * />
 * 
 * @example
 * // Selected state
 * <ReceiptCard
 *   receipt={receiptData}
 *   selected={true}
 *   onClick={handleClick}
 * />
 */
const ReceiptCard: React.FC<ReceiptCardProps> = ({
  receipt,
  onClick,
  selected = false,
  className,
}) => {
  const categoryData = RECEIPT_CATEGORIES[receipt.category];

  // Status icon and color mapping
  const statusConfig: Record<
    ReceiptStatus,
    { icon: typeof Clock; color: string; bgColor: string; label: string }
  > = {
    pending: {
      icon: Clock,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-50',
      label: 'ממתין',
    },
    processing: {
      icon: Clock,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      label: 'בעיבוד',
    },
    completed: {
      icon: CheckCircle2,
      color: 'text-emerald-600',
      bgColor: 'bg-emerald-50',
      label: 'הושלם',
    },
    failed: {
      icon: XCircle,
      color: 'text-red-600',
      bgColor: 'bg-red-50',
      label: 'נכשל',
    },
  };

  const status = statusConfig[receipt.status];
  const StatusIcon = status.icon;

  return (
    <Card
      padding="none"
      shadow="sm"
      hoverable
      onClick={() => onClick?.(receipt)}
      className={cn(
        'group relative overflow-hidden',
        // Selected state styling
        selected && [
          'ring-2 ring-primary ring-offset-2',
          'shadow-lg',
        ],
        className
      )}
    >
      {/* Image Thumbnail */}
      <div className="relative aspect-video bg-gray-100 overflow-hidden">
        <img
          src={receipt.imageUrl}
          alt={`קבלה מ-${receipt.businessName}`}
          className={cn(
            'w-full h-full object-cover',
            'transition-transform duration-300',
            'group-hover:scale-105'
          )}
          loading="lazy"
        />

        {/* Status Indicator Dot (Top-right corner) */}
        <div className="absolute top-2 right-2">
          <div
            className={cn(
              'p-1.5 rounded-full backdrop-blur-sm',
              status.bgColor,
              'border border-white/20'
            )}
          >
            <StatusIcon className={cn('w-4 h-4', status.color)} />
          </div>
        </div>

        {/* Verified Badge (if applicable) */}
        {receipt.verified && (
          <div className="absolute top-2 left-2">
            <div
              className={cn(
                'px-2 py-1 rounded-md backdrop-blur-sm',
                'bg-emerald-500/90 text-white',
                'flex items-center gap-1'
              )}
            >
              <CheckCircle2 className="w-3 h-3" />
              <span className="text-xs font-medium">מאומת</span>
            </div>
          </div>
        )}
      </div>

      {/* Card Content */}
      <div className="p-4 space-y-3">
        {/* Vendor Name */}
        <h3
          className={cn(
            'text-base font-semibold text-gray-900',
            'truncate',
            'group-hover:text-primary transition-colors'
          )}
          title={receipt.businessName}
        >
          {receipt.businessName}
        </h3>

        {/* Amount and Date Row */}
        <div className="flex items-center justify-between gap-2">
          {/* Amount - Large monospace display */}
          <div
            className={cn(
              'text-xl font-semibold',
              'font-mono', // IBM Plex Mono
              'text-gray-900'
            )}
            dir="ltr"
          >
            {formatCurrency(receipt.amount)}
          </div>

          {/* Date */}
          <div className="text-sm text-gray-500">
            {formatDate(receipt.date)}
          </div>
        </div>

        {/* Category Badge and Status */}
        <div className="flex items-center justify-between gap-2">
          {/* Category Badge */}
          <span
            className={cn(
              'inline-flex items-center',
              'px-2.5 py-1',
              'rounded-full',
              'text-xs font-medium',
              categoryData.color,
              'border border-current/20'
            )}
          >
            {categoryData.labelHe}
          </span>

          {/* Status Label */}
          <span
            className={cn(
              'text-xs font-medium',
              status.color
            )}
          >
            {status.label}
          </span>
        </div>

        {/* OCR Confidence Indicator (if low) */}
        {receipt.ocrData.confidence < 0.8 && (
          <div className="flex items-center gap-1.5 text-xs text-amber-600">
            <AlertCircle className="w-3.5 h-3.5" />
            <span>דורש אימות</span>
          </div>
        )}
      </div>
    </Card>
  );
};

export default ReceiptCard;
