# Error Handling & Logging Infrastructure

**Production-Grade Error Handling, Structured Logging, and Monitoring for Tik-Tax API**

---

## 📋 Overview

This infrastructure provides enterprise-level error handling, structured JSON logging, and error monitoring with Sentry integration.

### Key Features

✅ **Structured JSON Logging** - Machine-readable logs with full context  
✅ **Custom Exception Hierarchy** - Type-safe error handling  
✅ **Hebrew Error Messages** - User-facing messages in Hebrew  
✅ **Sentry Integration** - Real-time error monitoring  
✅ **Sensitive Data Filtering** - Automatic PII/credential filtering  
✅ **Request Tracking** - UUID-based request correlation  
✅ **Log Rotation** - Automatic rotation (10MB per file, 5 backups)  

---

## 🏗️ Architecture

```
Request → Middleware (Request ID) → Application Logic
            ↓                            ↓
        Logging                      Exception
            ↓                            ↓
    JSON Formatter              Global Handler
            ↓                            ↓
    Files + Console            Structured Response
            ↓                            ↓
        Sentry ←────────────────────────┘
```

---

## 📁 File Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── logging_config.py     # JSON logging setup
│   │   ├── monitoring.py         # Sentry integration
│   │   ├── exceptions.py         # Custom exception hierarchy
│   │   └── config.py             # Settings (updated)
│   ├── middleware/
│   │   └── error_handler.py      # Global exception handler
│   └── main.py                   # Application (updated)
├── logs/
│   ├── .gitkeep
│   ├── app.log                   # All logs (auto-created)
│   └── errors.log                # Errors only (auto-created)
└── tests/
    └── test_error_handling.py    # Comprehensive tests
```

---

## 🚀 Quick Start

### 1. Configuration

Add to `.env`:

```env
# Logging
LOG_LEVEL=INFO

# Environment
ENVIRONMENT=development  # development, staging, production

# Sentry (optional)
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
```

### 2. Usage in Code

#### Raising Exceptions

```python
from app.core.exceptions import (
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError
)

# Simple authentication error
raise AuthenticationError()

# Custom message
raise AuthenticationError(
    message="Invalid token",
    message_he="טוקן לא תקין"
)

# Not found with context
raise ResourceNotFoundError(
    resource="Receipt",
    resource_he="קבלה"
)

# Validation with details
raise ValidationError(
    message="Invalid email format",
    message_he="פורמט אימייל לא תקין",
    details={"field": "email", "value": "invalid"}
)
```

#### Logging with Context

```python
from app.core.logging_config import get_logger

logger = get_logger(__name__)

# Simple logging
logger.info("User logged in")
logger.warning("Rate limit approaching")
logger.error("Database connection failed")

# Structured logging with context
logger.info(
    "Receipt processed successfully",
    extra={
        "user_id": 123,
        "receipt_id": 456,
        "request_id": request.state.request_id,
        "processing_time_ms": 1500
    }
)

# Error with exception
try:
    process_receipt(file)
except Exception as e:
    logger.error(
        "Receipt processing failed",
        extra={
            "user_id": user.id,
            "filename": file.name
        },
        exc_info=True  # Include stack trace
    )
    raise
```

---

## 🎯 Exception Hierarchy

### Core Exceptions

| Exception | Status | Use Case | Hebrew Message |
|-----------|--------|----------|----------------|
| `AuthenticationError` | 401 | Invalid credentials, expired tokens | אימות נכשל |
| `AuthorizationError` | 403 | Permission denied | אין הרשאה לגישה |
| `ResourceNotFoundError` | 404 | Resource doesn't exist | [resource] לא נמצא |
| `ValidationError` | 422 | Invalid input data | שגיאת אימות נתונים |
| `DuplicateResourceError` | 409 | Resource already exists | [resource] כבר קיים |
| `RateLimitError` | 429 | Too many requests | יותר מדי בקשות |

### Service-Specific Exceptions

| Exception | Status | Use Case |
|-----------|--------|----------|
| `OCRProcessingError` | 422 | OCR extraction failed |
| `FileUploadError` | 400 | File upload issues |
| `StorageError` | 500 | S3 storage errors |
| `EmailError` | 500 | SendGrid failures |
| `SMSError` | 500 | Twilio failures |
| `DatabaseError` | 500 | DB operation errors |
| `ExternalServiceError` | 502 | Third-party API errors |
| `SubscriptionLimitError` | 402 | Plan limit reached |

### Error Response Format

All errors return consistent JSON:

```json
{
  "error": "Receipt not found",
  "error_he": "קבלה לא נמצאה",
  "details": {
    "receipt_id": 123
  }
}
```

---

## 📊 Logging

### Log Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages (recoverable issues)
- **ERROR**: Error messages (failures)
- **CRITICAL**: Critical failures

### JSON Log Format

```json
{
  "timestamp": "2025-11-04T14:30:00.000000Z",
  "level": "INFO",
  "logger": "app.services.receipt",
  "message": "Receipt processed successfully",
  "module": "receipt_service",
  "function": "process_receipt",
  "line": 145,
  "user_id": 123,
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "ip_address": "192.168.1.100",
  "duration_ms": 1500
}
```

### Log Files

| File | Content | Rotation |
|------|---------|----------|
| `logs/app.log` | All logs (INFO+) | 10MB, 5 backups |
| `logs/errors.log` | Errors only (ERROR+) | 10MB, 5 backups |

### Log Rotation

Automatic rotation when file reaches 10MB:
- Renames to `app.log.1`, `app.log.2`, etc.
- Keeps 5 backup files
- Deletes oldest when limit reached

---

## 🔒 Security Features

### Sensitive Data Filtering

Automatically filters from logs and Sentry:

**HTTP Headers:**
- `Authorization`
- `Cookie`
- `X-API-Key`
- `X-Auth-Token`

**Request Data:**
- `password`, `current_password`, `new_password`
- `token`, `refresh_token`, `access_token`
- `api_key`, `secret`
- `credit_card`, `cvv`, `ssn`

**Example:**

```python
# This log entry:
logger.info("User login: email=test@example.com, password=secret123")

# Becomes:
logger.info("[SENSITIVE DATA FILTERED - contains 'password']")
```

---

## 📡 Sentry Integration

### Setup

1. Create Sentry project at https://sentry.io
2. Copy DSN to `.env`:
   ```env
   SENTRY_DSN=https://abc123@sentry.io/456789
   ENVIRONMENT=production
   ```

3. Sentry auto-initializes on app startup

### Features

- **Error Tracking**: Automatic exception capture
- **Performance Monitoring**: 10% trace sampling in production
- **Breadcrumbs**: Request/response trail before errors
- **Context**: User ID, request ID, environment
- **Releases**: Version tracking (`tiktax-api@1.0.0`)

### Manual Capture

```python
from app.core.monitoring import (
    capture_exception,
    capture_message,
    set_user_context
)

# Capture exception
try:
    risky_operation()
except Exception as e:
    capture_exception(e, context={
        "operation": "risky",
        "user_id": 123
    })

# Capture message
capture_message(
    "Suspicious activity detected",
    level="warning",
    context={"ip": "1.2.3.4"}
)

# Set user context
set_user_context(user_id=123, email="user@example.com")
```

### Sampling Rates

| Environment | Transactions | Errors |
|-------------|--------------|--------|
| Development | 100% | 100% |
| Staging | 50% | 100% |
| Production | 10% | 100% |

---

## 🧪 Testing

### Unit Tests

```bash
cd backend
python -m pytest tests/test_error_handling.py -v
```

**Test Coverage:**
- ✅ All exception classes
- ✅ Error response format
- ✅ Hebrew message validation
- ✅ Logging configuration
- ✅ Sentry data filtering
- ✅ Request tracking

### Manual Testing

```bash
python test_error_handling_manual.py
```

**Tests:**
1. Structured JSON logging
2. All custom exceptions
3. Error response format
4. Sensitive data filtering
5. Exception + logging integration

### Integration Testing

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test error response
response = client.get("/api/v1/receipts/99999")
assert response.status_code == 404
assert "error_he" in response.json()

# Test request ID
response = client.get("/health")
assert "X-Request-ID" in response.headers
```

---

## 📈 Monitoring & Observability

### Request Tracking

Every request gets a unique UUID:

```
Request ID: 550e8400-e29b-41d4-a716-446655440000
```

Available in:
- Response header: `X-Request-ID`
- All log entries: `request_id` field
- Sentry events: `request_id` context

### Request Logging

```json
// Incoming request
{
  "level": "INFO",
  "message": "📨 POST /api/v1/receipts",
  "request_id": "uuid-123",
  "method": "POST",
  "path": "/api/v1/receipts",
  "ip_address": "192.168.1.1"
}

// Response
{
  "level": "INFO",
  "message": "✅ POST /api/v1/receipts - 201",
  "request_id": "uuid-123",
  "status_code": 201,
  "duration_ms": 1234.56
}
```

### Error Context

Errors include full context:

```json
{
  "level": "ERROR",
  "message": "Database operational error",
  "exception": "sqlalchemy.exc.OperationalError...",
  "request_id": "uuid-123",
  "user_id": 456,
  "ip_address": "192.168.1.1",
  "method": "POST",
  "path": "/api/v1/receipts"
}
```

---

## 🔧 Troubleshooting

### Logs Not Appearing

**Check log level:**
```python
# In .env
LOG_LEVEL=INFO  # Not DEBUG or WARNING
```

**Check file permissions:**
```bash
ls -la logs/
# Should be writable
```

### Sentry Not Working

**Verify DSN:**
```python
from app.core.config import settings
print(settings.SENTRY_DSN)
# Should not be empty
```

**Test manually:**
```python
from app.core.monitoring import capture_message
capture_message("Test from local", level="info")
# Check Sentry dashboard
```

### Request ID Missing

**Ensure middleware is active:**
```python
# In app/main.py
@app.middleware("http")
async def request_tracking_middleware(request, call_next):
    # Should be present
```

### Hebrew Not Displaying

**Check encoding:**
```python
# Logs should use UTF-8
# In logging_config.py:
error_handler = RotatingFileHandler(..., encoding='utf-8')
```

---

## 📚 Best Practices

### DO ✅

```python
# Use specific exceptions
raise ResourceNotFoundError(resource="Receipt", resource_he="קבלה")

# Include context in logs
logger.info("Operation succeeded", extra={"user_id": 123})

# Log before external calls
logger.info("Calling OCR service...")
result = ocr_service.process(image)
logger.info("OCR completed", extra={"confidence": result.confidence})

# Use exc_info for errors
except Exception as e:
    logger.error("Failed", exc_info=True)
```

### DON'T ❌

```python
# Don't use generic exceptions
raise Exception("Something went wrong")  # ❌

# Don't log sensitive data
logger.info(f"Password: {password}")  # ❌

# Don't swallow exceptions
except Exception:
    pass  # ❌

# Don't log without context
logger.error("Error")  # ❌ What error? Where?
```

---

## 🎓 Examples

### Complete Error Handling Example

```python
from app.core.logging_config import get_logger
from app.core.exceptions import (
    ResourceNotFoundError,
    OCRProcessingError,
    StorageError
)
from app.core.monitoring import capture_exception

logger = get_logger(__name__)

async def process_receipt(receipt_id: int, user_id: int):
    """Process a receipt with full error handling"""
    
    logger.info(
        "Starting receipt processing",
        extra={
            "receipt_id": receipt_id,
            "user_id": user_id
        }
    )
    
    try:
        # Get receipt
        receipt = await get_receipt(receipt_id, user_id)
        if not receipt:
            raise ResourceNotFoundError(
                resource="Receipt",
                resource_he="קבלה"
            )
        
        # Process with OCR
        logger.info("Calling OCR service", extra={"receipt_id": receipt_id})
        ocr_result = await ocr_service.process(receipt.image_url)
        
        if ocr_result.confidence < 0.8:
            raise OCRProcessingError(
                reason="Low confidence score",
                reason_he="דרגת ודאות נמוכה"
            )
        
        # Store results
        logger.info("Storing OCR results", extra={"receipt_id": receipt_id})
        await storage.save(receipt_id, ocr_result.data)
        
        logger.info(
            "Receipt processing completed",
            extra={
                "receipt_id": receipt_id,
                "confidence": ocr_result.confidence
            }
        )
        
        return ocr_result
        
    except ResourceNotFoundError:
        # Re-raise our custom exceptions
        raise
    
    except OCRProcessingError as e:
        # Log OCR failures
        logger.error(
            f"OCR processing failed: {e.message}",
            extra={"receipt_id": receipt_id},
            exc_info=True
        )
        raise
    
    except Exception as e:
        # Catch unexpected errors
        logger.error(
            f"Unexpected error processing receipt: {str(e)}",
            extra={
                "receipt_id": receipt_id,
                "user_id": user_id
            },
            exc_info=True
        )
        
        # Send to Sentry
        capture_exception(e, context={
            "receipt_id": receipt_id,
            "user_id": user_id,
            "operation": "process_receipt"
        })
        
        raise StorageError(
            message="Failed to process receipt",
            message_he="עיבוד הקבלה נכשל"
        )
```

---

## 📞 Support

For issues or questions:
1. Check logs in `logs/app.log` and `logs/errors.log`
2. Review Sentry dashboard for patterns
3. Run tests: `pytest tests/test_error_handling.py -v`
4. Check documentation: This file!

---

**Version:** 1.0.0  
**Last Updated:** November 4, 2025  
**Maintainer:** Tik-Tax Development Team
