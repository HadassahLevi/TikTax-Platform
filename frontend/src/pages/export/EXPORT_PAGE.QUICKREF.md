# Export Page - Quick Reference

## 📁 File Location
```
/src/pages/export/ExportPage.tsx
```

## 🚀 Quick Import
```typescript
import { ExportPage } from '@/pages/export';
```

## 🎯 Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| Format Selection | Excel/PDF/CSV | ✅ |
| Date Presets | This month, Last month, This year, Custom | ✅ |
| Category Filter | Multi-select with icons | ✅ |
| Include Images | Toggle for image export | ✅ |
| Real-time Preview | Live count and totals | ✅ |
| Export Progress | Animated progress bar | ✅ |
| Summary Card | Sticky sidebar metrics | ✅ |

## 📊 State Variables

```typescript
// Format & Settings
selectedFormat: 'excel' | 'pdf' | 'csv'
datePreset: 'this_month' | 'last_month' | 'this_year' | 'last_year' | 'custom'
customStartDate: string
customEndDate: string
selectedCategories: string[]
includeImages: boolean

// Export Progress
isExporting: boolean
exportProgress: number (0-100)
```

## 🔧 Key Functions

### getDateRange()
Calculates start and end dates based on preset selection.

```typescript
Returns: { startDate: string; endDate: string }
```

### toggleCategory(categoryId)
Toggles category in/out of selected categories array.

### handleExport()
Main export function - builds request and calls API.

## 🎨 Styling

### Colors
- Primary: `#2563EB` (Blue)
- Success: `#10B981` (Green)
- Error: `#EF4444` (Red)
- Info: `#3B82F6` (Blue)

### Spacing
- Card padding: `24px` (lg)
- Grid gap: `24px` (6)
- Button height: `48px` (lg)

## 📱 Responsive Breakpoints

```typescript
Mobile:  < 640px   → Single column
Tablet:  640-1024px → Two columns
Desktop: > 1024px  → Three columns (2:1)
```

## 🔌 API Call

```typescript
const response = await receiptService.exportReceipts({
  format: selectedFormat,
  filters: {
    startDate,
    endDate,
    categoryIds: selectedCategories.length > 0 ? selectedCategories : undefined
  },
  includeImages
});

// Open download
window.open(response.downloadUrl, '_blank');
```

## ⚡ Performance Tips

1. Use `React.memo` for category cards (future optimization)
2. Debounce custom date inputs if needed
3. Progress simulation runs at 200ms intervals
4. Auto-reset state after 2 seconds

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| Export disabled | Check `filteredReceipts.length > 0` |
| Progress stuck | Check API error handling |
| Custom dates not working | Both dates must be set |
| Categories not filtering | Verify state updates |

## 📋 Checklist for Integration

- [ ] Add route: `/export` → `<ExportPage />`
- [ ] Verify `useReceipt` hook is available
- [ ] Test `receiptService.exportReceipts()` API
- [ ] Check Hebrew text rendering (RTL)
- [ ] Test responsive layout (mobile/tablet/desktop)
- [ ] Verify sticky sidebar works
- [ ] Test export progress animation
- [ ] Check error handling displays Hebrew messages

## 🎯 User Flow

```
1. User selects format (Excel/PDF/CSV)
2. User chooses date range (preset or custom)
3. User optionally filters categories
4. User optionally toggles image inclusion
5. Preview shows filtered receipts and totals
6. User clicks "הורד דוח" (Download Report)
7. Progress bar animates (0→100%)
8. Download opens in new tab
9. State resets after 2 seconds
```

## 🌐 Hebrew UI Text

```typescript
// Buttons
"הורד דוח"        → "Download Report"
"נקה בחירה"      → "Clear Selection"
"מותאם אישית"    → "Custom"

// Labels
"בחר פורמט ייצוא"        → "Choose Export Format"
"טווח תאריכים"          → "Date Range"
"סינון לפי קטגוריות"    → "Filter by Categories"
"אפשרויות נוספות"       → "Additional Options"
"סיכום"                  → "Summary"
"קבלות לייצוא"          → "Receipts to Export"
```

## 📦 Component Dependencies

```
ExportPage
├── PageContainer (layout wrapper)
├── Button (export action)
├── Card (sections)
├── Input (date inputs)
├── useReceipt (hook for receipts data)
├── receipt.service (API calls)
└── receipt.types (types & utilities)
```

## 🔐 Security Notes

- All exports require authentication
- Download URLs are pre-signed (temporary)
- URLs expire after 7 days
- Images only included if explicitly requested

## 📈 Metrics Tracked

```typescript
filteredReceipts.length  → Count of receipts
totalAmount              → Sum of all amounts
totalVat                 → Sum of all VAT
selectedCategories.length → Number of filters
```

## 🎨 Design Tokens

```typescript
// Border Radius
Card: 12px (rounded-xl)
Button: 8px (rounded-lg)
Progress: 9999px (rounded-full)

// Shadows
Card: 0 4px 6px -1px rgba(0,0,0,0.1)
Format Card (selected): 0 4px 8px -2px rgba(0,0,0,0.12)

// Transitions
All: 0.2s ease
Progress: 0.3s ease-out
```

## 🧪 Testing Commands

```bash
# Check TypeScript
npm run type-check

# Run tests (when available)
npm run test src/pages/export

# Build check
npm run build
```

---

**Quick Start**: Import → Add Route → Test Export Flow  
**Status**: ✅ Production Ready  
**Updated**: Nov 3, 2025
