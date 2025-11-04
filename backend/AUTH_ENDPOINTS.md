# Authentication System Documentation

## Overview
Complete authentication system for Tik-Tax with SMS verification, JWT tokens, and password management.

## Endpoints

### 1. Send SMS Verification
**POST** `/api/v1/auth/send-verification`

Send SMS verification code to phone number.

**Request:**
```json
{
  "phone_number": "+972501234567"
}
```

**Response:**
```json
{
  "message": "קוד אימות נשלח בהצלחה"
}
```

**Rate Limit:** 3 requests per hour per phone number

---

### 2. Verify SMS Code
**POST** `/api/v1/auth/verify-sms`

Verify SMS verification code.

**Request:**
```json
{
  "phone_number": "+972501234567",
  "code": "123456"
}
```

**Response:**
```json
{
  "message": "מספר הטלפון אומת בהצלחה"
}
```

---

### 3. User Signup
**POST** `/api/v1/auth/signup`

Register new user with SMS verification.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe",
  "id_number": "123456789",
  "phone_number": "+972501234567",
  "business_name": "My Business",
  "business_number": "987654321",
  "business_type": "עוסק מורשה",
  "sms_code": "123456"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**Validations:**
- Email: Must be valid email format
- Password: Min 8 characters, must include uppercase, lowercase, number, special char
- ID Number: Valid Israeli ID (9 digits with checksum)
- Phone: Valid Israeli phone format (+972...)
- SMS Code: Must be valid and not expired

---

### 4. User Login
**POST** `/api/v1/auth/login`

Login with email and password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

---

### 5. Refresh Token
**POST** `/api/v1/auth/refresh`

Get new access token using refresh token.

**Request:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

---

### 6. Logout
**POST** `/api/v1/auth/logout`

Logout current user.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "message": "התנתקת בהצלחה"
}
```

**Note:** Client must delete tokens from memory.

---

### 7. Get Current User
**GET** `/api/v1/auth/me`

Get authenticated user information.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "phone_number": "+972501234567",
  "is_phone_verified": true,
  "business_name": "My Business",
  "business_number": "987654321",
  "subscription_plan": "FREE",
  "receipt_limit": 50,
  "receipts_used_this_month": 12,
  "created_at": "2024-01-01T00:00:00"
}
```

---

### 8. Forgot Password
**POST** `/api/v1/auth/forgot-password`

Request password reset link via email.

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "אם המייל קיים במערכת, נשלח אליו קישור לאיפוס סיסמה"
}
```

**Note:** Always returns success to prevent email enumeration.

---

### 9. Reset Password
**POST** `/api/v1/auth/reset-password`

Reset password using token from email.

**Request:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "new_password": "NewSecurePass123!"
}
```

**Response:**
```json
{
  "message": "הסיסמה שונתה בהצלחה"
}
```

**Token Validity:** 1 hour

---

### 10. Change Password
**PUT** `/api/v1/auth/change-password`

Change password for authenticated user.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "current_password": "OldPass123!",
  "new_password": "NewSecurePass123!"
}
```

**Response:**
```json
{
  "message": "הסיסמה שונתה בהצלחה"
}
```

---

## Error Responses

All endpoints return consistent error format:

```json
{
  "detail": "הודעת שגיאה בעברית"
}
```

### Common HTTP Status Codes:
- `200 OK` - Success
- `201 Created` - Resource created (signup)
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required or failed
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

---

## Security Features

### 1. Password Security
- **Hashing:** bcrypt with auto-generated salt
- **Minimum Requirements:**
  - 8 characters minimum
  - At least 1 uppercase letter
  - At least 1 lowercase letter
  - At least 1 number
  - At least 1 special character
- **Never logged or stored in plaintext**

### 2. Token Security
- **JWT Tokens:** HS256 algorithm
- **Access Token:** 60 minutes expiry
- **Refresh Token:** 30 days expiry
- **Storage:** Client-side memory only (never localStorage)
- **Auto-refresh:** Frontend handles automatic refresh

### 3. SMS Verification
- **Code Generation:** 6-digit random number
- **Expiry:** 10 minutes
- **Max Attempts:** 3 attempts per code
- **Rate Limiting:** Max 3 SMS per hour per phone

### 4. Israeli ID Validation
- **Format:** 9 digits
- **Checksum:** Luhn algorithm validation
- **Uniqueness:** Enforced at database level

### 5. Phone Validation
- **Format:** Israeli phone numbers only (+972...)
- **Verification:** Required via SMS
- **Uniqueness:** Enforced at database level

---

## Environment Variables Required

```bash
# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30

# Twilio SMS
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=+972...

# SendGrid Email
SENDGRID_API_KEY=your-sendgrid-key
SENDGRID_FROM_EMAIL=noreply@tiktax.co.il
SENDGRID_FROM_NAME=Tik-Tax

# Frontend URL
FRONTEND_URL=http://localhost:5173

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/tiktax
```

---

## Testing

Run auth tests:
```bash
cd backend
pytest tests/api/test_auth.py -v
```

Run all tests with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

---

## Usage Examples

### Frontend Integration (TypeScript)

```typescript
// 1. Signup Flow
const signup = async (userData: SignupData) => {
  // Step 1: Send SMS
  await api.post('/auth/send-verification', {
    phone_number: userData.phone
  });
  
  // Step 2: User enters code
  // Step 3: Complete signup
  const response = await api.post('/auth/signup', {
    ...userData,
    sms_code: code
  });
  
  // Store tokens in memory (Zustand store)
  authStore.setTokens(response.data);
};

// 2. Login
const login = async (email: string, password: string) => {
  const response = await api.post('/auth/login', {
    email,
    password
  });
  
  authStore.setTokens(response.data);
};

// 3. Auto-refresh on 401
axios.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      const refreshToken = authStore.getRefreshToken();
      const response = await api.post('/auth/refresh', {
        refresh_token: refreshToken
      });
      authStore.setTokens(response.data);
      
      // Retry original request
      return axios.request(error.config);
    }
    throw error;
  }
);

// 4. Logout
const logout = async () => {
  await api.post('/auth/logout');
  authStore.clearTokens();
};
```

---

## Production Considerations

### 1. Rate Limiting
- Implement Redis-based rate limiting
- Different limits per endpoint:
  - SMS: 3 per hour
  - Login: 5 attempts per 15 minutes
  - Signup: 3 per day per IP

### 2. SMS Code Storage
- Current: In-memory dictionary
- Production: Redis with TTL
- Clustering: Shared Redis instance

### 3. Email Delivery
- Current: SendGrid
- Monitor: Delivery rates and bounces
- Backup: Alternative email provider

### 4. Token Rotation
- Consider implementing token rotation
- Blacklist compromised tokens
- Redis for blacklist storage

### 5. Security Headers
- HTTPS only in production
- HSTS headers
- CSP headers
- X-Frame-Options

### 6. Logging
- Never log passwords
- Log authentication attempts
- Monitor suspicious patterns
- Use Sentry for error tracking

### 7. Monitoring
- Track signup conversion rate
- Monitor SMS delivery failures
- Alert on unusual login patterns
- Dashboard for key metrics

---

## API Flow Diagrams

### Signup Flow
```
User → Frontend → Backend
1. Enter phone → Send SMS verification
2. Enter code → Verify SMS
3. Enter details → Create user + Send tokens
4. Store tokens → Redirect to dashboard
```

### Login Flow
```
User → Frontend → Backend
1. Enter credentials → Validate user
2. Return tokens → Store in memory
3. Redirect to dashboard
```

### Token Refresh Flow
```
Frontend → Backend
1. Access token expires → 401 error
2. Send refresh token → Validate
3. Return new tokens → Store in memory
4. Retry original request
```

---

## Support

For issues or questions:
- Email: support@tiktax.co.il
- Documentation: https://docs.tiktax.co.il
- API Status: https://status.tiktax.co.il

---

**Last Updated:** November 2024
**Version:** 1.0.0
