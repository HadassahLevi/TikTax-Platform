/**
 * ReceiptDetail Component
 * 
 * Detailed view for archived receipts with complete metadata, image preview,
 * edit history, and actions (download PDF, delete, share).
 * 
 * Features:
 * - Full receipt information display
 * - Original image preview with zoom modal
 * - Edit history timeline
 * - PDF download with digital signature
 * - Delete with confirmation
 * - Share via Web Share API
 * - Category badge with color coding
 * - Status indicators
 * - Responsive layout (mobile-first)
 * 
 * @module components/receipt/ReceiptDetail
 */

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ArrowLeft, Download, Trash2, Share2, Edit2, History,
  Calendar, Building2, Hash, FileText, Tag,
  Clock, User, ZoomIn, ZoomOut, CheckCircle
} from 'lucide-react';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import Modal from '@/components/ui/Modal';
import { useReceipt } from '@/hooks/useReceipt';
import { formatAmount, formatDateIL, DEFAULT_CATEGORIES } from '@/types/receipt.types';
import type { ReceiptEdit } from '@/types/receipt.types';
import * as receiptService from '@/services/receipt.service';

/**
 * ReceiptDetail component
 * 
 * @example
 * ```tsx
 * // In router
 * <Route path="/receipts/:id" element={<ReceiptDetail />} />
 * ```
 */
export const ReceiptDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { currentReceipt, setCurrentReceipt, deleteReceipt } = useReceipt();
  
  // Image modal state
  const [isImageModalOpen, setIsImageModalOpen] = useState(false);
  const [imageZoom, setImageZoom] = useState(1);
  
  // History modal state
  const [showHistory, setShowHistory] = useState(false);
  const [editHistory, setEditHistory] = useState<ReceiptEdit[]>([]);
  
  // Loading states
  const [isDownloading, setIsDownloading] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  
  /**
   * Fetch receipt data on mount
   */
  useEffect(() => {
    if (id) {
      loadReceipt(id);
    }
  }, [id]);
  
  /**
   * Load receipt and its edit history
   */
  const loadReceipt = async (receiptId: string) => {
    try {
      const receipt = await receiptService.getReceipt(receiptId);
      setCurrentReceipt(receipt);
      
      // Load edit history if available
      if (receipt.editHistory && receipt.editHistory.length > 0) {
        setEditHistory(receipt.editHistory);
      } else {
        // Try loading from API
        setIsLoadingHistory(true);
        try {
          const history = await receiptService.getReceiptHistory(receiptId);
          setEditHistory(history || []);
        } catch (error) {
          console.error('Failed to load edit history:', error);
          setEditHistory([]);
        } finally {
          setIsLoadingHistory(false);
        }
      }
    } catch (error) {
      console.error('Failed to load receipt:', error);
      alert('שגיאה בטעינת הקבלה');
      navigate('/archive');
    }
  };
  
  /**
   * Handle receipt deletion with confirmation
   */
  const handleDelete = async () => {
    if (!currentReceipt) return;
    
    const confirmed = window.confirm(
      'האם אתה בטוח שברצונך למחוק קבלה זו? פעולה זו לא ניתנת לביטול.'
    );
    
    if (confirmed) {
      try {
        await deleteReceipt(currentReceipt.id);
        navigate('/archive');
      } catch (error) {
        alert('שגיאה במחיקת הקבלה');
      }
    }
  };
  
  /**
   * Handle PDF download with digital signature
   */
  const handleDownloadPDF = async () => {
    if (!currentReceipt?.pdfUrl) {
      alert('קובץ PDF לא זמין עבור קבלה זו');
      return;
    }
    
    setIsDownloading(true);
    try {
      const blob = await receiptService.downloadReceiptPDF(currentReceipt.id);
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `קבלה-${currentReceipt.vendorName}-${formatDateIL(currentReceipt.date)}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      alert('שגיאה בהורדת הקובץ');
      console.error('PDF download error:', error);
    } finally {
      setIsDownloading(false);
    }
  };
  
  /**
   * Handle sharing via Web Share API or clipboard fallback
   */
  const handleShare = async () => {
    if (!currentReceipt) return;
    
    if (navigator.share) {
      try {
        await navigator.share({
          title: `קבלה - ${currentReceipt.vendorName}`,
          text: `קבלה מ-${currentReceipt.vendorName} בסך ${formatAmount(currentReceipt.totalAmount)}`,
          url: window.location.href
        });
      } catch (error) {
        // User cancelled or share failed
        if ((error as Error).name !== 'AbortError') {
          console.error('Share error:', error);
        }
      }
    } else {
      // Fallback: Copy link to clipboard
      try {
        await navigator.clipboard.writeText(window.location.href);
        alert('הקישור הועתק ללוח');
      } catch (error) {
        console.error('Clipboard error:', error);
        alert('לא ניתן להעתיק את הקישור');
      }
    }
  };
  
  /**
   * Loading state
   */
  if (!currentReceipt) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">טוען קבלה...</p>
        </div>
      </div>
    );
  }
  
  // Find category details
  const category = DEFAULT_CATEGORIES.find(c => c.id === currentReceipt.categoryId);
  
  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {/* Header */}
      <div className="bg-white border-b sticky top-0 z-10 shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate('/archive')}
              icon={<ArrowLeft size={20} />}
            >
              חזור לארכיון
            </Button>
            
            <div className="flex gap-2">
              <button
                onClick={handleShare}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                aria-label="שתף קבלה"
              >
                <Share2 size={18} />
              </button>
              <button
                onClick={handleDelete}
                className="p-2 text-red-600 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors"
                aria-label="מחק קבלה"
              >
                <Trash2 size={18} />
              </button>
            </div>
          </div>
        </div>
      </div>
      
      {/* Main content */}
      <div className="max-w-4xl mx-auto px-4 py-6 space-y-6">
        
        {/* Receipt Image */}
        <Card shadow="md" padding="none">
          <div 
            className="relative cursor-pointer group overflow-hidden rounded-lg"
            onClick={() => setIsImageModalOpen(true)}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => e.key === 'Enter' && setIsImageModalOpen(true)}
            aria-label="הצג תמונה מוגדלת"
          >
            <img
              src={currentReceipt.imageUrl}
              alt="תמונת קבלה"
              className="w-full h-auto rounded-lg"
            />
            <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all rounded-lg flex items-center justify-center">
              <ZoomIn 
                size={48} 
                className="text-white opacity-0 group-hover:opacity-100 transition-opacity drop-shadow-lg" 
              />
            </div>
          </div>
        </Card>
        
        {/* Receipt Info */}
        <Card shadow="md" padding="lg">
          {/* Header with vendor name and category */}
          <div className="flex items-start justify-between mb-6 flex-wrap gap-4">
            <div>
              <h1 className="text-2xl font-600 text-gray-900 mb-2">
                {currentReceipt.vendorName}
              </h1>
              <p className="text-gray-600 flex items-center gap-2">
                <Calendar size={16} />
                {formatDateIL(currentReceipt.date)}
              </p>
            </div>
            
            {category && (
              <div 
                className="px-4 py-2 rounded-lg flex items-center gap-2"
                style={{ 
                  backgroundColor: `${category.color}20`, 
                  color: category.color 
                }}
              >
                <Tag size={18} />
                <span className="font-500">{category.nameHe}</span>
              </div>
            )}
          </div>
          
          {/* Amount breakdown with gradient */}
          <div className="bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl p-6 text-white mb-6">
            <p className="text-sm opacity-90 mb-1">סכום כולל</p>
            <p className="text-4xl font-700 mb-4">
              {formatAmount(currentReceipt.totalAmount)}
            </p>
            <div className="flex justify-between text-sm">
              <div>
                <p className="opacity-75">לפני מע"מ</p>
                <p className="font-600">{formatAmount(currentReceipt.preVatAmount)}</p>
              </div>
              <div>
                <p className="opacity-75">מע"מ (18%)</p>
                <p className="font-600">{formatAmount(currentReceipt.vatAmount)}</p>
              </div>
            </div>
          </div>
          
          {/* Details grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-start gap-3">
              <div className="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center flex-shrink-0">
                <Building2 size={20} className="text-gray-600" />
              </div>
              <div className="min-w-0 flex-1">
                <p className="text-sm text-gray-600">עסק</p>
                <p className="font-500 text-gray-900 truncate">{currentReceipt.vendorName}</p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <div className="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center flex-shrink-0">
                <Hash size={20} className="text-gray-600" />
              </div>
              <div className="min-w-0 flex-1">
                <p className="text-sm text-gray-600">מספר עסק</p>
                <p className="font-500 text-gray-900 font-mono">{currentReceipt.businessNumber}</p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <div className="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center flex-shrink-0">
                <FileText size={20} className="text-gray-600" />
              </div>
              <div className="min-w-0 flex-1">
                <p className="text-sm text-gray-600">מספר קבלה</p>
                <p className="font-500 text-gray-900 font-mono">
                  {currentReceipt.receiptNumber || 'לא זמין'}
                </p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <div className="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center flex-shrink-0">
                <Clock size={20} className="text-gray-600" />
              </div>
              <div className="min-w-0 flex-1">
                <p className="text-sm text-gray-600">הועלה ב</p>
                <p className="font-500 text-gray-900">
                  {new Date(currentReceipt.createdAt).toLocaleDateString('he-IL', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </p>
              </div>
            </div>
          </div>
          
          {/* Notes */}
          {currentReceipt.notes && (
            <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-100">
              <p className="text-sm font-600 text-blue-900 mb-1">הערות</p>
              <p className="text-sm text-blue-800">{currentReceipt.notes}</p>
            </div>
          )}
        </Card>
        
        {/* Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <Button
            variant="secondary"
            fullWidth
            onClick={handleDownloadPDF}
            icon={<Download size={20} />}
            loading={isDownloading}
            disabled={!currentReceipt.pdfUrl || isDownloading}
          >
            {isDownloading ? 'מוריד...' : 'הורד PDF חתום'}
          </Button>
          
          <Button
            variant="secondary"
            fullWidth
            onClick={() => navigate(`/receipts/${currentReceipt.id}/edit`)}
            icon={<Edit2 size={20} />}
          >
            ערוך פרטים
          </Button>
          
          <Button
            variant="secondary"
            fullWidth
            onClick={() => setShowHistory(true)}
            icon={<History size={20} />}
            disabled={editHistory.length === 0 && !isLoadingHistory}
          >
            {isLoadingHistory ? 'טוען...' : 'היסטוריית שינויים'}
          </Button>
        </div>
        
        {/* Digital signature info */}
        {currentReceipt.digitalSignature && currentReceipt.signedAt && (
          <Card shadow="sm" padding="md">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0">
                <CheckCircle size={24} className="text-green-600" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-600 text-gray-900">חתימה דיגיטלית</p>
                <p className="text-sm text-gray-600">
                  נחתם ב-{new Date(currentReceipt.signedAt).toLocaleDateString('he-IL', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </p>
              </div>
              <div className="text-green-600 text-sm font-600 flex items-center gap-1">
                <CheckCircle size={16} />
                מאומת
              </div>
            </div>
          </Card>
        )}
      </div>
      
      {/* Image zoom modal */}
      <Modal
        isOpen={isImageModalOpen}
        onClose={() => {
          setIsImageModalOpen(false);
          setImageZoom(1);
        }}
        size="full"
        showCloseButton={true}
      >
        <div className="relative h-full flex items-center justify-center bg-black">
          <img
            src={currentReceipt.imageUrl}
            alt="תמונת קבלה מוגדלת"
            style={{ 
              transform: `scale(${imageZoom})`,
              transition: 'transform 0.2s ease'
            }}
            className="max-w-full max-h-full object-contain"
          />
          
          {/* Zoom controls */}
          <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex gap-3 bg-white rounded-full px-4 py-2 shadow-lg">
            <button
              onClick={() => setImageZoom(Math.max(1, imageZoom - 0.25))}
              className="p-2 hover:bg-gray-100 rounded-full transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={imageZoom <= 1}
              aria-label="הקטן"
            >
              <ZoomOut size={24} />
            </button>
            <span className="px-4 py-2 text-sm font-600 min-w-[60px] text-center">
              {Math.round(imageZoom * 100)}%
            </span>
            <button
              onClick={() => setImageZoom(Math.min(3, imageZoom + 0.25))}
              className="p-2 hover:bg-gray-100 rounded-full transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={imageZoom >= 3}
              aria-label="הגדל"
            >
              <ZoomIn size={24} />
            </button>
          </div>
        </div>
      </Modal>
      
      {/* Edit history modal */}
      <Modal
        isOpen={showHistory}
        onClose={() => setShowHistory(false)}
        title="היסטוריית שינויים"
        size="md"
      >
        <div className="space-y-4">
          {isLoadingHistory ? (
            <div className="text-center py-8">
              <div className="w-8 h-8 border-4 border-primary-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
              <p className="text-gray-600">טוען היסטוריה...</p>
            </div>
          ) : editHistory.length === 0 ? (
            <div className="text-center py-8">
              <History size={48} className="text-gray-300 mx-auto mb-4" />
              <p className="text-gray-600">אין שינויים קודמים</p>
            </div>
          ) : (
            editHistory.map((edit, index) => (
              <div key={edit.id} className="flex gap-3">
                <div className="flex flex-col items-center">
                  <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center flex-shrink-0">
                    <User size={16} className="text-primary-600" />
                  </div>
                  {index < editHistory.length - 1 && (
                    <div className="w-0.5 flex-1 bg-gray-200 my-1" />
                  )}
                </div>
                
                <div className="flex-1 pb-4">
                  <p className="text-sm font-600 text-gray-900 mb-1">
                    {getFieldNameHe(edit.fieldChanged)} עודכן
                  </p>
                  <p className="text-sm text-gray-600 mb-2">
                    <span className="line-through">{String(edit.oldValue)}</span>
                    {' → '}
                    <span className="font-500">{String(edit.newValue)}</span>
                  </p>
                  <p className="text-xs text-gray-500">
                    {new Date(edit.changedAt).toLocaleString('he-IL', {
                      day: '2-digit',
                      month: '2-digit',
                      year: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </p>
                </div>
              </div>
            ))
          )}
        </div>
      </Modal>
    </div>
  );
};

/**
 * Helper function to get Hebrew field names
 */
const getFieldNameHe = (fieldName: string): string => {
  const fieldNameMap: Record<string, string> = {
    vendorName: 'שם העסק',
    businessNumber: 'מספר עסק',
    date: 'תאריך',
    totalAmount: 'סכום כולל',
    vatAmount: 'מע"מ',
    preVatAmount: 'סכום לפני מע"מ',
    receiptNumber: 'מספר קבלה',
    categoryId: 'קטגוריה',
    notes: 'הערות'
  };
  
  return fieldNameMap[fieldName] || fieldName;
};

export default ReceiptDetail;
