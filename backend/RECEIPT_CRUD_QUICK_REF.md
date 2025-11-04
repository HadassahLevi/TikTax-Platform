# 🎯 Receipt CRUD Endpoints - Quick Reference

## 📋 Endpoints Overview

| Method | Endpoint | Purpose | Status Required |
|--------|----------|---------|-----------------|
| **GET** | `/api/v1/receipts` | List receipts (with filters) | Any |
| **GET** | `/api/v1/receipts/{id}` | Get single receipt | Any |
| **PUT** | `/api/v1/receipts/{id}` | Update receipt | REVIEW, DUPLICATE |
| **POST** | `/api/v1/receipts/{id}/approve` | Approve receipt | REVIEW |
| **DELETE** | `/api/v1/receipts/{id}` | Delete receipt | Any |
| **POST** | `/api/v1/receipts/{id}/retry` | Retry processing | FAILED |

---

## 🔍 List Receipts - GET `/api/v1/receipts`

### Query Parameters
```
page          = 1-∞              (default: 1)
page_size     = 1-100            (default: 20)
date_from     = ISO datetime     (filter start date)
date_to       = ISO datetime     (filter end date)
category_ids  = "1,2,3"          (comma-separated)
amount_min    = 0-∞              (minimum amount)
amount_max    = 0-∞              (maximum amount)
status        = processing|review|approved|failed|duplicate
search_query  = "text"           (searches vendor/receipt/business number)
sort_by       = created_at|receipt_date|total_amount|vendor_name
sort_order    = asc|desc         (default: desc)
```

### Example Request
```bash
GET /api/v1/receipts?status=approved&date_from=2024-01-01T00:00:00Z&sort_by=total_amount&sort_order=desc
```

### Response
```json
{
  "receipts": [...],
  "total": 42,
  "page": 1,
  "page_size": 20,
  "pages": 3
}
```

---

## 📄 Get Receipt - GET `/api/v1/receipts/{id}`

### Response
```json
{
  "id": 123,
  "vendor_name": "Super-Pharm",
  "total_amount": 150.50,
  "category_name": "בריאות",
  "status": "approved",
  ...
}
```

---

## ✏️ Update Receipt - PUT `/api/v1/receipts/{id}`

### Request Body (all optional)
```json
{
  "vendor_name": "Updated Name",
  "business_number": "123456789",
  "receipt_number": "12345",
  "receipt_date": "2024-01-15T10:30:00Z",
  "total_amount": 150.00,
  "category_id": 5,
  "notes": "Updated notes"
}
```

### Constraints
- ✅ Only REVIEW or DUPLICATE status
- ✅ Business number: exactly 9 digits
- ✅ Total amount: > 0
- ✅ Creates edit history automatically

---

## ✅ Approve Receipt - POST `/api/v1/receipts/{id}/approve`

### Request Body (required fields marked *)
```json
{
  "vendor_name": "Vendor",              // *
  "receipt_date": "2024-01-15T10:30:00Z", // *
  "total_amount": 150.00,               // *
  "category_id": 5,                     // *
  "business_number": "123456789",       // optional
  "receipt_number": "12345",            // optional
  "notes": "Notes"                      // optional
}
```

### Result
- Status → APPROVED
- `approved_at` timestamp set
- VAT recalculated

---

## 🗑️ Delete Receipt - DELETE `/api/v1/receipts/{id}`

### Response
```
204 No Content
```

### Actions
- ✅ Deletes file from S3
- ✅ Removes from database
- ✅ Cascades to edit history

---

## 🔄 Retry Processing - POST `/api/v1/receipts/{id}/retry`

### Constraints
- ✅ Only FAILED status

### Response
```json
{
  "message": "מעבד מחדש את הקבלה"
}
```

### Result
- Status → PROCESSING
- Background OCR job started

---

## 🎨 Status Workflow

```
PROCESSING → REVIEW → APPROVED
     ↓         ↓
  FAILED   DUPLICATE
     ↑
  (retry)
```

**Status Descriptions:**
- `PROCESSING` - OCR in progress
- `REVIEW` - Awaiting user confirmation
- `APPROVED` - Finalized and archived
- `FAILED` - Processing error (can retry)
- `DUPLICATE` - Detected as duplicate

---

## 🔒 Security Rules

1. ✅ All endpoints require authentication
2. ✅ Users can only access their own receipts
3. ✅ 404 returned for wrong user (not 403)
4. ✅ Input validation on all fields
5. ✅ Edit history tracks all changes

---

## 🧪 Testing

### Run All Tests
```bash
cd backend
python run_receipt_tests.py
```

### Run Specific Tests
```bash
pytest tests/api/test_receipt_crud.py::TestListReceipts -v
pytest tests/api/test_receipt_crud.py::TestUpdateReceipt -v
pytest tests/integration/test_receipt_crud_integration.py -v
```

---

## 📊 Common Queries

### Get this month's receipts
```
GET /api/v1/receipts?date_from=2024-01-01T00:00:00Z&date_to=2024-01-31T23:59:59Z
```

### Get pending reviews
```
GET /api/v1/receipts?status=review&sort_by=created_at&sort_order=asc
```

### Get high-value receipts
```
GET /api/v1/receipts?amount_min=500&sort_by=total_amount&sort_order=desc
```

### Search by vendor
```
GET /api/v1/receipts?search_query=super-pharm
```

### Get food category receipts
```
GET /api/v1/receipts?category_ids=1&status=approved
```

---

## ⚡ Performance Tips

1. **Pagination**: Use page_size <= 50 for best performance
2. **Filters**: Apply specific filters to reduce result set
3. **Sorting**: Default sort (created_at) is fastest
4. **Caching**: Cache category list on client
5. **Indexes**: All sortable/filterable fields are indexed

---

## ❗ Common Errors

| Status | Message | Meaning |
|--------|---------|---------|
| 400 | לא ניתן לערוך קבלה שאושרה | Cannot edit approved receipt |
| 400 | לא ניתן לאשר קבלה שכבר אושרה | Already approved |
| 400 | ניתן לנסות שוב רק קבלות שנכשלו | Can only retry failed receipts |
| 404 | קבלה לא נמצאה | Receipt not found or wrong user |
| 422 | Validation error | Invalid input data |

---

## 📚 Documentation Files

- **API Documentation:** `RECEIPT_CRUD_API.md` - Complete API reference
- **Implementation:** `RECEIPT_CRUD_IMPLEMENTATION.md` - What was built
- **Developer Guide:** `RECEIPT_CRUD_DEVELOPER_GUIDE.md` - How to use/extend

---

## ✅ Checklist for Integration

- [ ] Set up authentication (Bearer token)
- [ ] Create categories in database
- [ ] Test list endpoint with filters
- [ ] Test update + approve workflow
- [ ] Implement error handling
- [ ] Add loading states for async operations
- [ ] Cache category list
- [ ] Implement pagination UI
- [ ] Add search debouncing
- [ ] Test with real OCR data

---

**Quick Start:** See `RECEIPT_CRUD_DEVELOPER_GUIDE.md`
**Last Updated:** November 4, 2025
