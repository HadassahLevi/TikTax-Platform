# ReceiptDetail - Quick Reference

## 🎯 Purpose
Detailed view for archived receipts with full metadata, image zoom, history, and actions.

---

## 📦 Import

```tsx
import { ReceiptDetail } from '@/components/receipt';
```

---

## 🚀 Basic Usage

```tsx
// In React Router
<Route path="/receipts/:id" element={<ReceiptDetail />} />

// Navigate to detail
navigate(`/receipts/${receiptId}`);
```

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Image Zoom** | Full-screen modal with 100%-300% zoom |
| **PDF Download** | Download digitally signed PDF |
| **Edit History** | Timeline of all changes |
| **Delete** | Safe deletion with confirmation |
| **Share** | Web Share API + clipboard fallback |
| **Category Badge** | Color-coded category display |
| **Digital Signature** | Verification status badge |

---

## 🎨 Visual Structure

```
┌─────────────────────────────────────┐
│ ← חזור    [Share] [Delete]          │ ← Header
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │                                 │ │
│ │     Receipt Image (clickable)   │ │ ← Image Preview
│ │                                 │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Vendor Name        [Category]   │ │
│ │ Date                            │ │
│ │                                 │ │
│ │ ┌─────────────────────────────┐ │ │
│ │ │   ₪1,234.56                 │ │ │ ← Amount Card
│ │ │   Pre-VAT  |  VAT           │ │ │
│ │ └─────────────────────────────┘ │ │
│ │                                 │ │
│ │ [Business] [Receipt #]          │ │ ← Details Grid
│ │ [Number]   [Upload Date]        │ │
│ │                                 │ │
│ │ [Notes section if exists]       │ │
│ └─────────────────────────────────┘ │
│                                     │
│ [Download PDF] [Edit] [History]    │ ← Actions
│                                     │
│ [✓ Digital Signature Badge]        │ ← If signed
└─────────────────────────────────────┘
```

---

## 🔧 Main Functions

### loadReceipt()
```typescript
// Loads receipt + history
const loadReceipt = async (receiptId: string) => {
  const receipt = await receiptService.getReceipt(receiptId);
  const history = await receiptService.getReceiptHistory(receiptId);
};
```

### handleDownloadPDF()
```typescript
// Downloads PDF with proper filename
const blob = await receiptService.downloadReceiptPDF(id);
const url = URL.createObjectURL(blob);
link.download = `קבלה-${vendor}-${date}.pdf`;
```

### handleDelete()
```typescript
// Delete with confirmation
const confirmed = window.confirm('האם אתה בטוח?');
if (confirmed) {
  await deleteReceipt(id);
  navigate('/archive');
}
```

### handleShare()
```typescript
// Web Share API with fallback
if (navigator.share) {
  await navigator.share({ title, text, url });
} else {
  await navigator.clipboard.writeText(url);
}
```

---

## 📊 State

```typescript
// Image modal
const [isImageModalOpen, setIsImageModalOpen] = useState(false);
const [imageZoom, setImageZoom] = useState(1); // 1.0 - 3.0

// History modal
const [showHistory, setShowHistory] = useState(false);
const [editHistory, setEditHistory] = useState<ReceiptEdit[]>([]);

// Loading
const [isDownloading, setIsDownloading] = useState(false);
const [isLoadingHistory, setIsLoadingHistory] = useState(false);
```

---

## 🎨 Key Components

### Amount Card
```tsx
<div className="bg-gradient-to-br from-primary-500 to-primary-600 
                rounded-xl p-6 text-white">
  <p className="text-4xl font-700">₪1,234.56</p>
  <div className="flex justify-between">
    <div>Pre-VAT: ₪1,046.61</div>
    <div>VAT: ₪187.95</div>
  </div>
</div>
```

### Detail Item
```tsx
<div className="flex items-start gap-3">
  <div className="w-10 h-10 rounded-lg bg-gray-100">
    <Icon size={20} />
  </div>
  <div>
    <p className="text-sm text-gray-600">Label</p>
    <p className="font-500 text-gray-900">Value</p>
  </div>
</div>
```

### Image Zoom Modal
```tsx
<Modal isOpen={isImageModalOpen} size="full">
  <div className="relative h-full bg-black">
    <img 
      style={{ transform: `scale(${imageZoom})` }}
      className="max-w-full max-h-full"
    />
    
    {/* Zoom controls */}
    <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2">
      <button onClick={() => setImageZoom(zoom - 0.25)}>
        <ZoomOut />
      </button>
      <span>{Math.round(imageZoom * 100)}%</span>
      <button onClick={() => setImageZoom(zoom + 0.25)}>
        <ZoomIn />
      </button>
    </div>
  </div>
</Modal>
```

### History Timeline
```tsx
{editHistory.map((edit, index) => (
  <div key={edit.id} className="flex gap-3">
    {/* Timeline dot + line */}
    <div className="flex flex-col items-center">
      <div className="w-8 h-8 rounded-full bg-primary-100">
        <User size={16} />
      </div>
      {index < history.length - 1 && (
        <div className="w-0.5 flex-1 bg-gray-200" />
      )}
    </div>
    
    {/* Edit info */}
    <div className="flex-1">
      <p className="font-600">{fieldName} עודכן</p>
      <p>
        <span className="line-through">{oldValue}</span> → 
        <span className="font-500">{newValue}</span>
      </p>
      <p className="text-xs text-gray-500">{timestamp}</p>
    </div>
  </div>
))}
```

---

## 📱 Responsive Breakpoints

```css
Mobile   (<640px):   Single column, stacked actions
Tablet   (640-1024): Two-column grid
Desktop  (>1024px):  Two-column grid, three-column actions
```

---

## ♿ Accessibility

```tsx
// Keyboard navigation
<div 
  onClick={handleClick}
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
  tabIndex={0}
  role="button"
  aria-label="Description"
/>

// ARIA labels for icon buttons
<button aria-label="שתף קבלה">
  <Share2 />
</button>
```

---

## 🎯 Actions Flow

### View Receipt
```
Archive Page → Click Receipt → ReceiptDetail
                ↓
          Load receipt data
                ↓
          Display full details
```

### Download PDF
```
Click "הורד PDF חתום" → Show loading state
         ↓
    Download blob from API
         ↓
    Create download link
         ↓
    Trigger download
         ↓
    Cleanup + hide loading
```

### Delete Receipt
```
Click Delete → Show confirmation
      ↓
  User confirms
      ↓
  Delete via API
      ↓
  Navigate to /archive
```

### View History
```
Click "היסטוריית שינויים" → Load history (if needed)
              ↓
         Open modal
              ↓
      Display timeline
```

---

## 🔌 Service Integration

```typescript
// Get receipt
const receipt = await receiptService.getReceipt(receiptId);

// Get history
const history = await receiptService.getReceiptHistory(receiptId);

// Download PDF
const blob = await receiptService.downloadReceiptPDF(receiptId);

// Delete receipt
await receiptService.deleteReceipt(receiptId);
```

---

## 🎨 Styling Classes

```css
/* Container */
.min-h-screen .bg-gray-50 .pb-20

/* Header */
.sticky .top-0 .z-10 .bg-white .border-b .shadow-sm

/* Amount Card */
.bg-gradient-to-br .from-primary-500 .to-primary-600
.rounded-xl .p-6 .text-white

/* Details Grid */
.grid .grid-cols-1 .md:grid-cols-2 .gap-4

/* Actions */
.grid .grid-cols-1 .md:grid-cols-3 .gap-3
```

---

## 🐛 Error Handling

```typescript
// Receipt not found
try {
  const receipt = await getReceipt(id);
} catch (error) {
  alert('שגיאה בטעינת הקבלה');
  navigate('/archive');
}

// PDF download failed
try {
  const blob = await downloadPDF(id);
} catch (error) {
  alert('שגיאה בהורדת הקובץ');
}

// Delete failed
try {
  await deleteReceipt(id);
} catch (error) {
  alert('שגיאה במחיקת הקבלה');
}
```

---

## 📋 Checklist

- [x] Fetch receipt on mount
- [x] Display all metadata
- [x] Image with hover effect
- [x] Clickable image → zoom modal
- [x] Zoom controls (1x - 3x)
- [x] Category badge with color
- [x] Amount card with gradient
- [x] Details grid (2 columns on desktop)
- [x] Notes section (if exists)
- [x] Download PDF button
- [x] Edit button → navigation
- [x] History button → modal
- [x] Share button (Web Share API)
- [x] Delete button (with confirmation)
- [x] Digital signature badge (if signed)
- [x] Edit history timeline
- [x] Loading states
- [x] Error handling
- [x] Responsive layout
- [x] Accessibility (ARIA, keyboard)
- [x] RTL support

---

## 🚀 Quick Start

```tsx
// 1. Add route
<Route path="/receipts/:id" element={<ReceiptDetail />} />

// 2. Navigate from archive
const navigate = useNavigate();
navigate(`/receipts/${receipt.id}`);

// 3. Component auto-loads data
// 4. User can view, download, edit, delete, share
```

---

## 📚 Related Components

- `ReceiptCard` - List item in archive
- `ReceiptUpload` - Upload new receipt
- `ReceiptProcessing` - OCR processing view
- `ReceiptForm` - Edit receipt data
- `Modal` - Zoom/history modals
- `Button` - All action buttons
- `Card` - Container layouts

---

## 💡 Tips

1. **Image Optimization**: Use proper image formats and sizes
2. **PDF Caching**: Consider caching PDFs after first download
3. **History Lazy Load**: Load history only when modal opens
4. **Share Feature**: Test on both mobile and desktop
5. **Delete Confirmation**: Always confirm destructive actions
6. **Zoom UX**: Smooth transitions, clear controls
7. **Error Messages**: Always in Hebrew, user-friendly

---

## 🎯 Key Metrics

- Load time: < 1s
- Image zoom: 25% increments (1x - 3x)
- PDF download: Progress indicator
- History items: Show all (no pagination)
- Mobile-first: Bottom padding for nav (pb-20)

---

**Component Status**: ✅ Production Ready

**Last Updated**: November 3, 2025
