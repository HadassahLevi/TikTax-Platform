# Excel Export Service - Complete Documentation

## Overview
The Excel Export Service generates professional, accountant-ready Excel workbooks with receipt data. Features include multi-sheet workbooks, Hebrew RTL support, automatic calculations, and secure temporary download URLs.

---

## Architecture

```
┌─────────────────┐
│  Export Request │
│  (Frontend)     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  POST /api/v1/export/generate   │
│  - Validate date range          │
│  - Query APPROVED receipts      │
│  - Apply filters                │
└────────┬────────────────────────┘
         │
         ▼
┌──────────────────────────┐
│  ExcelService            │
│  - Create 3 sheets       │
│  - Apply Hebrew RTL      │
│  - Format currency       │
│  - Calculate totals      │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  In-Memory Storage       │
│  - Generate UUID         │
│  - Store bytes + meta    │
│  - Set 1-hour expiry     │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  Return Download URL     │
│  /export/download/{uuid} │
└──────────────────────────┘
```

---

## API Endpoints

### 1. POST /api/v1/export/generate

Generate export file (Excel or CSV).

**Request Body:**
```json
{
  "format": "excel",              // "excel" | "csv" | "pdf"
  "date_from": "2024-01-01T00:00:00",
  "date_to": "2024-12-31T23:59:59",
  "category_ids": [1, 2, 3],      // Optional filter
  "include_images": false          // Not implemented yet
}
```

**Response:**
```json
{
  "export_id": "550e8400-e29b-41d4-a716-446655440000",
  "download_url": "/api/v1/export/download/550e8400-e29b-41d4-a716-446655440000",
  "expires_at": "2024-01-01T13:00:00",
  "file_size": 45678,
  "message": "הקובץ הופק בהצלחה - 125 קבלות"
}
```

**Validation Rules:**
- `date_from` must be before `date_to`
- Maximum date range: 2 years (730 days)
- Only includes `APPROVED` receipts
- Returns 404 if no receipts found

**Status Codes:**
- `201 Created` - Export generated successfully
- `400 Bad Request` - Invalid date range
- `404 Not Found` - No receipts in date range
- `401 Unauthorized` - Not authenticated
- `501 Not Implemented` - PDF format (coming soon)

---

### 2. GET /api/v1/export/download/{export_id}

Download generated export file.

**Path Parameters:**
- `export_id` - UUID from generate endpoint

**Response:**
- Binary file (Excel or CSV)
- Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` or `text/csv`
- Content-Disposition: `attachment; filename="tiktax_receipts_20240101_20241231.xlsx"`

**Security:**
- Requires authentication
- Users can only download their own exports
- Links expire after 1 hour

**Status Codes:**
- `200 OK` - File download successful
- `404 Not Found` - Export ID not found or expired
- `403 Forbidden` - Trying to access another user's export
- `410 Gone` - Export expired
- `401 Unauthorized` - Not authenticated

---

### 3. DELETE /api/v1/export/cleanup

Clean up expired exports (Admin/maintenance).

**Response:**
```json
{
  "message": "נוקו 15 קבצים שפג תוקפם",
  "cleaned_count": 15,
  "remaining_count": 8
}
```

---

## Excel Workbook Structure

### Sheet 1: סיכום (Summary)

**Content:**
- Report title
- Business information (name, number, type)
- Report period
- Creation date
- Financial totals:
  - Total receipts count
  - Pre-VAT amount
  - VAT amount
  - Total including VAT

**Styling:**
- Blue header (#2563EB)
- Green totals section (#059669)
- Highlighted grand total (light green background)
- Hebrew RTL layout

---

### Sheet 2: פירוט קבלות (Receipt Details)

**Columns:**
1. תאריך (Date) - DD/MM/YYYY
2. ספק (Vendor) - Business name
3. מספר עוסק (Business Number) - 9 digits
4. מספר קבלה (Receipt Number)
5. קטגוריה (Category) - Hebrew name
6. לפני מע"מ (Pre-VAT) - ₪#,##0.00
7. מע"מ (VAT) - ₪#,##0.00
8. סה"כ (Total) - ₪#,##0.00
9. הערות (Notes)

**Features:**
- Frozen header row
- Currency formatting on amount columns
- Borders on all cells
- RTL text alignment
- Sorted by date (ascending)

---

### Sheet 3: פירוט לפי קטגוריה (Category Breakdown)

**Columns:**
1. קטגוריה (Category)
2. מספר קבלות (Receipt Count)
3. סכום כולל (Total Amount) - ₪#,##0.00
4. אחוז (Percentage) - 0.0%

**Features:**
- Sorted by amount (descending)
- Total row at bottom
- Percentage calculations
- Frozen header row

---

## Code Examples

### Frontend: Generate Export

```typescript
import { exportService } from '@/services/export.service';

async function downloadExport() {
  try {
    setLoading(true);
    
    const request = {
      format: 'excel',
      date_from: new Date('2024-01-01'),
      date_to: new Date('2024-12-31'),
      category_ids: [1, 2, 3],
      include_images: false
    };
    
    const response = await exportService.generateExport(request);
    
    // Download the file
    const downloadResponse = await fetch(response.download_url, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    const blob = await downloadResponse.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `receipts_${Date.now()}.xlsx`;
    a.click();
    
    toast.success(response.message);
  } catch (error) {
    toast.error('שגיאה ביצירת הקובץ');
  } finally {
    setLoading(false);
  }
}
```

### Backend: Custom Export Logic

```python
from app.services.excel_service import excel_service

# Generate export
excel_bytes = excel_service.generate_export(
    user=current_user,
    receipts=receipts,
    categories=categories,
    date_from=datetime(2024, 1, 1),
    date_to=datetime(2024, 12, 31)
)

# Save to file
with open('export.xlsx', 'wb') as f:
    f.write(excel_bytes)
```

---

## Testing

### Run Unit Tests
```bash
pytest tests/services/test_excel_service.py -v
```

### Run Integration Tests
```bash
pytest tests/api/test_export.py -v
```

### Test Coverage
```bash
pytest tests/services/test_excel_service.py --cov=app.services.excel_service --cov-report=html
```

---

## Security Considerations

### 1. Authentication Required
All export endpoints require valid JWT token.

### 2. Authorization
Users can only export their own receipts and download their own exports.

### 3. Rate Limiting
Consider adding rate limiting to prevent abuse:
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@router.post("/generate")
@limiter.limit("10/hour")  # Max 10 exports per hour
async def generate_export(...):
    ...
```

### 4. Temporary URLs
Download URLs expire after 1 hour to prevent unauthorized sharing.

### 5. Data Validation
- Date ranges validated (max 2 years)
- Category IDs validated against user's categories
- Only APPROVED receipts included

---

## Performance Optimization

### 1. Large Exports
For exports with > 1000 receipts:
```python
# Consider pagination or background jobs
if len(receipts) > 1000:
    # Use Celery task
    task = generate_export_task.delay(user_id, request)
    return {"task_id": task.id, "status": "processing"}
```

### 2. Memory Management
Current implementation stores exports in memory. For production:

**Option A: Redis with TTL**
```python
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Store with 1-hour expiry
redis_client.setex(
    f"export:{export_id}",
    3600,  # 1 hour
    file_content
)
```

**Option B: S3 with Presigned URLs**
```python
import boto3

s3_client = boto3.client('s3')

# Upload to S3
s3_client.put_object(
    Bucket='tiktax-exports',
    Key=f'exports/{export_id}.xlsx',
    Body=file_content
)

# Generate presigned URL (1 hour expiry)
download_url = s3_client.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'tiktax-exports', 'Key': f'exports/{export_id}.xlsx'},
    ExpiresIn=3600
)
```

### 3. Cleanup Strategy
```python
# Scheduled job (run every hour)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job('cron', hour='*/1')
async def cleanup_expired_exports():
    await export_cleanup()
```

---

## Troubleshooting

### Issue: Hebrew text appears as gibberish in Excel

**Solution:** Ensure RTL is enabled:
```python
ws.sheet_view.rightToLeft = True
```

For CSV, use UTF-8 with BOM:
```python
output.write('\ufeff')  # BOM
csv_content.encode('utf-8-sig')
```

---

### Issue: Excel file is corrupted

**Solution:** Verify openpyxl version:
```bash
pip install openpyxl==3.1.2
```

Check that workbook is properly saved:
```python
output = io.BytesIO()
wb.save(output)
output.seek(0)  # IMPORTANT!
return output.read()
```

---

### Issue: Memory usage too high

**Solution:** Implement streaming for large exports:
```python
# Use openpyxl write_only mode
wb = Workbook(write_only=True)
ws = wb.create_sheet("Data")

for receipt in receipts:
    ws.append([...])  # Streams to file
```

---

### Issue: Export generation is slow

**Solution:** Optimize queries:
```python
# Use eager loading
receipts = db.query(Receipt).options(
    joinedload(Receipt.category)
).filter(...).all()

# Batch operations
category_dict = {cat.id: cat.name_hebrew for cat in categories}
```

---

## Future Enhancements

### 1. PDF Export (Planned)
- Single receipt PDF with business logo
- Multi-receipt PDF report
- Digital signature visualization

### 2. Email Delivery
```python
@router.post("/generate")
async def generate_export(..., send_email: bool = False):
    if send_email:
        await email_service.send_export(user.email, file_content)
```

### 3. Scheduled Exports
```python
@router.post("/schedule")
async def schedule_export(
    frequency: str,  # "daily", "weekly", "monthly"
    format: str,
    email: str
):
    # Create scheduled job
    ...
```

### 4. Custom Templates
Allow users to define custom Excel templates with their branding.

### 5. Multi-Currency Support
Support exports in USD, EUR, etc. with conversion rates.

---

## Dependencies

```
openpyxl==3.1.2          # Excel generation
pandas==2.1.3            # Future: advanced data processing
python-dateutil==2.8.2   # Date handling
```

---

## API Client Examples

### cURL
```bash
# Generate export
curl -X POST "http://localhost:8000/api/v1/export/generate" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "format": "excel",
    "date_from": "2024-01-01T00:00:00",
    "date_to": "2024-12-31T23:59:59"
  }'

# Download export
curl -X GET "http://localhost:8000/api/v1/export/download/UUID" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  --output receipts.xlsx
```

### Python
```python
import requests

# Generate
response = requests.post(
    'http://localhost:8000/api/v1/export/generate',
    headers={'Authorization': f'Bearer {token}'},
    json={
        'format': 'excel',
        'date_from': '2024-01-01T00:00:00',
        'date_to': '2024-12-31T23:59:59'
    }
)

export_data = response.json()

# Download
download_response = requests.get(
    f"http://localhost:8000{export_data['download_url']}",
    headers={'Authorization': f'Bearer {token}'}
)

with open('receipts.xlsx', 'wb') as f:
    f.write(download_response.content)
```

---

## Monitoring & Logging

### Key Metrics to Track
- Export generation time
- File sizes
- Download counts
- Error rates
- Memory usage

### Logging
```python
logger.info(f"Export generated: {export_id} | User: {user_id} | Format: {format} | Receipts: {count} | Size: {size}b")
logger.warning(f"Unauthorized download attempt: Export {export_id} | Requester: {user_id}")
logger.error(f"Export generation failed: {error}", exc_info=True)
```

---

## Compliance & Legal

### Israeli Tax Authority Requirements
- 7-year data retention
- Digital signatures on receipts
- Proper VAT calculations
- Business number validation

### GDPR Compliance
- Export includes personal data
- Users have right to data portability
- Temporary URLs auto-expire
- Proper access controls

---

## Summary

✅ **Implemented:**
- Multi-sheet Excel generation
- CSV export with Hebrew BOM
- Hebrew RTL support
- Secure temporary downloads
- Category breakdown
- Financial calculations
- Unit and integration tests

🚧 **Not Implemented (Future):**
- PDF export
- Email delivery
- Scheduled exports
- S3/Redis storage
- Receipt images in export

---

**For questions or issues, contact: dev@tiktax.co.il**
