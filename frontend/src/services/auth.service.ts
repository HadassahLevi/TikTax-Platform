/**
 * Authentication Service Layer
 * 
 * Handles all authentication-related API calls for Tik-Tax.
 * Includes signup, login, logout, token refresh, password management, and SMS verification.
 * 
 * All functions include proper error handling with Hebrew messages.
 * 
 * @module services/auth
 */

import axios from 'axios';
import apiClient from '../config/axios';
import {
  type SignupData,
  type LoginData,
  type AuthResponse,
  type RefreshTokenResponse,
  type User,
  type ChangePasswordData,
} from '../types/auth.types';
import { handleAPIError, logError } from '../utils/errorHandler';

// ============================================================================
// SIGNUP & REGISTRATION
// ============================================================================

/**
 * Register a new user account (3-step signup process)
 * 
 * POST /api/auth/signup
 * 
 * @param data - Signup data including personal info, business info, and verification
 * @returns Authentication response with user data and tokens
 * @throws Error with Hebrew message if signup fails
 * 
 * @example
 * ```typescript
 * try {
 *   const response = await signup({
 *     fullName: 'דוד כהן',
 *     idNumber: '123456789',
 *     email: 'david@example.com',
 *     password: 'SecurePass123',
 *     phone: '0501234567',
 *     businessName: 'דוד כהן - עיצוב גרפי',
 *     businessNumber: '123456789',
 *     businessType: 'licensed_dealer',
 *     verificationCode: '123456'
 *   });
 *   console.log('User registered:', response.user);
 * } catch (error) {
 *   console.error('Signup failed:', error.message);
 * }
 * ```
 */
export const signup = async (data: SignupData): Promise<AuthResponse> => {
  try {
    const response = await apiClient.post<AuthResponse>('/auth/signup', data);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      logError(error, 'Signup');
      const message = handleAPIError(error);
      throw new Error(message);
    }
    throw error;
  }
};

// ============================================================================
// LOGIN & LOGOUT
// ============================================================================

/**
 * Authenticate user with email and password
 * 
 * POST /api/auth/login
 * 
 * @param data - Login credentials (email, password, optional rememberMe)
 * @returns Authentication response with user data and tokens
 * @throws Error with Hebrew message if login fails
 * 
 * @example
 * ```typescript
 * try {
 *   const response = await login({
 *     email: 'david@example.com',
 *     password: 'SecurePass123',
 *     rememberMe: true
 *   });
 *   // Store tokens in auth store (NOT localStorage!)
 *   authStore.setTokens(response.accessToken, response.refreshToken);
 * } catch (error) {
 *   console.error('Login failed:', error.message);
 * }
 * ```
 */
export const login = async (data: LoginData): Promise<AuthResponse> => {
  try {
    const response = await apiClient.post<AuthResponse>('/auth/login', data);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      logError(error, 'Login');
      const message = handleAPIError(error);
      throw new Error(message);
    }
    throw error;
  }
};

/**
 * Log out current user
 * 
 * POST /api/auth/logout
 * 
 * Invalidates the current session and refresh token on the server.
 * Client should clear tokens from auth store after this call.
 * 
 * @throws Error with Hebrew message if logout fails
 * 
 * @example
 * ```typescript
 * try {
 *   await logout();
 *   authStore.clearAuth(); // Clear tokens from memory
 *   navigate('/login');
 * } catch (error) {
 *   console.error('Logout failed:', error.message);
 *   // Still clear local tokens even if server call fails
 *   authStore.clearAuth();
 * }
 * ```
 */
export const logout = async (): Promise<void> => {
  try {
    await apiClient.post('/auth/logout');
  } catch (error) {
    if (axios.isAxiosError(error)) {
      logError(error, 'Logout');
      const message = handleAPIError(error);
      throw new Error(message);
    }
    throw error;
  }
};

// ============================================================================
// TOKEN MANAGEMENT
// ============================================================================

/**
 * Refresh access token using refresh token
 * 
 * POST /api/auth/refresh
 * 
 * Used to obtain a new access token when the current one expires.
 * Called automatically by Axios interceptor on 401 responses.
 * 
 * @param refreshToken - Current refresh token
 * @returns New access token and expiry time
 * @throws Error with Hebrew message if refresh fails
 * 
 * @example
 * ```typescript
 * try {
 *   const currentRefreshToken = authStore.getRefreshToken();
 *   const response = await refreshToken(currentRefreshToken);
 *   authStore.setAccessToken(response.accessToken);
 * } catch (error) {
 *   console.error('Token refresh failed:', error.message);
 *   // Redirect to login
 *   authStore.clearAuth();
 *   navigate('/login');
 * }
 * ```
 */
export const refreshToken = async (refreshToken: string): Promise<RefreshTokenResponse> => {
  try {
    const response = await apiClient.post<RefreshTokenResponse>('/auth/refresh', {
      refreshToken,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      logError(error, 'Token Refresh');
      const message = handleAPIError(error);
      throw new Error(message);
    }
    throw error;
  }
};

// ============================================================================
// USER PROFILE
// ============================================================================

/**
 * Get current authenticated user's profile
 * 
 * GET /api/auth/me
 * 
 * Requires valid authentication token in request headers.
 * Used to verify user is still authenticated and get updated profile data.
 * 
 * @returns Current user object
 * @throws Error with Hebrew message if request fails
 * 
 * @example
 * ```typescript
 * try {
 *   const user = await getCurrentUser();
 *   console.log('Current user:', user.fullName);
 *   console.log('Receipts used:', user.receiptsUsedThisMonth);
 * } catch (error) {
 *   console.error('Failed to get user:', error.message);
 * }
 * ```
 */
export const getCurrentUser = async (): Promise<User> => {
  try {
    const response = await apiClient.get<User>('/auth/me');
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      logError(error, 'Get Current User');
      const message = handleAPIError(error);
      throw new Error(message);
    }
    throw error;
  }
};

// ============================================================================
// SMS VERIFICATION
// ============================================================================

/**
 * Send SMS verification code to phone number
 * 
 * POST /api/auth/send-verification
 * 
 * Sends a 6-digit verification code via SMS to the provided Israeli phone number.
 * Used during signup process (Step 3) and when user wants to change phone number.
 * 
 * @param phone - Israeli phone number (format: 05X-XXX-XXXX or 05XXXXXXXX)
 * @throws Error with Hebrew message if sending fails
 * 
 * @example
 * ```typescript
 * try {
 *   await sendSMSVerification('0501234567');
 *   console.log('Verification code sent!');
 *   // Show input field for code
 * } catch (error) {
 *   console.error('Failed to send SMS:', error.message);
 * }
 * ```
 */
export const sendSMSVerification = async (phone: string): Promise<void> => {
  try {
    await apiClient.post('/auth/send-verification', { phone });
  } catch (error) {
    if (axios.isAxiosError(error)) {
      logError(error, 'Send SMS Verification');
      const message = handleAPIError(error);
      throw new Error(message);
    }
    throw error;
  }
};

/**
 * Verify SMS code
 * 
 * POST /api/auth/verify-sms
 * 
 * Confirms the 6-digit verification code sent via SMS.
 * Required to complete phone verification during signup.
 * 
 * @param phone - Phone number being verified
 * @param code - 6-digit verification code from SMS
 * @throws Error with Hebrew message if verification fails
 * 
 * @example
 * ```typescript
 * try {
 *   await verifySMSCode('0501234567', '123456');
 *   console.log('Phone verified successfully!');
 *   // Proceed to complete signup
 * } catch (error) {
 *   console.error('Invalid verification code:', error.message);
 * }
 * ```
 */
export const verifySMSCode = async (phone: string, code: string): Promise<void> => {
  try {
    await apiClient.post('/auth/verify-sms', { phone, code });
  } catch (error) {
    if (axios.isAxiosError(error)) {
      logError(error, 'Verify SMS Code');
      const message = handleAPIError(error);
      throw new Error(message);
    }
    throw error;
  }
};

// ============================================================================
// PASSWORD MANAGEMENT
// ============================================================================

/**
 * Request password reset link
 * 
 * POST /api/auth/forgot-password
 * 
 * Sends password reset link to user's email address.
 * Email contains a time-limited token for password reset.
 * 
 * @param email - Email address of the account to reset
 * @throws Error with Hebrew message if request fails
 * 
 * @example
 * ```typescript
 * try {
 *   await requestPasswordReset('david@example.com');
 *   console.log('Password reset email sent!');
 *   // Show success message
 * } catch (error) {
 *   console.error('Failed to send reset email:', error.message);
 * }
 * ```
 */
export const requestPasswordReset = async (email: string): Promise<void> => {
  try {
    await apiClient.post('/auth/forgot-password', { email });
  } catch (error) {
    if (axios.isAxiosError(error)) {
      logError(error, 'Request Password Reset');
      const message = handleAPIError(error);
      throw new Error(message);
    }
    throw error;
  }
};

/**
 * Reset password using token from email
 * 
 * POST /api/auth/reset-password
 * 
 * Confirms password reset with token from email link.
 * Token is time-limited (usually 1 hour) and single-use.
 * 
 * @param token - Reset token from email URL parameter
 * @param newPassword - New password to set
 * @throws Error with Hebrew message if reset fails
 * 
 * @example
 * ```typescript
 * try {
 *   // Extract token from URL: /reset-password?token=abc123
 *   const token = new URLSearchParams(location.search).get('token');
 *   await resetPassword(token, 'NewSecurePass123');
 *   console.log('Password reset successfully!');
 *   // Redirect to login
 * } catch (error) {
 *   console.error('Password reset failed:', error.message);
 * }
 * ```
 */
export const resetPassword = async (token: string, newPassword: string): Promise<void> => {
  try {
    await apiClient.post('/auth/reset-password', { token, newPassword });
  } catch (error) {
    if (axios.isAxiosError(error)) {
      logError(error, 'Reset Password');
      const message = handleAPIError(error);
      throw new Error(message);
    }
    throw error;
  }
};

/**
 * Change password for authenticated user
 * 
 * PUT /api/auth/change-password
 * 
 * Requires current password for security verification.
 * Used in user settings/profile page.
 * 
 * @param data - Change password data (current password, new password, confirmation)
 * @throws Error with Hebrew message if change fails
 * 
 * @example
 * ```typescript
 * try {
 *   await changePassword({
 *     currentPassword: 'OldPass123',
 *     newPassword: 'NewSecurePass123',
 *     confirmPassword: 'NewSecurePass123'
 *   });
 *   console.log('Password changed successfully!');
 *   // Show success message
 * } catch (error) {
 *   console.error('Password change failed:', error.message);
 * }
 * ```
 */
export const changePassword = async (data: ChangePasswordData): Promise<void> => {
  try {
    await apiClient.put('/auth/change-password', data);
  } catch (error) {
    if (axios.isAxiosError(error)) {
      logError(error, 'Change Password');
      const message = handleAPIError(error);
      throw new Error(message);
    }
    throw error;
  }
};

// ============================================================================
// EXPORTS
// ============================================================================

/**
 * Auth Service
 * 
 * Export all authentication functions as a single service object
 * for easier imports and organization.
 * 
 * @example
 * ```typescript
 * import { authService } from '@/services/auth.service';
 * 
 * // Use service methods
 * await authService.login({ email, password });
 * await authService.logout();
 * ```
 */
export const authService = {
  signup,
  login,
  logout,
  refreshToken,
  getCurrentUser,
  sendSMSVerification,
  verifySMSCode,
  requestPasswordReset,
  resetPassword,
  changePassword,
};

// Also export individual functions for flexibility
export default authService;
