/**
 * Header Component - Demo Usage Examples
 * 
 * This file demonstrates various ways to use the Header component system.
 * Copy these examples into your application as needed.
 */

import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Header } from './Header';

// ============================================================
// EXAMPLE 1: Basic Usage (Most Common)
// ============================================================

export function BasicHeaderExample() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main id="main-content" className="container mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold">דף הבית</h1>
        <p className="mt-4">תוכן הדף שלך כאן...</p>
      </main>
    </div>
  );
}

// ============================================================
// EXAMPLE 2: With Custom Styling
// ============================================================

export function StyledHeaderExample() {
  return (
    <div className="min-h-screen">
      <Header className="shadow-lg border-b-2 border-primary-600" />
      <main id="main-content" className="p-8">
        <h1>דף עם עיצוב מותאם</h1>
      </main>
    </div>
  );
}

// ============================================================
// EXAMPLE 3: Full Application Layout
// ============================================================

export function FullLayoutExample() {
  return (
    <BrowserRouter>
      <div className="flex flex-col min-h-screen">
        {/* Header - Sticky at top */}
        <Header />

        {/* Main Content Area */}
        <main id="main-content" className="flex-1 bg-gray-50">
          <Routes>
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/archive" element={<ArchivePage />} />
            <Route path="/export" element={<ExportPage />} />
            <Route path="/profile" element={<ProfilePage />} />
          </Routes>
        </main>

        {/* Optional Footer */}
        <footer className="bg-white border-t border-gray-200 py-4 px-6">
          <p className="text-center text-sm text-gray-600">
            © 2025 Tik-Tax. כל הזכויות שמורות.
          </p>
        </footer>
      </div>
    </BrowserRouter>
  );
}

// ============================================================
// EXAMPLE 4: With Page Transition
// ============================================================

export function AnimatedLayoutExample() {
  return (
    <div className="min-h-screen">
      <Header />
      <main 
        id="main-content" 
        className="transition-opacity duration-200"
      >
        {/* Your routed content with transitions */}
      </main>
    </div>
  );
}

// ============================================================
// EXAMPLE 5: Conditional Header (Hide on specific pages)
// ============================================================

export function ConditionalHeaderExample() {
  const location = window.location.pathname;
  const hideHeaderRoutes = ['/login', '/signup', '/onboarding'];
  const shouldShowHeader = !hideHeaderRoutes.includes(location);

  return (
    <div className="min-h-screen">
      {shouldShowHeader && <Header />}
      <main id="main-content">
        {/* Your content */}
      </main>
    </div>
  );
}

// ============================================================
// EXAMPLE 6: With Protected Routes
// ============================================================

export function ProtectedLayoutExample() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes - No header */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />

        {/* Protected routes - With header */}
        <Route
          path="/*"
          element={
            <ProtectedLayout>
              <Routes>
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route path="/archive" element={<ArchivePage />} />
                <Route path="/export" element={<ExportPage />} />
                <Route path="/profile" element={<ProfilePage />} />
              </Routes>
            </ProtectedLayout>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

function ProtectedLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen">
      <Header />
      <main id="main-content" className="bg-gray-50">
        {children}
      </main>
    </div>
  );
}

// ============================================================
// EXAMPLE 7: Standalone Components Usage
// ============================================================

import { UserDropdown } from './UserDropdown';
import { MobileMenu } from './MobileMenu';

export function StandaloneComponentsExample() {
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);

  return (
    <div>
      {/* Use UserDropdown independently */}
      <div className="p-4 bg-white">
        <UserDropdown />
      </div>

      {/* Use MobileMenu independently */}
      <button onClick={() => setMobileMenuOpen(true)}>
        פתח תפריט
      </button>
      <MobileMenu 
        isOpen={mobileMenuOpen} 
        onClose={() => setMobileMenuOpen(false)} 
      />
    </div>
  );
}

// ============================================================
// Mock Pages for Examples
// ============================================================

function DashboardPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900">לוח בקרה</h1>
      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h2 className="text-lg font-semibold">קבלות החודש</h2>
          <p className="text-3xl font-bold text-primary-600 mt-2">24</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h2 className="text-lg font-semibold">סך הוצאות</h2>
          <p className="text-3xl font-bold text-primary-600 mt-2">₪8,450</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h2 className="text-lg font-semibold">ממתין לאישור</h2>
          <p className="text-3xl font-bold text-yellow-600 mt-2">3</p>
        </div>
      </div>
    </div>
  );
}

function ArchivePage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900">ארכיון קבלות</h1>
      <p className="mt-4 text-gray-600">כל הקבלות שלך במקום אחד</p>
    </div>
  );
}

function ExportPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900">ייצוא נתונים</h1>
      <p className="mt-4 text-gray-600">ייצא את הנתונים שלך לאקסל</p>
    </div>
  );
}

function ProfilePage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900">פרופיל משתמש</h1>
      <p className="mt-4 text-gray-600">ניהול הפרטים האישיים שלך</p>
    </div>
  );
}

function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
        <h1 className="text-2xl font-bold text-center">התחברות</h1>
        <p className="mt-2 text-center text-gray-600">ברוך הבא ל-Tik-Tax</p>
      </div>
    </div>
  );
}

function SignupPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
        <h1 className="text-2xl font-bold text-center">הרשמה</h1>
        <p className="mt-2 text-center text-gray-600">צור חשבון חדש</p>
      </div>
    </div>
  );
}

// ============================================================
// USAGE IN YOUR APP.TSX
// ============================================================

/**
 * Copy this structure to your main App.tsx:
 * 
 * ```tsx
 * import { Header } from '@/components/layout';
 * 
 * function App() {
 *   return (
 *     <BrowserRouter>
 *       <div className="min-h-screen">
 *         <Header />
 *         <main id="main-content" className="bg-gray-50">
 *           <Routes>
 *             // Your routes here
 *           </Routes>
 *         </main>
 *       </div>
 *     </BrowserRouter>
 *   );
 * }
 * ```
 */

export default BasicHeaderExample;
