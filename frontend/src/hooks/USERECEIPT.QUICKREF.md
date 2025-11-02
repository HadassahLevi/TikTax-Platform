# useReceipt Quick Reference

**Fast lookup for receipt hook usage**

---

## Import

```tsx
import {
  useReceipt,
  useLoadReceipts,
  useLoadStatistics,
  useReceiptValidation,
  useInfiniteScroll,
  useReceiptFilters
} from '@/hooks';
```

---

## Main Hook API

```tsx
const {
  // State
  currentReceipt,      // Receipt | null
  receipts,            // Receipt[]
  total,               // number
  hasMore,             // boolean
  statistics,          // ReceiptStatistics | null
  isUploading,         // boolean
  isProcessing,        // boolean
  isLoadingList,       // boolean
  isLoadingStats,      // boolean
  error,               // string | null
  uploadError,         // string | null
  
  // Actions
  uploadReceipt,       // (file: File) => Promise<string>
  retryProcessing,     // (id: string) => Promise<void>
  setCurrentReceipt,   // (receipt: Receipt | null) => void
  updateCurrentReceipt,// (updates: Partial<Receipt>) => void
  approveReceipt,      // (id: string, data: ReceiptUpdateRequest) => Promise<void>
  deleteReceipt,       // (id: string) => Promise<void>
  fetchReceipts,       // (reset?: boolean) => Promise<void>
  loadMoreReceipts,    // () => Promise<void>
  searchReceipts,      // (query: string) => void
  setFilters,          // (filters: ReceiptFilterOptions) => void
  clearFilters,        // () => void
  setSort,             // (sort: ReceiptSortOptions) => void
  fetchStatistics,     // () => Promise<void>
  clearError           // () => void
} = useReceipt();
```

---

## Common Patterns

### Upload Receipt
```tsx
const { uploadReceipt, isUploading } = useReceipt();

const id = await uploadReceipt(file);
```

### List Receipts (Auto-load)
```tsx
const { receipts } = useLoadReceipts();
```

### Infinite Scroll
```tsx
const { loadMoreReceipts } = useReceipt();
useInfiniteScroll(() => loadMoreReceipts());
```

### Search
```tsx
const { searchReceipts } = useReceipt();
searchReceipts('חשמל'); // min 2 chars
```

### Filter
```tsx
const { updateFilter, clearFilters } = useReceiptFilters();

updateFilter('status', 'approved');
updateFilter('category', 'food');
clearFilters();
```

### Approve
```tsx
const { approveReceipt } = useReceipt();

await approveReceipt(receiptId, {
  amount: 150.50,
  date: '2025-11-02',
  vendorName: 'סופר פארם',
  category: 'health'
});
```

### Delete (with confirmation)
```tsx
const { deleteReceipt } = useReceipt();

deleteReceipt(receiptId); // Shows confirmation
```

### Validate
```tsx
const {
  validateAmount,
  validateDate,
  validateVendorName,
  validateBusinessNumber
} = useReceiptValidation();

const error = validateAmount(amount);
if (error) {
  // Show error: "הסכום חייב להיות גדול מ-0"
}
```

### Statistics (Auto-load)
```tsx
const { statistics } = useLoadStatistics();

console.log(statistics?.totalAmount);
console.log(statistics?.totalReceipts);
```

---

## Validation Rules

| Field | Rule | Error Message (Hebrew) |
|-------|------|----------------------|
| Amount | > 0 | הסכום חייב להיות גדול מ-0 |
| Amount | ≤ 1,000,000 | הסכום גבוה מדי |
| Date | Not future | התאריך לא יכול להיות בעתיד |
| Date | < 7 years old | קבלה ישנה מדי (מעל 7 שנים) |
| Vendor Name | ≥ 2 chars | שם העסק חייב להכיל לפחות 2 תווים |
| Business Number | 9 digits | מספר עסק חייב להכיל 9 ספרות |

---

## Loading States

```tsx
const {
  isUploading,    // File upload in progress
  isProcessing,   // OCR processing
  isLoadingList,  // Fetching receipt list
  isLoadingStats  // Fetching statistics
} = useReceipt();

{isUploading && <Spinner />}
{isProcessing && <ProcessingIndicator />}
```

---

## Error Handling

```tsx
const { error, uploadError, clearError } = useReceipt();

{error && <ErrorAlert message={error} onClose={clearError} />}
{uploadError && <UploadError message={uploadError} />}
```

---

## Filter Options

```typescript
type ReceiptFilterOptions = {
  status?: 'pending' | 'processing' | 'approved' | 'failed';
  category?: string;
  startDate?: string;
  endDate?: string;
  minAmount?: number;
  maxAmount?: number;
  vendorName?: string;
  hasImage?: boolean;
};
```

---

## Sort Options

```typescript
type ReceiptSortOptions = {
  field: 'date' | 'amount' | 'vendorName' | 'createdAt';
  direction: 'asc' | 'desc';
};
```

---

## Complete Example

```tsx
import { useReceipt, useLoadReceipts, useInfiniteScroll } from '@/hooks';

function ReceiptArchive() {
  const { receipts } = useLoadReceipts();
  const {
    total,
    hasMore,
    isLoadingList,
    loadMoreReceipts,
    deleteReceipt
  } = useReceipt();
  
  useInfiniteScroll(() => loadMoreReceipts());
  
  return (
    <div>
      <h1>ארכיון קבלות ({total})</h1>
      
      {receipts.map(receipt => (
        <ReceiptCard
          key={receipt.id}
          receipt={receipt}
          onDelete={() => deleteReceipt(receipt.id)}
        />
      ))}
      
      {isLoadingList && <LoadingSpinner />}
      {!hasMore && <p>זה הכל!</p>}
    </div>
  );
}
```

---

**Quick Ref Version:** 1.0.0  
**Full Docs:** `/src/hooks/USERECEIPT.md`
