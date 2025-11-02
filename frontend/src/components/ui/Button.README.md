# Button Component

Professional, accessible button component following the Tik-Tax design system specifications.

## Features

✅ **4 Variants**: Primary, Secondary, Ghost, Danger  
✅ **3 Sizes**: Small (36px), Medium (44px), Large (52px)  
✅ **Loading State**: Built-in spinner animation  
✅ **Icon Support**: Left or right positioned icons  
✅ **Full Width Option**: Responsive layout support  
✅ **Accessibility**: WCAG 2.1 AA compliant  
✅ **RTL Support**: Right-to-left layout compatible  
✅ **TypeScript**: Full type safety  
✅ **Tailwind CSS**: Utility-first styling  

---

## Installation

The Button component is already set up in the project. Import it from the UI components:

```typescript
import { Button } from '@/components/ui';
```

---

## Basic Usage

### Variants

```tsx
// Primary (default) - Main actions
<Button variant="primary">שמור</Button>

// Secondary - Alternative actions
<Button variant="secondary">ביטול</Button>

// Ghost - Tertiary actions
<Button variant="ghost">עוד פרטים</Button>

// Danger - Destructive actions
<Button variant="danger">מחק</Button>
```

### Sizes

```tsx
<Button size="sm">קטן</Button>      // 36px height
<Button size="md">בינוני</Button>   // 44px height (default)
<Button size="lg">גדול</Button>     // 52px height
```

### With Icons

```tsx
import { Upload, Download, Save } from 'lucide-react';

// Icon on left (default)
<Button icon={<Upload />}>העלה קבלה</Button>

// Icon on right
<Button icon={<Download />} iconPosition="right">הורד</Button>

// Different sizes
<Button size="sm" icon={<Save />}>שמור</Button>
<Button size="lg" icon={<Save />}>שמור</Button>
```

---

## States

### Loading

Shows a spinner and disables interaction. Automatically sets `aria-busy="true"`.

```tsx
const [isLoading, setIsLoading] = useState(false);

<Button loading={isLoading} onClick={handleSave}>
  שומר...
</Button>

// Always loading
<Button loading>מעבד...</Button>
```

### Disabled

Disables interaction and applies disabled styling. Automatically sets `aria-disabled="true"`.

```tsx
<Button disabled>לא זמין</Button>
<Button disabled variant="primary">לא ניתן ללחוץ</Button>
```

---

## Layout

### Full Width

Makes the button span the full width of its container.

```tsx
<Button fullWidth>שמור שינויים</Button>

// Stacked mobile buttons
<div className="flex flex-col gap-2">
  <Button fullWidth variant="primary">פעולה ראשית</Button>
  <Button fullWidth variant="secondary">פעולה משנית</Button>
</div>
```

---

## Common Patterns

### Receipt Upload (Primary Use Case)

```tsx
<Button 
  variant="primary" 
  size="lg" 
  icon={<Upload />}
  fullWidth
  onClick={handleUpload}
>
  העלה קבלה חדשה
</Button>
```

### Form Actions

```tsx
<form onSubmit={handleSubmit}>
  <div className="flex gap-3">
    <Button type="submit" loading={isSubmitting}>
      שלח טופס
    </Button>
    <Button type="button" variant="ghost" onClick={handleCancel}>
      ביטול
    </Button>
  </div>
</form>
```

### Action Button Group

```tsx
<div className="flex gap-3">
  <Button variant="primary" icon={<Save />}>שמור</Button>
  <Button variant="secondary" icon={<X />}>ביטול</Button>
</div>
```

### Destructive Action

```tsx
<div className="flex gap-3">
  <Button 
    variant="danger" 
    size="sm" 
    icon={<Trash2 />}
    onClick={handleDelete}
  >
    מחק קבלה
  </Button>
  <Button variant="secondary" size="sm">
    ביטול
  </Button>
</div>
```

---

## Props API

```typescript
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  fullWidth?: boolean;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
  children: React.ReactNode;
}
```

### Prop Details

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `variant` | `'primary' \| 'secondary' \| 'ghost' \| 'danger'` | `'primary'` | Visual style variant |
| `size` | `'sm' \| 'md' \| 'lg'` | `'md'` | Button size |
| `loading` | `boolean` | `false` | Shows spinner, disables interaction |
| `disabled` | `boolean` | `false` | Disables the button |
| `fullWidth` | `boolean` | `false` | Makes button full width |
| `icon` | `React.ReactNode` | `undefined` | Icon to display |
| `iconPosition` | `'left' \| 'right'` | `'left'` | Icon position |
| `children` | `React.ReactNode` | **required** | Button content |

All standard HTML button attributes are supported (`onClick`, `type`, `form`, etc.)

---

## Design Specifications

### Colors

**Primary:**
- Background: `#2563EB` (primary-500)
- Hover: `#1D4ED8` (primary-600)
- Active: `#1E40AF` (primary-700)
- Text: `#FFFFFF`

**Secondary:**
- Background: `#FFFFFF`
- Border: `#D1D5DB` (gray-300)
- Hover: `#F9FAFB` (gray-50)
- Text: `#374151` (gray-700)

**Ghost:**
- Background: Transparent
- Hover: `#EFF6FF` (blue-50)
- Text: `#2563EB` (primary-600)

**Danger:**
- Background: `#EF4444` (error-500)
- Hover: `#DC2626` (error-600)
- Active: `#B91C1C` (error-700)
- Text: `#FFFFFF`

**Disabled:**
- Background: `#E5E7EB` (gray-200)
- Text: `#9CA3AF` (gray-400)

### Dimensions

| Size | Padding | Height | Font Size |
|------|---------|--------|-----------|
| Small | 8px 16px | 36px | 14px |
| Medium | 12px 24px | 44px | 15px |
| Large | 14px 28px | 52px | 16px |

### Other

- **Border Radius:** 8px
- **Font Weight:** 500 (Medium)
- **Transition:** 0.2s ease
- **Focus Ring:** 2px outline, 2px offset
- **Shadow (Hover):** Subtle elevation

---

## Accessibility

### WCAG 2.1 AA Compliance

✅ **Minimum Touch Target:** 44px × 44px (medium and large sizes)  
✅ **Color Contrast:** All variants meet 4.5:1 ratio  
✅ **Keyboard Navigation:** Full support for Tab, Enter, Space  
✅ **Focus Indicators:** Visible 2px outline ring  
✅ **Screen Reader:** Proper ARIA attributes  

### ARIA Attributes

The component automatically manages:
- `aria-disabled="true"` when disabled or loading
- `aria-busy="true"` when loading
- Custom `aria-label` can be added via props

### Example: Icon-Only Button

```tsx
<Button 
  icon={<Plus />} 
  aria-label="הוסף קבלה חדשה"
  variant="ghost"
/>
```

---

## Advanced Usage

### With Ref

```tsx
import { useRef } from 'react';

const buttonRef = useRef<HTMLButtonElement>(null);

<Button ref={buttonRef}>התמקד כאן</Button>

// Focus programmatically
buttonRef.current?.focus();
```

### Custom Styling

```tsx
// Extend with custom classes
<Button className="mt-4 shadow-xl">
  כפתור מותאם
</Button>

// Classes are merged intelligently with cn() utility
```

### All HTML Button Attributes

```tsx
<Button
  type="submit"
  form="my-form"
  name="action"
  value="save"
  onClick={handleClick}
  onFocus={handleFocus}
  onBlur={handleBlur}
  tabIndex={0}
>
  שמור
</Button>
```

---

## Testing

### Unit Tests

```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '@/components/ui';

test('renders button with text', () => {
  render(<Button>שמור</Button>);
  expect(screen.getByRole('button', { name: 'שמור' })).toBeInTheDocument();
});

test('calls onClick when clicked', () => {
  const handleClick = jest.fn();
  render(<Button onClick={handleClick}>לחץ</Button>);
  fireEvent.click(screen.getByRole('button'));
  expect(handleClick).toHaveBeenCalledTimes(1);
});

test('is disabled when loading', () => {
  render(<Button loading>שומר...</Button>);
  expect(screen.getByRole('button')).toBeDisabled();
  expect(screen.getByRole('button')).toHaveAttribute('aria-busy', 'true');
});
```

---

## Browser Support

- ✅ Chrome 90+
- ✅ Safari 14+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Mobile Safari (iOS 14+)
- ✅ Chrome Mobile (Android)

---

## Demo

A comprehensive demo is available at:

```
src/components/ui/Button.demo.tsx
```

To view the demo, import it into a page:

```tsx
import ButtonDemo from '@/components/ui/Button.demo';

// In your component
<ButtonDemo />
```

---

## Related Components

- **Input** (Coming soon)
- **Card** (Coming soon)
- **Modal** (Coming soon)

---

## Changelog

### v1.0.0 (Current)
- ✅ Initial release
- ✅ 4 variants (primary, secondary, ghost, danger)
- ✅ 3 sizes (sm, md, lg)
- ✅ Loading state with spinner
- ✅ Icon support (left/right)
- ✅ Full width option
- ✅ Complete accessibility
- ✅ RTL support
- ✅ TypeScript types

---

## License

Part of the Tik-Tax platform. Internal use only.
