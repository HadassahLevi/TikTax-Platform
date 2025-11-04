# Error Handling & Logging - Testing Checklist

## ✅ Implementation Testing Checklist

Use this checklist to verify the error handling and logging infrastructure is working correctly.

---

## 🧪 Unit Tests

### Run Test Suite

```bash
cd backend
python -m pytest tests/test_error_handling.py -v
```

**Expected Results:**
- [ ] All tests pass (24+ tests)
- [ ] No import errors
- [ ] All exception classes tested
- [ ] Error response format validated
- [ ] Hebrew messages validated
- [ ] Sentry filtering tested

---

## 🔨 Manual Tests

### 1. Run Manual Test Script

```bash
cd backend
python test_error_handling_manual.py
```

**Expected Results:**
- [ ] Script completes without errors
- [ ] Structured logging demonstrated
- [ ] All exception types shown
- [ ] Error response format correct
- [ ] Sensitive data filtering works
- [ ] Exception + logging integration works

### 2. Check Log Files

```bash
# Check that logs directory was created
ls -la logs/

# Check log contents
cat logs/app.log
cat logs/errors.log
```

**Expected Results:**
- [ ] `logs/` directory exists
- [ ] `logs/.gitkeep` file exists
- [ ] `logs/app.log` contains JSON-formatted logs
- [ ] `logs/errors.log` contains error logs only
- [ ] Logs have UTF-8 encoding (Hebrew displays correctly)
- [ ] Sensitive data is [FILTERED]

### 3. Verify Log Format

```bash
# Pretty-print JSON logs
cat logs/app.log | python -m json.tool
```

**Expected Fields:**
- [ ] `timestamp` (ISO 8601 format)
- [ ] `level` (INFO, WARNING, ERROR, etc.)
- [ ] `logger` (module name)
- [ ] `message` (log message)
- [ ] `module`, `function`, `line`
- [ ] Extra fields when present: `user_id`, `request_id`, `ip_address`

---

## 🚀 Integration Tests

### 1. Start the Application

```bash
cd backend
uvicorn app.main:app --reload
```

**Expected Results:**
- [ ] App starts without errors
- [ ] Startup logs appear in console (JSON format)
- [ ] "Starting Tik-Tax API" message logged
- [ ] Database connection successful
- [ ] Sentry initialized (if DSN configured)

### 2. Test Health Endpoint

```bash
curl http://localhost:8000/health
```

**Expected Results:**
- [ ] Returns 200 status
- [ ] Response includes `X-Request-ID` header
- [ ] Logs show request with UUID

### 3. Test 404 Error

```bash
curl http://localhost:8000/api/v1/nonexistent
```

**Expected Results:**
- [ ] Returns 404 status
- [ ] Response includes `error` and `error_he` fields
- [ ] Error logged with request context

### 4. Test Validation Error

```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "invalid", "password": "123"}'
```

**Expected Results:**
- [ ] Returns 422 status
- [ ] Response has `error`, `error_he`, and `details` fields
- [ ] Hebrew error message present

---

## 🔒 Security Tests

### 1. Test Sensitive Data Filtering in Logs

Create a test that logs sensitive data:

```python
from app.core.logging_config import get_logger

logger = get_logger(__name__)

# These should be filtered
logger.info("User password is secret123")
logger.info("Token: Bearer abc123")
logger.info("API key is xyz789")
```

**Expected Results:**
- [ ] Logs show `[SENSITIVE DATA FILTERED]` instead of actual values
- [ ] No passwords visible in `logs/app.log`

### 2. Test Sentry Data Filtering

```python
from app.core.monitoring import before_send_handler

event = {
    "request": {
        "headers": {"Authorization": "Bearer secret"},
        "data": {"password": "secret123"}
    }
}

filtered = before_send_handler(event, {})
```

**Expected Results:**
- [ ] `Authorization` header is `[FILTERED]`
- [ ] `password` field is `[FILTERED]`

---

## 📊 Sentry Integration Tests

### 1. Configure Sentry

Add to `.env`:
```env
SENTRY_DSN=https://your-key@sentry.io/project-id
ENVIRONMENT=development
```

### 2. Test Sentry Initialization

```bash
python -c "from app.core.monitoring import init_sentry; init_sentry(); print('✅ Sentry initialized')"
```

**Expected Results:**
- [ ] No errors
- [ ] Sentry initialized message

### 3. Send Test Event to Sentry

```python
from app.core.monitoring import capture_message

capture_message("Test error from Tik-Tax", level="error")
```

**Expected Results:**
- [ ] Event appears in Sentry dashboard
- [ ] Environment tag is correct (development/staging/production)
- [ ] Release tag shows `tiktax-api@1.0.0`

### 4. Test Exception Capture

```python
from app.core.monitoring import capture_exception

try:
    raise ValueError("Test exception")
except Exception as e:
    capture_exception(e, context={"test": True})
```

**Expected Results:**
- [ ] Exception appears in Sentry
- [ ] Stack trace is included
- [ ] Context data is attached

---

## 📈 Performance Tests

### 1. Test Log Rotation

```bash
# Fill app.log with data (>10MB)
cd backend
python -c "
from app.core.logging_config import setup_logging, get_logger
setup_logging()
logger = get_logger('test')

# Generate 10MB of logs
for i in range(100000):
    logger.info('x' * 200)  # ~20KB per 100 logs = ~2MB per 10K logs
"

# Check that rotation happened
ls -lh logs/
```

**Expected Results:**
- [ ] `app.log.1` exists (rotated file)
- [ ] Current `app.log` is smaller than 10MB
- [ ] Maximum 5 backup files (`.1` through `.5`)

### 2. Test Request Tracking Overhead

Benchmark with and without request tracking:

```bash
# With tracking
ab -n 1000 -c 10 http://localhost:8000/health

# Check performance impact
```

**Expected Results:**
- [ ] Minimal overhead (<5ms per request)
- [ ] All requests have unique request IDs

---

## 🌍 Hebrew Support Tests

### 1. Test Hebrew Error Messages

```python
from app.core.exceptions import ResourceNotFoundError

exc = ResourceNotFoundError(resource="Receipt", resource_he="קבלה")
print(exc.message_he)
```

**Expected Results:**
- [ ] Hebrew displays correctly
- [ ] No encoding errors
- [ ] Contains Hebrew characters (U+0590 to U+05FF)

### 2. Test Hebrew in Logs

```python
from app.core.logging_config import get_logger

logger = get_logger(__name__)
logger.info("קבלה נשמרה בהצלחה")  # "Receipt saved successfully" in Hebrew

# Check logs
cat logs/app.log
```

**Expected Results:**
- [ ] Hebrew characters preserved in JSON
- [ ] UTF-8 encoding maintained
- [ ] No �� replacement characters

---

## 🔄 Exception Handling Tests

### 1. Test Exception Chaining

```python
try:
    try:
        raise ValueError("Original error")
    except ValueError as e:
        raise DatabaseError("insert", "Failed") from e
except DatabaseError as db_err:
    # Should preserve original exception
    print(db_err.__cause__)
```

**Expected Results:**
- [ ] Original exception preserved
- [ ] Stack trace includes both exceptions

### 2. Test All Exception Status Codes

```python
from app.core.exceptions import *

exceptions = [
    (AuthenticationError(), 401),
    (AuthorizationError(), 403),
    (ResourceNotFoundError(), 404),
    (ValidationError("", "", {}), 422),
    (DuplicateResourceError(), 409),
    (RateLimitError(), 429),
    (OCRProcessingError(), 422),
    (FileUploadError("", ""), 400),
    (StorageError(), 500),
    (DatabaseError("", ""), 500),
]

for exc, expected_code in exceptions:
    assert exc.status_code == expected_code, f"Wrong status code for {exc.__class__.__name__}"
```

**Expected Results:**
- [ ] All status codes correct
- [ ] No assertion errors

---

## 📱 API Endpoint Tests

### 1. Test Error Response Format

Make requests to various endpoints and verify error format:

```bash
# 404
curl http://localhost:8000/api/v1/invalid

# 401 (if auth endpoint exists)
curl http://localhost:8000/api/v1/protected

# 422 (validation error)
curl -X POST http://localhost:8000/api/v1/endpoint -d '{}'
```

**Expected Response Format:**
```json
{
  "error": "English message",
  "error_he": "הודעה בעברית",
  "details": {}
}
```

**Check:**
- [ ] All responses have `error`, `error_he`, `details`
- [ ] Hebrew messages are appropriate
- [ ] Details contain relevant context

### 2. Test Request ID Propagation

```bash
curl -v http://localhost:8000/health
```

**Expected Results:**
- [ ] Response headers include `X-Request-ID`
- [ ] Request ID is a valid UUID
- [ ] Same request ID appears in logs

---

## 🛠️ Development Tools Tests

### 1. Test with Different Log Levels

In `.env`, try different levels:

```env
LOG_LEVEL=DEBUG
LOG_LEVEL=INFO
LOG_LEVEL=WARNING
LOG_LEVEL=ERROR
```

**Expected Results:**
- [ ] DEBUG shows all logs
- [ ] INFO shows INFO, WARNING, ERROR
- [ ] WARNING shows WARNING, ERROR
- [ ] ERROR shows ERROR only

### 2. Test with Different Environments

```env
ENVIRONMENT=development  # 100% trace sampling
ENVIRONMENT=staging      # 50% trace sampling
ENVIRONMENT=production   # 10% trace sampling
```

**Expected Results:**
- [ ] Sentry sampling rate adjusts
- [ ] Environment tag in Sentry matches

---

## ✅ Final Verification

### Pre-Production Checklist

- [ ] All unit tests pass
- [ ] Manual test script runs successfully
- [ ] Log files are created and rotated
- [ ] JSON log format is valid
- [ ] Hebrew messages display correctly
- [ ] Sensitive data is filtered
- [ ] Sentry receives events (if configured)
- [ ] Request IDs are unique and tracked
- [ ] All exception types return correct status codes
- [ ] Error responses have consistent format
- [ ] Documentation is complete

### Production Deployment Checklist

- [ ] `ENVIRONMENT=production` in .env
- [ ] `LOG_LEVEL=INFO` (not DEBUG)
- [ ] Sentry DSN configured
- [ ] Logs directory has write permissions
- [ ] Log rotation is configured
- [ ] Monitoring dashboard set up
- [ ] Error alerting configured
- [ ] Team trained on error handling patterns

---

## 🎉 Success Criteria

All items checked = Ready for production! ✅

**Questions or issues?** Check `ERROR_HANDLING_DOCUMENTATION.md` for troubleshooting.
