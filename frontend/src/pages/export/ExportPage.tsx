/**
 * Export Page Component
 * 
 * Comprehensive export interface for generating Excel/PDF/CSV reports.
 * Designed for accountant-ready exports with flexible filtering and formatting.
 * 
 * Features:
 * - Format selection (Excel/PDF/CSV)
 * - Date range picker with presets
 * - Category filtering (multi-select)
 * - Include images toggle
 * - Real-time preview of filtered receipts
 * - Export progress indicator
 * - Summary card with totals
 * 
 * @module pages/export/ExportPage
 */

import React, { useState } from 'react';
import { Download, Calendar, FileText, Image } from 'lucide-react';
import { PageContainer } from '@/components/layout/PageContainer';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import Input from '@/components/ui/Input';
import { useReceipt } from '@/hooks/useReceipt';
import { useAuth } from '@/hooks/useAuth';
import { formatAmount, formatDateIL, DEFAULT_CATEGORIES } from '@/types/receipt.types';
import { 
  generateExcelExport, 
  generateCSVExport, 
  generateExportFilename, 
  downloadBlob 
} from '@/services/export.service';
import { generatePDFExport } from '@/services/pdf-export.service';

// ============================================================================
// TYPES
// ============================================================================

type ExportFormat = 'excel' | 'pdf' | 'csv';
type DatePreset = 'this_month' | 'last_month' | 'this_year' | 'last_year' | 'custom';

interface FormatOption {
  format: ExportFormat;
  label: string;
  icon: string;
  desc: string;
}

interface DatePresetOption {
  preset: DatePreset;
  label: string;
}

// ============================================================================
// CONSTANTS
// ============================================================================

const FORMAT_OPTIONS: FormatOption[] = [
  { format: 'excel', label: 'Excel', icon: '📊', desc: 'מומלץ לרו"ח' },
  { format: 'pdf', label: 'PDF', icon: '📄', desc: 'דוח מעוצב' },
  { format: 'csv', label: 'CSV', icon: '📝', desc: 'נתונים גולמיים' }
];

const DATE_PRESETS: DatePresetOption[] = [
  { preset: 'this_month', label: 'החודש' },
  { preset: 'last_month', label: 'חודש שעבר' },
  { preset: 'this_year', label: 'השנה' },
  { preset: 'custom', label: 'מותאם אישית' }
];

// ============================================================================
// COMPONENT
// ============================================================================

export const ExportPage: React.FC = () => {
  const { receipts } = useReceipt();
  const { user } = useAuth();
  
  // Export settings state
  const [selectedFormat, setSelectedFormat] = useState<ExportFormat>('excel');
  const [datePreset, setDatePreset] = useState<DatePreset>('this_month');
  const [customStartDate, setCustomStartDate] = useState('');
  const [customEndDate, setCustomEndDate] = useState('');
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [includeImages, setIncludeImages] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [exportProgress, setExportProgress] = useState(0);
  
  // ============================================================================
  // DATE RANGE CALCULATION
  // ============================================================================
  
  /**
   * Calculate date range based on selected preset
   */
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
      default:
        startDate = new Date(now.getFullYear(), now.getMonth(), 1);
    }
    
    return {
      startDate: startDate.toISOString().split('T')[0],
      endDate: endDate.toISOString().split('T')[0]
    };
  };
  
  // ============================================================================
  // FILTERING LOGIC
  // ============================================================================
  
  const { startDate, endDate } = getDateRange();
  
  /**
   * Filter receipts based on selected criteria
   */
  const filteredReceipts = receipts.filter(receipt => {
    const receiptDate = new Date(receipt.date);
    const start = new Date(startDate);
    const end = new Date(endDate);
    
    const dateMatch = receiptDate >= start && receiptDate <= end;
    const categoryMatch = selectedCategories.length === 0 || 
                          selectedCategories.includes(receipt.categoryId);
    
    return dateMatch && categoryMatch;
  });
  
  // Calculate totals
  const totalAmount = filteredReceipts.reduce((sum, r) => sum + r.totalAmount, 0);
  const totalVat = filteredReceipts.reduce((sum, r) => sum + r.vatAmount, 0);
  
  // ============================================================================
  // CATEGORY TOGGLE HANDLER
  // ============================================================================
  
  const toggleCategory = (categoryId: string) => {
    setSelectedCategories(prev =>
      prev.includes(categoryId)
        ? prev.filter(id => id !== categoryId)
        : [...prev, categoryId]
    );
  };
  
  // ============================================================================
  // EXPORT HANDLER
  // ============================================================================
  
  const handleExport = async () => {
    setIsExporting(true);
    setExportProgress(0);
    
    try {
      // Simulate progress
      setExportProgress(20);
      
      let blob: Blob;
      let filename: string;
      const businessName = user?.businessName || 'עסק';
      
      // Generate export based on format
      switch (selectedFormat) {
        case 'excel':
          blob = generateExcelExport(filteredReceipts, businessName);
          filename = generateExportFilename('excel', businessName, startDate, endDate);
          setExportProgress(80);
          break;
          
        case 'csv':
          blob = generateCSVExport(filteredReceipts);
          filename = generateExportFilename('csv', businessName, startDate, endDate);
          setExportProgress(80);
          break;
          
        case 'pdf':
          setExportProgress(40);
          blob = await generatePDFExport(
            filteredReceipts, 
            businessName,
            includeImages
          );
          filename = generateExportFilename('pdf', businessName, startDate, endDate);
          setExportProgress(80);
          break;
          
        default:
          throw new Error('Invalid export format');
      }
      
      setExportProgress(90);
      
      // Download file
      downloadBlob(blob, filename);
      
      setExportProgress(100);
      
      // Reset state after 1 second
      setTimeout(() => {
        setIsExporting(false);
        setExportProgress(0);
      }, 1000);
      
    } catch (error) {
      console.error('Export failed:', error);
      setIsExporting(false);
      setExportProgress(0);
      alert('שגיאה בייצוא הנתונים. נסה שוב.');
    }
  };
  
  // ============================================================================
  // RENDER
  // ============================================================================
  
  return (
    <PageContainer
      title="ייצוא נתונים"
      subtitle="הורד דוח מסודר לרואה חשבון"
    >
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* ===================================================================== */}
        {/* LEFT COLUMN: EXPORT SETTINGS */}
        {/* ===================================================================== */}
        
        <div className="lg:col-span-2 space-y-6">
          
          {/* Format Selection */}
          <Card shadow="md" padding="lg">
            <h2 className="text-lg font-600 text-gray-900 mb-4 flex items-center gap-2">
              <FileText size={20} />
              בחר פורמט ייצוא
            </h2>
            
            <div className="grid grid-cols-3 gap-3">
              {FORMAT_OPTIONS.map(({ format, label, icon, desc }) => (
                <button
                  key={format}
                  onClick={() => setSelectedFormat(format)}
                  className={`
                    p-4 rounded-xl border-2 transition-all
                    ${selectedFormat === format
                      ? 'border-primary-600 bg-primary-50 shadow-md'
                      : 'border-gray-200 hover:border-gray-300'
                    }
                  `}
                >
                  <div className="text-3xl mb-2">{icon}</div>
                  <p className="font-600 text-gray-900">{label}</p>
                  <p className="text-xs text-gray-600 mt-1">{desc}</p>
                </button>
              ))}
            </div>
          </Card>
          
          {/* Date Range Selection */}
          <Card shadow="md" padding="lg">
            <h2 className="text-lg font-600 text-gray-900 mb-4 flex items-center gap-2">
              <Calendar size={20} />
              טווח תאריכים
            </h2>
            
            {/* Date Presets */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mb-4">
              {DATE_PRESETS.map(({ preset, label }) => (
                <button
                  key={preset}
                  onClick={() => setDatePreset(preset)}
                  className={`
                    px-4 py-2 rounded-lg font-500 transition-all
                    ${datePreset === preset
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }
                  `}
                >
                  {label}
                </button>
              ))}
            </div>
            
            {/* Custom Date Inputs */}
            {datePreset === 'custom' && (
              <div className="grid grid-cols-2 gap-3">
                <Input
                  type="date"
                  label="מתאריך"
                  value={customStartDate}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setCustomStartDate(e.target.value)}
                />
                <Input
                  type="date"
                  label="עד תאריך"
                  value={customEndDate}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setCustomEndDate(e.target.value)}
                />
              </div>
            )}
            
            {/* Selected Range Display */}
            <div className="mt-4 p-3 bg-blue-50 rounded-lg text-sm text-blue-800">
              <strong>טווח נבחר:</strong> {formatDateIL(startDate)} - {formatDateIL(endDate)}
            </div>
          </Card>
          
          {/* Category Filter */}
          <Card shadow="md" padding="lg">
            <h2 className="text-lg font-600 text-gray-900 mb-4">
              סינון לפי קטגוריות (אופציונלי)
            </h2>
            
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
              {DEFAULT_CATEGORIES.map(category => {
                const isSelected = selectedCategories.includes(category.id);
                return (
                  <button
                    key={category.id}
                    onClick={() => toggleCategory(category.id)}
                    className={`
                      p-3 rounded-lg border-2 transition-all text-right
                      ${isSelected
                        ? 'border-primary-600 bg-primary-50'
                        : 'border-gray-200 hover:border-gray-300'
                      }
                    `}
                  >
                    <div className="flex items-center gap-2">
                      <div 
                        className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                        style={{ backgroundColor: `${category.color}20` }}
                      >
                        <span className="text-lg">{category.icon}</span>
                      </div>
                      <span className="text-sm font-500 truncate">{category.nameHe}</span>
                    </div>
                  </button>
                );
              })}
            </div>
            
            {/* Clear Selection */}
            {selectedCategories.length > 0 && (
              <button
                onClick={() => setSelectedCategories([])}
                className="mt-3 text-sm text-primary-600 hover:text-primary-700 underline"
              >
                נקה בחירה ({selectedCategories.length} נבחרו)
              </button>
            )}
          </Card>
          
          {/* Additional Options */}
          <Card shadow="md" padding="lg">
            <h2 className="text-lg font-600 text-gray-900 mb-4">
              אפשרויות נוספות
            </h2>
            
            <label className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors">
              <input
                type="checkbox"
                checked={includeImages}
                onChange={(e) => setIncludeImages(e.target.checked)}
                className="w-5 h-5 text-primary-600 rounded focus:ring-2 focus:ring-primary-500"
              />
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <Image size={18} className="text-gray-600" />
                  <span className="font-500 text-gray-900">כלול תמונות קבלות</span>
                </div>
                <p className="text-sm text-gray-600 mt-1">
                  {selectedFormat === 'pdf' 
                    ? 'תמונות ישולבו בקובץ PDF' 
                    : 'יצוצר קובץ ZIP עם התמונות (גודל גדול יותר)'
                  }
                </p>
              </div>
            </label>
          </Card>
        </div>
        
        {/* ===================================================================== */}
        {/* RIGHT COLUMN: PREVIEW & SUMMARY */}
        {/* ===================================================================== */}
        
        <div className="space-y-6">
          
          {/* Summary Card (Sticky) */}
          <Card shadow="md" padding="lg" className="sticky top-24">
            <h2 className="text-lg font-600 text-gray-900 mb-4">
              סיכום
            </h2>
            
            {/* Metrics */}
            <div className="space-y-4 mb-6">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">קבלות לייצוא:</span>
                <span className="text-2xl font-700 text-gray-900">
                  {filteredReceipts.length}
                </span>
              </div>
              
              <div className="pt-4 border-t border-gray-200">
                <div className="flex justify-between mb-2">
                  <span className="text-gray-600">סכום כולל:</span>
                  <span className="font-600 text-gray-900">
                    {formatAmount(totalAmount)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">מע"מ:</span>
                  <span className="font-600 text-gray-900">
                    {formatAmount(totalVat)}
                  </span>
                </div>
              </div>
              
              <div className="pt-4 border-t border-gray-200 text-sm text-gray-600">
                <div className="flex items-start gap-2">
                  <FileText size={16} className="mt-0.5 flex-shrink-0" />
                  <span>
                    פורמט: <strong className="text-gray-900">{selectedFormat.toUpperCase()}</strong>
                  </span>
                </div>
                {selectedCategories.length > 0 && (
                  <div className="flex items-start gap-2 mt-2">
                    <span>קטגוריות: {selectedCategories.length}</span>
                  </div>
                )}
              </div>
            </div>
            
            {/* Export Button */}
            <Button
              variant="primary"
              fullWidth
              size="lg"
              onClick={handleExport}
              loading={isExporting}
              disabled={isExporting || filteredReceipts.length === 0}
              icon={<Download size={20} />}
            >
              {isExporting ? `מייצא... ${exportProgress}%` : 'הורד דוח'}
            </Button>
            
            {/* Progress Bar */}
            {isExporting && (
              <div className="mt-3">
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-primary-600 transition-all duration-300"
                    style={{ width: `${exportProgress}%` }}
                  />
                </div>
              </div>
            )}
            
            {/* No Receipts Warning */}
            {filteredReceipts.length === 0 && (
              <p className="mt-3 text-sm text-red-600 text-center">
                לא נמצאו קבלות בטווח התאריכים שנבחר
              </p>
            )}
          </Card>
          
          {/* Tips Card */}
          <Card shadow="sm" padding="md" className="bg-blue-50 border border-blue-200">
            <h3 className="font-600 text-blue-900 mb-2 flex items-center gap-2">
              💡 טיפים לייצוא
            </h3>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• קובץ Excel מומלץ לרוב רואי החשבון</li>
              <li>• PDF מתאים להדפסה ולשמירה</li>
              <li>• CSV לעיבוד במערכות אחרות</li>
              <li>• הקובץ יישמר 7 ימים בהיסטוריה</li>
            </ul>
          </Card>
        </div>
      </div>
    </PageContainer>
  );
};

export default ExportPage;
