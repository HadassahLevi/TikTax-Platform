# Authentication System - Quick Start Guide

## Prerequisites

- Python 3.11+
- PostgreSQL database
- Twilio account (for SMS)
- SendGrid account (for emails)
- Redis (optional for production)

## Installation Steps

### 1. Install Dependencies

```bash
cd backend

# Install Python packages
pip install twilio
pip install sendgrid
```

If not already in requirements.txt, add:
```txt
twilio==8.10.0
sendgrid==6.11.0
```

### 2. Environment Variables

Create or update `.env` file in `backend/` directory:

```bash
# Security (REQUIRED)
SECRET_KEY=your-super-secret-key-min-32-chars-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30

# Database (REQUIRED)
DATABASE_URL=postgresql://tiktax:password@localhost:5432/tiktax

# Twilio SMS (REQUIRED)
TWILIO_ACCOUNT_SID=AC...your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=+972...your-twilio-number

# SendGrid Email (REQUIRED)
SENDGRID_API_KEY=SG....your-sendgrid-api-key
SENDGRID_FROM_EMAIL=noreply@tiktax.co.il
SENDGRID_FROM_NAME=Tik-Tax

# Frontend (REQUIRED)
FRONTEND_URL=http://localhost:5173

# Optional
REDIS_URL=redis://localhost:6379/0
SENTRY_DSN=https://...your-sentry-dsn
```

### 3. Generate Secret Key

```python
# Run in Python shell
import secrets
print(secrets.token_urlsafe(32))
# Copy output to SECRET_KEY in .env
```

### 4. Set Up Twilio

1. Sign up at https://www.twilio.com
2. Get a phone number
3. Copy Account SID and Auth Token
4. Verify your test phone numbers (for development)

**Testing with Twilio:**
```python
# Use verified numbers in development
# Twilio Trial: Can only send to verified numbers
# Production: Remove verification requirement
```

### 5. Set Up SendGrid

1. Sign up at https://sendgrid.com
2. Create API key with "Mail Send" permissions
3. Verify sender email (noreply@tiktax.co.il)
4. Set up domain authentication (production)

**Testing with SendGrid:**
```python
# Development: Use your personal email
SENDGRID_FROM_EMAIL=your-email@gmail.com
```

### 6. Database Migration

Ensure the User model is migrated:

```bash
cd backend

# Create migration
alembic revision --autogenerate -m "Add user authentication"

# Apply migration
alembic upgrade head
```

### 7. Run Tests

```bash
cd backend

# Install test dependencies
pip install pytest pytest-cov

# Run auth tests
pytest tests/api/test_auth.py -v

# Run with coverage
pytest tests/api/test_auth.py --cov=app --cov-report=html

# View coverage
open htmlcov/index.html  # Mac/Linux
start htmlcov/index.html  # Windows
```

### 8. Start Server

```bash
cd backend

# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 9. Test API

**Option 1: Using Swagger UI**
```
Open: http://localhost:8000/api/v1/docs
```

**Option 2: Using curl**
```bash
# Send SMS verification
curl -X POST http://localhost:8000/api/v1/auth/send-verification \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+972501234567"}'

# Verify SMS
curl -X POST http://localhost:8000/api/v1/auth/verify-sms \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+972501234567", "code": "123456"}'

# Signup
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@test.com",
    "password": "SecurePass123!",
    "full_name": "Test User",
    "id_number": "123456789",
    "phone_number": "+972501234567",
    "business_name": "Test Business",
    "sms_code": "123456"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@test.com",
    "password": "SecurePass123!"
  }'
```

## Development Tips

### 1. Mock SMS in Development

Create `backend/app/services/sms_service_mock.py`:

```python
"""Mock SMS service for development"""
import logging

logger = logging.getLogger(__name__)

class MockSMSService:
    """Mock SMS service that logs codes instead of sending"""
    
    def __init__(self):
        self.codes = {}
    
    def generate_code(self):
        return "123456"  # Fixed code for testing
    
    async def send_verification_code(self, phone_number: str) -> bool:
        code = self.generate_code()
        self.codes[phone_number] = code
        logger.info(f"📱 [MOCK SMS] Code for {phone_number}: {code}")
        return True
    
    async def verify_code(self, phone_number: str, code: str) -> bool:
        stored_code = self.codes.get(phone_number)
        return stored_code == code

sms_service = MockSMSService()
```

Update imports in development:
```python
# In auth.py, use:
if settings.ENVIRONMENT == "development":
    from ....services.sms_service_mock import sms_service
else:
    from ....services.sms_service import sms_service
```

### 2. View Logs

```bash
# Tail logs
tail -f logs/app.log

# Or run with verbose logging
uvicorn app.main:app --reload --log-level debug
```

### 3. Database Inspection

```bash
# Connect to PostgreSQL
psql -U tiktax -d tiktax

# View users
SELECT id, email, full_name, is_phone_verified, created_at FROM users;

# Check phone verification
SELECT phone_number, is_phone_verified FROM users;
```

## Troubleshooting

### SMS Not Sending

**Problem:** "Failed to send SMS"

**Solutions:**
1. Check Twilio credentials in `.env`
2. Verify phone number format (+972...)
3. Check Twilio trial limitations
4. Use mock SMS service for development

### Email Not Sending

**Problem:** SendGrid errors

**Solutions:**
1. Verify API key
2. Check sender email is verified
3. Review SendGrid activity log
4. Check spam folder

### Token Errors

**Problem:** "Invalid token"

**Solutions:**
1. Check SECRET_KEY is set
2. Verify token hasn't expired
3. Ensure token format is correct
4. Check system time is accurate

### Database Errors

**Problem:** User model fields missing

**Solutions:**
```bash
# Run migrations
alembic upgrade head

# Or recreate database
alembic downgrade base
alembic upgrade head
```

### Import Errors

**Problem:** Module not found

**Solutions:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/TikTax/backend"
```

## Production Checklist

Before deploying to production:

- [ ] Set strong SECRET_KEY (32+ chars)
- [ ] Use production database
- [ ] Enable HTTPS only
- [ ] Set up Redis for SMS code storage
- [ ] Configure rate limiting
- [ ] Set up Sentry error tracking
- [ ] Enable CORS only for your domain
- [ ] Set up monitoring and alerts
- [ ] Configure backup for database
- [ ] Test email deliverability
- [ ] Verify SMS delivery rates
- [ ] Set up logging aggregation
- [ ] Configure firewall rules
- [ ] Enable DDoS protection
- [ ] Set up CDN (optional)
- [ ] Run security audit
- [ ] Load testing
- [ ] Documentation review

## Support

**Documentation:**
- API Docs: `AUTH_ENDPOINTS.md`
- Implementation: `AUTH_IMPLEMENTATION_SUMMARY.md`
- Tests: `tests/api/test_auth.py`

**Common Issues:**
- Check logs: `logs/app.log`
- Run tests: `pytest tests/api/test_auth.py -v`
- View API docs: http://localhost:8000/api/v1/docs

**Contact:**
- Email: dev@tiktax.co.il
- Docs: https://docs.tiktax.co.il

---

**Ready to go! 🚀**

Start the server and test the endpoints using Swagger UI or curl commands above.
