# Duplicate Detection & Search - Quick Reference

## Quick Start

### Check for Duplicates
```bash
curl -X POST "https://api.tiktax.co.il/api/v1/receipts/check-duplicate" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "vendor_name": "סופר מרקט",
    "receipt_date": "2024-11-01T10:30:00",
    "total_amount": 150.50
  }'
```

### Search Receipts
```bash
curl -X GET "https://api.tiktax.co.il/api/v1/receipts/search?q=סופר&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## API Endpoints

### POST /api/v1/receipts/check-duplicate
**Purpose**: Check if receipt is a duplicate before saving

**Request**:
- `vendor_name` (required): Vendor name
- `receipt_date` (required): Receipt date (ISO 8601)
- `total_amount` (required): Total amount (positive number)

**Response**:
- `is_duplicate`: Boolean
- `duplicate_receipt_id`: ID of similar receipt (if found)
- `similarity_score`: 0-100 percentage
- `message`: Hebrew message

**Thresholds**:
- Date: ±1 day
- Amount: ±5%
- Vendor similarity: 80%+ = duplicate

---

### GET /api/v1/receipts/search
**Purpose**: Search all receipt fields

**Parameters**:
- `q` (required): Search query (2-100 chars)
- `limit` (optional): Max results (1-100, default: 20)

**Response**:
- `results`: Array of matching receipts
- `total`: Total count
- `query`: Original search query

**Searched Fields**:
1. Vendor name (weight: 50-100)
2. Receipt number (weight: 60-100)
3. Business number (weight: 50-80)
4. Notes (weight: 20)

---

## Code Examples

### TypeScript/React - Duplicate Warning
```typescript
interface DuplicateCheckRequest {
  vendor_name: string;
  receipt_date: string;
  total_amount: number;
}

async function checkDuplicate(data: DuplicateCheckRequest) {
  const response = await fetch('/api/v1/receipts/check-duplicate', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });
  
  return await response.json();
}

// Usage
const result = await checkDuplicate({
  vendor_name: "סופר מרקט",
  receipt_date: "2024-11-01T10:30:00",
  total_amount: 150.50
});

if (result.is_duplicate) {
  const confirm = window.confirm(
    `נמצאה קבלה דומה (${result.similarity_score}% דמיון). להמשיך?`
  );
  if (!confirm) return;
}
```

### TypeScript/React - Search Bar
```typescript
import { debounce } from 'lodash';

const searchReceipts = debounce(async (query: string) => {
  if (query.length < 2) return;
  
  const response = await fetch(
    `/api/v1/receipts/search?q=${encodeURIComponent(query)}&limit=10`,
    {
      headers: { 'Authorization': `Bearer ${token}` }
    }
  );
  
  const data = await response.json();
  setSearchResults(data.results);
}, 300);

// In component
<input 
  onChange={(e) => searchReceipts(e.target.value)}
  placeholder="חפש קבלות..."
/>
```

### Python - Backend Service
```python
from app.utils.text_utils import normalize_hebrew_text
from difflib import SequenceMatcher

def calculate_similarity(vendor1: str, vendor2: str) -> float:
    """Calculate vendor name similarity"""
    norm1 = normalize_hebrew_text(vendor1)
    norm2 = normalize_hebrew_text(vendor2)
    return SequenceMatcher(None, norm1, norm2).ratio() * 100
```

---

## Testing

### Run Unit Tests
```bash
cd backend
pytest tests/utils/test_text_utils.py -v
```

### Run Integration Tests
```bash
pytest tests/integration/test_duplicate_search.py -v
```

### Run All Tests
```bash
pytest tests/ -v --cov=app
```

### Manual Testing
```bash
python test_duplicate_search_manual.py
```

---

## Common Use Cases

### 1. Prevent Duplicate on Upload
```typescript
// Before submitting receipt
const duplicate = await checkDuplicate(receiptData);
if (duplicate.is_duplicate) {
  showWarning(`Duplicate found: ${duplicate.similarity_score}%`);
}
```

### 2. Search While Typing
```typescript
// Debounced search in header
<SearchBar onSearch={searchReceipts} />
```

### 3. Find Similar Receipts
```typescript
// In receipt detail view
const similar = await searchReceipts(receipt.vendor_name);
showSimilarReceipts(similar.results);
```

---

## Troubleshooting

### Low Similarity Scores
**Issue**: Similar vendors not matching  
**Fix**: Check Hebrew normalization is applied

### No Search Results
**Issue**: Hebrew text not found  
**Fix**: Ensure UTF-8 encoding and minimum 2 characters

### Slow Performance
**Issue**: Search taking too long  
**Fix**: Add database indexes on searchable fields

---

## Key Functions

### Text Normalization
```python
normalize_hebrew_text(text: str) -> str
```
- Removes nikud (Hebrew diacritics)
- Removes special characters
- Converts to lowercase
- Normalizes whitespace

### Business Number Cleaning
```python
clean_business_number(number: str) -> str
```
- Removes non-digits
- Pads to 9 digits
- Returns empty string if invalid

### Hebrew Detection
```python
is_hebrew(text: str) -> bool
```
- Checks for Hebrew characters (U+0590-U+05FF)
- Returns True if any Hebrew found

---

## Database Indexes (Recommended)

```sql
CREATE INDEX idx_receipts_vendor_name ON receipts(vendor_name);
CREATE INDEX idx_receipts_receipt_number ON receipts(receipt_number);
CREATE INDEX idx_receipts_business_number ON receipts(business_number);
CREATE INDEX idx_receipts_date_amount ON receipts(receipt_date, total_amount);
CREATE INDEX idx_receipts_user_status ON receipts(user_id, status);
```

---

## Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| 200 | Success | - |
| 400 | Bad request | Check request format |
| 401 | Unauthorized | Add auth token |
| 422 | Validation error | Check field constraints |
| 500 | Server error | Contact support |

---

## Validation Rules

### Duplicate Check
- `vendor_name`: 1-200 characters
- `receipt_date`: Valid ISO 8601 datetime
- `total_amount`: Positive number

### Search
- `q`: 2-100 characters
- `limit`: 1-100 (default: 20)

---

## Performance Tips

1. **Use debouncing** for search (300ms recommended)
2. **Limit results** to necessary amount
3. **Add indexes** on searchable fields
4. **Cache** frequent searches
5. **Filter first** before fuzzy matching

---

## Security Notes

- ✅ All endpoints require authentication
- ✅ Users can only access their own receipts
- ✅ Input validation on all fields
- ✅ SQL injection protection (ORM)
- ✅ No sensitive data in URLs

---

## Support

- **Documentation**: `/backend/DUPLICATE_SEARCH_API.md`
- **Implementation**: `/backend/IMPLEMENTATION_DUPLICATE_SEARCH.md`
- **Tests**: `/backend/tests/integration/test_duplicate_search.py`

---

**Version**: 1.0.0  
**Last Updated**: November 4, 2024
