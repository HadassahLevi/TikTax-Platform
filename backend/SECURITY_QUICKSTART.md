# 🔐 Tik-Tax Security Quick Reference

## ✅ IMPLEMENTATION COMPLETE

All JWT authentication, password hashing, and security utilities have been successfully implemented!

---

## 📁 Files Created/Modified

### Core Files:
1. ✅ `/backend/app/core/security.py` - Password hashing, JWT, Israeli validators
2. ✅ `/backend/app/core/dependencies.py` - Auth dependencies for routes
3. ✅ `/backend/app/middleware/rate_limit.py` - Rate limiting (60/min per IP)
4. ✅ `/backend/app/middleware/error_handler.py` - Global error handler
5. ✅ `/backend/app/main.py` - Updated with middleware

### Test Files:
6. ✅ `/backend/tests/core/test_security.py` - 40+ unit tests
7. ✅ `/backend/tests/core/test_dependencies.py` - 15+ unit tests

---

## 🚀 Quick Start

### 1. Use in Your Routes

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db
from app.models.user import User

router = APIRouter()

# Protected route - requires authentication
@router.get("/me")
async def get_profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "email": current_user.email,
        "name": current_user.full_name
    }

# Receipt upload - checks subscription limit too
@router.post("/receipts/upload")
async def upload_receipt(
    current_user: User = Depends(get_current_user_with_subscription_check),
    db: Session = Depends(get_db)
):
    # User is authenticated AND within subscription limit
    pass
```

### 2. Validate User Input

```python
from app.core.security import (
    validate_email,
    validate_password_strength,
    validate_israeli_id,
    validate_israeli_phone,
    get_password_hash
)

# Email validation
if not validate_email("user@example.com"):
    raise ValueError("אימייל לא תקין")

# Password strength
is_valid, error = validate_password_strength("MyPass123")
if not is_valid:
    raise ValueError(error)  # Hebrew error message

# Israeli ID
if not validate_israeli_id("123456782"):
    raise ValueError("תעודת זהות לא תקינה")

# Phone number
if not validate_israeli_phone("0501234567"):
    raise ValueError("מספר טלפון לא תקין")

# Hash password before storing
hashed = get_password_hash("MyPass123")
```

### 3. Create JWT Tokens

```python
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token
)

# Login endpoint
@router.post("/auth/login")
async def login(email: str, password: str, db: Session = Depends(get_db)):
    # Find user
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise AuthenticationError("אימייל או סיסמה שגויים")
    
    # Create tokens
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
```

---

## 🧪 Testing

### Run all tests:
```bash
cd backend
python -m pytest tests/core/ -v
```

### Run specific tests:
```bash
# Password tests
python -m pytest tests/core/test_security.py::TestPasswordHashing -v

# JWT tests
python -m pytest tests/core/test_security.py::TestJWTTokens -v

# Israeli validators
python -m pytest tests/core/test_security.py::TestIsraeliIDValidation -v
```

---

## 🔒 Security Features

| Feature | Status | Details |
|---------|--------|---------|
| Password Hashing | ✅ | Bcrypt with automatic salting |
| JWT Access Tokens | ✅ | 60 minute expiry |
| JWT Refresh Tokens | ✅ | 30 day expiry |
| Token Verification | ✅ | Type checking (access/refresh) |
| Israeli ID Validation | ✅ | Checksum algorithm |
| Phone Validation | ✅ | Israeli mobile numbers |
| Password Strength | ✅ | 8+ chars, upper, lower, digit |
| Rate Limiting | ✅ | 60 requests/min per IP |
| Error Handling | ✅ | Hebrew error messages |
| Subscription Limits | ✅ | Enforced before receipt upload |

---

## ⚙️ Configuration

Add to your `.env` file:

```env
# Security
SECRET_KEY=your-super-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
```

**Generate a secret key:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## 📝 Important Notes

### ✅ DO:
- Always use `get_password_hash()` before storing passwords
- Use `get_current_user` dependency for protected routes
- Use `get_current_user_with_subscription_check` for receipt operations
- Validate all user inputs before processing
- Check Hebrew error messages in frontend

### ❌ DON'T:
- Never log passwords or tokens
- Never store passwords in plain text
- Never skip input validation
- Never use localStorage for tokens in frontend (use memory)

---

## 🚦 What's Next?

1. ✅ Test authentication endpoints
2. ✅ Verify error messages display correctly
3. ⚠️ For production: Replace in-memory rate limiting with Redis
4. 🔄 Implement token refresh endpoint
5. 🔄 Add logout with token blacklist

---

## 📚 Full Documentation

See `/backend/SECURITY_IMPLEMENTATION.md` for complete details.

---

**Status:** ✅ READY TO USE
**Last Updated:** November 4, 2025
