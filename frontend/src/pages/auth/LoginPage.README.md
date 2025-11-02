# LoginPage - README

## Component Overview

**LoginPage** is a professional, fully-featured authentication page designed for the Tik-Tax platform. It provides a secure and user-friendly login experience with comprehensive form validation, Hebrew language support, and modern UI/UX patterns.

---

## Key Features

### 🎨 Design
- **Professional card layout** centered on viewport
- **Tik-Tax branding** with logo and colors
- **Clean, minimal interface** following design system
- **RTL support** for Hebrew content
- **Responsive design** optimized for all devices

### 🔐 Security
- **Password visibility toggle** for user convenience
- **Secure credential handling** (no localStorage)
- **Input validation** (client-side)
- **Auto-complete support** for password managers
- **HTTPS enforcement** (backend)

### ✨ User Experience
- **Auto-focus email field** on page load
- **Real-time validation** with helpful error messages
- **Loading states** during authentication
- **Auto-redirect** if already logged in
- **Remember me** option (Phase 2)
- **Forgot password** recovery flow

### ♿ Accessibility
- **WCAG 2.1 AA compliant**
- **Keyboard navigation** support
- **Screen reader friendly** with ARIA labels
- **Visible focus indicators**
- **Semantic HTML** structure

---

## Installation

No additional installation needed - uses existing project dependencies:
- `react-hook-form` (already installed)
- `lucide-react` (already installed)
- `react-router-dom` (already installed)

---

## Usage

### Basic Setup

```tsx
// In your router configuration (App.tsx or routes.tsx)
import { LoginPage } from '@/pages/auth';

<Routes>
  <Route path="/login" element={<LoginPage />} />
  {/* Other routes */}
</Routes>
```

### With Protected Routes

```tsx
import { LoginPage } from '@/pages/auth';
import { useRequireAuth } from '@/hooks/useAuth';

// Login route (public)
<Route path="/login" element={<LoginPage />} />

// Protected route
<Route 
  path="/dashboard" 
  element={
    <RequireAuth>
      <Dashboard />
    </RequireAuth>
  } 
/>
```

---

## Component Architecture

### Dependencies

```typescript
// React Core
import React, { useState, useEffect } from 'react';

// Form Management
import { useForm } from 'react-hook-form';

// Routing
import { Link, useNavigate } from 'react-router-dom';

// Icons
import { Mail, Lock, Eye, EyeOff } from 'lucide-react';

// UI Components
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';

// Custom Hooks
import { useAuth } from '@/hooks/useAuth';
import { useToast } from '@/hooks/useToast';
```

### State Management

```typescript
// Form state (react-hook-form)
const { register, handleSubmit, formState } = useForm<LoginFormData>();

// Password visibility toggle
const [showPassword, setShowPassword] = useState(false);

// Authentication state (Zustand)
const { login, isAuthenticated } = useAuth();

// Notifications
const { showError, showSuccess } = useToast();
```

---

## Form Validation

### Validation Schema

The component uses `react-hook-form` with inline validation rules:

#### Email Field
```typescript
register('email', {
  required: 'אימייל הוא שדה חובה',
  pattern: {
    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
    message: 'כתובת אימייל לא תקינה'
  }
})
```

**Validates:**
- ✅ Email is not empty
- ✅ Email has valid format (user@domain.com)

#### Password Field
```typescript
register('password', {
  required: 'סיסמה היא שדה חובה',
  minLength: {
    value: 8,
    message: 'סיסמה חייבת להכיל לפחות 8 תווים'
  }
})
```

**Validates:**
- ✅ Password is not empty
- ✅ Password has minimum 8 characters

### Error Display

Errors are displayed below their respective fields:

```tsx
<Input
  {...register('email', validationRules)}
  error={errors.email?.message}  // Displays Hebrew error
/>
```

---

## Form Submission

### Submission Flow

```typescript
const onSubmit = async (data: LoginFormData) => {
  try {
    // 1. Call auth service via useAuth hook
    await login({ 
      email: data.email, 
      password: data.password 
    });
    
    // 2. Show success message
    showSuccess('התחברת בהצלחה!');
    
    // 3. Navigate to dashboard (handled by useAuth)
    
  } catch (error) {
    // 4. Show error message
    showError(error.message || 'שגיאה בהתחברות');
  }
};
```

### Loading States

During submission:
- ✅ Submit button shows spinner
- ✅ Submit button is disabled
- ✅ Form inputs remain enabled (for accessibility)
- ✅ Button text changes to "מתחבר..."

---

## Authentication Flow

### 1. User Enters Credentials
```
User fills email and password → React Hook Form validates
```

### 2. Form Submission
```
Submit button clicked → onSubmit called → Validation passes
```

### 3. API Call
```
useAuth.login() → auth.service.ts → POST /auth/login
```

### 4. Success Response
```
Token received → auth.store.ts updated → Auto-redirect to /dashboard
```

### 5. Error Response
```
Error thrown → Caught in catch block → Toast error displayed
```

---

## Password Visibility Toggle

### Implementation

```tsx
// State
const [showPassword, setShowPassword] = useState(false);

// Input type changes based on state
<Input
  type={showPassword ? 'text' : 'password'}
  {...otherProps}
/>

// Toggle button
<button 
  type="button"
  onClick={() => setShowPassword(!showPassword)}
>
  {showPassword ? <EyeOff /> : <Eye />}
</button>
```

### Accessibility
- Button has descriptive `aria-label`
- Type="button" prevents form submission
- Icons change to indicate current state

---

## Google OAuth Integration

### Current Implementation (Phase 1)

Google OAuth button is displayed but shows "coming soon" message:

```typescript
const handleGoogleLogin = () => {
  showError('התחברות עם Google תהיה זמינה בקרוב');
};
```

### Phase 2 Implementation Plan

```typescript
const handleGoogleLogin = async () => {
  try {
    // 1. Redirect to Google OAuth consent screen
    window.location.href = `${API_BASE_URL}/auth/google`;
    
    // 2. Google redirects back with authorization code
    // 3. Backend exchanges code for user info
    // 4. Backend creates/updates user and returns JWT
    // 5. Frontend stores token and redirects to dashboard
    
  } catch (error) {
    showError('שגיאה בהתחברות עם Google');
  }
};
```

---

## Remember Me Feature

### Current Implementation (Phase 1)

Checkbox is displayed but functionality is pending:

```tsx
<input
  {...register('rememberMe')}
  type="checkbox"
  // Value is captured but not used yet
/>
```

### Phase 2 Implementation Plan

```typescript
const onSubmit = async (data: LoginFormData) => {
  await login(
    { email: data.email, password: data.password },
    { rememberMe: data.rememberMe }  // Pass to auth service
  );
};

// In auth.service.ts
if (rememberMe) {
  // Request longer-lived refresh token (30 days vs 7 days)
  // Store preference in secure cookie
}
```

---

## Auto-Redirect Logic

### Preventing Access When Logged In

```typescript
useEffect(() => {
  if (isAuthenticated) {
    navigate('/dashboard');
  }
}, [isAuthenticated, navigate]);
```

**Why this is important:**
- Prevents logged-in users from seeing login page
- Improves UX (no need to manually navigate)
- Runs on component mount and when auth state changes

---

## Styling

### Layout

```css
Container:
  - min-h-screen (full viewport height)
  - bg-gray-50 (light gray background)
  - flex items-center justify-center (centered)
  - px-4 py-12 (padding for mobile)

Card:
  - max-w-[440px] (constrained width)
  - bg-white (white background)
  - rounded-2xl (16px border radius)
  - shadow-lg (elevation level 2)
  - p-10 (40px padding)
```

### Typography

```css
Page Title:
  - text-2xl (24px)
  - font-semibold (600 weight)
  - text-gray-900 (near black)
  - mb-2 (margin bottom)

Subtitle:
  - text-sm (14px)
  - text-gray-600 (medium gray)

Form Labels:
  - text-sm (14px)
  - font-medium (500 weight)
  - text-gray-700

Links:
  - text-blue-600 (primary blue)
  - hover:text-blue-700 (darker on hover)
  - font-medium (500 weight)
```

### Spacing

```css
Form Fields:
  - space-y-5 (20px gap between fields)

Submit Button:
  - mt-6 (24px margin top)

Divider:
  - my-6 (24px margin top/bottom)

Logo:
  - mb-8 (32px margin bottom)
```

---

## Responsive Behavior

### Desktop (> 1024px)
- Card centered with max-width 440px
- Full padding and spacing
- Hover effects on buttons and links

### Tablet (640px - 1024px)
- Card maintains 440px max-width
- Centered layout
- Same functionality as desktop

### Mobile (< 640px)
- Card full width with 16px horizontal margin
- Touch-optimized button sizes (48px height minimum)
- Same vertical spacing
- No hover effects (rely on active states)

---

## Accessibility Features

### Keyboard Navigation

**Tab Order:**
1. Email input
2. Password input
3. Password toggle button
4. Remember me checkbox
5. Forgot password link
6. Submit button
7. Google OAuth button
8. Signup link

**Keyboard Shortcuts:**
- `Tab`: Move to next element
- `Shift + Tab`: Move to previous element
- `Enter`: Submit form (when focused on inputs or buttons)
- `Space`: Toggle checkbox, activate buttons

### Screen Reader Support

**ARIA Attributes:**
```tsx
// Logo
<svg aria-label="Tik-Tax Logo">

// Password toggle
<button aria-label="הצג סיסמה">

// Form inputs
<input aria-invalid={!!errors.email} />
<input aria-describedby="email-error" />
```

**Semantic HTML:**
- `<form>` element for proper form context
- `<label>` elements for all inputs
- `<button>` elements (not div with onClick)
- Heading hierarchy (h1 for page title)

### Focus Indicators

All interactive elements have visible focus states:
```css
focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
```

---

## Error Handling

### Form Validation Errors

Displayed below field with red text and icon:

```tsx
<Input
  error="כתובת אימייל לא תקינה"
  // Renders:
  // <div class="text-red-600 text-sm flex items-center gap-1">
  //   <AlertCircle size={14} />
  //   כתובת אימייל לא תקינה
  // </div>
/>
```

### API Errors

Handled in try-catch block:

```typescript
try {
  await login({ email, password });
} catch (error) {
  // Error could be:
  // - "Invalid credentials"
  // - "Account locked"
  // - "Network error"
  // - etc.
  
  showError(error.message || 'שגיאה בהתחברות');
}
```

### Network Errors

Handled by axios interceptor in `auth.service.ts`:
- Connection timeout
- Server unavailable
- CORS errors
- etc.

---

## Testing

### Manual Testing

**Test Case 1: Valid Login**
1. Navigate to `/login`
2. Enter: `test@tiktax.co.il`
3. Enter: `password123`
4. Click "התחבר"
5. ✅ Should redirect to `/dashboard`

**Test Case 2: Invalid Email**
1. Enter: `invalid-email`
2. Tab to password field
3. ✅ Should show "כתובת אימייל לא תקינה"

**Test Case 3: Short Password**
1. Enter valid email
2. Enter: `123` (less than 8 chars)
3. Click submit
4. ✅ Should show "סיסמה חייבת להכיל לפחות 8 תווים"

**Test Case 4: Already Authenticated**
1. Login successfully
2. Navigate to `/login` manually
3. ✅ Should auto-redirect to `/dashboard`

### Accessibility Testing

**Keyboard Navigation:**
- [ ] Can navigate entire form with Tab key
- [ ] Enter key submits form
- [ ] Space bar toggles checkbox
- [ ] All focus indicators visible

**Screen Reader:**
- [ ] Form fields announced with labels
- [ ] Errors announced when displayed
- [ ] Button states announced (loading, disabled)
- [ ] Page title announced

---

## Common Issues & Solutions

### Issue 1: Form Not Submitting
**Symptoms:** Clicking submit does nothing
**Causes:**
- Validation errors present
- JavaScript errors in console
**Solution:**
- Check browser console for errors
- Verify form validation rules
- Ensure `handleSubmit` wrapper used

### Issue 2: Redirect Not Working
**Symptoms:** Login succeeds but stays on page
**Causes:**
- `navigate` function not imported
- Auth state not updating
**Solution:**
- Verify `useNavigate` hook used
- Check `auth.store.ts` state updates
- Ensure `useAuth` hook returns correct values

### Issue 3: Password Toggle Not Visible
**Symptoms:** Can't see eye icon
**Causes:**
- CSS positioning issue
- Icon not imported
**Solution:**
- Check Eye/EyeOff imports from lucide-react
- Verify CSS positioning styles
- Ensure button not hidden by z-index

### Issue 4: Error Messages in English
**Symptoms:** Validation errors show in English
**Causes:**
- Browser default validation triggered
- Forgot to override messages
**Solution:**
- Ensure custom error messages in Hebrew
- Use `noValidate` on form if needed
- Check validation rule definitions

---

## Performance Considerations

### Optimization Strategies

**1. Memoization:**
```typescript
// Not needed for this component (minimal re-renders)
// Form state managed by react-hook-form
```

**2. Lazy Loading:**
```typescript
// Can lazy load if part of larger route bundle
const LoginPage = lazy(() => import('@/pages/auth/LoginPage'));
```

**3. Code Splitting:**
```typescript
// Already split by route (React Router handles this)
```

**4. Asset Optimization:**
- SVG logo (minimal size)
- Icons from lucide-react (tree-shaken)
- No images or heavy assets

---

## Security Considerations

### Implemented Security

✅ **No Credential Storage:**
- Passwords not stored in state longer than needed
- No localStorage use for sensitive data

✅ **Auto-Complete Support:**
- Email field: `autocomplete="email"`
- Password field: `autocomplete="current-password"`
- Allows password managers to work

✅ **HTTPS Only:**
- Enforced by backend
- Credentials encrypted in transit

✅ **Input Validation:**
- Client-side validation for UX
- Server-side validation for security (in backend)

✅ **No Password Hints:**
- Password strength not shown (prevents info leak)

### Future Security Enhancements

🔄 **Rate Limiting** (Phase 2):
- Limit login attempts per IP
- Progressive delays after failures

🔄 **CAPTCHA** (Phase 2):
- Add reCAPTCHA after 3 failed attempts
- Prevent automated attacks

🔄 **Two-Factor Authentication** (Phase 3):
- SMS or authenticator app
- Required for sensitive operations

🔄 **Session Management** (Phase 3):
- Track active sessions
- Allow remote logout

---

## Maintenance

### Updating Error Messages

To change validation messages, edit the `register` calls:

```typescript
register('email', {
  required: 'NEW MESSAGE HERE',
  pattern: {
    value: /regex/,
    message: 'NEW MESSAGE HERE'
  }
})
```

### Adding New Fields

1. Update `LoginFormData` interface
2. Add field to form with `register()`
3. Add validation rules
4. Update API call if needed

Example - Adding "Language Preference":
```typescript
interface LoginFormData {
  email: string;
  password: string;
  rememberMe: boolean;
  language: 'he' | 'en';  // New field
}

// In form
<select {...register('language')}>
  <option value="he">עברית</option>
  <option value="en">English</option>
</select>
```

### Changing Styling

Component uses Tailwind CSS. To modify:

**Change card width:**
```tsx
// From:
<div className="w-full max-w-[440px]">

// To:
<div className="w-full max-w-[500px]">
```

**Change background color:**
```tsx
// From:
<div className="min-h-screen bg-gray-50">

// To:
<div className="min-h-screen bg-blue-50">
```

---

## Related Documentation

- [Button Component](../../components/ui/Button.README.md)
- [Input Component](../../components/ui/Input.README.md)
- [useAuth Hook](../../hooks/useAuth.ts)
- [Auth Service](../../services/AUTH_SERVICE.md)
- [Auth Store](../../stores/AUTH_STORE.IMPLEMENTATION.md)

---

## Support

For issues or questions:
1. Check this README and QUICKREF.md
2. Review component source code
3. Check browser console for errors
4. Verify backend is running and accessible

---

**Component Version:** 1.0.0  
**Last Updated:** November 2, 2025  
**Status:** ✅ Production Ready (Phase 1)  
**Maintainer:** Tik-Tax Development Team
