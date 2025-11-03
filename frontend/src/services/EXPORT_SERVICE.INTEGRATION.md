# ExportPage Integration Example

## How to Integrate Export Service into ExportPage.tsx

### 1. Update Imports

```typescript
// At the top of ExportPage.tsx, add:
import {
  generateExcelExport,
  generateCSVExport,
  generateExportFilename,
  downloadBlob
} from '@/services';
```

### 2. Replace handleExport Function

Replace the existing `handleExport` function with:

```typescript
const handleExport = async () => {
  setIsExporting(true);
  setExportProgress(0);
  
  try {
    // Validate
    if (filteredReceipts.length === 0) {
      alert('אין קבלות לייצוא');
      setIsExporting(false);
      return;
    }
    
    let blob: Blob;
    let filename: string;
    
    // Start progress
    setExportProgress(20);
    
    // Generate file based on format
    switch (selectedFormat) {
      case 'excel': {
        // Generate Excel
        blob = generateExcelExport(
          filteredReceipts,
          user?.businessName || 'עסק'
        );
        
        // Generate filename
        filename = generateExportFilename(
          'excel',
          user?.businessName || 'עסק',
          startDate,
          endDate
        );
        
        setExportProgress(70);
        break;
      }
      
      case 'csv': {
        // Generate CSV
        blob = generateCSVExport(filteredReceipts);
        
        // Generate filename
        filename = generateExportFilename(
          'csv',
          user?.businessName || 'עסק',
          startDate,
          endDate
        );
        
        setExportProgress(70);
        break;
      }
      
      case 'pdf': {
        // PDF not yet implemented
        alert('ייצוא PDF יושם בקרוב');
        setIsExporting(false);
        setExportProgress(0);
        return;
      }
      
      default:
        throw new Error('פורמט לא נתמך');
    }
    
    // Download file
    setExportProgress(90);
    downloadBlob(blob, filename);
    
    // Complete
    setExportProgress(100);
    
    // Reset after 2 seconds
    setTimeout(() => {
      setIsExporting(false);
      setExportProgress(0);
    }, 2000);
    
  } catch (error) {
    console.error('Export error:', error);
    setIsExporting(false);
    setExportProgress(0);
    alert('שגיאה בייצוא הנתונים. נסה שוב.');
  }
};
```

### 3. Remove Mock Service (if exists)

If there's a mock `exportReceipts` service call, remove it:

```typescript
// REMOVE THIS:
// const response = await receiptService.exportReceipts({
//   format: selectedFormat,
//   filters: { ... },
//   includeImages
// });
```

### 4. Update User Context (if needed)

Make sure you have access to `user?.businessName`:

```typescript
// At top of component
import { useAuthStore } from '@/stores';

// Inside component
const ExportPage: React.FC = () => {
  const { user } = useAuthStore();
  
  // ... rest of component
};
```

### 5. Test the Integration

```typescript
// Test data (can be removed after testing)
const testReceipts: Receipt[] = [
  {
    id: '1',
    vendorName: 'מסעדת הבוקר',
    businessNumber: '123456789',
    date: new Date().toISOString(),
    totalAmount: 50.00,
    preVatAmount: 42.37,
    vatAmount: 7.63,
    categoryId: 'food-drinks',
    receiptNumber: '1234',
    notes: 'ארוחת עבודה',
    status: 'approved',
    // ... other required fields
  }
];

// Test export
console.log('Testing export with', testReceipts.length, 'receipts');
const blob = generateExcelExport(testReceipts, 'טסט');
downloadBlob(blob, 'test.xlsx');
```

---

## Complete Updated ExportPage.tsx

### Imports Section

```typescript
import React, { useState, useMemo } from 'react';
import { Download, FileSpreadsheet, FileText, Calendar, X } from 'lucide-react';
import {
  generateExcelExport,
  generateCSVExport,
  generateExportFilename,
  downloadBlob
} from '@/services';
import { useAuthStore } from '@/stores';
import type { Receipt } from '@/types';
import { DEFAULT_CATEGORIES } from '@/types';

// ... rest of imports
```

### Component Code

```typescript
const ExportPage: React.FC = () => {
  // Auth context
  const { user } = useAuthStore();
  
  // State
  const [selectedFormat, setSelectedFormat] = useState<'excel' | 'pdf' | 'csv'>('excel');
  const [selectedRange, setSelectedRange] = useState<'this-month' | 'last-month' | 'this-year' | 'custom'>('this-month');
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [includeImages, setIncludeImages] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [exportProgress, setExportProgress] = useState(0);
  
  // TODO: Replace with actual receipt data from store/API
  const allReceipts: Receipt[] = useMemo(() => [], []);
  
  // Filter receipts
  const filteredReceipts = useMemo(() => {
    return allReceipts.filter(receipt => {
      // Date filter
      const receiptDate = new Date(receipt.date);
      const start = startDate ? new Date(startDate) : null;
      const end = endDate ? new Date(endDate) : null;
      
      if (start && receiptDate < start) return false;
      if (end && receiptDate > end) return false;
      
      // Category filter
      if (selectedCategories.length > 0 && !selectedCategories.includes(receipt.categoryId)) {
        return false;
      }
      
      return true;
    });
  }, [allReceipts, startDate, endDate, selectedCategories]);
  
  // Calculate totals
  const totalAmount = useMemo(() => 
    filteredReceipts.reduce((sum, r) => sum + r.totalAmount, 0),
    [filteredReceipts]
  );
  
  const vatAmount = useMemo(() =>
    filteredReceipts.reduce((sum, r) => sum + r.vatAmount, 0),
    [filteredReceipts]
  );
  
  // Export handler
  const handleExport = async () => {
    setIsExporting(true);
    setExportProgress(0);
    
    try {
      // Validate
      if (filteredReceipts.length === 0) {
        alert('אין קבלות לייצוא');
        setIsExporting(false);
        return;
      }
      
      let blob: Blob;
      let filename: string;
      
      setExportProgress(20);
      
      // Generate file
      switch (selectedFormat) {
        case 'excel': {
          blob = generateExcelExport(
            filteredReceipts,
            user?.businessName || 'עסק'
          );
          filename = generateExportFilename(
            'excel',
            user?.businessName || 'עסק',
            startDate,
            endDate
          );
          setExportProgress(70);
          break;
        }
        
        case 'csv': {
          blob = generateCSVExport(filteredReceipts);
          filename = generateExportFilename(
            'csv',
            user?.businessName || 'עסק',
            startDate,
            endDate
          );
          setExportProgress(70);
          break;
        }
        
        case 'pdf': {
          alert('ייצוא PDF יושם בקרוב');
          setIsExporting(false);
          setExportProgress(0);
          return;
        }
        
        default:
          throw new Error('פורמט לא נתמך');
      }
      
      // Download
      setExportProgress(90);
      downloadBlob(blob, filename);
      
      setExportProgress(100);
      
      // Reset
      setTimeout(() => {
        setIsExporting(false);
        setExportProgress(0);
      }, 2000);
      
    } catch (error) {
      console.error('Export error:', error);
      setIsExporting(false);
      setExportProgress(0);
      alert('שגיאה בייצוא הנתונים. נסה שוב.');
    }
  };
  
  // ... rest of component (JSX)
};

export default ExportPage;
```

---

## Testing Checklist

After integration, test the following:

### Excel Export
- [ ] Click "Excel" format
- [ ] Click "הורד דוח" button
- [ ] File downloads automatically
- [ ] File opens in Excel/LibreOffice/Numbers
- [ ] 3 sheets are present (סיכום, פירוט קבלות, סיכום לפי קטגוריה)
- [ ] Hebrew text displays correctly
- [ ] Currency formatted as ₪1,234.56
- [ ] Dates formatted as dd/MM/yyyy
- [ ] Calculations are correct
- [ ] Data is sorted correctly

### CSV Export
- [ ] Click "CSV" format
- [ ] Click "הורד דוח" button
- [ ] File downloads automatically
- [ ] File opens in Excel
- [ ] Hebrew text displays correctly (not gibberish)
- [ ] Comma separation works
- [ ] Quoted strings handled properly

### Filtering
- [ ] "This Month" preset works
- [ ] "Last Month" preset works
- [ ] "This Year" preset works
- [ ] Custom date range works
- [ ] Category filtering works
- [ ] Multiple categories work
- [ ] Summary totals update correctly

### Progress & UX
- [ ] Progress bar appears
- [ ] Progress percentage shows
- [ ] Button disables during export
- [ ] Progress resets after 2 seconds
- [ ] Error messages show if something fails

### Edge Cases
- [ ] Export with 0 receipts (should show alert)
- [ ] Export with 1 receipt
- [ ] Export with 1000+ receipts
- [ ] Export with missing business name (uses "עסק")
- [ ] Export with special characters in business name

---

## Troubleshooting

### Issue: Download doesn't start

**Check:**
1. Browser console for errors
2. Popup blocker settings
3. Download permissions

**Solution:**
- Ensure export is triggered by user click
- Check browser downloads settings
- Try different browser

### Issue: Hebrew text is gibberish in CSV

**Check:**
- File opened in Excel
- BOM prefix is present

**Solution:**
- Already handled in `generateCSVExport()`
- If still broken, try opening with "Data > From Text/CSV" in Excel

### Issue: Excel file won't open

**Check:**
- File extension is `.xlsx`
- File size is reasonable
- XLSX library installed

**Solution:**
- Verify `xlsx` package is installed
- Check TypeScript compilation
- Try re-generating file

---

## Next Steps After Integration

1. **Replace Mock Data**
   - Connect to actual receipt store
   - Use real user data
   
2. **Add Error Boundary**
   - Wrap export in try-catch
   - Show user-friendly error messages
   
3. **Add Success Toast**
   - Replace `alert()` with toast notifications
   - Show download progress
   
4. **Performance Optimization**
   - Add loading state for large datasets
   - Consider pagination for 1000+ receipts
   
5. **User Testing**
   - Test with real accountants
   - Gather feedback on format
   - Iterate on column widths/layout

---

**Ready to integrate!** 🚀
