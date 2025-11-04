# Statistics API - Quick Reference

## 🎯 Endpoints

```
GET /api/v1/statistics/dashboard       # Dashboard stats
GET /api/v1/statistics/yearly          # Yearly report
GET /api/v1/statistics/category/{id}   # Category stats
```

---

## 📊 Dashboard Statistics

### Request
```bash
curl -X GET "https://api.tiktax.co.il/api/v1/statistics/dashboard" \
  -H "Authorization: Bearer TOKEN"
```

### Response (Key Fields)
```json
{
  "monthly_receipts": 25,           // This month count
  "monthly_amount": 3500.75,        // This month total (₪)
  "monthly_average": 140.03,        // Average per receipt
  "receipts_change_percent": 25.0,  // % change from last month
  "amount_change_percent": 25.0,    // % change from last month
  "usage_percentage": 50.0,         // Subscription usage %
  "categories": [...],              // Top 5 categories
  "recent_receipts": [...],         // Last 5 receipts
  "monthly_trend": [...]            // 6-month trend
}
```

---

## 📅 Yearly Report

### Request
```bash
# Current year
curl -X GET "https://api.tiktax.co.il/api/v1/statistics/yearly" \
  -H "Authorization: Bearer TOKEN"

# Specific year
curl -X GET "https://api.tiktax.co.il/api/v1/statistics/yearly?year=2024" \
  -H "Authorization: Bearer TOKEN"
```

### Response (Key Fields)
```json
{
  "year": 2024,
  "total_receipts": 300,
  "total_amount": 42000.00,
  "total_vat": 7140.00,
  "categories": [...],        // All categories
  "monthly_breakdown": [...]  // 12 months
}
```

---

## 🏷️ Category Statistics

### Request
```bash
# All time
curl -X GET "https://api.tiktax.co.il/api/v1/statistics/category/1" \
  -H "Authorization: Bearer TOKEN"

# Specific year
curl -X GET "https://api.tiktax.co.il/api/v1/statistics/category/1?year=2024" \
  -H "Authorization: Bearer TOKEN"

# Specific month
curl -X GET "https://api.tiktax.co.il/api/v1/statistics/category/1?year=2024&month=1" \
  -H "Authorization: Bearer TOKEN"
```

### Response
```json
{
  "category_id": 1,
  "category_name": "משרד",
  "count": 15,
  "total_amount": 2400.50,
  "percentage": 32.5
}
```

---

## 🔧 JavaScript Usage

### Fetch Dashboard
```javascript
const response = await axios.get('/api/v1/statistics/dashboard', {
  headers: { Authorization: `Bearer ${token}` }
});

const { monthly_receipts, monthly_amount, usage_percentage } = response.data;
```

### Fetch Yearly Report
```javascript
const response = await axios.get('/api/v1/statistics/yearly', {
  params: { year: 2024 },
  headers: { Authorization: `Bearer ${token}` }
});

const { total_amount, total_vat } = response.data;
```

### Fetch Category Stats
```javascript
const response = await axios.get(`/api/v1/statistics/category/${categoryId}`, {
  params: { year: 2024, month: 1 },
  headers: { Authorization: `Bearer ${token}` }
});

const { count, total_amount } = response.data;
```

---

## 🐍 Python Usage

### Fetch Dashboard
```python
import requests

headers = {"Authorization": f"Bearer {token}"}
response = requests.get("https://api.tiktax.co.il/api/v1/statistics/dashboard", headers=headers)
data = response.json()

print(f"Monthly receipts: {data['monthly_receipts']}")
print(f"Usage: {data['usage_percentage']}%")
```

### Fetch Yearly Report
```python
response = requests.get(
    "https://api.tiktax.co.il/api/v1/statistics/yearly",
    params={"year": 2024},
    headers=headers
)
data = response.json()

print(f"Total: ₪{data['total_amount']}")
print(f"VAT: ₪{data['total_vat']}")
```

---

## ⚡ Performance

### Response Times (Target)
- Dashboard: < 500ms
- Yearly: < 300ms
- Category: < 100ms

### Caching (Recommended)
- Dashboard: 5 minutes
- Yearly: 1 hour
- Category: 10 minutes

### Rate Limits
- Dashboard: 60/min
- Yearly: 30/min
- Category: 60/min

---

## ❌ Error Codes

| Code | Status | Description |
|------|--------|-------------|
| 401 | Unauthorized | Invalid/missing token |
| 404 | Not Found | Category doesn't exist |
| 400 | Bad Request | Invalid year/month |
| 500 | Server Error | Statistics error |

---

## 🧪 Testing

### Run Tests
```bash
# All statistics tests
pytest backend/tests/api/test_statistics.py -v

# Specific test
pytest backend/tests/api/test_statistics.py::TestDashboardStatistics::test_dashboard_stats_with_receipts -v

# With coverage
pytest backend/tests/api/test_statistics.py --cov=app.api.v1.endpoints.statistics --cov-report=html
```

### Manual Testing
```bash
# 1. Start server
cd backend
uvicorn app.main:app --reload

# 2. Get token
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  | jq -r '.access_token')

# 3. Test endpoints
curl -X GET "http://localhost:8000/api/v1/statistics/dashboard" \
  -H "Authorization: Bearer $TOKEN" | jq

curl -X GET "http://localhost:8000/api/v1/statistics/yearly?year=2024" \
  -H "Authorization: Bearer $TOKEN" | jq

curl -X GET "http://localhost:8000/api/v1/statistics/category/1" \
  -H "Authorization: Bearer $TOKEN" | jq
```

---

## 📁 File Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   └── statistics.py       # ✨ Endpoints
│   │       └── router.py                # Updated
│   └── schemas/
│       └── statistics.py                # ✨ Schemas
├── tests/
│   └── api/
│       └── test_statistics.py           # ✨ Tests
└── docs/
    ├── STATISTICS_API_DOCUMENTATION.md   # ✨ API docs
    ├── STATISTICS_PERFORMANCE.md         # ✨ Performance guide
    └── STATISTICS_IMPLEMENTATION_SUMMARY.md  # ✨ Summary
```

---

## 🚀 Quick Start

### 1. Verify Installation
```bash
cd backend
python verify_statistics.py
```

### 2. Run Tests
```bash
pytest tests/api/test_statistics.py -v
```

### 3. Start Server
```bash
uvicorn app.main:app --reload
```

### 4. View API Docs
```
http://localhost:8000/docs
```

### 5. Test Endpoints
Use examples above or Swagger UI

---

## 📖 Full Documentation

- **API Reference**: `STATISTICS_API_DOCUMENTATION.md`
- **Performance Guide**: `STATISTICS_PERFORMANCE.md`
- **Implementation Summary**: `STATISTICS_IMPLEMENTATION_SUMMARY.md`

---

## ✅ Checklist

- [x] Schemas created
- [x] Endpoints implemented
- [x] Router updated
- [x] Tests written
- [x] Documentation complete
- [ ] Tests passing
- [ ] Server running
- [ ] Ready for deployment

---

**Need help?** Check the full documentation files!
