# Error Handling & Logging - Quick Reference

## 🎯 Common Tasks

### Raise an Error

```python
from app.core.exceptions import ResourceNotFoundError

raise ResourceNotFoundError(resource="Receipt", resource_he="קבלה")
```

### Log with Context

```python
from app.core.logging_config import get_logger

logger = get_logger(__name__)

logger.info(
    "Receipt processed",
    extra={
        "user_id": 123,
        "receipt_id": 456,
        "request_id": request.state.request_id
    }
)
```

### Send to Sentry

```python
from app.core.monitoring import capture_exception

try:
    risky_operation()
except Exception as e:
    capture_exception(e, context={"user_id": 123})
    raise
```

---

## 📋 Exception Quick Reference

| Exception | Code | Usage |
|-----------|------|-------|
| `AuthenticationError()` | 401 | Invalid login |
| `AuthorizationError()` | 403 | No permission |
| `ResourceNotFoundError("Receipt", "קבלה")` | 404 | Not found |
| `ValidationError(msg, msg_he, details)` | 422 | Bad input |
| `DuplicateResourceError("User", "משתמש")` | 409 | Already exists |
| `RateLimitError()` | 429 | Too many requests |
| `OCRProcessingError()` | 422 | OCR failed |
| `FileUploadError(reason, reason_he)` | 400 | Upload failed |
| `StorageError()` | 500 | S3 error |
| `DatabaseError(op, msg)` | 500 | DB error |

---

## 📊 Log Levels

```python
logger.debug("Detailed info")   # Development only
logger.info("Normal operation") # Always log
logger.warning("Recoverable")   # Needs attention
logger.error("Failed", exc_info=True)  # With stack trace
logger.critical("System down")  # Major failure
```

---

## 🔒 Sensitive Data - Auto Filtered

These are automatically removed from logs and Sentry:
- `password`, `token`, `api_key`, `secret`
- `Authorization`, `Cookie` headers
- `credit_card`, `cvv`, `ssn`

---

## 🧪 Testing

```bash
# Unit tests
cd backend
python -m pytest tests/test_error_handling.py -v

# Manual tests
python test_error_handling_manual.py

# Check logs
cat logs/app.log | jq .         # Pretty print JSON
tail -f logs/errors.log | jq .  # Watch errors
```

---

## 🔧 Configuration (.env)

```env
LOG_LEVEL=INFO
ENVIRONMENT=production
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `app/core/logging_config.py` | JSON logging setup |
| `app/core/monitoring.py` | Sentry integration |
| `app/core/exceptions.py` | Custom exceptions |
| `app/middleware/error_handler.py` | Global error handler |
| `logs/app.log` | All logs (JSON) |
| `logs/errors.log` | Errors only |

---

## 💡 Best Practices

✅ **Use specific exceptions**
```python
raise ResourceNotFoundError("Receipt", "קבלה")
```

✅ **Always include context**
```python
logger.error("Failed", extra={"user_id": user.id}, exc_info=True)
```

✅ **Re-raise custom exceptions**
```python
except ResourceNotFoundError:
    raise  # Don't catch and swallow
```

❌ **Don't use generic exceptions**
```python
raise Exception("Error")  # Bad!
```

❌ **Don't log sensitive data**
```python
logger.info(f"Password: {pwd}")  # Bad!
```

---

## 🚨 Emergency Debugging

```bash
# Check if app starts
cd backend
python -c "from app.main import app; print('✅ App loads')"

# Check Sentry connection
python -c "from app.core.monitoring import init_sentry; init_sentry(); print('✅ Sentry OK')"

# View recent errors
tail -20 logs/errors.log | jq .

# Check log size
du -h logs/
```

---

**Full documentation:** `ERROR_HANDLING_DOCUMENTATION.md`
