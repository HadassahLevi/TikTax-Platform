import { useCallback } from 'react';

/**
 * Toast notification types
 */
type ToastType = 'success' | 'error' | 'warning' | 'info';

/**
 * Toast notification hook
 * Provides simple alert-based notifications (to be replaced with proper toast UI)
 * 
 * @returns Toast notification functions
 * 
 * @example
 * ```tsx
 * const { showSuccess, showError } = useToast();
 * 
 * showSuccess('פעולה הושלמה בהצלחה!');
 * showError('אירעה שגיאה');
 * ```
 */
export const useToast = () => {
  const showToast = useCallback((message: string, type: ToastType) => {
    // TODO: Replace with proper toast notification component (Phase 2)
    // For now, using browser alert as temporary solution
    const prefix = {
      success: '✓',
      error: '✗',
      warning: '⚠',
      info: 'ℹ'
    }[type];
    
    alert(`${prefix} ${message}`);
  }, []);

  const showSuccess = useCallback((message: string) => {
    showToast(message, 'success');
  }, [showToast]);

  const showError = useCallback((message: string) => {
    showToast(message, 'error');
  }, [showToast]);

  const showWarning = useCallback((message: string) => {
    showToast(message, 'warning');
  }, [showToast]);

  const showInfo = useCallback((message: string) => {
    showToast(message, 'info');
  }, [showToast]);

  return {
    showSuccess,
    showError,
    showWarning,
    showInfo
  };
};