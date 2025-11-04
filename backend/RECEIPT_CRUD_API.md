# Receipt CRUD API Documentation

## Overview
Complete CRUD (Create, Read, Update, Delete) API for receipt management with advanced filtering, sorting, and pagination.

## Base URL
```
Production: https://api.tiktax.co.il/api/v1/receipts
Development: http://localhost:8000/api/v1/receipts
```

## Authentication
All endpoints require Bearer token authentication:
```
Authorization: Bearer <access_token>
```

---

## Endpoints

### 1. List Receipts
**GET** `/api/v1/receipts`

List user's receipts with filtering, sorting, and pagination.

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page` | integer | No | Page number (default: 1, min: 1) |
| `page_size` | integer | No | Items per page (default: 20, min: 1, max: 100) |
| `date_from` | datetime | No | Filter by start date (ISO 8601) |
| `date_to` | datetime | No | Filter by end date (ISO 8601) |
| `category_ids` | string | No | Comma-separated category IDs (e.g., "1,2,3") |
| `amount_min` | float | No | Minimum amount (inclusive) |
| `amount_max` | float | No | Maximum amount (inclusive) |
| `status` | string | No | Filter by status: `processing`, `review`, `approved`, `failed`, `duplicate` |
| `search_query` | string | No | Search in vendor name, receipt number, business number |
| `sort_by` | string | No | Sort field: `created_at`, `receipt_date`, `total_amount`, `vendor_name` (default: `created_at`) |
| `sort_order` | string | No | Sort order: `asc`, `desc` (default: `desc`) |

#### Response: 200 OK
```json
{
  "receipts": [
    {
      "id": 123,
      "vendor_name": "Super-Pharm",
      "receipt_date": "2024-01-15T10:30:00Z",
      "total_amount": 150.50,
      "category_name": "בריאות",
      "status": "approved",
      "is_duplicate": false,
      "created_at": "2024-01-15T10:35:00Z"
    }
  ],
  "total": 42,
  "page": 1,
  "page_size": 20,
  "pages": 3
}
```

#### Examples

**List all receipts (default)**
```bash
GET /api/v1/receipts
```

**Paginate through results**
```bash
GET /api/v1/receipts?page=2&page_size=10
```

**Filter by date range**
```bash
GET /api/v1/receipts?date_from=2024-01-01T00:00:00Z&date_to=2024-01-31T23:59:59Z
```

**Filter by categories**
```bash
GET /api/v1/receipts?category_ids=1,3,5
```

**Filter by amount range**
```bash
GET /api/v1/receipts?amount_min=100&amount_max=500
```

**Filter by status**
```bash
GET /api/v1/receipts?status=review
```

**Search receipts**
```bash
GET /api/v1/receipts?search_query=super-pharm
```

**Sort by amount (highest first)**
```bash
GET /api/v1/receipts?sort_by=total_amount&sort_order=desc
```

**Combine filters**
```bash
GET /api/v1/receipts?date_from=2024-01-01T00:00:00Z&category_ids=1,2&amount_min=50&status=approved&sort_by=receipt_date&sort_order=desc
```

---

### 2. Get Receipt Details
**GET** `/api/v1/receipts/{receipt_id}`

Get full details of a single receipt.

#### Path Parameters
- `receipt_id` (integer, required): Receipt ID

#### Response: 200 OK
```json
{
  "id": 123,
  "user_id": 456,
  "original_filename": "receipt_20240115.jpg",
  "file_url": "https://s3.amazonaws.com/tiktax-receipts/user-456/2024/01/abc123.jpg",
  "file_size": 204800,
  "vendor_name": "Super-Pharm",
  "business_number": "512345678",
  "receipt_number": "1234567",
  "receipt_date": "2024-01-15T10:30:00Z",
  "total_amount": 150.50,
  "vat_amount": 21.87,
  "pre_vat_amount": 128.63,
  "category_id": 5,
  "category_name": "בריאות",
  "status": "approved",
  "confidence_score": 0.92,
  "is_digitally_signed": false,
  "is_duplicate": false,
  "duplicate_of_id": null,
  "notes": "תרופות לחודש ינואר",
  "created_at": "2024-01-15T10:35:00Z",
  "updated_at": "2024-01-15T10:40:00Z",
  "approved_at": "2024-01-15T10:45:00Z"
}
```

#### Error Responses

**404 Not Found**
```json
{
  "detail": "קבלה לא נמצאה"
}
```

---

### 3. Update Receipt
**PUT** `/api/v1/receipts/{receipt_id}`

Update receipt data during review process. Creates edit history for all changes.

**Restrictions:**
- Can only update receipts in `review` or `duplicate` status
- Cannot update `approved` or `failed` receipts

#### Path Parameters
- `receipt_id` (integer, required): Receipt ID

#### Request Body
```json
{
  "vendor_name": "Super-Pharm - סניף רמת גן",
  "business_number": "512345678",
  "receipt_number": "1234567",
  "receipt_date": "2024-01-15T10:30:00Z",
  "total_amount": 155.00,
  "vat_amount": 22.52,
  "pre_vat_amount": 132.48,
  "category_id": 5,
  "notes": "תרופות + ויטמינים"
}
```

**All fields are optional** - only include fields you want to update.

#### Field Validation

| Field | Type | Constraints |
|-------|------|-------------|
| `vendor_name` | string | Min: 1 char, Max: 200 chars |
| `business_number` | string | Exactly 9 digits |
| `receipt_number` | string | Max: 50 chars |
| `receipt_date` | datetime | ISO 8601 format |
| `total_amount` | float | Greater than 0 |
| `vat_amount` | float | Greater than or equal to 0 |
| `pre_vat_amount` | float | Greater than or equal to 0 |
| `category_id` | integer | Must be valid category ID |
| `notes` | string | Max: 500 chars |

#### Response: 200 OK
Returns full receipt details (same as GET endpoint).

#### Error Responses

**400 Bad Request** - Cannot edit approved/failed receipts
```json
{
  "detail": "לא ניתן לערוך קבלה שאושרה או נכשלה"
}
```

**422 Unprocessable Entity** - Validation error
```json
{
  "detail": [
    {
      "loc": ["body", "business_number"],
      "msg": "מספר עסק חייב להכיל 9 ספרות",
      "type": "value_error"
    }
  ]
}
```

#### Edit History
All changes are tracked in the `receipt_edits` table:
- Field name
- Old value
- New value
- Timestamp
- User ID

---

### 4. Approve Receipt
**POST** `/api/v1/receipts/{receipt_id}/approve`

Approve receipt for final archiving. Updates status to `approved` and records approval timestamp.

**Restrictions:**
- Can only approve receipts in `review` status
- All required fields must be present

#### Path Parameters
- `receipt_id` (integer, required): Receipt ID

#### Request Body
```json
{
  "vendor_name": "Super-Pharm",
  "business_number": "512345678",
  "receipt_number": "1234567",
  "receipt_date": "2024-01-15T10:30:00Z",
  "total_amount": 150.50,
  "category_id": 5,
  "notes": "תרופות חודשיות"
}
```

**Required fields:** `vendor_name`, `receipt_date`, `total_amount`, `category_id`

**Optional fields:** `business_number`, `receipt_number`, `notes`

#### Response: 200 OK
Returns full receipt details with:
- `status` = "approved"
- `approved_at` timestamp set

#### Error Responses

**400 Bad Request** - Already approved
```json
{
  "detail": "לא ניתן לאשר קבלה שכבר אושרה"
}
```

---

### 5. Delete Receipt
**DELETE** `/api/v1/receipts/{receipt_id}`

Permanently delete receipt. Removes file from S3 storage and database record.

**Warning:** This action is irreversible. All associated data (edit history, etc.) will be deleted via CASCADE.

#### Path Parameters
- `receipt_id` (integer, required): Receipt ID

#### Response: 204 No Content
Empty body on success.

#### Error Responses

**404 Not Found**
```json
{
  "detail": "קבלה לא נמצאה"
}
```

---

### 6. Retry Processing
**POST** `/api/v1/receipts/{receipt_id}/retry`

Retry OCR processing for failed receipts.

**Restrictions:**
- Can only retry receipts in `failed` status

#### Path Parameters
- `receipt_id` (integer, required): Receipt ID

#### Response: 202 Accepted
```json
{
  "message": "מעבד מחדש את הקבלה"
}
```

Processing happens in the background. Check status via `/api/v1/receipts/{receipt_id}/status`.

#### Error Responses

**400 Bad Request** - Not a failed receipt
```json
{
  "detail": "ניתן לנסות שוב רק קבלות שנכשלו"
}
```

---

## Receipt Status Workflow

```
PROCESSING → OCR in progress
     ↓
REVIEW → Awaiting user confirmation
     ↓
APPROVED → Finalized and archived
```

**Alternative paths:**
- `PROCESSING` → `FAILED` (OCR error) → Can retry
- `PROCESSING` → `DUPLICATE` (Duplicate detected)

---

## Security

### Permission Checks
- All endpoints verify user owns the receipt
- Users can only access/modify their own receipts
- Attempting to access another user's receipt returns 404

### Data Validation
- Client-side validation (Pydantic schemas)
- Server-side validation (database constraints)
- Business rules (status transitions, edit permissions)

---

## Performance Optimization

### Database Indexes
Optimized for common queries:
- `idx_receipt_user_id` - User filtering
- `idx_receipt_status` - Status filtering
- `idx_receipt_date` - Date range queries
- `idx_receipt_vendor` - Search queries
- `idx_receipt_created_at` - Default sorting

### Pagination
- Default: 20 items per page
- Maximum: 100 items per page
- Use pagination for large result sets

### Caching Recommendations
Client-side caching for:
- Category list (changes infrequently)
- Receipt list (cache by filter combination)
- Individual receipts (invalidate on update)

---

## Error Codes Summary

| Status Code | Meaning | Common Causes |
|-------------|---------|---------------|
| 200 | OK | Success |
| 202 | Accepted | Background job started |
| 204 | No Content | Delete successful |
| 400 | Bad Request | Invalid status for operation |
| 401 | Unauthorized | Missing/invalid auth token |
| 404 | Not Found | Receipt doesn't exist or wrong user |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

---

## Example Workflows

### Complete Receipt Review Workflow
```bash
# 1. Upload receipt (via upload endpoint)
POST /api/v1/receipts/upload

# 2. Poll for processing completion
GET /api/v1/receipts/{id}/status

# 3. Review extracted data
GET /api/v1/receipts/{id}

# 4. Make corrections if needed
PUT /api/v1/receipts/{id}
{
  "vendor_name": "Corrected Name",
  "total_amount": 123.45,
  "category_id": 5
}

# 5. Approve for archiving
POST /api/v1/receipts/{id}/approve
{
  "vendor_name": "Final Name",
  "receipt_date": "2024-01-15T10:30:00Z",
  "total_amount": 123.45,
  "category_id": 5
}
```

### Monthly Export Workflow
```bash
# 1. Get all approved receipts for January 2024
GET /api/v1/receipts?status=approved&date_from=2024-01-01T00:00:00Z&date_to=2024-01-31T23:59:59Z&page_size=100

# 2. For each receipt, get full details if needed
GET /api/v1/receipts/{id}

# 3. Generate Excel export (separate endpoint)
POST /api/v1/export/excel
```

---

## Rate Limiting
- Default: 100 requests per minute per user
- List endpoint: 30 requests per minute
- Upload endpoint: 10 requests per minute

Exceeding limits returns `429 Too Many Requests`.

---

## Support
For issues or questions:
- Email: support@tiktax.co.il
- Documentation: https://docs.tiktax.co.il
