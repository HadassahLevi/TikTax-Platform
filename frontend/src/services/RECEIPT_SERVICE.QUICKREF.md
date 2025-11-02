# Receipt Service - Quick Reference

## Import
```typescript
import { uploadReceipt, getReceipts, approveReceipt } from '@/services/receipt.service';
```

---

## Common Operations

### 1️⃣ Upload Receipt
```typescript
const { receiptId } = await uploadReceipt(file);
```

### 2️⃣ Check Processing
```typescript
const status = await checkProcessingStatus(receiptId);
if (status.status === 'completed') {
  console.log(status.extractedData);
}
```

### 3️⃣ Get Receipt
```typescript
const receipt = await getReceipt(receiptId);
```

### 4️⃣ Update Receipt
```typescript
const updated = await updateReceipt(receiptId, {
  vendorName: 'רמי לוי',
  totalAmount: 125.50
});
```

### 5️⃣ Approve Receipt
```typescript
const approved = await approveReceipt(receiptId, finalData);
// Returns receipt with digital signature
```

### 6️⃣ Check Duplicate
```typescript
const check = await checkDuplicate('רמי לוי', '2024-01-15', 125.50);
if (check.isDuplicate) {
  // Handle duplicate
}
```

### 7️⃣ Get List with Filters
```typescript
const receipts = await getReceipts(
  { status: ['pending'], category: 'groceries' },
  { field: 'date', order: 'desc' },
  1,
  20
);
```

### 8️⃣ Search
```typescript
const results = await searchReceipts('רמי לוי');
```

### 9️⃣ Get Statistics
```typescript
const stats = await getReceiptStatistics();
console.log(stats.totalAmount);
```

### 🔟 Export
```typescript
const { downloadUrl } = await exportReceipts({
  format: 'excel',
  filters: { dateFrom: '2024-01-01' }
});
window.location.href = downloadUrl;
```

### 1️⃣1️⃣ Download PDF
```typescript
const blob = await downloadReceiptPDF(receiptId);
const url = URL.createObjectURL(blob);
window.open(url);
```

### 1️⃣2️⃣ Delete
```typescript
await deleteReceipt(receiptId);
```

---

## Filter Options
```typescript
{
  status?: ['pending' | 'approved' | 'failed'][];
  category?: string;
  dateFrom?: 'YYYY-MM-DD';
  dateTo?: 'YYYY-MM-DD';
  amountMin?: number;
  amountMax?: number;
  vendorName?: string;
}
```

---

## Error Handling
```typescript
try {
  await uploadReceipt(file);
} catch (error) {
  toast.error(error.message); // Hebrew message
}
```

---

## Complete Upload Flow
```typescript
// 1. Upload
const { receiptId } = await uploadReceipt(file);

// 2. Poll status
const interval = setInterval(async () => {
  const status = await checkProcessingStatus(receiptId);
  
  if (status.status === 'completed') {
    clearInterval(interval);
    
    // 3. Check duplicate
    const dup = await checkDuplicate(
      status.extractedData.vendorName,
      status.extractedData.date,
      status.extractedData.totalAmount
    );
    
    if (!dup.isDuplicate) {
      // 4. Show review screen
    }
  }
}, 2000);
```

---

## All Functions

| Function | Purpose |
|----------|---------|
| `uploadReceipt(file)` | Upload receipt image |
| `checkProcessingStatus(id)` | Check OCR status |
| `retryProcessing(id)` | Retry failed OCR |
| `getReceipt(id)` | Get receipt by ID |
| `updateReceipt(id, data)` | Update receipt data |
| `approveReceipt(id, data)` | Approve & archive |
| `deleteReceipt(id)` | Delete receipt |
| `checkDuplicate(vendor, date, amount)` | Check duplicates |
| `getReceipts(filters, sort, page, size)` | Get receipts list |
| `searchReceipts(query, page, size)` | Search receipts |
| `getReceiptStatistics()` | Get statistics |
| `exportReceipts(request)` | Export to Excel/PDF/CSV |
| `downloadReceiptPDF(id)` | Download signed PDF |
| `getReceiptHistory(id)` | Get edit history |

---

## Hebrew Error Messages
✅ All errors in Hebrew  
✅ Ready to display to users  
✅ No translation needed

---

**Full docs:** `RECEIPT_SERVICE.md`
