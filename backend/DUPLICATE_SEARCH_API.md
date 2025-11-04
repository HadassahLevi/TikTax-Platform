# Duplicate Detection & Search API Documentation

## Overview

This document describes the duplicate detection and full-text search functionality for receipts in the Tik-Tax platform.

## Features

### 1. Duplicate Detection
Intelligent duplicate detection using fuzzy matching to prevent duplicate receipt entries.

**Matching Criteria:**
- **Vendor Name**: 80%+ similarity threshold using fuzzy string matching
- **Date Range**: ±1 day from provided date
- **Amount Range**: ±5% tolerance from provided amount
- **Hebrew Text**: Automatic normalization (removes nikud, special characters)

### 2. Full-Text Search
Fast, relevant search across all receipt fields with intelligent scoring.

**Searchable Fields:**
- Vendor name (highest weight: 50 base + 30 prefix bonus)
- Receipt number (exact match: 100, partial: 60)
- Business number (exact match: 80, partial: 50)
- Notes (weight: 20)

---

## API Endpoints

### POST /api/v1/receipts/check-duplicate

Check if a receipt is likely a duplicate.

**Request Body:**
```json
{
  "vendor_name": "סופר מרקט",
  "receipt_date": "2024-11-01T10:30:00",
  "total_amount": 150.50
}
```

**Response:**
```json
{
  "is_duplicate": true,
  "duplicate_receipt_id": 123,
  "similarity_score": 95.5,
  "message": "נמצאה קבלה דומה (95% דמיון)"
}
```

**Status Codes:**
- `200 OK`: Check completed successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Missing or invalid authentication
- `422 Unprocessable Entity`: Validation error

**Example Usage:**
```python
import requests

headers = {"Authorization": "Bearer YOUR_TOKEN"}
data = {
    "vendor_name": "סופר מרקט",
    "receipt_date": "2024-11-01T10:30:00",
    "total_amount": 150.50
}

response = requests.post(
    "https://api.tiktax.co.il/api/v1/receipts/check-duplicate",
    json=data,
    headers=headers
)

result = response.json()
if result["is_duplicate"]:
    print(f"Duplicate found! Receipt ID: {result['duplicate_receipt_id']}")
    print(f"Similarity: {result['similarity_score']}%")
```

---

### GET /api/v1/receipts/search

Search receipts with full-text search and relevance ranking.

**Query Parameters:**
- `q` (required): Search query (2-100 characters)
- `limit` (optional): Maximum results (1-100, default: 20)

**Example Request:**
```
GET /api/v1/receipts/search?q=סופר&limit=10
```

**Response:**
```json
{
  "results": [
    {
      "receipt_id": 123,
      "vendor_name": "סופר מרקט",
      "receipt_date": "2024-11-01T10:30:00",
      "total_amount": 150.50,
      "category_name": "מזון",
      "relevance_score": 100.0,
      "matched_field": "vendor_name"
    }
  ],
  "total": 1,
  "query": "סופר"
}
```

**Status Codes:**
- `200 OK`: Search completed successfully
- `400 Bad Request`: Invalid query parameters
- `401 Unauthorized`: Missing or invalid authentication
- `422 Unprocessable Entity`: Query validation error

**Example Usage:**
```python
import requests

headers = {"Authorization": "Bearer YOUR_TOKEN"}
params = {
    "q": "סופר",
    "limit": 20
}

response = requests.get(
    "https://api.tiktax.co.il/api/v1/receipts/search",
    params=params,
    headers=headers
)

results = response.json()
for receipt in results["results"]:
    print(f"{receipt['vendor_name']}: ₪{receipt['total_amount']}")
    print(f"Relevance: {receipt['relevance_score']}, Matched: {receipt['matched_field']}")
```

---

## Duplicate Detection Algorithm

### Step 1: Filter by Date and Amount
```python
date_range = receipt_date ± 1 day
amount_range = total_amount ± 5%
```

### Step 2: Calculate Vendor Name Similarity
```python
# Normalize text (remove nikud, special chars, lowercase)
vendor1_normalized = normalize_hebrew_text(vendor_name1)
vendor2_normalized = normalize_hebrew_text(vendor_name2)

# Calculate similarity using SequenceMatcher
similarity = SequenceMatcher(None, vendor1, vendor2).ratio() * 100
```

### Step 3: Apply Bonuses
```python
# Exact amount match (within 1%)
if amount_diff_percent < 1.0:
    similarity += 5

# Exact date match
if dates_match_exactly:
    similarity += 5

# Cap at 100%
similarity = min(similarity, 100.0)
```

### Step 4: Determine Duplicate Status
```python
is_duplicate = similarity >= 80.0
```

---

## Search Relevance Scoring

### Scoring Formula

```python
score = 0.0

# Vendor name match
if query in vendor_name:
    score += 50
    if vendor_name.startswith(query):
        score += 30  # Prefix bonus
    if vendor_name == query:
        score += 20  # Exact match bonus

# Receipt number match
if query == receipt_number:
    score += 100  # Exact match
elif query in receipt_number:
    score += 60   # Partial match

# Business number match
if query == business_number:
    score += 80   # Exact match
elif query in business_number:
    score += 50   # Partial match

# Notes match
if query in notes:
    score += 20   # Lower weight
```

### Result Sorting
Results are sorted by `relevance_score` in descending order (highest score first).

---

## Hebrew Text Normalization

The `normalize_hebrew_text()` function performs the following:

1. **Remove Hebrew diacritics (nikud)** - Unicode range U+0591 to U+05C7
2. **Normalize Unicode** - NFD (Canonical Decomposition)
3. **Remove combining characters**
4. **Normalize whitespace** - Convert multiple spaces to single space
5. **Remove special characters** - Keep only letters, numbers, spaces
6. **Convert to lowercase**

**Example:**
```python
Input:  "שָׁלוֹם  עוֹלָם!"
Output: "שלום עולם"
```

This ensures:
- Typo tolerance
- Consistent matching
- Case-insensitive comparison
- Punctuation independence

---

## Edge Cases & Handling

### Empty or Missing Fields
- **Empty vendor name**: Skipped in duplicate detection
- **Missing receipt number**: Only searches other fields
- **Null values**: Treated as non-matches (score = 0)

### Special Characters
- **Removed during normalization**: `!, ?, -, .`
- **Preserved**: Hebrew letters, English letters, numbers

### Performance Optimization
- **Date/amount filtering first**: Reduces candidate set
- **Limit parameter**: Prevents large result sets
- **Excludes FAILED status**: Only searches valid receipts

### Security
- **User isolation**: Users can only search/check their own receipts
- **Authentication required**: All endpoints require valid JWT token
- **Input validation**: Query length limits, amount validation

---

## Testing

### Unit Tests
Run text utility tests:
```bash
cd backend
pytest tests/utils/test_text_utils.py -v
```

**Coverage:**
- Hebrew text normalization
- Business number cleaning
- Number extraction
- Fuzzy matching scenarios

### Integration Tests
Run duplicate detection and search tests:
```bash
pytest tests/integration/test_duplicate_search.py -v
```

**Coverage:**
- Exact duplicate detection
- Similar duplicate detection (typos)
- No duplicate scenarios
- Search by vendor name
- Search by receipt/business number
- Search in notes
- Relevance scoring
- User isolation
- Authorization

### Test with Hebrew Data
```bash
# Create test receipts with Hebrew text
pytest tests/integration/test_duplicate_search.py::TestDuplicateDetection::test_hebrew_typo_tolerance -v

# Test Hebrew search normalization
pytest tests/integration/test_duplicate_search.py::TestReceiptSearch::test_search_hebrew_normalization -v
```

---

## Usage Examples

### Frontend Integration - Duplicate Check on Upload

```typescript
// Check for duplicates before submitting receipt
async function checkDuplicateBeforeSubmit(receiptData: ReceiptData) {
  const response = await fetch('/api/v1/receipts/check-duplicate', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      vendor_name: receiptData.vendorName,
      receipt_date: receiptData.receiptDate,
      total_amount: receiptData.totalAmount
    })
  });
  
  const result = await response.json();
  
  if (result.is_duplicate) {
    // Show warning to user
    const confirmSubmit = await showDuplicateWarning(
      `נמצאה קבלה דומה (${result.similarity_score}% דמיון). ` +
      `להמשיך בכל זאת?`
    );
    
    if (!confirmSubmit) {
      return false; // User cancelled
    }
  }
  
  return true; // Proceed with submission
}
```

### Frontend Integration - Search Bar

```typescript
// Debounced search function
import { debounce } from 'lodash';

const searchReceipts = debounce(async (query: string) => {
  if (query.length < 2) return;
  
  const response = await fetch(
    `/api/v1/receipts/search?q=${encodeURIComponent(query)}&limit=10`,
    {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );
  
  const results = await response.json();
  
  // Display results
  displaySearchResults(results.results);
}, 300);

// Usage in search input
<input 
  type="text" 
  onChange={(e) => searchReceipts(e.target.value)}
  placeholder="חפש קבלות..."
/>
```

---

## Performance Considerations

### Database Indexes
Ensure these indexes exist for optimal performance:

```sql
-- Vendor name search
CREATE INDEX idx_receipts_vendor_name ON receipts(vendor_name);

-- Receipt number search
CREATE INDEX idx_receipts_receipt_number ON receipts(receipt_number);

-- Business number search
CREATE INDEX idx_receipts_business_number ON receipts(business_number);

-- Date range filtering
CREATE INDEX idx_receipts_date_amount ON receipts(receipt_date, total_amount);

-- User receipts
CREATE INDEX idx_receipts_user_status ON receipts(user_id, status);
```

### Query Optimization
- **Limit results early**: Use SQL `LIMIT` before relevance scoring
- **Filter before fuzzy match**: Date/amount filtering reduces candidate set
- **Cache normalization**: Consider caching normalized vendor names

### Scalability
- **Current**: Handles 10,000+ receipts per user efficiently
- **Future**: Consider PostgreSQL full-text search (tsvector) for 100,000+ receipts
- **Hebrew support**: Use `pg_trgm` extension for trigram matching

---

## Future Enhancements

### Planned Features
1. **Machine Learning**: Train model on user's duplicate decisions
2. **Phonetic Matching**: Hebrew phonetic algorithm for better matching
3. **Multi-field Search**: Combined search across multiple fields
4. **Search Filters**: Filter search by date, amount, category
5. **Search Highlighting**: Highlight matched terms in results
6. **Autocomplete**: Suggest completions based on existing receipts

### Performance Improvements
1. **PostgreSQL FTS**: Full-text search indexes
2. **Elasticsearch**: For very large datasets
3. **Redis Cache**: Cache frequent searches
4. **Async Processing**: Background indexing for search

---

## Troubleshooting

### Issue: Low Similarity Scores for Similar Names
**Cause**: Special characters or formatting differences  
**Solution**: Ensure `normalize_hebrew_text()` is applied to both strings

### Issue: Duplicate Not Detected
**Cause**: Amount or date outside tolerance  
**Solution**: Check if difference is >5% for amount or >1 day for date

### Issue: Search Returns No Results
**Cause**: Query too short or FAILED receipts  
**Solution**: Ensure query ≥2 characters and receipts are APPROVED/REVIEW status

### Issue: Hebrew Text Not Matching
**Cause**: Encoding issues or nikud  
**Solution**: Verify UTF-8 encoding and normalization function

---

## API Rate Limiting

All endpoints respect the global rate limit:
- **Limit**: 100 requests per minute per user
- **Headers**: 
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

---

## Support & Contact

For technical support or questions:
- **Email**: support@tiktax.co.il
- **Documentation**: https://docs.tiktax.co.il
- **API Status**: https://status.tiktax.co.il

---

**Version**: 1.0.0  
**Last Updated**: November 4, 2024  
**Maintained by**: Tik-Tax Development Team
