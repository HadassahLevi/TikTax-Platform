import React, { useState, useRef, useCallback, useEffect } from 'react';
import { Camera, Upload, X, RefreshCw } from 'lucide-react';
import Button from '@/components/ui/Button';
import { useReceipt } from '@/hooks/useReceipt';
import { MAX_FILE_SIZE, ALLOWED_FILE_TYPES } from '@/types/receipt.types';

/**
 * ReceiptUpload Component Props
 * 
 * @interface ReceiptUploadProps
 */
export interface ReceiptUploadProps {
  /** Callback when upload succeeds, receives receipt ID */
  onUploadSuccess: (receiptId: string) => void;
  
  /** Optional cancel callback */
  onCancel?: () => void;
}

/**
 * Receipt Upload Component
 * 
 * Full-featured receipt upload component with:
 * - Camera interface for real-time capture
 * - Gallery upload for existing photos
 * - File validation (type, size, dimensions)
 * - Preview before processing
 * - Drag-and-drop support
 * - Mobile-optimized touch interface
 * 
 * @component
 * @example
 * ```tsx
 * <ReceiptUpload
 *   onUploadSuccess={(id) => navigate(`/receipts/${id}`)}
 *   onCancel={() => navigate('/dashboard')}
 * />
 * ```
 */
export const ReceiptUpload: React.FC<ReceiptUploadProps> = ({
  onUploadSuccess,
  onCancel
}) => {
  const { uploadReceipt, isUploading, uploadError, clearError } = useReceipt();
  
  // Component state
  const [captureMode, setCaptureMode] = useState<'camera' | 'gallery' | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  
  // Refs for camera functionality
  const fileInputRef = useRef<HTMLInputElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  
  // ============================================================================
  // FILE VALIDATION
  // ============================================================================
  
  /**
   * Validate file type and size
   * @param file - File to validate
   * @returns Error message or null if valid
   */
  const validateFile = (file: File): string | null => {
    if (!ALLOWED_FILE_TYPES.includes(file.type)) {
      return 'סוג קובץ לא נתמך. השתמש ב-JPG, PNG או PDF';
    }
    if (file.size > MAX_FILE_SIZE) {
      return `הקובץ גדול מדי (מקסימום ${MAX_FILE_SIZE / 1024 / 1024}MB)`;
    }
    return null;
  };
  
  // ============================================================================
  // FILE SELECTION & PREVIEW
  // ============================================================================
  
  /**
   * Handle file selection from any source (gallery, camera, drag-drop)
   * @param file - Selected file
   */
  const handleFileSelect = useCallback((file: File) => {
    clearError();
    
    const error = validateFile(file);
    if (error) {
      alert(error);
      return;
    }
    
    setSelectedFile(file);
    
    // Create preview URL
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreviewUrl(e.target?.result as string);
    };
    reader.readAsDataURL(file);
  }, [clearError]);
  
  // ============================================================================
  // CAMERA FUNCTIONALITY
  // ============================================================================
  
  /**
   * Start camera stream
   * Requests back camera on mobile devices
   */
  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { 
          facingMode: 'environment', // Use back camera on mobile
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        }
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        videoRef.current.play();
      }
      
      setStream(mediaStream);
      setCaptureMode('camera');
    } catch (error) {
      alert('לא ניתן לגשת למצלמה. בדוק הרשאות.');
      console.error('Camera error:', error);
    }
  };
  
  /**
   * Stop camera stream and release resources
   */
  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    setCaptureMode(null);
  };
  
  /**
   * Capture photo from video stream to canvas
   * Converts to JPEG file with 95% quality
   */
  const capturePhoto = () => {
    if (!videoRef.current || !canvasRef.current) return;
    
    const video = videoRef.current;
    const canvas = canvasRef.current;
    
    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw current video frame to canvas
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    ctx.drawImage(video, 0, 0);
    
    // Convert canvas to blob and create File
    canvas.toBlob((blob) => {
      if (!blob) return;
      
      const file = new File([blob], `receipt-${Date.now()}.jpg`, {
        type: 'image/jpeg'
      });
      
      handleFileSelect(file);
      stopCamera();
    }, 'image/jpeg', 0.95);
  };
  
  // ============================================================================
  // GALLERY UPLOAD
  // ============================================================================
  
  /**
   * Trigger hidden file input click
   */
  const handleGalleryClick = () => {
    fileInputRef.current?.click();
  };
  
  /**
   * Handle file input change event
   */
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file);
      setCaptureMode('gallery');
    }
  };
  
  // ============================================================================
  // DRAG & DROP
  // ============================================================================
  
  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };
  
  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };
  
  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };
  
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileSelect(file);
      setCaptureMode('gallery');
    }
  };
  
  // ============================================================================
  // UPLOAD & RESET
  // ============================================================================
  
  /**
   * Upload selected file to server
   */
  const handleUpload = async () => {
    if (!selectedFile) return;
    
    try {
      const receiptId = await uploadReceipt(selectedFile);
      onUploadSuccess(receiptId);
    } catch (error) {
      // Error handled by store and displayed in UI
      console.error('Upload error:', error);
    }
  };
  
  /**
   * Reset component to initial state
   */
  const handleReset = () => {
    setPreviewUrl(null);
    setSelectedFile(null);
    setCaptureMode(null);
    stopCamera();
    clearError();
  };
  
  // ============================================================================
  // LIFECYCLE & CLEANUP
  // ============================================================================
  
  /**
   * Cleanup on unmount - stop camera and revoke preview URLs
   */
  useEffect(() => {
    return () => {
      stopCamera();
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, []);
  
  // ============================================================================
  // RENDER: CAMERA VIEW
  // ============================================================================
  
  if (captureMode === 'camera' && !selectedFile) {
    return (
      <div className="fixed inset-0 z-50 bg-black">
        {/* Video stream */}
        <video
          ref={videoRef}
          className="w-full h-full object-cover"
          playsInline
          autoPlay
          muted
        />
        
        {/* Hidden canvas for photo capture */}
        <canvas ref={canvasRef} className="hidden" />
        
        {/* Camera controls overlay */}
        <div className="absolute bottom-8 left-0 right-0 flex justify-center items-center gap-6 px-4">
          {/* Cancel button */}
          <Button
            variant="secondary"
            size="lg"
            onClick={stopCamera}
            icon={<X size={24} />}
          >
            ביטול
          </Button>
          
          {/* Capture button - large circle */}
          <button
            onClick={capturePhoto}
            className="w-20 h-20 rounded-full bg-white border-4 border-primary-600 hover:border-primary-700 active:scale-95 transition-all shadow-lg"
            aria-label="צלם קבלה"
          />
          
          {/* Switch camera button (placeholder for future feature) */}
          <Button
            variant="ghost"
            size="lg"
            onClick={() => {
              // Future: Switch between front/back camera
              console.log('Switch camera - future feature');
            }}
            icon={<RefreshCw size={24} />}
            className="text-white hover:bg-white/10"
          >
            החלף
          </Button>
        </div>
        
        {/* Overlay guide (optional) */}
        <div className="absolute inset-0 pointer-events-none flex items-center justify-center">
          <div className="w-[90%] max-w-md aspect-[3/4] border-2 border-white/30 rounded-lg" />
        </div>
      </div>
    );
  }
  
  // ============================================================================
  // RENDER: PREVIEW & UPLOAD
  // ============================================================================
  
  if (previewUrl && selectedFile) {
    return (
      <div className="flex flex-col h-full min-h-screen bg-gray-50">
        {/* Preview section */}
        <div className="flex-1 bg-gray-100 p-4 overflow-auto">
          <img
            src={previewUrl}
            alt="Receipt preview"
            className="max-w-full h-auto mx-auto rounded-lg shadow-md"
          />
        </div>
        
        {/* Actions section */}
        <div className="p-6 bg-white border-t space-y-4 shadow-lg">
          {/* Error display */}
          {uploadError && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              {uploadError}
            </div>
          )}
          
          {/* Primary actions */}
          <div className="flex gap-3">
            <Button
              variant="secondary"
              fullWidth
              onClick={handleReset}
              disabled={isUploading}
            >
              צלם מחדש
            </Button>
            
            <Button
              variant="primary"
              fullWidth
              onClick={handleUpload}
              loading={isUploading}
              disabled={isUploading}
            >
              {isUploading ? 'מעלה...' : 'המשך לעיבוד'}
            </Button>
          </div>
          
          {/* Cancel button */}
          {onCancel && (
            <Button
              variant="ghost"
              fullWidth
              onClick={onCancel}
              disabled={isUploading}
            >
              ביטול
            </Button>
          )}
        </div>
      </div>
    );
  }
  
  // ============================================================================
  // RENDER: UPLOAD OPTIONS
  // ============================================================================
  
  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] p-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-2">
          העלה קבלה חדשה
        </h2>
        <p className="text-gray-600">
          צלם קבלה חדשה או העלה מהגלריה
        </p>
      </div>
      
      {/* Drag & Drop Zone */}
      <div
        className={`
          w-full max-w-md p-8 border-2 border-dashed rounded-xl
          transition-all cursor-pointer
          ${isDragging 
            ? 'border-primary-600 bg-primary-50 scale-105' 
            : 'border-gray-300 bg-gray-50 hover:bg-gray-100 hover:border-gray-400'
          }
        `}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={handleGalleryClick}
      >
        <Upload 
          size={48} 
          className={`mx-auto mb-4 transition-colors ${
            isDragging ? 'text-primary-600' : 'text-gray-400'
          }`} 
        />
        <p className="text-center text-gray-600 mb-2 font-medium">
          גרור קובץ לכאן או לחץ להעלאה
        </p>
        <p className="text-center text-sm text-gray-500">
          JPG, PNG או PDF (עד 10MB)
        </p>
      </div>
      
      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*,application/pdf"
        onChange={handleFileChange}
        className="hidden"
      />
      
      {/* OR divider */}
      <div className="flex items-center gap-4 w-full max-w-md my-6">
        <div className="flex-1 h-px bg-gray-300" />
        <span className="text-gray-500 text-sm font-medium">או</span>
        <div className="flex-1 h-px bg-gray-300" />
      </div>
      
      {/* Camera button */}
      <Button
        variant="primary"
        size="lg"
        onClick={startCamera}
        icon={<Camera size={24} />}
        className="w-full max-w-md"
      >
        פתח מצלמה
      </Button>
      
      {/* Cancel button */}
      {onCancel && (
        <Button
          variant="ghost"
          onClick={onCancel}
          className="mt-4"
        >
          ביטול
        </Button>
      )}
    </div>
  );
};

export default ReceiptUpload;
