// Global type definitions for Tik-Tax

// ============================================================================
// AUTH TYPES
// ============================================================================

// Re-export auth types from dedicated module
export type {
  User,
  SignupData,
  AuthState
} from './auth.types';

// ============================================================================
// RECEIPT TYPES
// ============================================================================

// Re-export receipt types from dedicated module
export type {
  ReceiptStatus,
  ConfidenceLevel,
  ExpenseCategory,
  OCRData,
  Receipt,
  ReceiptEdit,
  ReceiptUploadRequest,
  ReceiptUploadResponse,
  OCRProcessingResponse,
  ReceiptUpdateRequest,
  ReceiptApprovalRequest,
  ReceiptFilterOptions,
  ReceiptSortField,
  ReceiptSortOrder,
  ReceiptSortOptions,
  ReceiptListResponse,
  ReceiptStatistics,
  DuplicateCheckResult,
  ExportRequest,
  ExportResponse
} from './receipt.types';

// Re-export receipt constants
export {
  DEFAULT_CATEGORIES,
  ISRAELI_VAT_RATE,
  MAX_FILE_SIZE,
  ALLOWED_FILE_TYPES,
  MAX_IMAGE_DIMENSION,
  OCR_TIMEOUT_MS,
  PROCESSING_POLL_INTERVAL,
  isValidBusinessNumber,
  isValidReceiptDate,
  isValidAmount,
  calculatePreVat,
  calculateVat,
  isVatValid,
  formatAmount,
  formatDateIL
} from './receipt.types';

// ============================================================================
// CONFIGURATION TYPES
// ============================================================================

export interface Config {
  // API Configuration
  apiBaseUrl: string;

  // External Services
  googleCloudVisionApiKey: string;
  stripePublicKey: string;
  awsS3Bucket: string;

  // Feature Flags
  enableAnalytics: boolean;
  maintenanceMode: boolean;

  // Environment
  isDevelopment: boolean;
  isProduction: boolean;
  isTest: boolean;
}

// ============================================================================
// API RESPONSE TYPES
// ============================================================================

/**
 * Generic API response wrapper
 */
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

/**
 * API error response
 */
export interface ApiError {
  success: false;
  error: string;
  message: string;
  statusCode: number;
}

// ============================================================================
// PAGINATION TYPES
// ============================================================================

/**
 * Pagination query parameters
 */
export interface PaginationParams {
  page: number;
  limit: number;
}

/**
 * Paginated response wrapper
 */
export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}
