# Receipt Types - Quick Reference

Fast lookup guide for Tik-Tax receipt type system.

---

## 🚀 Quick Imports

```typescript
// Types
import type {
  Receipt, ReceiptStatus, ExpenseCategory, OCRData,
  ReceiptFilterOptions, ReceiptStatistics
} from '@/types';

// Constants & Helpers
import {
  DEFAULT_CATEGORIES, ISRAELI_VAT_RATE,
  isValidBusinessNumber, calculateVat, formatAmount
} from '@/types';
```

---

## 📊 Status Flow

```
processing → review → approved
                  ↓
              duplicate
                  ↓
               failed
```

---

## 🎨 Category Colors

| Category | Hebrew | Color |
|----------|--------|-------|
| Office Supplies | ציוד משרדי | 🔵 #3B82F6 |
| Professional Services | שירותים מקצועיים | 🟣 #8B5CF6 |
| Marketing | שיווק ופרסום | 🔴 #EF4444 |
| Travel | נסיעות ותחבורה | 🟢 #10B981 |
| Meals | אירוח ואוכל | 🟡 #F59E0B |
| Rent | שכירות | 🔵 #6366F1 |
| Equipment | ציוד וטכנולוגיה | 🔵 #06B6D4 |
| Maintenance | תחזוקה | 🟢 #84CC16 |
| Insurance | ביטוח | 🟦 #14B8A6 |
| Bank Fees | עמלות | 🟣 #A855F7 |
| Education | הדרכה | 🩷 #EC4899 |
| Subscriptions | מנויים | 🟠 #F97316 |
| Other | אחר | ⚫ #6B7280 |

---

## ✅ Validation Cheatsheet

```typescript
// Business number (9 digits)
isValidBusinessNumber('514932221')  ✅
isValidBusinessNumber('12345')      ❌

// Date formats
isValidReceiptDate('15/03/2025')    ✅ DD/MM/YYYY
isValidReceiptDate('2025-03-15')    ✅ ISO
isValidReceiptDate('03/15/2025')    ❌

// Amount
isValidAmount(100)   ✅
isValidAmount(0)     ❌
isValidAmount(-50)   ❌

// VAT (18%, ₪1 tolerance)
isVatValid(118, 18)      ✅
isVatValid(118, 18.50)   ✅
isVatValid(118, 20)      ❌
```

---

## 💰 VAT Formulas

```typescript
// Israeli VAT = 18%
total = preVat * 1.18
vat = total - preVat
preVat = total / 1.18

// Examples
calculatePreVat(118)  // 100.00
calculateVat(118)     // 18.00
```

---

## 🔍 Confidence Levels

| Level | Range | Color | Action |
|-------|-------|-------|--------|
| `high` | 90%+ | 🟢 Green | Auto-approve safe |
| `medium` | 70-89% | 🟡 Yellow | Review recommended |
| `low` | <70% | 🔴 Red | Manual verification required |

---

## 📋 Common Filter Examples

```typescript
// This month's receipts
const filters: ReceiptFilterOptions = {
  startDate: '2025-11-01',
  endDate: '2025-11-30',
  status: ['approved']
};

// Office expenses over ₪500
const filters: ReceiptFilterOptions = {
  categoryIds: ['office-supplies', 'equipment'],
  minAmount: 500
};

// Search by vendor
const filters: ReceiptFilterOptions = {
  searchQuery: 'סופר פארם'  // SuperPharm
};
```

---

## 📊 Statistics Quick Access

```typescript
interface ReceiptStatistics {
  totalReceipts: number;      // Count
  totalAmount: number;        // ₪
  totalVat: number;          // ₪
  thisMonth: { count, amount };
  lastMonth: { count, amount };
  byCategory: [{
    categoryId,
    category,
    count,
    amount,
    percentage
  }];
  recentReceipts: Receipt[];
}
```

---

## 📤 Export Formats

```typescript
format: 'excel' | 'pdf' | 'csv'
```

---

## 🔢 Constants

```typescript
ISRAELI_VAT_RATE = 0.18              // 18%
MAX_FILE_SIZE = 10485760             // 10MB
ALLOWED_FILE_TYPES = ['image/jpeg', 'image/png', 'application/pdf']
MAX_IMAGE_DIMENSION = 4096           // pixels
OCR_TIMEOUT_MS = 60000               // 60s
PROCESSING_POLL_INTERVAL = 2000      // 2s
```

---

## 🎯 Most Common Types

### Receipt (main entity)
```typescript
{
  id, userId, imageUrl, vendorName, businessNumber,
  date, totalAmount, vatAmount, categoryId,
  status, confidence, createdAt
}
```

### OCRData (extraction)
```typescript
{
  vendorName, businessNumber, date,
  totalAmount, vatAmount, receiptNumber,
  confidence: { overall, vendorName, ... }
}
```

### ExpenseCategory
```typescript
{
  id, nameHe, nameEn, icon, color, sortOrder
}
```

---

## 💡 Pro Tips

1. **Always validate** business numbers, dates, and amounts
2. **Use confidence scores** to guide user review
3. **Check VAT** calculations (18% with ₪1 tolerance)
4. **Format for display**: `formatAmount()`, `formatDateIL()`
5. **Filter smartly**: Combine filters with AND logic
6. **Categories**: Use `DEFAULT_CATEGORIES` constant
7. **Dates**: Store ISO, display DD/MM/YYYY

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Type not found | Check import from `@/types` |
| Validation fails | Use helper functions |
| Wrong date format | Use `formatDateIL()` |
| VAT mismatch | Allow ₪1 tolerance |
| Category not found | Check `DEFAULT_CATEGORIES` |

---

## 📱 Mobile Considerations

- File size limit: **10MB**
- Image max dimension: **4096px**
- OCR timeout: **60 seconds**
- Poll interval: **2 seconds**

---

**File**: `/src/types/receipt.types.ts`  
**Docs**: `/src/types/RECEIPT_TYPES.md`  
**Updated**: November 2, 2025
