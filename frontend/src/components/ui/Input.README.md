# Input Component

A professional, accessible, and feature-rich input component for the Tik-Tax application. Fully compliant with the Tik-Tax design system and WCAG 2.1 AA accessibility standards.

## Features

✅ **Multiple Input Types** - text, email, password, tel, number, date, url  
✅ **Validation States** - default, error, success, disabled  
✅ **Password Toggle** - Show/hide password with eye icon  
✅ **Icon Support** - Left or right icon placement  
✅ **Character Counter** - Automatic counter when maxLength is set  
✅ **Helper Text** - Additional context below input  
✅ **Error Messages** - Clear error display with icons  
✅ **RTL Support** - Full right-to-left layout for Hebrew  
✅ **Accessibility** - WCAG 2.1 AA compliant with ARIA attributes  
✅ **TypeScript** - Full type safety with proper interfaces  
✅ **Responsive** - Mobile-first design  

---

## Installation

The component is already available in the project. Simply import it:

```tsx
import { Input } from '@/components/ui';
// or
import Input from '@/components/ui/Input';
```

---

## Basic Usage

```tsx
import { Input } from '@/components/ui';

function MyForm() {
  return (
    <Input 
      label="שם מלא" 
      placeholder="הזן שם מלא"
      type="text"
      required
    />
  );
}
```

---

## Props API

### InputProps Interface

```typescript
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  /** Label text displayed above the input */
  label?: string;
  
  /** Error message to display (triggers error state) */
  error?: string;
  
  /** Helper text displayed below the input */
  helperText?: string;
  
  /** Icon element to display inside input */
  icon?: React.ReactNode;
  
  /** Position of the icon */
  iconPosition?: 'left' | 'right';
  
  /** Required field indicator (shows red asterisk) */
  required?: boolean;
  
  /** Makes input full width */
  fullWidth?: boolean;
  
  /** Success state (shows green border and checkmark) */
  success?: boolean;
}
```

### Inherited Props

The component extends `React.InputHTMLAttributes<HTMLInputElement>`, so all standard HTML input props are available:

- `type` - Input type (text, email, password, etc.)
- `value` - Controlled value
- `defaultValue` - Uncontrolled default value
- `onChange` - Change handler
- `onBlur` - Blur handler
- `onFocus` - Focus handler
- `placeholder` - Placeholder text
- `disabled` - Disabled state
- `maxLength` - Maximum character length
- `minLength` - Minimum character length
- `pattern` - Validation pattern
- `autoFocus` - Auto-focus on mount
- `autoComplete` - Autocomplete behavior
- And all other standard input attributes...

---

## Examples

### 1. Basic Text Input

```tsx
<Input 
  label="שם מלא" 
  placeholder="הזן שם מלא"
  type="text"
/>
```

### 2. Required Field

```tsx
<Input 
  label="דוא״ל" 
  placeholder="example@tiktax.co.il"
  type="email"
  required
/>
```

### 3. With Helper Text

```tsx
<Input 
  label="סיסמה" 
  type="password"
  helperText="לפחות 8 תווים, אותיות ומספרים"
  required
/>
```

### 4. Error State

```tsx
<Input 
  label="דוא״ל" 
  type="email"
  value={email}
  error="כתובת דוא״ל לא תקינה"
/>
```

### 5. Success State

```tsx
<Input 
  label="דוא״ל" 
  type="email"
  value="user@example.com"
  success
/>
```

### 6. With Icon

```tsx
import { Mail } from 'lucide-react';

<Input 
  label="דוא״ל" 
  type="email"
  icon={<Mail size={20} />}
  iconPosition="right"
/>
```

### 7. Password Input (Auto Toggle)

```tsx
<Input 
  label="סיסמה" 
  type="password"
  placeholder="הזן סיסמה"
/>
// Password inputs automatically get show/hide toggle
```

### 8. Character Counter

```tsx
const [description, setDescription] = useState('');

<Input 
  label="תיאור" 
  maxLength={100}
  value={description}
  onChange={(e) => setDescription(e.target.value)}
/>
// Automatically shows character counter: 0/100
```

### 9. Full Width

```tsx
<Input 
  label="כתובת מלאה" 
  fullWidth
/>
```

### 10. Disabled State

```tsx
<Input 
  label="ערך קבוע" 
  value="לא ניתן לערוך"
  disabled
/>
```

---

## Form Integration

### React Hook Form

```tsx
import { useForm } from 'react-hook-form';
import { Input } from '@/components/ui';

function SignupForm() {
  const { register, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = (data) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Input
        label="שם מלא"
        {...register('fullName', { 
          required: 'שדה חובה',
          minLength: { value: 2, message: 'שם קצר מדי' }
        })}
        error={errors.fullName?.message}
        required
      />

      <Input
        label="דוא״ל"
        type="email"
        {...register('email', { 
          required: 'שדה חובה',
          pattern: {
            value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
            message: 'כתובת דוא״ל לא תקינה'
          }
        })}
        error={errors.email?.message}
        required
      />

      <Input
        label="סיסמה"
        type="password"
        {...register('password', { 
          required: 'שדה חובה',
          minLength: { value: 8, message: 'לפחות 8 תווים' }
        })}
        error={errors.password?.message}
        helperText="לפחות 8 תווים"
        required
      />

      <button type="submit">הרשם</button>
    </form>
  );
}
```

### Controlled Component

```tsx
import { useState } from 'react';
import { Input } from '@/components/ui';

function LoginForm() {
  const [email, setEmail] = useState('');
  const [emailError, setEmailError] = useState('');

  const validateEmail = (value: string) => {
    if (!value.includes('@')) {
      setEmailError('כתובת דוא״ל לא תקינה');
    } else {
      setEmailError('');
    }
  };

  return (
    <Input
      label="דוא״ל"
      type="email"
      value={email}
      onChange={(e) => {
        setEmail(e.target.value);
        validateEmail(e.target.value);
      }}
      error={emailError}
      required
    />
  );
}
```

### Uncontrolled with Ref

```tsx
import { useRef } from 'react';
import { Input } from '@/components/ui';

function SearchForm() {
  const searchRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const searchValue = searchRef.current?.value;
    console.log('Search:', searchValue);
  };

  return (
    <form onSubmit={handleSubmit}>
      <Input
        label="חיפוש"
        ref={searchRef}
        placeholder="חפש קבלות..."
      />
      <button type="submit">חפש</button>
    </form>
  );
}
```

---

## Visual States

### Default State
- **Border:** 1.5px solid #D1D5DB (gray-300)
- **Background:** #FFFFFF (white)
- **Text:** #111827 (gray-900)
- **Padding:** 12px 16px
- **Border Radius:** 8px
- **Font Size:** 16px

### Focus State
- **Border:** #2563EB (blue-600)
- **Shadow:** 0 0 0 3px rgba(37, 99, 235, 0.1)
- **Outline:** none

### Error State
- **Border:** #EF4444 (red-500)
- **Shadow:** 0 0 0 3px rgba(239, 68, 68, 0.1)
- **Icon:** AlertCircle (red)
- **Message:** #DC2626 (red-600)

### Success State
- **Border:** #10B981 (green-500)
- **Shadow:** 0 0 0 3px rgba(16, 185, 129, 0.1)
- **Icon:** CheckCircle (green)

### Disabled State
- **Background:** #F9FAFB (gray-50)
- **Border:** #E5E7EB (gray-200)
- **Text:** #9CA3AF (gray-400)
- **Cursor:** not-allowed

---

## Accessibility

The Input component is fully accessible and follows WCAG 2.1 AA guidelines:

### Features

✅ **Label Association** - Proper `<label htmlFor={id}>` connection  
✅ **ARIA Attributes** - `aria-invalid`, `aria-describedby`, `aria-label`  
✅ **Error Announcements** - Errors have `role="alert"` for screen readers  
✅ **Keyboard Navigation** - Full keyboard support (Tab, Enter, Escape)  
✅ **Focus Indicators** - Visible focus ring on all states  
✅ **Required Indicator** - Red asterisk with `aria-label="required"`  
✅ **Password Toggle** - Descriptive aria-label for show/hide  
✅ **Semantic HTML** - Proper element structure  

### Screen Reader Support

```tsx
// Error state announcement
<Input 
  label="דוא״ל"
  error="כתובת דוא״ל לא תקינה"
/>
// Screen reader: "דוא״ל, required, invalid data, כתובת דוא״ל לא תקינה"

// Password toggle
<Input type="password" label="סיסמה" />
// Screen reader: "הצג סיסמה" / "הסתר סיסמה"
```

### Keyboard Shortcuts

- **Tab** - Navigate to input
- **Shift + Tab** - Navigate to previous input
- **Enter** - Submit form (if in form)
- **Escape** - Clear input (native browser behavior)
- **Space** - Toggle password visibility (when focused on toggle)

---

## RTL Support

The Input component fully supports right-to-left (RTL) layout for Hebrew:

```tsx
// Icons automatically position correctly
<Input 
  label="דוא״ל"
  icon={<Mail size={20} />}
  iconPosition="right" // Right in RTL = visual right side
/>

// Text alignment is automatic
<Input 
  label="שם"
  placeholder="הזן שם" // RTL aligned automatically
/>
```

### RTL Features

✅ Text direction: RTL  
✅ Icon positioning: Adapts to RTL  
✅ Padding: Adjusts based on icon position  
✅ Character counter: Positioned correctly  
✅ Error messages: Right-aligned  
✅ Helper text: Right-aligned  

---

## Password Input Special Features

Password inputs automatically get special treatment:

1. **Show/Hide Toggle** - Eye icon appears automatically
2. **Toggle Button** - Click to reveal/hide password
3. **Accessible** - Proper aria-labels in Hebrew
4. **Positioned Correctly** - Always on the right in RTL

```tsx
<Input 
  type="password"
  label="סיסמה"
/>
// Automatically gets:
// - Eye icon toggle
// - Proper aria-label
// - Secure input masking
```

---

## Character Counter

When `maxLength` is provided with a controlled value, a character counter appears automatically:

```tsx
const [text, setText] = useState('');

<Input 
  label="תיאור"
  maxLength={100}
  value={text}
  onChange={(e) => setText(e.target.value)}
/>
// Shows: "0/100" → "50/100" → "100/100"
// Turns red when exceeding limit
```

---

## Styling & Customization

### Custom Classes

```tsx
// Add custom Tailwind classes
<Input 
  label="Custom"
  className="border-purple-500 focus:border-purple-700"
/>
```

### Using cn() Utility

```tsx
import { cn } from '@/utils/formatters';

<Input 
  label="Conditional"
  className={cn(
    'custom-base-class',
    isPremium && 'border-gold',
    hasError && 'border-red-500'
  )}
/>
```

---

## Best Practices

### ✅ DO

- **Always provide a label** for accessibility
- **Use appropriate input types** (email, tel, password, etc.)
- **Show clear error messages** in Hebrew
- **Use helper text** for additional context
- **Mark required fields** explicitly with `required` prop
- **Validate on blur** for better UX
- **Show success states** after successful validation
- **Use meaningful icons** that add context

### ❌ DON'T

- Don't omit labels (accessibility violation)
- Don't use generic error messages ("שגיאה")
- Don't use password type without helper text about requirements
- Don't forget RTL considerations
- Don't use decorative icons without meaning
- Don't validate on every keystroke (use debounce)

---

## Common Patterns

### Email Validation

```tsx
const [email, setEmail] = useState('');
const [error, setError] = useState('');

const validateEmail = (value: string) => {
  const emailRegex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
  if (!emailRegex.test(value)) {
    setError('כתובת דוא״ל לא תקינה');
  } else {
    setError('');
  }
};

<Input
  type="email"
  label="דוא״ל"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  onBlur={(e) => validateEmail(e.target.value)}
  error={error}
/>
```

### Phone Number with Formatting

```tsx
import { Phone } from 'lucide-react';

const formatPhone = (value: string) => {
  const cleaned = value.replace(/\D/g, '');
  const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
  if (match) {
    return `${match[1]}-${match[2]}-${match[3]}`;
  }
  return value;
};

<Input
  type="tel"
  label="טלפון נייד"
  icon={<Phone size={20} />}
  onChange={(e) => {
    const formatted = formatPhone(e.target.value);
    setPhone(formatted);
  }}
/>
```

### Real-time Character Counter

```tsx
const [bio, setBio] = useState('');
const maxLength = 200;

<Input
  label="ביוגרפיה"
  placeholder="ספר לנו עליך..."
  maxLength={maxLength}
  value={bio}
  onChange={(e) => setBio(e.target.value)}
  helperText={`${maxLength - bio.length} תווים נותרו`}
/>
```

---

## Performance Optimization

### Debounced Validation

```tsx
import { useState, useCallback } from 'react';
import { debounce } from 'lodash';

const [searchTerm, setSearchTerm] = useState('');

const debouncedSearch = useCallback(
  debounce((value: string) => {
    // Perform search/validation
    console.log('Searching for:', value);
  }, 300),
  []
);

<Input
  label="חיפוש"
  value={searchTerm}
  onChange={(e) => {
    setSearchTerm(e.target.value);
    debouncedSearch(e.target.value);
  }}
/>
```

### Memoization

```tsx
import { memo } from 'react';

const MemoizedInput = memo(Input);

// Use in forms with many inputs to prevent unnecessary re-renders
<MemoizedInput label="שם" />
```

---

## Testing

### Unit Tests

```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import Input from './Input';

describe('Input Component', () => {
  test('renders label correctly', () => {
    render(<Input label="שם מלא" />);
    expect(screen.getByText('שם מלא')).toBeInTheDocument();
  });

  test('shows error message', () => {
    render(<Input label="Email" error="Invalid email" />);
    expect(screen.getByRole('alert')).toHaveTextContent('Invalid email');
  });

  test('toggles password visibility', () => {
    render(<Input type="password" label="Password" />);
    const input = screen.getByLabelText('Password');
    const toggle = screen.getByLabelText('הצג סיסמה');
    
    expect(input).toHaveAttribute('type', 'password');
    fireEvent.click(toggle);
    expect(input).toHaveAttribute('type', 'text');
  });

  test('shows character counter', () => {
    render(<Input label="Bio" maxLength={100} value="Hello" />);
    expect(screen.getByText('5/100')).toBeInTheDocument();
  });
});
```

---

## Troubleshooting

### Issue: Label not clickable
**Solution:** Ensure `id` prop is set or let component auto-generate one.

### Issue: Icons not showing
**Solution:** Import icons from `lucide-react` and pass as JSX elements.

### Issue: Character counter not appearing
**Solution:** Ensure both `maxLength` AND `value` props are provided (controlled component).

### Issue: Password toggle not working
**Solution:** It should work automatically. Check if custom `type` is overriding it.

### Issue: RTL not working
**Solution:** Ensure parent has `dir="rtl"` attribute.

---

## Related Components

- **Button** - Primary action component
- **Select** - Dropdown selection (future)
- **Textarea** - Multi-line text input (future)
- **DatePicker** - Date selection (future)

---

## Changelog

### v1.0.0 (2025-11-02)
- Initial release
- Support for all basic input types
- Validation states (error, success)
- Password toggle
- Character counter
- Icon support
- RTL layout
- Full accessibility

---

## License

Part of the Tik-Tax application. Internal use only.

---

## Support

For questions or issues, contact the development team or refer to:
- Component Demo: `Input.demo.tsx`
- Quick Reference: `Input.QUICKREF.md`
- Design System: `.github/instructions/design_rules_.instructions.md`
