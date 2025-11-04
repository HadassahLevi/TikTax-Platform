# Statistics API Documentation

## Overview
The Statistics API provides comprehensive analytics and reporting endpoints for the Tik-Tax dashboard, yearly tax reports, and category-specific statistics.

**Base URL:** `/api/v1/statistics`  
**Authentication:** Required (Bearer token)

---

## Endpoints

### 1. Dashboard Statistics
Get comprehensive dashboard analytics with monthly trends, category breakdown, and subscription usage.

**Endpoint:** `GET /api/v1/statistics/dashboard`  
**Authentication:** Required  
**Rate Limit:** 60 requests/minute

#### Request
```http
GET /api/v1/statistics/dashboard HTTP/1.1
Host: api.tiktax.co.il
Authorization: Bearer <access_token>
```

#### Response
```json
{
  "total_receipts": 150,
  "approved_receipts": 145,
  "pending_receipts": 5,
  "monthly_receipts": 25,
  "monthly_amount": 3500.75,
  "monthly_average": 140.03,
  "prev_monthly_receipts": 20,
  "prev_monthly_amount": 2800.50,
  "receipts_change_percent": 25.0,
  "amount_change_percent": 25.0,
  "receipts_limit": 50,
  "receipts_used": 25,
  "receipts_remaining": 25,
  "usage_percentage": 50.0,
  "categories": [
    {
      "category_id": 1,
      "category_name": "משרד",
      "count": 8,
      "total_amount": 1200.50,
      "percentage": 35.2
    }
  ],
  "recent_receipts": [
    {
      "id": 123,
      "vendor_name": "סופר פארם",
      "receipt_date": "2024-01-15T10:30:00",
      "total_amount": 450.0,
      "category_name": "בריאות"
    }
  ],
  "monthly_trend": [
    {
      "month": "2024-01",
      "total_receipts": 15,
      "total_amount": 2450.50,
      "average_amount": 163.37
    }
  ]
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `total_receipts` | integer | Total receipts all time |
| `approved_receipts` | integer | Total approved receipts |
| `pending_receipts` | integer | Receipts awaiting review |
| `monthly_receipts` | integer | Receipts in current month |
| `monthly_amount` | float | Total amount current month (₪) |
| `monthly_average` | float | Average amount per receipt |
| `prev_monthly_receipts` | integer | Previous month receipt count |
| `prev_monthly_amount` | float | Previous month total (₪) |
| `receipts_change_percent` | float | Month-over-month change (%) |
| `amount_change_percent` | float | Month-over-month change (%) |
| `receipts_limit` | integer | Monthly receipt limit |
| `receipts_used` | integer | Receipts used this month |
| `receipts_remaining` | integer | Receipts remaining |
| `usage_percentage` | float | Subscription usage (%) |
| `categories` | array | Top 5 categories by spending |
| `recent_receipts` | array | Last 5 approved receipts |
| `monthly_trend` | array | Last 6 months trend data |

#### Error Responses

**401 Unauthorized**
```json
{
  "detail": "Could not validate credentials"
}
```

**500 Internal Server Error**
```json
{
  "detail": "Failed to fetch dashboard statistics"
}
```

#### Example Usage

**cURL**
```bash
curl -X GET "https://api.tiktax.co.il/api/v1/statistics/dashboard" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**JavaScript (Axios)**
```javascript
const response = await axios.get('/api/v1/statistics/dashboard', {
  headers: {
    Authorization: `Bearer ${accessToken}`
  }
});

console.log('Monthly receipts:', response.data.monthly_receipts);
console.log('Usage:', response.data.usage_percentage + '%');
```

**Python**
```python
import requests

headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(
    "https://api.tiktax.co.il/api/v1/statistics/dashboard",
    headers=headers
)

data = response.json()
print(f"Monthly receipts: {data['monthly_receipts']}")
print(f"Usage: {data['usage_percentage']}%")
```

---

### 2. Yearly Report
Get comprehensive yearly tax report with category and monthly breakdown.

**Endpoint:** `GET /api/v1/statistics/yearly`  
**Authentication:** Required  
**Rate Limit:** 30 requests/minute

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `year` | integer | No | Year for report (defaults to current year) |

#### Request
```http
GET /api/v1/statistics/yearly?year=2024 HTTP/1.1
Host: api.tiktax.co.il
Authorization: Bearer <access_token>
```

#### Response
```json
{
  "year": 2024,
  "total_receipts": 300,
  "total_amount": 42000.00,
  "total_vat": 7140.00,
  "categories": [
    {
      "category_id": 1,
      "category_name": "משרד",
      "count": 80,
      "total_amount": 12000.00,
      "percentage": 28.6
    },
    {
      "category_id": 2,
      "category_name": "דלק",
      "count": 50,
      "total_amount": 8000.00,
      "percentage": 19.0
    }
  ],
  "monthly_breakdown": [
    {
      "month": "2024-01",
      "total_receipts": 25,
      "total_amount": 3500.00,
      "average_amount": 140.00
    },
    {
      "month": "2024-02",
      "total_receipts": 28,
      "total_amount": 3800.00,
      "average_amount": 135.71
    }
  ]
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `year` | integer | Report year |
| `total_receipts` | integer | Total receipts for year |
| `total_amount` | float | Total amount for year (₪) |
| `total_vat` | float | Total VAT for year (₪) |
| `categories` | array | All categories breakdown |
| `monthly_breakdown` | array | 12-month breakdown |

#### Error Responses

**400 Bad Request**
```json
{
  "detail": "Year must be between 2000 and 2025"
}
```

**401 Unauthorized**
```json
{
  "detail": "Could not validate credentials"
}
```

#### Example Usage

**cURL**
```bash
# Current year
curl -X GET "https://api.tiktax.co.il/api/v1/statistics/yearly" \
  -H "Authorization: Bearer ${TOKEN}"

# Specific year
curl -X GET "https://api.tiktax.co.il/api/v1/statistics/yearly?year=2024" \
  -H "Authorization: Bearer ${TOKEN}"
```

**JavaScript**
```javascript
// Get 2024 tax report
const report = await axios.get('/api/v1/statistics/yearly', {
  params: { year: 2024 },
  headers: { Authorization: `Bearer ${token}` }
});

console.log('Total VAT:', report.data.total_vat);
console.log('Categories:', report.data.categories);
```

---

### 3. Category Statistics
Get detailed statistics for a specific category with optional date filtering.

**Endpoint:** `GET /api/v1/statistics/category/{category_id}`  
**Authentication:** Required  
**Rate Limit:** 60 requests/minute

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `category_id` | integer | Yes | Category ID |

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `year` | integer | No | Filter by year |
| `month` | integer | No | Filter by month (1-12) |

#### Request
```http
GET /api/v1/statistics/category/1?year=2024&month=1 HTTP/1.1
Host: api.tiktax.co.il
Authorization: Bearer <access_token>
```

#### Response
```json
{
  "category_id": 1,
  "category_name": "משרד",
  "count": 15,
  "total_amount": 2400.50,
  "percentage": 32.5
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `category_id` | integer | Category ID |
| `category_name` | string | Category name (Hebrew) |
| `count` | integer | Number of receipts |
| `total_amount` | float | Total amount (₪) |
| `percentage` | float | Percentage of total spending |

#### Error Responses

**404 Not Found**
```json
{
  "detail": "Category not found"
}
```

**400 Bad Request**
```json
{
  "detail": "Invalid month value"
}
```

#### Example Usage

**cURL**
```bash
# All time
curl -X GET "https://api.tiktax.co.il/api/v1/statistics/category/1" \
  -H "Authorization: Bearer ${TOKEN}"

# Specific year
curl -X GET "https://api.tiktax.co.il/api/v1/statistics/category/1?year=2024" \
  -H "Authorization: Bearer ${TOKEN}"

# Specific month
curl -X GET "https://api.tiktax.co.il/api/v1/statistics/category/1?year=2024&month=1" \
  -H "Authorization: Bearer ${TOKEN}"
```

**JavaScript**
```javascript
// Get office expenses for January 2024
const stats = await axios.get('/api/v1/statistics/category/1', {
  params: { year: 2024, month: 1 },
  headers: { Authorization: `Bearer ${token}` }
});

console.log('Office expenses:', stats.data.total_amount);
console.log('Receipt count:', stats.data.count);
```

---

## Data Models

### MonthlyStat
```typescript
interface MonthlyStat {
  month: string;           // YYYY-MM format
  total_receipts: number;  // >= 0
  total_amount: number;    // >= 0
  average_amount: number;  // >= 0
}
```

### CategoryBreakdown
```typescript
interface CategoryBreakdown {
  category_id: number;
  category_name: string;   // Hebrew name
  count: number;           // >= 0
  total_amount: number;    // >= 0
  percentage: number;      // 0-100
}
```

### RecentReceipt
```typescript
interface RecentReceipt {
  id: number;
  vendor_name: string | null;
  receipt_date: string | null;  // ISO 8601
  total_amount: number | null;
  category_name: string | null;
}
```

---

## Common Use Cases

### 1. Dashboard Widget
```javascript
// Fetch dashboard data
const dashboard = await api.get('/statistics/dashboard');

// Display monthly summary
console.log(`This month: ${dashboard.monthly_receipts} receipts`);
console.log(`Total: ₪${dashboard.monthly_amount.toFixed(2)}`);
console.log(`Change: ${dashboard.amount_change_percent > 0 ? '+' : ''}${dashboard.amount_change_percent}%`);

// Display usage
const usageColor = dashboard.usage_percentage > 80 ? 'red' : 'green';
console.log(`Usage: ${dashboard.usage_percentage}% (${usageColor})`);

// Display top categories
dashboard.categories.forEach(cat => {
  console.log(`${cat.category_name}: ₪${cat.total_amount} (${cat.percentage}%)`);
});
```

### 2. Tax Report Generation
```javascript
// Generate 2024 tax report
const report = await api.get('/statistics/yearly', {
  params: { year: 2024 }
});

// Export to PDF
const pdf = new jsPDF();
pdf.text(`Tax Report ${report.year}`, 10, 10);
pdf.text(`Total Receipts: ${report.total_receipts}`, 10, 20);
pdf.text(`Total Amount: ₪${report.total_amount.toFixed(2)}`, 10, 30);
pdf.text(`Total VAT: ₪${report.total_vat.toFixed(2)}`, 10, 40);

// Category breakdown
let y = 60;
report.categories.forEach(cat => {
  pdf.text(`${cat.category_name}: ₪${cat.total_amount.toFixed(2)}`, 10, y);
  y += 10;
});

pdf.save('tax-report-2024.pdf');
```

### 3. Category Analysis
```javascript
// Analyze office expenses for Q1 2024
const months = [1, 2, 3];
const officeExpenses = await Promise.all(
  months.map(month => 
    api.get('/statistics/category/1', {
      params: { year: 2024, month }
    })
  )
);

const q1Total = officeExpenses.reduce(
  (sum, data) => sum + data.total_amount, 
  0
);

console.log(`Q1 Office Expenses: ₪${q1Total.toFixed(2)}`);
```

### 4. Trend Analysis
```javascript
// Get dashboard with 6-month trend
const { monthly_trend } = await api.get('/statistics/dashboard');

// Calculate growth rate
const oldest = monthly_trend[0];
const newest = monthly_trend[monthly_trend.length - 1];

const growthRate = (
  (newest.total_amount - oldest.total_amount) / 
  oldest.total_amount * 100
);

console.log(`6-month growth: ${growthRate.toFixed(1)}%`);

// Find highest spending month
const maxMonth = monthly_trend.reduce((max, m) => 
  m.total_amount > max.total_amount ? m : max
);

console.log(`Highest month: ${maxMonth.month} (₪${maxMonth.total_amount})`);
```

---

## Performance Considerations

### Caching
- Dashboard data is cached for 5 minutes
- Yearly reports are cached for 1 hour
- Category stats are cached for 10 minutes

**Cache Headers:**
```http
Cache-Control: private, max-age=300
ETag: "abc123def456"
```

### Rate Limits
| Endpoint | Limit |
|----------|-------|
| Dashboard | 60/minute |
| Yearly | 30/minute |
| Category | 60/minute |

### Response Time Targets
- Dashboard: < 500ms
- Yearly Report: < 300ms
- Category Stats: < 100ms

---

## Error Handling

### Standard Error Format
```json
{
  "detail": "Error message in Hebrew/English",
  "error_code": "STATISTICS_ERROR",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Error Codes
| Code | Description |
|------|-------------|
| `UNAUTHORIZED` | Invalid or missing token |
| `CATEGORY_NOT_FOUND` | Category ID doesn't exist |
| `INVALID_YEAR` | Year out of valid range |
| `INVALID_MONTH` | Month not 1-12 |
| `STATISTICS_ERROR` | General statistics error |

---

## Testing

### Example Test Cases
```python
def test_dashboard_statistics(client, auth_token):
    """Test dashboard endpoint"""
    response = client.get(
        "/api/v1/statistics/dashboard",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_receipts" in data
    assert "categories" in data
    assert isinstance(data["monthly_trend"], list)

def test_yearly_report_default_year(client, auth_token):
    """Test yearly report defaults to current year"""
    response = client.get(
        "/api/v1/statistics/yearly",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["year"] == datetime.now().year

def test_category_stats_not_found(client, auth_token):
    """Test category not found error"""
    response = client.get(
        "/api/v1/statistics/category/9999",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 404
```

---

## Changelog

### v1.0.0 (2024-01-15)
- Initial release
- Dashboard statistics endpoint
- Yearly report endpoint
- Category statistics endpoint
- Performance optimizations
- Caching implementation

---

## Support

For questions or issues:
- Email: support@tiktax.co.il
- Documentation: https://docs.tiktax.co.il
- API Status: https://status.tiktax.co.il
