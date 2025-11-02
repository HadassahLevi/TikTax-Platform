# Environment & Axios Configuration

## Overview
This directory contains the environment configuration system and HTTP client setup for Tik-Tax.

## Files

### `index.ts` - Environment Configuration
**Purpose:** Typed configuration object from environment variables with validation

**Features:**
- ✅ Type-safe configuration access
- ✅ Required variable validation (throws in production)
- ✅ Development logging with masked sensitive values
- ✅ Feature flags support
- ✅ Environment detection (dev/prod/test)

**Usage:**
```typescript
import config from '@/config';

// Access configuration
const apiUrl = config.apiBaseUrl;
const isDevMode = config.isDevelopment;
```

**Configuration Properties:**
- `apiBaseUrl` - Backend API base URL
- `googleCloudVisionApiKey` - Google Vision API key for OCR
- `stripePublicKey` - Stripe public key for payments
- `awsS3Bucket` - AWS S3 bucket name for receipt storage
- `enableAnalytics` - Analytics feature flag
- `maintenanceMode` - Maintenance mode flag
- `isDevelopment` - Development environment flag
- `isProduction` - Production environment flag
- `isTest` - Test environment flag

---

### `axios.ts` - HTTP Client
**Purpose:** Configured Axios instance with interceptors for auth and error handling

**Features:**
- ✅ Base URL from config
- ✅ 30-second timeout
- ✅ Request interceptor: Auto-attach auth tokens
- ✅ Performance tracking: Log slow requests (>3s)
- ✅ Auto token refresh on 401
- ✅ Network error handling
- ✅ HTTP error logging

**Security:**
- 🔒 Tokens from Zustand store (NEVER localStorage)
- 🔒 Auto token refresh with retry logic
- 🔒 Auto logout on refresh failure

**Usage:**
```typescript
import axios from '@/config/axios';

// All requests automatically include auth token
const response = await axios.get('/receipts');
const data = await axios.post('/receipts', receiptData);
```

**Interceptor Flow:**

**Request:**
1. Get access token from auth store
2. Attach `Authorization: Bearer {token}` header
3. Add request timestamp for performance tracking

**Response:**
1. Check request duration (warn if >3 seconds)
2. On 401 (Unauthorized):
   - Try to refresh token automatically
   - Retry original request with new token
   - If refresh fails: clear auth, redirect to /login
3. On 403 (Forbidden): Log access denied
4. On 404: Log not found
5. On 500+: Log server error
6. On network error: Log connection issue

---

## Environment Variables

See `.env.example` for all available variables.

**Required Variables:**
- `VITE_API_BASE_URL` - Backend API URL

**Optional Variables:**
- All others have defaults

**Setup:**
1. Copy `.env.example` to `.env`
2. Fill in your actual values
3. NEVER commit `.env` (already in .gitignore)

---

## Security Notes

### 🔒 CRITICAL: Token Storage
- ❌ NEVER use localStorage for tokens
- ✅ ALWAYS use Zustand store (memory only)
- ✅ Tokens cleared on page refresh (by design)
- ✅ Use refresh token to maintain session

### Why Memory-Only?
- LocalStorage vulnerable to XSS attacks
- Memory storage requires refresh token flow
- More secure for sensitive financial data

---

## Error Handling

**Network Errors:**
```typescript
try {
  const response = await axios.get('/receipts');
} catch (error) {
  // Network error or HTTP error
  console.error(error);
}
```

**Auto-Handled:**
- 401: Token refresh + retry (automatic)
- 403: Logged to console
- 404: Logged to console
- 500+: Logged to console

**Manual Handling:**
Use in service layer for user-facing errors:
```typescript
import { handleAPIError } from '@/utils/errorHandlers';

try {
  await axios.post('/receipts', data);
} catch (error) {
  const message = handleAPIError(error);
  toast.error(message);
}
```

---

## Performance Monitoring

**Automatic Logging:**
- Requests >3 seconds logged to console
- Request duration tracked automatically
- View in browser console (development only)

**Example Output:**
```
⚠️ Slow Response: /receipts/process took 4532ms
```

---

## Development Tips

### View Configuration
Open browser console to see configuration on app load:
```
🔧 Application Configuration
  Environment: development
  API Base URL: http://localhost:3000/api
  Google Vision API Key: AIza...3xYz
  ...
```

### Test Token Refresh
1. Set token expiration to 1 minute (backend)
2. Wait for token to expire
3. Make API call - should auto-refresh
4. Check network tab for `/auth/refresh` call

### Debug Interceptors
Add breakpoints in:
- Request interceptor (line ~30)
- Response interceptor (line ~60)
- Token refresh logic (line ~90)

---

## Migration Notes

**From Old Setup:**
If migrating from localStorage-based auth:
1. Remove all `localStorage.setItem('token', ...)` calls
2. Use `useAuthStore.getState().setTokens()` instead
3. Remove manual Authorization header setting
4. Let interceptors handle it automatically

**Before:**
```typescript
localStorage.setItem('token', accessToken);
axios.get('/receipts', {
  headers: { Authorization: `Bearer ${accessToken}` }
});
```

**After:**
```typescript
useAuthStore.getState().setTokens(accessToken, refreshToken);
axios.get('/receipts'); // Token auto-attached
```

---

## Testing

**Mock Axios in Tests:**
```typescript
import axios from '@/config/axios';
import MockAdapter from 'axios-mock-adapter';

const mock = new MockAdapter(axios);
mock.onGet('/receipts').reply(200, mockData);
```

---

## Future Improvements

- [ ] Add request retry logic (3 attempts)
- [ ] Add request caching (React Query)
- [ ] Add request deduplication
- [ ] Add offline queue
- [ ] Add request/response transformers
- [ ] Add custom error classes

---

**Last Updated:** November 2, 2025
