# Quick Start Guide - Environment & Axios Configuration

## 🚀 Getting Started (5 Minutes)

### Step 1: Create Environment File
```bash
# In frontend directory
cp .env.example .env
```

### Step 2: Add Your API Keys
Edit `frontend/.env`:
```env
# Required - Update this
VITE_API_BASE_URL=http://localhost:3000/api

# Optional - Add when available
VITE_GOOGLE_CLOUD_VISION_API_KEY=your_actual_key_here
VITE_STRIPE_PUBLIC_KEY=pk_test_your_actual_key_here
VITE_AWS_S3_BUCKET=your_bucket_name_here
```

### Step 3: Start Development Server
```bash
npm run dev
```

### Step 4: Verify Configuration
1. Open browser console
2. Look for: `🔧 Application Configuration`
3. Verify all values are correct
4. Check sensitive values are masked (e.g., `AIza...3xYz`)

---

## 💻 Usage in Your Code

### Import Configured Axios
```typescript
import axios from '@/config/axios';
```

### Import Configuration
```typescript
import config from '@/config';
```

### Import Auth Store
```typescript
import { useAuthStore } from '@/stores';
```

---

## 📋 Common Use Cases

### 1. Make Authenticated API Call
```typescript
import axios from '@/config/axios';

async function getReceipts() {
  // Token automatically attached by interceptor
  const response = await axios.get('/receipts');
  return response.data;
}
```

### 2. Login User
```typescript
import axios from '@/config/axios';
import { useAuthStore } from '@/stores';

async function login(email: string, password: string) {
  const response = await axios.post('/auth/login', { email, password });
  const { accessToken, refreshToken, user } = response.data;
  
  // Store in memory (NOT localStorage!)
  useAuthStore.getState().setTokens(accessToken, refreshToken);
  useAuthStore.getState().setUser(user);
}
```

### 3. Logout User
```typescript
import { useAuthStore } from '@/stores';

function logout() {
  useAuthStore.getState().clearAuth();
  window.location.href = '/login';
}
```

### 4. Check Auth Status (In Component)
```typescript
import { useAuthStore } from '@/stores';

function MyComponent() {
  const { isAuthenticated, user } = useAuthStore();
  
  if (!isAuthenticated) {
    return <div>Please log in</div>;
  }
  
  return <div>Welcome, {user?.firstName}!</div>;
}
```

### 5. Access Configuration
```typescript
import config from '@/config';

function setupStripe() {
  const stripe = loadStripe(config.stripePublicKey);
  // ...
}

function checkEnvironment() {
  if (config.isDevelopment) {
    console.log('Running in development mode');
  }
}
```

---

## 🔒 Security Checklist

Before going to production, verify:

- [ ] ✅ Tokens stored in Zustand (memory only)
- [ ] ❌ NO tokens in localStorage
- [ ] ✅ .env file NOT committed to git
- [ ] ✅ .env.example IS committed (no secrets)
- [ ] ✅ Production API keys configured
- [ ] ✅ Token refresh flow tested
- [ ] ✅ HTTPS enabled in production
- [ ] ✅ CORS configured correctly

---

## 🧪 Test Token Refresh Flow

### Manual Testing:
1. Login to get tokens
2. Check auth store: `useAuthStore.getState().accessToken`
3. Set backend token expiration to 1 minute
4. Wait for expiration
5. Make API call
6. Watch network tab for `/auth/refresh` call
7. Verify original request retried automatically

### Expected Behavior:
```
1. GET /receipts → 401 Unauthorized
2. POST /auth/refresh → 200 OK (new tokens)
3. GET /receipts → 200 OK (retry with new token)
```

---

## 🐛 Common Issues

### Issue: "Missing required environment variables"
**Cause:** `.env` file not created  
**Fix:** `cp .env.example .env`

---

### Issue: Requests not authenticated
**Cause:** No token in auth store  
**Fix:** Login first to get tokens

---

### Issue: Token refresh loop
**Cause:** Refresh endpoint also returns 401  
**Fix:** Check backend `/auth/refresh` endpoint

---

### Issue: CORS errors
**Cause:** Backend not allowing frontend origin  
**Fix:** Configure backend CORS settings:
```javascript
// Backend CORS config
app.use(cors({
  origin: 'http://localhost:5173', // Vite dev server
  credentials: true
}));
```

---

### Issue: Changes to .env not reflected
**Cause:** Vite needs restart for env changes  
**Fix:** Stop dev server (Ctrl+C) and restart:
```bash
npm run dev
```

---

## 📚 Additional Resources

- **Full Documentation:** `src/config/README.md`
- **Implementation Summary:** `IMPLEMENTATION_SUMMARY.md`
- **Type Definitions:** `src/types/index.ts`
- **Auth Store:** `src/stores/auth.store.ts`

---

## 🎯 Next Steps

1. **Create Services:**
   - `src/services/auth.service.ts`
   - `src/services/receipt.service.ts`

2. **Create Pages:**
   - Login page
   - Signup page
   - Protected routes

3. **Test Integration:**
   - Login flow
   - Token refresh
   - Logout
   - API calls

4. **Add Error Handling:**
   - Create error handler utilities
   - Add toast notifications
   - Create error boundaries

---

**Quick Reference:**
- Axios instance: `@/config/axios`
- Configuration: `@/config`
- Auth store: `@/stores`
- Types: `@/types`

**Remember:** NEVER use localStorage for tokens! 🔒
