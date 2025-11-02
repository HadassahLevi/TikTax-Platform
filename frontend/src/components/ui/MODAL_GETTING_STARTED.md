# Modal Component - Getting Started

Quick start guide for using the Modal component in your Tik-Tax project.

---

## Step 1: Import

```tsx
import { Modal, useModal, Button } from '@/components/ui';
```

---

## Step 2: Create Modal State

Use the `useModal` hook for easy state management:

```tsx
function MyComponent() {
  const { isOpen, open, close } = useModal();
  
  // ... rest of component
}
```

---

## Step 3: Add Trigger Button

```tsx
<Button onClick={open}>
  Open Modal
</Button>
```

---

## Step 4: Add Modal

```tsx
<Modal
  isOpen={isOpen}
  onClose={close}
  title="Modal Title"
>
  <p>Your content here</p>
</Modal>
```

---

## Complete Example

```tsx
import { Modal, useModal, Button } from '@/components/ui';

function ExampleComponent() {
  const { isOpen, open, close } = useModal();

  return (
    <div>
      <Button onClick={open}>Open Modal</Button>

      <Modal
        isOpen={isOpen}
        onClose={close}
        title="Welcome"
        size="md"
      >
        <p>This is a simple modal example.</p>
      </Modal>
    </div>
  );
}
```

---

## Common Patterns

### 1. Form Modal

```tsx
const { isOpen, open, close } = useModal();
const [loading, setLoading] = useState(false);

const handleSubmit = async () => {
  setLoading(true);
  // ... submit form
  setLoading(false);
  close();
};

<Modal
  isOpen={isOpen}
  onClose={close}
  title="Add Item"
  closeOnOverlayClick={false} // Prevent accidental close
  footer={
    <div className="flex gap-3 justify-end">
      <Button variant="secondary" onClick={close}>
        Cancel
      </Button>
      <Button loading={loading} onClick={handleSubmit}>
        Save
      </Button>
    </div>
  }
>
  <form className="space-y-4">
    {/* Form fields */}
  </form>
</Modal>
```

### 2. Confirmation Modal

```tsx
const { isOpen, open, close } = useModal();

const handleConfirm = () => {
  // ... perform action
  close();
};

<Modal
  isOpen={isOpen}
  onClose={close}
  title="Confirm Action"
  size="sm"
  footer={
    <div className="flex gap-3 justify-end">
      <Button variant="secondary" onClick={close}>Cancel</Button>
      <Button variant="danger" onClick={handleConfirm}>Confirm</Button>
    </div>
  }
>
  <p>Are you sure you want to proceed?</p>
</Modal>
```

### 3. Information Modal

```tsx
<Modal
  isOpen={isOpen}
  onClose={close}
  title="Help"
  size="lg"
>
  <div className="prose">
    <h3>How to use this feature</h3>
    <p>Instructions here...</p>
  </div>
</Modal>
```

---

## Props Quick Reference

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `isOpen` | `boolean` | required | Show/hide modal |
| `onClose` | `function` | required | Close callback |
| `title` | `string` | - | Header title |
| `size` | `sm\|md\|lg\|xl\|full` | `md` | Modal width |
| `footer` | `ReactNode` | - | Action buttons |
| `closeOnOverlayClick` | `boolean` | `true` | Close when clicking backdrop |
| `closeOnEsc` | `boolean` | `true` | Close with ESC key |
| `showCloseButton` | `boolean` | `true` | Show X button |

---

## Size Guide

- **`sm`** (400px): Simple confirmations, alerts
- **`md`** (600px): Forms, standard dialogs
- **`lg`** (800px): Complex forms, tables
- **`xl`** (1200px): Dashboards, detailed views
- **`full`** (95vw): Galleries, full experiences

---

## Tips

✅ **Do:**
- Use `useModal()` hook for state
- Set `closeOnOverlayClick={false}` for forms
- Provide clear action buttons in footer
- Test keyboard navigation (Tab, ESC)
- Test on mobile devices

❌ **Don't:**
- Nest modals (use multi-step instead)
- Make content too long (keep under 70vh)
- Forget to handle loading states
- Block all close methods

---

## Accessibility

The Modal is fully accessible out of the box:

✅ Focus trap  
✅ ESC to close  
✅ ARIA attributes  
✅ Keyboard navigation  
✅ Screen reader support  

Just make sure your modal content is also accessible!

---

## Need More Help?

- 📖 **Full Docs:** `Modal.README.md`
- 🚀 **Quick Ref:** `Modal.QUICKREF.md`
- 🎨 **Examples:** `Modal.demo.tsx`
- 📋 **Implementation:** `MODAL_IMPLEMENTATION.md`

---

**Happy Coding! 🚀**
