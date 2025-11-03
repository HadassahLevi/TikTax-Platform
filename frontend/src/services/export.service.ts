/**
 * Export Service
 * 
 * Handles Excel, CSV, and PDF export generation for receipts.
 * Uses SheetJS (xlsx) library for Excel file creation.
 * 
 * Features:
 * - Multi-sheet Excel workbooks (Summary, Details, Category Breakdown)
 * - CSV export with Hebrew BOM support
 * - Automatic filename generation
 * - Client-side file download
 * - Proper RTL formatting for Hebrew
 * 
 * @module services/export.service
 */

import XLSX from 'xlsx';
import { formatCurrency, formatDate } from '@/utils/formatters';
import type { Receipt } from '@/types/receipt.types';
import { DEFAULT_CATEGORIES } from '@/types/receipt.types';

/**
 * Generate Excel file from receipts
 * 
 * Creates a multi-sheet Excel workbook with:
 * 1. Summary sheet - Totals, date range, business info
 * 2. Detailed receipts - Full receipt data in table format
 * 3. Category breakdown - Grouped totals by category
 * 
 * @param receipts - Array of receipts to export
 * @param businessName - Name of the business (for summary sheet)
 * @returns Blob object ready for download
 * 
 * @example
 * ```typescript
 * const blob = generateExcelExport(receipts, 'העסק שלי');
 * downloadBlob(blob, 'export.xlsx');
 * ```
 */
export const generateExcelExport = (
  receipts: Receipt[],
  businessName: string = 'עסק'
): Blob => {
  // Create workbook
  // @ts-ignore - XLSX type definitions are incomplete
  const workbook = XLSX.utils.book_new();
  
  // Sheet 1: Summary
  const summaryData = generateSummarySheet(receipts, businessName);
  const summarySheet = XLSX.utils.aoa_to_sheet(summaryData);
  
  // Set column widths for summary
  summarySheet['!cols'] = [
    { wch: 25 }, // Label
    { wch: 20 }  // Value
  ];
  
  // @ts-ignore - XLSX type definitions are incomplete
  XLSX.utils.book_append_sheet(workbook, summarySheet, 'סיכום');
  
  // Sheet 2: Detailed receipts
  const detailsData = generateDetailsSheet(receipts);
  const detailsSheet = XLSX.utils.aoa_to_sheet(detailsData);
  
  // Set column widths for details
  detailsSheet['!cols'] = [
    { wch: 12 }, // Date
    { wch: 25 }, // Vendor
    { wch: 15 }, // Business Number
    { wch: 20 }, // Category
    { wch: 15 }, // Pre-VAT
    { wch: 12 }, // VAT
    { wch: 15 }, // Total
    { wch: 15 }, // Receipt Number
    { wch: 30 }  // Notes
  ];
  
  // @ts-ignore - XLSX type definitions are incomplete
  XLSX.utils.book_append_sheet(workbook, detailsSheet, 'פירוט קבלות');
  
  // Sheet 3: By Category
  const categoryData = generateCategorySheet(receipts);
  const categorySheet = XLSX.utils.aoa_to_sheet(categoryData);
  
  categorySheet['!cols'] = [
    { wch: 25 }, // Category
    { wch: 12 }, // Count
    { wch: 18 }, // Total Amount
    { wch: 15 }  // Percentage
  ];
  
  // @ts-ignore - XLSX type definitions are incomplete
  XLSX.utils.book_append_sheet(workbook, categorySheet, 'סיכום לפי קטגוריה');
  
  // Generate binary file
  const excelBuffer = XLSX.write(workbook, { 
    bookType: 'xlsx', 
    type: 'buffer'
  }) as ArrayBuffer;
  
  return new Blob([excelBuffer], { 
    type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
  });
};

/**
 * Generate summary sheet data
 * 
 * Creates overview with:
 * - Business information
 * - Date range
 * - Financial totals (pre-VAT, VAT, total)
 * - Receipt count and average
 * - Report notes
 * 
 * @param receipts - Receipts to summarize
 * @param businessName - Business name for header
 * @returns 2D array for Excel sheet
 */
const generateSummarySheet = (receipts: Receipt[], businessName: string): any[][] => {
  const totalAmount = receipts.reduce((sum, r) => sum + r.totalAmount, 0);
  const totalVat = receipts.reduce((sum, r) => sum + r.vatAmount, 0);
  const totalPreVat = receipts.reduce((sum, r) => sum + r.preVatAmount, 0);
  
  const startDate = receipts.length > 0 
    ? new Date(Math.min(...receipts.map(r => new Date(r.date).getTime())))
    : new Date();
  const endDate = receipts.length > 0
    ? new Date(Math.max(...receipts.map(r => new Date(r.date).getTime())))
    : new Date();
  
  return [
    ['דוח הוצאות עסקיות - Tik-Tax'],
    [],
    ['שם העסק:', businessName],
    ['תאריך יצירת הדוח:', new Date().toLocaleDateString('he-IL')],
    ['טווח תאריכים:', `${formatDate(startDate.toISOString())} - ${formatDate(endDate.toISOString())}`],
    [],
    ['סיכום כספי'],
    ['סך כל ההוצאות (כולל מע"מ):', formatCurrency(totalAmount)],
    ['סך הוצאות לפני מע"מ:', formatCurrency(totalPreVat)],
    ['סך מע"מ (18%):', formatCurrency(totalVat)],
    [],
    ['סיכום קבלות'],
    ['מספר קבלות:', receipts.length],
    ['ממוצע לקבלה:', receipts.length > 0 ? formatCurrency(totalAmount / receipts.length) : '₪0.00'],
    [],
    ['הערות'],
    ['• דוח זה נוצר באמצעות מערכת Tik-Tax'],
    ['• כל הסכומים במטבע ש"ח (ILS)'],
    ['• מע"מ מחושב בשיעור 18%'],
    ['• לפרטים נוספים ראה גיליון "פירוט קבלות"']
  ];
};

/**
 * Generate detailed receipts sheet
 * 
 * Creates table with all receipt data:
 * - Date (sorted newest first)
 * - Vendor name
 * - Business number
 * - Category
 * - Financial breakdown (pre-VAT, VAT, total)
 * - Receipt number
 * - Notes
 * 
 * @param receipts - Receipts to detail
 * @returns 2D array with headers and data rows
 */
const generateDetailsSheet = (receipts: Receipt[]): any[][] => {
  const headers = [
    'תאריך',
    'שם העסק',
    'מספר עסק (ח.פ/ע.מ)',
    'קטגוריה',
    'סכום לפני מע"מ',
    'מע"מ',
    'סכום כולל',
    'מספר קבלה',
    'הערות'
  ];
  
  const rows = receipts
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
    .map(receipt => {
      const category = DEFAULT_CATEGORIES.find(c => c.id === receipt.categoryId);
      
      return [
        formatDate(receipt.date),
        receipt.vendorName,
        receipt.businessNumber,
        category?.nameHe || 'אחר',
        formatCurrency(receipt.preVatAmount),
        formatCurrency(receipt.vatAmount),
        formatCurrency(receipt.totalAmount),
        receipt.receiptNumber || '',
        receipt.notes || ''
      ];
    });
  
  return [headers, ...rows];
};

/**
 * Generate category summary sheet
 * 
 * Groups receipts by category and shows:
 * - Category name
 * - Receipt count
 * - Total amount
 * - Percentage of total expenses
 * - Totals row at bottom
 * 
 * Sorted by amount (highest first)
 * 
 * @param receipts - Receipts to group
 * @returns 2D array with category breakdown
 */
const generateCategorySheet = (receipts: Receipt[]): any[][] => {
  const totalAmount = receipts.reduce((sum, r) => sum + r.totalAmount, 0);
  
  // Group by category
  const categoryMap = new Map<string, { count: number; amount: number }>();
  
  receipts.forEach(receipt => {
    const existing = categoryMap.get(receipt.categoryId) || { count: 0, amount: 0 };
    categoryMap.set(receipt.categoryId, {
      count: existing.count + 1,
      amount: existing.amount + receipt.totalAmount
    });
  });
  
  const headers = ['קטגוריה', 'מספר קבלות', 'סכום כולל', 'אחוז מסך ההוצאות'];
  
  const rows = Array.from(categoryMap.entries())
    .map(([categoryId, data]) => {
      const category = DEFAULT_CATEGORIES.find(c => c.id === categoryId);
      const percentage = totalAmount > 0 ? (data.amount / totalAmount) * 100 : 0;
      
      return [
        category?.nameHe || 'אחר',
        data.count,
        formatCurrency(data.amount),
        `${percentage.toFixed(1)}%`
      ];
    })
    .sort((a, b) => {
      // Sort by amount (b[2] - a[2])
      const amountA = parseFloat((a[2] as string).replace(/[^\d.-]/g, ''));
      const amountB = parseFloat((b[2] as string).replace(/[^\d.-]/g, ''));
      return amountB - amountA;
    });
  
  // Add totals row
  rows.push([
    'סך הכל',
    receipts.length,
    formatCurrency(totalAmount),
    '100%'
  ]);
  
  return [headers, ...rows];
};

/**
 * Generate filename for export
 * 
 * Format: Tik-Tax_[BusinessName]_[DateRange].[extension]
 * 
 * @param format - Export format (excel, pdf, csv)
 * @param businessName - Business name to include
 * @param startDate - Optional start date (ISO string)
 * @param endDate - Optional end date (ISO string)
 * @returns Sanitized filename
 * 
 * @example
 * ```typescript
 * generateExportFilename('excel', 'העסק שלי', '2024-01-01', '2024-01-31')
 * // => 'Tik-Tax_העסק_שלי_01-01-2024-31-01-2024.xlsx'
 * ```
 */
export const generateExportFilename = (
  format: 'excel' | 'pdf' | 'csv',
  businessName: string,
  startDate?: string,
  endDate?: string
): string => {
  const dateStr = startDate && endDate
    ? `${formatDate(startDate)}-${formatDate(endDate)}`.replace(/\//g, '-')
    : new Date().toLocaleDateString('he-IL').replace(/\//g, '-');
  
  const sanitizedName = businessName.replace(/[^a-zA-Z0-9\u0590-\u05FF]/g, '_');
  
  const extensions = {
    excel: 'xlsx',
    pdf: 'pdf',
    csv: 'csv'
  };
  
  return `Tik-Tax_${sanitizedName}_${dateStr}.${extensions[format]}`;
};

/**
 * Download blob as file
 * 
 * Creates temporary download link and triggers download.
 * Automatically cleans up URL object after download.
 * 
 * @param blob - File blob to download
 * @param filename - Filename for download
 * 
 * @example
 * ```typescript
 * const blob = generateExcelExport(receipts, 'My Business');
 * downloadBlob(blob, 'export.xlsx');
 * ```
 */
export const downloadBlob = (blob: Blob, filename: string): void => {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};

/**
 * Generate CSV export (alternative to Excel)
 * 
 * Creates comma-separated values file with:
 * - Header row
 * - All receipt data
 * - BOM prefix for Hebrew support in Excel
 * - Quoted strings for proper parsing
 * 
 * @param receipts - Receipts to export
 * @returns CSV Blob with UTF-8 BOM
 * 
 * @example
 * ```typescript
 * const blob = generateCSVExport(receipts);
 * downloadBlob(blob, 'receipts.csv');
 * ```
 */
export const generateCSVExport = (receipts: Receipt[]): Blob => {
  const headers = [
    'תאריך',
    'שם העסק',
    'מספר עסק',
    'קטגוריה',
    'סכום לפני מע"מ',
    'מע"מ',
    'סכום כולל',
    'מספר קבלה',
    'הערות'
  ].join(',');
  
  const rows = receipts
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
    .map(receipt => {
      const category = DEFAULT_CATEGORIES.find(c => c.id === receipt.categoryId);
      
      return [
        formatDate(receipt.date),
        `"${receipt.vendorName}"`,
        receipt.businessNumber,
        `"${category?.nameHe || 'אחר'}"`,
        formatCurrency(receipt.preVatAmount),
        formatCurrency(receipt.vatAmount),
        formatCurrency(receipt.totalAmount),
        receipt.receiptNumber || '',
        `"${receipt.notes || ''}"`
      ].join(',');
    }).join('\n');
  
  const csv = `${headers}\n${rows}`;
  
  // Add BOM for Hebrew support in Excel
  const BOM = '\uFEFF';
  
  return new Blob([BOM + csv], { type: 'text/csv;charset=utf-8;' });
};
