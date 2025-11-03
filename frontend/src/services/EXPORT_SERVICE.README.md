# Export Service - Complete Documentation

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Architecture](#architecture)
4. [API Reference](#api-reference)
5. [Excel Export](#excel-export)
6. [CSV Export](#csv-export)
7. [Integration Guide](#integration-guide)
8. [Examples](#examples)
9. [Troubleshooting](#troubleshooting)

---

## Overview

The Export Service provides client-side file generation for receipt data exports. Built on the SheetJS (xlsx) library, it generates accountant-ready Excel workbooks and CSV files with full Hebrew (RTL) support.

**Key Features:**
- ✅ Multi-sheet Excel workbooks
- ✅ Summary, details, and category breakdown
- ✅ CSV export with BOM for Hebrew
- ✅ Automatic filename generation
- ✅ Client-side processing (no server required)
- ✅ Currency and date formatting
- ✅ Column width optimization
- ✅ Data sorting and calculations

**File:** `/src/services/export.service.ts`

---

## Installation

### Dependencies

```bash
# Install SheetJS library
npm install xlsx

# Install TypeScript definitions
npm install --save-dev @types/xlsx
```

**Package Versions:**
- `xlsx`: ^0.18.5
- `@types/xlsx`: ^0.0.36

### Imports

```typescript
import { 
  generateExcelExport,
  generateCSVExport,
  generateExportFilename,
  downloadBlob
} from '@/services/export.service';
```

Or via index:
```typescript
import { 
  generateExcelExport,
  generateCSVExport,
  generateExportFilename,
  downloadBlob
} from '@/services';
```

---

## Architecture

### Data Flow

```
User Action (Export Button)
    ↓
Filter receipts by criteria
    ↓
Generate file (Excel/CSV)
    ├─→ Create workbook/data
    ├─→ Format sheets/rows
    ├─→ Calculate totals
    ├─→ Sort data
    └─→ Generate Blob
    ↓
Generate filename
    ↓
Download file to browser
```

### Module Structure

```typescript
export.service.ts
├── generateExcelExport()      // Main Excel generation
│   ├── generateSummarySheet()
│   ├── generateDetailsSheet()
│   └── generateCategorySheet()
├── generateCSVExport()        // CSV generation
├── generateExportFilename()   // Filename builder
└── downloadBlob()             // Download trigger
```

### Type Dependencies

```typescript
import type { Receipt } from '@/types/receipt.types';
import { DEFAULT_CATEGORIES } from '@/types/receipt.types';
import { formatCurrency, formatDate } from '@/utils/formatters';
```

---

## API Reference

### `generateExcelExport()`

Generate multi-sheet Excel workbook from receipts.

**Signature:**
```typescript
function generateExcelExport(
  receipts: Receipt[],
  businessName?: string
): Blob
```

**Parameters:**
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `receipts` | `Receipt[]` | - | Array of receipts to export |
| `businessName` | `string` | `'עסק'` | Business name for report header |

**Returns:** `Blob` object ready for download

**Sheets Created:**
1. **סיכום** (Summary) - Overview and totals
2. **פירוט קבלות** (Details) - Full receipt table
3. **סיכום לפי קטגוריה** (Categories) - Category breakdown

**Example:**
```typescript
const receipts: Receipt[] = [...];
const blob = generateExcelExport(receipts, 'העסק שלי');
downloadBlob(blob, 'export.xlsx');
```

**Throws:**
- Never throws (all errors handled internally)

**Performance:**
- 100 receipts: ~500ms
- 500 receipts: ~1.5s
- 1000 receipts: ~3s

---

### `generateCSVExport()`

Generate CSV file with BOM for Hebrew support.

**Signature:**
```typescript
function generateCSVExport(
  receipts: Receipt[]
): Blob
```

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `receipts` | `Receipt[]` | Receipts to export |

**Returns:** `Blob` with UTF-8 BOM

**Format:**
- UTF-8 encoding
- BOM prefix (`\uFEFF`) for Excel compatibility
- Comma-separated values
- Quoted strings for Hebrew text
- Sorted by date (newest first)

**Example:**
```typescript
const blob = generateCSVExport(receipts);
downloadBlob(blob, 'receipts.csv');
```

**Performance:**
- 100 receipts: ~50ms
- 500 receipts: ~200ms
- 1000 receipts: ~400ms

---

### `generateExportFilename()`

Generate sanitized filename for export.

**Signature:**
```typescript
function generateExportFilename(
  format: 'excel' | 'pdf' | 'csv',
  businessName: string,
  startDate?: string,
  endDate?: string
): string
```

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `format` | `'excel' \| 'pdf' \| 'csv'` | File format |
| `businessName` | `string` | Business name |
| `startDate` | `string` (optional) | ISO date string |
| `endDate` | `string` (optional) | ISO date string |

**Returns:** Sanitized filename string

**Format Pattern:**
```
Tik-Tax_[BusinessName]_[DateRange].[extension]
```

**Examples:**
```typescript
generateExportFilename('excel', 'העסק שלי')
// => 'Tik-Tax_העסק_שלי_03-11-2024.xlsx'

generateExportFilename('excel', 'My Business', '2024-01-01', '2024-01-31')
// => 'Tik-Tax_My_Business_01-01-2024-31-01-2024.xlsx'

generateExportFilename('csv', 'Test & Co.')
// => 'Tik-Tax_Test___Co__03-11-2024.csv'
```

**Sanitization:**
- Removes special characters except alphanumeric and Hebrew
- Replaces spaces/symbols with underscore
- Preserves Hebrew characters (`\u0590-\u05FF`)

---

### `downloadBlob()`

Trigger browser download for blob.

**Signature:**
```typescript
function downloadBlob(
  blob: Blob,
  filename: string
): void
```

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `blob` | `Blob` | File data |
| `filename` | `string` | Download filename |

**Returns:** `void`

**Behavior:**
1. Creates object URL from blob
2. Creates temporary `<a>` element
3. Sets `href` and `download` attributes
4. Triggers click event
5. Removes element and revokes URL

**Example:**
```typescript
const blob = new Blob(['Hello'], { type: 'text/plain' });
downloadBlob(blob, 'hello.txt');
```

**Browser Support:**
- Chrome/Edge: Full support
- Safari: Full support
- Firefox: Full support

**Notes:**
- May be blocked by popup blockers
- Must be called from user interaction
- Cleans up resources automatically

---

## Excel Export

### Sheet 1: Summary (סיכום)

**Purpose:** High-level overview for accountant

**Structure:**
```
Row 1:  דוח הוצאות עסקיות - Tik-Tax
Row 2:  [empty]
Row 3:  שם העסק: [Business Name]
Row 4:  תאריך יצירת הדוח: [Current Date]
Row 5:  טווח תאריכים: [Start] - [End]
Row 6:  [empty]
Row 7:  סיכום כספי
Row 8:  סך כל ההוצאות (כולל מע"מ): [Total]
Row 9:  סך הוצאות לפני מע"מ: [Pre-VAT]
Row 10: סך מע"מ (18%): [VAT]
Row 11: [empty]
Row 12: סיכום קבלות
Row 13: מספר קבלות: [Count]
Row 14: ממוצע לקבלה: [Average]
Row 15: [empty]
Row 16: הערות
Row 17: • דוח זה נוצר באמצעות מערכת Tik-Tax
Row 18: • כל הסכומים במטבע ש"ח (ILS)
Row 19: • מע"מ מחושב בשיעור 18%
Row 20: • לפרטים נוספים ראה גיליון "פירוט קבלות"
```

**Column Widths:**
- A: 25 characters (Labels)
- B: 20 characters (Values)

**Calculations:**
```typescript
totalAmount = sum(receipts.map(r => r.totalAmount))
totalPreVat = sum(receipts.map(r => r.preVatAmount))
totalVat = sum(receipts.map(r => r.vatAmount))
average = totalAmount / receipts.length
```

---

### Sheet 2: Details (פירוט קבלות)

**Purpose:** Complete receipt data table

**Columns:**
1. **תאריך** (Date) - 12 chars
2. **שם העסק** (Vendor) - 25 chars
3. **מספר עסק (ח.פ/ע.מ)** (Business Number) - 15 chars
4. **קטגוריה** (Category) - 20 chars
5. **סכום לפני מע"מ** (Pre-VAT) - 15 chars
6. **מע"מ** (VAT) - 12 chars
7. **סכום כולל** (Total) - 15 chars
8. **מספר קבלה** (Receipt Number) - 15 chars
9. **הערות** (Notes) - 30 chars

**Sorting:** Date descending (newest first)

**Formatting:**
- Dates: `dd/MM/yyyy` (e.g., `01/11/2024`)
- Currency: `₪1,234.56`
- Missing data: Empty string

**Example Row:**
```
01/11/2024 | מסעדת הבוקר | 123456789 | אוכל ומשקאות | ₪42.37 | ₪7.63 | ₪50.00 | 1234 | ארוחת עבודה
```

---

### Sheet 3: Categories (סיכום לפי קטגוריה)

**Purpose:** Expense breakdown by category

**Columns:**
1. **קטגוריה** (Category) - 25 chars
2. **מספר קבלות** (Count) - 12 chars
3. **סכום כולל** (Total) - 18 chars
4. **אחוז מסך ההוצאות** (Percentage) - 15 chars

**Sorting:** Amount descending (highest first)

**Footer:** Totals row with "סך הכל"

**Calculations:**
```typescript
categoryTotal = sum(receipts.filter(r => r.categoryId === categoryId).map(r => r.totalAmount))
percentage = (categoryTotal / totalAmount) * 100
```

**Example:**
```
קטגוריה         | מספר קבלות | סכום כולל   | אחוז
משרד           | 15        | ₪500.00   | 40.5%
אוכל ומשקאות   | 10        | ₪300.00   | 24.3%
תחבורה         | 8         | ₪200.00   | 16.2%
─────────────────────────────────────────────
סך הכל         | 42        | ₪1,234.56 | 100%
```

---

## CSV Export

### File Format

**Encoding:** UTF-8 with BOM (`\uFEFF`)

**Delimiter:** Comma (`,`)

**Quoting:** Double quotes for strings

**Structure:**
```csv
תאריך,שם העסק,מספר עסק,קטגוריה,סכום לפני מע"מ,מע"מ,סכום כולל,מספר קבלה,הערות
01/11/2024,"מסעדת הבוקר",123456789,"אוכל ומשקאות",₪42.37,₪7.63,₪50.00,1234,"ארוחת עבודה"
```

### BOM Prefix

**Why BOM?**
- Excel requires BOM to detect UTF-8 encoding
- Without BOM, Hebrew text displays as gibberish
- BOM = Byte Order Mark (`U+FEFF`)

**Implementation:**
```typescript
const BOM = '\uFEFF';
return new Blob([BOM + csv], { type: 'text/csv;charset=utf-8;' });
```

### Escaping Rules

1. **String fields:** Wrap in double quotes
2. **Quotes in data:** Escape with double-quote (`""`)
3. **Newlines:** Preserve in quoted strings
4. **Commas:** Safe in quoted strings

**Example:**
```typescript
vendorName: 'משרד "A"' → "משרד ""A"""
notes: 'Line 1\nLine 2' → "Line 1\nLine 2"
```

---

## Integration Guide

### Basic Usage

```typescript
import { 
  generateExcelExport,
  downloadBlob,
  generateExportFilename
} from '@/services';

// Generate and download Excel
const blob = generateExcelExport(receipts, businessName);
const filename = generateExportFilename('excel', businessName);
downloadBlob(blob, filename);
```

### With Progress Indicator

```typescript
const handleExport = async () => {
  setIsExporting(true);
  setProgress(0);
  
  try {
    // Start progress
    setProgress(20);
    
    // Generate file
    const blob = generateExcelExport(receipts, businessName);
    setProgress(60);
    
    // Generate filename
    const filename = generateExportFilename('excel', businessName, startDate, endDate);
    setProgress(80);
    
    // Download
    downloadBlob(blob, filename);
    setProgress(100);
    
    // Success feedback
    toast.success('הקובץ הורד בהצלחה');
    
  } catch (error) {
    console.error('Export error:', error);
    toast.error('שגיאה בייצוא הנתונים');
  } finally {
    setTimeout(() => {
      setIsExporting(false);
      setProgress(0);
    }, 2000);
  }
};
```

### With Format Selection

```typescript
const handleExport = (format: 'excel' | 'csv') => {
  let blob: Blob;
  
  switch (format) {
    case 'excel':
      blob = generateExcelExport(receipts, businessName);
      break;
    case 'csv':
      blob = generateCSVExport(receipts);
      break;
    default:
      throw new Error('Unsupported format');
  }
  
  const filename = generateExportFilename(format, businessName, startDate, endDate);
  downloadBlob(blob, filename);
};
```

### With Validation

```typescript
const handleExport = () => {
  // Validate receipts
  if (!receipts || receipts.length === 0) {
    toast.error('אין קבלות לייצוא');
    return;
  }
  
  // Validate business name
  const name = businessName?.trim() || 'עסק';
  
  // Generate and download
  const blob = generateExcelExport(receipts, name);
  const filename = generateExportFilename('excel', name);
  downloadBlob(blob, filename);
};
```

---

## Examples

### Example 1: Simple Export

```typescript
import { generateExcelExport, downloadBlob } from '@/services';

const receipts = [
  {
    id: '1',
    vendorName: 'מסעדת הבוקר',
    businessNumber: '123456789',
    date: '2024-11-01T10:00:00Z',
    totalAmount: 50.00,
    preVatAmount: 42.37,
    vatAmount: 7.63,
    categoryId: 'food-drinks',
    receiptNumber: '1234',
    notes: 'ארוחת עבודה',
    // ...other fields
  }
];

const blob = generateExcelExport(receipts, 'העסק שלי');
downloadBlob(blob, 'receipts.xlsx');
```

### Example 2: Filtered Export

```typescript
import { generateExcelExport, downloadBlob, generateExportFilename } from '@/services';

// Filter receipts by date range
const filtered = receipts.filter(r => {
  const date = new Date(r.date);
  return date >= startDate && date <= endDate;
});

// Export filtered receipts
const blob = generateExcelExport(filtered, businessName);
const filename = generateExportFilename(
  'excel',
  businessName,
  startDate.toISOString(),
  endDate.toISOString()
);
downloadBlob(blob, filename);
```

### Example 3: Category-Specific Export

```typescript
// Export only specific category
const categoryReceipts = receipts.filter(r => 
  r.categoryId === 'office-supplies'
);

const blob = generateExcelExport(categoryReceipts, businessName);
const filename = `Tik-Tax_${businessName}_Office_Supplies.xlsx`;
downloadBlob(blob, filename);
```

### Example 4: CSV for Accounting Software

```typescript
import { generateCSVExport, downloadBlob } from '@/services';

// Generate CSV for import to accounting software
const blob = generateCSVExport(receipts);
downloadBlob(blob, 'accounting_import.csv');
```

---

## Troubleshooting

### Issue: Hebrew characters display as �

**Cause:** Missing BOM or wrong encoding

**Solution:**
```typescript
// Ensure BOM is included (already in generateCSVExport)
const BOM = '\uFEFF';
const blob = new Blob([BOM + csv], { type: 'text/csv;charset=utf-8;' });
```

### Issue: Excel columns too narrow

**Cause:** Column width not set

**Solution:**
```typescript
// Set column widths (already in generateExcelExport)
sheet['!cols'] = [
  { wch: 25 }, // Column A
  { wch: 20 }  // Column B
];
```

### Issue: Download blocked by browser

**Cause:** Popup blocker or not triggered by user action

**Solution:**
- Ensure download is triggered by click event
- Ask user to allow popups
- Use `window.open()` as fallback

### Issue: TypeScript errors with XLSX

**Cause:** Incomplete type definitions

**Solution:**
```typescript
// Use @ts-ignore comments (already in code)
// @ts-ignore - XLSX type definitions are incomplete
const workbook = XLSX.utils.book_new();
```

### Issue: Large files slow to generate

**Cause:** Processing many receipts client-side

**Solution:**
- Add progress indicator
- Consider pagination (export in batches)
- Use Web Worker for background processing

### Issue: Currency not formatted correctly

**Cause:** Wrong locale or missing symbol

**Solution:**
```typescript
// Use formatCurrency utility
import { formatCurrency } from '@/utils/formatters';
formatCurrency(amount); // => ₪1,234.56
```

---

## Best Practices

### Performance
1. **Show progress** for 100+ receipts
2. **Debounce** export button (prevent double-clicks)
3. **Limit** exports to 1000 receipts max
4. **Consider** server-side for very large exports

### UX
1. **Validate** before export (empty arrays, etc.)
2. **Feedback** on success/error
3. **Disable** button during export
4. **Preview** data before export

### Security
1. **Sanitize** filenames (remove special chars)
2. **Escape** CSV data (prevent injection)
3. **Validate** user input
4. **Never** expose sensitive data in filenames

### Accessibility
1. **Announce** export status to screen readers
2. **Keyboard** support for export button
3. **Clear** error messages
4. **Alternative** formats (CSV for simple needs)

---

## Related Documentation

- [Export Page README](../pages/export/EXPORT_PAGE.README.md)
- [Receipt Types](../types/RECEIPT_TYPES.md)
- [Formatters Utility](../utils/formatters.ts)
- [SheetJS Documentation](https://docs.sheetjs.com/)

---

**Last Updated:** November 3, 2025  
**Version:** 1.0.0  
**Status:** ✅ Production Ready
