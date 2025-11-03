# ReceiptProcessing Component - Quick Reference

## Overview
Animated processing screen displayed during receipt OCR processing with real-time progress updates, stage visualization, and error handling.

---

## Import

```tsx
import { ReceiptProcessing } from '@/components/receipt';
```

---

## Basic Usage

```tsx
import { ReceiptProcessing } from '@/components/receipt';
import { useNavigate } from 'react-router-dom';

function ProcessingPage() {
  const navigate = useNavigate();
  
  return (
    <ReceiptProcessing
      receiptId="receipt-123"
      onComplete={() => navigate('/receipts/review')}
      onError={(error) => console.error(error)}
      onTimeout={() => console.warn('Processing timeout')}
    />
  );
}
```

---

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `receiptId` | `string` | ✅ | ID of receipt being processed |
| `onComplete` | `() => void` | ✅ | Callback when processing succeeds |
| `onError` | `(error: string) => void` | ✅ | Callback when processing fails |
| `onTimeout` | `() => void` | ✅ | Callback when processing times out |

---

## Features

### ✅ Animated Progress
- Rotating loader icon (framer-motion)
- Animated progress bar (0-100%)
- Smooth transitions between stages

### ✅ Real-Time Status
- 5 processing stages with labels
- Status icons (pending/active/complete)
- Elapsed time counter (MM:SS format)

### ✅ Error Handling
- Error state with friendly message
- Timeout detection (60 seconds)
- Retry button with animation

### ✅ Stage Visualization
- Upload → OCR → Extraction → Validation → Categorization
- Color-coded borders (gray/blue/green)
- Stage duration estimates

---

## Processing Stages

```typescript
const PROCESSING_STAGES = [
  { id: 'upload', label: 'העלאת תמונה', duration: 2 },
  { id: 'ocr', label: 'זיהוי טקסט', duration: 5 },
  { id: 'extraction', label: 'חילוץ נתונים', duration: 3 },
  { id: 'validation', label: 'אימות מידע', duration: 2 },
  { id: 'categorization', label: 'סיווג הוצאה', duration: 2 }
];
```

**Total Expected Time:** ~14 seconds  
**Timeout Threshold:** 60 seconds

---

## State Management

### Receipt Store Integration

```tsx
const { currentReceipt, isProcessing, error, retryProcessing } = useReceipt();
```

**Monitors:**
- `isProcessing`: Controls UI state
- `currentReceipt.status`: Triggers completion/error callbacks
- `error`: Displays error message

**Actions:**
- `retryProcessing(receiptId)`: Retry failed processing

---

## Completion Logic

```typescript
useEffect(() => {
  if (currentReceipt && currentReceipt.id === receiptId && !isProcessing) {
    if (currentReceipt.status === 'review' || currentReceipt.status === 'approved') {
      onComplete(); // Navigate to review page
    } else if (currentReceipt.status === 'failed') {
      onError('עיבוד הקבלה נכשל');
    }
  }
}, [currentReceipt, receiptId, isProcessing, onComplete, onError]);
```

---

## Error States

### Processing Error
```tsx
<ReceiptProcessing
  receiptId="receipt-123"
  onError={(error) => {
    toast.error(error);
    navigate('/upload');
  }}
  // ...
/>
```

**Displays:**
- ❌ Red error icon
- Error message from store
- "חזור" and "נסה שוב" buttons

### Timeout Error
```tsx
<ReceiptProcessing
  receiptId="receipt-123"
  onTimeout={() => {
    logEvent('processing_timeout', { receiptId });
    // Still allows retry
  }}
  // ...
/>
```

**Displays:**
- ⏱️ "העיבוד לוקח זמן רב מהרגיל"
- Helpful explanation
- Retry button enabled

---

## Full Example (Upload Flow)

```tsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ReceiptUpload, ReceiptProcessing } from '@/components/receipt';
import { useReceipt } from '@/hooks/useReceipt';

function UploadPage() {
  const navigate = useNavigate();
  const { uploadReceipt } = useReceipt();
  const [uploadedReceiptId, setUploadedReceiptId] = useState<string | null>(null);
  
  const handleUpload = async (file: File) => {
    try {
      const receiptId = await uploadReceipt(file);
      setUploadedReceiptId(receiptId);
    } catch (error) {
      console.error('Upload failed:', error);
    }
  };
  
  if (uploadedReceiptId) {
    return (
      <ReceiptProcessing
        receiptId={uploadedReceiptId}
        onComplete={() => navigate(`/receipts/${uploadedReceiptId}/review`)}
        onError={(error) => {
          console.error(error);
          setUploadedReceiptId(null); // Return to upload
        }}
        onTimeout={() => {
          console.warn('Processing timeout');
          // Still can retry, don't reset
        }}
      />
    );
  }
  
  return <ReceiptUpload onUpload={handleUpload} />;
}
```

---

## Styling

### Progress Bar
- Background: `#E5E7EB` (gray-200)
- Fill: Gradient `#6366F1` to `#4F46E5` (primary-500 to primary-600)
- Height: 8px (0.5rem)
- Border radius: Full (9999px)

### Stage Cards
```css
Active:   border-primary-600 bg-primary-50
Complete: border-green-200 bg-green-50
Pending:  border-gray-200 bg-white
```

### Icons
- Complete: Green checkmark (`CheckCircle`)
- Active: Spinning loader (`Loader2`)
- Pending: Gray outline circle

---

## Animations

### Loader Rotation
```tsx
<motion.div
  animate={{ rotate: 360 }}
  transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
>
  <Loader2 size={64} className="text-primary-600" />
</motion.div>
```

### Progress Bar
```tsx
<motion.div
  className="h-full bg-gradient-to-r from-primary-500 to-primary-600"
  initial={{ width: 0 }}
  animate={{ width: `${progressPercentage}%` }}
  transition={{ duration: 0.5, ease: 'easeOut' }}
/>
```

### Stage Cards
```tsx
<motion.div
  key={stage.id}
  initial={{ opacity: 0, x: -20 }}
  animate={{ opacity: 1, x: 0 }}
  exit={{ opacity: 0, x: 20 }}
  transition={{ delay: index * 0.1 }}
>
  {/* Stage content */}
</motion.div>
```

### Error Icon
```tsx
<motion.div
  initial={{ scale: 0 }}
  animate={{ scale: 1 }}
  transition={{ type: 'spring', duration: 0.5 }}
>
  <XCircle size={48} className="text-red-600" />
</motion.div>
```

---

## Accessibility

### Keyboard Navigation
- ✅ Retry button focusable
- ✅ Back button focusable
- ✅ Tab order logical

### Screen Readers
```tsx
<h2 className="text-2xl font-semibold text-gray-900 mb-2">
  מעבד קבלה...
</h2>
```
- Clear heading hierarchy
- Descriptive error messages
- Stage labels announced

### Motion Preferences
- Uses `framer-motion` (respects `prefers-reduced-motion`)
- All animations can be disabled via system settings

---

## Performance

### Timers
- Stage interval: 3 seconds
- Time counter: 1 second
- Both cleanup on unmount

### Re-renders
- Minimal: Only updates on stage change or time tick
- Memoization not needed (simple state)

---

## Testing

### Test Cases

```tsx
import { render, screen, waitFor } from '@testing-library/react';
import { ReceiptProcessing } from './ReceiptProcessing';

// Mock hooks
jest.mock('@/hooks/useReceipt');

describe('ReceiptProcessing', () => {
  it('displays processing state', () => {
    render(
      <ReceiptProcessing
        receiptId="test-123"
        onComplete={jest.fn()}
        onError={jest.fn()}
        onTimeout={jest.fn()}
      />
    );
    
    expect(screen.getByText('מעבד קבלה...')).toBeInTheDocument();
    expect(screen.getByText('העלאת תמונה')).toBeInTheDocument();
  });
  
  it('calls onComplete when processing succeeds', async () => {
    const onComplete = jest.fn();
    
    // Mock receipt store
    (useReceipt as jest.Mock).mockReturnValue({
      currentReceipt: { id: 'test-123', status: 'review' },
      isProcessing: false,
      error: null
    });
    
    render(
      <ReceiptProcessing
        receiptId="test-123"
        onComplete={onComplete}
        onError={jest.fn()}
        onTimeout={jest.fn()}
      />
    );
    
    await waitFor(() => {
      expect(onComplete).toHaveBeenCalled();
    });
  });
  
  it('displays error state and allows retry', () => {
    (useReceipt as jest.Mock).mockReturnValue({
      currentReceipt: null,
      isProcessing: false,
      error: 'תמונה לא ברורה'
    });
    
    render(
      <ReceiptProcessing
        receiptId="test-123"
        onComplete={jest.fn()}
        onError={jest.fn()}
        onTimeout={jest.fn()}
      />
    );
    
    expect(screen.getByText('שגיאה בעיבוד')).toBeInTheDocument();
    expect(screen.getByText('נסה שוב')).toBeInTheDocument();
  });
  
  it('triggers timeout after 60 seconds', async () => {
    jest.useFakeTimers();
    const onTimeout = jest.fn();
    
    (useReceipt as jest.Mock).mockReturnValue({
      currentReceipt: null,
      isProcessing: true,
      error: null
    });
    
    render(
      <ReceiptProcessing
        receiptId="test-123"
        onComplete={jest.fn()}
        onError={jest.fn()}
        onTimeout={onTimeout}
      />
    );
    
    // Fast-forward 60 seconds
    jest.advanceTimersByTime(60000);
    
    await waitFor(() => {
      expect(onTimeout).toHaveBeenCalled();
    });
    
    jest.useRealTimers();
  });
});
```

---

## Common Issues

### Issue: onComplete not called
**Cause:** Receipt status not 'review' or 'approved'  
**Fix:** Check receipt store status in backend

### Issue: Stages stuck
**Cause:** `isProcessing` still true  
**Fix:** Ensure backend updates receipt status

### Issue: Timeout too aggressive
**Cause:** 60 seconds too short for slow connections  
**Fix:** Increase `TIMEOUT_SECONDS` constant

---

## Related Components

- `ReceiptUpload` - Initiates processing
- `ReceiptReview` - Next step after completion
- `useReceipt` hook - State management

---

## Design Tokens

```typescript
// Colors
Primary:   #2563EB (primary-600)
Success:   #10B981 (green-600)
Error:     #EF4444 (red-600)
Gray:      #6B7280 (gray-600)

// Spacing
Container: p-8 (32px)
Stage gap: space-y-3 (12px)
Icon size: 64px (loader), 24px (stages)

// Animation
Rotation:  2s linear infinite
Progress:  0.5s ease-out
Stages:    0.1s stagger
```

---

**Version:** 1.0.0  
**Last Updated:** November 2025  
**Status:** ✅ Production Ready
