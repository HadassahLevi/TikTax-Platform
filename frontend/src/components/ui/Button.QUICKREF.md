# Button Component - Quick Reference

## Import

```tsx
import { Button } from '@/components/ui';
```

## Variants

```tsx
<Button variant="primary">שמור</Button>     // Blue, main actions
<Button variant="secondary">ביטול</Button>  // White, alternative
<Button variant="ghost">פרטים</Button>      // Transparent, tertiary
<Button variant="danger">מחק</Button>       // Red, destructive
```

## Sizes

```tsx
<Button size="sm">קטן</Button>    // 36px
<Button size="md">בינוני</Button> // 44px (default)
<Button size="lg">גדול</Button>   // 52px
```

## Icons

```tsx
import { Upload, Save } from 'lucide-react';

<Button icon={<Upload />}>העלה</Button>                    // Left
<Button icon={<Save />} iconPosition="right">שמור</Button> // Right
```

## States

```tsx
<Button loading>שומר...</Button>    // Shows spinner
<Button disabled>לא זמין</Button>   // Disabled
```

## Layout

```tsx
<Button fullWidth>רוחב מלא</Button>
```

## Most Common Use Cases

### 1. Receipt Upload (Primary Action)
```tsx
<Button variant="primary" size="lg" icon={<Upload />} fullWidth>
  העלה קבלה חדשה
</Button>
```

### 2. Form Submit/Cancel
```tsx
<Button type="submit" loading={isSubmitting}>שלח</Button>
<Button variant="ghost" onClick={onCancel}>ביטול</Button>
```

### 3. Delete Confirmation
```tsx
<Button variant="danger" size="sm" icon={<Trash2 />}>מחק</Button>
<Button variant="secondary" size="sm">ביטול</Button>
```

### 4. Action Group
```tsx
<div className="flex gap-3">
  <Button variant="primary">שמור</Button>
  <Button variant="secondary">ביטול</Button>
</div>
```

### 5. Mobile Stack
```tsx
<div className="flex flex-col gap-2">
  <Button fullWidth variant="primary">ראשי</Button>
  <Button fullWidth variant="secondary">משני</Button>
</div>
```

## Props Reference

| Prop | Values | Default |
|------|--------|---------|
| `variant` | `primary`, `secondary`, `ghost`, `danger` | `primary` |
| `size` | `sm`, `md`, `lg` | `md` |
| `loading` | `boolean` | `false` |
| `disabled` | `boolean` | `false` |
| `fullWidth` | `boolean` | `false` |
| `icon` | `ReactNode` | - |
| `iconPosition` | `left`, `right` | `left` |

## Accessibility

- ✅ Min 44px touch target
- ✅ Keyboard navigation
- ✅ Focus indicators
- ✅ ARIA attributes
- ✅ Screen reader support

## Colors

- **Primary:** #2563EB (blue)
- **Secondary:** #FFFFFF (white) + gray border
- **Ghost:** Transparent + blue text
- **Danger:** #EF4444 (red)
- **Disabled:** #E5E7EB (gray)

## Files

- Component: `src/components/ui/Button.tsx`
- Export: `src/components/ui/index.ts`
- Demo: `src/components/ui/Button.demo.tsx`
- Docs: `src/components/ui/Button.README.md`
