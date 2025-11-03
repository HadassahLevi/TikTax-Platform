/**
 * ReceiptProcessing Component
 * 
 * Displays animated progress indicator during receipt OCR processing.
 * Shows real-time status updates, processing stages, error handling,
 * and timeout detection.
 * 
 * @module components/receipt/ReceiptProcessing
 */

import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Loader2, CheckCircle, XCircle, Clock } from 'lucide-react';
import Button from '@/components/ui/Button';
import { useReceipt } from '@/hooks/useReceipt';

/**
 * ReceiptProcessing Component Props
 * 
 * @interface ReceiptProcessingProps
 */
export interface ReceiptProcessingProps {
  /** ID of the receipt being processed */
  receiptId: string;
  
  /** Callback when processing completes successfully */
  onComplete: () => void;
  
  /** Callback when processing fails */
  onError: (error: string) => void;
  
  /** Callback when processing times out */
  onTimeout: () => void;
}

/**
 * Processing stage definition
 * 
 * @interface ProcessingStage
 */
interface ProcessingStage {
  /** Unique stage identifier */
  id: string;
  
  /** Stage label in Hebrew */
  label: string;
  
  /** Expected duration in seconds */
  duration: number;
}

/**
 * Processing stages (Hebrew labels)
 * Total expected time: ~14 seconds
 */
const PROCESSING_STAGES: ProcessingStage[] = [
  { id: 'upload', label: 'העלאת תמונה', duration: 2 },
  { id: 'ocr', label: 'זיהוי טקסט', duration: 5 },
  { id: 'extraction', label: 'חילוץ נתונים', duration: 3 },
  { id: 'validation', label: 'אימות מידע', duration: 2 },
  { id: 'categorization', label: 'סיווג הוצאה', duration: 2 }
];

/**
 * Timeout threshold (60 seconds)
 * Normal processing should complete in 10-15 seconds
 */
const TIMEOUT_SECONDS = 60;

/**
 * Stage progression interval (milliseconds)
 * Advance to next stage every 3 seconds
 */
const STAGE_INTERVAL_MS = 3000;

/**
 * ReceiptProcessing Component
 * 
 * Animated processing screen with:
 * - Rotating loader icon
 * - Progress bar (0-100%)
 * - Processing stage list with status indicators
 * - Elapsed time counter
 * - Error state with retry option
 * - Timeout detection and handling
 * 
 * @component
 * @example
 * ```tsx
 * <ReceiptProcessing
 *   receiptId="receipt-123"
 *   onComplete={() => navigate('/receipts/review')}
 *   onError={(err) => console.error(err)}
 *   onTimeout={() => console.warn('Processing timeout')}
 * />
 * ```
 */
export const ReceiptProcessing: React.FC<ReceiptProcessingProps> = ({
  receiptId,
  onComplete,
  onError,
  onTimeout
}) => {
  // Receipt state from store
  const { currentReceipt, isProcessing, error, retryProcessing } = useReceipt();
  
  // Local state
  const [currentStage, setCurrentStage] = useState(0);
  const [elapsedTime, setElapsedTime] = useState(0);
  const [hasTimedOut, setHasTimedOut] = useState(false);
  
  /**
   * Calculate progress percentage (0-100)
   * Based on current stage completion
   */
  const progressPercentage = Math.min(
    Math.round(((currentStage + 1) / PROCESSING_STAGES.length) * 100),
    100
  );
  
  /**
   * Effect: Simulate stage progression
   * Advance to next stage every 3 seconds while processing
   */
  useEffect(() => {
    if (!isProcessing) return;
    
    const timer = setInterval(() => {
      setCurrentStage(prev => {
        if (prev < PROCESSING_STAGES.length - 1) {
          return prev + 1;
        }
        return prev;
      });
    }, STAGE_INTERVAL_MS);
    
    return () => clearInterval(timer);
  }, [isProcessing]);
  
  /**
   * Effect: Track elapsed time
   * Increment counter every second while processing
   */
  useEffect(() => {
    if (!isProcessing) return;
    
    const timer = setInterval(() => {
      setElapsedTime(prev => prev + 1);
    }, 1000);
    
    return () => clearInterval(timer);
  }, [isProcessing]);
  
  /**
   * Effect: Timeout detection
   * Trigger timeout callback if processing exceeds 60 seconds
   */
  useEffect(() => {
    if (elapsedTime >= TIMEOUT_SECONDS && isProcessing) {
      setHasTimedOut(true);
      onTimeout();
    }
  }, [elapsedTime, isProcessing, onTimeout]);
  
  /**
   * Effect: Check processing completion
   * Trigger appropriate callback based on receipt status
   */
  useEffect(() => {
    if (currentReceipt && currentReceipt.id === receiptId && !isProcessing) {
      if (currentReceipt.status === 'review' || currentReceipt.status === 'approved') {
        onComplete();
      } else if (currentReceipt.status === 'failed') {
        onError('עיבוד הקבלה נכשל');
      }
    }
  }, [currentReceipt, receiptId, isProcessing, onComplete, onError]);
  
  /**
   * Handle retry button click
   * Reset state and retry processing
   */
  const handleRetry = async () => {
    setCurrentStage(0);
    setElapsedTime(0);
    setHasTimedOut(false);
    
    try {
      await retryProcessing(receiptId);
    } catch (err) {
      onError('ניסיון חוזר נכשל');
    }
  };
  
  /**
   * Format seconds to MM:SS display
   * 
   * @param seconds - Total seconds
   * @returns Formatted time string (e.g., "1:23")
   */
  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${String(secs).padStart(2, '0')}`;
  };
  
  // ============================================================================
  // ERROR STATE RENDER
  // ============================================================================
  
  if (error || hasTimedOut) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] p-8 text-center">
        {/* Error icon with scale animation */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', duration: 0.5 }}
        >
          <div className="w-20 h-20 rounded-full bg-red-100 flex items-center justify-center mb-6">
            <XCircle size={48} className="text-red-600" />
          </div>
        </motion.div>
        
        {/* Error title */}
        <h2 className="text-2xl font-semibold text-gray-900 mb-3">
          {hasTimedOut ? 'העיבוד לוקח זמן רב מהרגיל' : 'שגיאה בעיבוד'}
        </h2>
        
        {/* Error description */}
        <p className="text-gray-600 mb-6 max-w-md">
          {hasTimedOut
            ? 'העיבוד אמור להימשך 10-15 שניות. ייתכן שהתמונה לא ברורה או שיש בעיית חיבור.'
            : error || 'אירעה שגיאה בעיבוד הקבלה. אנא נסה שוב.'
          }
        </p>
        
        {/* Action buttons */}
        <div className="flex gap-3">
          <Button
            variant="secondary"
            onClick={() => window.history.back()}
          >
            חזור
          </Button>
          
          <Button
            variant="primary"
            onClick={handleRetry}
            icon={<Loader2 size={20} className="animate-spin" />}
          >
            נסה שוב
          </Button>
        </div>
      </div>
    );
  }
  
  // ============================================================================
  // PROCESSING STATE RENDER
  // ============================================================================
  
  return (
    <div className="flex flex-col items-center justify-center min-h-[500px] p-8">
      {/* Animated rotating loader */}
      <div className="mb-8">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
        >
          <Loader2 size={64} className="text-primary-600" />
        </motion.div>
      </div>
      
      {/* Processing title */}
      <h2 className="text-2xl font-semibold text-gray-900 mb-2">
        מעבד קבלה...
      </h2>
      
      {/* Elapsed time counter */}
      <div className="flex items-center gap-2 text-gray-600 mb-8">
        <Clock size={18} />
        <span className="text-sm">{formatTime(elapsedTime)}</span>
      </div>
      
      {/* Progress bar */}
      <div className="w-full max-w-md mb-8">
        <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
          <motion.div
            style={{
              width: `${progressPercentage}%`,
              height: '100%',
              background: 'linear-gradient(to right, #6366F1, #4F46E5)'
            }}
            initial={{ width: 0 }}
            animate={{ width: `${progressPercentage}%` }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
          />
        </div>
        <p className="text-sm text-gray-600 mt-2 text-center">
          {progressPercentage}% הושלם
        </p>
      </div>
      
      {/* Processing stages list */}
      <div className="w-full max-w-md space-y-3">
        <AnimatePresence mode="wait">
          {PROCESSING_STAGES.map((stage, index) => {
            const isActive = index === currentStage;
            const isComplete = index < currentStage;
            
            const cardClasses = `
              flex items-center gap-3 p-4 rounded-lg border
              transition-colors duration-300
              ${isActive ? 'border-primary-600 bg-primary-50' : ''}
              ${isComplete ? 'border-green-200 bg-green-50' : ''}
              ${!isActive && !isComplete ? 'border-gray-200 bg-white' : ''}
            `;
            
            return (
              <motion.div
                key={stage.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ delay: index * 0.1 }}
              >
                <div className={cardClasses}>
                  {/* Status icon */}
                  <div className="flex-shrink-0">
                    {isComplete ? (
                      <CheckCircle size={24} className="text-green-600" />
                    ) : isActive ? (
                      <Loader2 size={24} className="text-primary-600 animate-spin" />
                    ) : (
                      <div className="w-6 h-6 rounded-full border-2 border-gray-300" />
                    )}
                  </div>
                  
                  {/* Stage label */}
                  <div className="flex-1">
                    <p className={`text-sm font-medium ${
                      isActive ? 'text-primary-900' : 
                      isComplete ? 'text-green-900' : 
                      'text-gray-600'
                    }`}>
                      {stage.label}
                    </p>
                  </div>
                  
                  {/* Duration (only show for active stage) */}
                  {isActive && (
                    <div className="text-xs text-gray-500">
                      ~{stage.duration} שניות
                    </div>
                  )}
                </div>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default ReceiptProcessing;
