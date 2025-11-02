// Global type definitions for Tik-Tax

// User Types
export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  phone?: string;
  businessName?: string;
  createdAt: string;
  updatedAt: string;
}

// Receipt Types
export interface Receipt {
  id: string;
  userId: string;
  businessName: string;
  amount: number;
  currency: string;
  date: string;
  category: ReceiptCategory;
  status: ReceiptStatus;
  imageUrl: string;
  ocrData: OCRData;
  verified: boolean;
  createdAt: string;
  updatedAt: string;
}

export type ReceiptCategory =
  | 'office-supplies'
  | 'utilities'
  | 'equipment'
  | 'marketing'
  | 'travel'
  | 'meals'
  | 'professional-services'
  | 'rent'
  | 'insurance'
  | 'software'
  | 'fuel'
  | 'maintenance'
  | 'other';

export type ReceiptStatus = 'pending' | 'processing' | 'completed' | 'failed';

export interface OCRData {
  businessName?: string;
  amount?: number;
  date?: string;
  taxId?: string;
  confidence: number;
  rawText: string;
}

// Auth Types
export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupData {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  businessName?: string;
  phone?: string;
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

export interface ApiError {
  success: false;
  error: string;
  message: string;
  statusCode: number;
}

// Pagination Types
export interface PaginationParams {
  page: number;
  limit: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

// Filter Types
export interface ReceiptFilters {
  category?: ReceiptCategory;
  status?: ReceiptStatus;
  dateFrom?: string;
  dateTo?: string;
  minAmount?: number;
  maxAmount?: number;
  searchQuery?: string;
}
