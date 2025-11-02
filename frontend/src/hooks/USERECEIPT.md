# useReceipt Hook System

Complete React hooks for receipt management in Tik-Tax.

---

## 📦 Available Hooks

### 1. `useReceipt()` - Main Receipt Hook
Primary hook for all receipt operations.

**Returns:**
```typescript
{
  // State
  currentReceipt: Receipt | null;
  receipts: Receipt[];
  total: number;
  hasMore: boolean;
  statistics: ReceiptStatistics | null;
  isUploading: boolean;
  isProcessing: boolean;
  isLoadingList: boolean;
  isLoadingStats: boolean;
  error: string | null;
  uploadError: string | null;
  
  // Actions
  uploadReceipt: (file: File) => Promise<string>;
  retryProcessing: (receiptId: string) => Promise<void>;
  setCurrentReceipt: (receipt: Receipt | null) => void;
  updateCurrentReceipt: (updates: Partial<Receipt>) => void;
  approveReceipt: (receiptId: string, data: ReceiptUpdateRequest) => Promise<void>;
  deleteReceipt: (receiptId: string) => Promise<void>;
  fetchReceipts: (reset?: boolean) => Promise<void>;
  loadMoreReceipts: () => Promise<void>;
  searchReceipts: (query: string) => void;
  setFilters: (filters: ReceiptFilterOptions) => void;
  clearFilters: () => void;
  setSort: (sort: ReceiptSortOptions) => void;
  fetchStatistics: () => Promise<void>;
  clearError: () => void;
}
```

---

## 🎯 Usage Examples

### Example 1: Upload Receipt Component

```tsx
import { useReceipt } from '@/hooks';
import { useState } from 'react';

function UploadReceipt() {
  const { uploadReceipt, isUploading, uploadError } = useReceipt();
  const [file, setFile] = useState<File | null>(null);
  
  const handleUpload = async () => {
    if (!file) return;
    
    try {
      const receiptId = await uploadReceipt(file);
      console.log('Receipt uploaded:', receiptId);
      // Navigate to review page
    } catch (error) {
      console.error('Upload failed:', error);
    }
  };
  
  return (
    <div>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        disabled={isUploading}
      />
      
      <button
        onClick={handleUpload}
        disabled={!file || isUploading}
      >
        {isUploading ? 'מעלה...' : 'העלה קבלה'}
      </button>
      
      {uploadError && (
        <div className="error">{uploadError}</div>
      )}
    </div>
  );
}
```

---

### Example 2: Receipt List with Infinite Scroll

```tsx
import { useReceipt, useLoadReceipts, useInfiniteScroll } from '@/hooks';

function ReceiptList() {
  const { receipts } = useLoadReceipts(); // Auto-loads on mount
  const { loadMoreReceipts, hasMore, isLoadingList } = useReceipt();
  
  // Infinite scroll
  useInfiniteScroll(() => {
    loadMoreReceipts();
  });
  
  return (
    <div>
      {receipts.map(receipt => (
        <ReceiptCard key={receipt.id} receipt={receipt} />
      ))}
      
      {isLoadingList && <LoadingSpinner />}
      {!hasMore && <p>לא נמצאו קבלות נוספות</p>}
    </div>
  );
}
```

---

### Example 3: Dashboard with Statistics

```tsx
import { useLoadStatistics } from '@/hooks';

function Dashboard() {
  const { statistics } = useLoadStatistics(); // Auto-loads on mount
  
  if (!statistics) {
    return <LoadingSpinner />;
  }
  
  return (
    <div>
      <h1>סיכום חודשי</h1>
      
      <div className="stats">
        <StatCard
          title="סה״כ קבלות"
          value={statistics.totalReceipts}
        />
        <StatCard
          title="סה״כ סכום"
          value={`₪${statistics.totalAmount.toLocaleString()}`}
        />
        <StatCard
          title="ממוצע לקבלה"
          value={`₪${statistics.averageAmount.toFixed(2)}`}
        />
      </div>
      
      <CategoryBreakdown data={statistics.byCategory} />
    </div>
  );
}
```

---

### Example 4: Receipt Review with Validation

```tsx
import { useReceipt, useReceiptValidation } from '@/hooks';
import { useState } from 'react';

function ReceiptReview({ receiptId }: { receiptId: string }) {
  const { currentReceipt, approveReceipt, updateCurrentReceipt } = useReceipt();
  const {
    validateAmount,
    validateDate,
    validateVendorName,
    validateBusinessNumber
  } = useReceiptValidation();
  
  const [errors, setErrors] = useState<Record<string, string>>({});
  
  const handleApprove = async () => {
    // Validate all fields
    const newErrors: Record<string, string> = {};
    
    const amountError = validateAmount(currentReceipt?.amount || 0);
    if (amountError) newErrors.amount = amountError;
    
    const dateError = validateDate(currentReceipt?.date || '');
    if (dateError) newErrors.date = dateError;
    
    const vendorError = validateVendorName(currentReceipt?.vendorName || '');
    if (vendorError) newErrors.vendorName = vendorError;
    
    if (currentReceipt?.businessNumber) {
      const businessError = validateBusinessNumber(currentReceipt.businessNumber);
      if (businessError) newErrors.businessNumber = businessError;
    }
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    
    // Approve receipt
    try {
      await approveReceipt(receiptId, {
        amount: currentReceipt!.amount,
        date: currentReceipt!.date,
        vendorName: currentReceipt!.vendorName,
        businessNumber: currentReceipt?.businessNumber,
        category: currentReceipt!.category
      });
      // Navigate to archive
    } catch (error) {
      console.error('Approval failed:', error);
    }
  };
  
  return (
    <div>
      <Input
        label="סכום"
        type="number"
        value={currentReceipt?.amount || 0}
        onChange={(e) => updateCurrentReceipt({ amount: parseFloat(e.target.value) })}
        error={errors.amount}
      />
      
      <Input
        label="שם העסק"
        value={currentReceipt?.vendorName || ''}
        onChange={(e) => updateCurrentReceipt({ vendorName: e.target.value })}
        error={errors.vendorName}
      />
      
      <button onClick={handleApprove}>אשר קבלה</button>
    </div>
  );
}
```

---

### Example 5: Filter Panel

```tsx
import { useReceiptFilters } from '@/hooks';
import { EXPENSE_CATEGORIES } from '@/constants';

function FilterPanel() {
  const {
    filters,
    updateFilter,
    clearFilters,
    hasActiveFilters
  } = useReceiptFilters();
  
  return (
    <div className="filter-panel">
      <h3>סינון</h3>
      
      {/* Status filter */}
      <select
        value={filters.status || ''}
        onChange={(e) => updateFilter('status', e.target.value || undefined)}
      >
        <option value="">כל הסטטוסים</option>
        <option value="pending">ממתין לאישור</option>
        <option value="approved">מאושר</option>
        <option value="processing">בעיבוד</option>
      </select>
      
      {/* Category filter */}
      <select
        value={filters.category || ''}
        onChange={(e) => updateFilter('category', e.target.value || undefined)}
      >
        <option value="">כל הקטגוריות</option>
        {EXPENSE_CATEGORIES.map(cat => (
          <option key={cat.id} value={cat.id}>
            {cat.nameHe}
          </option>
        ))}
      </select>
      
      {/* Date range */}
      <input
        type="date"
        value={filters.startDate || ''}
        onChange={(e) => updateFilter('startDate', e.target.value || undefined)}
      />
      
      <input
        type="date"
        value={filters.endDate || ''}
        onChange={(e) => updateFilter('endDate', e.target.value || undefined)}
      />
      
      {/* Amount range */}
      <input
        type="number"
        placeholder="סכום מינימלי"
        value={filters.minAmount || ''}
        onChange={(e) => updateFilter('minAmount', e.target.value ? parseFloat(e.target.value) : undefined)}
      />
      
      <input
        type="number"
        placeholder="סכום מקסימלי"
        value={filters.maxAmount || ''}
        onChange={(e) => updateFilter('maxAmount', e.target.value ? parseFloat(e.target.value) : undefined)}
      />
      
      {/* Clear filters */}
      {hasActiveFilters() && (
        <button onClick={clearFilters}>
          נקה סינון
        </button>
      )}
    </div>
  );
}
```

---

### Example 6: Search with Debounce

```tsx
import { useReceipt } from '@/hooks';
import { useState, useEffect } from 'react';

function SearchBar() {
  const { searchReceipts, receipts, isLoadingList } = useReceipt();
  const [query, setQuery] = useState('');
  
  // Debounce search
  useEffect(() => {
    const timer = setTimeout(() => {
      searchReceipts(query);
    }, 300);
    
    return () => clearTimeout(timer);
  }, [query, searchReceipts]);
  
  return (
    <div>
      <input
        type="search"
        placeholder="חיפוש קבלות..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      
      {isLoadingList && <LoadingSpinner />}
      
      {query && receipts.length === 0 && !isLoadingList && (
        <p>לא נמצאו תוצאות עבור "{query}"</p>
      )}
    </div>
  );
}
```

---

### Example 7: Delete Receipt with Confirmation

```tsx
import { useReceipt } from '@/hooks';

function ReceiptCard({ receipt }: { receipt: Receipt }) {
  const { deleteReceipt } = useReceipt();
  
  // deleteReceipt already includes confirmation dialog
  const handleDelete = () => {
    deleteReceipt(receipt.id);
  };
  
  return (
    <div className="receipt-card">
      <h3>{receipt.vendorName}</h3>
      <p>₪{receipt.amount}</p>
      
      <button onClick={handleDelete} className="btn-danger">
        מחק
      </button>
    </div>
  );
}
```

---

### Example 8: Retry Failed Processing

```tsx
import { useReceipt } from '@/hooks';

function FailedReceiptCard({ receipt }: { receipt: Receipt }) {
  const { retryProcessing, isProcessing } = useReceipt();
  
  const handleRetry = async () => {
    try {
      await retryProcessing(receipt.id);
      console.log('Processing restarted');
    } catch (error) {
      console.error('Retry failed:', error);
    }
  };
  
  return (
    <div className="receipt-card error">
      <h3>עיבוד נכשל</h3>
      <p>{receipt.vendorName}</p>
      
      <button
        onClick={handleRetry}
        disabled={isProcessing}
      >
        {isProcessing ? 'מעבד...' : 'נסה שוב'}
      </button>
    </div>
  );
}
```

---

## 🔧 Hook Details

### `useLoadReceipts()`
Auto-loads receipts on component mount if store is empty.

**Use when:**
- Mounting receipt list pages
- Need receipts available immediately
- Don't want manual fetch calls

**Example:**
```tsx
function Archive() {
  const { receipts } = useLoadReceipts();
  
  return <ReceiptList receipts={receipts} />;
}
```

---

### `useLoadStatistics()`
Auto-loads statistics on component mount if not already loaded.

**Use when:**
- Mounting dashboard
- Displaying summary cards
- Need stats available immediately

**Example:**
```tsx
function Dashboard() {
  const { statistics } = useLoadStatistics();
  
  return <StatsPanel stats={statistics} />;
}
```

---

### `useReceiptValidation()`
Provides validation functions for receipt fields.

**Functions:**
- `validateAmount(amount: number): string | null`
- `validateDate(date: string): string | null`
- `validateVendorName(name: string): string | null`
- `validateBusinessNumber(num: string): string | null`

**Returns:**
- `null` if valid
- Error message string if invalid

**Example:**
```tsx
const { validateAmount } = useReceiptValidation();

const error = validateAmount(amount);
if (error) {
  setError(error); // "הסכום חייב להיות גדול מ-0"
}
```

---

### `useInfiniteScroll(callback: () => void)`
Automatically triggers callback when scrolling near page bottom.

**Parameters:**
- `callback` - Function to call (usually `loadMoreReceipts`)

**Behavior:**
- Triggers when 500px from bottom
- Only if `hasMore === true`
- Only if not currently loading

**Example:**
```tsx
function ReceiptList() {
  const { loadMoreReceipts } = useReceipt();
  
  useInfiniteScroll(() => {
    loadMoreReceipts();
  });
  
  return <div>...</div>;
}
```

---

### `useReceiptFilters()`
Manages receipt filter state.

**Returns:**
```typescript
{
  filters: ReceiptFilterOptions;
  updateFilter: (key, value) => void;
  clearFilters: () => void;
  hasActiveFilters: () => boolean;
}
```

**Example:**
```tsx
const { filters, updateFilter, clearFilters, hasActiveFilters } = useReceiptFilters();

// Update single filter
updateFilter('status', 'approved');
updateFilter('category', 'food');

// Check if any filters active
if (hasActiveFilters()) {
  // Show "Clear Filters" button
}

// Clear all filters
clearFilters();
```

---

## 🎨 Pattern Recommendations

### ✅ DO:
```tsx
// Use hooks at component level
function MyComponent() {
  const { receipts, uploadReceipt } = useReceipt();
  return <div>...</div>;
}

// Combine hooks for complex features
function Dashboard() {
  const { statistics } = useLoadStatistics();
  const { receipts } = useLoadReceipts();
  const { hasActiveFilters, clearFilters } = useReceiptFilters();
  
  return <DashboardView />;
}
```

### ❌ DON'T:
```tsx
// Don't use hooks in conditionals
function MyComponent() {
  if (condition) {
    const { receipts } = useReceipt(); // ❌ Error
  }
}

// Don't use hooks in callbacks
function MyComponent() {
  const handleClick = () => {
    const { uploadReceipt } = useReceipt(); // ❌ Error
  };
}
```

---

## 🔐 Security Notes

1. **File Upload:**
   - `uploadReceipt()` handles validation
   - Max 10MB enforced
   - Only image types allowed

2. **Deletion:**
   - `deleteReceipt()` includes confirmation
   - User must confirm before deletion
   - No undo available

3. **Validation:**
   - Always validate before approval
   - Use `useReceiptValidation()` helpers
   - Show clear error messages

---

## 🐛 Error Handling

All hooks handle errors gracefully:

```tsx
const { error, uploadError, clearError } = useReceipt();

// Display errors
{error && <ErrorAlert message={error} onClose={clearError} />}
{uploadError && <ErrorAlert message={uploadError} />}

// Handle in try-catch
try {
  await uploadReceipt(file);
} catch (err) {
  console.error('Upload failed:', err);
  // Error automatically set in store
}
```

---

## 📚 Related Documentation

- **Receipt Store:** `/src/stores/RECEIPT_STORE.md`
- **Receipt Service:** `/src/services/RECEIPT_SERVICE.md`
- **Receipt Types:** `/src/types/RECEIPT_TYPES.md`
- **Design System:** `/.github/instructions/design_rules_.instructions.md`

---

**Last Updated:** 2025-11-02
**Version:** 1.0.0
**Status:** ✅ Complete
