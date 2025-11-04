# PDF Export - Quick Reference

## 🚀 Quick Start

### Generate PDF Export

```bash
curl -X POST https://api.tiktax.co.il/api/v1/export/generate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "format": "pdf",
    "date_from": "2024-01-01T00:00:00",
    "date_to": "2024-12-31T23:59:59",
    "include_images": false
  }'
```

### Download PDF

```bash
curl -X GET https://api.tiktax.co.il/api/v1/export/download/EXPORT_ID \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -o report.pdf
```

---

## 📋 API Endpoints

### POST /api/v1/export/generate

**Request Body:**
```json
{
  "format": "pdf",                    // Required: "pdf"
  "date_from": "2024-01-01T00:00:00", // Required: ISO 8601
  "date_to": "2024-12-31T23:59:59",   // Required: ISO 8601
  "category_ids": [1, 2, 3],          // Optional: filter
  "include_images": false              // Optional: default false
}
```

**Response 201:**
```json
{
  "export_id": "550e8400-...",
  "download_url": "/api/v1/export/download/550e8400-...",
  "expires_at": "2024-01-15T12:00:00",
  "file_size": 45678,
  "message": "הקובץ מוכן להורדה"
}
```

### GET /api/v1/export/download/{export_id}

**Response 200:**
- Headers:
  - `Content-Type: application/pdf`
  - `Content-Disposition: attachment; filename=tiktax_receipts_YYYYMMDD_YYYYMMDD.pdf`
- Body: Binary PDF data

---

## 💻 Code Examples

### Python

```python
from app.services.pdf_service import pdf_service

pdf_bytes = pdf_service.generate_export(
    user=current_user,
    receipts=receipts,
    categories=categories,
    date_from=datetime(2024, 1, 1),
    date_to=datetime(2024, 12, 31),
    include_images=False
)

with open('report.pdf', 'wb') as f:
    f.write(pdf_bytes)
```

### JavaScript/TypeScript

```typescript
const response = await fetch('/api/v1/export/generate', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    format: 'pdf',
    date_from: '2024-01-01T00:00:00',
    date_to: '2024-12-31T23:59:59',
    include_images: false
  })
});

const { export_id, download_url } = await response.json();

// Download
window.location.href = `/api/v1/export/download/${export_id}`;
```

---

## 📊 PDF Structure

```
┌────────────────────────────────┐
│  Page 1: Title                 │
│  - Business info               │
│  - Report period               │
└────────────────────────────────┘
┌────────────────────────────────┐
│  Page 2: Summary               │
│  - Total receipts              │
│  - Financial totals            │
│  - Category breakdown          │
└────────────────────────────────┘
┌────────────────────────────────┐
│  Page 3+: Details              │
│  - All receipt data            │
│  - Paginated (30/page)         │
└────────────────────────────────┘
┌────────────────────────────────┐
│  Page N+ (optional): Images    │
│  - Receipt images              │
│  - One per page                │
└────────────────────────────────┘
```

---

## ⚙️ Configuration

### Include Images

```python
# Small export (faster)
include_images=False  # Recommended default

# Complete export (slower, larger file)
include_images=True   # Use for archival
```

### Performance

| Receipts | Images | Size    | Time    |
|----------|--------|---------|---------|
| 10       | No     | ~15 KB  | <1s     |
| 100      | No     | ~50 KB  | 1-2s    |
| 10       | Yes    | ~1 MB   | 5-10s   |
| 100      | Yes    | ~10 MB  | 30-60s  |

---

## 🧪 Testing

### Unit Tests
```bash
pytest tests/services/test_pdf_service.py -v
```

### Integration Tests
```bash
pytest tests/integration/test_pdf_export.py -v
```

### Manual Test
```bash
python test_pdf_manual.py
```

---

## 🔧 Common Issues

### Hebrew text shows as boxes
**Fix:** Register Hebrew TTF font
```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Hebrew', 'fonts/NotoSansHebrew.ttf'))
```

### Images not loading
**Check:**
- S3 URL is valid
- Network connectivity
- Timeout settings (default: 10s)

### PDF is blank
**Debug:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📦 Dependencies

```bash
pip install reportlab PyPDF2 pillow
```

**requirements.txt:**
```
reportlab==4.0.7
pypdf2==3.0.1
pillow==10.1.0
```

---

## 🔐 Security

- ✅ JWT authentication required
- ✅ User isolation (only own receipts)
- ✅ Export expires after 1 hour
- ✅ Date range validation (max 2 years)
- ✅ Input sanitization

---

## 📈 Response Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 201  | Created | Export generated successfully |
| 200  | OK      | PDF downloaded |
| 400  | Bad Request | Invalid date range |
| 401  | Unauthorized | Missing/invalid token |
| 403  | Forbidden | Not owner of export |
| 404  | Not Found | No receipts / Export expired |
| 500  | Server Error | PDF generation failed |

---

## 🎯 Best Practices

1. **Default:** `include_images=false` for better performance
2. **Large exports:** Consider background processing
3. **User experience:** Show progress indicator
4. **Storage:** Clean up expired exports (1 hour TTL)
5. **Rate limiting:** Prevent abuse (implement in production)

---

## 📚 Related Files

- Service: `/backend/app/services/pdf_service.py`
- Endpoint: `/backend/app/api/v1/endpoints/export.py`
- Tests: `/backend/tests/services/test_pdf_service.py`
- Integration: `/backend/tests/integration/test_pdf_export.py`
- Docs: `/backend/PDF_EXPORT_DOCUMENTATION.md`

---

## 🆘 Support

**Logs:**
```python
logger.info(f"PDF generated: {file_size} bytes")
logger.error(f"PDF generation failed: {error}")
```

**Check:**
- Export service logs
- S3 connectivity
- Hebrew font registration
- Memory usage

---

**Version:** 1.0.0  
**Last Updated:** January 2025  
**Status:** ✅ Production Ready
