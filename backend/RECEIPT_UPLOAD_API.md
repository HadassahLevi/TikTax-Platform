# Receipt Upload API Documentation

## Overview
Secure file upload system for receipt images with AWS S3 storage, image optimization, and background OCR processing.

---

## Endpoints

### 1. Upload Receipt
**POST** `/api/v1/receipts/upload`

Upload a receipt image for OCR processing and archival.

#### Authentication
- Requires: Bearer token in `Authorization` header
- Checks: Subscription limits before upload

#### Request
**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Body (multipart/form-data):**
```
file: <image_file>
```

**File Requirements:**
- **Allowed formats:** JPEG, PNG, HEIC, HEIF
- **Size limits:** 10 KB - 10 MB
- **Optimization:** Images are automatically resized (max 2000x2000), converted to JPEG, and compressed

#### Response
**Success (201 Created):**
```json
{
  "receipt_id": 123,
  "status": "processing",
  "message": "הקבלה הועלתה בהצלחה ונמצאת בעיבוד"
}
```

**Error Responses:**

| Status | Description | Hebrew Message |
|--------|-------------|----------------|
| 400 | Invalid file type | סוג קובץ לא נתמך. נתמכים: JPEG, PNG, HEIC |
| 400 | File too small | קובץ קטן מדי. מינימום: 10KB |
| 413 | File too large | קובץ גדול מדי. מקסימום: 10MB |
| 402 | Subscription limit exceeded | הגעת למכסת הקבלות החודשית (X). שדרג את המנוי שלך. |
| 500 | Upload/processing failed | העלאת הקבלה נכשלה. נסה שוב. |

#### Example (cURL)
```bash
curl -X POST "https://api.tiktax.co.il/api/v1/receipts/upload" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@/path/to/receipt.jpg"
```

#### Example (JavaScript/Fetch)
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('/api/v1/receipts/upload', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  },
  body: formData
});

const data = await response.json();
console.log('Receipt ID:', data.receipt_id);
```

#### Workflow
1. **Validation:** File type and size validated
2. **Subscription Check:** User's monthly limit verified
3. **Image Optimization:** Resize, convert to JPEG, compress
4. **S3 Upload:** Encrypted upload to AWS S3
5. **Database Record:** Receipt entry created with status "processing"
6. **Background OCR:** OCR task queued for processing
7. **Response:** Receipt ID returned immediately

---

### 2. Get Processing Status
**GET** `/api/v1/receipts/{receipt_id}/status`

Poll receipt processing status and retrieve OCR results when ready.

#### Authentication
- Requires: Bearer token in `Authorization` header
- Authorization: Only receipt owner can access

#### Request
**Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `receipt_id` (integer): Receipt ID from upload response

#### Response
**Success (200 OK):**
```json
{
  "receipt_id": 123,
  "status": "review",
  "progress": 80,
  "message": "הקבלה מוכנה לבדיקה",
  "ocr_data": {
    "vendor_name": "סופר פארם",
    "business_number": "512345678",
    "receipt_number": "RCP-12345",
    "receipt_date": "2024-11-04",
    "total_amount": 156.80,
    "vat_amount": 22.75,
    "pre_vat_amount": 134.05,
    "confidence": {
      "vendor_name": 0.95,
      "business_number": 0.88,
      "receipt_number": 0.92,
      "total_amount": 0.98,
      "vat_amount": 0.85
    }
  }
}
```

**Status Values:**

| Status | Progress | Description |
|--------|----------|-------------|
| processing | 50% | OCR in progress |
| review | 80% | OCR complete, awaiting user review |
| approved | 100% | User approved and archived |
| failed | 0% | Processing failed |
| duplicate | 100% | Detected as duplicate |

**Error Responses:**

| Status | Description | Hebrew Message |
|--------|-------------|----------------|
| 404 | Receipt not found | קבלה לא נמצאה |

#### Example (cURL)
```bash
curl -X GET "https://api.tiktax.co.il/api/v1/receipts/123/status" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Example (JavaScript/Fetch with Polling)
```javascript
async function pollReceiptStatus(receiptId) {
  const maxAttempts = 30;
  const interval = 2000; // 2 seconds
  
  for (let i = 0; i < maxAttempts; i++) {
    const response = await fetch(`/api/v1/receipts/${receiptId}/status`, {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    });
    
    const data = await response.json();
    
    if (data.status === 'review' || data.status === 'failed') {
      return data; // Processing complete
    }
    
    await new Promise(resolve => setTimeout(resolve, interval));
  }
  
  throw new Error('Processing timeout');
}

// Usage
const result = await pollReceiptStatus(123);
if (result.status === 'review') {
  console.log('OCR Data:', result.ocr_data);
}
```

---

## Security Features

### 1. File Validation
- **MIME type checking:** Only image formats allowed
- **Size limits:** Prevents DoS attacks and excessive storage
- **Image verification:** Pillow library validates image integrity

### 2. AWS S3 Security
- **Server-side encryption:** AES-256 encryption at rest
- **Secure transfer:** HTTPS/TLS for uploads
- **Access control:** IAM policies restrict access
- **Metadata tracking:** User ID, upload date stored

### 3. Rate Limiting
- **Subscription-based limits:** Free (50), Starter (200), Pro (1000), Business (unlimited)
- **Monthly reset:** Limits reset on subscription renewal
- **Real-time checking:** Validated before upload starts

### 4. Privacy
- **EXIF stripping:** Image optimization removes metadata
- **User isolation:** Users can only access their own receipts
- **Presigned URLs:** Temporary access for secure downloads

---

## File Processing Pipeline

```
1. USER UPLOAD
   ↓
2. VALIDATION
   - File type check
   - Size validation
   - Subscription limit
   ↓
3. OPTIMIZATION
   - Resize (max 2000x2000)
   - Convert to JPEG
   - Compress (85% quality)
   - Strip EXIF
   ↓
4. S3 UPLOAD
   - Generate unique filename
   - Upload with encryption
   - Store metadata
   ↓
5. DATABASE RECORD
   - Create receipt entry
   - Status: "processing"
   - Increment user counter
   ↓
6. BACKGROUND OCR
   - Google Vision API
   - Extract Hebrew text
   - Parse receipt data
   - Update status to "review"
   ↓
7. USER REVIEW
   - Poll status endpoint
   - Receive OCR data
   - Approve/edit fields
```

---

## S3 Storage Structure

```
receipts/
├── {user_id}/
│   ├── {year}/
│   │   ├── {month}/
│   │   │   ├── {uuid}.jpg
│   │   │   ├── {uuid}.jpg
│   │   │   └── ...
```

**Example:**
```
receipts/123/2024/11/a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg
```

**Benefits:**
- Easy user data export/deletion (GDPR compliance)
- Organized by date for archival
- UUID prevents filename collisions
- Supports millions of receipts per user

---

## Error Handling

All errors return consistent Hebrew messages for Israeli users:

```json
{
  "detail": "הודעת שגיאה בעברית"
}
```

**Client should:**
1. Check response status code
2. Display `detail` message to user
3. Log full error for debugging
4. Retry on 5xx errors (max 3 attempts)

---

## Performance Considerations

### Upload Optimization
- **Image compression:** Reduces storage costs and upload time
- **Background processing:** Returns immediately, processes async
- **S3 multipart:** Handles large files efficiently

### Status Polling
- **Recommended interval:** 2-3 seconds
- **Timeout:** 60 seconds (OCR typically completes in 10-20s)
- **Exponential backoff:** Increase interval if processing is slow

### Caching
- **S3 URLs:** Cache for 1 hour
- **Presigned URLs:** Valid for 1 hour by default
- **OCR results:** Cached after first retrieval

---

## Subscription Limits

| Plan | Monthly Receipts | Price |
|------|-----------------|-------|
| Free | 50 | ₪0 |
| Starter | 200 | ₪29 |
| Pro | 1,000 | ₪99 |
| Business | Unlimited | ₪299 |

**Limit Enforcement:**
- Checked before upload starts
- Returns 402 Payment Required if exceeded
- Resets on subscription renewal date

---

## Testing

### Unit Tests
```bash
# Test storage service
pytest tests/services/test_storage_service.py -v

# Test upload endpoint
pytest tests/api/test_receipt_upload.py -v
```

### Integration Tests
```bash
# Full upload flow with S3
pytest tests/integration/test_receipt_flow.py -v
```

### Manual Testing with cURL
```bash
# Upload receipt
curl -X POST "http://localhost:8000/api/v1/receipts/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@test_receipt.jpg"

# Check status
curl -X GET "http://localhost:8000/api/v1/receipts/1/status" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Monitoring & Logging

### Key Metrics
- Upload success/failure rate
- Average processing time
- S3 storage usage
- OCR accuracy scores
- Subscription limit hits

### Logs
All operations are logged with:
- Timestamp
- User ID
- Receipt ID
- Action (upload, process, approve)
- Result (success/error)
- Processing time

**Example:**
```
2024-11-04 10:15:23 - INFO - Receipt uploaded: 123 by user 45
2024-11-04 10:15:30 - INFO - OCR completed successfully for receipt 123
```

---

## Future Enhancements

1. **Batch Upload:** Multiple receipts at once
2. **Mobile App Camera:** Direct camera integration
3. **Email Forwarding:** Forward receipts via email
4. **WhatsApp Integration:** Send receipts via WhatsApp
5. **Real-time WebSocket:** Push notifications for processing completion
6. **ML Categorization:** Auto-categorize based on vendor
7. **Duplicate Detection:** Prevent duplicate uploads
8. **Multi-language OCR:** Support Arabic, English, Russian

---

## Support

For technical issues or questions:
- Email: support@tiktax.co.il
- Docs: https://docs.tiktax.co.il
- Status: https://status.tiktax.co.il
