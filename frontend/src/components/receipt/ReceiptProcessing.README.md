# ReceiptProcessing Component

**Professional animated processing screen with real-time status updates, stage visualization, error handling, and timeout detection.**

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Props API](#props-api)
5. [Usage Examples](#usage-examples)
6. [Processing Stages](#processing-stages)
7. [State Management](#state-management)
8. [Error Handling](#error-handling)
9. [Animations](#animations)
10. [Accessibility](#accessibility)
11. [Testing](#testing)
12. [Troubleshooting](#troubleshooting)

---

## Overview

The `ReceiptProcessing` component displays an animated, user-friendly interface during OCR receipt processing. It provides:

- **Visual feedback:** Rotating loader, progress bar, stage indicators
- **Time awareness:** Elapsed time counter, timeout detection
- **Error recovery:** Retry mechanism, clear error messages
- **Smooth animations:** framer-motion powered transitions

**Typical Flow:**
```
ReceiptUpload → ReceiptProcessing → ReceiptReview
     ↓                ↓                    ↓
  (Image)        (OCR Process)        (Edit/Approve)
```

---

## Features

### ✅ Animated Progress Visualization
- **Rotating loader:** Continuous 360° rotation (2s cycle)
- **Progress bar:** Animated 0-100% fill with gradient
- **Smooth transitions:** All state changes animated

### ✅ Real-Time Status Updates
- **5 processing stages:** Upload → OCR → Extraction → Validation → Categorization
- **Status indicators:**
  - ⭕ Gray outline: Pending
  - 🔵 Spinning loader: Active
  - ✅ Green checkmark: Complete
- **Elapsed time:** MM:SS format counter

### ✅ Comprehensive Error Handling
- **Error detection:** Catches API errors from receipt store
- **Timeout detection:** Triggers warning after 60 seconds
- **Retry mechanism:** One-click retry with state reset
- **User-friendly messages:** Hebrew error descriptions

### ✅ Responsive Design
- **Mobile-optimized:** min-h-[500px] with padding
- **RTL support:** Hebrew text alignment
- **Touch-friendly:** Large buttons, clear targets

---

## Installation

Component is part of the receipt component library. No separate installation needed.

```tsx
import { ReceiptProcessing } from '@/components/receipt';
```

**Dependencies:**
- `react` 18.2+
- `framer-motion` 10.16+
- `lucide-react` 0.294+
- `@/components/ui/Button`
- `@/hooks/useReceipt`

---

## Props API

### ReceiptProcessingProps

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `receiptId` | `string` | ✅ | - | Unique ID of receipt being processed |
| `onComplete` | `() => void` | ✅ | - | Callback invoked when processing succeeds (status: review/approved) |
| `onError` | `(error: string) => void` | ✅ | - | Callback invoked when processing fails (status: failed or error in store) |
| `onTimeout` | `() => void` | ✅ | - | Callback invoked when processing exceeds 60 seconds |

**TypeScript Definition:**
```typescript
export interface ReceiptProcessingProps {
  receiptId: string;
  onComplete: () => void;
  onError: (error: string) => void;
  onTimeout: () => void;
}
```

---

## Usage Examples

### Basic Usage

```tsx
import { ReceiptProcessing } from '@/components/receipt';
import { useNavigate } from 'react-router-dom';

function ProcessingPage() {
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
        console.warn('Processing timeout - but allowing retry');
      }}
    />
  );
}
```

### Complete Upload → Processing → Review Flow

```tsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ReceiptUpload, ReceiptProcessing } from '@/components/receipt';
import { useReceipt } from '@/hooks/useReceipt';
import { useToast } from '@/hooks/useToast';

function UploadFlow() {
  const navigate = useNavigate();
  const { uploadReceipt } = useReceipt();
  const { toast } = useToast();
  
  const [stage, setStage] = useState<'upload' | 'processing' | 'review'>('upload');
  const [receiptId, setReceiptId] = useState<string | null>(null);
  
  const handleUpload = async (file: File) => {
    try {
      const id = await uploadReceipt(file);
      setReceiptId(id);
      setStage('processing');
    } catch (error) {
      toast.error('העלאה נכשלה');
    }
  };
  
  const handleComplete = () => {
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
      {stage === 'upload' && <ReceiptUpload onUpload={handleUpload} />}
      
      {stage === 'processing' && receiptId && (
        <ReceiptProcessing
          receiptId={receiptId}
          onComplete={handleComplete}
          onError={handleError}
          onTimeout={handleTimeout}
        />
      )}
    </div>
  );
}
```

### With Analytics

```tsx
import { ReceiptProcessing } from '@/components/receipt';
import { useNavigate } from 'react-router-dom';
import { logEvent } from '@/utils/analytics';

function ProcessingPage({ receiptId }: { receiptId: string }) {
  const navigate = useNavigate();
  
  return (
    <ReceiptProcessing
      receiptId={receiptId}
      onComplete={() => {
        logEvent('processing_completed', { receiptId, duration: elapsedTime });
        navigate(`/receipts/${receiptId}/review`);
      }}
      onError={(error) => {
        logEvent('processing_failed', { receiptId, error });
        navigate('/upload');
      }}
      onTimeout={() => {
        logEvent('processing_timeout', { receiptId });
        // Don't navigate - allow retry
      }}
    />
  );
}
```

---

## Processing Stages

### Stage Definitions

```typescript
const PROCESSING_STAGES: ProcessingStage[] = [
  { id: 'upload', label: 'העלאת תמונה', duration: 2 },      // Upload image
  { id: 'ocr', label: 'זיהוי טקסט', duration: 5 },         // OCR text recognition
  { id: 'extraction', label: 'חילוץ נתונים', duration: 3 }, // Data extraction
  { id: 'validation', label: 'אימות מידע', duration: 2 },   // Validation
  { id: 'categorization', label: 'סיווג הוצאה', duration: 2 } // Categorization
];
```

### Stage Progression

- **Automatic:** Advances every 3 seconds (simulated, not tied to actual backend)
- **Visual indicators:**
  - Pending: Gray outline circle
  - Active: Blue spinning loader + highlighted card
  - Complete: Green checkmark + green card

**Example:**
```
Stage 0 (Active)   → Upload image        🔵 (0-20%)
Stage 1 (Pending)  → OCR text            ⭕ 
Stage 2 (Pending)  → Extract data        ⭕
Stage 3 (Pending)  → Validate info       ⭕
Stage 4 (Pending)  → Categorize expense  ⭕

... 3 seconds later ...

Stage 0 (Complete) → Upload image        ✅ (20-40%)
Stage 1 (Active)   → OCR text            🔵
Stage 2 (Pending)  → Extract data        ⭕
Stage 3 (Pending)  → Validate info       ⭕
Stage 4 (Pending)  → Categorize expense  ⭕
```

### Progress Calculation

```typescript
const progressPercentage = Math.min(
  Math.round(((currentStage + 1) / PROCESSING_STAGES.length) * 100),
  100
);
```

**Progress Mapping:**
- Stage 0 → 20%
- Stage 1 → 40%
- Stage 2 → 60%
- Stage 3 → 80%
- Stage 4 → 100%

---

## State Management

### Receipt Store Integration

The component integrates with the global receipt store via `useReceipt()` hook:

```typescript
const { currentReceipt, isProcessing, error, retryProcessing } = useReceipt();
```

**Monitored State:**
- `currentReceipt`: Receipt object being processed
- `isProcessing`: Boolean indicating active processing
- `error`: Error message from failed processing
- `retryProcessing()`: Function to retry failed processing

### Completion Detection

```typescript
useEffect(() => {
  if (currentReceipt && currentReceipt.id === receiptId && !isProcessing) {
    if (currentReceipt.status === 'review' || currentReceipt.status === 'approved') {
      onComplete(); // Success
    } else if (currentReceipt.status === 'failed') {
      onError('עיבוד הקבלה נכשל'); // Failure
    }
  }
}, [currentReceipt, receiptId, isProcessing, onComplete, onError]);
```

**Status Flow:**
```
processing → review    (Success - call onComplete)
processing → approved  (Success - call onComplete)
processing → failed    (Failure - call onError)
```

### Local State

```typescript
const [currentStage, setCurrentStage] = useState(0);        // Stage index (0-4)
const [elapsedTime, setElapsedTime] = useState(0);          // Seconds elapsed
const [hasTimedOut, setHasTimedOut] = useState(false);      // Timeout flag
```

---

## Error Handling

### Error Types

#### 1. API Error (from store)
```typescript
// Triggered when receipt.error is set
if (error) {
  return <ErrorState message={error} />;
}
```

**Example errors:**
- "תמונה לא ברורה" (Image not clear)
- "שגיאת שרת" (Server error)
- "חיבור נכשל" (Connection failed)

#### 2. Timeout Error
```typescript
// Triggered after 60 seconds
if (elapsedTime >= 60 && isProcessing) {
  setHasTimedOut(true);
  onTimeout();
}
```

**Displayed message:**
> "העיבוד לוקח זמן רב מהרגיל"  
> "העיבוד אמור להימשך 10-15 שניות. ייתכן שהתמונה לא ברורה או שיש בעיית חיבור."

#### 3. Processing Failure
```typescript
// Triggered when receipt.status === 'failed'
if (currentReceipt.status === 'failed') {
  onError('עיבוד הקבלה נכשל');
}
```

### Retry Mechanism

```typescript
const handleRetry = async () => {
  // Reset local state
  setCurrentStage(0);
  setElapsedTime(0);
  setHasTimedOut(false);
  
  try {
    // Retry via store
    await retryProcessing(receiptId);
  } catch (err) {
    onError('ניסיון חוזר נכשל');
  }
};
```

**Retry button:**
```tsx
<Button
  variant="primary"
  onClick={handleRetry}
  icon={<Loader2 size={20} className="animate-spin" />}
>
  נסה שוב
</Button>
```

---

## Animations

### 1. Rotating Loader

```tsx
<motion.div
  animate={{ rotate: 360 }}
  transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
  className="mb-8"
>
  <Loader2 size={64} className="text-primary-600" />
</motion.div>
```

**Properties:**
- Rotation: 360° continuous
- Duration: 2 seconds per cycle
- Easing: Linear (constant speed)
- Size: 64px

### 2. Progress Bar

```tsx
<motion.div
  className="h-full bg-gradient-to-r from-primary-500 to-primary-600"
  initial={{ width: 0 }}
  animate={{ width: `${progressPercentage}%` }}
  transition={{ duration: 0.5, ease: 'easeOut' }}
/>
```

**Properties:**
- Animation: Width 0% → current percentage
- Duration: 0.5 seconds
- Easing: ease-out (slows at end)
- Gradient: Blue (primary-500 to primary-600)

### 3. Stage Cards

```tsx
<motion.div
  key={stage.id}
  initial={{ opacity: 0, x: -20 }}
  animate={{ opacity: 1, x: 0 }}
  exit={{ opacity: 0, x: 20 }}
  transition={{ delay: index * 0.1 }}
  className={/* dynamic classes */}
>
  {/* Stage content */}
</motion.div>
```

**Properties:**
- Entry: Fade in from left (x: -20)
- Exit: Fade out to right (x: 20)
- Stagger: 0.1s delay per stage (0s, 0.1s, 0.2s, 0.3s, 0.4s)

### 4. Error Icon

```tsx
<motion.div
  initial={{ scale: 0 }}
  animate={{ scale: 1 }}
  transition={{ type: 'spring', duration: 0.5 }}
>
  <XCircle size={48} className="text-red-600" />
</motion.div>
```

**Properties:**
- Animation: Scale from 0 to 1 (pop effect)
- Type: Spring (bounce)
- Duration: 0.5 seconds

### Reduced Motion

All animations respect `prefers-reduced-motion` via framer-motion's built-in support.

```css
@media (prefers-reduced-motion: reduce) {
  /* framer-motion automatically disables animations */
}
```

---

## Accessibility

### Keyboard Navigation

✅ **Focusable elements:**
- Retry button (Tab to focus, Enter to activate)
- Back button (Tab to focus, Enter to activate)

✅ **Tab order:**
1. Error icon (not focusable)
2. Back button
3. Retry button

### Screen Readers

✅ **Semantic HTML:**
```tsx
<h2 className="text-2xl font-semibold text-gray-900 mb-2">
  מעבד קבלה...
</h2>
```

✅ **Descriptive labels:**
- Stage names: "העלאת תמונה", "זיהוי טקסט", etc.
- Error messages: Full sentences explaining issue
- Time counter: "0:45" format (announced as "zero minutes forty-five seconds")

✅ **Status announcements:**
```tsx
<p className="text-sm text-gray-600 mt-2 text-center">
  {progressPercentage}% הושלם
</p>
```

### Visual Accessibility

✅ **Color contrast:**
- Text on white: 4.5:1+ (WCAG AA)
- Error text: Red #DC2626 on white background
- Success text: Green #059669 on white background

✅ **Icon + text:**
- Not relying on color alone
- Each stage has icon AND text label

✅ **Focus indicators:**
- Browser default (outline)
- High contrast mode compatible

---

## Testing

### Unit Tests

```tsx
import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ReceiptProcessing } from './ReceiptProcessing';
import { useReceipt } from '@/hooks/useReceipt';

jest.mock('@/hooks/useReceipt');

describe('ReceiptProcessing', () => {
  const mockUseReceipt = useReceipt as jest.MockedFunction<typeof useReceipt>;
  
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  it('renders processing state with all stages', () => {
    mockUseReceipt.mockReturnValue({
      currentReceipt: null,
      isProcessing: true,
      error: null,
      retryProcessing: jest.fn()
    });
    
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
    expect(screen.getByText('זיהוי טקסט')).toBeInTheDocument();
    expect(screen.getByText('חילוץ נתונים')).toBeInTheDocument();
    expect(screen.getByText('אימות מידע')).toBeInTheDocument();
    expect(screen.getByText('סיווג הוצאה')).toBeInTheDocument();
    expect(screen.getByText('0% הושלם')).toBeInTheDocument();
  });
  
  it('calls onComplete when processing succeeds', async () => {
    const onComplete = jest.fn();
    
    mockUseReceipt.mockReturnValue({
      currentReceipt: { id: 'test-123', status: 'review' },
      isProcessing: false,
      error: null,
      retryProcessing: jest.fn()
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
      expect(onComplete).toHaveBeenCalledTimes(1);
    });
  });
  
  it('calls onError when processing fails', async () => {
    const onError = jest.fn();
    
    mockUseReceipt.mockReturnValue({
      currentReceipt: { id: 'test-123', status: 'failed' },
      isProcessing: false,
      error: null,
      retryProcessing: jest.fn()
    });
    
    render(
      <ReceiptProcessing
        receiptId="test-123"
        onComplete={jest.fn()}
        onError={onError}
        onTimeout={jest.fn()}
      />
    );
    
    await waitFor(() => {
      expect(onError).toHaveBeenCalledWith('עיבוד הקבלה נכשל');
    });
  });
  
  it('displays error state with retry button', () => {
    mockUseReceipt.mockReturnValue({
      currentReceipt: null,
      isProcessing: false,
      error: 'תמונה לא ברורה',
      retryProcessing: jest.fn()
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
    expect(screen.getByText('תמונה לא ברורה')).toBeInTheDocument();
    expect(screen.getByText('נסה שוב')).toBeInTheDocument();
    expect(screen.getByText('חזור')).toBeInTheDocument();
  });
  
  it('calls retryProcessing when retry button clicked', async () => {
    const user = userEvent.setup();
    const retryProcessing = jest.fn();
    
    mockUseReceipt.mockReturnValue({
      currentReceipt: null,
      isProcessing: false,
      error: 'שגיאה',
      retryProcessing
    });
    
    render(
      <ReceiptProcessing
        receiptId="test-123"
        onComplete={jest.fn()}
        onError={jest.fn()}
        onTimeout={jest.fn()}
      />
    );
    
    await user.click(screen.getByText('נסה שוב'));
    
    expect(retryProcessing).toHaveBeenCalledWith('test-123');
  });
  
  it('triggers timeout after 60 seconds', async () => {
    jest.useFakeTimers();
    const onTimeout = jest.fn();
    
    mockUseReceipt.mockReturnValue({
      currentReceipt: null,
      isProcessing: true,
      error: null,
      retryProcessing: jest.fn()
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
    act(() => {
      jest.advanceTimersByTime(60000);
    });
    
    await waitFor(() => {
      expect(onTimeout).toHaveBeenCalled();
    });
    
    jest.useRealTimers();
  });
  
  it('updates progress bar as stages advance', async () => {
    jest.useFakeTimers();
    
    mockUseReceipt.mockReturnValue({
      currentReceipt: null,
      isProcessing: true,
      error: null,
      retryProcessing: jest.fn()
    });
    
    render(
      <ReceiptProcessing
        receiptId="test-123"
        onComplete={jest.fn()}
        onError={jest.fn()}
        onTimeout={jest.fn()}
      />
    );
    
    // Initially 20%
    expect(screen.getByText('20% הושלם')).toBeInTheDocument();
    
    // After 3 seconds → 40%
    act(() => {
      jest.advanceTimersByTime(3000);
    });
    expect(screen.getByText('40% הושלם')).toBeInTheDocument();
    
    // After 6 seconds → 60%
    act(() => {
      jest.advanceTimersByTime(3000);
    });
    expect(screen.getByText('60% הושלם')).toBeInTheDocument();
    
    jest.useRealTimers();
  });
});
```

### Integration Tests

```tsx
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import UploadFlow from './UploadFlow';

describe('Upload → Processing → Review Flow', () => {
  it('completes full flow', async () => {
    render(
      <BrowserRouter>
        <UploadFlow />
      </BrowserRouter>
    );
    
    // 1. Upload
    const file = new File(['receipt'], 'receipt.jpg', { type: 'image/jpeg' });
    const input = screen.getByLabelText(/upload/i);
    await userEvent.upload(input, file);
    
    // 2. Processing screen appears
    await waitFor(() => {
      expect(screen.getByText('מעבד קבלה...')).toBeInTheDocument();
    });
    
    // 3. Processing completes
    await waitFor(() => {
      expect(screen.getByText('Review Receipt')).toBeInTheDocument();
    }, { timeout: 5000 });
  });
});
```

---

## Troubleshooting

### Issue: onComplete never called

**Symptoms:**
- Processing screen stuck
- Receipt processed but screen doesn't change

**Possible causes:**
1. Receipt status not 'review' or 'approved'
2. `isProcessing` flag still true in store
3. `receiptId` mismatch

**Solution:**
```tsx
// Add debug logging
useEffect(() => {
  console.log('Current receipt:', currentReceipt);
  console.log('Is processing:', isProcessing);
  console.log('Receipt ID match:', currentReceipt?.id === receiptId);
}, [currentReceipt, isProcessing, receiptId]);
```

### Issue: Stages advance too quickly

**Symptoms:**
- All stages complete in 1 second

**Cause:**
- Multiple `setInterval` timers running

**Solution:**
```tsx
// Ensure cleanup
useEffect(() => {
  if (!isProcessing) return;
  
  const timer = setInterval(() => { /* ... */ }, 3000);
  
  return () => clearInterval(timer); // ✅ Cleanup
}, [isProcessing]);
```

### Issue: Memory leak warning

**Symptoms:**
- React warning: "Can't perform state update on unmounted component"

**Cause:**
- Timers not cleaned up

**Solution:**
```tsx
// All timers have cleanup functions
useEffect(() => {
  // ...
  return () => clearInterval(timer);
}, []);
```

### Issue: Timeout triggers immediately

**Symptoms:**
- Timeout warning appears after 1 second

**Cause:**
- `elapsedTime` incrementing too fast

**Solution:**
```tsx
// Check interval (should be 1000ms)
setInterval(() => {
  setElapsedTime(prev => prev + 1);
}, 1000); // ✅ Not 100 or 10
```

### Issue: Error state shows default message

**Symptoms:**
- Error says "אירעה שגיאה..." instead of specific error

**Cause:**
- `error` from store is null/undefined

**Solution:**
```tsx
// Use fallback
error || 'אירעה שגיאה בעיבוד הקבלה. אנא נסה שוב.'
```

---

## Design Tokens

```typescript
// Colors
const colors = {
  primary: '#2563EB',      // Primary blue (loader, active stage)
  success: '#10B981',      // Green (completed stages)
  error: '#EF4444',        // Red (error state)
  gray: {
    200: '#E5E7EB',        // Progress bar background
    600: '#6B7280',        // Secondary text
    900: '#111827'         // Primary text
  }
};

// Spacing
const spacing = {
  container: '2rem',       // p-8
  stageGap: '0.75rem',     // space-y-3
  iconGap: '0.75rem'       // gap-3
};

// Sizing
const sizing = {
  loaderIcon: '64px',      // Main loader
  stageIcon: '24px',       // Stage status icons
  progressBar: '8px',      // Progress bar height
  errorIcon: '48px'        // Error/success icons
};

// Animation timing
const timing = {
  loaderRotation: '2s',    // Full 360° rotation
  progressBar: '0.5s',     // Width animation
  stageStagger: '0.1s',    // Delay between stages
  errorIconSpring: '0.5s'  // Spring animation
};
```

---

## Related Components

- **ReceiptUpload** - Initiates processing
- **ReceiptReview** - Next step after completion
- **Button** - Used for retry/back actions

## Related Hooks

- **useReceipt** - Receipt state management
- **useToast** - Error notifications (optional)

## Related Types

- **ReceiptProcessingProps** - Component props
- **ProcessingStage** - Stage definition
- **ReceiptStatus** - Receipt status enum

---

**Version:** 1.0.0  
**Author:** Tik-Tax Development Team  
**Last Updated:** November 2025  
**Status:** ✅ Production Ready

---

## Quick Links

- [Quick Reference](./ReceiptProcessing.QUICKREF.md)
- [Receipt Types](../../types/RECEIPT_TYPES.md)
- [useReceipt Hook](../../hooks/USERECEIPT.README.md)
- [Button Component](../ui/Button.tsx)
