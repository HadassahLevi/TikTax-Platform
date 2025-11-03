# ReceiptDetail Component - Complete Documentation

## Overview

The `ReceiptDetail` component provides a comprehensive, detailed view of individual receipt records in the Tik-Tax archive. It displays complete receipt metadata, original image with zoom functionality, edit history timeline, and provides actions for downloading PDFs, editing, sharing, and deletion.

---

## Features

### ✅ Core Features
- **Full Receipt Information Display** - All metadata with professional layout
- **Image Preview with Zoom Modal** - Full-screen view with 100%-300% zoom
- **Edit History Timeline** - Visual timeline of all changes
- **PDF Download** - Download digitally signed PDF receipts
- **Delete with Confirmation** - Safe deletion with user confirmation
- **Share Functionality** - Web Share API with clipboard fallback
- **Category Badge** - Color-coded category display
- **Digital Signature Badge** - Shows verification status

### 🎨 Design Features
- Clean header with back navigation
- Large, clickable image with hover effect
- Gradient amount display (prominent)
- Icon-based information grid
- Responsive layout (mobile-first)
- Action buttons row
- Full-screen image modal
- Timeline-style history display

---

## File Location

```
/src/components/receipt/ReceiptDetail.tsx
```

---

## Usage

### Basic Usage (with React Router)

```tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ReceiptDetail } from '@/components/receipt';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/receipts/:id" element={<ReceiptDetail />} />
      </Routes>
    </BrowserRouter>
  );
}
```

### Navigation to Receipt Detail

```tsx
import { useNavigate } from 'react-router-dom';

function ArchivePage() {
  const navigate = useNavigate();
  
  const handleViewReceipt = (receiptId: string) => {
    navigate(`/receipts/${receiptId}`);
  };
  
  return (
    <div>
      {receipts.map(receipt => (
        <div key={receipt.id} onClick={() => handleViewReceipt(receipt.id)}>
          {receipt.vendorName}
        </div>
      ))}
    </div>
  );
}
```

---

## Component Structure

### State Management

```typescript
// Image zoom modal
const [isImageModalOpen, setIsImageModalOpen] = useState(false);
const [imageZoom, setImageZoom] = useState(1);

// History modal
const [showHistory, setShowHistory] = useState(false);
const [editHistory, setEditHistory] = useState<ReceiptEdit[]>([]);

// Loading states
const [isDownloading, setIsDownloading] = useState(false);
const [isLoadingHistory, setIsLoadingHistory] = useState(false);
```

### Main Sections

1. **Header** - Back button + share/delete actions
2. **Receipt Image** - Clickable preview with zoom modal
3. **Receipt Info Card** - Vendor, date, category, amounts
4. **Details Grid** - Business info, receipt number, timestamps
5. **Action Buttons** - Download PDF, Edit, View History
6. **Digital Signature Badge** - Verification indicator (if signed)
7. **Image Zoom Modal** - Full-screen with zoom controls
8. **Edit History Modal** - Timeline of changes

---

## Props

### Component Props

The component receives no direct props. It uses:

- **URL Params**: `id` from React Router (receipt ID)
- **Store State**: `currentReceipt` from `useReceipt()` hook

---

## Key Functions

### loadReceipt(receiptId: string)

Loads receipt data and edit history from API.

```typescript
const loadReceipt = async (receiptId: string) => {
  // 1. Fetch receipt by ID
  const receipt = await receiptService.getReceipt(receiptId);
  setCurrentReceipt(receipt);
  
  // 2. Load edit history
  const history = await receiptService.getReceiptHistory(receiptId);
  setEditHistory(history || []);
};
```

### handleDelete()

Deletes receipt with user confirmation.

```typescript
const handleDelete = async () => {
  const confirmed = window.confirm(
    'האם אתה בטוח שברצונך למחוק קבלה זו?'
  );
  
  if (confirmed) {
    await deleteReceipt(currentReceipt.id);
    navigate('/archive');
  }
};
```

### handleDownloadPDF()

Downloads digitally signed PDF receipt.

```typescript
const handleDownloadPDF = async () => {
  // 1. Get PDF blob from API
  const blob = await receiptService.downloadReceiptPDF(currentReceipt.id);
  
  // 2. Create download link
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `קבלה-${vendorName}-${date}.pdf`;
  link.click();
  
  // 3. Cleanup
  window.URL.revokeObjectURL(url);
};
```

### handleShare()

Shares receipt via Web Share API or clipboard.

```typescript
const handleShare = async () => {
  if (navigator.share) {
    // Native share (mobile)
    await navigator.share({
      title: `קבלה - ${vendorName}`,
      text: `קבלה מ-${vendorName} בסך ${amount}`,
      url: window.location.href
    });
  } else {
    // Fallback: Copy to clipboard
    await navigator.clipboard.writeText(window.location.href);
    alert('הקישור הועתק ללוח');
  }
};
```

---

## Receipt Data Display

### Amount Section (Gradient Card)

```tsx
<div className="bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl p-6 text-white">
  <p className="text-sm opacity-90">סכום כולל</p>
  <p className="text-4xl font-700">{formatAmount(totalAmount)}</p>
  
  <div className="flex justify-between">
    <div>
      <p className="opacity-75">לפני מע"מ</p>
      <p className="font-600">{formatAmount(preVatAmount)}</p>
    </div>
    <div>
      <p className="opacity-75">מע"מ (18%)</p>
      <p className="font-600">{formatAmount(vatAmount)}</p>
    </div>
  </div>
</div>
```

### Details Grid

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
  {/* Business Name */}
  <DetailItem icon={<Building2 />} label="עסק" value={vendorName} />
  
  {/* Business Number */}
  <DetailItem icon={<Hash />} label="מספר עסק" value={businessNumber} />
  
  {/* Receipt Number */}
  <DetailItem icon={<FileText />} label="מספר קבלה" value={receiptNumber} />
  
  {/* Upload Time */}
  <DetailItem icon={<Clock />} label="הועלה ב" value={uploadDate} />
</div>
```

---

## Image Zoom Modal

### Features
- Full-screen black background
- Image scaling: 100% - 300%
- Zoom controls at bottom center
- Close button (X) at top-right
- Smooth zoom transitions

### Zoom Controls

```tsx
<div className="absolute bottom-8 left-1/2 transform -translate-x-1/2">
  <div className="flex gap-3 bg-white rounded-full px-4 py-2 shadow-lg">
    {/* Zoom Out */}
    <button 
      onClick={() => setImageZoom(Math.max(1, imageZoom - 0.25))}
      disabled={imageZoom <= 1}
    >
      <ZoomOut size={24} />
    </button>
    
    {/* Current Zoom */}
    <span className="px-4 py-2 font-600">
      {Math.round(imageZoom * 100)}%
    </span>
    
    {/* Zoom In */}
    <button 
      onClick={() => setImageZoom(Math.min(3, imageZoom + 0.25))}
      disabled={imageZoom >= 3}
    >
      <ZoomIn size={24} />
    </button>
  </div>
</div>
```

---

## Edit History Timeline

### Structure

```tsx
{editHistory.map((edit, index) => (
  <div key={edit.id} className="flex gap-3">
    {/* Timeline dot */}
    <div className="flex flex-col items-center">
      <div className="w-8 h-8 rounded-full bg-primary-100">
        <User size={16} className="text-primary-600" />
      </div>
      {index < editHistory.length - 1 && (
        <div className="w-0.5 flex-1 bg-gray-200" />
      )}
    </div>
    
    {/* Edit details */}
    <div className="flex-1">
      <p className="font-600">{fieldName} עודכן</p>
      <p className="text-gray-600">
        <span className="line-through">{oldValue}</span> → 
        <span className="font-500">{newValue}</span>
      </p>
      <p className="text-xs text-gray-500">{timestamp}</p>
    </div>
  </div>
))}
```

### Field Name Translation

```typescript
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
```

---

## Digital Signature Badge

### Display Logic

```tsx
{currentReceipt.digitalSignature && currentReceipt.signedAt && (
  <Card shadow="sm" padding="md">
    <div className="flex items-center gap-3">
      {/* Icon */}
      <div className="w-12 h-12 rounded-full bg-green-100">
        <CheckCircle size={24} className="text-green-600" />
      </div>
      
      {/* Info */}
      <div className="flex-1">
        <p className="font-600">חתימה דיגיטלית</p>
        <p className="text-sm text-gray-600">
          נחתם ב-{formatDate(signedAt)}
        </p>
      </div>
      
      {/* Status */}
      <div className="text-green-600 font-600">
        <CheckCircle size={16} /> מאומת
      </div>
    </div>
  </Card>
)}
```

---

## Action Buttons

### Download PDF

```tsx
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
```

**States:**
- Disabled if no PDF available
- Loading state while downloading
- Shows spinner during download

### Edit Receipt

```tsx
<Button
  variant="secondary"
  fullWidth
  onClick={() => navigate(`/receipts/${id}/edit`)}
  icon={<Edit2 size={20} />}
>
  ערוך פרטים
</Button>
```

**Behavior:**
- Navigates to edit page
- Always enabled

### View History

```tsx
<Button
  variant="secondary"
  fullWidth
  onClick={() => setShowHistory(true)}
  icon={<History size={20} />}
  disabled={editHistory.length === 0}
>
  היסטוריית שינויים
</Button>
```

**States:**
- Disabled if no edit history
- Opens modal when clicked

---

## Loading States

### Initial Loading

```tsx
if (!currentReceipt) {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <div className="w-12 h-12 border-4 border-primary-500 
                        border-t-transparent rounded-full animate-spin" />
        <p className="text-gray-600">טוען קבלה...</p>
      </div>
    </div>
  );
}
```

### History Loading

```tsx
{isLoadingHistory ? (
  <div className="text-center py-8">
    <div className="w-8 h-8 border-4 border-primary-500 
                    border-t-transparent rounded-full animate-spin" />
    <p className="text-gray-600">טוען היסטוריה...</p>
  </div>
) : /* ... show history */ }
```

### PDF Download Loading

```tsx
<Button
  loading={isDownloading}
  disabled={isDownloading}
>
  {isDownloading ? 'מוריד...' : 'הורד PDF חתום'}
</Button>
```

---

## Responsive Design

### Mobile (< 640px)

```css
- Single column layout
- Full-width action buttons
- Stacked detail items
- Bottom spacing for navigation (pb-20)
- Touch-friendly targets (min 44px)
```

### Tablet (640px - 1024px)

```css
- Two-column details grid
- Max width: 4xl (896px)
- Horizontal padding: 24px
```

### Desktop (> 1024px)

```css
- Two-column details grid
- Max width: 4xl (896px)
- Three-column action buttons
- Hover effects enabled
```

---

## Error Handling

### Receipt Not Found

```typescript
const loadReceipt = async (receiptId: string) => {
  try {
    const receipt = await receiptService.getReceipt(receiptId);
    setCurrentReceipt(receipt);
  } catch (error) {
    console.error('Failed to load receipt:', error);
    alert('שגיאה בטעינת הקבלה');
    navigate('/archive'); // Redirect back
  }
};
```

### PDF Download Error

```typescript
try {
  const blob = await receiptService.downloadReceiptPDF(id);
  // ... download logic
} catch (error) {
  alert('שגיאה בהורדת הקובץ');
  console.error('PDF download error:', error);
}
```

### Delete Error

```typescript
try {
  await deleteReceipt(currentReceipt.id);
  navigate('/archive');
} catch (error) {
  alert('שגיאה במחיקת הקבלה');
}
```

---

## Accessibility Features

### Keyboard Navigation

```tsx
// Image click with keyboard
<div 
  onClick={() => setIsImageModalOpen(true)}
  onKeyDown={(e) => e.key === 'Enter' && setIsImageModalOpen(true)}
  tabIndex={0}
  role="button"
  aria-label="הצג תמונה מוגדלת"
>
```

### ARIA Labels

```tsx
<button aria-label="שתף קבלה">
  <Share2 />
</button>

<button aria-label="מחק קבלה">
  <Trash2 />
</button>

<button aria-label="הקטן">
  <ZoomOut />
</button>
```

### Screen Reader Support

- Semantic HTML (header, main, buttons)
- Alt text for images
- ARIA labels for icon-only buttons
- Role attributes where needed

---

## Integration with Stores

### useReceipt Hook

```typescript
const { 
  currentReceipt,      // Current receipt data
  setCurrentReceipt,   // Set current receipt
  deleteReceipt        // Delete receipt action
} = useReceipt();
```

### Receipt Service

```typescript
import * as receiptService from '@/services/receipt.service';

// Get receipt by ID
const receipt = await receiptService.getReceipt(receiptId);

// Get edit history
const history = await receiptService.getReceiptHistory(receiptId);

// Download PDF
const blob = await receiptService.downloadReceiptPDF(receiptId);
```

---

## Styling Classes

### Container

```css
.min-h-screen     /* Full viewport height */
.bg-gray-50       /* Light gray background */
.pb-20            /* Bottom padding for mobile nav */
```

### Header (Sticky)

```css
.sticky           /* Sticks to top on scroll */
.top-0            /* Position at top */
.z-10             /* Above other content */
.bg-white         /* White background */
.border-b         /* Bottom border */
.shadow-sm        /* Subtle shadow */
```

### Amount Card (Gradient)

```css
.bg-gradient-to-br       /* Gradient direction */
.from-primary-500        /* Start color */
.to-primary-600          /* End color */
.rounded-xl              /* Large border radius */
.p-6                     /* Padding */
.text-white              /* White text */
```

### Detail Items

```css
.flex .items-start .gap-3    /* Flexbox layout */
.w-10 .h-10                  /* Icon container size */
.rounded-lg                  /* Rounded corners */
.bg-gray-100                 /* Light background */
```

---

## Performance Optimizations

### Lazy Loading

```typescript
// Load history only when modal opens
const [showHistory, setShowHistory] = useState(false);

useEffect(() => {
  if (showHistory && editHistory.length === 0) {
    loadEditHistory();
  }
}, [showHistory]);
```

### Image Optimization

```typescript
// Use responsive images
<img 
  src={currentReceipt.imageUrl}
  loading="lazy"  // Browser lazy loading
  alt="תמונת קבלה"
/>
```

### Cleanup

```typescript
// Cleanup object URLs after download
window.URL.revokeObjectURL(url);
```

---

## Testing Scenarios

### Unit Tests

```typescript
describe('ReceiptDetail', () => {
  it('loads receipt on mount', async () => {
    render(<ReceiptDetail />);
    expect(await screen.findByText('עסק')).toBeInTheDocument();
  });
  
  it('opens image modal on click', () => {
    render(<ReceiptDetail />);
    fireEvent.click(screen.getByAltText('תמונת קבלה'));
    expect(screen.getByRole('dialog')).toBeInTheDocument();
  });
  
  it('downloads PDF on button click', async () => {
    render(<ReceiptDetail />);
    const downloadBtn = screen.getByText('הורד PDF חתום');
    fireEvent.click(downloadBtn);
    expect(mockDownloadPDF).toHaveBeenCalled();
  });
});
```

### Integration Tests

```typescript
it('deletes receipt and navigates to archive', async () => {
  render(<ReceiptDetail />);
  
  const deleteBtn = screen.getByLabelText('מחק קבלה');
  fireEvent.click(deleteBtn);
  
  // Confirm dialog
  window.confirm = jest.fn(() => true);
  
  await waitFor(() => {
    expect(mockNavigate).toHaveBeenCalledWith('/archive');
  });
});
```

---

## Common Issues & Solutions

### Issue: Image not loading

```typescript
// Check if imageUrl exists and is valid
{currentReceipt.imageUrl ? (
  <img src={currentReceipt.imageUrl} alt="Receipt" />
) : (
  <div className="bg-gray-200 h-64 flex items-center justify-center">
    <p>תמונה לא זמינה</p>
  </div>
)}
```

### Issue: PDF download fails

```typescript
// Add timeout and better error handling
try {
  const blob = await receiptService.downloadReceiptPDF(id);
  if (!blob || blob.size === 0) {
    throw new Error('Empty PDF response');
  }
  // ... download logic
} catch (error) {
  if (error.code === 'ECONNABORTED') {
    alert('הורדת הקובץ נכשלה - נסה שוב');
  } else {
    alert('שגיאה בהורדת הקובץ');
  }
}
```

### Issue: History not loading

```typescript
// Graceful fallback
const history = await receiptService.getReceiptHistory(receiptId);
setEditHistory(history || []);  // Default to empty array

// Or use receipt's embedded history
setEditHistory(receipt.editHistory || []);
```

---

## Future Enhancements

1. **Print View** - Dedicated print layout
2. **Export Options** - Export as JSON, CSV
3. **Annotation Tool** - Add notes to specific parts of image
4. **Related Receipts** - Show similar receipts from same vendor
5. **Quick Edit** - Inline editing without navigation
6. **Duplicate Warning** - Show if similar receipt exists
7. **Tags Management** - Add/remove tags inline
8. **Comparison View** - Compare with original OCR data

---

## Dependencies

```json
{
  "react": "^18.2.0",
  "react-router-dom": "^6.0.0",
  "lucide-react": "^0.294.0",
  "@/components/ui/Button": "local",
  "@/components/ui/Card": "local",
  "@/components/ui/Modal": "local",
  "@/hooks/useReceipt": "local",
  "@/services/receipt.service": "local",
  "@/types/receipt.types": "local"
}
```

---

## Summary

The `ReceiptDetail` component is a fully-featured, professional receipt viewing interface that provides:

✅ Complete receipt metadata display  
✅ Interactive image zoom  
✅ Edit history tracking  
✅ PDF download with digital signature  
✅ Safe deletion with confirmation  
✅ Native sharing capabilities  
✅ Responsive mobile-first design  
✅ Accessibility compliance  
✅ Error handling and loading states  
✅ Professional Hebrew UI

Perfect for the Tik-Tax archive and receipt management system! 🚀
