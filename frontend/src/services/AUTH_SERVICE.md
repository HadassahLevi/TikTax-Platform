# Authentication Service Documentation

## Overview

The authentication service layer provides a clean, type-safe interface for all auth-related API calls in Tik-Tax. All functions include proper error handling with Hebrew messages and comprehensive TypeScript typing.

## File Location

```
/src/services/auth.service.ts
```

## Features

✅ **Full TypeScript Support** - All functions fully typed with interfaces from `auth.types.ts`  
✅ **Hebrew Error Messages** - User-friendly error messages via `errorHandler.ts`  
✅ **Comprehensive JSDoc** - Every function documented with examples  
✅ **Consistent Error Handling** - All errors caught and transformed  
✅ **Development Logging** - Detailed error logs in development mode  
✅ **30-Second Timeout** - All requests timeout after 30 seconds  
✅ **Auto Token Injection** - Access token automatically added by Axios interceptor

## Installation & Setup

### Import Individual Functions

```typescript
import { login, signup, logout } from '@/services/auth.service';
```

### Import Service Object

```typescript
import { authService } from '@/services';

await authService.login({ email, password });
```

## API Functions

### 1. Signup

Register a new user account (3-step signup process).

```typescript
signup(data: SignupData): Promise<AuthResponse>
```

**Endpoint:** `POST /api/auth/signup`

**Parameters:**
```typescript
{
  // Step 1: Personal Info
  fullName: string;        // "דוד כהן"
  idNumber: string;        // "123456789"
  email: string;           // "david@example.com"
  password: string;        // "SecurePass123"
  phone: string;           // "0501234567"
  
  // Step 2: Business Info
  businessName: string;    // "דוד כהן - עיצוב גרפי"
  businessNumber: string;  // "123456789"
  businessType: 'licensed_dealer' | 'exempt_dealer' | 'limited_company';
  
  // Step 3: Verification
  verificationCode: string; // "123456"
}
```

**Returns:**
```typescript
{
  user: User;
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}
```

**Example:**
```typescript
try {
  const response = await signup({
    fullName: 'דוד כהן',
    idNumber: '123456789',
    email: 'david@example.com',
    password: 'SecurePass123',
    phone: '0501234567',
    businessName: 'דוד כהן - עיצוב גרפי',
    businessNumber: '123456789',
    businessType: 'licensed_dealer',
    verificationCode: '123456'
  });
  
  // Store tokens in auth store (NOT localStorage!)
  useAuthStore.getState().setAuth(
    response.user,
    response.accessToken,
    response.refreshToken
  );
  
  navigate('/dashboard');
} catch (error) {
  toast.error(error.message); // Hebrew error message
}
```

---

### 2. Login

Authenticate user with email and password.

```typescript
login(data: LoginData): Promise<AuthResponse>
```

**Endpoint:** `POST /api/auth/login`

**Parameters:**
```typescript
{
  email: string;           // "david@example.com"
  password: string;        // "SecurePass123"
  rememberMe?: boolean;    // extends token expiry
}
```

**Returns:** Same as signup

**Example:**
```typescript
try {
  const response = await login({
    email: 'david@example.com',
    password: 'SecurePass123',
    rememberMe: true
  });
  
  useAuthStore.getState().setAuth(
    response.user,
    response.accessToken,
    response.refreshToken
  );
  
  navigate('/dashboard');
} catch (error) {
  toast.error(error.message); // "שם משתמש או סיסמה שגויים"
}
```

---

### 3. Logout

Log out current user and invalidate session.

```typescript
logout(): Promise<void>
```

**Endpoint:** `POST /api/auth/logout`

**Example:**
```typescript
try {
  await logout();
  useAuthStore.getState().clearAuth();
  navigate('/login');
} catch (error) {
  console.error('Logout failed:', error.message);
  // Still clear local tokens even if server call fails
  useAuthStore.getState().clearAuth();
}
```

---

### 4. Refresh Token

Obtain new access token using refresh token.

```typescript
refreshToken(refreshToken: string): Promise<RefreshTokenResponse>
```

**Endpoint:** `POST /api/auth/refresh`

**Parameters:**
- `refreshToken` - Current refresh token from auth store

**Returns:**
```typescript
{
  accessToken: string;
  expiresIn: number;
}
```

**Example:**
```typescript
try {
  const currentRefreshToken = useAuthStore.getState().refreshToken;
  const response = await refreshToken(currentRefreshToken);
  
  // Update access token in store
  useAuthStore.getState().setAccessToken(response.accessToken);
} catch (error) {
  console.error('Token refresh failed:', error.message);
  // Redirect to login
  useAuthStore.getState().clearAuth();
  navigate('/login');
}
```

**Note:** This is usually called automatically by the Axios interceptor on 401 responses.

---

### 5. Get Current User

Get current authenticated user's profile.

```typescript
getCurrentUser(): Promise<User>
```

**Endpoint:** `GET /api/auth/me`

**Returns:** User object with all profile data

**Example:**
```typescript
try {
  const user = await getCurrentUser();
  console.log('Current user:', user.fullName);
  console.log('Receipts used:', user.receiptsUsedThisMonth);
  console.log('Subscription:', user.subscriptionPlan);
  
  // Update user in store
  useAuthStore.getState().setUser(user);
} catch (error) {
  console.error('Failed to get user:', error.message);
}
```

---

### 6. Send SMS Verification

Send 6-digit verification code via SMS.

```typescript
sendSMSVerification(phone: string): Promise<void>
```

**Endpoint:** `POST /api/auth/send-verification`

**Parameters:**
- `phone` - Israeli phone number (format: `05XXXXXXXX` or `05X-XXX-XXXX`)

**Example:**
```typescript
try {
  await sendSMSVerification('0501234567');
  toast.success('קוד אימות נשלח בהצלחה!');
  setShowCodeInput(true);
} catch (error) {
  toast.error(error.message); // "שליחת קוד האימות נכשלה"
}
```

---

### 7. Verify SMS Code

Confirm 6-digit verification code from SMS.

```typescript
verifySMSCode(phone: string, code: string): Promise<void>
```

**Endpoint:** `POST /api/auth/verify-sms`

**Parameters:**
- `phone` - Phone number being verified
- `code` - 6-digit code from SMS

**Example:**
```typescript
try {
  await verifySMSCode('0501234567', '123456');
  toast.success('מספר הטלפון אומת בהצלחה!');
  setPhoneVerified(true);
  // Proceed to complete signup
} catch (error) {
  toast.error(error.message); // "קוד אימות שגוי"
}
```

---

### 8. Request Password Reset

Send password reset link to email.

```typescript
requestPasswordReset(email: string): Promise<void>
```

**Endpoint:** `POST /api/auth/forgot-password`

**Parameters:**
- `email` - Email address of account to reset

**Example:**
```typescript
try {
  await requestPasswordReset('david@example.com');
  toast.success('קישור לאיפוס סיסמה נשלח למייל שלך');
  setEmailSent(true);
} catch (error) {
  toast.error(error.message);
}
```

---

### 9. Reset Password

Confirm password reset with token from email.

```typescript
resetPassword(token: string, newPassword: string): Promise<void>
```

**Endpoint:** `POST /api/auth/reset-password`

**Parameters:**
- `token` - Reset token from email URL
- `newPassword` - New password to set

**Example:**
```typescript
try {
  // Extract token from URL: /reset-password?token=abc123
  const urlParams = new URLSearchParams(location.search);
  const token = urlParams.get('token');
  
  await resetPassword(token, 'NewSecurePass123');
  toast.success('הסיסמה שונתה בהצלחה!');
  navigate('/login');
} catch (error) {
  toast.error(error.message); // "קישור לאיפוס סיסמה פג תוקפו"
}
```

---

### 10. Change Password

Change password for authenticated user.

```typescript
changePassword(data: ChangePasswordData): Promise<void>
```

**Endpoint:** `PUT /api/auth/change-password`

**Parameters:**
```typescript
{
  currentPassword: string;
  newPassword: string;
  confirmPassword: string;
}
```

**Example:**
```typescript
try {
  await changePassword({
    currentPassword: 'OldPass123',
    newPassword: 'NewSecurePass123',
    confirmPassword: 'NewSecurePass123'
  });
  toast.success('הסיסמה שונתה בהצלחה!');
} catch (error) {
  toast.error(error.message); // "הסיסמה הנוכחית שגויה"
}
```

---

## Error Handling

All functions use consistent error handling:

```typescript
try {
  await authService.login({ email, password });
} catch (error) {
  // error.message contains Hebrew error message
  toast.error(error.message);
}
```

### Common Error Messages

| Error Code | Hebrew Message |
|------------|---------------|
| `INVALID_CREDENTIALS` | שם משתמש או סיסמה שגויים |
| `EMAIL_EXISTS` | כתובת המייל כבר קיימת במערכת |
| `PHONE_EXISTS` | מספר הטלפון כבר רשום במערכת |
| `TOKEN_EXPIRED` | תוקף ההתחברות פג. אנא התחבר מחדש |
| `INVALID_VERIFICATION_CODE` | קוד אימות שגוי |
| `WEAK_PASSWORD` | הסיסמה חלשה מדי |
| `NETWORK_ERROR` | שגיאת רשת. אנא בדוק את החיבור לאינטרנט |
| `SERVER_ERROR` | שגיאת שרת. אנא נסה שוב מאוחר יותר |

See `utils/errorHandler.ts` for complete list.

---

## Integration with Auth Store

The auth service works seamlessly with the Zustand auth store:

```typescript
import { useAuthStore } from '@/stores/auth.store';
import { authService } from '@/services';

// Login flow
const handleLogin = async (email: string, password: string) => {
  try {
    const response = await authService.login({ email, password });
    
    // Store in Zustand (memory only - NOT localStorage!)
    useAuthStore.getState().setAuth(
      response.user,
      response.accessToken,
      response.refreshToken
    );
    
    navigate('/dashboard');
  } catch (error) {
    toast.error(error.message);
  }
};

// Logout flow
const handleLogout = async () => {
  try {
    await authService.logout();
  } catch (error) {
    console.error('Logout failed:', error);
  } finally {
    // Always clear local auth state
    useAuthStore.getState().clearAuth();
    navigate('/login');
  }
};
```

---

## Security Best Practices

### ✅ DO:
- Store tokens in Zustand auth store (memory only)
- Use `refreshToken()` to renew expired access tokens
- Clear auth state on logout
- Validate user input before sending to API
- Show Hebrew error messages to users

### ❌ DON'T:
- **NEVER** store tokens in `localStorage` (security vulnerability!)
- **NEVER** log sensitive data (passwords, tokens) in production
- **NEVER** expose tokens in URLs or query parameters
- **NEVER** store tokens in cookies without `httpOnly` flag

---

## Development Tips

### Enable Request Logging

Errors are automatically logged in development mode:

```typescript
if (import.meta.env.DEV) {
  console.group('❌ Error (Login)');
  console.error(error);
  console.log('Status:', error.response?.status);
  console.log('Data:', error.response?.data);
  console.groupEnd();
}
```

### Test with Mock Data

For development without backend:

```typescript
// In auth.service.ts (development only!)
if (import.meta.env.DEV && import.meta.env.VITE_USE_MOCK_AUTH) {
  return {
    user: { /* mock user data */ },
    accessToken: 'mock-access-token',
    refreshToken: 'mock-refresh-token',
    expiresIn: 900
  };
}
```

---

## Complete Example: Signup Flow

```typescript
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '@/services';
import { useAuthStore } from '@/stores/auth.store';
import { toast } from '@/components/ui/Toast';

function SignupFlow() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    fullName: '',
    idNumber: '',
    email: '',
    password: '',
    phone: '',
    businessName: '',
    businessNumber: '',
    businessType: 'licensed_dealer',
    verificationCode: ''
  });
  
  // Step 3: Send SMS verification
  const handleSendCode = async () => {
    try {
      await authService.sendSMSVerification(formData.phone);
      toast.success('קוד אימות נשלח בהצלחה!');
      setStep(3);
    } catch (error) {
      toast.error(error.message);
    }
  };
  
  // Step 3: Verify code and complete signup
  const handleVerifyAndSignup = async () => {
    try {
      // Verify SMS code first
      await authService.verifySMSCode(formData.phone, formData.verificationCode);
      
      // Complete signup
      const response = await authService.signup(formData);
      
      // Store auth data
      useAuthStore.getState().setAuth(
        response.user,
        response.accessToken,
        response.refreshToken
      );
      
      toast.success('החשבון נוצר בהצלחה!');
      navigate('/dashboard');
    } catch (error) {
      toast.error(error.message);
    }
  };
  
  return (
    <div>
      {/* Step 1: Personal Info */}
      {/* Step 2: Business Info */}
      {/* Step 3: SMS Verification */}
    </div>
  );
}
```

---

## Testing

### Unit Tests

```typescript
import { describe, it, expect, vi } from 'vitest';
import { authService } from './auth.service';
import apiClient from '../config/axios';

vi.mock('../config/axios');

describe('Auth Service', () => {
  it('should login successfully', async () => {
    const mockResponse = {
      data: {
        user: { id: '1', email: 'test@example.com' },
        accessToken: 'token',
        refreshToken: 'refresh',
        expiresIn: 900
      }
    };
    
    apiClient.post.mockResolvedValue(mockResponse);
    
    const result = await authService.login({
      email: 'test@example.com',
      password: 'password123'
    });
    
    expect(result).toEqual(mockResponse.data);
  });
  
  it('should handle login errors', async () => {
    apiClient.post.mockRejectedValue({
      response: {
        status: 401,
        data: { code: 'INVALID_CREDENTIALS' }
      }
    });
    
    await expect(authService.login({
      email: 'test@example.com',
      password: 'wrong'
    })).rejects.toThrow('שם משתמש או סיסמה שגויים');
  });
});
```

---

## Related Files

- **Types:** `/src/types/auth.types.ts`
- **Axios Config:** `/src/config/axios.ts`
- **Error Handler:** `/src/utils/errorHandler.ts`
- **Auth Store:** `/src/stores/auth.store.ts`

---

## Support

For issues or questions:
1. Check error handler messages in `utils/errorHandler.ts`
2. Review Axios interceptor in `config/axios.ts`
3. Verify backend API endpoints match
4. Check browser console for detailed error logs (development mode)

---

**Last Updated:** November 2, 2025  
**Version:** 1.0.0
