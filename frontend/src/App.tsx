import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { SubscriptionPage, CheckoutSuccessPage, CheckoutCancelPage } from './pages';

// TEMPORARY: Showing SubscriptionPage for testing
// TODO: Revert to original welcome screen after testing
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SubscriptionPage />} />
        <Route path="/checkout/success" element={<CheckoutSuccessPage />} />
        <Route path="/checkout/cancel" element={<CheckoutCancelPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
