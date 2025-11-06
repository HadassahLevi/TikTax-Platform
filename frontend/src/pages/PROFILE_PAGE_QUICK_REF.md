# ProfilePage - Quick Reference

## 🚀 Quick Start

```tsx
import { ProfilePage } from '@/pages/ProfilePage';

// In router
<Route path="/profile" element={<ProfilePage />} />
```

---

## 📋 Features at a Glance

### Profile Tab (Personal & Business Info)
- **Editable:** Full name, phone, business name, business number
- **Read-only:** Email address
- **Validation:** Real-time with Hebrew error messages

### Security Tab
- **Password Change:** Modal with strength requirements
- **Verification Status:** Phone and email badges
- **Sessions:** View current session and logout

### Subscription Tab
- **Current Plan:** Visual card with pricing
- **Usage Tracking:** Progress bar (green → orange → red)
- **Features List:** Dynamic based on plan
- **Billing:** Placeholder for future integration

### Danger Zone
- **Delete Account:** Two-step confirmation
- **Warning:** Lists all data that will be deleted
- **Permanent:** Cannot be undone

---

## 🎨 Visual Reference

### Tab States
```tsx
// Active tab
className="bg-white text-primary-600 border-b-2 border-primary-600"

// Inactive tab
className="text-gray-600 hover:text-gray-900 hover:bg-gray-100"
```

### Usage Bar Colors
```tsx
usagePercentage >= 100 ? 'bg-red-500' :     // Limit reached
usagePercentage >= 80  ? 'bg-warning-500' : // Warning
'bg-primary-600'                             // Normal
```

### Plan Badges
```tsx
free:     'bg-gray-100 text-gray-900'
basic:    'bg-blue-100 text-blue-900'
pro:      'bg-purple-100 text-purple-900'
business: 'bg-gold-100 text-gold-900'
```

---

## 🔌 useAuth Hook - New Methods

```tsx
const {
  updateProfile,    // Update user profile
  changePassword,   // Change password
  deleteAccount     // Delete account
} = useAuth();
```

### updateProfile()
```tsx
await updateProfile({
  fullName: 'David Cohen',
  phone: '0501234567',
  businessName: 'Cohen Design',
  businessNumber: '123456789'
});
```

### changePassword()
```tsx
await changePassword(
  'currentPassword123',  // Current password
  'NewSecurePass456'     // New password
);
```

### deleteAccount()
```tsx
await deleteAccount(); // Permanently deletes account
```

---

## ✅ Validation Rules

### Phone Number
```regex
/^(05\d{8}|05\d-\d{7})$/
```
Examples:
- ✅ `0501234567`
- ✅ `050-1234567`
- ❌ `+972501234567`
- ❌ `02-1234567`

### Business Number
```regex
/^\d{8,9}$/
```
Examples:
- ✅ `12345678`
- ✅ `123456789`
- ❌ `1234567` (too short)
- ❌ `12-345-678` (has dashes)

### Password Strength
```regex
/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/
```
Requirements:
- ✅ Minimum 8 characters
- ✅ At least one uppercase letter
- ✅ At least one lowercase letter
- ✅ At least one number
- ✅ At least one special character `@$!%*?&`

Examples:
- ✅ `SecurePass123!`
- ✅ `MyP@ssw0rd`
- ❌ `password` (no uppercase, number, special)
- ❌ `Pass1!` (too short)

---

## 🌐 API Endpoints

### Update Profile
```http
PUT /api/auth/profile
Authorization: Bearer {token}

Body: {
  "fullName": "string",
  "phone": "string",
  "businessName": "string",
  "businessNumber": "string"
}

Response: { "user": {...} }
```

### Change Password
```http
PUT /api/auth/change-password
Authorization: Bearer {token}

Body: {
  "currentPassword": "string",
  "newPassword": "string",
  "confirmPassword": "string"
}

Response: { "message": "Password changed successfully" }
```

### Delete Account
```http
DELETE /api/auth/account
Authorization: Bearer {token}

Response: { "message": "Account deleted successfully" }
```

---

## 🎯 Common Use Cases

### Navigate to Profile Page
```tsx
import { useNavigate } from 'react-router-dom';

function Header() {
  const navigate = useNavigate();
  
  return (
    <button onClick={() => navigate('/profile')}>
      <User size={20} />
      הגדרות
    </button>
  );
}
```

### Pre-select a Tab
```tsx
// Navigate with state
navigate('/profile', { state: { tab: 'security' } });

// In ProfilePage, read from location state
const { state } = useLocation();
const [activeTab, setActiveTab] = useState(state?.tab || 'profile');
```

### Check if User Can Edit
```tsx
const { user } = useAuth();

// Email is always read-only
<Input disabled value={user?.email} />

// Other fields editable
<Input {...form.register('fullName')} />
```

---

## 🐛 Error Handling

### Form Validation Errors
```tsx
// Automatic from react-hook-form
{errors.fullName && (
  <span className="text-error-600 text-sm">
    {errors.fullName.message}
  </span>
)}
```

### API Errors
```tsx
try {
  await updateProfile(data);
  showSuccess('הפרטים עודכנו בהצלחה');
} catch (error) {
  showError(error.message); // Hebrew error from API
}
```

### Password Mismatch
```tsx
if (newPassword !== confirmPassword) {
  showError('הסיסמאות אינן תואמות');
  return;
}
```

---

## 🎨 Styling Classes

### Form Section
```tsx
<div className="space-y-6">
  <h3 className="text-lg font-semibold text-gray-900 mb-4">
    {title}
  </h3>
  <div className="space-y-4">
    {/* Form fields */}
  </div>
</div>
```

### Info Card (Security Tab)
```tsx
<div className="bg-gray-50 rounded-lg p-4 flex items-center justify-between">
  <div className="flex items-start gap-3">
    <Icon className="text-gray-600 mt-0.5" size={20} />
    <div>
      <h4 className="font-medium text-gray-900">{title}</h4>
      <p className="text-sm text-gray-600 mt-1">{description}</p>
    </div>
  </div>
  <Button variant="secondary" size="sm">{action}</Button>
</div>
```

### Verification Badge
```tsx
{/* Verified */}
<span className="inline-flex items-center gap-1 text-sm text-success-600">
  <CheckCircle size={16} />
  מאומת
</span>

{/* Not Verified */}
<span className="text-sm text-warning-600">
  לא מאומת
</span>
```

---

## 📱 Responsive Breakpoints

```tsx
// Mobile (< 640px)
<div className="grid grid-cols-1 gap-4">

// Tablet+ (>= 640px)
<div className="grid md:grid-cols-2 gap-4">

// Desktop only
<div className="hidden lg:block">
```

---

## ♿ Accessibility

### Tab Navigation
```tsx
<button
  role="tab"
  aria-selected={active}
  className={/* ... */}
>
  {/* Tab content */}
</button>
```

### Modal
```tsx
<Modal
  isOpen={showModal}
  onClose={() => setShowModal(false)}
  title="Modal Title"
  closeOnEsc={true}
  closeOnOverlayClick={true}
>
  {/* Modal content */}
</Modal>
```

### Form Labels
```tsx
<Input
  label="שם מלא"
  required
  error={errors.fullName?.message}
  {...register('fullName')}
/>
```

---

## 🔐 Security Best Practices

### Password Validation
```tsx
// Client-side validation
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/;
if (!passwordRegex.test(newPassword)) {
  showError('הסיסמה חייבת להכיל אות גדולה, קטנה, מספר ותו מיוחד');
  return;
}

// Also validated on server
```

### Account Deletion Confirmation
```tsx
// Two-step process
1. Click "Delete Account" button
2. Confirm in modal with detailed warning

// Modal shows:
- Warning icon
- "Action cannot be undone" message
- List of data to be deleted
- Cancel and Confirm buttons
```

### Session Management
```tsx
// Show current session
<div className="bg-gray-50 rounded-lg p-4">
  <Shield className="text-primary-600" size={20} />
  <h4>מכשיר נוכחי</h4>
  <p>התחברת לאחרונה: היום בשעה 14:30</p>
  <Button onClick={logout}>התנתק</Button>
</div>
```

---

## 🧪 Testing Checklist

### Manual Tests

**Profile Tab:**
```bash
✓ Fill form with valid data → Success
✓ Leave required field empty → Validation error
✓ Invalid phone format → Format error
✓ Invalid business number → Validation error
✓ Try to edit email → Field is disabled
```

**Security Tab:**
```bash
✓ Open password modal → Modal appears
✓ Submit weak password → Strength error
✓ Passwords don't match → Mismatch error
✓ Valid password → Success and modal closes
✓ Click logout → Redirects to login
```

**Subscription Tab:**
```bash
✓ Check plan display → Correct plan and price
✓ Check usage bar → Correct percentage
✓ At 80% usage → Orange warning
✓ At 100% usage → Red with message
```

**Account Deletion:**
```bash
✓ Open delete modal → Warning displayed
✓ Cancel → Modal closes, no action
✓ Confirm → Account deleted, redirect
```

---

## 💡 Tips & Tricks

### Pre-fill Form from User Data
```tsx
const profileForm = useForm({
  defaultValues: {
    fullName: user?.fullName || '',
    businessName: user?.businessName || '',
    // ...
  }
});
```

### Reset Form After Modal Close
```tsx
<Modal
  onClose={() => {
    setShowModal(false);
    form.reset(); // Clear form data
  }}
>
```

### Show Loading State
```tsx
const [loading, setLoading] = useState(false);

const handleSubmit = async (data) => {
  setLoading(true);
  try {
    await updateProfile(data);
  } finally {
    setLoading(false); // Always reset
  }
};

<Button loading={loading} disabled={loading}>
  {loading ? 'שומר...' : 'שמור'}
</Button>
```

### Conditional Rendering
```tsx
{user?.phoneVerified ? (
  <span className="text-success-600">מאומת</span>
) : (
  <Button size="sm">אמת עכשיו</Button>
)}
```

---

## 📚 Related Components

- `Button` - `/src/components/ui/Button.tsx`
- `Input` - `/src/components/ui/Input.tsx`
- `Modal` - `/src/components/ui/Modal.tsx`
- `PageContainer` - `/src/components/layout/PageContainer.tsx`
- `useAuth` - `/src/hooks/useAuth.ts`
- `useToast` - `/src/hooks/useToast.ts`

---

## 🔗 External Dependencies

```json
{
  "react-hook-form": "^7.49.0",
  "framer-motion": "^10.16.0",
  "lucide-react": "^0.294.0",
  "zustand": "^4.4.0",
  "react-router-dom": "^6.20.0"
}
```

---

**Last Updated:** November 6, 2025  
**Version:** 1.0.0  
**Status:** Production Ready ✅
