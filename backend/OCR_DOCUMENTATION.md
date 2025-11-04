# OCR Service Documentation

## Overview
Google Cloud Vision API integration for Hebrew receipt text extraction in Tik-Tax.

## Features
- ✅ Hebrew text recognition (primary)
- ✅ English text recognition (secondary)
- ✅ Mixed Hebrew-English text handling
- ✅ Intelligent field extraction
- ✅ Confidence scoring
- ✅ Retry mechanism with exponential backoff
- ✅ Error handling and logging

---

## Supported Receipt Types

### Israeli Receipts (Primary)
- **Supermarkets**: Shufersal, Rami Levy, Mega, etc.
- **Restaurants & Cafes**: Hebrew and English names
- **Gas Stations**: PAZ, Delek, Sonol
- **Pharmacies**: Super-Pharm, etc.
- **General retail**: Any Israeli business

### Requirements
- **Image Quality**: Minimum 300 DPI recommended
- **File Formats**: JPG, PNG, PDF
- **Max File Size**: 10MB
- **Languages**: Hebrew (primary), English (secondary)

---

## Extracted Fields

### Core Fields
| Field | Hebrew Name | Pattern Examples | Confidence Target |
|-------|------------|------------------|-------------------|
| Vendor Name | שם העסק | First line of receipt | 85%+ |
| Business Number | ח.פ / ע.מ | 9-digit number | 90%+ |
| Receipt Number | מספר קבלה | Sequential number | 85%+ |
| Receipt Date | תאריך | DD/MM/YYYY, DD.MM.YYYY | 80%+ |
| Total Amount | סה״כ | Final amount with ₪ | 80%+ |
| VAT Amount | מע״מ | 17% of total | 85%+ |
| Pre-VAT Amount | לפני מע״מ | Calculated | 85%+ |

### Pattern Recognition

#### Business Number Patterns
```regex
ח\.?פ\.?\s*:?\s*(\d{9})           # ח.פ: 123456789
עוסק מורשה\s*:?\s*(\d{9})         # עוסק מורשה: 123456789
ע\.?מ\.?\s*:?\s*(\d{9})           # ע.מ: 123456789
business.*?(\d{9})                 # Business: 123456789
```

#### Receipt Number Patterns
```regex
קבלה\s*(?:מס\'|מספר|#)?\s*:?\s*(\d+)    # קבלה מספר: 123
receipt\s*(?:no|number|#)?\s*:?\s*(\d+)  # Receipt #: 123
מסמך\s*:?\s*(\d+)                        # מסמך: 123
חשבונית\s*(?:מס\'|מספר)?\s*:?\s*(\d+)  # חשבונית: 123
```

#### Amount Patterns
```regex
סה[״\"]כ\s*:?\s*₪?\s*([\d,]+\.?\d{0,2})      # סה״כ: ₪100.00
total\s*:?\s*₪?\s*([\d,]+\.?\d{0,2})          # Total: 100.00
לתשלום\s*:?\s*₪?\s*([\d,]+\.?\d{0,2})        # לתשלום: 100.00
```

#### Date Patterns
```regex
(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{2,4})  # DD/MM/YYYY
(\d{2,4})[\/\-\.](\d{1,2})[\/\-\.](\d{1,2})  # YYYY/MM/DD
```

---

## Confidence Scoring

### Calculation Method
Each field has an individual confidence score (0.0 - 1.0):
- **High confidence (0.85+)**: Direct pattern match with validation
- **Medium confidence (0.70-0.84)**: Partial match or calculated
- **Low confidence (< 0.70)**: Weak match or fallback logic

### Overall Receipt Confidence
Average of all field confidence scores:
```python
overall_confidence = sum(field_confidences) / len(field_confidences)
```

### Confidence Thresholds
- **✅ Auto-approve**: 0.90+ (future feature)
- **👁️ Review Required**: 0.70-0.89 (current default)
- **⚠️ Low Quality**: < 0.70 (flag for manual review)

---

## Auto-Categorization

### Keyword-Based System
Simple keyword matching for 13 expense categories:

#### Category Mappings
```python
{
    "מזון ושתייה": ["מסעדה", "קפה", "פיצה", "המבורגר", "סושי"],
    "תחבורה": ["דלק", "דיזל", "תדלוק", "paz", "delek", "חניה"],
    "ציוד משרדי": ["משרד", "נייר", "מדפסת", "office"],
    "שיווק ופרסום": ["פרסום", "שיווק", "google", "facebook"],
    "אינטרנט וטלפון": ["סלקום", "פרטנר", "הוט", "בזק"],
    # ... 8 more categories
}
```

### Accuracy
- **Target**: 70% correct categorization
- **Fallback**: Manual categorization by user
- **Future**: ML-based categorization (Phase 2)

---

## Duplicate Detection

### Detection Logic
Receipts considered duplicates if **ALL** conditions match:
1. **Same user**
2. **Same vendor name** (exact match)
3. **Date within ±1 day**
4. **Amount within ±5%**
5. **Not failed status**

### Example
```python
Original:  Cafe Cafe, 01/11/2024, ₪85.00
Duplicate: Cafe Cafe, 01/11/2024, ₪86.00  # 1.2% difference - DUPLICATE
Not Dupe:  Cafe Cafe, 03/11/2024, ₪85.00  # 2 days later - NOT DUPLICATE
```

---

## Error Handling

### Retry Strategy
Exponential backoff with 3 attempts:
```python
Attempt 1: Immediate
Attempt 2: Wait 2 seconds
Attempt 3: Wait 4 seconds
Attempt 4: Wait 8 seconds (max 3 retries)
```

### Common Errors

#### Vision API Errors
| Error | Cause | Solution |
|-------|-------|----------|
| `QUOTA_EXCEEDED` | API quota limit | Wait or upgrade plan |
| `INVALID_IMAGE` | Corrupted/invalid file | Re-upload image |
| `IMAGE_TOO_LARGE` | File > 10MB | Compress image |
| `UNSUPPORTED_FORMAT` | Wrong file type | Convert to JPG/PNG |

#### Parsing Errors
- **No text found**: Image too blurry → Mark for manual entry
- **Invalid date**: Format not recognized → Set to null
- **No amounts**: Pattern mismatch → Set to null
- **Invalid business number**: Wrong format → Set to null

### Error Response Format
```json
{
  "success": false,
  "error": "Vision API error: QUOTA_EXCEEDED",
  "full_text": "",
  "parsed_data": {}
}
```

---

## Performance Metrics

### Processing Times
- **OCR Extraction**: 2-5 seconds (Google Vision)
- **Text Parsing**: < 0.1 seconds
- **Total Pipeline**: 3-7 seconds

### Accuracy Targets
| Field | Target Accuracy | Current Estimate |
|-------|----------------|------------------|
| Vendor Name | 90% | 85% |
| Business Number | 95% | 90% |
| Total Amount | 95% | 80% |
| Date | 90% | 80% |
| VAT Amount | 85% | 85% |
| Overall | 90% | 80% |

**Note**: Current estimates based on limited testing. Will improve with production data.

---

## Usage Examples

### Basic OCR Extraction
```python
from app.services.ocr_service import ocr_service

# Extract text from receipt
result = await ocr_service.extract_text_from_url(
    "https://s3.amazonaws.com/receipts/123.jpg"
)

if result["success"]:
    print(f"Vendor: {result['parsed_data']['vendor_name']}")
    print(f"Amount: {result['parsed_data']['total_amount']}")
    print(f"Confidence: {result['parsed_data']['confidence']}")
else:
    print(f"Error: {result['error']}")
```

### With Retry Logic
```python
# Retry up to 3 times with exponential backoff
result = await ocr_service.retry_extraction(
    image_url="https://s3.amazonaws.com/receipts/456.jpg"
)
```

### Full Processing Pipeline
```python
from app.services.receipt_service import receipt_service

# Process receipt (OCR + categorize + duplicate check)
await receipt_service.process_receipt(
    receipt_id=123,
    db=db_session
)
```

---

## Configuration

### Environment Variables
```bash
# Google Cloud Vision credentials
GOOGLE_CLOUD_VISION_CREDENTIALS=/path/to/service-account.json

# OCR settings
OCR_CONFIDENCE_THRESHOLD=0.8

# Israeli VAT rate
VAT_RATE=0.17
```

### Google Cloud Setup
1. Create GCP project
2. Enable Vision API
3. Create service account
4. Download JSON credentials
5. Set `GOOGLE_CLOUD_VISION_CREDENTIALS` path

---

## Testing

### Run Unit Tests
```bash
pytest tests/services/test_ocr_service.py -v
```

### Run Integration Tests
```bash
pytest tests/integration/test_ocr_integration.py -v
```

### Test Coverage Target
- **Unit Tests**: 90%+
- **Integration Tests**: 80%+
- **E2E Tests**: Key workflows covered

---

## Limitations & Known Issues

### Current Limitations
1. **Handwritten receipts**: Not supported (print only)
2. **Thermal receipts**: Faded text may fail
3. **Non-Israeli formats**: Optimized for Israeli receipts
4. **Multiple currencies**: Only ILS (₪) supported
5. **Image quality**: Requires clear, well-lit photos

### Known Issues
1. **Date ambiguity**: DD/MM vs MM/DD can confuse parser
2. **Vendor name**: Sometimes includes address or extra text
3. **Amount extraction**: Multiple prices can cause confusion
4. **Hebrew OCR**: ~5% character recognition errors

### Workarounds
- **Poor quality**: Manual data entry fallback
- **Ambiguous dates**: User review required
- **Multiple amounts**: Selects largest as total (usually correct)

---

## Improvements Roadmap

### Phase 1 (MVP) ✅
- [x] Basic Hebrew OCR
- [x] Field extraction
- [x] Confidence scoring
- [x] Retry logic

### Phase 2 (Q1 2026)
- [ ] ML-based categorization
- [ ] Smart field validation
- [ ] Auto-correction for common errors
- [ ] Support for thermal receipt enhancement

### Phase 3 (Q2 2026)
- [ ] Multi-page invoice support
- [ ] Table extraction (itemized receipts)
- [ ] Handwriting recognition
- [ ] Multi-currency support

---

## Support & Troubleshooting

### Common Questions

**Q: Why is accuracy lower than expected?**
A: Image quality is key. Ensure good lighting, focus, and resolution (300+ DPI).

**Q: What if OCR fails completely?**
A: Receipt status set to `FAILED`. User can manually enter data.

**Q: Can I reprocess a failed receipt?**
A: Yes, trigger re-processing from admin panel (future feature).

**Q: How to improve categorization?**
A: Add more keywords to category mappings or use ML (Phase 2).

### Debug Mode
Enable detailed logging:
```python
import logging
logging.getLogger('app.services.ocr_service').setLevel(logging.DEBUG)
```

---

## API Reference

### `OCRService.extract_text_from_url(image_url)`
Extract text from receipt image.

**Parameters:**
- `image_url` (str): S3 URL to receipt image

**Returns:**
```python
{
    "success": bool,
    "full_text": str,
    "parsed_data": {
        "vendor_name": str | None,
        "business_number": str | None,
        "receipt_number": str | None,
        "receipt_date": str | None,  # YYYY-MM-DD
        "total_amount": float | None,
        "vat_amount": float | None,
        "pre_vat_amount": float | None,
        "confidence": {
            "vendor_name": float,
            "business_number": float,
            # ... etc
        }
    },
    "raw_response": dict
}
```

### `OCRService.retry_extraction(image_url, attempt=1)`
Retry OCR with exponential backoff.

**Parameters:**
- `image_url` (str): S3 URL to receipt image
- `attempt` (int): Starting attempt number (default: 1)

**Returns:** Same as `extract_text_from_url()`

---

## License
Internal Tik-Tax documentation. Confidential.

**Last Updated**: November 4, 2025
**Version**: 1.0.0
**Maintainer**: Tik-Tax Development Team
