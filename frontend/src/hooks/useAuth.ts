import { useAuthStore } from '@/stores/auth.store';
import { useNavigate } from 'react-router-dom';
import { useCallback, useState, useEffect } from 'react';
import type { LoginData, SignupData } from '@/types/auth.types';
import { authService } from '@/services/auth.service';
import apiClient from '@/config/axios';

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
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const {
    user,
    isAuthenticated,
    setTokens,
    setUser,
    clearAuth
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
    setIsLoading(true);
    setError(null);
    try {
      const response = await authService.login(data);
      setTokens(response.accessToken, response.refreshToken);
      setUser(response.user);
      navigate('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'שגיאה בהתחברות');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [navigate, setTokens, setUser]);

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
   *   fullName: 'David Cohen',
   *   businessName: 'Cohen Design Studio'
   * });
   * ```
   */
  const signup = useCallback(async (data: SignupData) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await authService.signup(data);
      setTokens(response.accessToken, response.refreshToken);
      setUser(response.user);
      navigate('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'שגיאה בהרשמה');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [navigate, setTokens, setUser]);

  /**
   * Logout user and redirect to login
   * 
   * @example
   * ```tsx
   * await logout();
   * ```
   */
  const logout = useCallback(async () => {
    setIsLoading(true);
    try {
      await authService.logout();
    } catch (err) {
      // Silent fail - clear auth anyway
      console.error('Logout error:', err);
    } finally {
      clearAuth();
      setIsLoading(false);
      navigate('/login');
    }
  }, [navigate, clearAuth]);

  /**
   * Update user profile
   * 
   * @param data - Profile data to update
   * @throws {Error} If update fails
   * 
   * @example
   * ```tsx
   * await updateProfile({
   *   fullName: 'David Cohen',
   *   phone: '0501234567',
   *   businessName: 'Cohen Design'
   * });
   * ```
   */
  const updateProfile = useCallback(async (data: Partial<{
    fullName: string;
    businessName: string;
    businessNumber: string;
    phone: string;
  }>) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.put('/auth/profile', data);
      setUser(response.data.user);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'שגיאה בעדכון הפרטים');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [setUser]);

  /**
   * Change user password
   * 
   * @param currentPassword - Current password for verification
   * @param newPassword - New password to set
   * @throws {Error} If change fails
   * 
   * @example
   * ```tsx
   * await changePassword('oldPass123', 'newSecurePass456');
   * ```
   */
  const changePassword = useCallback(async (currentPassword: string, newPassword: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await authService.changePassword({
        currentPassword,
        newPassword,
        confirmPassword: newPassword
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'שגיאה בשינוי הסיסמה');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Delete user account permanently
   * 
   * @throws {Error} If deletion fails
   * 
   * @example
   * ```tsx
   * await deleteAccount();
   * ```
   */
  const deleteAccount = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      await apiClient.delete('/auth/account');
      clearAuth();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'שגיאה במחיקת החשבון');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [clearAuth]);

  /**
   * Check authentication status
   * Fetches current user data from server
   */
  const checkAuth = useCallback(async () => {
    setIsLoading(true);
    try {
      const userData = await authService.getCurrentUser();
      setUser(userData);
    } catch (err) {
      clearAuth();
    } finally {
      setIsLoading(false);
    }
  }, [setUser, clearAuth]);

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
    const userPlan = user.subscriptionPlan || 'free';
    return planHierarchy[userPlan as keyof typeof planHierarchy] >= planHierarchy[plan];
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
    updateProfile,
    changePassword,
    deleteAccount,
    
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
