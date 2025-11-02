import { useEffect, useRef, useCallback, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import { cn } from '@/utils/formatters';

/**
 * Modal Component Props Interface
 * 
 * @interface ModalProps
 */
export interface ModalProps {
  /** Controls modal visibility */
  isOpen: boolean;
  /** Callback function when modal should close */
  onClose: () => void;
  /** Modal title (displays in header) */
  title?: string;
  /** Modal content */
  children: React.ReactNode;
  /** Footer content (usually action buttons) */
  footer?: React.ReactNode;
  /** Size variant of the modal */
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  /** Allow closing when clicking overlay */
  closeOnOverlayClick?: boolean;
  /** Allow closing with ESC key */
  closeOnEsc?: boolean;
  /** Show close button (X) in header */
  showCloseButton?: boolean;
}

/**
 * Custom hook for managing focus trap within modal
 * Ensures keyboard navigation stays within modal when open
 */
const useFocusTrap = (isOpen: boolean, containerRef: React.RefObject<HTMLDivElement | null>) => {
  const previousActiveElement = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (!isOpen) return;

    // Store the element that had focus before modal opened
    previousActiveElement.current = document.activeElement as HTMLElement;

    const container = containerRef.current;
    if (!container) return;

    // Get all focusable elements within modal
    const getFocusableElements = () => {
      const focusableSelectors = [
        'a[href]',
        'button:not([disabled])',
        'textarea:not([disabled])',
        'input:not([disabled])',
        'select:not([disabled])',
        '[tabindex]:not([tabindex="-1"])',
      ].join(', ');

      return Array.from(
        container.querySelectorAll<HTMLElement>(focusableSelectors)
      ).filter((el) => {
        return (
          el.offsetParent !== null &&
          !el.hasAttribute('disabled') &&
          !el.getAttribute('aria-hidden')
        );
      });
    };

    // Focus first focusable element
    const focusableElements = getFocusableElements();
    if (focusableElements.length > 0) {
      focusableElements[0].focus();
    }

    // Handle Tab key to trap focus
    const handleTabKey = (e: KeyboardEvent) => {
      const focusable = getFocusableElements();
      if (focusable.length === 0) return;

      const firstElement = focusable[0];
      const lastElement = focusable[focusable.length - 1];

      if (e.shiftKey) {
        // Shift + Tab
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement.focus();
        }
      } else {
        // Tab
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement.focus();
        }
      }
    };

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Tab') {
        handleTabKey(e);
      }
    };

    container.addEventListener('keydown', handleKeyDown);

    // Cleanup: restore focus when modal closes
    return () => {
      container.removeEventListener('keydown', handleKeyDown);
      if (previousActiveElement.current) {
        previousActiveElement.current.focus();
      }
    };
  }, [isOpen, containerRef]);
};

/**
 * Custom hook for managing body scroll lock
 * Prevents background scrolling when modal is open
 */
const useBodyScrollLock = (isOpen: boolean) => {
  useEffect(() => {
    if (isOpen) {
      // Store original overflow style
      const originalOverflow = document.body.style.overflow;
      const originalPaddingRight = document.body.style.paddingRight;

      // Calculate scrollbar width to prevent layout shift
      const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;

      // Lock scroll
      document.body.style.overflow = 'hidden';
      if (scrollbarWidth > 0) {
        document.body.style.paddingRight = `${scrollbarWidth}px`;
      }

      return () => {
        // Restore original styles
        document.body.style.overflow = originalOverflow;
        document.body.style.paddingRight = originalPaddingRight;
      };
    }
  }, [isOpen]);
};

/**
 * Animation variants for modal overlay (backdrop)
 */
const overlayVariants = {
  hidden: { opacity: 0 },
  visible: { 
    opacity: 1,
    transition: { duration: 0.2, ease: 'easeOut' }
  },
  exit: { 
    opacity: 0,
    transition: { duration: 0.15, ease: 'easeIn' }
  },
};

/**
 * Animation variants for modal container
 * Desktop: Fade + Scale
 * Mobile: Slide up from bottom
 */
const getModalVariants = (isMobile: boolean) => ({
  hidden: isMobile 
    ? { opacity: 0, y: '100%', scale: 1 }
    : { opacity: 0, y: 50, scale: 0.95 },
  visible: { 
    opacity: 1, 
    y: 0, 
    scale: 1,
    transition: { 
      duration: 0.3, 
      ease: [0.4, 0, 0.2, 1], // Custom easing
      type: 'spring',
      damping: 25,
      stiffness: 300,
    }
  },
  exit: isMobile
    ? { 
        opacity: 0, 
        y: '100%',
        transition: { duration: 0.25, ease: 'easeIn' }
      }
    : { 
        opacity: 0, 
        y: 30, 
        scale: 0.95,
        transition: { duration: 0.2, ease: 'easeIn' }
      },
});

/**
 * Fully Accessible Modal Component
 * 
 * Features:
 * - Framer Motion animations (fade, slide, scale)
 * - Focus trap (keyboard navigation contained within modal)
 * - Body scroll lock when open
 * - ESC key to close
 * - Click overlay to close
 * - Restore focus on close
 * - Full ARIA attributes
 * - Mobile optimized (full screen on small devices)
 * - Safe area support (notch devices)
 * 
 * @component
 * @example
 * ```tsx
 * const [isOpen, setIsOpen] = useState(false);
 * 
 * <Modal
 *   isOpen={isOpen}
 *   onClose={() => setIsOpen(false)}
 *   title="הוסף קבלה"
 *   footer={
 *     <div className="flex gap-3 justify-end">
 *       <Button variant="secondary" onClick={() => setIsOpen(false)}>ביטול</Button>
 *       <Button variant="primary" onClick={handleSubmit}>שמור</Button>
 *     </div>
 *   }
 * >
 *   <p>Modal content goes here...</p>
 * </Modal>
 * ```
 */
const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  footer,
  size = 'md',
  closeOnOverlayClick = true,
  closeOnEsc = true,
  showCloseButton = true,
}) => {
  const modalRef = useRef<HTMLDivElement>(null);
  const titleId = useRef(`modal-title-${Math.random().toString(36).slice(2, 9)}`).current;
  const bodyId = useRef(`modal-body-${Math.random().toString(36).slice(2, 9)}`).current;

  // Detect mobile viewport
  const [isMobile, setIsMobile] = useState(window.innerWidth < 640);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 640);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Custom hooks
  useFocusTrap(isOpen, modalRef);
  useBodyScrollLock(isOpen);

  // Handle ESC key
  useEffect(() => {
    if (!isOpen || !closeOnEsc) return;

    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, closeOnEsc, onClose]);

  // Handle overlay click
  const handleOverlayClick = useCallback(
    (e: React.MouseEvent<HTMLDivElement>) => {
      if (closeOnOverlayClick && e.target === e.currentTarget) {
        onClose();
      }
    },
    [closeOnOverlayClick, onClose]
  );

  // Size variants
  const sizeClasses = {
    sm: 'max-w-[400px]',
    md: 'max-w-[600px]',
    lg: 'max-w-[800px]',
    xl: 'max-w-[1200px]',
    full: 'max-w-[95vw]',
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          {/* Overlay (Backdrop) */}
          <motion.div
            {...({
              className: 'fixed inset-0 bg-black/50 backdrop-blur-sm',
              variants: overlayVariants,
              initial: 'hidden',
              animate: 'visible',
              exit: 'exit',
              onClick: handleOverlayClick,
              'aria-hidden': 'true',
            } as any)}
          />

          {/* Modal Container */}
          <div
            className={cn(
              'flex min-h-full items-center justify-center',
              'p-4 sm:p-6',
              // Mobile: align to bottom
              'sm:items-center items-end'
            )}
            onClick={handleOverlayClick}
          >
            <motion.div
              {...({
                ref: modalRef,
                className: cn(
                  // Base styles
                  'relative w-full bg-white',
                  'shadow-[0_20px_25px_-5px_rgba(0,0,0,0.15),0_10px_10px_-5px_rgba(0,0,0,0.08)]',
                  
                  // Border radius
                  'rounded-t-2xl sm:rounded-2xl', // Mobile: rounded top only
                  
                  // Size variants
                  sizeClasses[size],
                  
                  // Mobile: full width, fixed to bottom
                  isMobile && size !== 'full' && 'w-full max-w-full',
                  
                  // Safe area support (iOS notch)
                  'pb-safe',
                  
                  // Ensure above overlay
                  'z-50'
                ),
                variants: getModalVariants(isMobile),
                initial: 'hidden',
                animate: 'visible',
                exit: 'exit',
                role: 'dialog',
                'aria-modal': 'true',
                'aria-labelledby': title ? titleId : undefined,
                'aria-describedby': bodyId,
                onClick: (e: React.MouseEvent<HTMLDivElement>) => e.stopPropagation(),
              } as any)}
            >
              {/* Header */}
              {(title || showCloseButton) && (
                <div
                  className={cn(
                    'flex items-center justify-between',
                    'px-6 pt-6 pb-4 sm:px-8 sm:pt-8 sm:pb-6',
                    // Border bottom if there's content
                    children && 'border-b border-gray-200'
                  )}
                >
                  {title && (
                    <h2
                      id={titleId}
                      className="text-2xl font-semibold text-gray-900 leading-8"
                    >
                      {title}
                    </h2>
                  )}

                  {showCloseButton && (
                    <button
                      type="button"
                      onClick={onClose}
                      className={cn(
                        'flex items-center justify-center',
                        'w-10 h-10 -mr-2 -mt-2',
                        'rounded-lg',
                        'text-gray-400 hover:text-gray-600',
                        'hover:bg-gray-100',
                        'transition-colors duration-200',
                        'focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-offset-2',
                        // Ensure it's always on the right (RTL support)
                        !title && 'ml-auto'
                      )}
                      aria-label="סגור חלון"
                    >
                      <X size={20} strokeWidth={2} />
                    </button>
                  )}
                </div>
              )}

              {/* Body */}
              <div
                id={bodyId}
                className={cn(
                  'px-6 sm:px-8',
                  // Padding top if no header
                  !title && !showCloseButton && 'pt-6 sm:pt-8',
                  // Padding bottom if no footer
                  !footer && 'pb-6 sm:pb-8',
                  // Scrollable with max height
                  'overflow-y-auto',
                  'max-h-[70vh]',
                  // Custom scrollbar styling
                  'scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100',
                  '[&::-webkit-scrollbar]:w-2',
                  '[&::-webkit-scrollbar-track]:bg-gray-100',
                  '[&::-webkit-scrollbar-track]:rounded-full',
                  '[&::-webkit-scrollbar-thumb]:bg-gray-300',
                  '[&::-webkit-scrollbar-thumb]:rounded-full',
                  '[&::-webkit-scrollbar-thumb]:hover:bg-gray-400'
                )}
              >
                {children}
              </div>

              {/* Footer */}
              {footer && (
                <div
                  className={cn(
                    'px-6 pb-6 pt-6 sm:px-8 sm:pb-8 sm:pt-6',
                    'border-t border-gray-200',
                    'flex items-center justify-end gap-3',
                    // Sticky at bottom on mobile
                    'sm:static sticky bottom-0 bg-white',
                    // Safe area padding for iOS
                    'pb-safe'
                  )}
                >
                  {footer}
                </div>
              )}
            </motion.div>
          </div>
        </div>
      )}
    </AnimatePresence>
  );
};

/**
 * Custom hook for managing modal state
 * Provides open/close handlers and state
 * 
 * @returns {object} Modal state and handlers
 * 
 * @example
 * ```tsx
 * const { isOpen, open, close, toggle } = useModal();
 * 
 * <Button onClick={open}>פתח חלון</Button>
 * <Modal isOpen={isOpen} onClose={close} title="כותרת">
 *   תוכן...
 * </Modal>
 * ```
 */
export const useModal = (initialState = false) => {
  const [isOpen, setIsOpen] = useState(initialState);

  const open = useCallback(() => setIsOpen(true), []);
  const close = useCallback(() => setIsOpen(false), []);
  const toggle = useCallback(() => setIsOpen((prev) => !prev), []);

  return {
    isOpen,
    open,
    close,
    toggle,
    setIsOpen,
  };
};

export default Modal;
