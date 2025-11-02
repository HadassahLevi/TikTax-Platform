# Modal Component - Quick Reference

## Import

```tsx
import { Modal, useModal } from '@/components/ui';
```

## Basic Usage

```tsx
const { isOpen, open, close } = useModal();

<Modal
  isOpen={isOpen}
  onClose={close}
  title="הוסף קבלה"
>
  <p>תוכן החלון כאן...</p>
</Modal>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `isOpen` | `boolean` | **required** | Controls modal visibility |
| `onClose` | `() => void` | **required** | Callback when modal closes |
| `title` | `string` | `undefined` | Modal header title |
| `children` | `ReactNode` | **required** | Modal body content |
| `footer` | `ReactNode` | `undefined` | Footer content (buttons) |
| `size` | `'sm' \| 'md' \| 'lg' \| 'xl' \| 'full'` | `'md'` | Modal width |
| `closeOnOverlayClick` | `boolean` | `true` | Close when clicking backdrop |
| `closeOnEsc` | `boolean` | `true` | Close with ESC key |
| `showCloseButton` | `boolean` | `true` | Show X button in header |

## Size Variants

```tsx
// Small - 400px max width
<Modal size="sm" {...props}>

// Medium (default) - 600px max width
<Modal size="md" {...props}>

// Large - 800px max width
<Modal size="lg" {...props}>

// Extra Large - 1200px max width
<Modal size="xl" {...props}>

// Full - 95vw max width
<Modal size="full" {...props}>
```

## With Footer (Actions)

```tsx
<Modal
  isOpen={isOpen}
  onClose={close}
  title="אישור פעולה"
  footer={
    <div className="flex gap-3 justify-end">
      <Button variant="secondary" onClick={close}>
        ביטול
      </Button>
      <Button variant="primary" onClick={handleConfirm}>
        אישור
      </Button>
    </div>
  }
>
  <p>האם אתה בטוח שברצונך לבצע פעולה זו?</p>
</Modal>
```

## useModal Hook

```tsx
const { isOpen, open, close, toggle, setIsOpen } = useModal();

// or with initial state
const modal = useModal(true); // starts open
```

### Hook API

| Property | Type | Description |
|----------|------|-------------|
| `isOpen` | `boolean` | Current state |
| `open` | `() => void` | Open modal |
| `close` | `() => void` | Close modal |
| `toggle` | `() => void` | Toggle modal |
| `setIsOpen` | `(value: boolean) => void` | Set state directly |

## Form Modal Example

```tsx
import { useForm } from 'react-hook-form';

const FormModal = () => {
  const { isOpen, open, close } = useModal();
  const { register, handleSubmit } = useForm();

  const onSubmit = (data) => {
    console.log(data);
    close();
  };

  return (
    <>
      <Button onClick={open}>פתח טופס</Button>
      
      <Modal
        isOpen={isOpen}
        onClose={close}
        title="מלא פרטים"
        size="md"
        footer={
          <div className="flex gap-3 justify-end">
            <Button variant="secondary" onClick={close}>
              ביטול
            </Button>
            <Button 
              variant="primary" 
              onClick={handleSubmit(onSubmit)}
            >
              שמור
            </Button>
          </div>
        }
      >
        <form className="space-y-4">
          <Input
            label="שם"
            {...register('name', { required: true })}
          />
          <Input
            label="אימייל"
            type="email"
            {...register('email')}
          />
        </form>
      </Modal>
    </>
  );
};
```

## Confirmation Modal Pattern

```tsx
const ConfirmDeleteModal = ({ itemName, onConfirm }) => {
  const { isOpen, open, close } = useModal();

  const handleConfirm = () => {
    onConfirm();
    close();
  };

  return (
    <>
      <Button variant="danger" onClick={open}>מחק</Button>
      
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
            <Button variant="danger" onClick={handleConfirm}>
              מחק
            </Button>
          </div>
        }
      >
        <p className="text-gray-600">
          האם אתה בטוח שברצונך למחוק את <strong>{itemName}</strong>?
          פעולה זו אינה ניתנת לביטול.
        </p>
      </Modal>
    </>
  );
};
```

## Disable Close Options

```tsx
// Can't close by clicking overlay or ESC
<Modal
  isOpen={isOpen}
  onClose={close}
  closeOnOverlayClick={false}
  closeOnEsc={false}
  showCloseButton={false}
  footer={
    <Button onClick={close}>סגור</Button>
  }
>
  חייב לסגור דרך הכפתור בלבד
</Modal>
```

## Accessibility Features

✅ **Focus Management:**
- Traps focus inside modal when open
- Focuses first focusable element on open
- Restores focus to trigger element on close

✅ **Keyboard Navigation:**
- Tab/Shift+Tab cycles through focusable elements
- ESC key closes modal (if enabled)

✅ **ARIA Attributes:**
- `role="dialog"`
- `aria-modal="true"`
- `aria-labelledby` (title)
- `aria-describedby` (body)

✅ **Body Scroll Lock:**
- Prevents background scrolling
- Compensates for scrollbar width

## Mobile Behavior

- **< 640px:** Full width, slides up from bottom
- **≥ 640px:** Centered, fades + scales in
- Safe area support for notched devices
- Sticky footer on mobile
- Optimized touch targets

## Animation Details

**Desktop:**
- Overlay: Fade in/out (200ms)
- Modal: Fade + Scale + Slight Y movement (300ms spring)

**Mobile:**
- Overlay: Fade in/out (200ms)
- Modal: Slide up from bottom (300ms spring)

## Styling Notes

- **Shadow:** Level 4 elevation (design system)
- **Border Radius:** 16px (spacious)
- **Max Height:** 70vh for body content
- **Scrollbar:** Custom styled (thin, gray)
- **z-index:** 50 (above most content)

## Common Patterns

### Loading State in Modal

```tsx
<Modal {...props} footer={
  <Button loading disabled>
    שומר...
  </Button>
}>
  {/* content */}
</Modal>
```

### Multi-Step Modal

```tsx
const [step, setStep] = useState(1);

<Modal
  {...props}
  title={`שלב ${step} מתוך 3`}
  footer={
    <div className="flex gap-3 justify-between w-full">
      <Button 
        variant="secondary" 
        onClick={() => setStep(s => s - 1)}
        disabled={step === 1}
      >
        חזור
      </Button>
      <Button onClick={() => setStep(s => s + 1)}>
        {step === 3 ? 'סיום' : 'המשך'}
      </Button>
    </div>
  }
>
  {/* Step content */}
</Modal>
```

### Scrollable Content

```tsx
<Modal {...props}>
  <div className="space-y-4">
    {items.map(item => (
      <Card key={item.id}>{item.name}</Card>
    ))}
  </div>
</Modal>
```

The modal body automatically becomes scrollable when content exceeds 70vh.

## Tips

1. **Always provide onClose** even if other close methods are disabled
2. **Use size="sm"** for simple confirmations
3. **Use size="lg" or "xl"** for forms with many fields
4. **Footer buttons** should be right-aligned (RTL support)
5. **Avoid nested modals** - use multi-step pattern instead
6. **Test keyboard navigation** - ensure all actions are accessible

---

**Version:** 1.0  
**Last Updated:** 2025-11-02
