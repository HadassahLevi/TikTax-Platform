# ReceiptUpload - Quick Reference

## 🚀 INSTANT USAGE

```tsx
import { ReceiptUpload } from '@/components/receipt';

<ReceiptUpload
  onUploadSuccess={(receiptId) => navigate(`/receipts/${receiptId}`)}
  onCancel={() => navigate('/dashboard')}
/>
```

---

## 📋 PROPS

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `onUploadSuccess` | `(receiptId: string) => void` | ✅ Yes | Called when upload succeeds |
| `onCancel` | `() => void` | ❌ No | Called when user cancels |

---

## 🎨 UI STATES

### 1. Upload Options (Default)
- Drag-drop zone
- Gallery upload button
- Camera button
- Cancel button

### 2. Camera View
- Full-screen video
- Large capture button (80px circle)
- Cancel & switch camera buttons

### 3. Preview & Upload
- Image preview
- Retake button
- Upload button (with loading)
- Error display

---

## ⚙️ FEATURES

| Feature | Status | Description |
|---------|--------|-------------|
| Camera Access | ✅ | Uses back camera on mobile |
| Gallery Upload | ✅ | File picker integration |
| Drag & Drop | ✅ | Desktop file drag-drop |
| File Validation | ✅ | Type & size checks |
| Preview | ✅ | Before upload confirmation |
| Loading States | ✅ | Upload progress indication |
| Error Handling | ✅ | Hebrew error messages |
| Auto-cleanup | ✅ | Memory & stream management |

---

## 📱 MOBILE BEHAVIOR

- **Camera**: Back camera prioritized (`facingMode: 'environment'`)
- **Touch targets**: 48px+ for easy tapping
- **Full-screen**: Immersive camera experience
- **Thumb-zone**: Controls at bottom

---

## 🛡️ VALIDATION

```typescript
// Type validation
ALLOWED_FILE_TYPES = ['image/jpeg', 'image/png', 'application/pdf']

// Size validation
MAX_FILE_SIZE = 10MB (10 * 1024 * 1024 bytes)
```

### Error Messages (Hebrew)
```
"סוג קובץ לא נתמך. השתמש ב-JPG, PNG או PDF"
"הקובץ גדול מדי (מקסימום 10MB)"
"לא ניתן לגשת למצלמה. בדוק הרשאות."
```

---

## 🔌 DEPENDENCIES

```typescript
// Required
import Button from '@/components/ui/Button';
import { useReceipt } from '@/hooks/useReceipt';
import { MAX_FILE_SIZE, ALLOWED_FILE_TYPES } from '@/types/receipt.types';

// Icons
import { Camera, Upload, X, RefreshCw } from 'lucide-react';
```

---

## 🔄 WORKFLOW

```
┌─────────────────┐
│ Upload Options  │ ← Start here
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────┐   ┌────────┐
│Camera│   │Gallery │
└──┬──┘   └───┬────┘
   │          │
   └────┬─────┘
        ▼
   ┌─────────┐
   │ Preview │
   └────┬────┘
        ▼
   ┌────────┐
   │ Upload │
   └────┬───┘
        ▼
   ┌─────────┐
   │ Success │
   └─────────┘
```

---

## 💡 COMMON PATTERNS

### Full-Screen Upload Page
```tsx
export const UploadPage = () => {
  const navigate = useNavigate();
  
  return (
    <div className="h-screen">
      <ReceiptUpload
        onUploadSuccess={(id) => navigate(`/receipts/${id}`)}
        onCancel={() => navigate(-1)}
      />
    </div>
  );
};
```

### Modal Upload
```tsx
const [showUpload, setShowUpload] = useState(false);

<Modal isOpen={showUpload}>
  <ReceiptUpload
    onUploadSuccess={(id) => {
      setShowUpload(false);
      navigate(`/receipts/${id}`);
    }}
    onCancel={() => setShowUpload(false)}
  />
</Modal>
```

### With Notifications
```tsx
const { showToast } = useToast();

<ReceiptUpload
  onUploadSuccess={(id) => {
    showToast({ type: 'success', message: 'הקבלה הועלתה!' });
    navigate(`/receipts/${id}`);
  }}
/>
```

---

## 🎯 KEY METHODS

| Method | Purpose | When Called |
|--------|---------|-------------|
| `startCamera()` | Request camera access | User clicks camera button |
| `capturePhoto()` | Capture frame to file | User taps capture button |
| `handleFileSelect()` | Process file | Gallery/drag-drop/camera |
| `validateFile()` | Check type & size | Before preview |
| `handleUpload()` | Upload to server | User confirms upload |
| `handleReset()` | Clear state | User clicks retake |

---

## 🧹 CLEANUP

Component automatically handles:
- ✅ Camera stream shutdown
- ✅ Preview URL revocation
- ✅ Event listener cleanup
- ✅ Memory release on unmount

```typescript
useEffect(() => {
  return () => {
    stopCamera();
    if (previewUrl) URL.revokeObjectURL(previewUrl);
  };
}, []);
```

---

## 🎨 STYLING

### Camera View
```css
.camera-view {
  position: fixed;
  inset: 0;
  z-index: 50;
  background: black;
}

.capture-button {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: white;
  border: 4px solid #2563eb;
}
```

### Drag-Drop Zone
```css
.drop-zone {
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  padding: 32px;
}

.drop-zone.dragging {
  border-color: #2563eb;
  background: #eff6ff;
  transform: scale(1.05);
}
```

---

## 📊 STATE MANAGEMENT

```typescript
// Component State
const [captureMode, setCaptureMode] = useState<'camera' | 'gallery' | null>(null);
const [previewUrl, setPreviewUrl] = useState<string | null>(null);
const [selectedFile, setSelectedFile] = useState<File | null>(null);
const [isDragging, setIsDragging] = useState(false);
const [stream, setStream] = useState<MediaStream | null>(null);

// From useReceipt Hook
const {
  uploadReceipt,      // Function to upload file
  isUploading,        // Boolean: upload in progress
  uploadError,        // String: error message
  clearError          // Function to clear error
} = useReceipt();
```

---

## 🔧 CUSTOMIZATION

### Camera Settings
```typescript
const mediaStream = await navigator.mediaDevices.getUserMedia({
  video: { 
    facingMode: 'environment',  // 'user' for front camera
    width: { ideal: 1920 },
    height: { ideal: 1080 }
  }
});
```

### Capture Quality
```typescript
canvas.toBlob((blob) => {
  // ...
}, 'image/jpeg', 0.95);  // 95% quality
```

---

## 🚨 ERROR HANDLING

### Camera Errors
```typescript
try {
  await startCamera();
} catch (error) {
  alert('לא ניתן לגשת למצלמה. בדוק הרשאות.');
  console.error('Camera error:', error);
}
```

### Upload Errors
```tsx
{uploadError && (
  <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
    {uploadError}
  </div>
)}
```

---

## ✅ TESTING CHECKLIST

- [ ] Camera opens on mobile
- [ ] Back camera used (not front)
- [ ] Capture button works
- [ ] Gallery upload works
- [ ] Drag-drop works (desktop)
- [ ] File type validation
- [ ] File size validation
- [ ] Preview displays correctly
- [ ] Upload button triggers upload
- [ ] Loading state shows
- [ ] Success callback fires
- [ ] Cancel works
- [ ] Reset clears state
- [ ] Component unmounts cleanly
- [ ] Works on iOS Safari
- [ ] Works on Chrome Android

---

## 📚 RELATED DOCS

- `RECEIPTUPLOAD.SUMMARY.md` - Full implementation details
- `useReceipt.ts` - Upload hook documentation
- `receipt.types.ts` - Type definitions
- `Button.tsx` - Button component API

---

## 🎉 READY TO USE!

Component is production-ready with:
- ✅ Full TypeScript types
- ✅ Mobile optimization
- ✅ Error handling
- ✅ Accessibility
- ✅ Clean code
- ✅ Documentation

Just import and integrate! 🚀
