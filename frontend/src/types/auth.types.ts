/**
 * Authentication Type Definitions for Tik-Tax
 * 
 * This file contains all TypeScript interfaces and types related to authentication,
 * user management, and authorization in the Tik-Tax application.
 * 
 * @module types/auth
 */

// ============================================================================
// USER ENTITY
// ============================================================================

/**
 * Represents a registered user in the Tik-Tax system.
 * 
 * Contains personal information, business details, subscription data,
 * and account status information.
 */
export interface User {
  /** Unique identifier for the user */
  id: string;
  
  /** User's email address (used for login) */
  email: string;
  
  /** User's full name in Hebrew or English */
  fullName: string;
  
  /** Israeli phone number (format: 05X-XXX-XXXX) */
  phone: string;
  
  /** Israeli ID number (9 digits with checksum) */
  idNumber: string;
  
  /** Business/Company name */
  businessName: string;
  
  /** Israeli business registration number (עוסק מורשה / חברה בע"מ) */
  businessNumber: string;
  
  /** Type of business entity in Israel */
  businessType: 'licensed_dealer' | 'exempt_dealer' | 'limited_company';
  
  /** Current subscription plan */
  subscriptionPlan: 'free' | 'basic' | 'pro' | 'business';
  
  /** Subscription status */
  subscriptionStatus: 'active' | 'trial' | 'cancelled' | 'past_due';
  
  /** Number of receipts processed this month */
  receiptsUsedThisMonth: number;
  
  /** Monthly receipt limit based on subscription plan */
  receiptsLimit: number;
  
  /** Account creation timestamp (ISO 8601) */
  createdAt: string;
  
  /** Last successful login timestamp (ISO 8601) */
  lastLoginAt?: string;
  
  /** Whether email has been verified */
  emailVerified: boolean;
  
  /** Whether phone number has been verified (required for Israeli businesses) */
  phoneVerified: boolean;
}

// ============================================================================
// SIGNUP & REGISTRATION
// ============================================================================

/**
 * Form data for user registration (3-step signup process).
 * 
 * Step 1: Personal Information
 * Step 2: Business Information
 * Step 3: Verification
 */
export interface SignupData {
  // Step 1: Personal Info
  /** User's full name */
  fullName: string;
  
  /** Israeli ID number (9 digits) */
  idNumber: string;
  
  /** Email address */
  email: string;
  
  /** Password (min 8 chars, uppercase, lowercase, number) */
  password: string;
  
  /** Israeli phone number */
  phone: string;
  
  // Step 2: Business Info
  /** Business name */
  businessName: string;
  
  /** Business registration number */
  businessNumber: string;
  
  /** Type of business entity */
  businessType: 'licensed_dealer' | 'exempt_dealer' | 'limited_company';
  
  // Step 3: Verification
  /** SMS verification code (6 digits) */
  verificationCode: string;
}

// ============================================================================
// LOGIN
// ============================================================================

/**
 * Credentials required for user login.
 */
export interface LoginData {
  /** User's email address */
  email: string;
  
  /** User's password */
  password: string;
  
  /** Keep user logged in (extends token expiry) */
  rememberMe?: boolean;
}

// ============================================================================
// API RESPONSES
// ============================================================================

/**
 * Response from successful authentication (login or signup).
 * 
 * Contains user data and JWT tokens for subsequent API calls.
 */
export interface AuthResponse {
  /** Authenticated user data */
  user: User;
  
  /** JWT access token (short-lived, ~15 minutes) */
  accessToken: string;
  
  /** JWT refresh token (long-lived, ~7 days) */
  refreshToken: string;
  
  /** Access token expiry in seconds */
  expiresIn: number;
}

/**
 * Response from token refresh endpoint.
 * 
 * Used to obtain a new access token without re-authentication.
 */
export interface RefreshTokenResponse {
  /** New JWT access token */
  accessToken: string;
  
  /** Token expiry in seconds */
  expiresIn: number;
}

// ============================================================================
// PASSWORD MANAGEMENT
// ============================================================================

/**
 * Request to initiate password reset flow.
 * 
 * Sends reset link to user's email.
 */
export interface PasswordResetRequest {
  /** Email address of the account to reset */
  email: string;
}

/**
 * Confirm password reset with token from email.
 */
export interface PasswordResetConfirm {
  /** Reset token from email link */
  token: string;
  
  /** New password to set */
  newPassword: string;
}

/**
 * Change password for authenticated user.
 * 
 * Requires current password for security.
 */
export interface ChangePasswordData {
  /** Current password for verification */
  currentPassword: string;
  
  /** New password */
  newPassword: string;
  
  /** Confirmation of new password (must match) */
  confirmPassword: string;
}

// ============================================================================
// SMS VERIFICATION
// ============================================================================

/**
 * Request SMS verification code.
 * 
 * Required for phone verification during signup.
 */
export interface SMSVerificationRequest {
  /** Israeli phone number to verify */
  phone: string;
}

/**
 * Confirm SMS verification code.
 */
export interface SMSVerificationConfirm {
  /** Phone number being verified */
  phone: string;
  
  /** 6-digit verification code from SMS */
  code: string;
}

// ============================================================================
// ERROR HANDLING
// ============================================================================

/**
 * Standardized authentication error object.
 * 
 * Used for consistent error handling across the auth flow.
 */
export interface AuthError {
  /** Error code (e.g., 'INVALID_CREDENTIALS', 'EMAIL_EXISTS') */
  code: string;
  
  /** Human-readable error message (localized) */
  message: string;
  
  /** Optional field name for form validation errors */
  field?: string;
}

// ============================================================================
// ZUSTAND STORE STATE & ACTIONS
// ============================================================================

/**
 * Authentication state managed by Zustand store.
 * 
 * Represents the current authentication status of the user.
 */
export interface AuthState {
  /** Currently authenticated user (null if not logged in) */
  user: User | null;
  
  /** JWT access token stored in memory (NEVER localStorage) */
  accessToken: string | null;
  
  /** JWT refresh token stored in memory (NEVER localStorage) */
  refreshToken: string | null;
  
  /** Computed: whether user is authenticated */
  isAuthenticated: boolean;
  
  /** Loading state for async auth operations */
  isLoading: boolean;
  
  /** Current authentication error (null if no error) */
  error: AuthError | null;
}

/**
 * Authentication actions available in Zustand store.
 * 
 * Methods for managing authentication state and performing auth operations.
 */
export interface AuthActions {
  /**
   * Set user data in store.
   * @param user - User object to store
   */
  setUser: (user: User) => void;
  
  /**
   * Set authentication tokens in memory.
   * @param accessToken - JWT access token
   * @param refreshToken - JWT refresh token
   */
  setTokens: (accessToken: string, refreshToken: string) => void;
  
  /**
   * Clear all authentication data (logout locally).
   */
  clearAuth: () => void;
  
  /**
   * Authenticate user with email and password.
   * @param data - Login credentials
   * @throws AuthError if login fails
   */
  login: (data: LoginData) => Promise<void>;
  
  /**
   * Register new user account.
   * @param data - Signup form data
   * @throws AuthError if signup fails
   */
  signup: (data: SignupData) => Promise<void>;
  
  /**
   * Log out user (clear local state + notify server).
   * @throws AuthError if server logout fails
   */
  logout: () => Promise<void>;
  
  /**
   * Refresh access token using refresh token.
   * @returns New access token
   * @throws AuthError if refresh fails
   */
  refreshToken: () => Promise<string>;
  
  /**
   * Check if user is authenticated (verify token validity).
   * Used on app initialization.
   */
  checkAuth: () => Promise<void>;
  
  /**
   * Set loading state.
   * @param loading - Loading state
   */
  setLoading: (loading: boolean) => void;
  
  /**
   * Set authentication error.
   * @param error - Error object or null to clear
   */
  setError: (error: AuthError | null) => void;
}

/**
 * Combined authentication store type.
 * 
 * Merges state and actions for use in Zustand store.
 */
export type AuthStore = AuthState & AuthActions;

// ============================================================================
// VALIDATION HELPERS
// ============================================================================

/**
 * Validate email address format.
 * 
 * @param email - Email string to validate
 * @returns True if valid email format
 * 
 * @example
 * isValidEmail('user@example.com') // true
 * isValidEmail('invalid.email') // false
 */
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email.trim());
};

/**
 * Validate Israeli ID number (תעודת זהות).
 * 
 * Checks:
 * - Exactly 9 digits
 * - Valid checksum using Luhn algorithm
 * 
 * @param id - ID number to validate (string or number)
 * @returns True if valid Israeli ID
 * 
 * @example
 * isValidIsraeliID('123456782') // true (valid checksum)
 * isValidIsraeliID('123456789') // false (invalid checksum)
 */
export const isValidIsraeliID = (id: string): boolean => {
  // Clean input and ensure 9 digits
  const cleanId = id.toString().trim().padStart(9, '0');
  
  if (!/^\d{9}$/.test(cleanId)) {
    return false;
  }
  
  // Luhn algorithm for Israeli ID validation
  let sum = 0;
  for (let i = 0; i < 9; i++) {
    let digit = parseInt(cleanId[i], 10);
    
    // Double every second digit
    if (i % 2 === 0) {
      digit *= 1;
    } else {
      digit *= 2;
      // If result is two digits, add them together
      if (digit > 9) {
        digit = Math.floor(digit / 10) + (digit % 10);
      }
    }
    
    sum += digit;
  }
  
  // Valid if sum is divisible by 10
  return sum % 10 === 0;
};

/**
 * Validate Israeli phone number.
 * 
 * Accepts formats:
 * - 05X-XXX-XXXX
 * - 05XXXXXXXX
 * - 0X-XXX-XXXX (landline)
 * 
 * @param phone - Phone number to validate
 * @returns True if valid Israeli phone format
 * 
 * @example
 * isValidIsraeliPhone('050-123-4567') // true
 * isValidIsraeliPhone('0501234567') // true
 * isValidIsraeliPhone('02-123-4567') // true (landline)
 * isValidIsraeliPhone('123456') // false
 */
export const isValidIsraeliPhone = (phone: string): boolean => {
  // Remove all non-digit characters
  const cleaned = phone.replace(/\D/g, '');
  
  // Must be 9-10 digits starting with 0
  if (!/^0\d{8,9}$/.test(cleaned)) {
    return false;
  }
  
  // Valid prefixes:
  // 02, 03, 04, 08, 09 (landline)
  // 050, 051, 052, 053, 054, 055, 058 (mobile)
  const validPrefixes = /^0(5[0-8]|[2-4]|[89])\d{7,8}$/;
  
  return validPrefixes.test(cleaned);
};

/**
 * Validate password strength.
 * 
 * Requirements:
 * - Minimum 8 characters
 * - At least one uppercase letter
 * - At least one lowercase letter
 * - At least one number
 * 
 * @param password - Password to validate
 * @returns True if password meets requirements
 * 
 * @example
 * isValidPassword('Password123') // true
 * isValidPassword('password') // false (no uppercase, no number)
 * isValidPassword('PASS123') // false (no lowercase)
 */
export const isValidPassword = (password: string): boolean => {
  if (password.length < 8) {
    return false;
  }
  
  const hasUppercase = /[A-Z]/.test(password);
  const hasLowercase = /[a-z]/.test(password);
  const hasNumber = /\d/.test(password);
  
  return hasUppercase && hasLowercase && hasNumber;
};

/**
 * Validate Israeli business number (עוסק מורשה).
 * 
 * @param businessNumber - Business number to validate
 * @returns True if valid format (9 digits)
 * 
 * @example
 * isValidBusinessNumber('123456789') // true
 * isValidBusinessNumber('12345') // false
 */
export const isValidBusinessNumber = (businessNumber: string): boolean => {
  const cleaned = businessNumber.replace(/\D/g, '');
  return /^\d{9}$/.test(cleaned);
};

// ============================================================================
// TYPE GUARDS
// ============================================================================

/**
 * Type guard to check if error is an AuthError.
 * 
 * @param error - Error object to check
 * @returns True if error is AuthError
 */
export const isAuthError = (error: unknown): error is AuthError => {
  return (
    typeof error === 'object' &&
    error !== null &&
    'code' in error &&
    'message' in error &&
    typeof (error as AuthError).code === 'string' &&
    typeof (error as AuthError).message === 'string'
  );
};

/**
 * Type guard to check if user object is valid.
 * 
 * @param user - Object to check
 * @returns True if object is a valid User
 */
export const isUser = (user: unknown): user is User => {
  return (
    typeof user === 'object' &&
    user !== null &&
    'id' in user &&
    'email' in user &&
    'fullName' in user &&
    typeof (user as User).id === 'string' &&
    typeof (user as User).email === 'string' &&
    typeof (user as User).fullName === 'string'
  );
};

// ============================================================================
// CONSTANTS
// ============================================================================

/**
 * Business type labels in Hebrew.
 */
export const BUSINESS_TYPE_LABELS: Record<User['businessType'], string> = {
  licensed_dealer: 'עוסק מורשה',
  exempt_dealer: 'עוסק פטור',
  limited_company: 'חברה בע"מ',
};

/**
 * Subscription plan labels.
 */
export const SUBSCRIPTION_PLAN_LABELS: Record<User['subscriptionPlan'], string> = {
  free: 'חינם',
  basic: 'בסיסי',
  pro: 'מקצועי',
  business: 'עסקי',
};

/**
 * Subscription status labels in Hebrew.
 */
export const SUBSCRIPTION_STATUS_LABELS: Record<User['subscriptionStatus'], string> = {
  active: 'פעיל',
  trial: 'תקופת ניסיון',
  cancelled: 'מבוטל',
  past_due: 'תשלום באיחור',
};

// ============================================================================
// EXPORTS
// ============================================================================

// All interfaces and types are already exported individually above
// Export the combined store type for convenience
export type { AuthStore as default };
