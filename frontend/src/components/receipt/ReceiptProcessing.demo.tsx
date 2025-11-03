/**
 * ReceiptProcessing Component - Usage Demo
 * 
 * Demonstrates all features and use cases of the ReceiptProcessing component.
 * Copy and adapt these examples for your implementation.
 */

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ReceiptProcessing } from '@/components/receipt';
import { useToast } from '@/hooks/useToast';

// ============================================================================
// EXAMPLE 1: Basic Usage
// ============================================================================

export function BasicProcessingExample() {
  const navigate = useNavigate();
  const receiptId = 'receipt-abc123';
  
  return (
    <ReceiptProcessing
      receiptId={receiptId}
      onComplete={() => {
        navigate(`/receipts/${receiptId}/review`);
      }}
      onError={(error) => {
        console.error('Processing failed:', error);
        navigate('/upload');
      }}
      onTimeout={() => {
        console.warn('Processing timeout');
      }}
    />
  );
}

// ============================================================================
// EXAMPLE 2: Complete Upload → Processing → Review Flow
// ============================================================================

export function CompleteFlowExample() {
  const navigate = useNavigate();
  const { toast } = useToast();
  
  const [stage, setStage] = useState<'upload' | 'processing' | 'review'>('upload');
  const [receiptId, setReceiptId] = useState<string | null>(null);
  
  const handleUpload = async (file: File) => {
    try {
      // Upload file to backend
      const response = await fetch('/api/receipts/upload', {
        method: 'POST',
        body: file
      });
      
      const data = await response.json();
      setReceiptId(data.receiptId);
      setStage('processing');
    } catch (error) {
      toast.error('העלאה נכשלה');
    }
  };
  
  const handleComplete = () => {
    toast.success('עיבוד הושלם בהצלחה!');
    setStage('review');
    navigate(`/receipts/${receiptId}/review`);
  };
  
  const handleError = (error: string) => {
    toast.error(error);
    setStage('upload');
    setReceiptId(null);
  };
  
  const handleTimeout = () => {
    toast.warning('העיבוד לוקח זמן רב - אנא המתן או נסה שוב');
  };
  
  return (
    <div>
      {stage === 'upload' && (
        <div>
          <h1>Upload Receipt</h1>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) handleUpload(file);
            }}
          />
        </div>
      )}
      
      {stage === 'processing' && receiptId && (
        <ReceiptProcessing
          receiptId={receiptId}
          onComplete={handleComplete}
          onError={handleError}
          onTimeout={handleTimeout}
        />
      )}
      
      {stage === 'review' && (
        <div>
          <h1>Review Receipt</h1>
          {/* ReceiptReview component */}
        </div>
      )}
    </div>
  );
}

// ============================================================================
// EXAMPLE 3: With Analytics Tracking
// ============================================================================

export function AnalyticsExample() {
  const navigate = useNavigate();
  const receiptId = 'receipt-xyz789';
  const [startTime] = useState(Date.now());
  
  const logEvent = (eventName: string, data: Record<string, any>) => {
    console.log(`[Analytics] ${eventName}`, data);
    // Replace with your analytics service (GA4, Mixpanel, etc.)
  };
  
  return (
    <ReceiptProcessing
      receiptId={receiptId}
      onComplete={() => {
        const duration = Date.now() - startTime;
        
        logEvent('processing_completed', {
          receiptId,
          duration,
          timestamp: new Date().toISOString()
        });
        
        navigate(`/receipts/${receiptId}/review`);
      }}
      onError={(error) => {
        logEvent('processing_failed', {
          receiptId,
          error,
          duration: Date.now() - startTime
        });
        
        navigate('/upload');
      }}
      onTimeout={() => {
        logEvent('processing_timeout', {
          receiptId,
          duration: Date.now() - startTime
        });
        
        // Don't navigate - allow retry
      }}
    />
  );
}

// ============================================================================
// EXAMPLE 4: With Error Recovery
// ============================================================================

export function ErrorRecoveryExample() {
  const navigate = useNavigate();
  const { toast } = useToast();
  
  const [receiptId, setReceiptId] = useState<string>('receipt-123');
  const [retryCount, setRetryCount] = useState(0);
  const MAX_RETRIES = 3;
  
  const handleError = (error: string) => {
    if (retryCount < MAX_RETRIES) {
      // Automatic retry
      setRetryCount(prev => prev + 1);
      toast.warning(`מנסה שוב (ניסיון ${retryCount + 1}/${MAX_RETRIES})...`);
      
      // Component will auto-retry via receipt store
    } else {
      // Max retries reached
      toast.error('העיבוד נכשל מספר פעמים. אנא נסה להעלות תמונה אחרת.');
      navigate('/upload');
    }
  };
  
  return (
    <ReceiptProcessing
      receiptId={receiptId}
      onComplete={() => {
        toast.success('עיבוד הושלם!');
        navigate(`/receipts/${receiptId}/review`);
      }}
      onError={handleError}
      onTimeout={() => {
        toast.warning('העיבוד לוקח זמן רב');
      }}
    />
  );
}

// ============================================================================
// EXAMPLE 5: With Loading State Persistence
// ============================================================================

export function PersistenceExample() {
  const navigate = useNavigate();
  
  // Persist to localStorage (for page refresh)
  const saveProcessingState = (receiptId: string) => {
    localStorage.setItem('processingReceiptId', receiptId);
    localStorage.setItem('processingStartTime', Date.now().toString());
  };
  
  const clearProcessingState = () => {
    localStorage.removeItem('processingReceiptId');
    localStorage.removeItem('processingStartTime');
  };
  
  // On component mount, check if there's an active processing
  React.useEffect(() => {
    const processingReceiptId = localStorage.getItem('processingReceiptId');
    const startTime = localStorage.getItem('processingStartTime');
    
    if (processingReceiptId && startTime) {
      const elapsed = Date.now() - parseInt(startTime);
      
      // If less than 2 minutes, resume
      if (elapsed < 120000) {
        console.log('Resuming processing:', processingReceiptId);
      } else {
        // Too old, clear
        clearProcessingState();
      }
    }
  }, []);
  
  const receiptId = localStorage.getItem('processingReceiptId') || 'new-receipt';
  
  return (
    <ReceiptProcessing
      receiptId={receiptId}
      onComplete={() => {
        clearProcessingState();
        navigate(`/receipts/${receiptId}/review`);
      }}
      onError={(error) => {
        clearProcessingState();
        navigate('/upload');
      }}
      onTimeout={() => {
        console.warn('Processing timeout');
      }}
    />
  );
}

// ============================================================================
// EXAMPLE 6: Standalone Page Component
// ============================================================================

export function ProcessingPage() {
  const navigate = useNavigate();
  const { toast } = useToast();
  
  // Get receiptId from URL params or state
  const params = new URLSearchParams(window.location.search);
  const receiptId = params.get('receiptId');
  
  if (!receiptId) {
    navigate('/upload');
    return null;
  }
  
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-xl font-semibold text-gray-900">
            מעבד קבלה
          </h1>
        </div>
      </header>
      
      {/* Processing Component */}
      <main>
        <ReceiptProcessing
          receiptId={receiptId}
          onComplete={() => {
            toast.success('עיבוד הושלם בהצלחה!');
            navigate(`/receipts/${receiptId}/review`);
          }}
          onError={(error) => {
            toast.error(error);
            navigate('/upload');
          }}
          onTimeout={() => {
            toast.warning('העיבוד לוקח זמן רב מהרגיל');
          }}
        />
      </main>
    </div>
  );
}

// ============================================================================
// EXAMPLE 7: Testing Helper
// ============================================================================

export function TestingWrapper() {
  const [mockReceiptId] = useState('test-receipt-123');
  const [mockStatus, setMockStatus] = useState<'processing' | 'review' | 'failed'>('processing');
  
  // Simulate status changes for testing
  React.useEffect(() => {
    const timer = setTimeout(() => {
      setMockStatus('review'); // Simulate success after 10 seconds
    }, 10000);
    
    return () => clearTimeout(timer);
  }, []);
  
  return (
    <div>
      <div className="p-4 bg-yellow-100 text-yellow-900">
        <p>Testing Mode - Mock Status: {mockStatus}</p>
        <button onClick={() => setMockStatus('review')}>Simulate Success</button>
        <button onClick={() => setMockStatus('failed')}>Simulate Error</button>
      </div>
      
      <ReceiptProcessing
        receiptId={mockReceiptId}
        onComplete={() => console.log('✅ onComplete called')}
        onError={(error) => console.log('❌ onError called:', error)}
        onTimeout={() => console.log('⏱️ onTimeout called')}
      />
    </div>
  );
}

// ============================================================================
// EXAMPLE 8: Usage in React Router
// ============================================================================

/*
// In your router configuration:

import { ProcessingPage } from './ProcessingPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        path: 'upload',
        element: <UploadPage />
      },
      {
        path: 'processing/:receiptId',
        element: <ProcessingPage />
      },
      {
        path: 'receipts/:receiptId/review',
        element: <ReviewPage />
      }
    ]
  }
]);

// Then in UploadPage:
const handleUploadComplete = (receiptId: string) => {
  navigate(`/processing/${receiptId}`);
};
*/

export default ReceiptProcessing;
