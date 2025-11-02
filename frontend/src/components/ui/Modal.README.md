# Modal Component - Complete Documentation

## Overview

The Modal component is a fully accessible, animated dialog component built with **Framer Motion**, following the Tik-Tax design system. It provides a professional user experience with focus management, body scroll locking, keyboard navigation, and mobile optimization.

---

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Props API](#props-api)
4. [Size Variants](#size-variants)
5. [Accessibility Features](#accessibility-features)
6. [Custom Hooks](#custom-hooks)
7. [Animation System](#animation-system)
8. [Mobile Optimization](#mobile-optimization)
9. [Examples](#examples)
10. [Best Practices](#best-practices)

---

## Installation

The Modal component is already included in the UI component library. Import it:

```tsx
import { Modal, useModal } from '@/components/ui';
```

**Dependencies:**
- `framer-motion` - Animation library
- `lucide-react` - Icon library (X icon)

---

## Basic Usage

### Minimal Example

```tsx
import { Modal, useModal } from '@/components/ui';

function MyComponent() {
  const { isOpen, open, close } = useModal();

  return (
    <>
      <button onClick={open}>Open Modal</button>
      
      <Modal isOpen={isOpen} onClose={close}>
        <p>Modal content goes here</p>
      </Modal>
    </>
  );
}
```

### With Title and Footer

```tsx
<Modal
  isOpen={isOpen}
  onClose={close}
  title="הוסף קבלה חדשה"
  footer={
    <div className="flex gap-3">
      <Button variant="secondary" onClick={close}>ביטול</Button>
      <Button variant="primary" onClick={handleSave}>שמור</Button>
    </div>
  }
>
  <p>תוכן החלון כאן...</p>
</Modal>
```

---

## Props API

### ModalProps Interface

```typescript
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  closeOnOverlayClick?: boolean;
  closeOnEsc?: boolean;
  showCloseButton?: boolean;
}
```

### Prop Details

#### `isOpen` (required)
- **Type:** `boolean`
- **Description:** Controls the visibility of the modal
- **Example:** `isOpen={isModalOpen}`

#### `onClose` (required)
- **Type:** `() => void`
- **Description:** Callback function invoked when modal should close
- **Triggered by:**
  - Clicking overlay (if `closeOnOverlayClick` is true)
  - Pressing ESC key (if `closeOnEsc` is true)
  - Clicking close button (if `showCloseButton` is true)
- **Example:** `onClose={() => setIsModalOpen(false)}`

#### `title`
- **Type:** `string | undefined`
- **Default:** `undefined`
- **Description:** Title displayed in modal header
- **Example:** `title="אישור פעולה"`

#### `children`
- **Type:** `React.ReactNode`
- **Description:** Content displayed in modal body
- **Example:**
  ```tsx
  <Modal {...props}>
    <form>...</form>
  </Modal>
  ```

#### `footer`
- **Type:** `React.ReactNode | undefined`
- **Default:** `undefined`
- **Description:** Content displayed in modal footer (typically action buttons)
- **Example:**
  ```tsx
  footer={
    <div className="flex gap-3 justify-end">
      <Button>ביטול</Button>
      <Button>שמור</Button>
    </div>
  }
  ```

#### `size`
- **Type:** `'sm' | 'md' | 'lg' | 'xl' | 'full'`
- **Default:** `'md'`
- **Description:** Controls the maximum width of the modal
- **Sizes:**
  - `sm`: 400px max-width
  - `md`: 600px max-width
  - `lg`: 800px max-width
  - `xl`: 1200px max-width
  - `full`: 95vw max-width

#### `closeOnOverlayClick`
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Allow closing modal by clicking on the backdrop/overlay

#### `closeOnEsc`
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Allow closing modal by pressing the ESC key

#### `showCloseButton`
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Show the X button in the header for closing

---

## Size Variants

### Small (`sm`)
**Max Width:** 400px  
**Best For:** Simple confirmations, alerts, single-field forms

```tsx
<Modal size="sm" title="מחק קבלה" {...props}>
  <p>האם אתה בטוח?</p>
</Modal>
```

### Medium (`md`) - Default
**Max Width:** 600px  
**Best For:** Standard forms, most common use cases

```tsx
<Modal size="md" title="ערוך קבלה" {...props}>
  <form>...</form>
</Modal>
```

### Large (`lg`)
**Max Width:** 800px  
**Best For:** Forms with many fields, data tables

```tsx
<Modal size="lg" title="הגדרות מתקדמות" {...props}>
  {/* Complex content */}
</Modal>
```

### Extra Large (`xl`)
**Max Width:** 1200px  
**Best For:** Rich content, dashboards, detailed views

```tsx
<Modal size="xl" title="דוח מפורט" {...props}>
  {/* Wide content with charts/tables */}
</Modal>
```

### Full
**Max Width:** 95vw  
**Best For:** Full-screen experiences, galleries

```tsx
<Modal size="full" title="גלריית תמונות" {...props}>
  {/* Full-width content */}
</Modal>
```

---

## Accessibility Features

### Focus Management

The Modal component implements a **focus trap** that:

1. **Captures focus** when modal opens
2. **Focuses first focusable element** automatically
3. **Constrains Tab navigation** within modal
4. **Restores focus** to trigger element when modal closes

**Focusable elements detected:**
- Links (`<a href="...">`)
- Buttons (not disabled)
- Form inputs (not disabled)
- Select elements
- Textareas
- Elements with `tabindex` (except -1)

### Keyboard Navigation

| Key | Action |
|-----|--------|
| **Tab** | Move focus to next element (loops at end) |
| **Shift + Tab** | Move focus to previous element (loops at start) |
| **ESC** | Close modal (if `closeOnEsc={true}`) |

### ARIA Attributes

The Modal automatically sets:

```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title-xyz"
  aria-describedby="modal-body-xyz"
>
```

- **`role="dialog"`**: Identifies the modal as a dialog
- **`aria-modal="true"`**: Indicates this is a modal dialog
- **`aria-labelledby`**: References the title element
- **`aria-describedby`**: References the body content

### Body Scroll Lock

When modal is open:
- Background content is **not scrollable**
- Prevents confusing multi-layer scrolling
- Compensates for scrollbar width (prevents layout shift)
- Restores original scroll state on close

### Screen Reader Support

- Modal title is announced when opened
- Close button has `aria-label="סגור חלון"`
- Content is properly associated with dialog

---

## Custom Hooks

### `useModal(initialState?)`

Convenience hook for managing modal state.

**Parameters:**
- `initialState` (optional): Initial open state (default: `false`)

**Returns:**
```typescript
{
  isOpen: boolean;
  open: () => void;
  close: () => void;
  toggle: () => void;
  setIsOpen: (value: boolean) => void;
}
```

**Example:**
```tsx
const { isOpen, open, close, toggle } = useModal();

<Button onClick={open}>פתח</Button>
<Button onClick={toggle}>החלף מצב</Button>
<Modal isOpen={isOpen} onClose={close}>...</Modal>
```

### `useFocusTrap(isOpen, containerRef)`

Internal hook that implements focus trapping. Automatically used by Modal component.

### `useBodyScrollLock(isOpen)`

Internal hook that locks body scroll when modal is open. Automatically used by Modal component.

---

## Animation System

### Technology

Animations powered by **Framer Motion** for smooth, performant transitions.

### Overlay Animation

```typescript
const overlayVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.2 } },
  exit: { opacity: 0, transition: { duration: 0.15 } }
};
```

**Effect:** Simple fade in/out for backdrop.

### Modal Container Animation

#### Desktop (≥640px)

```typescript
{
  hidden: { opacity: 0, y: 50, scale: 0.95 },
  visible: { 
    opacity: 1, 
    y: 0, 
    scale: 1,
    transition: { duration: 0.3, type: 'spring' }
  },
  exit: { opacity: 0, y: 30, scale: 0.95 }
}
```

**Effect:** Fade + slight upward movement + subtle scale (feels professional).

#### Mobile (<640px)

```typescript
{
  hidden: { opacity: 0, y: '100%' },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.3, type: 'spring' }
  },
  exit: { opacity: 0, y: '100%' }
}
```

**Effect:** Slide up from bottom (native app feel).

### Animation Timing

- **Overlay fade in:** 200ms
- **Modal appear:** 300ms (spring animation)
- **Overlay fade out:** 150ms
- **Modal disappear:** 200ms

### Reduced Motion Support

Animations respect `prefers-reduced-motion` media query via Framer Motion's built-in support.

---

## Mobile Optimization

### Responsive Behavior

| Screen Size | Behavior |
|-------------|----------|
| **< 640px (Mobile)** | Full width, slides from bottom, rounded top corners only |
| **≥ 640px (Desktop)** | Centered, max-width based on size prop, fully rounded |

### Mobile-Specific Features

1. **Full-screen on mobile:** Maximizes screen real estate
2. **Slide-up animation:** Familiar mobile pattern
3. **Sticky footer:** Action buttons always visible
4. **Safe area insets:** Supports notched devices (iPhone X+)
5. **Touch-optimized:** Large touch targets for close button

### Safe Area Support

```tsx
className="pb-safe" // Adds padding for iOS home indicator
```

Works with devices that have:
- Notches (iPhone X and newer)
- Home indicators
- Rounded screen corners

---

## Examples

### 1. Confirmation Dialog

```tsx
const DeleteConfirmation = ({ itemName, onConfirm }) => {
  const { isOpen, open, close } = useModal();

  const handleDelete = () => {
    onConfirm();
    close();
  };

  return (
    <>
      <Button variant="danger" onClick={open}>
        מחק
      </Button>

      <Modal
        isOpen={isOpen}
        onClose={close}
        title="אישור מחיקה"
        size="sm"
        footer={
          <div className="flex gap-3 justify-end">
            <Button variant="secondary" onClick={close}>
              ביטול
            </Button>
            <Button variant="danger" onClick={handleDelete}>
              מחק
            </Button>
          </div>
        }
      >
        <div className="space-y-4">
          <p className="text-gray-600">
            האם אתה בטוח שברצונך למחוק את <strong>{itemName}</strong>?
          </p>
          <p className="text-sm text-gray-500">
            פעולה זו אינה ניתנת לביטול.
          </p>
        </div>
      </Modal>
    </>
  );
};
```

### 2. Form Modal

```tsx
import { useForm } from 'react-hook-form';

const AddReceiptModal = () => {
  const { isOpen, open, close } = useModal();
  const { register, handleSubmit, formState: { errors } } = useForm();
  const [loading, setLoading] = useState(false);

  const onSubmit = async (data) => {
    setLoading(true);
    try {
      await api.createReceipt(data);
      close();
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Button onClick={open} icon={<Plus />}>
        הוסף קבלה
      </Button>

      <Modal
        isOpen={isOpen}
        onClose={close}
        title="הוסף קבלה חדשה"
        size="md"
        closeOnOverlayClick={false} // Prevent accidental close
        footer={
          <div className="flex gap-3 justify-end">
            <Button 
              variant="secondary" 
              onClick={close}
              disabled={loading}
            >
              ביטול
            </Button>
            <Button 
              variant="primary" 
              onClick={handleSubmit(onSubmit)}
              loading={loading}
            >
              שמור
            </Button>
          </div>
        }
      >
        <form className="space-y-4">
          <Input
            label="שם עסק"
            error={errors.businessName?.message}
            {...register('businessName', { 
              required: 'שדה חובה' 
            })}
          />
          
          <Input
            label="סכום"
            type="number"
            error={errors.amount?.message}
            {...register('amount', { 
              required: 'שדה חובה',
              min: { value: 0, message: 'סכום חייב להיות חיובי' }
            })}
          />

          <Input
            label="תאריך"
            type="date"
            {...register('date')}
          />
        </form>
      </Modal>
    </>
  );
};
```

### 3. Multi-Step Modal

```tsx
const OnboardingModal = () => {
  const { isOpen, open, close } = useModal();
  const [step, setStep] = useState(1);
  const totalSteps = 3;

  const nextStep = () => setStep(s => Math.min(s + 1, totalSteps));
  const prevStep = () => setStep(s => Math.max(s - 1, 1));

  const handleFinish = () => {
    // Save data
    close();
    setStep(1); // Reset for next time
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={close}
      title={`שלב ${step} מתוך ${totalSteps}`}
      size="lg"
      closeOnOverlayClick={false}
      closeOnEsc={false}
      footer={
        <div className="flex gap-3 justify-between w-full">
          <Button 
            variant="secondary"
            onClick={prevStep}
            disabled={step === 1}
          >
            חזור
          </Button>
          
          <Button
            variant="primary"
            onClick={step === totalSteps ? handleFinish : nextStep}
          >
            {step === totalSteps ? 'סיום' : 'המשך'}
          </Button>
        </div>
      }
    >
      {step === 1 && <Step1Content />}
      {step === 2 && <Step2Content />}
      {step === 3 && <Step3Content />}
    </Modal>
  );
};
```

### 4. Information Modal (Read-Only)

```tsx
const HelpModal = () => {
  const { isOpen, open, close } = useModal();

  return (
    <>
      <Button variant="ghost" icon={<HelpCircle />} onClick={open}>
        עזרה
      </Button>

      <Modal
        isOpen={isOpen}
        onClose={close}
        title="מדריך למשתמש"
        size="lg"
      >
        <div className="prose prose-sm max-w-none">
          <h3>כיצד להשתמש במערכת</h3>
          <p>ברוכים הבאים למערכת ניהול הקבלות...</p>
          
          <h4>שלב 1: העלאת קבלה</h4>
          <ul>
            <li>צלם תמונה של הקבלה</li>
            <li>או העלה קובץ מהמכשיר</li>
          </ul>

          {/* More content */}
        </div>
      </Modal>
    </>
  );
};
```

### 5. Loading State Modal

```tsx
const ProcessingModal = ({ isProcessing }) => {
  return (
    <Modal
      isOpen={isProcessing}
      onClose={() => {}} // Can't close
      closeOnOverlayClick={false}
      closeOnEsc={false}
      showCloseButton={false}
      size="sm"
    >
      <div className="flex flex-col items-center gap-4 py-6">
        <Loader2 className="w-12 h-12 animate-spin text-blue-600" />
        <p className="text-lg font-medium">מעבד קבלה...</p>
        <p className="text-sm text-gray-500">אנא המתן</p>
      </div>
    </Modal>
  );
};
```

---

## Best Practices

### ✅ Do's

1. **Always provide `onClose`** - Even if all close methods are disabled, provide a way to close
2. **Use appropriate sizes** - Match size to content complexity
3. **Loading states** - Show loading in footer buttons during async operations
4. **Prevent accidental close** - Set `closeOnOverlayClick={false}` for forms
5. **Clear actions** - Footer should have clear primary/secondary actions
6. **Responsive content** - Ensure modal content works on mobile
7. **Accessible labels** - Provide meaningful titles
8. **Test keyboard nav** - Ensure all interactive elements are accessible

### ❌ Don'ts

1. **Don't nest modals** - Use multi-step pattern instead
2. **Don't put too much content** - If scrolling is extensive, consider a full page
3. **Don't forget mobile** - Always test on small screens
4. **Don't disable all close methods** - Users need an escape route
5. **Don't use for critical system messages** - Use toast/alert for those
6. **Don't auto-open on page load** - Respect user attention

### Performance Tips

1. **Lazy load modal content** - Don't render heavy content until modal opens
2. **Cleanup on close** - Reset form state when modal closes
3. **Debounce form submissions** - Prevent double-clicks on save
4. **Optimize animations** - Framer Motion handles this, but avoid heavy re-renders

### Accessibility Checklist

- [ ] Modal has a descriptive title
- [ ] Focus moves to modal when opened
- [ ] Tab navigation works correctly
- [ ] ESC key closes modal (or explain why not)
- [ ] Focus returns to trigger element on close
- [ ] Close button has accessible label
- [ ] Color contrast meets WCAG AA
- [ ] Works with screen readers
- [ ] Respects reduced motion preferences

---

## Troubleshooting

### Modal doesn't close with ESC

**Check:** `closeOnEsc` prop is `true` (default)

### Background still scrollable

**Cause:** Multiple modals or another scroll lock mechanism  
**Fix:** Ensure only one modal is open at a time

### Focus not trapping

**Check:** Modal content has focusable elements  
**Debug:** Inspect with browser dev tools, ensure elements aren't `disabled` or have `tabindex="-1"`

### Animation feels janky on mobile

**Check:** Device performance, reduce animation complexity if needed  
**Fix:** Test on actual devices, not just browser DevTools

### Modal appears behind other content

**Check:** z-index conflicts  
**Fix:** Modal uses `z-50`, ensure other fixed elements use lower z-index

---

## Design System Alignment

The Modal component follows the Tik-Tax design system:

- **Colors:** Uses system colors (primary blue, grays)
- **Typography:** H2 for title (24px, weight 600)
- **Spacing:** 8-point grid (padding: 32px desktop, 24px mobile)
- **Border Radius:** 16px (spacious variant)
- **Shadow:** Level 4 elevation
- **Transitions:** 0.2-0.3s ease
- **Accessibility:** WCAG 2.1 AA compliant

---

## Browser Support

- ✅ Chrome 90+
- ✅ Safari 14+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Mobile Safari (iOS 14+)
- ✅ Chrome Mobile

---

## Version History

**v1.0** (2025-11-02)
- Initial release
- Full accessibility support
- Framer Motion animations
- Mobile optimization
- Focus trap implementation
- Body scroll lock
- useModal hook

---

**Component Author:** Tik-Tax Development Team  
**Last Updated:** 2025-11-02  
**Design System Version:** 2.0
