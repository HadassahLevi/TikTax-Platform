import { format, parseISO } from 'date-fns';

/**
 * Format currency amount in ILS
 * @param amount - The amount to format
 * @param showSymbol - Whether to show the currency symbol
 * @returns Formatted currency string
 */
export const formatCurrency = (amount: number, showSymbol = true): string => {
  const formatted = new Intl.NumberFormat('he-IL', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);

  return showSymbol ? `₪${formatted}` : formatted;
};

/**
 * Format date string to Hebrew locale
 * @param dateString - ISO date string
 * @param formatString - date-fns format string
 * @returns Formatted date string
 */
export const formatDate = (dateString: string, formatString = 'dd/MM/yyyy'): string => {
  try {
    const date = parseISO(dateString);
    return format(date, formatString);
  } catch (error) {
    console.error('Error formatting date:', error);
    return dateString;
  }
};

/**
 * Format date to Hebrew long format
 * @param dateString - ISO date string
 * @returns Formatted Hebrew date string
 */
export const formatDateHebrew = (dateString: string): string => {
  try {
    const date = parseISO(dateString);
    return new Intl.DateTimeFormat('he-IL', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    }).format(date);
  } catch (error) {
    console.error('Error formatting Hebrew date:', error);
    return dateString;
  }
};

/**
 * Truncate text to specified length
 * @param text - Text to truncate
 * @param maxLength - Maximum length
 * @returns Truncated text with ellipsis
 */
export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
};

/**
 * Format phone number for display
 * @param phone - Phone number string
 * @returns Formatted phone number
 */
export const formatPhoneNumber = (phone: string): string => {
  // Remove all non-digit characters
  const cleaned = phone.replace(/\D/g, '');

  // Format as Israeli phone number (xxx-xxx-xxxx)
  if (cleaned.length === 10) {
    return `${cleaned.slice(0, 3)}-${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
  }

  return phone;
};

/**
 * Get initials from name
 * @param firstName - First name
 * @param lastName - Last name
 * @returns Initials (e.g., "AB")
 */
export const getInitials = (firstName: string, lastName: string): string => {
  return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
};
