/**
 * Receipt Management System - Type Definitions
 * 
 * Complete TypeScript type system for the Tik-Tax receipt processing,
 * OCR extraction, categorization, and archiving functionality.
 * 
 * @module receipt.types
 */

// ============================================================================
// ENUMS & BASIC TYPES
// ============================================================================

/**
 * Receipt processing status
 * 
 * @typedef {string} ReceiptStatus
 * - `processing`: OCR extraction in progress
 * - `review`: Awaiting user confirmation of extracted data
 * - `approved`: User approved, archived with digital signature
 * - `failed`: Processing failed (OCR error, invalid image, etc.)
 * - `duplicate`: Detected as duplicate of existing receipt
 */
export type ReceiptStatus = 
  | 'processing'    // OCR in progress
  | 'review'        // Awaiting user confirmation
  | 'approved'      // User approved, archived
  | 'failed'        // Processing failed
  | 'duplicate';    // Detected as duplicate

/**
 * Confidence level for OCR extracted fields
 * 
 * @typedef {string} ConfidenceLevel
 * - `high`: 90%+ confidence (green indicator)
 * - `medium`: 70-89% confidence (yellow indicator, review recommended)
 * - `low`: <70% confidence (red indicator, manual verification required)
 */
export type ConfidenceLevel = 'high' | 'medium' | 'low';

// ============================================================================
// CATEGORY SYSTEM
// ============================================================================

/**
 * Expense category definition (bilingual Hebrew/English)
 * 
 * Categories are used for:
 * - Automatic receipt classification
 * - Filtering and grouping in archive
 * - Statistics and reporting
 * - Export organization
 * 
 * @interface ExpenseCategory
 */
export interface ExpenseCategory {
  /** Unique category identifier (kebab-case) */
  id: string;
  
  /** Category name in Hebrew (primary language) */
  nameHe: string;
  
  /** Category name in English (secondary language) */
  nameEn: string;
  
  /** Lucide icon name (e.g., 'Package', 'Briefcase') */
  icon: string;
  
  /** Hex color for UI display (e.g., '#3B82F6') */
  color: string;
  
  /** Display order (1-based index) */
  sortOrder: number;
}

// ============================================================================
// OCR DATA STRUCTURES
// ============================================================================

/**
 * OCR extracted data with confidence scores
 * 
 * Represents raw data extracted from receipt image via Google Vision API.
 * All fields include confidence levels to guide user review.
 * 
 * @interface OCRData
 */
export interface OCRData {
  /** Business/vendor name */
  vendorName: string;
  
  /** Israeli business number (9 digits) */
  businessNumber: string;
  
  /** Receipt date (ISO 8601 or DD/MM/YYYY) */
  date: string;
  
  /** Total amount including VAT (₪) */
  totalAmount: number;
  
  /** VAT amount (₪) */
  vatAmount: number;
  
  /** Pre-VAT amount (₪) */
  preVatAmount: number;
  
  /** Receipt/invoice number */
  receiptNumber: string;
  
  /** Confidence scores for each extracted field */
  confidence: {
    vendorName: ConfidenceLevel;
    businessNumber: ConfidenceLevel;
    date: ConfidenceLevel;
    totalAmount: ConfidenceLevel;
    vatAmount: ConfidenceLevel;
    receiptNumber: ConfidenceLevel;
    /** Overall extraction confidence (lowest of all fields) */
    overall: ConfidenceLevel;
  };
}

// ============================================================================
// RECEIPT ENTITY (MAIN)
// ============================================================================

/**
 * Complete receipt entity
 * 
 * Main data structure representing a processed receipt in the system.
 * Includes:
 * - Original image data
 * - Extracted/validated data
 * - Classification and categorization
 * - Archive information (PDF, digital signature)
 * - Full audit trail
 * 
 * @interface Receipt
 */
export interface Receipt {
  /** Unique receipt identifier (UUID) */
  id: string;
  
  /** Owner user ID */
  userId: string;
  
  // --- Image Data ---
  
  /** URL to original receipt image (S3) */
  imageUrl: string;
  
  /** Original uploaded filename */
  originalFileName: string;
  
  /** File size in bytes */
  fileSize: number;
  
  // --- Extracted Data ---
  
  /** Business/vendor name */
  vendorName: string;
  
  /** Israeli business number (9 digits) */
  businessNumber: string;
  
  /** Receipt date (ISO 8601) */
  date: string;
  
  /** Total amount including VAT (₪) */
  totalAmount: number;
  
  /** VAT amount (₪) */
  vatAmount: number;
  
  /** Pre-VAT amount (₪) */
  preVatAmount: number;
  
  /** Receipt/invoice number */
  receiptNumber: string;
  
  // --- Classification ---
  
  /** Assigned category ID */
  categoryId: string;
  
  /** Populated category object (optional, for display) */
  category?: ExpenseCategory;
  
  // --- Status & Validation ---
  
  /** Current processing status */
  status: ReceiptStatus;
  
  /** Whether receipt is marked as duplicate */
  isDuplicate: boolean;
  
  /** ID of original receipt if duplicate (optional) */
  duplicateOf?: string;
  
  /** Whether VAT calculation was validated */
  vatValidated: boolean;
  
  // --- Metadata ---
  
  /** User notes (optional, free text) */
  notes?: string;
  
  /** User-defined tags for organization (optional) */
  tags?: string[];
  
  // --- Archive Data ---
  
  /** URL to archived PDF version (optional, after approval) */
  pdfUrl?: string;
  
  /** Digital signature from Israeli CA (optional, after approval) */
  digitalSignature?: string;
  
  /** Timestamp when digitally signed (ISO 8601, optional) */
  signedAt?: string;
  
  // --- Audit Trail ---
  
  /** Receipt creation timestamp (ISO 8601) */
  createdAt: string;
  
  /** Last update timestamp (ISO 8601) */
  updatedAt: string;
  
  /** User approval timestamp (ISO 8601, optional) */
  approvedAt?: string;
  
  // --- Confidence Scores ---
  
  /** OCR confidence scores for review guidance */
  confidence: OCRData['confidence'];
  
  // --- Edit History ---
  
  /** History of manual edits (optional) */
  editHistory?: ReceiptEdit[];
}

/**
 * Receipt edit history entry
 * 
 * Tracks manual corrections made during review process.
 * Used for:
 * - Audit trail
 * - OCR accuracy improvement
 * - User behavior analytics
 * 
 * @interface ReceiptEdit
 */
export interface ReceiptEdit {
  /** Unique edit ID */
  id: string;
  
  /** Parent receipt ID */
  receiptId: string;
  
  /** Field name that was changed */
  fieldChanged: string;
  
  /** Original value (before edit) */
  oldValue: string | number;
  
  /** New value (after edit) */
  newValue: string | number;
  
  /** Timestamp of change (ISO 8601) */
  changedAt: string;
  
  /** User ID who made the change */
  changedBy: string;
}

// ============================================================================
// API REQUEST/RESPONSE TYPES
// ============================================================================

/**
 * Receipt upload request
 * 
 * @interface ReceiptUploadRequest
 */
export interface ReceiptUploadRequest {
  /** Receipt image file (JPEG, PNG, or PDF) */
  file: File;
  
  /** User ID uploading the receipt */
  userId: string;
}

/**
 * Receipt upload response
 * 
 * @interface ReceiptUploadResponse
 */
export interface ReceiptUploadResponse {
  /** Newly created receipt ID */
  receiptId: string;
  
  /** URL to uploaded image */
  imageUrl: string;
  
  /** Success message */
  message: string;
}

/**
 * OCR processing completion response
 * 
 * @interface OCRProcessingResponse
 */
export interface OCRProcessingResponse {
  /** Receipt ID that was processed */
  receiptId: string;
  
  /** New status after processing */
  status: ReceiptStatus;
  
  /** Extracted data with confidence scores */
  extractedData: OCRData;
  
  /** AI-suggested category (optional) */
  suggestedCategory?: ExpenseCategory;
  
  /** Processing time in milliseconds */
  processingTime: number;
}

/**
 * Receipt update request (partial updates)
 * 
 * Used for:
 * - Manual corrections during review
 * - Adding notes/tags
 * - Changing category
 * 
 * @interface ReceiptUpdateRequest
 */
export interface ReceiptUpdateRequest {
  /** Update vendor name (optional) */
  vendorName?: string;
  
  /** Update business number (optional) */
  businessNumber?: string;
  
  /** Update date (optional) */
  date?: string;
  
  /** Update total amount (optional) */
  totalAmount?: number;
  
  /** Update VAT amount (optional) */
  vatAmount?: number;
  
  /** Change category (optional) */
  categoryId?: string;
  
  /** Add/update notes (optional) */
  notes?: string;
  
  /** Add/update tags (optional) */
  tags?: string[];
}

/**
 * Receipt approval request
 * 
 * Triggers:
 * - Archive to secure storage
 * - Digital signature generation
 * - PDF creation
 * - Status change to 'approved'
 * 
 * @interface ReceiptApprovalRequest
 */
export interface ReceiptApprovalRequest {
  /** Receipt ID to approve */
  receiptId: string;
  
  /** Final validated data (includes any manual corrections) */
  finalData: ReceiptUpdateRequest;
}

// ============================================================================
// FILTERING & SORTING
// ============================================================================

/**
 * Receipt archive filter options
 * 
 * All filters are optional and combined with AND logic.
 * 
 * @interface ReceiptFilterOptions
 */
export interface ReceiptFilterOptions {
  /** Filter by start date (ISO 8601, inclusive) */
  startDate?: string;
  
  /** Filter by end date (ISO 8601, inclusive) */
  endDate?: string;
  
  /** Filter by category IDs (OR logic within array) */
  categoryIds?: string[];
  
  /** Minimum amount filter (₪) */
  minAmount?: number;
  
  /** Maximum amount filter (₪) */
  maxAmount?: number;
  
  /** Filter by vendor names (OR logic within array) */
  vendorNames?: string[];
  
  /** Filter by status (OR logic within array) */
  status?: ReceiptStatus[];
  
  /** Full-text search query (searches vendor, notes, receipt number) */
  searchQuery?: string;
}

/**
 * Receipt sort field options
 * 
 * @typedef {string} ReceiptSortField
 */
export type ReceiptSortField = 'date' | 'amount' | 'vendor' | 'createdAt';

/**
 * Sort order direction
 * 
 * @typedef {string} ReceiptSortOrder
 */
export type ReceiptSortOrder = 'asc' | 'desc';

/**
 * Receipt sorting options
 * 
 * @interface ReceiptSortOptions
 */
export interface ReceiptSortOptions {
  /** Field to sort by */
  field: ReceiptSortField;
  
  /** Sort direction */
  order: ReceiptSortOrder;
}

// ============================================================================
// PAGINATION & LISTING
// ============================================================================

/**
 * Paginated receipt list response
 * 
 * @interface ReceiptListResponse
 */
export interface ReceiptListResponse {
  /** Array of receipts for current page */
  receipts: Receipt[];
  
  /** Total count of receipts matching filters */
  total: number;
  
  /** Current page number (1-based) */
  page: number;
  
  /** Items per page */
  pageSize: number;
  
  /** Whether more pages exist */
  hasMore: boolean;
}

// ============================================================================
// STATISTICS & ANALYTICS
// ============================================================================

/**
 * Receipt statistics for dashboard
 * 
 * Provides:
 * - Overall totals
 * - Monthly comparisons
 * - Category breakdown
 * - Recent receipts
 * 
 * @interface ReceiptStatistics
 */
export interface ReceiptStatistics {
  /** Total number of approved receipts */
  totalReceipts: number;
  
  /** Total amount across all receipts (₪) */
  totalAmount: number;
  
  /** Total VAT across all receipts (₪) */
  totalVat: number;
  
  /** Current month statistics */
  thisMonth: {
    /** Count of receipts this month */
    count: number;
    /** Total amount this month (₪) */
    amount: number;
  };
  
  /** Previous month statistics */
  lastMonth: {
    /** Count of receipts last month */
    count: number;
    /** Total amount last month (₪) */
    amount: number;
  };
  
  /** Breakdown by category */
  byCategory: {
    /** Category ID */
    categoryId: string;
    /** Category details */
    category: ExpenseCategory;
    /** Number of receipts in category */
    count: number;
    /** Total amount in category (₪) */
    amount: number;
    /** Percentage of total amount */
    percentage: number;
  }[];
  
  /** Most recent receipts (limited to 5-10) */
  recentReceipts: Receipt[];
}

// ============================================================================
// DUPLICATE DETECTION
// ============================================================================

/**
 * Duplicate detection result
 * 
 * Checks for potential duplicates based on:
 * - Business number + date + amount
 * - Receipt number
 * - Image similarity
 * 
 * @interface DuplicateCheckResult
 */
export interface DuplicateCheckResult {
  /** Whether potential duplicate(s) detected */
  isDuplicate: boolean;
  
  /** Array of potential duplicate receipts */
  duplicateReceipts: Receipt[];
  
  /** Similarity score (0.0 - 1.0) */
  similarityScore: number;
}

// ============================================================================
// EXPORT FUNCTIONALITY
// ============================================================================

/**
 * Export request
 * 
 * @interface ExportRequest
 */
export interface ExportRequest {
  /** Export format */
  format: 'excel' | 'pdf' | 'csv';
  
  /** Filters to apply (same as archive filters) */
  filters: ReceiptFilterOptions;
  
  /** Whether to include receipt images in export */
  includeImages: boolean;
}

/**
 * Export response with download link
 * 
 * @interface ExportResponse
 */
export interface ExportResponse {
  /** Pre-signed download URL (temporary) */
  downloadUrl: string;
  
  /** Generated filename */
  fileName: string;
  
  /** File size in bytes */
  fileSize: number;
  
  /** URL expiration timestamp (ISO 8601) */
  expiresAt: string;
}

// ============================================================================
// VALIDATION HELPERS
// ============================================================================

/**
 * Validate Israeli business number (9 digits)
 * 
 * @param {string} num - Business number to validate
 * @returns {boolean} True if valid 9-digit number
 * 
 * @example
 * isValidBusinessNumber('514932221') // true
 * isValidBusinessNumber('51-493-2221') // true (accepts hyphens)
 * isValidBusinessNumber('12345') // false
 */
export const isValidBusinessNumber = (num: string): boolean => {
  const cleaned = num.replace(/\D/g, '');
  return /^\d{9}$/.test(cleaned);
};

/**
 * Validate receipt date format
 * 
 * Accepts:
 * - DD/MM/YYYY (Israeli format)
 * - YYYY-MM-DD (ISO format)
 * 
 * @param {string} date - Date string to validate
 * @returns {boolean} True if valid format
 * 
 * @example
 * isValidReceiptDate('15/03/2025') // true
 * isValidReceiptDate('2025-03-15') // true
 * isValidReceiptDate('03/15/2025') // false
 */
export const isValidReceiptDate = (date: string): boolean => {
  const ddmmyyyy = /^\d{2}\/\d{2}\/\d{4}$/;
  const yyyymmdd = /^\d{4}-\d{2}-\d{2}$/;
  return ddmmyyyy.test(date) || yyyymmdd.test(date);
};

/**
 * Validate amount is positive number
 * 
 * @param {number} amount - Amount to validate
 * @returns {boolean} True if positive and valid number
 * 
 * @example
 * isValidAmount(100.50) // true
 * isValidAmount(0) // false
 * isValidAmount(-50) // false
 * isValidAmount(NaN) // false
 */
export const isValidAmount = (amount: number): boolean => {
  return amount > 0 && !isNaN(amount);
};

/**
 * Calculate pre-VAT amount from total
 * 
 * Uses Israeli VAT rate of 18%.
 * Formula: preVat = total / 1.18
 * 
 * @param {number} total - Total amount including VAT
 * @returns {number} Pre-VAT amount (rounded to 2 decimals)
 * 
 * @example
 * calculatePreVat(118) // 100.00
 * calculatePreVat(236) // 200.00
 */
export const calculatePreVat = (total: number): number => {
  return Math.round((total / 1.18) * 100) / 100;
};

/**
 * Calculate VAT amount from total
 * 
 * Uses Israeli VAT rate of 18%.
 * Formula: vat = total - (total / 1.18)
 * 
 * @param {number} total - Total amount including VAT
 * @returns {number} VAT amount (rounded to 2 decimals)
 * 
 * @example
 * calculateVat(118) // 18.00
 * calculateVat(236) // 36.00
 */
export const calculateVat = (total: number): number => {
  const preVat = calculatePreVat(total);
  return Math.round((total - preVat) * 100) / 100;
};

/**
 * Validate VAT calculation
 * 
 * Checks if provided VAT matches expected VAT (with ₪1 tolerance).
 * Tolerance accounts for rounding differences on receipts.
 * 
 * @param {number} total - Total amount including VAT
 * @param {number} vat - Claimed VAT amount
 * @returns {boolean} True if VAT is within ₪1 of expected
 * 
 * @example
 * isVatValid(118, 18) // true
 * isVatValid(118, 18.50) // true (within tolerance)
 * isVatValid(118, 20) // false (exceeds tolerance)
 */
export const isVatValid = (total: number, vat: number): boolean => {
  const expectedVat = calculateVat(total);
  return Math.abs(vat - expectedVat) <= 1;
};

/**
 * Format amount to Israeli currency
 * 
 * @param {number} amount - Amount to format
 * @returns {string} Formatted currency string (e.g., "₪100.50")
 * 
 * @example
 * formatAmount(100) // "₪100.00"
 * formatAmount(1234.56) // "₪1,234.56"
 */
export const formatAmount = (amount: number): string => {
  return new Intl.NumberFormat('he-IL', {
    style: 'currency',
    currency: 'ILS',
    minimumFractionDigits: 2
  }).format(amount);
};

/**
 * Format date to Israeli format (DD/MM/YYYY)
 * 
 * @param {string | Date} date - Date to format (ISO string or Date object)
 * @returns {string} Formatted date string (DD/MM/YYYY)
 * 
 * @example
 * formatDateIL('2025-03-15') // "15/03/2025"
 * formatDateIL(new Date(2025, 2, 15)) // "15/03/2025"
 */
export const formatDateIL = (date: string | Date): string => {
  const d = typeof date === 'string' ? new Date(date) : date;
  const day = String(d.getDate()).padStart(2, '0');
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const year = d.getFullYear();
  return `${day}/${month}/${year}`;
};

// ============================================================================
// CONSTANTS
// ============================================================================

/**
 * Default expense categories
 * 
 * Pre-defined categories for Israeli small businesses.
 * Categories are bilingual (Hebrew primary, English secondary).
 * 
 * @constant {ExpenseCategory[]}
 */
export const DEFAULT_CATEGORIES: ExpenseCategory[] = [
  {
    id: 'office-supplies',
    nameHe: 'ציוד משרדי',
    nameEn: 'Office Supplies',
    icon: 'Package',
    color: '#3B82F6',
    sortOrder: 1
  },
  {
    id: 'professional-services',
    nameHe: 'שירותים מקצועיים',
    nameEn: 'Professional Services',
    icon: 'Briefcase',
    color: '#8B5CF6',
    sortOrder: 2
  },
  {
    id: 'marketing',
    nameHe: 'שיווק ופרסום',
    nameEn: 'Marketing & Advertising',
    icon: 'Megaphone',
    color: '#EF4444',
    sortOrder: 3
  },
  {
    id: 'travel',
    nameHe: 'נסיעות ותחבורה',
    nameEn: 'Travel & Transportation',
    icon: 'Car',
    color: '#10B981',
    sortOrder: 4
  },
  {
    id: 'meals',
    nameHe: 'אירוח ואוכל',
    nameEn: 'Meals & Entertainment',
    icon: 'Coffee',
    color: '#F59E0B',
    sortOrder: 5
  },
  {
    id: 'rent',
    nameHe: 'שכירות וחשמל/מים',
    nameEn: 'Rent & Utilities',
    icon: 'Home',
    color: '#6366F1',
    sortOrder: 6
  },
  {
    id: 'equipment',
    nameHe: 'ציוד וטכנולוגיה',
    nameEn: 'Equipment & Technology',
    icon: 'Laptop',
    color: '#06B6D4',
    sortOrder: 7
  },
  {
    id: 'maintenance',
    nameHe: 'תחזוקה ותיקונים',
    nameEn: 'Maintenance & Repairs',
    icon: 'Wrench',
    color: '#84CC16',
    sortOrder: 8
  },
  {
    id: 'insurance',
    nameHe: 'ביטוח',
    nameEn: 'Insurance',
    icon: 'Shield',
    color: '#14B8A6',
    sortOrder: 9
  },
  {
    id: 'bank-fees',
    nameHe: 'עמלות בנקאיות',
    nameEn: 'Bank Fees',
    icon: 'CreditCard',
    color: '#A855F7',
    sortOrder: 10
  },
  {
    id: 'education',
    nameHe: 'הדרכה והכשרה',
    nameEn: 'Education & Training',
    icon: 'GraduationCap',
    color: '#EC4899',
    sortOrder: 11
  },
  {
    id: 'subscriptions',
    nameHe: 'מנויים',
    nameEn: 'Memberships & Subscriptions',
    icon: 'Repeat',
    color: '#F97316',
    sortOrder: 12
  },
  {
    id: 'other',
    nameHe: 'אחר',
    nameEn: 'Other',
    icon: 'MoreHorizontal',
    color: '#6B7280',
    sortOrder: 13
  }
];

/**
 * Israeli VAT rate (standard rate as of 2025)
 * 
 * @constant {number}
 */
export const ISRAELI_VAT_RATE = 0.18; // 18%

/**
 * Maximum file upload size
 * 
 * @constant {number}
 */
export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

/**
 * Allowed file MIME types for upload
 * 
 * @constant {string[]}
 */
export const ALLOWED_FILE_TYPES = ['image/jpeg', 'image/png', 'application/pdf'];

/**
 * Maximum image dimension (width or height)
 * 
 * @constant {number}
 */
export const MAX_IMAGE_DIMENSION = 4096;

/**
 * OCR processing timeout (milliseconds)
 * 
 * @constant {number}
 */
export const OCR_TIMEOUT_MS = 60000; // 60 seconds

/**
 * Polling interval for processing status (milliseconds)
 * 
 * @constant {number}
 */
export const PROCESSING_POLL_INTERVAL = 2000; // 2 seconds
