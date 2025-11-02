/**
 * Validation utilities for forms and user input
 */

/**
 * Validate email format
 * @param email - Email address to validate
 * @returns true if valid, false otherwise
 */
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Validate Israeli phone number
 * @param phone - Phone number to validate
 * @returns true if valid, false otherwise
 */
export const isValidPhone = (phone: string): boolean => {
  // Remove all non-digit characters
  const cleaned = phone.replace(/\D/g, '');
  // Israeli phone numbers are 9-10 digits
  return cleaned.length >= 9 && cleaned.length <= 10;
};

/**
 * Validate password strength
 * @param password - Password to validate
 * @returns Object with validation result and message
 */
export const validatePassword = (
  password: string
): { isValid: boolean; message: string } => {
  if (password.length < 8) {
    return { isValid: false, message: 'הסיסמה חייבת להכיל לפחות 8 תווים' };
  }

  if (!/[A-Z]/.test(password)) {
    return { isValid: false, message: 'הסיסמה חייבת להכיל לפחות אות גדולה אחת' };
  }

  if (!/[a-z]/.test(password)) {
    return { isValid: false, message: 'הסיסמה חייבת להכיל לפחות אות קטנה אחת' };
  }

  if (!/[0-9]/.test(password)) {
    return { isValid: false, message: 'הסיסמה חייבת להכיל לפחות ספרה אחת' };
  }

  return { isValid: true, message: 'סיסמה תקינה' };
};

/**
 * Validate Israeli Tax ID (מספר עוסק מורשה)
 * @param taxId - Tax ID to validate
 * @returns true if valid, false otherwise
 */
export const isValidTaxId = (taxId: string): boolean => {
  // Remove all non-digit characters
  const cleaned = taxId.replace(/\D/g, '');
  // Israeli Tax ID is 9 digits
  return cleaned.length === 9;
};

/**
 * Sanitize user input to prevent XSS
 * @param input - User input string
 * @returns Sanitized string
 */
export const sanitizeInput = (input: string): string => {
  return input
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;');
};

/**
 * Validate file type for receipt images
 * @param file - File object
 * @returns true if valid image type
 */
export const isValidImageFile = (file: File): boolean => {
  const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/heic'];
  return validTypes.includes(file.type.toLowerCase());
};

/**
 * Validate file size (max 10MB)
 * @param file - File object
 * @returns true if size is valid
 */
export const isValidFileSize = (file: File): boolean => {
  const maxSize = 10 * 1024 * 1024; // 10MB
  return file.size <= maxSize;
};

/**
 * Validate amount is positive number
 * @param amount - Amount to validate
 * @returns true if valid
 */
export const isValidAmount = (amount: number): boolean => {
  return amount > 0 && !isNaN(amount) && isFinite(amount);
};
