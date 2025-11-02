# Input Component - Quick Reference

## Import
```tsx
import { Input } from '@/components/ui';
// or
import Input from '@/components/ui/Input';
```

## Basic Usage
```tsx
<Input label="שם מלא" placeholder="הזן שם" />
```

## Props Quick Reference

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `string` | - | Label text above input |
| `error` | `string` | - | Error message (triggers error state) |
| `helperText` | `string` | - | Helper text below input |
| `icon` | `ReactNode` | - | Icon inside input |
| `iconPosition` | `'left' \| 'right'` | `'right'` | Icon position |
| `required` | `boolean` | `false` | Shows red asterisk |
| `fullWidth` | `boolean` | `false` | Makes input full width |
| `success` | `boolean` | `false` | Shows success state |
| `type` | `string` | `'text'` | Input type (text, email, password, etc.) |
| `disabled` | `boolean` | `false` | Disables input |
| `maxLength` | `number` | - | Character limit (shows counter) |

**Plus all standard HTML input attributes** (`placeholder`, `value`, `onChange`, `onBlur`, etc.)

## Common Patterns

### 1. Required Text Input
```tsx
<Input 
  label="שם מלא" 
  placeholder="הזן שם מלא"
  required
/>
```

### 2. Email with Validation
```tsx
<Input 
  type="email"
  label="דוא״ל"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  error={emailError ? "כתובת דוא״ל לא תקינה" : undefined}
/>
```

### 3. Password Input
```tsx
<Input 
  type="password"
  label="סיסמה"
  placeholder="לפחות 8 תווים"
  helperText="השתמש באותיות, מספרים ותווים מיוחדים"
  required
/>
```

### 4. With Icon
```tsx
import { Mail } from 'lucide-react';

<Input 
  type="email"
  label="דוא״ל"
  icon={<Mail size={20} />}
  iconPosition="right"
/>
```

### 5. Success State
```tsx
<Input 
  type="email"
  label="דוא״ל"
  value="user@example.com"
  success
/>
```

### 6. With Character Counter
```tsx
<Input 
  label="תיאור"
  placeholder="תיאור קצר"
  maxLength={100}
  value={description}
  onChange={(e) => setDescription(e.target.value)}
/>
```

### 7. Phone Number
```tsx
import { Phone } from 'lucide-react';

<Input 
  type="tel"
  label="טלפון נייד"
  placeholder="050-1234567"
  icon={<Phone size={20} />}
  iconPosition="right"
/>
```

### 8. Disabled State
```tsx
<Input 
  label="ערך קבוע"
  value="לא ניתן לערוך"
  disabled
/>
```

## Input Types Supported
- `text` - Default text input
- `email` - Email input
- `password` - Password (with show/hide toggle)
- `tel` - Phone number
- `number` - Numeric input
- `date` - Date picker
- `url` - URL input
- All other standard HTML5 input types

## Visual States

### Default
- Border: 1.5px solid #D1D5DB (gray-300)
- Background: white
- Focus: Blue border with glow

### Error
- Border: #EF4444 (red-500)
- Error icon: AlertCircle
- Error message below
- Red glow on focus

### Success
- Border: #10B981 (green-500)
- Success icon: CheckCircle
- Green glow on focus

### Disabled
- Background: #F9FAFB (gray-50)
- Border: #E5E7EB (gray-200)
- Text: #9CA3AF (gray-400)
- Cursor: not-allowed

## Form Integration

### React Hook Form
```tsx
import { useForm } from 'react-hook-form';

const { register, formState: { errors } } = useForm();

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
/>
```

### Controlled Component
```tsx
const [value, setValue] = useState('');

<Input
  label="שם"
  value={value}
  onChange={(e) => setValue(e.target.value)}
/>
```

### Uncontrolled with Ref
```tsx
const inputRef = useRef<HTMLInputElement>(null);

<Input
  label="שם"
  ref={inputRef}
/>

// Access value
const value = inputRef.current?.value;
```

## Accessibility

✓ Proper `<label>` association with `htmlFor`  
✓ ARIA attributes (`aria-invalid`, `aria-describedby`)  
✓ Error announcements for screen readers (`role="alert"`)  
✓ Keyboard navigation (Tab, Enter, Escape)  
✓ Focus visible indicators  
✓ Required indicator with `aria-label`  
✓ Password toggle with descriptive `aria-label`  

## RTL Support

✓ Text direction automatically set to RTL  
✓ Icons adapt position (right in RTL, left in LTR)  
✓ Padding adjusts based on icon position  
✓ Character counter positioned correctly  

## Styling Customization

```tsx
// Add custom classes
<Input 
  label="Custom"
  className="border-purple-500 focus:border-purple-700"
/>

// Override styles with Tailwind
<Input 
  label="Custom"
  className={cn('custom-class', someCondition && 'another-class')}
/>
```

## Best Practices

1. **Always provide a label** for accessibility
2. **Use appropriate input types** (email, tel, etc.)
3. **Show clear error messages** in Hebrew
4. **Use helper text** for additional context
5. **Mark required fields** explicitly
6. **Validate on blur** for better UX
7. **Show success states** after validation
8. **Use icons meaningfully** (not decoratively)

## Common Mistakes to Avoid

❌ No label (accessibility issue)  
❌ Generic error messages ("שגיאה")  
❌ Using password type without helper text  
❌ Not handling RTL properly  
❌ Forgetting to mark required fields  
❌ Using icons without semantic meaning  

## Performance Tips

- Use `React.memo` for forms with many inputs
- Debounce validation for real-time checks
- Use controlled components only when needed
- Avoid inline functions in onChange when possible

## Testing

```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import Input from './Input';

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
```

## Design Tokens

```css
/* Borders */
--input-border-default: 1.5px solid #D1D5DB;
--input-border-focus: #2563EB;
--input-border-error: #EF4444;
--input-border-success: #10B981;

/* Shadows */
--input-shadow-focus: 0 0 0 3px rgba(37, 99, 235, 0.1);
--input-shadow-error: 0 0 0 3px rgba(239, 68, 68, 0.1);
--input-shadow-success: 0 0 0 3px rgba(16, 185, 129, 0.1);

/* Spacing */
--input-padding: 12px 16px;
--input-border-radius: 8px;

/* Typography */
--input-font-size: 16px;
--label-font-size: 14px;
--helper-font-size: 13px;
```
