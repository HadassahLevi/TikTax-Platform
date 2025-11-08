import React, { useState } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { Menu, Receipt } from 'lucide-react';
import { cn } from '@/utils/formatters';
import { UserDropdown } from './UserDropdown';
import { MobileMenu } from './MobileMenu';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { KeyboardShortcutsModal } from '@/components/KeyboardShortcutsModal';
import { NotificationCenter } from '@/components/NotificationCenter';

interface NavigationItem {
  label: string;
  href: string;
  key: string;
}

interface HeaderProps {
  className?: string;
}

/**
 * Responsive Header Component
 * 
 * Features:
 * - Sticky positioned at top with shadow
 * - Desktop: Full navigation menu + user dropdown
 * - Mobile: Hamburger menu + logo + avatar
 * - Active route highlighting
 * - RTL support (logo on right, menu on left)
 * - Skip to main content link for accessibility
 * 
 * Desktop Layout (>768px):
 * ┌─────────────────────────────────────────────────────────┐
 * │  [Logo]    [Dashboard] [Archive] [Export]      [Avatar▼]│
 * └─────────────────────────────────────────────────────────┘
 * 
 * Mobile Layout (<768px):
 * ┌─────────────────────────────────────────────────────────┐
 * │  [☰]                [Logo]                      [Avatar]│
 * └─────────────────────────────────────────────────────────┘
 * 
 * @component
 */
export const Header: React.FC<HeaderProps> = ({ className }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // Navigation items configuration
  const navigationItems: NavigationItem[] = [
    { label: 'לוח בקרה', href: '/dashboard', key: 'dashboard' },
    { label: 'ארכיון', href: '/archive', key: 'archive' },
    { label: 'ייצוא', href: '/export', key: 'export' },
    { label: 'פרופיל', href: '/profile', key: 'profile' },
  ];

  return (
    <>
      {/* Skip to Main Content Link (Accessibility) */}
      <a
        href="#main-content"
        className={cn(
          'sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4',
          'bg-primary-600 text-white px-4 py-2 rounded-lg z-50',
          'focus:outline-none focus:ring-2 focus:ring-primary-600 focus:ring-offset-2'
        )}
      >
        דלג לתוכן הראשי
      </a>

      {/* Header Container */}
      <header
        className={cn(
          'sticky top-0 z-40',
          'bg-white border-b border-gray-200 shadow-sm',
          'transition-shadow duration-200',
          className
        )}
      >
        <div className="max-w-screen-2xl mx-auto px-4 md:px-6 lg:px-8">
          {/* Breadcrumbs */}
          <Breadcrumbs />
          
          <div className="flex items-center justify-between h-16">
          {/* Left Section (RTL: Right Section) - Logo + Desktop Nav */}
          <div className="flex items-center gap-8">
            {/* Logo */}
            <Link
              to="/dashboard"
              className={cn(
                'flex items-center gap-2',
                'focus:outline-none focus:ring-2 focus:ring-primary-600 focus:ring-offset-2 rounded-lg',
                'transition-opacity hover:opacity-80'
              )}
              aria-label="Tik-Tax - חזרה לדף הבית"
            >
              <Receipt className="w-7 h-7 text-primary-600" aria-hidden="true" />
              <span
                className="text-2xl font-bold text-primary-600"
                style={{ fontFamily: 'Rubik, sans-serif' }}
              >
                Tik-Tax
              </span>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center gap-1" aria-label="ניווט ראשי">
              {navigationItems.map((item) => (
                <NavLink
                  key={item.key}
                  to={item.href}
                  className={({ isActive }) =>
                    cn(
                      'relative px-4 py-2 rounded-lg text-sm font-medium transition-all',
                      'hover:text-primary-600 hover:bg-primary-50',
                      'focus:outline-none focus:ring-2 focus:ring-primary-600 focus:ring-inset',
                      isActive
                        ? 'text-primary-600'
                        : 'text-gray-700'
                    )
                  }
                >
                  {({ isActive }) => (
                    <>
                      <span>{item.label}</span>
                      {/* Active Underline */}
                      {isActive && (
                        <span
                          className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary-600 rounded-full"
                          aria-hidden="true"
                        />
                      )}
                    </>
                  )}
                </NavLink>
              ))}
            </nav>
          </div>

          {/* Right Section (RTL: Left Section) - Actions + User */}
          <div className="flex items-center gap-2">
            {/* Keyboard Shortcuts Button (Desktop Only) */}
            <div className="hidden md:block">
              <KeyboardShortcutsModal />
            </div>
            
            {/* Notification Center */}
            <NotificationCenter />
            
            {/* Mobile Hamburger Menu Button */}
            <button
              onClick={() => setIsMobileMenuOpen(true)}
              className={cn(
                'md:hidden p-2 rounded-lg transition-colors',
                'hover:bg-gray-100 active:bg-gray-200',
                'focus:outline-none focus:ring-2 focus:ring-primary-600'
              )}
              aria-label="פתח תפריט ניווט"
              aria-expanded={isMobileMenuOpen}
            >
              <Menu className="w-6 h-6 text-gray-700" />
            </button>

            {/* User Avatar Dropdown */}
            <UserDropdown />
          </div>
        </div>
        </div>
      </header>

      {/* Mobile Menu (Slide-in Panel) */}
      <MobileMenu
        isOpen={isMobileMenuOpen}
        onClose={() => setIsMobileMenuOpen(false)}
      />
    </>
  );
};
