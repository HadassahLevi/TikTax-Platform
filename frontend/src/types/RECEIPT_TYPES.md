# Receipt Types Documentation

Complete TypeScript type system for the Tik-Tax receipt management system.

---

## 📁 File Location

`/src/types/receipt.types.ts`

---

## 📋 Overview

This module provides comprehensive type definitions for:
- Receipt entities and status tracking
- OCR data extraction and confidence scoring
- Expense categorization (13 categories, bilingual)
- Filtering, sorting, and pagination
- Statistics and analytics
- Export functionality
- Israeli VAT validation

---

## 🔑 Core Types

### Status Types

```typescript
type ReceiptStatus = 
  | 'processing'  // OCR in progress
  | 'review'      // Awaiting user confirmation
  | 'approved'    // User approved, archived
  | 'failed'      // Processing failed
  | 'duplicate'   // Detected as duplicate

type ConfidenceLevel = 'high' | 'medium' | 'low'
```

### Receipt Entity

Main receipt object with all data:

```typescript
interface Receipt {
  id: string;
  userId: string;
  
  // Image data
  imageUrl: string;
  originalFileName: string;
  fileSize: number;
  
  // Extracted data
  vendorName: string;
  businessNumber: string;
  date: string;
  totalAmount: number;
  vatAmount: number;
  preVatAmount: number;
  receiptNumber: string;
  
  // Classification
  categoryId: string;
  category?: ExpenseCategory;
  
  // Status & validation
  status: ReceiptStatus;
  isDuplicate: boolean;
  duplicateOf?: string;
  vatValidated: boolean;
  
  // Metadata
  notes?: string;
  tags?: string[];
  
  // Archive data
  pdfUrl?: string;
  digitalSignature?: string;
  signedAt?: string;
  
  // Audit trail
  createdAt: string;
  updatedAt: string;
  approvedAt?: string;
  
  // Confidence scores
  confidence: OCRData['confidence'];
  
  // Edit history
  editHistory?: ReceiptEdit[];
}
```

---

## 📊 Category System

### ExpenseCategory Interface

```typescript
interface ExpenseCategory {
  id: string;
  nameHe: string;      // Hebrew name (primary)
  nameEn: string;      // English name (secondary)
  icon: string;        // Lucide icon name
  color: string;       // Hex color
  sortOrder: number;   // Display order
}
```

### 13 Default Categories

1. **Office Supplies** (ציוד משרדי) - `#3B82F6`
2. **Professional Services** (שירותים מקצועיים) - `#8B5CF6`
3. **Marketing & Advertising** (שיווק ופרסום) - `#EF4444`
4. **Travel & Transportation** (נסיעות ותחבורה) - `#10B981`
5. **Meals & Entertainment** (אירוח ואוכל) - `#F59E0B`
6. **Rent & Utilities** (שכירות וחשמל/מים) - `#6366F1`
7. **Equipment & Technology** (ציוד וטכנולוגיה) - `#06B6D4`
8. **Maintenance & Repairs** (תחזוקה ותיקונים) - `#84CC16`
9. **Insurance** (ביטוח) - `#14B8A6`
10. **Bank Fees** (עמלות בנקאיות) - `#A855F7`
11. **Education & Training** (הדרכה והכשרה) - `#EC4899`
12. **Memberships & Subscriptions** (מנויים) - `#F97316`
13. **Other** (אחר) - `#6B7280`

Access via:
```typescript
import { DEFAULT_CATEGORIES } from '@/types';
```

---

## 🔍 OCR & Processing

### OCRData Interface

```typescript
interface OCRData {
  vendorName: string;
  businessNumber: string;
  date: string;
  totalAmount: number;
  vatAmount: number;
  preVatAmount: number;
  receiptNumber: string;
  confidence: {
    vendorName: ConfidenceLevel;
    businessNumber: ConfidenceLevel;
    date: ConfidenceLevel;
    totalAmount: ConfidenceLevel;
    vatAmount: ConfidenceLevel;
    receiptNumber: ConfidenceLevel;
    overall: ConfidenceLevel;  // Lowest of all fields
  };
}
```

### Processing Response

```typescript
interface OCRProcessingResponse {
  receiptId: string;
  status: ReceiptStatus;
  extractedData: OCRData;
  suggestedCategory?: ExpenseCategory;
  processingTime: number;  // milliseconds
}
```

---

## 🔧 API Types

### Upload

```typescript
interface ReceiptUploadRequest {
  file: File;
  userId: string;
}

interface ReceiptUploadResponse {
  receiptId: string;
  imageUrl: string;
  message: string;
}
```

### Update & Approval

```typescript
interface ReceiptUpdateRequest {
  vendorName?: string;
  businessNumber?: string;
  date?: string;
  totalAmount?: number;
  vatAmount?: number;
  categoryId?: string;
  notes?: string;
  tags?: string[];
}

interface ReceiptApprovalRequest {
  receiptId: string;
  finalData: ReceiptUpdateRequest;
}
```

---

## 🔎 Filtering & Sorting

### Filter Options

```typescript
interface ReceiptFilterOptions {
  startDate?: string;          // ISO 8601
  endDate?: string;            // ISO 8601
  categoryIds?: string[];      // OR logic
  minAmount?: number;          // ₪
  maxAmount?: number;          // ₪
  vendorNames?: string[];      // OR logic
  status?: ReceiptStatus[];    // OR logic
  searchQuery?: string;        // Full-text search
}
```

### Sort Options

```typescript
type ReceiptSortField = 'date' | 'amount' | 'vendor' | 'createdAt';
type ReceiptSortOrder = 'asc' | 'desc';

interface ReceiptSortOptions {
  field: ReceiptSortField;
  order: ReceiptSortOrder;
}
```

### Paginated Response

```typescript
interface ReceiptListResponse {
  receipts: Receipt[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}
```

---

## 📈 Statistics

```typescript
interface ReceiptStatistics {
  totalReceipts: number;
  totalAmount: number;        // ₪
  totalVat: number;          // ₪
  
  thisMonth: {
    count: number;
    amount: number;
  };
  
  lastMonth: {
    count: number;
    amount: number;
  };
  
  byCategory: {
    categoryId: string;
    category: ExpenseCategory;
    count: number;
    amount: number;
    percentage: number;
  }[];
  
  recentReceipts: Receipt[];
}
```

---

## 📤 Export

```typescript
interface ExportRequest {
  format: 'excel' | 'pdf' | 'csv';
  filters: ReceiptFilterOptions;
  includeImages: boolean;
}

interface ExportResponse {
  downloadUrl: string;        // Pre-signed S3 URL
  fileName: string;
  fileSize: number;
  expiresAt: string;         // ISO 8601
}
```

---

## ✅ Validation Helpers

### Business Number Validation

```typescript
isValidBusinessNumber('514932221')  // true
isValidBusinessNumber('51-493-2221') // true (accepts hyphens)
isValidBusinessNumber('12345')       // false
```

### Date Validation

```typescript
isValidReceiptDate('15/03/2025')  // true (DD/MM/YYYY)
isValidReceiptDate('2025-03-15')  // true (ISO)
isValidReceiptDate('03/15/2025')  // false
```

### Amount Validation

```typescript
isValidAmount(100.50)  // true
isValidAmount(0)       // false
isValidAmount(-50)     // false
```

### VAT Calculations

Israeli VAT rate: **18%**

```typescript
// Calculate pre-VAT amount
calculatePreVat(118)  // 100.00

// Calculate VAT amount
calculateVat(118)     // 18.00

// Validate VAT (₪1 tolerance)
isVatValid(118, 18)     // true
isVatValid(118, 18.50)  // true (within tolerance)
isVatValid(118, 20)     // false
```

### Formatting

```typescript
// Format amount to ILS
formatAmount(1234.56)  // "₪1,234.56"

// Format date to Israeli format
formatDateIL('2025-03-15')  // "15/03/2025"
formatDateIL(new Date())    // "02/11/2025"
```

---

## 🔢 Constants

```typescript
// VAT rate
ISRAELI_VAT_RATE = 0.18  // 18%

// File upload constraints
MAX_FILE_SIZE = 10 * 1024 * 1024  // 10MB
ALLOWED_FILE_TYPES = ['image/jpeg', 'image/png', 'application/pdf']
MAX_IMAGE_DIMENSION = 4096

// Processing timeouts
OCR_TIMEOUT_MS = 60000              // 60 seconds
PROCESSING_POLL_INTERVAL = 2000     // 2 seconds
```

---

## 📦 Usage Examples

### Import Types

```typescript
import type {
  Receipt,
  ReceiptStatus,
  ExpenseCategory,
  ReceiptFilterOptions,
  ReceiptStatistics
} from '@/types';
```

### Import Constants

```typescript
import {
  DEFAULT_CATEGORIES,
  ISRAELI_VAT_RATE,
  isValidBusinessNumber,
  calculateVat,
  formatAmount
} from '@/types';
```

### Create Filter

```typescript
const filters: ReceiptFilterOptions = {
  startDate: '2025-01-01',
  endDate: '2025-12-31',
  categoryIds: ['office-supplies', 'equipment'],
  minAmount: 100,
  status: ['approved']
};
```

### Validate Receipt Data

```typescript
const isValid = 
  isValidBusinessNumber(receipt.businessNumber) &&
  isValidReceiptDate(receipt.date) &&
  isValidAmount(receipt.totalAmount) &&
  isVatValid(receipt.totalAmount, receipt.vatAmount);
```

### Display Category

```typescript
const category = DEFAULT_CATEGORIES.find(c => c.id === receipt.categoryId);

<div style={{ color: category.color }}>
  <Icon name={category.icon} />
  {category.nameHe}
</div>
```

---

## 🎯 Type Safety Benefits

1. **Autocomplete**: Full IntelliSense in VS Code
2. **Compile-time validation**: Catch errors before runtime
3. **Refactoring safety**: Rename with confidence
4. **Documentation**: JSDoc comments on all types
5. **Consistency**: Single source of truth

---

## 🔗 Related Files

- `/src/types/auth.types.ts` - Authentication types
- `/src/types/index.ts` - Central type exports
- `/src/services/receipt.service.ts` - Receipt API service (uses these types)
- `/src/stores/receipt.store.ts` - Receipt state management (uses these types)

---

## 📝 Notes

- All dates use **ISO 8601** format internally
- Display dates use **DD/MM/YYYY** (Israeli format)
- All amounts in **Israeli Shekel (₪)**
- Hebrew text is **primary** language
- VAT rate is **18%** as of 2025
- Business numbers must be **9 digits**

---

**Created**: November 2, 2025  
**Version**: 1.0.0  
**Status**: ✅ Production Ready
