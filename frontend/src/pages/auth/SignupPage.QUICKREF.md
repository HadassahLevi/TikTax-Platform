# SignupPage Component - Quick Reference

## Import
```typescript
import { SignupPage } from '@/pages/auth';
// or
import SignupPage from '@/pages/auth/SignupPage';
```

## Usage
```tsx
<Route path="/signup" element={<SignupPage />} />
```

## Features
✅ 3-step wizard with progress indicator
✅ Step 1: Personal information (name, ID, email, password, phone)
✅ Step 2: Business information (name, number, type)
✅ Step 3: SMS verification with 6-digit OTP
✅ Full form validation with react-hook-form
✅ Password strength indicator
✅ Israeli ID number checksum validation
✅ Phone number auto-formatting
✅ Data persistence between steps
✅ Countdown timer for SMS resend (60 seconds)
✅ Mobile-optimized design
✅ RTL support for Hebrew

## Step Breakdown

### Step 1: Personal Information
**Fields:**
- Full Name (שם מלא) - Min 2 words, Hebrew/English
- ID Number (תעודת זהות) - 9 digits with checksum
- Email (אימייל) - Valid email format
- Password (סיסמה) - Min 8 chars, uppercase, lowercase, number
- Confirm Password (אימות סיסמה) - Must match password
- Phone (טלפון) - Israeli format (10 digits, starts with 05)

**Validation:**
- Real-time password strength indicator
- Israeli ID checksum validation
- Phone number formatting on blur

### Step 2: Business Information
**Fields:**
- Business Name (שם העסק) - Min 2 characters
- Business Number (מספר עוסק / ח.פ) - 9 digits
- Business Type (סוג עסק) - Radio buttons:
  * עוסק מורשה (Licensed Dealer)
  * עוסק פטור (Exempt Dealer)
  * חברה בע"מ (Limited Company)

**Navigation:**
- Back button preserves Step 1 data
- Next button sends SMS verification code

### Step 3: SMS Verification
**Features:**
- 6-digit OTP input (auto-focus, auto-advance)
- Phone number masking for privacy (050-XXX-4567)
- Auto-submit when all 6 digits entered
- Countdown timer (60 seconds)
- Resend code button (enabled after countdown)
- Clear all button
- Back button returns to Step 2

## Form Data Structure
```typescript
interface SignupFormData {
  // Step 1
  fullName: string;
  idNumber: string;
  email: string;
  password: string;
  confirmPassword: string;
  phone: string;
  
  // Step 2
  businessName: string;
  businessNumber: string;
  businessType: 'licensed_dealer' | 'exempt_dealer' | 'limited_company';
  
  // Step 3
  verificationCode: string;
}
```

## Validation Rules

### Full Name
- Required
- Minimum 2 words
- Hebrew or English letters only
- Error: "יש להזין שם פרטי ושם משפחה"

### ID Number
- Required
- Exactly 9 digits
- Israeli ID checksum validation
- Error: "מספר תעודת זהות לא תקין"

### Email
- Required
- Valid email format
- Error: "כתובת אימייל לא תקינה"

### Password
- Required
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- Shows strength indicator (weak/medium/strong)

### Confirm Password
- Required
- Must match password
- Error: "הסיסמאות אינן תואמות"

### Phone
- Required
- Exactly 10 digits
- Must start with "05"
- Auto-formats to 050-XXX-XXXX
- Error: "מספר טלפון חייב להכיל 10 ספרות"

### Business Name
- Required
- Minimum 2 characters

### Business Number
- Required
- Exactly 9 digits

### Business Type
- Required
- One option must be selected

## API Integration

### SMS Verification Flow
```typescript
// Step 2 → Step 3 transition
await sendSMSVerification(phone);

// Step 3: Verify code
await verifySMSCode(phone, code);

// Final submission
await signup(signupData);
```

### Error Handling
- Field validation errors show below inputs
- API errors show in toast notifications
- Invalid OTP keeps input focused for retry
- Network errors handled gracefully

## State Management
```typescript
const [currentStep, setCurrentStep] = useState(1);
const [formData, setFormData] = useState<Partial<SignupFormData>>({});
const [showPassword, setShowPassword] = useState(false);
const [showConfirmPassword, setShowConfirmPassword] = useState(false);
```

## Dependencies
- `react-hook-form` - Form validation
- `react-otp-input` - SMS code input
- `lucide-react` - Icons
- `@/components/ui/Button` - Primary button
- `@/components/ui/Input` - Input fields
- `@/components/ui/Card` - Container card
- `@/components/auth/ProgressIndicator` - Step progress
- `@/components/auth/PasswordStrength` - Password validation
- `@/components/auth/SMSVerification` - OTP input

## Helper Functions

### Israeli ID Validation
```typescript
const validateIsraeliID = (id: string): boolean => {
  if (!/^\d{9}$/.test(id)) return false;
  
  const digits = id.split('').map(Number);
  const sum = digits.reduce((acc, digit, index) => {
    let value = digit * ((index % 2) + 1);
    if (value > 9) value -= 9;
    return acc + value;
  }, 0);
  
  return sum % 10 === 0;
};
```

### Phone Formatting
```typescript
const formatPhone = (phone: string): string => {
  const cleaned = phone.replace(/\D/g, '');
  if (cleaned.length === 10) {
    return `${cleaned.slice(0, 3)}-${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
  }
  return phone;
};
```

## Styling
- Card: white background, rounded corners, shadow
- Progress indicator: 3 steps with colored circles
- Inputs: full width, error states, icons
- Buttons: full width (Step 1, 3), side-by-side (Step 2)
- Mobile: optimized touch targets, responsive layout

## Accessibility
- Proper label associations
- ARIA attributes
- Keyboard navigation support
- Focus management
- Error announcements
- Required field indicators

## Mobile Optimization
- Numeric keyboard for phone/ID inputs
- Touch-friendly button sizes (48px height)
- Auto-focus on first field
- Auto-advance in OTP input
- Responsive card width

## Success Flow
1. User completes Step 1 → saves data, moves to Step 2
2. User completes Step 2 → sends SMS, moves to Step 3
3. User enters valid OTP → verifies phone
4. System completes signup → redirects to dashboard (via useAuth)

## Error Scenarios
- Invalid ID checksum → "מספר תעודת זהות לא תקין"
- Passwords don't match → "הסיסמאות אינן תואמות"
- SMS send fails → Toast error, stays on Step 2
- Invalid OTP → "קוד שגוי. נסה שוב.", keeps input open
- Signup fails → Toast error with message

## Tips
- Back navigation preserves all entered data
- OTP auto-submits when complete
- Countdown timer prevents SMS spam
- Phone number masked in Step 3 for privacy
- Password strength updates in real-time
