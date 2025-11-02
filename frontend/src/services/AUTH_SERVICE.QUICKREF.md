# Auth Service Quick Reference

## Import

```typescript
import { authService } from '@/services';
// or
import { login, signup, logout } from '@/services/auth.service';
```

## Quick Function Reference

### 🔐 Authentication

```typescript
// Signup
await authService.signup(signupData);

// Login
await authService.login({ email, password, rememberMe });

// Logout
await authService.logout();
```

### 🔄 Token Management

```typescript
// Refresh access token
await authService.refreshToken(currentRefreshToken);

// Get current user
await authService.getCurrentUser();
```

### 📱 SMS Verification

```typescript
// Send code
await authService.sendSMSVerification('0501234567');

// Verify code
await authService.verifySMSCode('0501234567', '123456');
```

### 🔑 Password Management

```typescript
// Request reset
await authService.requestPasswordReset('email@example.com');

// Reset with token
await authService.resetPassword(token, newPassword);

// Change (authenticated)
await authService.changePassword({
  currentPassword,
  newPassword,
  confirmPassword
});
```

## Error Handling Pattern

```typescript
try {
  const response = await authService.login({ email, password });
  // Success handling
} catch (error) {
  toast.error(error.message); // Hebrew error message
}
```

## Common Patterns

### Login Flow
```typescript
const response = await authService.login({ email, password });
useAuthStore.getState().setAuth(
  response.user,
  response.accessToken,
  response.refreshToken
);
navigate('/dashboard');
```

### Logout Flow
```typescript
await authService.logout();
useAuthStore.getState().clearAuth();
navigate('/login');
```

### Protected API Call
```typescript
// Access token automatically added by Axios interceptor
const user = await authService.getCurrentUser();
```

## Security Rules

✅ **DO:** Store tokens in Zustand (memory)  
❌ **DON'T:** Use localStorage for tokens  
✅ **DO:** Clear auth on logout  
✅ **DO:** Handle token refresh automatically

## Error Messages (Hebrew)

| Code | Message |
|------|---------|
| INVALID_CREDENTIALS | שם משתמש או סיסמה שגויים |
| EMAIL_EXISTS | כתובת המייל כבר קיימת במערכת |
| TOKEN_EXPIRED | תוקף ההתחברות פג |
| NETWORK_ERROR | שגיאת רשת |

See `errorHandler.ts` for complete list.
