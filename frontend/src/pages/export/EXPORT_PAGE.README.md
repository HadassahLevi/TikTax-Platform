# Export Page Component

## Overview

Comprehensive export interface for generating accountant-ready reports in multiple formats (Excel, PDF, CSV).

## File Location

```
/src/pages/export/ExportPage.tsx
```

## Features

### ✅ Format Selection
- **Excel** (📊): Recommended for accountants - structured spreadsheet
- **PDF** (📄): Formatted report - ready for printing/archiving
- **CSV** (📝): Raw data - for import into other systems

### ✅ Date Range Filtering
**Presets:**
- **החודש** (This Month): Current month to date
- **חודש שעבר** (Last Month): Complete previous month
- **השנה** (This Year): Current year to date
- **מותאם אישית** (Custom): Manual date range selection

### ✅ Category Filtering
- Multi-select category filter
- Visual category cards with icons and colors
- "Clear selection" button
- Shows count of selected categories

### ✅ Include Images Toggle
- Checkbox to include receipt images in export
- Format-specific descriptions:
  - **PDF**: Images embedded in document
  - **Excel/CSV**: Creates ZIP file with images

### ✅ Real-time Preview
- Live count of receipts to be exported
- Total amount calculation
- VAT amount calculation
- Selected format and filter summary

### ✅ Export Progress
- Animated progress bar (0-100%)
- Percentage display in button
- Progress simulation during export
- Auto-reset after completion

## Props

```typescript
// No props - uses hooks internally
```

## State Management

```typescript
// Export Settings
const [selectedFormat, setSelectedFormat] = useState<ExportFormat>('excel');
const [datePreset, setDatePreset] = useState<DatePreset>('this_month');
const [customStartDate, setCustomStartDate] = useState('');
const [customEndDate, setCustomEndDate] = useState('');
const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
const [includeImages, setIncludeImages] = useState(false);

// Export Progress
const [isExporting, setIsExporting] = useState(false);
const [exportProgress, setExportProgress] = useState(0);
```

## Hook Dependencies

```typescript
import { useReceipt } from '@/hooks/useReceipt';

const { receipts, filters, setFilters } = useReceipt();
```

## Service Dependencies

```typescript
import * as receiptService from '@/services/receipt.service';

// Export API call
const response = await receiptService.exportReceipts(exportRequest);
```

## Layout Structure

```
┌─────────────────────────────────────┬─────────────────┐
│ LEFT COLUMN (lg:col-span-2)         │ RIGHT COLUMN    │
│                                     │                 │
│ ┌─────────────────────────────────┐ │ ┌─────────────┐ │
│ │ Format Selection Card           │ │ │ Summary Card│ │
│ │ - Excel/PDF/CSV icons           │ │ │ (Sticky)    │ │
│ └─────────────────────────────────┘ │ │             │ │
│                                     │ │ - Receipts  │ │
│ ┌─────────────────────────────────┐ │ │ - Total     │ │
│ │ Date Range Card                 │ │ │ - VAT       │ │
│ │ - Preset buttons                │ │ │ - Format    │ │
│ │ - Custom date inputs            │ │ │             │ │
│ │ - Selected range display        │ │ │ [Export]    │ │
│ └─────────────────────────────────┘ │ │ Progress    │ │
│                                     │ └─────────────┘ │
│ ┌─────────────────────────────────┐ │                 │
│ │ Category Filter Card            │ │ ┌─────────────┐ │
│ │ - Multi-select grid             │ │ │ Tips Card   │ │
│ │ - Icon + color visual           │ │ │ - Blue bg   │ │
│ │ - Clear button                  │ │ │ - Helpful   │ │
│ └─────────────────────────────────┘ │ │   hints     │ │
│                                     │ └─────────────┘ │
│ ┌─────────────────────────────────┐ │                 │
│ │ Additional Options Card         │ │                 │
│ │ - Include images checkbox       │ │                 │
│ └─────────────────────────────────┘ │                 │
└─────────────────────────────────────┴─────────────────┘
```

## Date Range Calculation Logic

```typescript
const getDateRange = (): { startDate: string; endDate: string } => {
  const now = new Date();
  let startDate: Date;
  let endDate: Date = now;
  
  switch (datePreset) {
    case 'this_month':
      startDate = new Date(now.getFullYear(), now.getMonth(), 1);
      break;
    case 'last_month':
      startDate = new Date(now.getFullYear(), now.getMonth() - 1, 1);
      endDate = new Date(now.getFullYear(), now.getMonth(), 0);
      break;
    case 'this_year':
      startDate = new Date(now.getFullYear(), 0, 1);
      break;
    case 'last_year':
      startDate = new Date(now.getFullYear() - 1, 0, 1);
      endDate = new Date(now.getFullYear() - 1, 11, 31);
      break;
    case 'custom':
      return {
        startDate: customStartDate,
        endDate: customEndDate
      };
  }
  
  return {
    startDate: startDate.toISOString().split('T')[0],
    endDate: endDate.toISOString().split('T')[0]
  };
};
```

## Filtering Logic

```typescript
const filteredReceipts = receipts.filter(receipt => {
  const receiptDate = new Date(receipt.date);
  const start = new Date(startDate);
  const end = new Date(endDate);
  
  const dateMatch = receiptDate >= start && receiptDate <= end;
  const categoryMatch = selectedCategories.length === 0 || 
                        selectedCategories.includes(receipt.categoryId);
  
  return dateMatch && categoryMatch;
});
```

## Export Flow

```
1. User configures export settings
   ├─ Select format (Excel/PDF/CSV)
   ├─ Choose date range (preset or custom)
   ├─ Filter categories (optional)
   └─ Toggle include images (optional)

2. User clicks "הורד דוח" button
   └─ handleExport() triggered

3. Export process starts
   ├─ Set isExporting = true
   ├─ Start progress simulation (10% increments)
   └─ Build ExportRequest object

4. API call to receipt service
   └─ await receiptService.exportReceipts(exportRequest)

5. Response received
   ├─ Set progress to 100%
   ├─ Open download URL in new tab
   └─ Auto-reset after 2 seconds

6. Error handling
   └─ Show Hebrew error message
```

## Export Request Structure

```typescript
const exportRequest: ExportRequest = {
  format: selectedFormat,              // 'excel' | 'pdf' | 'csv'
  filters: {
    startDate,                          // ISO date string
    endDate,                            // ISO date string
    categoryIds: selectedCategories.length > 0 
      ? selectedCategories 
      : undefined                       // Optional category filter
  },
  includeImages                         // boolean
};
```

## Styling Details

### Format Selector Cards
```css
Selected:
  - border-primary-600 (2px)
  - bg-primary-50
  - shadow-md

Unselected:
  - border-gray-200 (2px)
  - hover:border-gray-300
```

### Date Preset Buttons
```css
Selected:
  - bg-primary-600
  - text-white

Unselected:
  - bg-gray-100
  - text-gray-700
  - hover:bg-gray-200
```

### Category Filter Cards
```css
Selected:
  - border-primary-600 (2px)
  - bg-primary-50

Unselected:
  - border-gray-200 (2px)
  - hover:border-gray-300
```

### Progress Bar
```css
Container:
  - h-2
  - bg-gray-200
  - rounded-full

Fill:
  - h-full
  - bg-primary-600
  - transition-all duration-300
  - width: {exportProgress}%
```

## Responsive Design

### Mobile (< 640px)
- Single column layout
- Full-width cards
- Stacked date presets (2 columns)
- Stacked format cards

### Tablet (640px - 1024px)
- Two-column layout for categories
- Date presets in 4 columns
- Summary card below settings

### Desktop (> 1024px)
- Three-column grid (2:1 ratio)
- Summary card sticky in sidebar
- Full category grid (3 columns)

## Validation & Edge Cases

### No Receipts Warning
```typescript
{filteredReceipts.length === 0 && (
  <p className="mt-3 text-sm text-red-600 text-center">
    לא נמצאו קבלות בטווח התאריכים שנבחר
  </p>
)}
```

### Disabled Export Button
```typescript
disabled={isExporting || filteredReceipts.length === 0}
```

### Custom Date Validation
- Only shown when datePreset === 'custom'
- Both startDate and endDate required
- HTML5 date input type

## Accessibility

### Keyboard Navigation
- All buttons and inputs keyboard accessible
- Tab order: Format → Date → Categories → Options → Export

### Screen Reader Support
- Descriptive labels for all inputs
- Status updates for export progress
- Error messages announced

### Focus States
```css
focus:ring-2 focus:ring-primary-500
```

## Usage Example

```typescript
import { ExportPage } from '@/pages/export';

function App() {
  return (
    <Routes>
      <Route path="/export" element={<ExportPage />} />
    </Routes>
  );
}
```

## Tips for Users (Displayed in UI)

```
💡 טיפים לייצוא
• קובץ Excel מומלץ לרוב רואי החשבון
• PDF מתאים להדפסה ולשמירה
• CSV לעיבוד במערכות אחרות
• הקובץ יישמר 7 ימים בהיסטוריה
```

## Performance Optimizations

1. **Sticky Summary Card**: Uses `position: sticky` for sidebar
2. **Filtered Receipts**: Computed on-the-fly (no separate state)
3. **Progress Simulation**: Interval cleared on completion
4. **Auto-reset**: 2-second timeout to reset export state

## Future Enhancements (Phase 2)

- [ ] Email export option (send to accountant)
- [ ] Export history list
- [ ] Schedule recurring exports
- [ ] Custom templates
- [ ] Multi-format batch export
- [ ] Export presets (save filter combinations)

## Testing Checklist

- [ ] Format selection updates correctly
- [ ] Date presets calculate correct ranges
- [ ] Custom date inputs work properly
- [ ] Category multi-select toggles correctly
- [ ] Clear categories button works
- [ ] Include images checkbox updates
- [ ] Filtered receipts count is accurate
- [ ] Total amount calculation is correct
- [ ] VAT calculation is correct
- [ ] Export button disabled when no receipts
- [ ] Progress bar animates smoothly
- [ ] Download opens in new tab
- [ ] Error handling shows Hebrew message
- [ ] Responsive layout on mobile
- [ ] Responsive layout on tablet
- [ ] Responsive layout on desktop
- [ ] Sticky sidebar works correctly

## Dependencies

```json
{
  "lucide-react": "^0.294.0",
  "react": "^18.2.0",
  "@/components/layout/PageContainer": "internal",
  "@/components/ui/Button": "internal",
  "@/components/ui/Card": "internal",
  "@/components/ui/Input": "internal",
  "@/hooks/useReceipt": "internal",
  "@/types/receipt.types": "internal",
  "@/services/receipt.service": "internal"
}
```

## API Integration

### Endpoint
```
POST /api/receipts/export
```

### Request Body
```json
{
  "format": "excel",
  "filters": {
    "startDate": "2025-01-01",
    "endDate": "2025-01-31",
    "categoryIds": ["office-supplies", "travel"]
  },
  "includeImages": true
}
```

### Response
```json
{
  "downloadUrl": "https://s3.amazonaws.com/tiktax/exports/...",
  "fileName": "tiktax_export_2025-01.xlsx",
  "fileSize": 1048576,
  "expiresAt": "2025-02-01T12:00:00Z"
}
```

## Troubleshooting

### Issue: Export button stays disabled
**Solution**: Check that filteredReceipts.length > 0 and datePreset is valid

### Issue: Progress bar stuck at 90%
**Solution**: Check API response and error handling

### Issue: Custom dates not working
**Solution**: Ensure both startDate and endDate are set

### Issue: Categories not filtering
**Solution**: Verify selectedCategories state updates correctly

---

**Component Status**: ✅ Production Ready  
**Last Updated**: November 3, 2025  
**Maintainer**: Tik-Tax Development Team
