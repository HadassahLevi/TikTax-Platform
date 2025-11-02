import { useAuthStore } from '@/stores/auth.store';
import { useNavigate } from 'react-router-dom';
import { useCallback, useEffect, useState } from 'react';
import type { LoginData, SignupData } from '@/types/auth.types';

/**
 * Custom hook for authentication
 * Provides convenient access to auth state and actions
 * 
 * @returns Auth state and helper functions
 * 
 * @example
 * ```tsx
 * const { user, login, logout, isAuthenticated } = useAuth();
 * 
 * // Login with redirect
 * await login({ email: 'user@example.com', password: '123456' });
 * 
 * // Check subscription
 * if (hasPlan('pro')) {
 *   // Access pro features
 * }
 * 
 * // Check usage
 * const remaining = remainingReceipts();
 * const usage = usagePercentage();
 * ```
 */
export const useAuth = () => {
  const navigate = useNavigate();
  
  const {
    user,
    isAuthenticated,
    isLoading,
    error,
    login: storeLogin,
    signup: storeSignup,
    logout: storeLogout,
    checkAuth
  } = useAuthStore();

  /**
   * Login user and redirect to dashboard
   * 
   * @param data - Login credentials
   * @throws {Error} If login fails
   * 
   * @example
   * ```tsx
   * await login({ 
   *   email: 'user@tiktax.co.il', 
   *   password: 'securePassword123' 
   * });
   * ```
   */
  const login = useCallback(async (data: LoginData) => {
    await storeLogin(data);
    navigate('/dashboard');
  }, [storeLogin, navigate]);

  /**
   * Signup user and redirect to dashboard
   * 
   * @param data - Signup data
   * @throws {Error} If signup fails
   * 
   * @example
   * ```tsx
   * await signup({
   *   email: 'user@tiktax.co.il',
   *   password: 'securePassword123',
   *   firstName: 'David',
   *   lastName: 'Cohen',
   *   businessName: 'Cohen Design Studio'
   * });
   * ```
   */
  const signup = useCallback(async (data: SignupData) => {
    await storeSignup(data);
    navigate('/dashboard');
  }, [storeSignup, navigate]);

  /**
   * Logout user and redirect to login
   * 
   * @example
   * ```tsx
   * await logout();
   * ```
   */
  const logout = useCallback(async () => {
    await storeLogout();
    navigate('/login');
  }, [storeLogout, navigate]);

  /**
   * Check if user has specific subscription plan or higher
   * 
   * @param plan - Required plan level
   * @returns True if user has the plan or higher
   * 
   * @example
   * ```tsx
   * if (hasPlan('pro')) {
   *   // User has pro or business plan
   * }
   * ```
   */
  const hasPlan = useCallback((plan: 'free' | 'basic' | 'pro' | 'business') => {
    if (!user) return false;
    const planHierarchy = { free: 0, basic: 1, pro: 2, business: 3 };
    return planHierarchy[user.subscriptionPlan] >= planHierarchy[plan];
  }, [user]);

  /**
   * Check if user has reached monthly receipt limit
   * 
   * @returns True if limit reached
   * 
   * @example
   * ```tsx
   * if (hasReachedLimit()) {
   *   toast.error('מכסת הקבלות מלאה לחודש זה');
   *   return;
   * }
   * ```
   */
  const hasReachedLimit = useCallback(() => {
    if (!user) return false;
    return user.receiptsUsedThisMonth >= user.receiptsLimit;
  }, [user]);

  /**
   * Get remaining receipts for current month
   * 
   * @returns Number of receipts remaining
   * 
   * @example
   * ```tsx
   * const remaining = remainingReceipts();
   * console.log(`${remaining} receipts left this month`);
   * ```
   */
  const remainingReceipts = useCallback(() => {
    if (!user) return 0;
    return Math.max(0, user.receiptsLimit - user.receiptsUsedThisMonth);
  }, [user]);

  /**
   * Get usage percentage for current month
   * 
   * @returns Percentage (0-100)
   * 
   * @example
   * ```tsx
   * const usage = usagePercentage();
   * <ProgressBar value={usage} />
   * ```
   */
  const usagePercentage = useCallback(() => {
    if (!user) return 0;
    return Math.round((user.receiptsUsedThisMonth / user.receiptsLimit) * 100);
  }, [user]);

  return {
    // State
    user,
    isAuthenticated,
    isLoading,
    error,
    
    // Actions
    login,
    signup,
    logout,
    checkAuth,
    
    // Helpers
    hasPlan,
    hasReachedLimit,
    remainingReceipts,
    usagePercentage
  };
};

/**
 * Hook to require authentication
 * Redirects to login if not authenticated
 * Use in protected routes/components
 * 
 * @returns Authentication status
 * 
 * @example
 * ```tsx
 * function ProtectedPage() {
 *   const { isAuthenticated, isLoading } = useRequireAuth();
 *   
 *   if (isLoading) return <LoadingScreen />;
 *   
 *   return <div>Protected Content</div>;
 * }
 * ```
 */
export const useRequireAuth = () => {
  const { isAuthenticated, isLoading } = useAuth();
  const navigate = useNavigate();
  
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      navigate('/login', { replace: true });
    }
  }, [isAuthenticated, isLoading, navigate]);
  
  return { isAuthenticated, isLoading };
};

/**
 * Hook to gate features by subscription plan
 * Shows upgrade prompt if user doesn't have required plan
 * 
 * @param requiredPlan - Minimum plan level required
 * @returns Access check function and upgrade modal state
 * 
 * @example
 * ```tsx
 * function AdvancedReportsPage() {
 *   const { checkAccess, showUpgrade, setShowUpgrade } = useSubscriptionGate('pro');
 *   
 *   const handleGenerateReport = () => {
 *     if (!checkAccess()) return; // Shows upgrade modal
 *     
 *     // Generate report...
 *   };
 *   
 *   return (
 *     <>
 *       <Button onClick={handleGenerateReport}>
 *         ייצא דוח מתקדם
 *       </Button>
 *       
 *       {showUpgrade && (
 *         <UpgradeModal 
 *           plan="pro"
 *           onClose={() => setShowUpgrade(false)}
 *         />
 *       )}
 *     </>
 *   );
 * }
 * ```
 */
export const useSubscriptionGate = (requiredPlan: 'basic' | 'pro' | 'business') => {
  const { hasPlan } = useAuth();
  const [showUpgrade, setShowUpgrade] = useState(false);
  
  /**
   * Check if user has access to feature
   * Shows upgrade modal if access denied
   * 
   * @returns True if user has access
   */
  const checkAccess = useCallback(() => {
    if (!hasPlan(requiredPlan)) {
      setShowUpgrade(true);
      return false;
    }
    return true;
  }, [hasPlan, requiredPlan]);
  
  return { 
    checkAccess, 
    showUpgrade, 
    setShowUpgrade 
  };
};

export default useAuth;
