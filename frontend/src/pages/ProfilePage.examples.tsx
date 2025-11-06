/**
 * ProfilePage Integration Examples
 * 
 * This file demonstrates various ways to integrate and use the ProfilePage component
 * in different scenarios.
 */

import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { ProfilePage } from './ProfilePage';
import { useAuth } from '@/hooks/useAuth';
import { User, Settings } from 'lucide-react';

// ============================================================================
// EXAMPLE 1: Basic Router Integration
// ============================================================================

export function Example1_BasicRouterIntegration() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </BrowserRouter>
  );
}

// ============================================================================
// EXAMPLE 2: Protected Route Pattern
// ============================================================================

/**
 * Protected Route Wrapper
 * Redirects to login if user is not authenticated
 */
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();
  
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-600">טוען...</p>
        </div>
      </div>
    );
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
}

export function Example2_ProtectedRoutePattern() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <ProfilePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

// ============================================================================
// EXAMPLE 3: Header Integration with Profile Link
// ============================================================================

export function Example3_HeaderWithProfileLink() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [showDropdown, setShowDropdown] = React.useState(false);
  
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold text-primary-600">Tik-Tax</h1>
          </div>
          
          {/* User Menu */}
          <div className="relative">
            <button
              onClick={() => setShowDropdown(!showDropdown)}
              className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                <User className="text-primary-600" size={18} />
              </div>
              <span className="text-sm font-medium text-gray-900">
                {user?.fullName || 'משתמש'}
              </span>
            </button>
            
            {/* Dropdown Menu */}
            {showDropdown && (
              <div className="absolute left-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1">
                <button
                  onClick={() => {
                    navigate('/profile');
                    setShowDropdown(false);
                  }}
                  className="w-full px-4 py-2 text-right text-sm text-gray-700 hover:bg-gray-100 flex items-center gap-2"
                >
                  <Settings size={16} />
                  הגדרות חשבון
                </button>
                <hr className="my-1" />
                <button
                  onClick={async () => {
                    await logout();
                    setShowDropdown(false);
                  }}
                  className="w-full px-4 py-2 text-right text-sm text-red-600 hover:bg-red-50"
                >
                  התנתק
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}

// ============================================================================
// EXAMPLE 4: Navigate to Specific Tab
// ============================================================================

export function Example4_NavigateToSpecificTab() {
  const navigate = useNavigate();
  
  const handleOpenProfileSettings = () => {
    // Navigate to profile page with specific tab
    navigate('/profile', { state: { tab: 'profile' } });
  };
  
  const handleOpenSecuritySettings = () => {
    navigate('/profile', { state: { tab: 'security' } });
  };
  
  const handleOpenSubscriptionSettings = () => {
    navigate('/profile', { state: { tab: 'subscription' } });
  };
  
  return (
    <div className="space-y-4">
      <button
        onClick={handleOpenProfileSettings}
        className="px-4 py-2 bg-primary-600 text-white rounded-lg"
      >
        ערוך פרטים אישיים
      </button>
      
      <button
        onClick={handleOpenSecuritySettings}
        className="px-4 py-2 bg-gray-600 text-white rounded-lg"
      >
        שנה סיסמה
      </button>
      
      <button
        onClick={handleOpenSubscriptionSettings}
        className="px-4 py-2 bg-purple-600 text-white rounded-lg"
      >
        נהל מנוי
      </button>
    </div>
  );
}

// ============================================================================
// EXAMPLE 5: Usage Warning with Link to Subscription
// ============================================================================

export function Example5_UsageWarningWithLink() {
  const { usagePercentage, remainingReceipts } = useAuth();
  const navigate = useNavigate();
  
  const usage = usagePercentage();
  
  if (usage < 80) return null; // Don't show warning if usage is low
  
  return (
    <div className={`
      p-4 rounded-lg border flex items-start gap-3
      ${usage >= 100 
        ? 'bg-red-50 border-red-200' 
        : 'bg-yellow-50 border-yellow-200'
      }
    `}>
      <div className="flex-1">
        <h4 className="font-semibold text-gray-900 mb-1">
          {usage >= 100 ? 'הגעת למכסת הקבלות החודשית' : 'אזהרת שימוש'}
        </h4>
        <p className="text-sm text-gray-700">
          {usage >= 100 
            ? 'שדרג את התוכנית שלך כדי להמשיך להעלות קבלות.'
            : `נותרו ${remainingReceipts} קבלות בלבד החודש.`
          }
        </p>
      </div>
      <button
        onClick={() => navigate('/profile', { state: { tab: 'subscription' } })}
        className="px-4 py-2 bg-primary-600 text-white text-sm rounded-lg hover:bg-primary-700 transition-colors"
      >
        {usage >= 100 ? 'שדרג עכשיו' : 'צפה בשימוש'}
      </button>
    </div>
  );
}

// ============================================================================
// EXAMPLE 6: Bottom Navigation with Profile Link
// ============================================================================

export function Example6_BottomNavWithProfile() {
  const navigate = useNavigate();
  const location = window.location.pathname;
  
  const isActive = (path: string) => location === path;
  
  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 md:hidden">
      <div className="grid grid-cols-4 gap-1 px-2 py-2">
        <button
          onClick={() => navigate('/dashboard')}
          className={`
            flex flex-col items-center gap-1 px-3 py-2 rounded-lg transition-colors
            ${isActive('/dashboard') 
              ? 'text-primary-600 bg-primary-50' 
              : 'text-gray-600 hover:bg-gray-100'
            }
          `}
        >
          <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          <span className="text-xs font-medium">בית</span>
        </button>
        
        <button
          onClick={() => navigate('/archive')}
          className={`
            flex flex-col items-center gap-1 px-3 py-2 rounded-lg transition-colors
            ${isActive('/archive') 
              ? 'text-primary-600 bg-primary-50' 
              : 'text-gray-600 hover:bg-gray-100'
            }
          `}
        >
          <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
          </svg>
          <span className="text-xs font-medium">ארכיון</span>
        </button>
        
        <button
          onClick={() => navigate('/receipts/new')}
          className="flex flex-col items-center gap-1 px-3 py-2"
        >
          <div className="w-12 h-12 bg-primary-600 rounded-full flex items-center justify-center -mt-6 shadow-lg">
            <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
          </div>
        </button>
        
        <button
          onClick={() => navigate('/profile')}
          className={`
            flex flex-col items-center gap-1 px-3 py-2 rounded-lg transition-colors
            ${isActive('/profile') 
              ? 'text-primary-600 bg-primary-50' 
              : 'text-gray-600 hover:bg-gray-100'
            }
          `}
        >
          <User className="w-6 h-6" />
          <span className="text-xs font-medium">פרופיל</span>
        </button>
      </div>
    </nav>
  );
}

// ============================================================================
// EXAMPLE 7: Settings Page with Subsections
// ============================================================================

export function Example7_SettingsPageWithSubsections() {
  const navigate = useNavigate();
  
  const settingsSections = [
    {
      title: 'חשבון',
      items: [
        { label: 'פרטים אישיים', action: () => navigate('/profile', { state: { tab: 'profile' } }) },
        { label: 'אבטחה וסיסמה', action: () => navigate('/profile', { state: { tab: 'security' } }) },
        { label: 'מנוי ותשלום', action: () => navigate('/profile', { state: { tab: 'subscription' } }) },
      ]
    },
    {
      title: 'העדפות',
      items: [
        { label: 'התראות', action: () => navigate('/settings/notifications') },
        { label: 'שפה', action: () => navigate('/settings/language') },
        { label: 'תצוגה', action: () => navigate('/settings/appearance') },
      ]
    },
  ];
  
  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">הגדרות</h1>
      
      <div className="space-y-6">
        {settingsSections.map((section) => (
          <div key={section.title} className="bg-white rounded-lg border border-gray-200 overflow-hidden">
            <h2 className="px-4 py-3 bg-gray-50 font-semibold text-gray-900 border-b">
              {section.title}
            </h2>
            <div className="divide-y">
              {section.items.map((item) => (
                <button
                  key={item.label}
                  onClick={item.action}
                  className="w-full px-4 py-3 text-right hover:bg-gray-50 transition-colors flex items-center justify-between"
                >
                  <span className="text-gray-900">{item.label}</span>
                  <svg className="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ============================================================================
// EXAMPLE 8: Onboarding Prompt for Profile Completion
// ============================================================================

export function Example8_ProfileCompletionPrompt() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [isDismissed, setIsDismissed] = React.useState(false);
  
  // Check if profile is incomplete
  const isProfileIncomplete = !user?.fullName || !user?.businessName || !user?.phone;
  
  if (!isProfileIncomplete || isDismissed) return null;
  
  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1">
          <h4 className="font-semibold text-blue-900 mb-1">
            השלם את הפרטים שלך
          </h4>
          <p className="text-sm text-blue-700 mb-3">
            מילוי הפרטים האישיים והעסקיים יעזור לנו לספק לך חוויה טובה יותר.
          </p>
          <button
            onClick={() => navigate('/profile')}
            className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors"
          >
            השלם עכשיו
          </button>
        </div>
        <button
          onClick={() => setIsDismissed(true)}
          className="text-blue-600 hover:text-blue-800"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  );
}

// ============================================================================
// MOCK COMPONENTS FOR EXAMPLES
// ============================================================================

function DashboardPage() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold">לוח בקרה</h1>
      <Example5_UsageWarningWithLink />
      <Example8_ProfileCompletionPrompt />
    </div>
  );
}

function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-lg shadow-lg">
        <h1 className="text-2xl font-bold mb-4">התחברות</h1>
        <p className="text-gray-600">טופס התחברות כאן...</p>
      </div>
    </div>
  );
}

// ============================================================================
// EXPORT ALL EXAMPLES
// ============================================================================

export default {
  Example1_BasicRouterIntegration,
  Example2_ProtectedRoutePattern,
  Example3_HeaderWithProfileLink,
  Example4_NavigateToSpecificTab,
  Example5_UsageWarningWithLink,
  Example6_BottomNavWithProfile,
  Example7_SettingsPageWithSubsections,
  Example8_ProfileCompletionPrompt,
};
