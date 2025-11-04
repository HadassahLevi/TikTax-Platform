# Statistics API - Performance Optimization Guide

## Overview
The Statistics API provides aggregated analytics for dashboard, yearly reports, and category breakdowns. This document covers performance optimizations, caching strategies, and query optimization.

---

## Database Indexes

### Required Indexes (Already Implemented)
```sql
-- Receipt table indexes (from models/receipt.py)
CREATE INDEX idx_receipt_user_id ON receipts(user_id);
CREATE INDEX idx_receipt_status ON receipts(status);
CREATE INDEX idx_receipt_date ON receipts(receipt_date);
CREATE INDEX idx_receipt_vendor ON receipts(vendor_name);
CREATE INDEX idx_receipt_created_at ON receipts(created_at);

-- User table indexes
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_user_id_number ON users(id_number);
```

### Additional Recommended Indexes
```sql
-- Composite index for common statistics queries
CREATE INDEX idx_receipt_user_status_date ON receipts(user_id, status, receipt_date);

-- Category statistics optimization
CREATE INDEX idx_receipt_category_amount ON receipts(category_id, total_amount) WHERE status = 'approved';

-- Monthly aggregation optimization
CREATE INDEX idx_receipt_user_month ON receipts(user_id, date_trunc('month', receipt_date));
```

---

## Query Optimization Strategies

### 1. Dashboard Statistics (`GET /api/v1/statistics/dashboard`)

**Optimizations Implemented:**
- ✅ Single query for overall counts using conditional aggregation
- ✅ Batch queries for current/previous month stats
- ✅ JOIN optimization for category breakdown
- ✅ LIMIT 5 for top categories and recent receipts
- ✅ date_trunc for monthly trend aggregation

**Query Plan:**
```
Total Queries: 7
- 1 overall counts (conditional SUM)
- 1 current month stats
- 1 previous month stats
- 1 category breakdown (with JOIN)
- 1 recent receipts (with LEFT JOIN)
- 1 monthly trend
- Subscription data from user object (no query)
```

**Performance Targets:**
- < 200ms for users with < 1,000 receipts
- < 500ms for users with 1,000-10,000 receipts
- < 1s for users with > 10,000 receipts

### 2. Yearly Report (`GET /api/v1/statistics/yearly`)

**Optimizations Implemented:**
- ✅ Single aggregate query for year totals
- ✅ GROUP BY for category and monthly breakdowns
- ✅ Date range filtering on indexed column

**Query Plan:**
```
Total Queries: 3
- 1 year totals (COUNT, SUM with date filter)
- 1 category breakdown (GROUP BY category_id)
- 1 monthly breakdown (GROUP BY month)
```

**Performance Targets:**
- < 300ms for annual reports (all years)

### 3. Category Statistics (`GET /api/v1/statistics/category/{id}`)

**Optimizations Implemented:**
- ✅ Filtered aggregation with optional date range
- ✅ Percentage calculation with total context

**Performance Targets:**
- < 100ms for single category queries

---

## Caching Strategy

### Recommended Caching
```python
from functools import lru_cache
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

# Cache dashboard for 5 minutes per user
@router.get("/dashboard", response_model=ReceiptStatistics)
@cache(expire=300)  # 5 minutes
async def get_dashboard_statistics(...):
    ...

# Cache yearly report for 1 hour (historical data rarely changes)
@router.get("/yearly", response_model=YearlyReport)
@cache(expire=3600)  # 1 hour
async def get_yearly_report(...):
    ...
```

### Cache Invalidation Strategy
```python
# Invalidate cache on receipt changes
@router.post("/receipts")
async def create_receipt(...):
    receipt = create_new_receipt(...)
    
    # Invalidate dashboard cache
    await cache.delete(f"dashboard:{user.id}")
    
    return receipt
```

### Redis Cache Configuration
```python
# app/main.py
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="tiktax-cache:")
```

---

## Database Query Optimization

### Using Database Views (Advanced)

Create materialized views for expensive aggregations:

```sql
-- Monthly statistics materialized view
CREATE MATERIALIZED VIEW user_monthly_stats AS
SELECT
    user_id,
    date_trunc('month', receipt_date) as month,
    COUNT(*) as receipt_count,
    SUM(total_amount) as total_amount,
    AVG(total_amount) as avg_amount
FROM receipts
WHERE status = 'approved'
GROUP BY user_id, date_trunc('month', receipt_date);

-- Create index on materialized view
CREATE INDEX idx_monthly_stats_user ON user_monthly_stats(user_id, month);

-- Refresh strategy
-- Option 1: Scheduled refresh (daily at midnight)
-- Option 2: Trigger on receipt approval
-- Option 3: Concurrent refresh (no locking)
REFRESH MATERIALIZED VIEW CONCURRENTLY user_monthly_stats;
```

### Query with Materialized View
```python
# Use materialized view for monthly trend
monthly_trend = db.query(UserMonthlyStats).filter(
    UserMonthlyStats.user_id == current_user.id,
    UserMonthlyStats.month >= six_months_ago
).order_by(UserMonthlyStats.month).all()
```

---

## Connection Pooling

### SQLAlchemy Configuration
```python
# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:pass@localhost/tiktax"

engine = create_engine(
    DATABASE_URL,
    pool_size=20,          # Concurrent connections
    max_overflow=10,       # Burst capacity
    pool_pre_ping=True,    # Test connections before use
    pool_recycle=3600,     # Recycle connections every hour
    echo=False             # Disable SQL logging in production
)
```

---

## Query Result Pagination

For very large result sets, implement pagination:

```python
@router.get("/category/{category_id}/receipts")
async def get_category_receipts(
    category_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get paginated receipts for category"""
    offset = (page - 1) * per_page
    
    receipts = db.query(Receipt).filter(
        Receipt.user_id == current_user.id,
        Receipt.category_id == category_id,
        Receipt.status == ReceiptStatus.APPROVED
    ).order_by(
        Receipt.receipt_date.desc()
    ).limit(per_page).offset(offset).all()
    
    total = db.query(func.count(Receipt.id)).filter(
        Receipt.user_id == current_user.id,
        Receipt.category_id == category_id,
        Receipt.status == ReceiptStatus.APPROVED
    ).scalar()
    
    return {
        "items": receipts,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page
    }
```

---

## Monitoring & Performance Testing

### Query Performance Monitoring
```python
import time
import logging

logger = logging.getLogger(__name__)

def log_slow_queries(threshold_ms: float = 100):
    """Decorator to log slow queries"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start = time.time()
            result = await func(*args, **kwargs)
            duration = (time.time() - start) * 1000
            
            if duration > threshold_ms:
                logger.warning(f"Slow query in {func.__name__}: {duration:.2f}ms")
            
            return result
        return wrapper
    return decorator

@router.get("/dashboard")
@log_slow_queries(threshold_ms=200)
async def get_dashboard_statistics(...):
    ...
```

### Load Testing with Locust
```python
# locustfile.py
from locust import HttpUser, task, between

class TikTaxUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Login
        response = self.client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "password123"
        })
        self.token = response.json()["access_token"]
    
    @task(5)
    def dashboard(self):
        self.client.get(
            "/api/v1/statistics/dashboard",
            headers={"Authorization": f"Bearer {self.token}"}
        )
    
    @task(2)
    def yearly_report(self):
        self.client.get(
            "/api/v1/statistics/yearly?year=2024",
            headers={"Authorization": f"Bearer {self.token}"}
        )
    
    @task(1)
    def category_stats(self):
        self.client.get(
            "/api/v1/statistics/category/1",
            headers={"Authorization": f"Bearer {self.token}"}
        )
```

### Run Load Test
```bash
# Install locust
pip install locust

# Run load test
locust -f locustfile.py --host=http://localhost:8000

# Open browser: http://localhost:8089
# Set users: 100, spawn rate: 10
```

---

## Database Query EXPLAIN Analysis

### Analyze Query Performance
```sql
-- Dashboard query analysis
EXPLAIN ANALYZE
SELECT
    COUNT(id) as total,
    SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) as approved,
    SUM(CASE WHEN status IN ('processing', 'review') THEN 1 ELSE 0 END) as pending
FROM receipts
WHERE user_id = 1;

-- Expected output should show:
-- Index Scan using idx_receipt_user_id
-- Cost: < 100
-- Execution time: < 10ms
```

---

## Production Deployment Checklist

### Database Optimization
- [x] All indexes created
- [ ] Materialized views configured (optional)
- [ ] Connection pooling configured
- [ ] Query timeout set (30s default)
- [ ] VACUUM ANALYZE scheduled (weekly)

### Application Optimization
- [ ] Redis cache configured
- [ ] Cache invalidation strategy implemented
- [ ] Slow query logging enabled
- [ ] Connection pool monitoring
- [ ] Query performance metrics

### Monitoring
- [ ] Application Performance Monitoring (APM) configured
- [ ] Database query monitoring
- [ ] Cache hit rate monitoring
- [ ] API response time tracking
- [ ] Error rate alerts

---

## Troubleshooting Common Performance Issues

### Issue 1: Slow Dashboard Queries
**Symptom:** Dashboard takes > 1s to load  
**Diagnosis:**
```sql
-- Check if indexes exist
SELECT * FROM pg_indexes WHERE tablename = 'receipts';

-- Check query plan
EXPLAIN ANALYZE [paste slow query];
```
**Solutions:**
1. Verify indexes are created
2. Run VACUUM ANALYZE on receipts table
3. Implement caching
4. Reduce date range for trends

### Issue 2: High Memory Usage
**Symptom:** Database memory usage spikes  
**Solutions:**
1. Reduce connection pool size
2. Implement pagination for large results
3. Use LIMIT on all queries
4. Clear old materialized views

### Issue 3: Cache Miss Rate High
**Symptom:** Low cache hit rate  
**Solutions:**
1. Increase cache TTL
2. Pre-warm cache for common queries
3. Implement stale-while-revalidate pattern
4. Review cache key strategy

---

## Future Optimizations

### Phase 2: Advanced Analytics
- [ ] Real-time statistics with WebSocket
- [ ] Predictive analytics (spending forecast)
- [ ] Anomaly detection (unusual expenses)
- [ ] Category auto-suggestions based on history

### Phase 3: Big Data
- [ ] Move to TimescaleDB for time-series data
- [ ] Implement data warehouse for historical analytics
- [ ] Use read replicas for reporting queries
- [ ] Implement query result streaming

---

## Summary

**Key Performance Metrics:**
- Dashboard: < 500ms (target)
- Yearly Report: < 300ms (target)
- Category Stats: < 100ms (target)
- Cache Hit Rate: > 80% (target)

**Critical Optimizations:**
1. ✅ Database indexes on all filtered columns
2. ✅ Optimized JOIN queries
3. ✅ Limited result sets (LIMIT 5)
4. 🔄 Caching (recommended for production)
5. 🔄 Materialized views (optional for large datasets)

**Monitoring:**
- Track query execution time
- Monitor cache hit rates
- Alert on slow queries (> 1s)
- Regular database maintenance (VACUUM, ANALYZE)
