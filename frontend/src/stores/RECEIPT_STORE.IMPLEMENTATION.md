# Receipt Store - Implementation Guide

## Overview

The Receipt Store is a Zustand-based state management solution for the Tik-Tax receipt processing system. It handles:

- ✅ Receipt upload with progress tracking
- ✅ Automatic OCR processing status polling
- ✅ Receipt list management with pagination
- ✅ Advanced search and filtering
- ✅ Statistics caching
- ✅ Optimistic updates
- ✅ Error handling with Hebrew messages
- ✅ DevTools integration

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Receipt Store (Zustand)                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  STATE                                                        │
│  ├── currentReceipt (Receipt being processed)                │
│  ├── receipts[] (Archive list)                               │
│  ├── filters, sort, searchQuery                              │
│  ├── statistics (ReceiptStatistics)                          │
│  └── loading states (isUploading, isProcessing, etc.)        │
│                                                               │
│  ACTIONS                                                      │
│  ├── Upload Flow                                             │
│  │   └── uploadReceipt → pollProcessingStatus → setCurrentReceipt
│  ├── List Management                                         │
│  │   └── fetchReceipts → loadMoreReceipts                    │
│  ├── Search & Filter                                         │
│  │   └── searchReceipts, setFilters, setSort                 │
│  └── CRUD Operations                                         │
│      └── updateCurrentReceipt, approveReceipt, deleteReceipt │
│                                                               │
└─────────────────────────────────────────────────────────────┘
         ↓                           ↓
┌────────────────┐         ┌─────────────────────┐
│ Receipt Service │         │  UI Components      │
│ (API Layer)     │         │  (React)            │
└────────────────┘         └─────────────────────┘
```

## State Structure

### Receipt Upload Flow

```
1. User selects file
   ↓
2. uploadReceipt(file)
   ├── Set isUploading = true
   ├── Call receiptService.uploadReceipt()
   ├── Get receiptId
   ├── Set isUploading = false
   └── Auto-start pollProcessingStatus(receiptId)

3. pollProcessingStatus(receiptId)
   ├── Set isProcessing = true
   ├── Poll every 2 seconds (max 30 attempts)
   │   ├── If status === 'review' or 'approved'
   │   │   ├── Fetch full receipt data
   │   │   ├── Set currentReceipt
   │   │   └── Stop polling
   │   ├── If status === 'failed'
   │   │   ├── Set error message
   │   │   └── Stop polling
   │   └── If status === 'processing'
   │       └── Continue polling
   └── Timeout after 60 seconds

4. User reviews currentReceipt
   ↓
5. approveReceipt(receiptId, finalData)
   ├── Update receipt data
   ├── Add to receipts list
   ├── Increment total
   └── Refresh statistics
```

### Pagination Flow

```
Initial Load:
fetchReceipts(reset=true)
├── page = 1
├── receipts = response.receipts
├── hasMore = response.hasMore
└── total = response.total

Load More:
loadMoreReceipts()
├── Check: hasMore && !isLoadingList
├── page = page + 1
├── receipts = [...receipts, ...response.receipts]
├── hasMore = response.hasMore
└── total = response.total

Filter/Sort Change:
setFilters() or setSort()
├── Update filters/sort
├── page = 1
└── fetchReceipts(reset=true)
```

### Search Flow

```
searchReceipts(query)
├── Set searchQuery = query
├── Set isLoadingList = true
├── Call receiptService.searchReceipts()
├── receipts = response.receipts (replace, not append)
├── page = 1
├── hasMore = response.hasMore
└── isLoadingList = false
```

## Key Features

### 1. Automatic Polling

```typescript
pollProcessingStatus: async (receiptId: string) => {
  // Stop any existing polling
  get().stopPolling();
  
  set({ isProcessing: true, error: null });
  
  let attempts = 0;
  const maxAttempts = 30; // 60 seconds max
  
  const poll = async () => {
    attempts++;
    
    if (attempts > maxAttempts) {
      get().stopPolling();
      set({ 
        isProcessing: false, 
        error: 'העיבוד לוקח זמן רב מהרגיל. נסה שוב מאוחר יותר.' 
      });
      return;
    }
    
    const response = await receiptService.checkProcessingStatus(receiptId);
    
    if (response.status === 'review' || response.status === 'approved') {
      // Complete - fetch full data
      get().stopPolling();
      const receipt = await receiptService.getReceipt(receiptId);
      set({ currentReceipt: receipt, isProcessing: false });
    } else if (response.status === 'failed') {
      // Failed
      get().stopPolling();
      set({ isProcessing: false, error: 'עיבוד הקבלה נכשל. נסה שוב.' });
    }
    // Otherwise continue polling
  };
  
  const intervalId = window.setInterval(poll, 2000);
  set({ pollingIntervalId: intervalId });
  
  poll(); // First check immediately
}
```

**Important:**
- Always call `stopPolling()` before starting new polling
- Clean up on unmount with `cleanupReceiptStore()`
- Max 30 attempts (60 seconds) prevents infinite polling

### 2. Optimistic Updates (Delete)

```typescript
deleteReceipt: async (receiptId: string) => {
  // Store current state for rollback
  const previousReceipts = get().receipts;
  const previousTotal = get().total;
  
  // Update UI immediately
  set({
    receipts: get().receipts.filter(r => r.id !== receiptId),
    total: get().total - 1
  });
  
  try {
    await receiptService.deleteReceipt(receiptId);
    // Success - UI already updated
  } catch (error) {
    // Rollback on error
    set({
      receipts: previousReceipts,
      total: previousTotal
    });
    throw error;
  }
}
```

**Benefits:**
- Instant UI feedback
- Better perceived performance
- Automatic rollback on error

### 3. Pagination with Infinite Scroll

```typescript
fetchReceipts: async (reset = false) => {
  const page = reset ? 1 : get().page;
  const response = await receiptService.getReceipts(filters, sort, page, pageSize);
  
  set({
    receipts: reset 
      ? response.receipts              // Replace on reset
      : [...get().receipts, ...response.receipts], // Append on load more
    page: response.page,
    hasMore: response.hasMore
  });
}

loadMoreReceipts: async () => {
  if (!get().hasMore || get().isLoadingList) return; // Guard
  set({ page: get().page + 1 });
  await get().fetchReceipts(false); // Don't reset
}
```

**Usage:**
```typescript
const ReceiptList = () => {
  const { receipts, loadMoreReceipts, hasMore } = useReceiptStore();
  
  return (
    <InfiniteScroll
      dataLength={receipts.length}
      next={loadMoreReceipts}
      hasMore={hasMore}
    >
      {receipts.map(r => <ReceiptCard key={r.id} receipt={r} />)}
    </InfiniteScroll>
  );
};
```

### 4. Filter & Sort Integration

```typescript
setFilters: (filters: Partial<ReceiptFilterOptions>) => {
  set({ 
    filters: { ...get().filters, ...filters },
    page: 1 // Reset to page 1
  });
  get().fetchReceipts(true); // Fetch with new filters
}

setSort: (sort: ReceiptSortOptions) => {
  set({ sort, page: 1 });
  get().fetchReceipts(true); // Fetch with new sort
}
```

**Auto-fetch behavior:**
- Filter change → reset page → fetch
- Sort change → reset page → fetch
- Search → reset page → fetch

### 5. Error Handling

All errors are Hebrew messages from the service layer:

```typescript
try {
  await uploadReceipt(file);
} catch (error) {
  // error.message is Hebrew
  // uploadError is automatically set in store
  console.error(error.message);
}
```

**Error types:**
- `uploadError` - File upload errors
- `error` - General errors (processing, fetch, update, etc.)

**Clear errors:**
```typescript
clearError() // Clears both uploadError and error
```

## Performance Optimization

### Use Selectors

```typescript
// ❌ Bad - re-renders on ANY store change
const { receipts, statistics, filters, sort } = useReceiptStore();

// ✅ Good - re-renders only when receipts change
const receipts = useReceiptStore(selectReceipts);
```

### Actions-Only Hook

```typescript
// No re-renders on store changes
const actions = useReceiptActions();

const handleUpload = async (file: File) => {
  await actions.uploadReceipt(file);
};
```

### Custom Selectors

```typescript
// Create custom selector
const selectFilteredReceipts = (state: ReceiptStore) => 
  state.receipts.filter(r => r.status === 'approved');

// Use in component
const approvedReceipts = useReceiptStore(selectFilteredReceipts);
```

## Integration Examples

### Upload Page

```typescript
import { useReceiptStore } from '@/stores/receipt.store';

const UploadPage = () => {
  const { uploadReceipt, currentReceipt, isUploading, isProcessing } = useReceiptStore();

  const handleFileSelect = async (file: File) => {
    try {
      const receiptId = await uploadReceipt(file);
      // Polling starts automatically
    } catch (error) {
      toast.error(error.message);
    }
  };

  useEffect(() => {
    if (currentReceipt && currentReceipt.status === 'review') {
      // Navigate to review page
      navigate(`/receipts/${currentReceipt.id}/review`);
    }
  }, [currentReceipt]);

  return (
    <div>
      <CameraCapture onCapture={handleFileSelect} />
      {isUploading && <UploadProgress />}
      {isProcessing && <ProcessingSpinner />}
    </div>
  );
};
```

### Review Page

```typescript
const ReviewPage = () => {
  const { receiptId } = useParams();
  const { 
    currentReceipt, 
    setCurrentReceipt,
    updateCurrentReceipt, 
    approveReceipt 
  } = useReceiptStore();

  useEffect(() => {
    // Fetch receipt if not in store
    const fetchReceipt = async () => {
      if (!currentReceipt || currentReceipt.id !== receiptId) {
        const receipt = await receiptService.getReceipt(receiptId);
        setCurrentReceipt(receipt);
      }
    };
    fetchReceipt();
  }, [receiptId]);

  const handleApprove = async (finalData: ReceiptUpdateRequest) => {
    try {
      await approveReceipt(receiptId, finalData);
      toast.success('הקבלה אושרה בהצלחה');
      navigate('/archive');
    } catch (error) {
      toast.error(error.message);
    }
  };

  return <ReviewForm receipt={currentReceipt} onApprove={handleApprove} />;
};
```

### Archive Page

```typescript
const ArchivePage = () => {
  const { 
    receipts, 
    fetchReceipts, 
    loadMoreReceipts,
    filters,
    setFilters,
    clearFilters,
    isLoadingList,
    hasMore
  } = useReceiptStore();

  useEffect(() => {
    fetchReceipts(true); // Initial load
  }, []);

  return (
    <div>
      <FilterPanel 
        filters={filters}
        onFilterChange={setFilters}
        onClearFilters={clearFilters}
      />
      
      <InfiniteScroll
        dataLength={receipts.length}
        next={loadMoreReceipts}
        hasMore={hasMore}
        loader={<LoadingSpinner />}
      >
        {receipts.map(receipt => (
          <ReceiptCard key={receipt.id} receipt={receipt} />
        ))}
      </InfiniteScroll>
    </div>
  );
};
```

### Dashboard with Statistics

```typescript
const Dashboard = () => {
  const { statistics, fetchStatistics, isLoadingStats } = useReceiptStore();

  useEffect(() => {
    fetchStatistics();
  }, []);

  if (isLoadingStats) return <StatsSkeleton />;

  return (
    <div className="grid grid-cols-3 gap-4">
      <StatCard 
        label="סה״כ קבלות" 
        value={statistics?.totalReceipts}
        icon={<Receipt />}
      />
      <StatCard 
        label="סכום כולל" 
        value={formatCurrency(statistics?.totalAmount)}
        icon={<DollarSign />}
      />
      <StatCard 
        label="חודש זה" 
        value={statistics?.currentMonthCount}
        icon={<Calendar />}
      />
    </div>
  );
};
```

## Cleanup

### On Component Unmount

```typescript
import { cleanupReceiptStore } from '@/stores/receipt.store';

const ReceiptPage = () => {
  useEffect(() => {
    return () => {
      cleanupReceiptStore(); // Stop polling
    };
  }, []);

  return <ReceiptContent />;
};
```

### On Logout

```typescript
const handleLogout = () => {
  useReceiptStore.getState().reset(); // Clear all receipt data
  useAuthStore.getState().clearAuth(); // Clear auth
  navigate('/login');
};
```

## DevTools

Store is integrated with Redux DevTools:

```typescript
export const useReceiptStore = create<ReceiptStore>()(
  devtools(
    (set, get) => ({ /* store implementation */ }),
    { name: 'receipt-store' }
  )
);
```

**Usage:**
1. Install Redux DevTools extension
2. Open DevTools in browser
3. Select "receipt-store" from dropdown
4. View state changes in real-time

## Testing

### Mock Store for Tests

```typescript
import { useReceiptStore } from '@/stores/receipt.store';

// Reset before each test
beforeEach(() => {
  useReceiptStore.getState().reset();
});

// Mock upload
const mockUpload = vi.fn().mockResolvedValue('receipt-123');
useReceiptStore.setState({ uploadReceipt: mockUpload });

// Test
const { result } = renderHook(() => useReceiptStore());
await result.current.uploadReceipt(mockFile);
expect(mockUpload).toHaveBeenCalledWith(mockFile);
```

## Migration from Context API

If migrating from Context API:

```typescript
// Before (Context)
const { receipts, uploadReceipt } = useReceiptContext();

// After (Zustand)
const { receipts, uploadReceipt } = useReceiptStore();

// Or with selectors
const receipts = useReceiptStore(selectReceipts);
const uploadReceipt = useReceiptStore(state => state.uploadReceipt);
```

## Best Practices

1. **Always use selectors** for performance
2. **Clean up polling** on unmount with `cleanupReceiptStore()`
3. **Reset store** on logout with `reset()`
4. **Handle errors** in try-catch blocks
5. **Show loading states** for better UX
6. **Debounce search** (300ms recommended)
7. **Use optimistic updates** for instant feedback
8. **Refresh statistics** after mutations (approve, delete)
9. **Check guards** before actions (e.g., `hasMore` before `loadMore`)
10. **Log in development** - store includes `import.meta.env.DEV` checks

## Common Patterns

### Conditional Fetch on Mount

```typescript
const { receipts, fetchReceipts } = useReceiptStore();

useEffect(() => {
  if (receipts.length === 0) {
    fetchReceipts(true); // Only fetch if empty
  }
}, []);
```

### Refetch on Filter Change

```typescript
useEffect(() => {
  fetchReceipts(true); // Reset and fetch with new filters
}, [filters]); // Re-fetch when filters change
```

### Loading State Combination

```typescript
const isAnyLoading = useReceiptStore(selectIsLoading);
// Combines: isUploading || isProcessing || isLoadingList || isLoadingStats

if (isAnyLoading) return <GlobalSpinner />;
```

### Error Toast Integration

```typescript
const error = useReceiptStore(selectError);

useEffect(() => {
  if (error) {
    toast.error(error);
    // Auto-clear after showing
    setTimeout(() => clearError(), 5000);
  }
}, [error]);
```

## Troubleshooting

### Polling Doesn't Stop

**Problem:** Polling continues after navigating away

**Solution:**
```typescript
useEffect(() => {
  return () => cleanupReceiptStore();
}, []);
```

### Duplicate Requests

**Problem:** Multiple fetch requests firing

**Solution:**
```typescript
const hasFetched = useRef(false);

useEffect(() => {
  if (!hasFetched.current) {
    fetchReceipts(true);
    hasFetched.current = true;
  }
}, []);
```

### Filter Reset Not Working

**Problem:** Filters don't clear properly

**Solution:**
```typescript
// Use clearFilters action
clearFilters(); // Resets filters AND refetches
```

### State Not Updating

**Problem:** Component doesn't re-render

**Solution:**
```typescript
// Use selector instead of direct access
const receipts = useReceiptStore(selectReceipts); // ✅
// Not: const store = useReceiptStore(); const receipts = store.receipts; // ❌
```

## Conclusion

The Receipt Store provides a robust, performant, and developer-friendly state management solution for the Tik-Tax receipt system. With automatic polling, optimistic updates, and comprehensive error handling, it simplifies complex workflows while maintaining excellent UX.
