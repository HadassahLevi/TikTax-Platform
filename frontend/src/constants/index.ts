import type { ReceiptCategory } from '@/types';

// Receipt Categories with Hebrew labels
export const RECEIPT_CATEGORIES: Record<
  ReceiptCategory,
  { label: string; labelHe: string; color: string }
> = {
  'office-supplies': {
    label: 'Office Supplies',
    labelHe: 'ציוד משרדי',
    color: 'bg-blue-100 text-blue-800',
  },
  utilities: {
    label: 'Utilities',
    labelHe: 'חשמל ומים',
    color: 'bg-yellow-100 text-yellow-800',
  },
  equipment: {
    label: 'Equipment',
    labelHe: 'ציוד',
    color: 'bg-purple-100 text-purple-800',
  },
  marketing: {
    label: 'Marketing',
    labelHe: 'שיווק',
    color: 'bg-pink-100 text-pink-800',
  },
  travel: {
    label: 'Travel',
    labelHe: 'נסיעות',
    color: 'bg-indigo-100 text-indigo-800',
  },
  meals: {
    label: 'Meals & Entertainment',
    labelHe: 'ארוחות ואירוח',
    color: 'bg-orange-100 text-orange-800',
  },
  'professional-services': {
    label: 'Professional Services',
    labelHe: 'שירותים מקצועיים',
    color: 'bg-teal-100 text-teal-800',
  },
  rent: {
    label: 'Rent',
    labelHe: 'שכירות',
    color: 'bg-red-100 text-red-800',
  },
  insurance: {
    label: 'Insurance',
    labelHe: 'ביטוח',
    color: 'bg-cyan-100 text-cyan-800',
  },
  software: {
    label: 'Software & Subscriptions',
    labelHe: 'תוכנה ומנויים',
    color: 'bg-violet-100 text-violet-800',
  },
  fuel: {
    label: 'Fuel',
    labelHe: 'דלק',
    color: 'bg-amber-100 text-amber-800',
  },
  maintenance: {
    label: 'Maintenance',
    labelHe: 'תחזוקה',
    color: 'bg-lime-100 text-lime-800',
  },
  other: {
    label: 'Other',
    labelHe: 'אחר',
    color: 'bg-gray-100 text-gray-800',
  },
};

// Status labels
export const RECEIPT_STATUS_LABELS = {
  pending: { label: 'Pending', labelHe: 'ממתין', color: 'bg-yellow-100 text-yellow-800' },
  processing: {
    label: 'Processing',
    labelHe: 'בעיבוד',
    color: 'bg-blue-100 text-blue-800',
  },
  completed: { label: 'Completed', labelHe: 'הושלם', color: 'bg-green-100 text-green-800' },
  failed: { label: 'Failed', labelHe: 'נכשל', color: 'bg-red-100 text-red-800' },
};

// Currency
export const DEFAULT_CURRENCY = 'ILS';
export const CURRENCY_SYMBOL = '₪';

// API Endpoints (relative to base URL)
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    SIGNUP: '/auth/signup',
    REFRESH: '/auth/refresh',
    LOGOUT: '/auth/logout',
  },
  RECEIPTS: {
    LIST: '/receipts',
    CREATE: '/receipts',
    GET: (id: string) => `/receipts/${id}`,
    UPDATE: (id: string) => `/receipts/${id}`,
    DELETE: (id: string) => `/receipts/${id}`,
    PROCESS: '/receipts/process',
    EXPORT: '/receipts/export',
  },
  USER: {
    PROFILE: '/user/profile',
    UPDATE: '/user/update',
  },
} as const;
