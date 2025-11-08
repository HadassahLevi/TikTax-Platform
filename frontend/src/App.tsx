import './App.css';
import { Suspense, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { SubscriptionPage, CheckoutSuccessPage, CheckoutCancelPage } from './pages';
import { NotificationDemo } from './pages/NotificationDemo';
import { NotFoundPage, ServerErrorPage, NetworkErrorPage, MaintenancePage } from './pages/errors';
import { ToastProvider } from './contexts/ToastContext';
import { LoadingSpinner } from './components/loading/LoadingSpinner';
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts';
import { initBrowserFixes } from '@/utils/browserFixes';

// Lazy load route components for code splitting
// Uncomment when these routes are active:
// const DashboardPage = React.lazy(() => import('./pages/dashboard/DashboardPage'));
// const ArchivePage = React.lazy(() => import('./pages/receipts/ArchivePage'));
// const ProfilePage = React.lazy(() => import('./pages/ProfilePage'));
// const ExportPage = React.lazy(() => import('./pages/ExportPage'));

// Suspense fallback component
const PageLoader = () => (
  <div className="min-h-screen flex items-center justify-center bg-gray-50">
    <LoadingSpinner size="lg" text="טוען עמוד..." />
  </div>
);

function App() {
  // Initialize keyboard shortcuts
  useKeyboardShortcuts();

  // Initialize browser fixes
  useEffect(() => {
    initBrowserFixes();
  }, []);

  return (
    <ToastProvider>
      <BrowserRouter>
        <Suspense fallback={<PageLoader />}>
          <Routes>
            <Route path="/" element={<SubscriptionPage />} />
            <Route path="/checkout/success" element={<CheckoutSuccessPage />} />
            <Route path="/checkout/cancel" element={<CheckoutCancelPage />} />
            <Route path="/notification-demo" element={<NotificationDemo />} />
            
            {/* Error Pages */}
            <Route path="/error/500" element={<ServerErrorPage />} />
            <Route path="/error/network" element={<NetworkErrorPage />} />
            <Route path="/maintenance" element={<MaintenancePage />} />
            
            {/* 
            TODO: Uncomment when implementing full routing:
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/archive" element={<ArchivePage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/export" element={<ExportPage />} />
            */}
            
            {/* 404 Fallback - must be last */}
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </Suspense>
      </BrowserRouter>
    </ToastProvider>
  );
}

export default App;
