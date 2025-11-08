/**
 * Accessibility utility functions for TIK-TAX
 * Ensures WCAG 2.1 AA compliance
 */

/**
 * Trap focus within an element (for modals, dialogs)
 */
export const trapFocus = (element: HTMLElement): (() => void) => {
  const focusableSelectors = [
    'button:not([disabled])',
    '[href]',
    'input:not([disabled])',
    'select:not([disabled])',
    'textarea:not([disabled])',
    '[tabindex]:not([tabindex="-1"])',
    '[contenteditable="true"]'
  ].join(', ');

  const focusableElements = Array.from(
    element.querySelectorAll<HTMLElement>(focusableSelectors)
  );

  if (focusableElements.length === 0) return () => {};

  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];

  const handleTabKey = (e: KeyboardEvent) => {
    if (e.key !== 'Tab') return;

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

  // Focus first element
  firstElement.focus();

  // Add event listener
  element.addEventListener('keydown', handleTabKey);

  // Return cleanup function
  return () => element.removeEventListener('keydown', handleTabKey);
};

/**
 * Announce message to screen readers
 */
export const announceToScreenReader = (message: string, priority: 'polite' | 'assertive' = 'polite') => {
  const announcement = document.createElement('div');
  announcement.setAttribute('role', 'status');
  announcement.setAttribute('aria-live', priority);
  announcement.setAttribute('aria-atomic', 'true');
  announcement.className = 'sr-only';
  announcement.textContent = message;

  document.body.appendChild(announcement);

  // Remove after announcement
  setTimeout(() => {
    document.body.removeChild(announcement);
  }, 1000);
};

/**
 * Get ARIA label for common elements
 */
export const getAriaLabel = (element: string, context?: string): string => {
  const labels: Record<string, string> = {
    'close': 'סגור',
    'menu': 'תפריט',
    'search': 'חיפוש',
    'filter': 'סינון',
    'sort': 'מיון',
    'upload': 'העלאת קבלה',
    'delete': 'מחיקה',
    'edit': 'עריכה',
    'save': 'שמירה',
    'cancel': 'ביטול',
    'back': 'חזרה',
    'next': 'הבא',
    'previous': 'הקודם',
    'first': 'ראשון',
    'last': 'אחרון',
    'home': 'דף הבית',
    'logout': 'התנתקות',
    'settings': 'הגדרות',
    'profile': 'פרופיל',
    'help': 'עזרה',
    'more': 'עוד'
  };

  const label = labels[element] || element;
  return context ? `${label} - ${context}` : label;
};

/**
 * Check if element is visible on screen (for lazy loading)
 */
export const isElementInViewport = (element: HTMLElement): boolean => {
  const rect = element.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
};

/**
 * Check if user prefers reduced motion
 */
export const prefersReducedMotion = (): boolean => {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
};

/**
 * Check if user prefers high contrast
 */
export const prefersHighContrast = (): boolean => {
  return window.matchMedia('(prefers-contrast: high)').matches;
};

/**
 * Validate color contrast ratio (WCAG AA requires 4.5:1 for normal text)
 */
export const getContrastRatio = (foreground: string, background: string): number => {
  // Simplified contrast calculation
  // In production, use a library like 'color-contrast-checker'
  const getLuminance = (hex: string): number => {
    const rgb = parseInt(hex.slice(1), 16);
    const r = (rgb >> 16) & 0xff;
    const g = (rgb >> 8) & 0xff;
    const b = (rgb >> 0) & 0xff;
    
    const rsRGB = r / 255;
    const gsRGB = g / 255;
    const bsRGB = b / 255;
    
    const rLin = rsRGB <= 0.03928 ? rsRGB / 12.92 : Math.pow((rsRGB + 0.055) / 1.055, 2.4);
    const gLin = gsRGB <= 0.03928 ? gsRGB / 12.92 : Math.pow((gsRGB + 0.055) / 1.055, 2.4);
    const bLin = bsRGB <= 0.03928 ? bsRGB / 12.92 : Math.pow((bsRGB + 0.055) / 1.055, 2.4);
    
    return 0.2126 * rLin + 0.7152 * gLin + 0.0722 * bLin;
  };

  const l1 = getLuminance(foreground);
  const l2 = getLuminance(background);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  
  return (lighter + 0.05) / (darker + 0.05);
};
