# Archive Page - Quick Reference

## Overview
Complete receipt archive with search, filters, sorting, and dual view modes (grid/list).

## File Location
```
/src/pages/receipts/ArchivePage.tsx
```

## Features

### ✅ Search & Filters
- **Debounced Search**: 500ms delay, minimum 2 characters
- **Date Range Filter**: Start/end date selection
- **Category Filter**: Multi-select from 13 categories
- **Amount Range Filter**: Min/max amount filtering
- **Active Filter Chips**: Visual display of active filters with quick removal

### ✅ Sorting
- Sort by: Date, Amount, Vendor Name, Upload Date
- Sort order: Ascending/Descending
- Persistent sort state

### ✅ View Modes
- **Grid View**: 3-column responsive layout with image previews
- **List View**: Horizontal cards with thumbnails
- Toggle button (desktop only)

### ✅ Stats Summary
- Total expenses (all receipts)
- This month receipts count
- Average per receipt

### ✅ Infinite Scroll
- Automatic load more when scrolling near bottom
- Loading indicator during pagination
- Respects `hasMore` flag from store

### ✅ Empty States
- No receipts message
- Search/filter no results
- CTA button to add first receipt

## Usage

### Basic Import
```tsx
import { ArchivePage } from '@/pages/receipts';

// In router
<Route path="/archive" element={<ArchivePage />} />
```

### Hooks Used
```tsx
const {
  receipts,           // Array of receipts
  total,              // Total count
  isLoadingList,      // Loading state
  searchReceipts,     // Search function
  loadMoreReceipts,   // Pagination function
  setSort,            // Sort function
  clearFilters        // Clear all filters
} = useReceipt();

const { 
  filters,            // Current filter state
  updateFilter,       // Update single filter
  hasActiveFilters    // Check if filters active
} = useReceiptFilters();

useLoadReceipts();    // Auto-load on mount
useInfiniteScroll(loadMoreReceipts); // Auto pagination
```

## Components Structure

### Stats Bar
```tsx
<div className="grid grid-cols-1 md:grid-cols-3 gap-4">
  <Card>Total Expenses</Card>
  <Card>This Month Count</Card>
  <Card>Average Amount</Card>
</div>
```

### Search & Actions Bar
```tsx
<div className="flex flex-col md:flex-row gap-3">
  <Input type="search" />
  <Button>Filter</Button>
  <Button>Sort</Button>
  <Button>Export</Button>
  <ViewToggle />
</div>
```

### Grid View Card
```tsx
<Card onClick={navigate}>
  <img />                    // 16:9 aspect ratio
  <div>
    <h3>Vendor Name</h3>
    <CategoryIcon />
    <Amount />
    <Date />
  </div>
</Card>
```

### List View Card
```tsx
<Card onClick={navigate}>
  <div className="flex">
    <img />                  // 20x20 thumbnail
    <div>
      <h3>Vendor + Amount</h3>
      <Date + Category />
    </div>
  </div>
</Card>
```

## Modals

### Filter Modal
```tsx
<Modal title="סינון קבלות" size="md">
  <DateRangeInputs />
  <CategoryGrid />         // Multi-select buttons
  <AmountRangeInputs />
  
  <Footer>
    <Button>Clear All</Button>
    <Button>Apply</Button>
  </Footer>
</Modal>
```

### Sort Modal
```tsx
<Modal title="מיון קבלות" size="sm">
  {sortOptions.map(option => (
    <>
      <Button>High to Low</Button>
      <Button>Low to High</Button>
    </>
  ))}
</Modal>
```

## State Management

### Local UI State
```tsx
const [searchQuery, setSearchQuery] = useState('');
const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
const [showFilterModal, setShowFilterModal] = useState(false);
const [showSortModal, setShowSortModal] = useState(false);
```

### Filter State
```tsx
const [dateRange, setDateRange] = useState({ start: '', end: '' });
const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
const [amountRange, setAmountRange] = useState({ min: '', max: '' });
```

### Sort State
```tsx
const [sortField, setSortField] = useState<ReceiptSortField>('date');
const [sortOrder, setSortOrder] = useState<ReceiptSortOrder>('desc');
```

## Key Functions

### Search (Debounced)
```tsx
useEffect(() => {
  const timer = setTimeout(() => {
    if (searchQuery.length >= 2 || searchQuery.length === 0) {
      searchReceipts(searchQuery);
    }
  }, 500);
  
  return () => clearTimeout(timer);
}, [searchQuery, searchReceipts]);
```

### Apply Filters
```tsx
const applyFilters = () => {
  updateFilter('startDate', dateRange.start || undefined);
  updateFilter('endDate', dateRange.end || undefined);
  updateFilter('categoryIds', selectedCategories.length > 0 ? selectedCategories : undefined);
  updateFilter('minAmount', amountRange.min ? parseFloat(amountRange.min) : undefined);
  updateFilter('maxAmount', amountRange.max ? parseFloat(amountRange.max) : undefined);
  setShowFilterModal(false);
};
```

### Apply Sort
```tsx
const handleSort = (field: ReceiptSortField, order: ReceiptSortOrder) => {
  setSortField(field);
  setSortOrder(order);
  setSort({ field, order });
  setShowSortModal(false);
};
```

### Clear Filters
```tsx
const handleClearFilters = () => {
  setDateRange({ start: '', end: '' });
  setSelectedCategories([]);
  setAmountRange({ min: '', max: '' });
  clearFilters();
  setShowFilterModal(false);
};
```

## Styling

### Responsive Grid
```tsx
// Grid View
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"

// Stats Bar
className="grid grid-cols-1 md:grid-cols-3 gap-4"
```

### View Toggle (Desktop Only)
```tsx
<div className="hidden md:flex border border-gray-300 rounded-lg overflow-hidden">
  <button className={viewMode === 'grid' ? 'bg-primary-50' : 'bg-white'}>
    <Grid />
  </button>
  <button className={viewMode === 'list' ? 'bg-primary-50' : 'bg-white'}>
    <List />
  </button>
</div>
```

### Filter Chips
```tsx
<div className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm flex items-center gap-2">
  {filterLabel}
  <button onClick={removeFilter}>
    <X size={14} />
  </button>
</div>
```

## Performance

### Optimizations
- ✅ Debounced search (500ms)
- ✅ Infinite scroll with threshold (500px from bottom)
- ✅ Memoized category lookups
- ✅ Conditional rendering based on loading state
- ✅ Lazy modal rendering (only when open)

### Loading States
```tsx
// Initial load
{isLoadingList && receipts.length === 0 && <PageContainer loading />}

// Pagination load
{isLoadingList && receipts.length > 0 && <LoadingSpinner />}
```

## Empty States

### No Receipts
```tsx
{receipts.length === 0 && !isLoadingList && (
  <EmptyState
    icon={<Search />}
    title="לא נמצאו קבלות"
    description={hasActiveFilters() ? "נסה לשנות..." : "התחל על ידי..."}
    action={!hasActiveFilters() && <Button>הוסף קבלה</Button>}
  />
)}
```

## Navigation

### Click Handlers
```tsx
// Receipt card click
onClick={() => navigate(`/receipts/${receipt.id}`)}

// Add receipt button
onClick={() => navigate('/receipts/new')}

// Export button
onClick={() => navigate('/export')}
```

## Accessibility

### ARIA Labels
```tsx
<button aria-label="תצוגת רשת">
  <Grid />
</button>

<button aria-label="תצוגת רשימה">
  <List />
</button>
```

### Keyboard Navigation
- All interactive elements are keyboard accessible
- Modal focus management via Modal component
- Tab order: Search → Filters → Sort → View Toggle → Cards

## TypeScript Types

### Sort Types
```tsx
type ReceiptSortField = 'date' | 'amount' | 'vendor' | 'createdAt';
type ReceiptSortOrder = 'asc' | 'desc';
```

### View Mode Type
```tsx
type ViewMode = 'grid' | 'list';
```

## Integration Points

### Required Components
- ✅ PageContainer (layout wrapper)
- ✅ Button (all variants: primary, secondary)
- ✅ Input (search, date, number types)
- ✅ Card (hoverable, various padding)
- ✅ Modal (with footer support)

### Required Hooks
- ✅ useReceipt (main receipt state)
- ✅ useLoadReceipts (auto-load on mount)
- ✅ useInfiniteScroll (pagination)
- ✅ useReceiptFilters (filter management)

### Required Utils
- ✅ formatAmount (₪1,234.56)
- ✅ formatDateIL (DD/MM/YYYY)
- ✅ DEFAULT_CATEGORIES (category data)

## Testing Checklist

### Search
- [ ] Search with 2+ characters triggers API call
- [ ] Search clears on empty string
- [ ] Debounce delays by 500ms
- [ ] Results update correctly

### Filters
- [ ] Date range filtering works
- [ ] Category multi-select works
- [ ] Amount range filtering works
- [ ] Filter chips display correctly
- [ ] Remove filter chip works
- [ ] Clear all filters works
- [ ] Apply filters closes modal

### Sorting
- [ ] All sort options work (4 fields × 2 orders)
- [ ] Sort persists across interactions
- [ ] Sort modal closes after selection
- [ ] Visual indicator shows active sort

### Views
- [ ] Grid view displays correctly (3 columns desktop)
- [ ] List view displays correctly (horizontal cards)
- [ ] Toggle switches views
- [ ] Cards navigate on click
- [ ] Images load properly

### Pagination
- [ ] Infinite scroll triggers near bottom
- [ ] Loading indicator shows during load
- [ ] Prevents double-loading
- [ ] Respects hasMore flag

### Stats
- [ ] Total amount calculates correctly
- [ ] This month count is accurate
- [ ] Average calculates correctly
- [ ] Updates when receipts change

### Responsive
- [ ] Mobile: Single column grid
- [ ] Mobile: View toggle hidden
- [ ] Tablet: 2 column grid
- [ ] Desktop: 3 column grid
- [ ] Stats bar responsive (3 cols → 1 col)

### Empty States
- [ ] Shows when no receipts exist
- [ ] Shows when search/filter returns nothing
- [ ] Different messages for each case
- [ ] CTA button appears when appropriate

## Common Issues & Solutions

### Issue: Search not triggering
**Solution**: Check debounce timer and minimum character length

### Issue: Filters not applying
**Solution**: Verify `updateFilter` is called and modal closes

### Issue: Categories not displaying
**Solution**: Check `DEFAULT_CATEGORIES` import and icon rendering

### Issue: Infinite scroll not working
**Solution**: Verify scroll threshold (500px) and `hasMore` flag

### Issue: Images not loading
**Solution**: Check `imageUrl` format and CORS settings

## Future Enhancements

### Potential Features
- [ ] Bulk selection and actions
- [ ] Save filter presets
- [ ] Export filtered results
- [ ] Advanced search (multi-field)
- [ ] Sort by multiple fields
- [ ] Custom date range presets (This Week, Last Month, etc.)
- [ ] Receipt comparison view
- [ ] Print view
- [ ] Keyboard shortcuts
- [ ] URL state sync (filters in URL params)

---

**Last Updated**: November 3, 2025  
**Status**: ✅ Complete and Production-Ready
