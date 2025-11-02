# Receipt Store - Usage Examples

## Example 1: Complete Upload Flow with Progress

```typescript
import { useReceiptStore } from '@/stores/receipt.store';
import { useToast } from '@/hooks/useToast';

const UploadPage = () => {
  const { 
    uploadReceipt, 
    currentReceipt,
    isUploading, 
    isProcessing,
    uploadError,
    error 
  } = useReceiptStore();
  const { toast } = useToast();
  const navigate = useNavigate();

  const handleFileUpload = async (file: File) => {
    try {
      // Upload file
      const receiptId = await uploadReceipt(file);
      toast.success('הקובץ הועלה בהצלחה');
      
      // Polling starts automatically
      // Wait for processing to complete...
    } catch (err) {
      toast.error(uploadError || 'שגיאה בהעלאת הקובץ');
    }
  };

  // Navigate to review when processing complete
  useEffect(() => {
    if (currentReceipt && currentReceipt.status === 'review') {
      navigate(`/receipts/${currentReceipt.id}/review`);
    }
  }, [currentReceipt, navigate]);

  return (
    <div className="upload-page">
      <CameraCapture onCapture={handleFileUpload} />
      
      {isUploading && (
        <div className="upload-progress">
          <Spinner />
          <p>מעלה קובץ...</p>
        </div>
      )}
      
      {isProcessing && (
        <div className="processing-status">
          <Spinner />
          <p>מעבד קבלה...</p>
          <p className="text-sm text-gray-600">זה לוקח בדרך כלל 10-15 שניות</p>
        </div>
      )}
      
      {error && (
        <Alert variant="error">
          {error}
          <Button onClick={() => retryProcessing(currentReceipt?.id!)}>
            נסה שוב
          </Button>
        </Alert>
      )}
    </div>
  );
};
```

## Example 2: Archive with Infinite Scroll

```typescript
import { useReceiptStore, selectReceipts, selectIsLoadingList } from '@/stores/receipt.store';
import InfiniteScroll from 'react-infinite-scroll-component';

const ArchivePage = () => {
  const receipts = useReceiptStore(selectReceipts);
  const isLoading = useReceiptStore(selectIsLoadingList);
  const { fetchReceipts, loadMoreReceipts, hasMore } = useReceiptStore();

  // Initial fetch
  useEffect(() => {
    fetchReceipts(true); // reset = true
  }, [fetchReceipts]);

  return (
    <div className="archive-page">
      <h1>ארכיון קבלות</h1>
      
      {receipts.length === 0 && !isLoading ? (
        <EmptyState 
          title="אין קבלות"
          description="התחל להעלות קבלות כדי לראות אותן כאן"
        />
      ) : (
        <InfiniteScroll
          dataLength={receipts.length}
          next={loadMoreReceipts}
          hasMore={hasMore}
          loader={
            <div className="flex justify-center p-4">
              <Spinner />
            </div>
          }
          endMessage={
            <p className="text-center text-gray-500 p-4">
              הצגת כל הקבלות ({receipts.length})
            </p>
          }
        >
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {receipts.map(receipt => (
              <ReceiptCard key={receipt.id} receipt={receipt} />
            ))}
          </div>
        </InfiniteScroll>
      )}
    </div>
  );
};
```

## Example 3: Search with Debounce

```typescript
import { useReceiptStore } from '@/stores/receipt.store';
import { useDebouncedCallback } from 'use-debounce';

const SearchBar = () => {
  const { searchReceipts, isLoadingList } = useReceiptStore();
  const [query, setQuery] = useState('');

  // Debounce search for 300ms
  const debouncedSearch = useDebouncedCallback(
    (searchQuery: string) => {
      if (searchQuery.length >= 2) {
        searchReceipts(searchQuery);
      } else if (searchQuery.length === 0) {
        // Clear search - fetch all
        fetchReceipts(true);
      }
    },
    300
  );

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    debouncedSearch(value);
  };

  return (
    <div className="relative">
      <input
        type="search"
        value={query}
        onChange={handleSearch}
        placeholder="חיפוש קבלות (עסק, סכום, תאריך...)"
        className="w-full px-4 py-2 pr-10 border rounded-lg"
      />
      <Search className="absolute right-3 top-3 text-gray-400" size={20} />
      {isLoadingList && (
        <Spinner className="absolute left-3 top-3" size={20} />
      )}
    </div>
  );
};
```

## Example 4: Advanced Filters Panel

```typescript
import { useReceiptStore, selectFilters, selectHasActiveFilters } from '@/stores/receipt.store';
import { EXPENSE_CATEGORIES } from '@/constants';

const FilterPanel = () => {
  const filters = useReceiptStore(selectFilters);
  const hasFilters = useReceiptStore(selectHasActiveFilters);
  const { setFilters, clearFilters } = useReceiptStore();

  const handleCategoryChange = (categoryId: string) => {
    setFilters({ category: categoryId || undefined });
  };

  const handleDateRangeChange = (start: string, end: string) => {
    setFilters({ startDate: start, endDate: end });
  };

  const handleStatusChange = (status: string[]) => {
    setFilters({ status });
  };

  const handleAmountRangeChange = (min: number, max: number) => {
    setFilters({ minAmount: min, maxAmount: max });
  };

  return (
    <div className="filter-panel bg-white p-4 rounded-lg shadow">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">מסננים</h3>
        {hasFilters && (
          <button onClick={clearFilters} className="text-primary-600">
            נקה הכל
          </button>
        )}
      </div>

      {/* Category Filter */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">קטגוריה</label>
        <select
          value={filters.category || ''}
          onChange={(e) => handleCategoryChange(e.target.value)}
          className="w-full border rounded-lg px-3 py-2"
        >
          <option value="">כל הקטגוריות</option>
          {EXPENSE_CATEGORIES.map(cat => (
            <option key={cat.id} value={cat.id}>
              {cat.nameHe}
            </option>
          ))}
        </select>
      </div>

      {/* Date Range Filter */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">טווח תאריכים</label>
        <div className="grid grid-cols-2 gap-2">
          <input
            type="date"
            value={filters.startDate || ''}
            onChange={(e) => handleDateRangeChange(e.target.value, filters.endDate || '')}
            className="border rounded-lg px-3 py-2"
          />
          <input
            type="date"
            value={filters.endDate || ''}
            onChange={(e) => handleDateRangeChange(filters.startDate || '', e.target.value)}
            className="border rounded-lg px-3 py-2"
          />
        </div>
      </div>

      {/* Status Filter */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">סטטוס</label>
        <div className="space-y-2">
          {['review', 'approved', 'failed'].map(status => (
            <label key={status} className="flex items-center">
              <input
                type="checkbox"
                checked={filters.status?.includes(status) || false}
                onChange={(e) => {
                  const current = filters.status || [];
                  const updated = e.target.checked
                    ? [...current, status]
                    : current.filter(s => s !== status);
                  handleStatusChange(updated);
                }}
                className="ml-2"
              />
              <span>{getStatusLabel(status)}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Amount Range */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">טווח סכום</label>
        <div className="grid grid-cols-2 gap-2">
          <input
            type="number"
            placeholder="מינימום"
            value={filters.minAmount || ''}
            onChange={(e) => handleAmountRangeChange(
              Number(e.target.value), 
              filters.maxAmount || 0
            )}
            className="border rounded-lg px-3 py-2"
          />
          <input
            type="number"
            placeholder="מקסימום"
            value={filters.maxAmount || ''}
            onChange={(e) => handleAmountRangeChange(
              filters.minAmount || 0, 
              Number(e.target.value)
            )}
            className="border rounded-lg px-3 py-2"
          />
        </div>
      </div>
    </div>
  );
};
```

## Example 5: Review and Approve Receipt

```typescript
import { useReceiptStore } from '@/stores/receipt.store';
import { useForm } from 'react-hook-form';

const ReviewPage = () => {
  const { receiptId } = useParams<{ receiptId: string }>();
  const { 
    currentReceipt, 
    setCurrentReceipt,
    approveReceipt, 
    updateCurrentReceipt,
    isProcessing 
  } = useReceiptStore();
  const navigate = useNavigate();
  const { toast } = useToast();

  const { register, handleSubmit, formState: { errors } } = useForm<ReceiptUpdateRequest>({
    defaultValues: currentReceipt || undefined
  });

  // Fetch receipt on mount
  useEffect(() => {
    const fetchReceipt = async () => {
      if (!currentReceipt || currentReceipt.id !== receiptId) {
        const receipt = await receiptService.getReceipt(receiptId!);
        setCurrentReceipt(receipt);
      }
    };
    fetchReceipt();
  }, [receiptId]);

  const onSubmit = async (data: ReceiptUpdateRequest) => {
    try {
      await approveReceipt(receiptId!, data);
      toast.success('הקבלה אושרה בהצלחה');
      navigate('/archive');
    } catch (error) {
      toast.error('שגיאה באישור הקבלה');
    }
  };

  if (!currentReceipt) return <LoadingSkeleton />;

  return (
    <div className="review-page">
      <h1>בדיקת קבלה</h1>

      {/* Receipt Image */}
      <div className="receipt-image mb-6">
        <img 
          src={currentReceipt.imageUrl} 
          alt="Receipt" 
          className="max-w-full rounded-lg shadow"
        />
      </div>

      {/* OCR Confidence Indicator */}
      <ConfidenceBadge confidence={currentReceipt.ocrData?.confidence.overall} />

      {/* Edit Form */}
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <Input
          label="שם העסק"
          {...register('vendorName', { required: 'שדה חובה' })}
          error={errors.vendorName?.message}
          confidence={currentReceipt.ocrData?.confidence.vendorName}
        />

        <Input
          label="מספר עסק"
          {...register('businessNumber', { 
            required: 'שדה חובה',
            pattern: { value: /^\d{9}$/, message: '9 ספרות' }
          })}
          error={errors.businessNumber?.message}
          confidence={currentReceipt.ocrData?.confidence.businessNumber}
        />

        <Input
          label="תאריך"
          type="date"
          {...register('date', { required: 'שדה חובה' })}
          error={errors.date?.message}
          confidence={currentReceipt.ocrData?.confidence.date}
        />

        <Input
          label="סכום כולל"
          type="number"
          step="0.01"
          {...register('totalAmount', { required: 'שדה חובה', min: 0 })}
          error={errors.totalAmount?.message}
          confidence={currentReceipt.ocrData?.confidence.totalAmount}
        />

        <Select
          label="קטגוריה"
          {...register('categoryId', { required: 'שדה חובה' })}
          error={errors.categoryId?.message}
        >
          {EXPENSE_CATEGORIES.map(cat => (
            <option key={cat.id} value={cat.id}>{cat.nameHe}</option>
          ))}
        </Select>

        <div className="flex gap-3">
          <Button 
            type="submit" 
            disabled={isProcessing}
            className="flex-1"
          >
            {isProcessing ? 'מאשר...' : 'אשר וארכב'}
          </Button>
          <Button 
            type="button" 
            variant="secondary"
            onClick={() => navigate('/upload')}
          >
            ביטול
          </Button>
        </div>
      </form>
    </div>
  );
};

// Confidence Badge Component
const ConfidenceBadge = ({ confidence }: { confidence?: 'high' | 'medium' | 'low' }) => {
  const config = {
    high: { color: 'green', text: 'דיוק גבוה', icon: CheckCircle },
    medium: { color: 'yellow', text: 'בדוק שדות מסומנים', icon: AlertTriangle },
    low: { color: 'red', text: 'דיוק נמוך - בדוק היטב', icon: AlertCircle }
  };

  const { color, text, icon: Icon } = config[confidence || 'high'];

  return (
    <div className={`flex items-center gap-2 p-3 bg-${color}-50 border border-${color}-200 rounded-lg mb-4`}>
      <Icon className={`text-${color}-600`} size={20} />
      <span className={`text-${color}-800 font-medium`}>{text}</span>
    </div>
  );
};
```

## Example 6: Dashboard with Statistics

```typescript
import { useReceiptStore, selectStatistics, selectIsLoadingStats } from '@/stores/receipt.store';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const statistics = useReceiptStore(selectStatistics);
  const isLoading = useReceiptStore(selectIsLoadingStats);
  const { fetchStatistics } = useReceiptStore();

  useEffect(() => {
    fetchStatistics();
  }, [fetchStatistics]);

  if (isLoading) {
    return <DashboardSkeleton />;
  }

  if (!statistics) {
    return <ErrorState message="שגיאה בטעינת סטטיסטיקות" />;
  }

  return (
    <div className="dashboard">
      <h1>סיכום חודשי</h1>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <StatCard
          title="סה״כ קבלות"
          value={statistics.totalReceipts}
          icon={<Receipt />}
          trend={statistics.receiptsTrend}
        />
        <StatCard
          title="סכום כולל"
          value={formatCurrency(statistics.totalAmount)}
          icon={<DollarSign />}
          trend={statistics.amountTrend}
        />
        <StatCard
          title="ממוצע לקבלה"
          value={formatCurrency(statistics.averageAmount)}
          icon={<TrendingUp />}
        />
      </div>

      {/* Category Breakdown Chart */}
      <Card className="mb-6">
        <h2>פילוח לפי קטגוריה</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={statistics.byCategory}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="categoryName" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="amount" fill="#2563eb" />
          </BarChart>
        </ResponsiveContainer>
      </Card>

      {/* Recent Receipts */}
      <Card>
        <h2>קבלות אחרונות</h2>
        <ReceiptList limit={5} />
      </Card>
    </div>
  );
};

const StatCard = ({ title, value, icon, trend }: any) => (
  <Card className="p-4">
    <div className="flex items-center justify-between mb-2">
      <span className="text-gray-600 text-sm">{title}</span>
      {icon}
    </div>
    <div className="text-2xl font-bold">{value}</div>
    {trend && (
      <div className={`text-sm ${trend > 0 ? 'text-green-600' : 'text-red-600'}`}>
        {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}% מהחודש הקודם
      </div>
    )}
  </Card>
);
```

## Example 7: Cleanup on Logout

```typescript
import { useAuthStore } from '@/stores/auth.store';
import { useReceiptStore } from '@/stores/receipt.store';

const LogoutButton = () => {
  const { clearAuth } = useAuthStore();
  const { reset: resetReceipts, stopPolling } = useReceiptStore();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      // Stop any ongoing polling
      stopPolling();
      
      // Clear all receipt data
      resetReceipts();
      
      // Clear auth
      await authService.logout();
      clearAuth();
      
      // Navigate to login
      navigate('/login');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  return (
    <button onClick={handleLogout}>
      התנתק
    </button>
  );
};
```

## Example 8: Delete with Confirmation

```typescript
const DeleteReceiptButton = ({ receiptId }: { receiptId: string }) => {
  const { deleteReceipt } = useReceiptStore();
  const { toast } = useToast();
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDelete = async () => {
    const confirmed = window.confirm('האם אתה בטוח שברצונך למחוק קבלה זו?');
    if (!confirmed) return;

    setIsDeleting(true);
    try {
      await deleteReceipt(receiptId);
      toast.success('הקבלה נמחקה בהצלחה');
    } catch (error) {
      toast.error('שגיאה במחיקת הקבלה');
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <button
      onClick={handleDelete}
      disabled={isDeleting}
      className="text-red-600 hover:text-red-800"
    >
      {isDeleting ? <Spinner size={16} /> : <Trash2 size={16} />}
      מחק
    </button>
  );
};
```

## Example 9: Sort Dropdown

```typescript
const SortDropdown = () => {
  const sort = useReceiptStore(selectSort);
  const { setSort } = useReceiptStore();

  const sortOptions = [
    { field: 'date', order: 'desc', label: 'תאריך (חדש לישן)' },
    { field: 'date', order: 'asc', label: 'תאריך (ישן לחדש)' },
    { field: 'totalAmount', order: 'desc', label: 'סכום (גבוה לנמוך)' },
    { field: 'totalAmount', order: 'asc', label: 'סכום (נמוך לגבוה)' },
    { field: 'vendorName', order: 'asc', label: 'שם עסק (א-ת)' }
  ];

  const currentValue = `${sort.field}-${sort.order}`;

  return (
    <select
      value={currentValue}
      onChange={(e) => {
        const [field, order] = e.target.value.split('-');
        setSort({ field, order } as ReceiptSortOptions);
      }}
      className="border rounded-lg px-3 py-2"
    >
      {sortOptions.map(opt => (
        <option key={`${opt.field}-${opt.order}`} value={`${opt.field}-${opt.order}`}>
          {opt.label}
        </option>
      ))}
    </select>
  );
};
```

## Example 10: Receipt Card with Actions

```typescript
const ReceiptCard = ({ receipt }: { receipt: Receipt }) => {
  const { setCurrentReceipt, deleteReceipt } = useReceiptStore();
  const navigate = useNavigate();

  const handleView = () => {
    setCurrentReceipt(receipt);
    navigate(`/receipts/${receipt.id}`);
  };

  const handleEdit = () => {
    if (receipt.status === 'approved') {
      alert('לא ניתן לערוך קבלה מאושרת');
      return;
    }
    setCurrentReceipt(receipt);
    navigate(`/receipts/${receipt.id}/review`);
  };

  return (
    <Card className="receipt-card hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h3 className="font-semibold text-lg">{receipt.vendorName}</h3>
          <p className="text-sm text-gray-600">{formatDate(receipt.date)}</p>
          <p className="text-2xl font-bold mt-2">
            {formatCurrency(receipt.totalAmount)}
          </p>
          <CategoryBadge categoryId={receipt.categoryId} />
        </div>
        
        <StatusBadge status={receipt.status} />
      </div>

      <div className="flex gap-2 mt-4">
        <Button variant="ghost" size="sm" onClick={handleView}>
          <Eye size={16} className="ml-1" />
          צפה
        </Button>
        {receipt.status !== 'approved' && (
          <Button variant="ghost" size="sm" onClick={handleEdit}>
            <Edit size={16} className="ml-1" />
            ערוך
          </Button>
        )}
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={() => deleteReceipt(receipt.id)}
          className="text-red-600"
        >
          <Trash2 size={16} className="ml-1" />
          מחק
        </Button>
      </div>
    </Card>
  );
};
```

These examples demonstrate real-world usage patterns and best practices for the Receipt Store in the Tik-Tax application.
