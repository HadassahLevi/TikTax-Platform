/**
 * Receipt Service
 * Handles all receipt-related API calls
 * 
 * @module services/receipt.service
 * 
 * Features:
 * - Receipt upload and OCR processing
 * - Receipt CRUD operations
 * - Duplicate detection
 * - Search and filtering
 * - Statistics and analytics
 * - Export functionality (Excel, PDF, CSV)
 * - Hebrew error messages
 * - Request timeout handling
 * 
 * Usage Example:
 * ```typescript
 * import { uploadReceipt, getReceipts } from '@/services/receipt.service';
 * 
 * // Upload receipt
 * const file = event.target.files[0];
 * const result = await uploadReceipt(file);
 * 
 * // Get receipts with filters
 * const receipts = await getReceipts(
 *   { status: ['pending'], category: 'office-supplies' },
 *   { field: 'date', order: 'desc' },
 *   1,
 *   20
 * );
 * ```
 */

import axios from 'axios';
import apiClient from '@/config/axios';
import type {
  Receipt,
  ReceiptUploadResponse,
  OCRProcessingResponse,
  ReceiptUpdateRequest,
  ReceiptFilterOptions,
  ReceiptSortOptions,
  ReceiptListResponse,
  ReceiptStatistics,
  DuplicateCheckResult,
  ExportRequest,
  ExportResponse
} from '@/types/receipt.types';

// ============================================================================
// ERROR HANDLING
// ============================================================================

/**
 * Hebrew error messages mapped to backend error codes
 */
const ERROR_MESSAGES: Record<string, string> = {
  // File upload errors
  'FILE_TOO_LARGE': 'הקובץ גדול מדי (מקסימום 10MB)',
  'INVALID_FILE_TYPE': 'סוג קובץ לא נתמך (רק JPG, PNG, PDF)',
  'FILE_CORRUPTED': 'הקובץ פגום ולא ניתן לקרוא אותו',
  
  // OCR processing errors
  'PROCESSING_FAILED': 'שגיאה בעיבוד הקבלה. נסה שוב.',
  'OCR_NO_TEXT_FOUND': 'לא נמצא טקסט בקבלה. ודא שהתמונה ברורה.',
  'OCR_LOW_CONFIDENCE': 'איכות הסריקה נמוכה. צלם שוב תמונה ברורה יותר.',
  'OCR_TIMEOUT': 'העיבוד לוקח זמן רב מהרגיל. נסה שוב מאוחר יותר.',
  
  // Receipt errors
  'RECEIPT_NOT_FOUND': 'קבלה לא נמצאה',
  'DUPLICATE_RECEIPT': 'קבלה זו כבר קיימת במערכת',
  'RECEIPT_ALREADY_APPROVED': 'הקבלה כבר אושרה ולא ניתן לערוך',
  'RECEIPT_ARCHIVED': 'לא ניתן לערוך קבלה מאורכבת',
  
  // Validation errors
  'INVALID_DATE': 'תאריך לא תקין',
  'INVALID_AMOUNT': 'סכום לא תקין',
  'INVALID_CATEGORY': 'קטגוריה לא תקינה',
  'MISSING_REQUIRED_FIELD': 'שדה חובה חסר',
  
  // Network & Server errors
  'NETWORK_ERROR': 'שגיאת רשת. בדוק את החיבור לאינטרנט.',
  'TIMEOUT': 'הבקשה לקחה זמן רב מדי. נסה שוב.',
  'UNAUTHORIZED': 'נדרשת התחברות מחדש',
  'FORBIDDEN': 'אין לך הרשאה לבצע פעולה זו',
  'SERVER_ERROR': 'שגיאת שרת. צור קשר עם התמיכה.',
  'SERVICE_UNAVAILABLE': 'השירות אינו זמין כרגע. נסה שוב מאוחר יותר.',
  
  // Export errors
  'EXPORT_FAILED': 'שגיאה בייצוא הנתונים',
  'EXPORT_TOO_MANY_RECEIPTS': 'יותר מדי קבלות לייצוא (מקסימום 1000)',
  'EXPORT_NO_DATA': 'אין נתונים לייצוא',
  
  // Generic
  'UNKNOWN_ERROR': 'שגיאה לא ידועה. נסה שוב.'
};

/**
 * Generic error handler
 * Transforms backend errors to user-friendly Hebrew messages
 */
const handleError = (error: unknown): never => {
  // Log error in development
  if (import.meta.env.DEV) {
    console.error('[Receipt Service Error]:', error);
  }

  // Axios error
  if (axios.isAxiosError(error)) {
    // Network error (no response)
    if (!error.response) {
      if (error.code === 'ECONNABORTED') {
        throw new Error(ERROR_MESSAGES.TIMEOUT);
      }
      throw new Error(ERROR_MESSAGES.NETWORK_ERROR);
    }

    // HTTP status errors
    const status = error.response.status;
    if (status === 401) {
      throw new Error(ERROR_MESSAGES.UNAUTHORIZED);
    }
    if (status === 403) {
      throw new Error(ERROR_MESSAGES.FORBIDDEN);
    }
    if (status === 503) {
      throw new Error(ERROR_MESSAGES.SERVICE_UNAVAILABLE);
    }

    // Backend error code
    const errorCode = error.response?.data?.code;
    if (errorCode && ERROR_MESSAGES[errorCode]) {
      throw new Error(ERROR_MESSAGES[errorCode]);
    }

    // Fallback to generic server error
    throw new Error(ERROR_MESSAGES.SERVER_ERROR);
  }

  // Re-throw if already an Error
  if (error instanceof Error) {
    throw error;
  }

  // Unknown error
  throw new Error(ERROR_MESSAGES.UNKNOWN_ERROR);
};

// ============================================================================
// UPLOAD & PROCESSING
// ============================================================================

/**
 * Upload receipt image for OCR processing
 * 
 * @param file - Image file (JPG, PNG, PDF - max 10MB)
 * @returns Upload response with receipt ID and processing status
 * 
 * @example
 * ```typescript
 * const file = event.target.files[0];
 * const result = await uploadReceipt(file);
 * console.log('Receipt ID:', result.receiptId);
 * 
 * // Poll for processing status
 * const status = await checkProcessingStatus(result.receiptId);
 * ```
 */
export const uploadReceipt = async (file: File): Promise<ReceiptUploadResponse> => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await apiClient.post<ReceiptUploadResponse>(
      '/receipts/upload',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 30000 // 30 seconds for upload
      }
    );
    
    if (import.meta.env.DEV) {
      console.log('[Upload Receipt] Success:', response.data);
    }
    
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

/**
 * Check receipt OCR processing status
 * 
 * @param receiptId - Receipt ID from upload response
 * @returns Processing status and extracted data (if complete)
 * 
 * @example
 * ```typescript
 * const status = await checkProcessingStatus('rec_123');
 * 
 * if (status.status === 'completed') {
 *   console.log('Extracted data:', status.extractedData);
 * } else if (status.status === 'processing') {
 *   console.log('Progress:', status.progress);
 * }
 * ```
 */
export const checkProcessingStatus = async (receiptId: string): Promise<OCRProcessingResponse> => {
  try {
    const response = await apiClient.get<OCRProcessingResponse>(
      `/receipts/${receiptId}/status`
    );
    
    if (import.meta.env.DEV) {
      console.log('[Processing Status]:', response.data);
    }
    
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

/**
 * Retry failed OCR processing
 * 
 * @param receiptId - Receipt ID to retry
 * @returns New processing response
 * 
 * @example
 * ```typescript
 * const result = await retryProcessing('rec_123');
 * console.log('Retry initiated:', result.status);
 * ```
 */
export const retryProcessing = async (receiptId: string): Promise<OCRProcessingResponse> => {
  try {
    const response = await apiClient.post<OCRProcessingResponse>(
      `/receipts/${receiptId}/retry`
    );
    
    if (import.meta.env.DEV) {
      console.log('[Retry Processing]:', response.data);
    }
    
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

// ============================================================================
// RECEIPT CRUD OPERATIONS
// ============================================================================

/**
 * Get receipt by ID
 * 
 * @param receiptId - Receipt ID
 * @returns Complete receipt data
 * 
 * @example
 * ```typescript
 * const receipt = await getReceipt('rec_123');
 * console.log('Vendor:', receipt.vendorName);
 * ```
 */
export const getReceipt = async (receiptId: string): Promise<Receipt> => {
  try {
    const response = await apiClient.get<Receipt>(`/receipts/${receiptId}`);
    
    if (import.meta.env.DEV) {
      console.log('[Get Receipt]:', response.data);
    }
    
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

/**
 * Update receipt data (manual corrections)
 * 
 * @param receiptId - Receipt ID
 * @param data - Fields to update
 * @returns Updated receipt
 * 
 * @example
 * ```typescript
 * const updated = await updateReceipt('rec_123', {
 *   vendorName: 'רמי לוי',
 *   totalAmount: 125.50,
 *   category: 'groceries'
 * });
 * ```
 */
export const updateReceipt = async (
  receiptId: string,
  data: ReceiptUpdateRequest
): Promise<Receipt> => {
  try {
    const response = await apiClient.put<Receipt>(`/receipts/${receiptId}`, data);
    
    if (import.meta.env.DEV) {
      console.log('[Update Receipt]:', response.data);
    }
    
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

/**
 * Approve receipt and archive with digital signature
 * 
 * @param receiptId - Receipt ID
 * @param finalData - Final corrected data
 * @returns Approved receipt with signature
 * 
 * @example
 * ```typescript
 * const approved = await approveReceipt('rec_123', {
 *   vendorName: 'רמי לוי',
 *   totalAmount: 125.50,
 *   category: 'groceries',
 *   notes: 'קניות חודשיות'
 * });
 * console.log('Signature:', approved.digitalSignature);
 * ```
 */
export const approveReceipt = async (
  receiptId: string,
  finalData: ReceiptUpdateRequest
): Promise<Receipt> => {
  try {
    const response = await apiClient.post<Receipt>(
      `/receipts/${receiptId}/approve`,
      finalData
    );
    
    if (import.meta.env.DEV) {
      console.log('[Approve Receipt]:', response.data);
    }
    
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

/**
 * Delete receipt
 * 
 * @param receiptId - Receipt ID to delete
 * 
 * @example
 * ```typescript
 * await deleteReceipt('rec_123');
 * console.log('Receipt deleted');
 * ```
 */
export const deleteReceipt = async (receiptId: string): Promise<void> => {
  try {
    await apiClient.delete(`/receipts/${receiptId}`);
    
    if (import.meta.env.DEV) {
      console.log('[Delete Receipt] Success');
    }
  } catch (error) {
    return handleError(error);
  }
};

// ============================================================================
// DUPLICATE DETECTION
// ============================================================================

/**
 * Check for duplicate receipts
 * 
 * @param vendorName - Vendor name
 * @param date - Receipt date (YYYY-MM-DD)
 * @param amount - Total amount
 * @returns Duplicate check result
 * 
 * @example
 * ```typescript
 * const check = await checkDuplicate('רמי לוי', '2024-01-15', 125.50);
 * 
 * if (check.isDuplicate) {
 *   console.log('Possible duplicates:', check.possibleDuplicates);
 * }
 * ```
 */
export const checkDuplicate = async (
  vendorName: string,
  date: string,
  amount: number
): Promise<DuplicateCheckResult> => {
  try {
    const response = await apiClient.post<DuplicateCheckResult>(
      '/receipts/check-duplicate',
      { vendorName, date, amount }
    );
    
    if (import.meta.env.DEV) {
      console.log('[Check Duplicate]:', response.data);
    }
    
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

// ============================================================================
// LIST, SEARCH & FILTER
// ============================================================================

/**
 * Get user's receipts with filters, sorting, and pagination
 * 
 * @param filters - Filter options (status, category, date range, etc.)
 * @param sort - Sort options (field and order)
 * @param page - Page number (1-indexed)
 * @param pageSize - Items per page
 * @returns Paginated receipt list
 * 
 * @example
 * ```typescript
 * // Get pending receipts, sorted by date (newest first)
 * const receipts = await getReceipts(
 *   { status: ['pending'], category: 'office-supplies' },
 *   { field: 'date', order: 'desc' },
 *   1,
 *   20
 * );
 * 
 * console.log('Total:', receipts.total);
 * console.log('Receipts:', receipts.receipts);
 * ```
 */
export const getReceipts = async (
  filters?: ReceiptFilterOptions,
  sort?: ReceiptSortOptions,
  page: number = 1,
  pageSize: number = 20
): Promise<ReceiptListResponse> => {
  try {
    const response = await apiClient.get<ReceiptListResponse>('/receipts', {
      params: {
        ...filters,
        sortField: sort?.field,
        sortOrder: sort?.order,
        page,
        pageSize
      }
    });
    
    if (import.meta.env.DEV) {
      console.log('[Get Receipts]:', {
        total: response.data.total,
        page: response.data.page,
        count: response.data.receipts.length
      });
    }
    
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

/**
 * Search receipts by text query
 * Searches across vendor name, category, notes, and reference number
 * 
 * @param query - Search query
 * @param page - Page number
 * @param pageSize - Items per page
 * @returns Matching receipts
 * 
 * @example
 * ```typescript
 * const results = await searchReceipts('רמי לוי', 1, 20);
 * console.log('Found:', results.total, 'receipts');
 * ```
 */
export const searchReceipts = async (
  query: string,
  page: number = 1,
  pageSize: number = 20
): Promise<ReceiptListResponse> => {
  try {
    const response = await apiClient.get<ReceiptListResponse>('/receipts/search', {
      params: { query, page, pageSize }
    });
    
    if (import.meta.env.DEV) {
      console.log('[Search Receipts]:', {
        query,
        results: response.data.total
      });
    }
    
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

// ============================================================================
// STATISTICS & ANALYTICS
// ============================================================================

/**
 * Get receipt statistics for dashboard
 * 
 * @returns Statistics (totals, by category, by month, etc.)
 * 
 * @example
 * ```typescript
 * const stats = await getReceiptStatistics();
 * console.log('Total receipts:', stats.totalReceipts);
 * console.log('Total amount:', stats.totalAmount);
 * console.log('By category:', stats.byCategory);
 * ```
 */
export const getReceiptStatistics = async (): Promise<ReceiptStatistics> => {
  try {
    const response = await apiClient.get<ReceiptStatistics>('/receipts/statistics');
    
    if (import.meta.env.DEV) {
      console.log('[Receipt Statistics]:', response.data);
    }
    
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

// ============================================================================
// EXPORT FUNCTIONALITY
// ============================================================================

/**
 * Export receipts to Excel/PDF/CSV
 * 
 * @param request - Export configuration
 * @returns Export response with download URL
 * 
 * @example
 * ```typescript
 * const exportResult = await exportReceipts({
 *   format: 'excel',
 *   filters: {
 *     dateFrom: '2024-01-01',
 *     dateTo: '2024-12-31'
 *   },
 *   includeImages: true
 * });
 * 
 * // Download file
 * window.location.href = exportResult.downloadUrl;
 * ```
 */
export const exportReceipts = async (request: ExportRequest): Promise<ExportResponse> => {
  try {
    const response = await apiClient.post<ExportResponse>(
      '/receipts/export',
      request,
      {
        timeout: 60000 // 60 seconds for export generation
      }
    );
    
    if (import.meta.env.DEV) {
      console.log('[Export Receipts]:', response.data);
    }
    
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

/**
 * Download signed PDF for a single receipt
 * 
 * @param receiptId - Receipt ID
 * @returns PDF blob
 * 
 * @example
 * ```typescript
 * const pdfBlob = await downloadReceiptPDF('rec_123');
 * 
 * // Create download link
 * const url = URL.createObjectURL(pdfBlob);
 * const link = document.createElement('a');
 * link.href = url;
 * link.download = `receipt_${receiptId}.pdf`;
 * link.click();
 * URL.revokeObjectURL(url);
 * ```
 */
export const downloadReceiptPDF = async (receiptId: string): Promise<Blob> => {
  try {
    const response = await apiClient.get(`/receipts/${receiptId}/pdf`, {
      responseType: 'blob',
      timeout: 30000
    });
    
    if (import.meta.env.DEV) {
      console.log('[Download PDF] Success:', response.data.size, 'bytes');
    }
    
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

// ============================================================================
// HISTORY & AUDIT
// ============================================================================

/**
 * Get receipt edit history
 * 
 * @param receiptId - Receipt ID
 * @returns Edit history array
 * 
 * @example
 * ```typescript
 * const history = await getReceiptHistory('rec_123');
 * 
 * history.forEach(edit => {
 *   console.log(`${edit.timestamp}: ${edit.field} changed to ${edit.newValue}`);
 * });
 * ```
 */
export const getReceiptHistory = async (
  receiptId: string
): Promise<Receipt['editHistory']> => {
  try {
    const response = await apiClient.get(`/receipts/${receiptId}/history`);
    
    if (import.meta.env.DEV) {
      console.log('[Receipt History]:', response.data);
    }
    
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

// ============================================================================
// EXPORTS
// ============================================================================

export default {
  // Upload & Processing
  uploadReceipt,
  checkProcessingStatus,
  retryProcessing,
  
  // CRUD
  getReceipt,
  updateReceipt,
  approveReceipt,
  deleteReceipt,
  
  // Duplicate Detection
  checkDuplicate,
  
  // List & Search
  getReceipts,
  searchReceipts,
  
  // Statistics
  getReceiptStatistics,
  
  // Export
  exportReceipts,
  downloadReceiptPDF,
  
  // History
  getReceiptHistory
};
