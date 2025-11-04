# Receipt CRUD Endpoints - Developer Guide

## 🎯 Quick Start

### Run Tests
```bash
cd backend
python run_receipt_tests.py
```

Or run individually:
```bash
# Unit tests only
pytest tests/api/test_receipt_crud.py -v

# Integration tests only
pytest tests/integration/test_receipt_crud_integration.py -v

# All receipt tests
pytest tests/api/test_receipt_crud.py tests/integration/test_receipt_crud_integration.py -v
```

### Start Development Server
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Test Endpoints Manually
```bash
# Get auth token first
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Use token for requests
export TOKEN="your_access_token_here"

# List receipts
curl -X GET http://localhost:8000/api/v1/receipts \
  -H "Authorization: Bearer $TOKEN"

# Get specific receipt
curl -X GET http://localhost:8000/api/v1/receipts/1 \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📁 File Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── receipts.py          # CRUD endpoints
│   ├── schemas/
│   │   └── receipt.py                   # Pydantic schemas
│   ├── models/
│   │   ├── receipt.py                   # Receipt model
│   │   └── receipt_edit.py              # Edit history model
│   └── services/
│       └── receipt_service.py           # Business logic
├── tests/
│   ├── api/
│   │   └── test_receipt_crud.py         # Unit tests
│   └── integration/
│       └── test_receipt_crud_integration.py  # Integration tests
├── RECEIPT_CRUD_API.md                  # API documentation
├── RECEIPT_CRUD_IMPLEMENTATION.md       # Implementation summary
└── run_receipt_tests.py                 # Test runner
```

---

## 🔧 Implementation Details

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/receipts` | List receipts with filters |
| GET | `/api/v1/receipts/{id}` | Get single receipt |
| PUT | `/api/v1/receipts/{id}` | Update receipt |
| POST | `/api/v1/receipts/{id}/approve` | Approve receipt |
| DELETE | `/api/v1/receipts/{id}` | Delete receipt |
| POST | `/api/v1/receipts/{id}/retry` | Retry failed processing |

### Key Features

**Filtering:**
- Date range (date_from, date_to)
- Categories (category_ids)
- Amount range (amount_min, amount_max)
- Status (processing, review, approved, failed, duplicate)
- Search (vendor name, receipt number, business number)

**Sorting:**
- Fields: created_at, receipt_date, total_amount, vendor_name
- Order: asc, desc

**Pagination:**
- Configurable page size (1-100)
- Total count included
- Page calculation

**Security:**
- User can only access their own receipts
- Permission checks on all operations
- Data validation on all inputs

**Edit History:**
- All changes tracked in `receipt_edits` table
- Field-level tracking
- Old/new value recording

---

## 🧪 Testing

### Test Coverage

**Unit Tests (30+ cases):**
- ✅ List receipts with pagination
- ✅ Filter by date, category, amount, status
- ✅ Search functionality
- ✅ Sorting (all fields, both directions)
- ✅ Get single receipt
- ✅ Update receipt with validation
- ✅ Edit history creation
- ✅ Approve receipt
- ✅ Delete receipt
- ✅ Retry processing
- ✅ Permission checks
- ✅ Error handling

**Integration Tests (15+ cases):**
- ✅ Complete receipt lifecycle
- ✅ Complex filter combinations
- ✅ Large dataset pagination
- ✅ Multi-user isolation
- ✅ Edit history tracking
- ✅ Sorting by all fields
- ✅ Security verification

### Running Specific Tests

```bash
# Run only list tests
pytest tests/api/test_receipt_crud.py::TestListReceipts -v

# Run only update tests
pytest tests/api/test_receipt_crud.py::TestUpdateReceipt -v

# Run with coverage
pytest tests/api/test_receipt_crud.py --cov=app.api.v1.endpoints.receipts

# Run with detailed output
pytest tests/api/test_receipt_crud.py -vv --tb=long
```

---

## 📊 Database Schema

### Receipt Table
```sql
CREATE TABLE receipts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    
    -- File info
    original_filename VARCHAR NOT NULL,
    file_url VARCHAR NOT NULL,
    file_size INTEGER NOT NULL,
    mime_type VARCHAR NOT NULL,
    
    -- Receipt data
    vendor_name VARCHAR,
    business_number VARCHAR(9),
    receipt_number VARCHAR,
    receipt_date TIMESTAMP,
    
    -- Financial
    total_amount FLOAT,
    vat_amount FLOAT,
    pre_vat_amount FLOAT,
    
    -- Classification
    category_id INTEGER REFERENCES categories(id),
    
    -- OCR metadata
    ocr_data JSON,
    confidence_score FLOAT,
    
    -- Status
    status VARCHAR NOT NULL,
    processing_started_at TIMESTAMP,
    processing_completed_at TIMESTAMP,
    approved_at TIMESTAMP,
    
    -- User input
    notes TEXT,
    
    -- Digital signature
    is_digitally_signed BOOLEAN DEFAULT FALSE,
    signature_timestamp TIMESTAMP,
    signature_certificate_id VARCHAR,
    
    -- Duplicate detection
    is_duplicate BOOLEAN DEFAULT FALSE,
    duplicate_of_id INTEGER REFERENCES receipts(id),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_receipt_user_id ON receipts(user_id);
CREATE INDEX idx_receipt_status ON receipts(status);
CREATE INDEX idx_receipt_date ON receipts(receipt_date);
CREATE INDEX idx_receipt_vendor ON receipts(vendor_name);
CREATE INDEX idx_receipt_business_number ON receipts(business_number);
CREATE INDEX idx_receipt_created_at ON receipts(created_at);
```

### Receipt Edit Table
```sql
CREATE TABLE receipt_edits (
    id SERIAL PRIMARY KEY,
    receipt_id INTEGER REFERENCES receipts(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    
    field_name VARCHAR NOT NULL,
    old_value VARCHAR,
    new_value VARCHAR,
    
    edited_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_receipt_edit_receipt ON receipt_edits(receipt_id);
CREATE INDEX idx_receipt_edit_user ON receipt_edits(user_id);
```

---

## 🚀 Common Use Cases

### 1. Monthly Expense Report
```python
# Get all approved receipts for January 2024
params = {
    "status": "approved",
    "date_from": "2024-01-01T00:00:00Z",
    "date_to": "2024-01-31T23:59:59Z",
    "page_size": 100,
    "sort_by": "receipt_date",
    "sort_order": "asc"
}
response = requests.get(f"{API_BASE}/receipts", params=params, headers=auth_headers)
receipts = response.json()["receipts"]
```

### 2. Review Pending Receipts
```python
# Get all receipts awaiting review
params = {
    "status": "review",
    "sort_by": "created_at",
    "sort_order": "desc"
}
response = requests.get(f"{API_BASE}/receipts", params=params, headers=auth_headers)
pending = response.json()["receipts"]

# Update and approve each
for receipt in pending:
    # Update if needed
    if receipt["vendor_name"] is None:
        update_data = {"vendor_name": "Corrected Name"}
        requests.put(f"{API_BASE}/receipts/{receipt['id']}", json=update_data, headers=auth_headers)
    
    # Approve
    approve_data = {
        "vendor_name": receipt["vendor_name"],
        "receipt_date": receipt["receipt_date"],
        "total_amount": receipt["total_amount"],
        "category_id": 1
    }
    requests.post(f"{API_BASE}/receipts/{receipt['id']}/approve", json=approve_data, headers=auth_headers)
```

### 3. Category-Based Analysis
```python
# Get all food receipts over $50
params = {
    "category_ids": "1",  # Food category
    "amount_min": 50.0,
    "status": "approved"
}
response = requests.get(f"{API_BASE}/receipts", params=params, headers=auth_headers)
food_receipts = response.json()["receipts"]

# Calculate total
total = sum(r["total_amount"] for r in food_receipts)
print(f"Total food expenses: ${total:.2f}")
```

### 4. Search and Filter
```python
# Find all Super-Pharm receipts from last month
from datetime import datetime, timedelta

last_month = datetime.now() - timedelta(days=30)
params = {
    "search_query": "super-pharm",
    "date_from": last_month.isoformat()
}
response = requests.get(f"{API_BASE}/receipts", params=params, headers=auth_headers)
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: ReceiptStatus Import Error
**Error:** `ImportError: cannot import name 'ReceiptStatus' from 'app.schemas.receipt'`

**Solution:** ReceiptStatus enum is defined in `app.models.receipt`, not schemas. Use:
```python
from app.models.receipt import ReceiptStatus
```

### Issue 2: Category Name Not Showing
**Problem:** `category_name` is None in list response

**Solution:** Make sure category exists and has `name_hebrew` field:
```python
category = db.query(Category).filter(Category.id == receipt.category_id).first()
if category:
    category_name = category.name_hebrew
```

### Issue 3: Edit History Not Created
**Problem:** Updates don't create edit history

**Solution:** Ensure you're using `update_data.dict(exclude_unset=True)` to only get provided fields:
```python
for field, new_value in update_data.dict(exclude_unset=True).items():
    if new_value is not None:
        old_value = getattr(receipt, field)
        if old_value != new_value:
            # Create edit record
```

### Issue 4: Cannot Update Approved Receipt
**Error:** `400 Bad Request: לא ניתן לערוך קבלה שאושרה או נכשלה`

**Solution:** This is intentional. Only receipts in REVIEW or DUPLICATE status can be edited. To modify approved receipts, you'd need a separate "edit approved" endpoint (not implemented).

---

## 🔐 Security Checklist

- ✅ All endpoints require authentication
- ✅ Users can only access their own receipts
- ✅ Input validation on all fields
- ✅ SQL injection prevention (using ORM)
- ✅ XSS prevention (data validation)
- ✅ Rate limiting (handled by middleware)
- ✅ File deletion on receipt delete
- ✅ Audit trail (edit history)

---

## 📈 Performance Optimization

### Database Indexes
All critical fields are indexed:
- user_id (for filtering by user)
- status (for status filtering)
- receipt_date (for date range queries)
- vendor_name (for search)
- created_at (for default sorting)

### Query Optimization
- Use `count()` before loading data
- Apply filters before pagination
- Only join Category when needed
- Use LIMIT/OFFSET for pagination

### Caching Recommendations
Cache these on client-side:
- Category list (rarely changes)
- Receipt list (invalidate on create/update/delete)
- Individual receipts (invalidate on update)

---

## 🎓 Next Steps

### Potential Enhancements
1. **Batch Operations**
   - Bulk approve
   - Bulk categorize
   - Bulk delete

2. **Advanced Search**
   - Fuzzy matching
   - Search in notes
   - Regular expression search

3. **Export**
   - Direct Excel export from list
   - PDF generation
   - Email receipts

4. **Analytics**
   - Spending trends
   - Category breakdown
   - Vendor analysis

---

## 📞 Support

**Questions?** Check:
- API Documentation: `RECEIPT_CRUD_API.md`
- Implementation Summary: `RECEIPT_CRUD_IMPLEMENTATION.md`
- Code Comments: Inline documentation in source files

**Issues?** Run tests first:
```bash
python run_receipt_tests.py
```

---

**Last Updated:** November 4, 2025
**Version:** 1.0.0
**Status:** ✅ Production Ready
