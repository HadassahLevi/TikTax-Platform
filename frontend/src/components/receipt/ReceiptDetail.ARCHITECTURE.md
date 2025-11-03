# ReceiptDetail Component - Architecture Diagram

## 🏗️ Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        ReceiptDetail                            │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ URL Params (id)                                           │ │
│  └───────────────────────────────────────────────────────────┘ │
│                              ↓                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ useEffect (loadReceipt)                                   │ │
│  │  ├─ receiptService.getReceipt(id)                         │ │
│  │  └─ receiptService.getReceiptHistory(id)                  │ │
│  └───────────────────────────────────────────────────────────┘ │
│                              ↓                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Store (useReceipt)                                        │ │
│  │  ├─ currentReceipt                                        │ │
│  │  ├─ setCurrentReceipt                                     │ │
│  │  └─ deleteReceipt                                         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                              ↓                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Local State                                               │ │
│  │  ├─ isImageModalOpen                                      │ │
│  │  ├─ imageZoom (1.0 - 3.0)                                 │ │
│  │  ├─ showHistory                                           │ │
│  │  ├─ editHistory []                                        │ │
│  │  ├─ isDownloading                                         │ │
│  │  └─ isLoadingHistory                                      │ │
│  └───────────────────────────────────────────────────────────┘ │
│                              ↓                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Render UI                                                 │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎨 UI Component Tree

```
ReceiptDetail
│
├─ Header (sticky)
│  ├─ Button (back to archive)
│  └─ Action buttons
│     ├─ Share button
│     └─ Delete button
│
├─ Main Content (max-w-4xl)
│  │
│  ├─ Receipt Image Card
│  │  └─ Image (clickable → modal)
│  │     └─ Hover overlay (ZoomIn icon)
│  │
│  ├─ Receipt Info Card
│  │  ├─ Header
│  │  │  ├─ Vendor name + date
│  │  │  └─ Category badge
│  │  │
│  │  ├─ Amount Card (gradient)
│  │  │  ├─ Total amount (large)
│  │  │  └─ Pre-VAT / VAT breakdown
│  │  │
│  │  ├─ Details Grid (2 columns)
│  │  │  ├─ Business name
│  │  │  ├─ Business number
│  │  │  ├─ Receipt number
│  │  │  └─ Upload timestamp
│  │  │
│  │  └─ Notes section (conditional)
│  │
│  ├─ Action Buttons Grid
│  │  ├─ Download PDF button
│  │  ├─ Edit button
│  │  └─ View History button
│  │
│  └─ Digital Signature Card (conditional)
│     ├─ Checkmark icon
│     ├─ Signature info
│     └─ Verified status
│
├─ Image Zoom Modal
│  ├─ Full-screen container (black bg)
│  ├─ Scaled image (transform: scale)
│  └─ Zoom controls (bottom center)
│     ├─ Zoom Out button
│     ├─ Current zoom %
│     └─ Zoom In button
│
└─ Edit History Modal
   ├─ Modal header ("היסטוריית שינויים")
   └─ Timeline list
      └─ Edit items (forEach)
         ├─ Timeline dot + line
         └─ Edit details
            ├─ Field name
            ├─ Old → New values
            └─ Timestamp
```

---

## 🔄 Data Flow Diagram

```
┌─────────────┐
│   Browser   │
│   /receipts │
│   /:id      │
└──────┬──────┘
       │
       ↓
┌──────────────────┐
│  ReceiptDetail   │
│  Component       │
└──────┬───────────┘
       │
       ├─→ useParams() ──→ Extract ID
       │
       ├─→ useReceipt() ──→ Store access
       │
       └─→ useEffect() ──→ loadReceipt(id)
                  │
                  ├─→ receiptService.getReceipt(id)
                  │        ↓
                  │   ┌─────────────┐
                  │   │   Backend   │
                  │   │   API       │
                  │   └─────────────┘
                  │        ↓
                  │   setCurrentReceipt(receipt)
                  │
                  └─→ receiptService.getReceiptHistory(id)
                           ↓
                      ┌─────────────┐
                      │   Backend   │
                      │   API       │
                      └─────────────┘
                           ↓
                      setEditHistory(history)
                           ↓
                      ┌─────────────┐
                      │   Render    │
                      │   Receipt   │
                      │   Details   │
                      └─────────────┘
```

---

## 🎬 User Interaction Flows

### 1. View Receipt

```
User clicks receipt in archive
         ↓
Navigate to /receipts/:id
         ↓
Component loads
         ↓
Fetch receipt data
         ↓
Display full details
```

### 2. Zoom Image

```
User clicks receipt image
         ↓
setIsImageModalOpen(true)
         ↓
Modal opens (full-screen)
         ↓
User clicks zoom controls
         ↓
setImageZoom(zoom ± 0.25)
         ↓
Image scales (CSS transform)
         ↓
User clicks X or outside
         ↓
setIsImageModalOpen(false)
setImageZoom(1)
```

### 3. Download PDF

```
User clicks "הורד PDF חתום"
         ↓
setIsDownloading(true)
         ↓
Call receiptService.downloadReceiptPDF(id)
         ↓
Receive Blob from API
         ↓
Create object URL
         ↓
Create download link
         ↓
Trigger download
         ↓
Cleanup (revoke URL)
         ↓
setIsDownloading(false)
```

### 4. Delete Receipt

```
User clicks delete button
         ↓
Show confirmation dialog
         ↓
User confirms
         ↓
Call deleteReceipt(id)
         ↓
API deletes receipt
         ↓
Navigate to /archive
```

### 5. View History

```
User clicks "היסטוריית שינויים"
         ↓
Check if history loaded
         ↓
If not loaded:
  setIsLoadingHistory(true)
  Load from API
  setIsLoadingHistory(false)
         ↓
setShowHistory(true)
         ↓
Modal opens with timeline
         ↓
User clicks X or outside
         ↓
setShowHistory(false)
```

### 6. Share Receipt

```
User clicks share button
         ↓
Check if navigator.share exists
         ↓
If YES (mobile):
  ├─ Call navigator.share()
  ├─ Show native share sheet
  └─ User selects app/action
         ↓
If NO (desktop):
  ├─ Call navigator.clipboard.writeText()
  ├─ Copy URL to clipboard
  └─ Show alert "הקישור הועתק ללוח"
```

---

## 🔌 Service Integration Flow

```
ReceiptDetail Component
         │
         ├─→ receiptService.getReceipt(id)
         │        ↓
         │   GET /receipts/:id
         │        ↓
         │   Returns Receipt object
         │        ↓
         │   setCurrentReceipt(receipt)
         │
         ├─→ receiptService.getReceiptHistory(id)
         │        ↓
         │   GET /receipts/:id/history
         │        ↓
         │   Returns ReceiptEdit[]
         │        ↓
         │   setEditHistory(history)
         │
         ├─→ receiptService.downloadReceiptPDF(id)
         │        ↓
         │   GET /receipts/:id/pdf
         │        ↓
         │   Returns Blob
         │        ↓
         │   Create download link
         │
         └─→ deleteReceipt(id)
                  ↓
             DELETE /receipts/:id
                  ↓
             Receipt deleted
                  ↓
             Navigate to /archive
```

---

## 📊 State Management Flow

```
Initial State:
├─ currentReceipt: null
├─ isImageModalOpen: false
├─ imageZoom: 1
├─ showHistory: false
├─ editHistory: []
├─ isDownloading: false
└─ isLoadingHistory: false

↓ (after loadReceipt)

Loaded State:
├─ currentReceipt: Receipt object
├─ editHistory: ReceiptEdit[]
└─ (other states unchanged)

↓ (user interactions)

Active States:
├─ isImageModalOpen: true (when viewing image)
├─ imageZoom: 1.0 - 3.0 (when zooming)
├─ showHistory: true (when viewing history)
├─ isDownloading: true (when downloading PDF)
└─ isLoadingHistory: true (when loading history)
```

---

## 🎨 Styling Architecture

```
Component Styling
│
├─ Tailwind Utility Classes
│  ├─ Layout: flex, grid, max-w-4xl
│  ├─ Spacing: p-4, py-6, gap-3
│  ├─ Colors: bg-white, text-gray-900
│  ├─ Borders: border-b, rounded-lg
│  └─ Responsive: md:grid-cols-2
│
├─ Dynamic Inline Styles
│  ├─ Category color: backgroundColor, color
│  └─ Image zoom: transform: scale()
│
└─ Conditional Classes
   ├─ Disabled states: opacity-50
   ├─ Hover states: hover:bg-gray-100
   └─ Focus states: focus:ring-2
```

---

## 🔐 Security Flow

```
User Action
     ↓
Component validates input
     ↓
API call via axios client
     ↓
Interceptor adds auth token
     ↓
Backend validates token
     ↓
Backend authorizes action
     ↓
Response returned
     ↓
Component handles result
```

---

## ♿ Accessibility Tree

```
ReceiptDetail (main)
│
├─ Header (sticky navigation)
│  ├─ Button [role=button, aria-label="חזור לארכיון"]
│  ├─ Button [role=button, aria-label="שתף קבלה"]
│  └─ Button [role=button, aria-label="מחק קבלה"]
│
├─ Image Preview [role=button, tabindex=0, aria-label="הצג תמונה מוגדלת"]
│
├─ Receipt Info Card
│  ├─ Heading (vendor name)
│  ├─ Text (date, amounts, details)
│  └─ Region (notes, if exists)
│
├─ Action Buttons
│  ├─ Button [disabled when no PDF]
│  ├─ Button [always enabled]
│  └─ Button [disabled when no history]
│
├─ Modal (image zoom) [role=dialog, aria-modal=true]
│  ├─ Image [alt="תמונת קבלה מוגדלת"]
│  └─ Controls
│     ├─ Button [aria-label="הקטן"]
│     ├─ Text (zoom percentage)
│     └─ Button [aria-label="הגדל"]
│
└─ Modal (edit history) [role=dialog, aria-modal=true]
   ├─ Heading (modal title)
   └─ List (timeline)
      └─ Items (edit history entries)
```

---

## 📱 Responsive Breakpoints Flow

```
Screen Width
     │
     ├─ < 640px (Mobile)
     │  ├─ Single column layout
     │  ├─ Full-width buttons
     │  ├─ Stacked details
     │  └─ Bottom padding: 80px
     │
     ├─ 640px - 1024px (Tablet)
     │  ├─ Two-column details grid
     │  ├─ Three-column buttons
     │  └─ Max width: 896px
     │
     └─ > 1024px (Desktop)
        ├─ Two-column details grid
        ├─ Three-column buttons
        ├─ Hover effects active
        └─ Max width: 896px
```

---

## 🚀 Performance Optimization Flow

```
Component Mount
     │
     ├─→ Load receipt (immediate)
     │
     ├─→ Load image (lazy)
     │
     └─→ Defer history (on modal open)

User Interaction
     │
     ├─→ Zoom controls (CSS transform - GPU accelerated)
     │
     ├─→ Modal animations (optimized transitions)
     │
     └─→ Scroll handling (passive listeners)

Cleanup
     │
     ├─→ Revoke object URLs
     │
     ├─→ Clear state on unmount
     │
     └─→ Cancel pending requests
```

---

## 🧩 Component Dependencies

```
ReceiptDetail
     │
     ├─→ React (useState, useEffect)
     ├─→ React Router (useParams, useNavigate)
     │
     ├─→ UI Components
     │   ├─ Button
     │   ├─ Card
     │   └─ Modal
     │
     ├─→ Icons (lucide-react)
     │   ├─ ArrowLeft, Download, Trash2, Share2
     │   ├─ Edit2, History, Calendar
     │   ├─ Building2, Hash, FileText, Tag
     │   ├─ Clock, User, ZoomIn, ZoomOut
     │   └─ CheckCircle
     │
     ├─→ Hooks
     │   └─ useReceipt
     │
     ├─→ Services
     │   └─ receiptService
     │
     └─→ Types & Utils
         ├─ Receipt, ReceiptEdit
         ├─ formatAmount
         ├─ formatDateIL
         └─ DEFAULT_CATEGORIES
```

---

## 🎯 Error Handling Flow

```
API Call
     │
     ├─→ Success
     │   └─→ Update state
     │       └─→ Render UI
     │
     └─→ Error
         │
         ├─→ Receipt not found
         │   ├─ Console error
         │   ├─ Alert user
         │   └─ Navigate to /archive
         │
         ├─→ PDF download failed
         │   ├─ Console error
         │   ├─ Alert user
         │   └─ Reset loading state
         │
         ├─→ Delete failed
         │   ├─ Console error
         │   ├─ Alert user
         │   └─ Stay on page
         │
         └─→ Network error
             ├─ Axios interceptor
             ├─ Generic error message
             └─ User can retry
```

---

This architecture ensures the ReceiptDetail component is:
- ✅ Well-structured
- ✅ Easy to understand
- ✅ Maintainable
- ✅ Scalable
- ✅ Type-safe
- ✅ Accessible
- ✅ Performant
