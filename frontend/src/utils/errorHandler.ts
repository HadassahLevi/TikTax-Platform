/**
 * Error Handler Utility
 * 
 * Transforms API errors into user-friendly Hebrew messages.
 * Handles Axios errors, network errors, and timeout errors.
 * 
 * @module utils/errorHandler
 */

import { AxiosError } from 'axios';

/**
 * API Error response structure
 */
interface APIErrorResponse {
  code?: string;
  message?: string;
  field?: string;
  errors?: Array<{
    field: string;
    message: string;
  }>;
}

/**
 * Hebrew error messages mapped to error codes
 */
const errorMessages: Record<string, string> = {
  // Authentication errors
  INVALID_CREDENTIALS: 'שם משתמש או סיסמה שגויים',
  EMAIL_EXISTS: 'כתובת המייל כבר קיימת במערכת',
  PHONE_EXISTS: 'מספר הטלפון כבר רשום במערכת',
  INVALID_TOKEN: 'טוקן לא תקין או פג תוקפו',
  TOKEN_EXPIRED: 'תוקף ההתחברות פג. אנא התחבר מחדש',
  UNAUTHORIZED: 'אין לך הרשאה לבצע פעולה זו',
  SESSION_EXPIRED: 'תוקף ההתחברות פג. אנא התחבר מחדש',
  
  // User/Account errors
  USER_NOT_FOUND: 'משתמש לא נמצא',
  ACCOUNT_DISABLED: 'החשבון הושעה. אנא פנה לתמיכה',
  EMAIL_NOT_VERIFIED: 'כתובת המייל טרם אומתה',
  PHONE_NOT_VERIFIED: 'מספר הטלפון טרם אומת',
  
  // Validation errors
  INVALID_EMAIL: 'כתובת מייל לא תקינה',
  INVALID_PHONE: 'מספר טלפון לא תקין',
  INVALID_ID_NUMBER: 'מספר תעודת זהות לא תקין',
  INVALID_BUSINESS_NUMBER: 'מספר עוסק לא תקין',
  WEAK_PASSWORD: 'הסיסמה חלשה מדי. חייב להכיל לפחות 8 תווים, אות גדולה, אות קטנה ומספר',
  PASSWORD_MISMATCH: 'הסיסמאות אינן תואמות',
  
  // SMS Verification errors
  INVALID_VERIFICATION_CODE: 'קוד אימות שגוי',
  VERIFICATION_CODE_EXPIRED: 'קוד האימות פג תוקפו',
  TOO_MANY_ATTEMPTS: 'נעשו יותר מדי ניסיונות. אנא נסה שוב מאוחר יותר',
  SMS_SEND_FAILED: 'שליחת קוד האימות נכשלה. אנא נסה שוב',
  
  // Password reset errors
  INVALID_RESET_TOKEN: 'קישור לאיפוס סיסמה לא תקין או פג תוקפו',
  RESET_TOKEN_EXPIRED: 'קישור לאיפוס סיסמה פג תוקפו',
  
  // Subscription/Limits errors
  RECEIPT_LIMIT_REACHED: 'הגעת למגבלת הקבלות החודשית',
  SUBSCRIPTION_EXPIRED: 'המנוי פג תוקפו',
  SUBSCRIPTION_PAYMENT_FAILED: 'תשלום המנוי נכשל',
  
  // Network/Server errors
  NETWORK_ERROR: 'שגיאת רשת. אנא בדוק את החיבור לאינטרנט',
  SERVER_ERROR: 'שגיאת שרת. אנא נסה שוב מאוחר יותר',
  SERVICE_UNAVAILABLE: 'השירות אינו זמין כעת. אנא נסה שוב מאוחר יותר',
  TIMEOUT: 'הבקשה נמשכת זמן רב מדי. אנא נסה שוב',
  
  // Generic errors
  UNKNOWN_ERROR: 'אירעה שגיאה לא צפויה. אנא נסה שוב',
  VALIDATION_ERROR: 'נתונים לא תקינים',
  BAD_REQUEST: 'בקשה לא תקינה',
};

/**
 * Handle API errors and return user-friendly Hebrew message
 * 
 * @param error - Axios error object
 * @returns Hebrew error message string
 * 
 * @example
 * ```typescript
 * try {
 *   await apiClient.post('/auth/login', data);
 * } catch (error) {
 *   if (axios.isAxiosError(error)) {
 *     const message = handleAPIError(error);
 *     toast.error(message);
 *   }
 * }
 * ```
 */
export const handleAPIError = (error: AxiosError<APIErrorResponse>): string => {
  // Network error (no response from server)
  if (!error.response) {
    if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
      return errorMessages.TIMEOUT;
    }
    return errorMessages.NETWORK_ERROR;
  }

  // Get error data from response
  const { status, data } = error.response;

  // Try to get error code from response
  const errorCode = data?.code;
  
  // If we have a known error code, return its message
  if (errorCode && errorMessages[errorCode]) {
    return errorMessages[errorCode];
  }

  // If backend provides a message, use it
  if (data?.message) {
    return data.message;
  }

  // Fallback to HTTP status code messages
  switch (status) {
    case 400:
      return errorMessages.BAD_REQUEST;
    case 401:
      return errorMessages.UNAUTHORIZED;
    case 403:
      return 'אין לך הרשאה לבצע פעולה זו';
    case 404:
      return 'המשאב המבוקש לא נמצא';
    case 422:
      return errorMessages.VALIDATION_ERROR;
    case 429:
      return errorMessages.TOO_MANY_ATTEMPTS;
    case 500:
      return errorMessages.SERVER_ERROR;
    case 503:
      return errorMessages.SERVICE_UNAVAILABLE;
    default:
      return errorMessages.UNKNOWN_ERROR;
  }
};

/**
 * Extract validation errors from API response
 * 
 * @param error - Axios error object
 * @returns Object mapping field names to error messages
 * 
 * @example
 * ```typescript
 * const validationErrors = getValidationErrors(error);
 * // { email: 'כתובת מייל לא תקינה', phone: 'מספר טלפון לא תקין' }
 * ```
 */
export const getValidationErrors = (
  error: AxiosError<APIErrorResponse>
): Record<string, string> => {
  const validationErrors: Record<string, string> = {};

  if (error.response?.data?.errors) {
    error.response.data.errors.forEach((err) => {
      validationErrors[err.field] = err.message;
    });
  }

  return validationErrors;
};

/**
 * Check if error is an authentication error (401 or token-related)
 * 
 * @param error - Axios error object
 * @returns True if authentication error
 */
export const isAuthError = (error: AxiosError<APIErrorResponse>): boolean => {
  if (error.response?.status === 401) {
    return true;
  }

  const errorCode = error.response?.data?.code;
  const authErrorCodes = [
    'INVALID_TOKEN',
    'TOKEN_EXPIRED',
    'SESSION_EXPIRED',
    'UNAUTHORIZED',
  ];

  return errorCode ? authErrorCodes.includes(errorCode) : false;
};

/**
 * Check if error is a network/connection error
 * 
 * @param error - Axios error object
 * @returns True if network error
 */
export const isNetworkError = (error: AxiosError): boolean => {
  return !error.response || error.code === 'ECONNABORTED' || error.message.includes('Network Error');
};

/**
 * Log error to console in development
 * 
 * @param error - Error object
 * @param context - Additional context (e.g., 'Login', 'Signup')
 */
export const logError = (error: unknown, context?: string): void => {
  if (import.meta.env.DEV) {
    console.group(`❌ Error ${context ? `(${context})` : ''}`);
    console.error(error);
    if (error instanceof AxiosError) {
      console.log('Status:', error.response?.status);
      console.log('Data:', error.response?.data);
      console.log('Headers:', error.response?.headers);
    }
    console.groupEnd();
  }
};
