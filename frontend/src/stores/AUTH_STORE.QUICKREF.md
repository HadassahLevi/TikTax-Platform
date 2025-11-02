# Auth Store Quick Reference

**File:** `src/stores/auth.store.ts`

Complete Zustand store for authentication state management with TypeScript, DevTools, and Hebrew error messages.

---

## ✅ Implementation Complete

- ✅ Zustand installed (`npm install zustand`)
- ✅ Full TypeScript support
- ✅ DevTools integration for debugging
- ✅ Memory-only token storage (NOT localStorage)
- ✅ Hebrew error messages
- ✅ Optimized selectors
- ✅ All async actions (login, signup, logout, token refresh, check auth)

---

## 🔥 Quick Usage

### 1. Login Page
```typescript
import { useAuthStore } from '@/stores';

function LoginPage() {
  const { login, isLoading, error } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (data) => {
    try {
      await login(data);
      navigate('/dashboard');
    } catch (err) {
      // Error already in store.error
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && <div className="error">{error.message}</div>}
      <button disabled={isLoading}>
        {isLoading ? 'מתחבר...' : 'התחבר'}
      </button>
    </form>
  );
}
```

### 2. Protected Route
```typescript
import { useAuthStore, selectIsAuthenticated } from '@/stores';

function ProtectedRoute({ children }) {
  const isAuthenticated = useAuthStore(selectIsAuthenticated);
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  return children;
}
```

### 3. User Profile Display
```typescript
import { useAuthStore, selectUser } from '@/stores';

function UserProfile() {
  const user = useAuthStore(selectUser);
  
  if (!user) return null;
  
  return (
    <div>
      <h2>{user.fullName}</h2>
      <p>{user.businessName}</p>
      <p>חבילה: {user.subscriptionPlan}</p>
      <p>קבלות: {user.receiptsUsedThisMonth}/{user.receiptsLimit}</p>
    </div>
  );
}
```

### 4. App Initialization
```typescript
import { useEffect } from 'react';
import { useAuthStore } from '@/stores';

function App() {
  const { checkAuth } = useAuthStore();
  
  useEffect(() => {
    // Restore session on app load
    checkAuth();
  }, [checkAuth]);
  
  return <Routes>...</Routes>;
}
```

### 5. Logout Button
```typescript
import { useAuthStore } from '@/stores';

function LogoutButton() {
  const { logout, isLoading } = useAuthStore();
  const navigate = useNavigate();
  
  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (err) {
      // Auth cleared anyway, safe to redirect
      navigate('/login');
    }
  };
  
  return (
    <button onClick={handleLogout} disabled={isLoading}>
      התנתק
    </button>
  );
}
```

---

## 📦 Available State

| Property | Type | Description |
|----------|------|-------------|
| `user` | `User \| null` | Current authenticated user |
| `accessToken` | `string \| null` | JWT access token (memory only) |
| `refreshToken` | `string \| null` | JWT refresh token (memory only) |
| `isAuthenticated` | `boolean` | Whether user is logged in |
| `isLoading` | `boolean` | Loading state for async operations |
| `error` | `AuthError \| null` | Current error (Hebrew message) |

---

## 🎯 Available Actions

### Sync Actions
| Action | Signature | Description |
|--------|-----------|-------------|
| `setUser` | `(user: User) => void` | Set user data |
| `setTokens` | `(access: string, refresh: string) => void` | Set auth tokens |
| `clearAuth` | `() => void` | Clear all auth state |
| `setLoading` | `(loading: boolean) => void` | Set loading state |
| `setError` | `(error: AuthError \| null) => void` | Set/clear error |

### Async Actions
| Action | Signature | Description |
|--------|-----------|-------------|
| `login` | `(data: LoginData) => Promise<void>` | Log in user |
| `signup` | `(data: SignupData) => Promise<void>` | Register new user |
| `logout` | `() => Promise<void>` | Log out user |
| `refreshAccessToken` | `() => Promise<string>` | Refresh access token |
| `checkAuth` | `() => Promise<void>` | Verify token validity |

---

## 🎨 Optimized Selectors

Use selectors to prevent unnecessary re-renders:

```typescript
import { 
  useAuthStore,
  selectUser,
  selectIsAuthenticated,
  selectIsLoading,
  selectError,
  selectAccessToken,
  selectRefreshToken,
  selectSubscriptionInfo,
  selectBusinessInfo
} from '@/stores';

// Usage
const user = useAuthStore(selectUser);
const isAuthenticated = useAuthStore(selectIsAuthenticated);
const subscriptionInfo = useAuthStore(selectSubscriptionInfo);
```

### Composite Selectors

**selectSubscriptionInfo** - Returns:
```typescript
{
  plan: 'free' | 'basic' | 'pro' | 'business',
  status: 'active' | 'trial' | 'cancelled' | 'past_due',
  receiptsUsed: number,
  receiptsLimit: number
} | null
```

**selectBusinessInfo** - Returns:
```typescript
{
  name: string,
  number: string,
  type: 'licensed_dealer' | 'exempt_dealer' | 'limited_company'
} | null
```

---

## 🔐 Security Features

1. **Memory-Only Storage**: Tokens NEVER stored in localStorage/sessionStorage
2. **Automatic Cleanup**: Auth cleared on logout, token refresh failure, or session expiry
3. **Error Handling**: Hebrew error messages for user-facing errors
4. **Token Refresh**: Automatic token refresh on 401 errors (via Axios interceptor)
5. **Type Safety**: Full TypeScript support with strict types

---

## 🛠️ DevTools

The store includes Zustand DevTools support for debugging:

1. Install Redux DevTools Extension in your browser
2. Open DevTools → Redux tab
3. See all auth state changes in real-time
4. Time-travel through state changes
5. Monitor async action flow

Store name in DevTools: **`auth-store`**

---

## 📝 TypeScript Types

All types are imported from `@/types/auth.types`:

```typescript
import type { 
  User,
  LoginData,
  SignupData,
  AuthState,
  AuthActions,
  AuthError
} from '@/types/auth.types';
```

---

## ⚠️ Important Notes

### 1. Token Persistence
Tokens are stored **in memory only** and will be lost on page refresh. This is intentional for security.

To restore session:
```typescript
useEffect(() => {
  checkAuth(); // Call on app initialization
}, []);
```

### 2. Error Handling
All async actions throw errors but also set `store.error`:

```typescript
try {
  await login(data);
} catch (error) {
  // Error available at: useAuthStore.getState().error
  console.error(error.message); // Hebrew message
}
```

### 3. Logout Always Succeeds
The `logout` action will **always** clear local auth state, even if the server call fails:

```typescript
await logout(); // Always safe to navigate after this
navigate('/login');
```

### 4. Token Refresh
The `refreshAccessToken` action is typically called by Axios interceptor, not manually:

```typescript
// In axios.ts interceptor
const newToken = await useAuthStore.getState().refreshAccessToken();
config.headers.Authorization = `Bearer ${newToken}`;
```

---

## 🔄 State Flow Diagram

```
User Action (login/signup)
    ↓
setLoading(true)
    ↓
Call Auth Service
    ↓
Success? ──┬── Yes → Set user + tokens + isAuthenticated
           │         setLoading(false)
           │
           └── No → Set error (Hebrew)
                    setLoading(false)
                    Throw error
```

---

## 📚 Related Files

- **Types**: `src/types/auth.types.ts` - All TypeScript definitions
- **Service**: `src/services/auth.service.ts` - API layer
- **Axios Config**: `src/config/axios.ts` - HTTP client with interceptors

---

## ✅ Checklist for Integration

- [ ] Import store in login page
- [ ] Import store in signup page
- [ ] Create protected route wrapper with `selectIsAuthenticated`
- [ ] Call `checkAuth()` on app initialization
- [ ] Set up Axios interceptor for token refresh
- [ ] Display `error.message` in Hebrew to user
- [ ] Show loading state during async operations
- [ ] Test logout clears all state
- [ ] Verify tokens not in localStorage (check DevTools Application tab)

---

## 🚀 Next Steps

1. **Create Login Page**: Use store for authentication
2. **Create Signup Page**: Multi-step form with store
3. **Protected Routes**: Wrap routes with auth check
4. **Axios Interceptor**: Auto-refresh tokens on 401
5. **Error Display**: Toast notifications for auth errors

---

**Last Updated:** November 2, 2025
**Status:** ✅ Complete and Ready to Use
