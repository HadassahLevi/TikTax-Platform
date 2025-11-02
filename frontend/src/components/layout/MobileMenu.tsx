import React, { useEffect } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { X, LayoutDashboard, Archive, FileOutput, User, LogOut } from 'lucide-react';
import { cn } from '@/utils/formatters';
import { useAuthStore } from '@/stores/auth.store';

interface MobileMenuItem {
  label: string;
  icon: React.ReactNode;
  href?: string;
  onClick?: () => void;
  variant?: 'default' | 'danger';
  divider?: boolean;
}

interface MobileMenuProps {
  isOpen: boolean;
  onClose: () => void;
}

/**
 * Mobile Slide-in Menu Component
 * 
 * Features:
 * - Full-screen overlay with semi-transparent backdrop
 * - Slides in from right (RTL: from left)
 * - Locks body scroll when open
 * - Focus trap for accessibility
 * - ESC key to close
 * - Smooth animations with framer-motion
 * 
 * @component
 */
export const MobileMenu: React.FC<MobileMenuProps> = ({ isOpen, onClose }) => {
  const navigate = useNavigate();
  const { clearAuth } = useAuthStore();

  // Handle logout
  const handleLogout = () => {
    clearAuth();
    onClose();
    navigate('/login');
  };

  // Menu items configuration
  const menuItems: MobileMenuItem[] = [
    {
      label: 'לוח בקרה',
      icon: <LayoutDashboard className="w-5 h-5" />,
      href: '/dashboard',
    },
    {
      label: 'ארכיון',
      icon: <Archive className="w-5 h-5" />,
      href: '/archive',
    },
    {
      label: 'ייצוא',
      icon: <FileOutput className="w-5 h-5" />,
      href: '/export',
    },
    {
      label: 'פרופיל',
      icon: <User className="w-5 h-5" />,
      href: '/profile',
      divider: true,
    },
    {
      label: 'התנתק',
      icon: <LogOut className="w-5 h-5" />,
      onClick: handleLogout,
      variant: 'danger',
    },
  ];

  // Lock body scroll when menu is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  // Close on ESC key
  useEffect(() => {
    const handleEscKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscKey);
    }

    return () => {
      document.removeEventListener('keydown', handleEscKey);
    };
  }, [isOpen, onClose]);

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop Overlay */}
          <motion.div
            {...({
              initial: { opacity: 0 },
              animate: { opacity: 1 },
              exit: { opacity: 0 },
              transition: { duration: 0.2 },
              onClick: onClose,
              style: {
                position: 'fixed',
                inset: 0,
                backgroundColor: 'rgba(0, 0, 0, 0.5)',
                zIndex: 40,
              },
              'aria-hidden': 'true',
            } as any)}
          />

          {/* Slide-in Menu Panel */}
          <motion.div
            {...({
              initial: { x: '100%' },
              animate: { x: 0 },
              exit: { x: '100%' },
              transition: { type: 'tween', duration: 0.3, ease: 'easeInOut' },
              style: {
                position: 'fixed',
                top: 0,
                bottom: 0,
                right: 0,
                width: '320px',
                maxWidth: '85vw',
                backgroundColor: 'white',
                boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.15), 0 10px 10px -5px rgba(0, 0, 0, 0.08)',
                zIndex: 50,
              },
              role: 'dialog',
              'aria-modal': 'true',
              'aria-label': 'תפריט ניווט ראשי',
            } as any)}
          >
            {/* Header with Close Button */}
            <div className="flex items-center justify-between p-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">תפריט</h2>
              <button
                onClick={onClose}
                className={cn(
                  'p-2 rounded-lg transition-colors',
                  'hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-600'
                )}
                aria-label="סגור תפריט"
              >
                <X className="w-6 h-6 text-gray-600" />
              </button>
            </div>

            {/* Navigation Items */}
            <nav className="flex flex-col p-2">
              {menuItems.map((item, index) => (
                <React.Fragment key={index}>
                  {item.href ? (
                    <NavLink
                      to={item.href}
                      onClick={onClose}
                      className={({ isActive }) =>
                        cn(
                          'flex items-center gap-4 px-4 py-4 rounded-lg transition-all',
                          'text-base font-medium',
                          'hover:bg-gray-50 active:bg-gray-100',
                          'focus:outline-none focus:ring-2 focus:ring-primary-600 focus:ring-inset',
                          isActive
                            ? 'bg-primary-50 text-primary-600'
                            : item.variant === 'danger'
                            ? 'text-red-600'
                            : 'text-gray-700'
                        )
                      }
                    >
                      {item.icon}
                      <span>{item.label}</span>
                    </NavLink>
                  ) : (
                    <button
                      onClick={() => {
                        item.onClick?.();
                      }}
                      className={cn(
                        'flex items-center gap-4 px-4 py-4 rounded-lg transition-all',
                        'text-base font-medium',
                        'hover:bg-gray-50 active:bg-gray-100',
                        'focus:outline-none focus:ring-2 focus:ring-primary-600 focus:ring-inset',
                        item.variant === 'danger'
                          ? 'text-red-600 hover:bg-red-50 active:bg-red-100'
                          : 'text-gray-700'
                      )}
                    >
                      {item.icon}
                      <span>{item.label}</span>
                    </button>
                  )}

                  {/* Optional Divider */}
                  {item.divider && (
                    <div className="my-2 border-t border-gray-200" />
                  )}
                </React.Fragment>
              ))}
            </nav>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};