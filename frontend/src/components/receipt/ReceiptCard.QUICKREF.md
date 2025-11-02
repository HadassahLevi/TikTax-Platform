# ReceiptCard Component - Quick Reference

## Import
```typescript
import { ReceiptCard } from '@/components/receipt';
```

## Props
```typescript
interface ReceiptCardProps {
  receipt: Receipt;                        // Required
  onClick?: (receipt: Receipt) => void;
  selected?: boolean;                      // Default: false
  className?: string;
}
```

## Receipt Type
```typescript
interface Receipt {
  id: string;
  userId: string;
  businessName: string;
  amount: number;
  currency: string;
  date: string;                           // ISO 8601
  category: ReceiptCategory;
  status: ReceiptStatus;
  imageUrl: string;
  ocrData: OCRData;
  verified: boolean;
  createdAt: string;
  updatedAt: string;
}

type ReceiptStatus = 'pending' | 'processing' | 'completed' | 'failed';
```

## Basic Usage
```tsx
<ReceiptCard
  receipt={receiptData}
  onClick={(receipt) => viewDetails(receipt)}
/>
```

## Grid Layout
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {receipts.map((receipt) => (
    <ReceiptCard
      key={receipt.id}
      receipt={receipt}
      onClick={handleReceiptClick}
    />
  ))}
</div>
```

## Selected State
```tsx
<ReceiptCard
  receipt={receipt}
  selected={selectedId === receipt.id}
  onClick={handleSelect}
/>
```

## Archive Page Example
```tsx
const ArchivePage = () => {
  const [selectedReceipt, setSelectedReceipt] = useState<string | null>(null);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {receipts.map((receipt) => (
        <ReceiptCard
          key={receipt.id}
          receipt={receipt}
          selected={selectedReceipt === receipt.id}
          onClick={(r) => setSelectedReceipt(r.id)}
        />
      ))}
    </div>
  );
};
```

## Visual Elements

### Status Indicators
- **Pending**: Yellow clock icon (ממתין)
- **Processing**: Blue clock icon (בעיבוד)
- **Completed**: Green checkmark (הושלם)
- **Failed**: Red X circle (נכשל)

### Category Badges
Displays category with color-coded badge:
- Office Supplies (ציוד משרדי) - Blue
- Utilities (חשמל ומים) - Yellow
- Travel (נסיעות) - Indigo
- etc.

### Verified Badge
Green badge with checkmark when `receipt.verified === true`

### Low Confidence Warning
Amber alert when `receipt.ocrData.confidence < 0.8`

## Card Structure
```
┌─────────────────────────┐
│ [Image 16:9]            │ ← Receipt image
│   [Status] [✓ Verified] │ ← Top badges
├─────────────────────────┤
│ Business Name           │ ← Bold, truncated
│ ₪1,234.56      12/10/24 │ ← Amount + Date
│ [Category]     [Status] │ ← Badge + Status
│ [⚠ Requires Verify]     │ ← Warning (if needed)
└─────────────────────────┘
```

## Hover Effects
- Image scales to 105%
- Card lifts up 2px
- Shadow increases
- Business name changes to primary color
- Smooth transitions (0.3s for image, 0.2s for card)

## Accessibility
- Keyboard navigable
- Focus ring on keyboard focus
- Image alt text: "קבלה מ-{businessName}"
- Title attribute on truncated text
- Semantic HTML structure

## Responsive Behavior
```tsx
// Mobile: 1 column
<div className="grid grid-cols-1 gap-4">

// Tablet: 2 columns
<div className="grid grid-cols-1 md:grid-cols-2 gap-4">

// Desktop: 3 columns
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
```

## Currency & Date Formatting
- Uses `formatCurrency()` from utils
- Uses `formatDate()` from utils
- Numbers displayed LTR (dir="ltr")
- Monospace font for amounts
