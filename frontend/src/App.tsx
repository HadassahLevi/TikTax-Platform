import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { SubscriptionPage, CheckoutSuccessPage, CheckoutCancelPage } from './pages';
import { NotificationDemo } from './pages/NotificationDemo';
import { ToastProvider } from './contexts/ToastContext';

// TEMPORARY: Showing SubscriptionPage for testing
// TODO: Revert to original welcome screen after testing
function App() {
  return (
    <ToastProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<SubscriptionPage />} />
          <Route path="/checkout/success" element={<CheckoutSuccessPage />} />
          <Route path="/checkout/cancel" element={<CheckoutCancelPage />} />
          <Route path="/notification-demo" element={<NotificationDemo />} />
        </Routes>
      </BrowserRouter>
    </ToastProvider>
  );
}

export default App;
