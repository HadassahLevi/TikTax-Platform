import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

interface ShortcutConfig {
  key: string;
  ctrlOrCmd?: boolean;
  shift?: boolean;
  alt?: boolean;
  description: string;
  action: () => void;
}

export const useKeyboardShortcuts = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Detect Mac vs Windows/Linux
      const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
      const ctrlOrCmd = isMac ? e.metaKey : e.ctrlKey;

      // Don't trigger shortcuts when typing in inputs
      const activeElement = document.activeElement;
      const isTyping = activeElement && (
        activeElement.tagName === 'INPUT' ||
        activeElement.tagName === 'TEXTAREA' ||
        (activeElement as HTMLElement).isContentEditable
      );

      // Ctrl/Cmd + K: Focus search (works even when typing)
      if (ctrlOrCmd && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector<HTMLInputElement>('[data-search-input]');
        if (searchInput) {
          searchInput.focus();
          searchInput.select();
        }
        return;
      }

      // Skip other shortcuts if typing
      if (isTyping) return;

      // Ctrl/Cmd + U: Upload receipt
      if (ctrlOrCmd && e.key === 'u') {
        e.preventDefault();
        navigate('/upload');
        return;
      }

      // Ctrl/Cmd + E: Go to export page
      if (ctrlOrCmd && e.key === 'e') {
        e.preventDefault();
        navigate('/export');
        return;
      }

      // Ctrl/Cmd + D: Go to dashboard
      if (ctrlOrCmd && e.key === 'd') {
        e.preventDefault();
        navigate('/dashboard');
        return;
      }

      // Ctrl/Cmd + H: Go to help/FAQ
      if (ctrlOrCmd && e.key === 'h') {
        e.preventDefault();
        navigate('/help');
        return;
      }

      // Ctrl/Cmd + ,: Go to settings
      if (ctrlOrCmd && e.key === ',') {
        e.preventDefault();
        navigate('/profile');
        return;
      }

      // /: Focus search (alternative, Gmail-style)
      if (e.key === '/') {
        e.preventDefault();
        const searchInput = document.querySelector<HTMLInputElement>('[data-search-input]');
        if (searchInput) {
          searchInput.focus();
          searchInput.select();
        }
        return;
      }

      // ?: Show keyboard shortcuts help
      if (e.shiftKey && e.key === '?') {
        e.preventDefault();
        document.dispatchEvent(new CustomEvent('showKeyboardShortcuts'));
        return;
      }

      // ESC: Close modals/dropdowns/overlays
      if (e.key === 'Escape') {
        document.dispatchEvent(new CustomEvent('closeModals'));
        return;
      }

      // Arrow navigation in lists (when list is focused)
      if (activeElement?.hasAttribute('data-list-item')) {
        if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
          e.preventDefault();
          const items = Array.from(document.querySelectorAll('[data-list-item]'));
          const currentIndex = items.indexOf(activeElement);
          
          if (e.key === 'ArrowDown' && currentIndex < items.length - 1) {
            (items[currentIndex + 1] as HTMLElement).focus();
          } else if (e.key === 'ArrowUp' && currentIndex > 0) {
            (items[currentIndex - 1] as HTMLElement).focus();
          }
          return;
        }

        // Enter: Activate focused list item
        if (e.key === 'Enter') {
          e.preventDefault();
          (activeElement as HTMLElement).click();
          return;
        }
      }
    };

    // Add event listener
    window.addEventListener('keydown', handleKeyDown);

    // Cleanup
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [navigate]);
};

// Keyboard shortcuts configuration for reference
export const KEYBOARD_SHORTCUTS: ShortcutConfig[] = [
  {
    key: 'K',
    ctrlOrCmd: true,
    description: 'פתח חיפוש',
    action: () => {}
  },
  {
    key: 'U',
    ctrlOrCmd: true,
    description: 'העלה קבלה חדשה',
    action: () => {}
  },
  {
    key: 'E',
    ctrlOrCmd: true,
    description: 'עבור לעמוד ייצוא',
    action: () => {}
  },
  {
    key: 'D',
    ctrlOrCmd: true,
    description: 'עבור לדשבורד',
    action: () => {}
  },
  {
    key: 'H',
    ctrlOrCmd: true,
    description: 'עזרה ותמיכה',
    action: () => {}
  },
  {
    key: ',',
    ctrlOrCmd: true,
    description: 'הגדרות',
    action: () => {}
  },
  {
    key: '/',
    ctrlOrCmd: false,
    description: 'חיפוש מהיר',
    action: () => {}
  },
  {
    key: '?',
    shift: true,
    description: 'הצג קיצורי מקלדת',
    action: () => {}
  },
  {
    key: 'ESC',
    ctrlOrCmd: false,
    description: 'סגור חלונות ותפריטים',
    action: () => {}
  },
  {
    key: '↑↓',
    ctrlOrCmd: false,
    description: 'נווט ברשימות',
    action: () => {}
  }
];
