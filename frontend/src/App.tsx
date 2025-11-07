import './App.css';
import { Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { SubscriptionPage, CheckoutSuccessPage, CheckoutCancelPage } from './pages';
import { NotificationDemo } from './pages/NotificationDemo';
import { ToastProvider } from './contexts/ToastContext';
import { LoadingSpinner } from './components/loading/LoadingSpinner';

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

// TEMPORARY: Showing SubscriptionPage for testing
// TODO: Revert to original welcome screen after testing
function App() {
  return (
    <ToastProvider>
      <BrowserRouter>
        <Suspense fallback={<PageLoader />}>
          <Routes>
            <Route path="/" element={<SubscriptionPage />} />
            <Route path="/checkout/success" element={<CheckoutSuccessPage />} />
            <Route path="/checkout/cancel" element={<CheckoutCancelPage />} />
            <Route path="/notification-demo" element={<NotificationDemo />} />
            {/* 
            TODO: Uncomment when implementing full routing:
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/archive" element={<ArchivePage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/export" element={<ExportPage />} />
            */}
          </Routes>
        </Suspense>
      </BrowserRouter>
    </ToastProvider>
  );
}

export default App;
