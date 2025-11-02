import React, { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { User, Settings, LogOut, ChevronDown } from 'lucide-react';
import { cn, getInitials } from '@/utils/formatters';
import { useAuthStore } from '@/stores/auth.store';

interface DropdownItem {
  label: string;
  icon: React.ReactNode;
  href?: string;
  onClick?: () => void;
  variant?: 'default' | 'danger';
  divider?: boolean;
}

interface UserDropdownProps {
  className?: string;
}

/**
 * User Avatar Dropdown Component
 * 
 * Features:
 * - Click to toggle dropdown (not hover for accessibility)
 * - Click outside to close
 * - ESC key to close
 * - Keyboard navigation with arrow keys
 * - Auto-positioning (below avatar, right-aligned for RTL)
 * 
 * @component
 */
export const UserDropdown: React.FC<UserDropdownProps> = ({ className }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  
  const { user, clearAuth } = useAuthStore();

  // Handle logout
  const handleLogout = () => {
    clearAuth();
    navigate('/login');
  };

  // Dropdown items configuration
  const dropdownItems: DropdownItem[] = [
    {
      label: 'פרופיל',
      icon: <User className="w-4 h-4" />,
      href: '/profile',
      variant: 'default',
    },
    {
      label: 'הגדרות',
      icon: <Settings className="w-4 h-4" />,
      href: '/settings',
      variant: 'default',
      divider: true, // Add divider after this item
    },
    {
      label: 'התנתק',
      icon: <LogOut className="w-4 h-4" />,
      onClick: handleLogout,
      variant: 'danger',
    },
  ];

  // Get user initials for avatar
  const initials = user 
    ? getInitials(user.firstName || 'U', user.lastName || 'U') 
    : 'TT';

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  // Close dropdown on ESC key
  useEffect(() => {
    const handleEscKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && isOpen) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscKey);
    }

    return () => {
      document.removeEventListener('keydown', handleEscKey);
    };
  }, [isOpen]);

  // Keyboard navigation in dropdown
  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (!isOpen) return;

    const items = dropdownRef.current?.querySelectorAll('[role="menuitem"]');
    if (!items || items.length === 0) return;

    const currentIndex = Array.from(items).findIndex(
      (item) => item === document.activeElement
    );

    switch (event.key) {
      case 'ArrowDown':
        event.preventDefault();
        const nextIndex = currentIndex < items.length - 1 ? currentIndex + 1 : 0;
        (items[nextIndex] as HTMLElement).focus();
        break;
      case 'ArrowUp':
        event.preventDefault();
        const prevIndex = currentIndex > 0 ? currentIndex - 1 : items.length - 1;
        (items[prevIndex] as HTMLElement).focus();
        break;
      case 'Enter':
      case ' ':
        event.preventDefault();
        (document.activeElement as HTMLElement).click();
        break;
    }
  };

  return (
    <div className={cn('relative', className)} ref={dropdownRef}>
      {/* Avatar Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={cn(
          'flex items-center gap-2 p-1 rounded-full transition-all duration-200',
          'hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-600 focus:ring-offset-2',
          isOpen && 'bg-gray-100'
        )}
        aria-label="תפריט משתמש"
        aria-expanded={isOpen}
        aria-haspopup="true"
      >
        {/* Avatar Circle */}
        <div
          className={cn(
            'w-10 h-10 rounded-full bg-gradient-to-br from-primary-500 to-primary-600',
            'flex items-center justify-center text-white font-semibold text-sm',
            'shadow-sm'
          )}
        >
          {initials}
        </div>

        {/* Chevron Icon (Desktop only) */}
        <ChevronDown
          className={cn(
            'w-4 h-4 text-gray-600 transition-transform duration-200',
            'hidden md:block',
            isOpen && 'rotate-180'
          )}
        />
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div
          className={cn(
            'absolute top-full mt-2 w-56',
            'bg-white rounded-lg shadow-lg border border-gray-200',
            'py-1 z-50',
            'animate-in fade-in slide-in-from-top-2 duration-200',
            // RTL positioning: left-aligned, LTR: right-aligned
            'ltr:right-0 rtl:left-0'
          )}
          role="menu"
          aria-orientation="vertical"
          onKeyDown={handleKeyDown}
        >
          {/* User Info Header */}
          {user && (
            <div className="px-4 py-3 border-b border-gray-100">
              <p className="text-sm font-semibold text-gray-900">
                {user.firstName} {user.lastName}
              </p>
              <p className="text-xs text-gray-500 truncate">
                {user.email}
              </p>
            </div>
          )}

          {/* Dropdown Items */}
          {dropdownItems.map((item, index) => (
            <React.Fragment key={index}>
              {item.href ? (
                <Link
                  to={item.href}
                  className={cn(
                    'flex items-center gap-3 px-4 py-2.5 text-sm transition-colors',
                    'hover:bg-gray-50 focus:bg-gray-50 focus:outline-none',
                    item.variant === 'danger'
                      ? 'text-red-600 hover:bg-red-50 focus:bg-red-50'
                      : 'text-gray-700'
                  )}
                  role="menuitem"
                  onClick={() => setIsOpen(false)}
                >
                  {item.icon}
                  <span>{item.label}</span>
                </Link>
              ) : (
                <button
                  onClick={() => {
                    item.onClick?.();
                    setIsOpen(false);
                  }}
                  className={cn(
                    'w-full flex items-center gap-3 px-4 py-2.5 text-sm transition-colors',
                    'hover:bg-gray-50 focus:bg-gray-50 focus:outline-none',
                    item.variant === 'danger'
                      ? 'text-red-600 hover:bg-red-50 focus:bg-red-50'
                      : 'text-gray-700'
                  )}
                  role="menuitem"
                >
                  {item.icon}
                  <span>{item.label}</span>
                </button>
              )}

              {/* Optional Divider */}
              {item.divider && (
                <div className="my-1 border-t border-gray-100" role="separator" />
              )}
            </React.Fragment>
          ))}
        </div>
      )}
    </div>
  );
};
