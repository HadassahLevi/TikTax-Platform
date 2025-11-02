# Receipt Service Documentation

## Overview
Complete service layer for all receipt-related API operations in Tik-Tax.

**Location:** `/src/services/receipt.service.ts`

## Features
- ✅ Receipt upload with OCR processing
- ✅ Receipt CRUD operations
- ✅ Duplicate detection
- ✅ Advanced search and filtering
- ✅ Statistics and analytics
- ✅ Export to Excel/PDF/CSV
- ✅ Digital signature support
- ✅ Edit history tracking
- ✅ Hebrew error messages
- ✅ Comprehensive timeout handling
- ✅ Full TypeScript typing

---

## Import

```typescript
// Import individual functions
import { uploadReceipt, getReceipts, exportReceipts } from '@/services/receipt.service';

// Or import service object
import { receiptService } from '@/services';
await receiptService.uploadReceipt(file);
```

---

## API Functions

### 📤 Upload & Processing

#### `uploadReceipt(file: File): Promise<ReceiptUploadResponse>`
Upload receipt image for OCR processing.

**Parameters:**
- `file` - Image file (JPG, PNG, PDF - max 10MB)

**Returns:**
- `receiptId` - Unique receipt identifier
- `status` - Processing status ('pending' | 'processing' | 'completed' | 'failed')
- `estimatedTime` - Estimated processing time in seconds

**Example:**
```typescript
const file = event.target.files[0];

try {
  const result = await uploadReceipt(file);
  console.log('Upload successful:', result.receiptId);
  
  // Poll for status
  const intervalId = setInterval(async () => {
    const status = await checkProcessingStatus(result.receiptId);
    
    if (status.status === 'completed') {
      clearInterval(intervalId);
      console.log('Extracted data:', status.extractedData);
    }
  }, 2000);
  
} catch (error) {
  console.error('Upload failed:', error.message); // Hebrew message
}
```

**Errors:**
- `FILE_TOO_LARGE` - "הקובץ גדול מדי (מקסימום 10MB)"
- `INVALID_FILE_TYPE` - "סוג קובץ לא נתמך (רק JPG, PNG, PDF)"
- `NETWORK_ERROR` - "שגיאת רשת. בדוק את החיבור לאינטרנט."

---

#### `checkProcessingStatus(receiptId: string): Promise<OCRProcessingResponse>`
Check OCR processing status.

**Parameters:**
- `receiptId` - Receipt ID from upload

**Returns:**
- `status` - Current status
- `progress` - Progress percentage (0-100)
- `extractedData` - Extracted receipt data (when completed)
- `confidenceScores` - OCR confidence scores per field

**Example:**
```typescript
const status = await checkProcessingStatus('rec_abc123');

if (status.status === 'completed') {
  console.log('Vendor:', status.extractedData.vendorName);
  console.log('Amount:', status.extractedData.totalAmount);
  console.log('Confidence:', status.confidenceScores.overall);
} else if (status.status === 'failed') {
  console.error('Processing failed');
}
```

---

#### `retryProcessing(receiptId: string): Promise<OCRProcessingResponse>`
Retry failed OCR processing.

**Parameters:**
- `receiptId` - Receipt ID to retry

**Returns:**
- New processing response

**Example:**
```typescript
try {
  const result = await retryProcessing('rec_abc123');
  console.log('Retry initiated, status:', result.status);
} catch (error) {
  console.error('Retry failed:', error.message);
}
```

---

### 📋 CRUD Operations

#### `getReceipt(receiptId: string): Promise<Receipt>`
Get complete receipt data by ID.

**Example:**
```typescript
const receipt = await getReceipt('rec_abc123');

console.log(receipt.vendorName);      // "רמי לוי"
console.log(receipt.totalAmount);     // 125.50
console.log(receipt.category);        // "groceries"
console.log(receipt.status);          // "approved"
console.log(receipt.digitalSignature); // "sig_xyz789"
```

---

#### `updateReceipt(receiptId: string, data: ReceiptUpdateRequest): Promise<Receipt>`
Update receipt data (manual corrections).

**Parameters:**
- `receiptId` - Receipt ID
- `data` - Fields to update

**Example:**
```typescript
const updated = await updateReceipt('rec_abc123', {
  vendorName: 'רמי לוי',
  totalAmount: 125.50,
  category: 'groceries',
  notes: 'קניות חודשיות',
  paymentMethod: 'credit-card'
});

console.log('Updated:', updated.updatedAt);
```

**Editable Fields:**
- `vendorName`
- `taxId`
- `totalAmount`
- `vatAmount`
- `date`
- `category`
- `subcategory`
- `paymentMethod`
- `currency`
- `notes`

---

#### `approveReceipt(receiptId: string, finalData: ReceiptUpdateRequest): Promise<Receipt>`
Approve receipt and archive with digital signature.

**Parameters:**
- `receiptId` - Receipt ID
- `finalData` - Final corrected data

**Returns:**
- Approved receipt with digital signature

**Example:**
```typescript
const approved = await approveReceipt('rec_abc123', {
  vendorName: 'רמי לוי',
  totalAmount: 125.50,
  category: 'groceries'
});

console.log('Status:', approved.status); // "approved"
console.log('Signature:', approved.digitalSignature);
console.log('Approved at:', approved.approvedAt);
```

**Important:**
- Once approved, receipt cannot be edited
- Digital signature is generated
- Receipt moves to archive
- Complies with Israeli 7-year storage law

---

#### `deleteReceipt(receiptId: string): Promise<void>`
Delete receipt permanently.

**Example:**
```typescript
await deleteReceipt('rec_abc123');
console.log('Receipt deleted');
```

**Note:** Approved receipts cannot be deleted (legal requirement).

---

### 🔍 Duplicate Detection

#### `checkDuplicate(vendorName: string, date: string, amount: number): Promise<DuplicateCheckResult>`
Check for duplicate receipts.

**Parameters:**
- `vendorName` - Vendor name
- `date` - Receipt date (YYYY-MM-DD format)
- `amount` - Total amount

**Returns:**
- `isDuplicate` - Boolean
- `confidence` - Confidence score (0-100)
- `possibleDuplicates` - Array of potential duplicates

**Example:**
```typescript
const check = await checkDuplicate('רמי לוי', '2024-01-15', 125.50);

if (check.isDuplicate) {
  console.log('Warning: Possible duplicate!');
  console.log('Confidence:', check.confidence);
  
  check.possibleDuplicates.forEach(dup => {
    console.log(`Found: ${dup.vendorName} on ${dup.date} - ₪${dup.totalAmount}`);
  });
  
  // Ask user to confirm
  const shouldContinue = confirm('קבלה דומה כבר קיימת. להמשיך?');
}
```

---

### 📚 List, Search & Filter

#### `getReceipts(filters?, sort?, page?, pageSize?): Promise<ReceiptListResponse>`
Get receipts with advanced filtering, sorting, and pagination.

**Parameters:**
- `filters` - Filter options (optional)
- `sort` - Sort configuration (optional)
- `page` - Page number, 1-indexed (default: 1)
- `pageSize` - Items per page (default: 20)

**Filter Options:**
```typescript
{
  status?: ReceiptStatus[];          // ['pending', 'approved']
  category?: string;                 // 'groceries'
  subcategory?: string;              // 'vegetables'
  dateFrom?: string;                 // '2024-01-01'
  dateTo?: string;                   // '2024-12-31'
  amountMin?: number;                // 50
  amountMax?: number;                // 500
  vendorName?: string;               // 'רמי לוי'
  paymentMethod?: PaymentMethod[];   // ['credit-card']
  hasVAT?: boolean;                  // true
}
```

**Sort Options:**
```typescript
{
  field: 'date' | 'totalAmount' | 'vendorName' | 'createdAt';
  order: 'asc' | 'desc';
}
```

**Example 1: Get recent pending receipts**
```typescript
const receipts = await getReceipts(
  { status: ['pending'] },
  { field: 'date', order: 'desc' },
  1,
  20
);

console.log('Total pending:', receipts.total);
console.log('Receipts:', receipts.receipts);
```

**Example 2: Get groceries from Q1 2024**
```typescript
const q1Groceries = await getReceipts(
  {
    category: 'groceries',
    dateFrom: '2024-01-01',
    dateTo: '2024-03-31'
  },
  { field: 'date', order: 'asc' }
);

const total = q1Groceries.receipts.reduce(
  (sum, r) => sum + r.totalAmount,
  0
);
console.log('Q1 groceries total: ₪', total);
```

**Example 3: Large expenses**
```typescript
const largeExpenses = await getReceipts(
  { amountMin: 1000 },
  { field: 'totalAmount', order: 'desc' }
);
```

**Response:**
```typescript
{
  receipts: Receipt[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
  hasNextPage: boolean;
  hasPreviousPage: boolean;
}
```

---

#### `searchReceipts(query: string, page?, pageSize?): Promise<ReceiptListResponse>`
Full-text search across receipts.

**Searches in:**
- Vendor name
- Category
- Notes
- Reference number

**Example:**
```typescript
// Search for all "רמי לוי" receipts
const results = await searchReceipts('רמי לוי', 1, 20);

console.log(`Found ${results.total} receipts`);

results.receipts.forEach(receipt => {
  console.log(`${receipt.date}: ₪${receipt.totalAmount}`);
});
```

---

### 📊 Statistics & Analytics

#### `getReceiptStatistics(): Promise<ReceiptStatistics>`
Get comprehensive receipt statistics for dashboard.

**Returns:**
```typescript
{
  totalReceipts: number;
  totalAmount: number;
  averageAmount: number;
  byStatus: {
    pending: number;
    approved: number;
    failed: number;
  };
  byCategory: {
    [category: string]: {
      count: number;
      totalAmount: number;
    };
  };
  byMonth: {
    [month: string]: {
      count: number;
      totalAmount: number;
    };
  };
  topVendors: {
    vendorName: string;
    count: number;
    totalAmount: number;
  }[];
}
```

**Example:**
```typescript
const stats = await getReceiptStatistics();

console.log('Total receipts:', stats.totalReceipts);
console.log('Total spent: ₪', stats.totalAmount);
console.log('Average: ₪', stats.averageAmount);

// Category breakdown
Object.entries(stats.byCategory).forEach(([category, data]) => {
  console.log(`${category}: ${data.count} receipts, ₪${data.totalAmount}`);
});

// Top vendors
stats.topVendors.forEach((vendor, i) => {
  console.log(`${i + 1}. ${vendor.vendorName}: ₪${vendor.totalAmount}`);
});
```

---

### 📥 Export Functionality

#### `exportReceipts(request: ExportRequest): Promise<ExportResponse>`
Export receipts to Excel, PDF, or CSV.

**Request:**
```typescript
{
  format: 'excel' | 'pdf' | 'csv';
  filters?: ReceiptFilterOptions;  // Same as getReceipts
  includeImages?: boolean;          // Include receipt images
  groupBy?: 'category' | 'month' | 'vendor';
}
```

**Response:**
```typescript
{
  downloadUrl: string;
  fileName: string;
  fileSize: number;
  expiresAt: string;  // ISO timestamp
}
```

**Example 1: Export all 2024 receipts to Excel**
```typescript
const exportResult = await exportReceipts({
  format: 'excel',
  filters: {
    dateFrom: '2024-01-01',
    dateTo: '2024-12-31'
  },
  includeImages: false
});

// Trigger download
window.location.href = exportResult.downloadUrl;

console.log('File:', exportResult.fileName);
console.log('Size:', exportResult.fileSize / 1024, 'KB');
```

**Example 2: Export Q4 report grouped by category**
```typescript
const q4Report = await exportReceipts({
  format: 'pdf',
  filters: {
    dateFrom: '2024-10-01',
    dateTo: '2024-12-31'
  },
  groupBy: 'category',
  includeImages: true
});

// Download
const link = document.createElement('a');
link.href = q4Report.downloadUrl;
link.download = q4Report.fileName;
link.click();
```

**Limits:**
- Maximum 1000 receipts per export
- Files expire after 24 hours
- Max file size: 50MB

---

#### `downloadReceiptPDF(receiptId: string): Promise<Blob>`
Download digitally signed PDF for a single receipt.

**Example:**
```typescript
const pdfBlob = await downloadReceiptPDF('rec_abc123');

// Create download
const url = URL.createObjectURL(pdfBlob);
const link = document.createElement('a');
link.href = url;
link.download = `receipt_rec_abc123.pdf`;
link.click();

// Clean up
URL.revokeObjectURL(url);
```

---

### 📜 History & Audit

#### `getReceiptHistory(receiptId: string): Promise<Receipt['editHistory']>`
Get complete edit history for a receipt.

**Returns:**
```typescript
Array<{
  timestamp: string;
  userId: string;
  field: string;
  oldValue: any;
  newValue: any;
  action: 'created' | 'updated' | 'approved' | 'deleted';
}>
```

**Example:**
```typescript
const history = await getReceiptHistory('rec_abc123');

history.forEach(edit => {
  const date = new Date(edit.timestamp).toLocaleString('he-IL');
  console.log(`${date}: ${edit.field} changed from "${edit.oldValue}" to "${edit.newValue}"`);
});
```

---

## Error Handling

All functions throw errors with **Hebrew messages** that can be displayed directly to users.

### Error Categories

#### File Upload Errors
```typescript
'FILE_TOO_LARGE' → 'הקובץ גדול מדי (מקסימום 10MB)'
'INVALID_FILE_TYPE' → 'סוג קובץ לא נתמך (רק JPG, PNG, PDF)'
'FILE_CORRUPTED' → 'הקובץ פגום ולא ניתן לקרוא אותו'
```

#### OCR Processing Errors
```typescript
'PROCESSING_FAILED' → 'שגיאה בעיבוד הקבלה. נסה שוב.'
'OCR_NO_TEXT_FOUND' → 'לא נמצא טקסט בקבלה. ודא שהתמונה ברורה.'
'OCR_LOW_CONFIDENCE' → 'איכות הסריקה נמוכה. צלם שוב תמונה ברורה יותר.'
'OCR_TIMEOUT' → 'העיבוד לוקח זמן רב מהרגיל. נסה שוב מאוחר יותר.'
```

#### Receipt Errors
```typescript
'RECEIPT_NOT_FOUND' → 'קבלה לא נמצאה'
'DUPLICATE_RECEIPT' → 'קבלה זו כבר קיימת במערכת'
'RECEIPT_ALREADY_APPROVED' → 'הקבלה כבר אושרה ולא ניתן לערוך'
```

#### Network Errors
```typescript
'NETWORK_ERROR' → 'שגיאת רשת. בדוק את החיבור לאינטרנט.'
'TIMEOUT' → 'הבקשה לקחה זמן רב מדי. נסה שוב.'
'UNAUTHORIZED' → 'נדרשת התחברות מחדש'
```

### Usage Pattern
```typescript
import { uploadReceipt } from '@/services/receipt.service';
import { toast } from '@/hooks/useToast';

try {
  const result = await uploadReceipt(file);
  toast.success('הקבלה הועלתה בהצלחה');
} catch (error) {
  // Error message is already in Hebrew
  toast.error(error.message);
}
```

---

## TypeScript Types

All functions are fully typed. Import types from:
```typescript
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
```

---

## Complete Usage Example

```typescript
import {
  uploadReceipt,
  checkProcessingStatus,
  getReceipt,
  updateReceipt,
  approveReceipt,
  checkDuplicate,
  getReceipts,
  getReceiptStatistics,
  exportReceipts
} from '@/services/receipt.service';

// ============================================================
// UPLOAD FLOW
// ============================================================
async function handleUpload(file: File) {
  try {
    // 1. Upload
    const { receiptId } = await uploadReceipt(file);
    
    // 2. Poll for processing
    const pollInterval = setInterval(async () => {
      const status = await checkProcessingStatus(receiptId);
      
      if (status.status === 'completed') {
        clearInterval(pollInterval);
        
        // 3. Check for duplicates
        const dupCheck = await checkDuplicate(
          status.extractedData.vendorName,
          status.extractedData.date,
          status.extractedData.totalAmount
        );
        
        if (dupCheck.isDuplicate && dupCheck.confidence > 80) {
          const confirm = window.confirm('קבלה דומה כבר קיימת. להמשיך?');
          if (!confirm) return;
        }
        
        // 4. Show review screen
        showReviewScreen(receiptId, status.extractedData);
      }
    }, 2000);
    
  } catch (error) {
    toast.error(error.message);
  }
}

// ============================================================
// REVIEW & APPROVE FLOW
// ============================================================
async function handleApprove(receiptId: string, corrections: any) {
  try {
    // 1. Apply corrections
    const updated = await updateReceipt(receiptId, corrections);
    
    // 2. Approve and archive
    const approved = await approveReceipt(receiptId, corrections);
    
    toast.success('הקבלה אושרה ונשמרה בארכיון');
    
    return approved;
  } catch (error) {
    toast.error(error.message);
  }
}

// ============================================================
// ARCHIVE PAGE
// ============================================================
async function loadArchive(filters: any, page: number) {
  try {
    const receipts = await getReceipts(
      filters,
      { field: 'date', order: 'desc' },
      page,
      20
    );
    
    return receipts;
  } catch (error) {
    toast.error(error.message);
  }
}

// ============================================================
// DASHBOARD
// ============================================================
async function loadDashboard() {
  try {
    const stats = await getReceiptStatistics();
    
    return {
      totalSpent: stats.totalAmount,
      receiptCount: stats.totalReceipts,
      categoryBreakdown: stats.byCategory,
      monthlyTrend: stats.byMonth
    };
  } catch (error) {
    toast.error(error.message);
  }
}

// ============================================================
// EXPORT FOR ACCOUNTANT
// ============================================================
async function exportForAccountant() {
  try {
    const exportResult = await exportReceipts({
      format: 'excel',
      filters: {
        dateFrom: '2024-01-01',
        dateTo: '2024-12-31',
        status: ['approved']
      },
      includeImages: true,
      groupBy: 'category'
    });
    
    // Download
    window.location.href = exportResult.downloadUrl;
    
    toast.success('הקובץ ייוצא בהצלחה');
  } catch (error) {
    toast.error(error.message);
  }
}
```

---

## Testing

```typescript
import { vi, describe, it, expect } from 'vitest';
import { uploadReceipt, getReceipts } from './receipt.service';

describe('Receipt Service', () => {
  it('should upload receipt successfully', async () => {
    const file = new File(['test'], 'receipt.jpg', { type: 'image/jpeg' });
    const result = await uploadReceipt(file);
    
    expect(result.receiptId).toBeDefined();
    expect(result.status).toBe('processing');
  });
  
  it('should get receipts with filters', async () => {
    const receipts = await getReceipts(
      { status: ['approved'] },
      { field: 'date', order: 'desc' }
    );
    
    expect(receipts.total).toBeGreaterThan(0);
    expect(receipts.receipts).toBeInstanceOf(Array);
  });
});
```

---

## Integration with React Components

### Upload Component
```typescript
import { useState } from 'react';
import { uploadReceipt, checkProcessingStatus } from '@/services/receipt.service';

function ReceiptUpload() {
  const [uploading, setUploading] = useState(false);
  
  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    setUploading(true);
    
    try {
      const { receiptId } = await uploadReceipt(file);
      
      // Poll for status
      const interval = setInterval(async () => {
        const status = await checkProcessingStatus(receiptId);
        
        if (status.status === 'completed') {
          clearInterval(interval);
          // Navigate to review
        }
      }, 2000);
      
    } catch (error) {
      toast.error(error.message);
    } finally {
      setUploading(false);
    }
  };
  
  return <input type="file" onChange={handleFileChange} disabled={uploading} />;
}
```

---

## Performance Considerations

- **Timeouts:**
  - Upload: 30 seconds
  - Export: 60 seconds
  - Default: 10 seconds (from axios config)

- **Polling:**
  - Poll status every 2 seconds
  - Stop after 30 attempts (60 seconds total)

- **Pagination:**
  - Default page size: 20 items
  - Maximum page size: 100 items

- **Caching:**
  - Consider using React Query for caching
  - Cache statistics for 5 minutes
  - Cache receipt list for 1 minute

---

## Security Notes

- ✅ All requests authenticated with JWT token (auto-handled by axios interceptor)
- ✅ File size validation (max 10MB)
- ✅ File type validation (JPG, PNG, PDF only)
- ✅ HTTPS required in production
- ✅ Token refresh on 401 (handled by auth service)
- ✅ XSS protection (all data sanitized)

---

## Maintenance

### Adding New Functions
1. Add function to `receipt.service.ts`
2. Add types to `receipt.types.ts`
3. Add error messages to `ERROR_MESSAGES`
4. Update this documentation
5. Export from `services/index.ts`

### Updating Error Messages
Edit `ERROR_MESSAGES` object in `receipt.service.ts`:
```typescript
const ERROR_MESSAGES: Record<string, string> = {
  'NEW_ERROR_CODE': 'הודעת שגיאה בעברית',
  // ...
};
```

---

## Related Files
- **Types:** `/src/types/receipt.types.ts`
- **Axios Config:** `/src/config/axios.ts`
- **Auth Service:** `/src/services/auth.service.ts`

---

**Status:** ✅ Complete and Production-Ready
