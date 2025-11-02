import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ReceiptUpload } from '@/components/receipt';
import { useToast } from '@/hooks/useToast';

/**
 * Receipt Upload Page
 * 
 * Full-screen page for uploading new receipts via camera or gallery.
 * Redirects to review page after successful upload.
 * 
 * Route: /receipts/upload
 * 
 * @page
 * @example
 * ```tsx
 * // In router
 * <Route path="/receipts/upload" element={<UploadPage />} />
 * ```
 */
export const UploadPage: React.FC = () => {
  const navigate = useNavigate();
  const { showSuccess } = useToast();
  
  /**
   * Handle successful upload
   * Navigate to review page with receipt ID
   */
  const handleUploadSuccess = (receiptId: string) => {
    showSuccess('הקבלה הועלתה בהצלחה! מעבר לעמוד הסקירה...');
    
    // Navigate to review page
    navigate(`/receipts/${receiptId}/review`, {
      replace: true // Don't allow back to upload page
    });
  };
  
  /**
   * Handle cancel
   * Return to previous page (usually dashboard)
   */
  const handleCancel = () => {
    navigate(-1); // Go back
  };
  
  return (
    <div className="h-screen bg-gray-50">
      <ReceiptUpload
        onUploadSuccess={handleUploadSuccess}
        onCancel={handleCancel}
      />
    </div>
  );
};

export default UploadPage;
