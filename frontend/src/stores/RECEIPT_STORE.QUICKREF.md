# Receipt Store - Quick Reference

## Import

```typescript
import { 
  useReceiptStore, 
  useReceiptActions,
  selectReceipts,
  selectIsLoading 
} from '@/stores/receipt.store';
```

## Basic Usage

### Upload Receipt

```typescript
const UploadButton = () => {
  const { uploadReceipt, isUploading, uploadError } = useReceiptStore();

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      const receiptId = await uploadReceipt(file);
      // Polling starts automatically
      console.log('Upload successful:', receiptId);
    } catch (error) {
      console.error('Upload failed:', error);
    }
  };

  return (
    <>
      <input type="file" onChange={handleFileChange} accept="image/*" />
      {isUploading && <Spinner />}
      {uploadError && <ErrorMessage>{uploadError}</ErrorMessage>}
    </>
  );
};
```

### Display Receipts List

```typescript
const ReceiptList = () => {
  const { receipts, fetchReceipts, isLoadingList } = useReceiptStore();

  useEffect(() => {
    fetchReceipts(true); // Reset and fetch
  }, [fetchReceipts]);

  if (isLoadingList) return <LoadingSkeleton />;

  return (
    <div>
      {receipts.map(receipt => (
        <ReceiptCard key={receipt.id} receipt={receipt} />
      ))}
    </div>
  );
};
```

### Infinite Scroll

```typescript
const ReceiptArchive = () => {
  const { receipts, loadMoreReceipts, hasMore, isLoadingList } = useReceiptStore();

  return (
    <InfiniteScroll
      dataLength={receipts.length}
      next={loadMoreReceipts}
      hasMore={hasMore}
      loader={<Spinner />}
    >
      {receipts.map(receipt => (
        <ReceiptCard key={receipt.id} receipt={receipt} />
      ))}
    </InfiniteScroll>
  );
};
```

### Search

```typescript
const SearchBar = () => {
  const { searchReceipts } = useReceiptStore();
  const [query, setQuery] = useState('');

  const handleSearch = useMemo(
    () => debounce((q: string) => searchReceipts(q), 300),
    [searchReceipts]
  );

  return (
    <input
      type="search"
      value={query}
      onChange={(e) => {
        setQuery(e.target.value);
        handleSearch(e.target.value);
      }}
      placeholder="חיפוש קבלות..."
    />
  );
};
```

### Filters

```typescript
const FilterPanel = () => {
  const { filters, setFilters, clearFilters } = useReceiptStore();

  return (
    <div>
      <select 
        value={filters.category || ''}
        onChange={(e) => setFilters({ category: e.target.value })}
      >
        <option value="">כל הקטגוריות</option>
        <option value="office-supplies">ציוד משרדי</option>
        {/* More options */}
      </select>

      <DateRangePicker
        startDate={filters.startDate}
        endDate={filters.endDate}
        onChange={(start, end) => setFilters({ startDate: start, endDate: end })}
      />

      <button onClick={clearFilters}>נקה מסננים</button>
    </div>
  );
};
```

### Approve Receipt

```typescript
const ReviewPage = () => {
  const { currentReceipt, approveReceipt, isProcessing } = useReceiptStore();
  const [formData, setFormData] = useState<ReceiptUpdateRequest>({});

  const handleApprove = async () => {
    if (!currentReceipt) return;

    try {
      await approveReceipt(currentReceipt.id, formData);
      // Receipt approved and added to archive
      navigate('/archive');
    } catch (error) {
      console.error('Approval failed:', error);
    }
  };

  return (
    <div>
      {/* Form fields */}
      <button onClick={handleApprove} disabled={isProcessing}>
        {isProcessing ? 'מאשר...' : 'אשר קבלה'}
      </button>
    </div>
  );
};
```

### Delete Receipt

```typescript
const DeleteButton = ({ receiptId }: { receiptId: string }) => {
  const { deleteReceipt } = useReceiptStore();

  const handleDelete = async () => {
    if (!confirm('האם למחוק את הקבלה?')) return;

    try {
      await deleteReceipt(receiptId);
      // Optimistic update - UI updates immediately
    } catch (error) {
      // Rollback on error
      console.error('Delete failed:', error);
    }
  };

  return <button onClick={handleDelete}>מחק</button>;
};
```

### Statistics

```typescript
const Dashboard = () => {
  const { statistics, fetchStatistics, isLoadingStats } = useReceiptStore();

  useEffect(() => {
    fetchStatistics();
  }, [fetchStatistics]);

  if (isLoadingStats) return <Spinner />;

  return (
    <div>
      <StatCard label="סה״כ קבלות" value={statistics?.totalReceipts} />
      <StatCard label="סכום כולל" value={formatCurrency(statistics?.totalAmount)} />
      {/* More stats */}
    </div>
  );
};
```

## Using Selectors (Performance)

```typescript
// ❌ Bad - subscribes to entire store
const MyComponent = () => {
  const store = useReceiptStore();
  return <div>{store.receipts.length}</div>;
};

// ✅ Good - subscribes to specific selector
const MyComponent = () => {
  const receipts = useReceiptStore(selectReceipts);
  return <div>{receipts.length}</div>;
};

// ✅ Best - multiple selectors
const MyComponent = () => {
  const receipts = useReceiptStore(selectReceipts);
  const isLoading = useReceiptStore(selectIsLoading);
  const error = useReceiptStore(selectError);

  return (
    <div>
      {isLoading && <Spinner />}
      {error && <ErrorMessage>{error}</ErrorMessage>}
      {receipts.map(r => <ReceiptCard key={r.id} receipt={r} />)}
    </div>
  );
};
```

## Actions Only (No Re-renders)

```typescript
const UploadForm = () => {
  const actions = useReceiptActions();
  // Component never re-renders on store changes

  const handleSubmit = async (file: File) => {
    await actions.uploadReceipt(file);
  };

  return <form onSubmit={handleSubmit}>...</form>;
};
```

## Cleanup on Unmount

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

## Available Selectors

| Selector | Returns | Use Case |
|----------|---------|----------|
| `selectCurrentReceipt` | `Receipt \| null` | Current receipt being processed |
| `selectReceipts` | `Receipt[]` | Receipts list |
| `selectStatistics` | `ReceiptStatistics \| null` | Statistics data |
| `selectIsLoading` | `boolean` | Any loading state |
| `selectIsUploading` | `boolean` | Upload loading |
| `selectIsProcessing` | `boolean` | Processing loading |
| `selectIsLoadingList` | `boolean` | List loading |
| `selectPaginationInfo` | `{ page, pageSize, total, hasMore }` | Pagination data |
| `selectFilters` | `ReceiptFilterOptions` | Active filters |
| `selectSort` | `ReceiptSortOptions` | Sort options |
| `selectSearchQuery` | `string` | Search query |
| `selectError` | `string \| null` | Error message |
| `selectUploadError` | `string \| null` | Upload error |
| `selectHasActiveFilters` | `boolean` | If filters active |

## State Properties

| Property | Type | Description |
|----------|------|-------------|
| `currentReceipt` | `Receipt \| null` | Receipt being processed/edited |
| `receipts` | `Receipt[]` | Archive list |
| `total` | `number` | Total receipts count |
| `page` | `number` | Current page |
| `pageSize` | `number` | Items per page |
| `hasMore` | `boolean` | More pages available |
| `filters` | `ReceiptFilterOptions` | Active filters |
| `sort` | `ReceiptSortOptions` | Sort settings |
| `searchQuery` | `string` | Search query |
| `statistics` | `ReceiptStatistics \| null` | Statistics |
| `isUploading` | `boolean` | Upload in progress |
| `isProcessing` | `boolean` | OCR processing |
| `isLoadingList` | `boolean` | List loading |
| `isLoadingStats` | `boolean` | Stats loading |
| `error` | `string \| null` | General error |
| `uploadError` | `string \| null` | Upload error |

## Actions

| Action | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `uploadReceipt` | `file: File` | `Promise<string>` | Upload and start polling |
| `pollProcessingStatus` | `receiptId: string` | `Promise<void>` | Poll OCR status |
| `stopPolling` | - | `void` | Stop polling |
| `retryProcessing` | `receiptId: string` | `Promise<void>` | Retry failed processing |
| `setCurrentReceipt` | `receipt: Receipt \| null` | `void` | Set current receipt |
| `updateCurrentReceipt` | `data: ReceiptUpdateRequest` | `Promise<void>` | Update receipt |
| `approveReceipt` | `receiptId, data` | `Promise<void>` | Approve receipt |
| `deleteReceipt` | `receiptId: string` | `Promise<void>` | Delete receipt |
| `fetchReceipts` | `reset?: boolean` | `Promise<void>` | Fetch receipts |
| `loadMoreReceipts` | - | `Promise<void>` | Load next page |
| `searchReceipts` | `query: string` | `Promise<void>` | Search receipts |
| `setFilters` | `filters: Partial<ReceiptFilterOptions>` | `void` | Set filters |
| `clearFilters` | - | `void` | Clear all filters |
| `setSort` | `sort: ReceiptSortOptions` | `void` | Set sort |
| `fetchStatistics` | - | `Promise<void>` | Fetch statistics |
| `setError` | `error: string \| null` | `void` | Set error |
| `clearError` | - | `void` | Clear errors |
| `reset` | - | `void` | Reset store |

## Error Handling

All errors are Hebrew messages from the service layer:

```typescript
const MyComponent = () => {
  const { uploadReceipt, uploadError, error } = useReceiptStore();

  const handleUpload = async (file: File) => {
    try {
      await uploadReceipt(file);
    } catch (err) {
      // uploadError is automatically set
      // Show toast or error message
    }
  };

  return (
    <>
      {uploadError && <Toast variant="error">{uploadError}</Toast>}
      {error && <Toast variant="error">{error}</Toast>}
    </>
  );
};
```

## Polling Behavior

- Starts automatically after `uploadReceipt`
- Polls every 2 seconds
- Max 30 attempts (60 seconds)
- Stops on: `review`, `approved`, `failed`, `duplicate`, or timeout
- Clean up with `stopPolling()` or `cleanupReceiptStore()`

## Best Practices

1. **Use selectors** for performance
2. **Clean up polling** on unmount
3. **Handle errors** in try-catch
4. **Reset on logout** with `reset()`
5. **Debounce search** (300ms recommended)
6. **Show loading states** for better UX
7. **Optimistic updates** for delete
8. **Refresh stats** after approve/delete
