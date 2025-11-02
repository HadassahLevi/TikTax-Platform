import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, FolderOpen, Plus, Download, User } from 'lucide-react';
import { cn } from '@/utils/formatters';

interface NavItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  route?: string;
  onClick?: () => void;
  isCenter?: boolean;
}

interface BottomNavProps {
  onExportClick?: () => void;
  className?: string;
}

/**
 * Mobile-Only Bottom Navigation Bar
 * 
 * Features:
 * - Visible only on mobile/tablet (<768px)
 * - Elevated center button for primary action (Add Receipt)
 * - Active route highlighting
 * - Touch-friendly 48px targets
 * - iOS safe area support
 * - Smooth transitions
 * 
 * Navigation Items:
 * - Home (Dashboard)
 * - Archive
 * - Add Receipt (elevated center button)
 * - Export (modal trigger)
 * - Profile
 * 
 * @component
 */
export const BottomNav: React.FC<BottomNavProps> = ({ 
  onExportClick, 
  className 
}) => {
  const location = useLocation();

  // Check if route is active
  const isActive = (route: string): boolean => {
    return location.pathname === route;
  };

  // Navigation items configuration
  const navItems: NavItem[] = [
    {
      id: 'home',
      label: 'בית',
      icon: <Home className="w-6 h-6" />,
      route: '/dashboard',
    },
    {
      id: 'archive',
      label: 'ארכיון',
      icon: <FolderOpen className="w-6 h-6" />,
      route: '/archive',
    },
    {
      id: 'add-receipt',
      label: '', // No label for center button
      icon: <Plus className="w-7 h-7" />,
      route: '/receipts/new',
      isCenter: true,
    },
    {
      id: 'export',
      label: 'ייצוא',
      icon: <Download className="w-6 h-6" />,
      onClick: onExportClick,
    },
    {
      id: 'profile',
      label: 'פרופיל',
      icon: <User className="w-6 h-6" />,
      route: '/profile',
    },
  ];

  return (
    <nav
      className={cn(
        // Base positioning - fixed at bottom, full width
        'fixed bottom-0 left-0 right-0 z-50',
        // Height and layout
        'h-16',
        // Styling
        'bg-white border-t border-gray-200',
        'shadow-[0_-2px_8px_rgba(0,0,0,0.08)]',
        // iOS safe area support
        'pb-[env(safe-area-inset-bottom)]',
        // Responsive - hide on desktop (≥768px)
        'md:hidden',
        className
      )}
      role="navigation"
      aria-label="ניווט ראשי"
    >
      {/* Navigation Container */}
      <div className="h-full flex items-center justify-around px-2 relative">
        {navItems.map((item) => {
          const active = item.route ? isActive(item.route) : false;

          // Center button (Add Receipt) - elevated and special styling
          if (item.isCenter) {
            return (
              <Link
                key={item.id}
                to={item.route!}
                className={cn(
                  // Positioning - absolute to elevate above nav bar
                  'absolute left-1/2 -translate-x-1/2 -top-5',
                  // Size
                  'w-16 h-16',
                  // Styling - gradient background with shadow
                  'bg-gradient-to-br from-primary-600 to-primary-700',
                  'rounded-full',
                  'shadow-[0_4px_12px_rgba(37,99,235,0.4)]',
                  // Flex layout for icon centering
                  'flex items-center justify-center',
                  // Text color
                  'text-white',
                  // Transitions and interactions
                  'transition-all duration-200 ease-in-out',
                  'hover:scale-105 active:scale-95',
                  'focus:outline-none focus:ring-2 focus:ring-primary-600 focus:ring-offset-2',
                  // Touch target enhancement
                  'touch-manipulation'
                )}
                aria-label="הוסף קבלה חדשה"
                role="button"
              >
                {item.icon}
              </Link>
            );
          }

          // Regular navigation items
          if (item.route) {
            return (
              <Link
                key={item.id}
                to={item.route}
                className={cn(
                  // Layout - column with icon above label
                  'flex flex-col items-center justify-center gap-1',
                  // Sizing - minimum touch target 48px
                  'min-w-[48px] min-h-[48px] px-3 py-2',
                  // Text styling
                  'text-xs font-medium',
                  // Colors - conditional based on active state
                  active 
                    ? 'text-primary-600' 
                    : 'text-gray-500',
                  // Transitions
                  'transition-colors duration-200',
                  // Hover state (non-active items)
                  !active && 'hover:text-gray-700',
                  // Focus state
                  'focus:outline-none focus:text-primary-600',
                  // Touch enhancement
                  'touch-manipulation'
                )}
                aria-label={item.label}
                aria-current={active ? 'page' : undefined}
              >
                {/* Icon */}
                <div className={cn(
                  'transition-transform duration-200',
                  active && 'scale-110'
                )}>
                  {item.icon}
                </div>

                {/* Label */}
                {item.label && (
                  <span className={cn(
                    'transition-all duration-200',
                    active && 'font-semibold'
                  )}>
                    {item.label}
                  </span>
                )}
              </Link>
            );
          }

          // Button items (e.g., Export)
          return (
            <button
              key={item.id}
              onClick={item.onClick}
              className={cn(
                // Layout - column with icon above label
                'flex flex-col items-center justify-center gap-1',
                // Sizing - minimum touch target 48px
                'min-w-[48px] min-h-[48px] px-3 py-2',
                // Text styling
                'text-xs font-medium',
                // Colors - conditional based on active state
                active 
                  ? 'text-primary-600' 
                  : 'text-gray-500',
                // Transitions
                'transition-colors duration-200',
                // Hover state (non-active items)
                !active && 'hover:text-gray-700',
                // Focus state
                'focus:outline-none focus:text-primary-600',
                // Touch enhancement
                'touch-manipulation'
              )}
              aria-label={item.label}
              role="button"
            >
              {/* Icon */}
              <div className="transition-transform duration-200">
                {item.icon}
              </div>

              {/* Label */}
              {item.label && (
                <span className="transition-all duration-200">
                  {item.label}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
};