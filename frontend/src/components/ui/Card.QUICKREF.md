# Card Component - Quick Reference

## Import
```typescript
import { Card } from '@/components/ui';
```

## Props
```typescript
interface CardProps {
  children: React.ReactNode;
  shadow?: 'none' | 'sm' | 'md' | 'lg';    // Default: 'md'
  padding?: 'none' | 'sm' | 'md' | 'lg';   // Default: 'md'
  hoverable?: boolean;                      // Default: false
  onClick?: () => void;
  className?: string;
  as?: 'div' | 'article' | 'section';      // Default: 'div'
}
```

## Basic Usage
```tsx
<Card>
  <h3>כותרת</h3>
  <p>תוכן הכרטיס</p>
</Card>
```

## Shadow Variants
```tsx
<Card shadow="none">No shadow</Card>
<Card shadow="sm">Small shadow (resting)</Card>
<Card shadow="md">Medium shadow (default)</Card>
<Card shadow="lg">Large shadow (elevated)</Card>
```

## Padding Variants
```tsx
<Card padding="none">No padding</Card>
<Card padding="sm">16px padding</Card>
<Card padding="md">24px padding (default)</Card>
<Card padding="lg">32px padding</Card>
```

## Hoverable Card
```tsx
<Card hoverable onClick={() => console.log('Clicked')}>
  Hover over me!
</Card>
```

## Image Card (no padding)
```tsx
<Card padding="none" shadow="sm">
  <img src="/receipt.jpg" alt="Receipt" className="w-full" />
  <div className="p-4">
    <h3>Receipt Details</h3>
  </div>
</Card>
```

## Semantic HTML
```tsx
<Card as="article">
  <h2>Blog Post Title</h2>
  <p>Content...</p>
</Card>
```

## Design System Mapping
- **Shadow none**: No shadow
- **Shadow sm**: Level 1 (0 1px 3px 0 rgba(0,0,0,0.08))
- **Shadow md**: Level 2 (0 4px 6px -1px rgba(0,0,0,0.1))
- **Shadow lg**: Level 3 (0 10px 15px -3px rgba(0,0,0,0.15))

- **Padding sm**: 16px (p-4)
- **Padding md**: 24px (p-6) - Standard card
- **Padding lg**: 32px (p-8) - Large card

## Hover Behavior
When `hoverable={true}`:
- Lifts up 2px (translateY(-2px))
- Shadow increases to next level
- Cursor changes to pointer
- Smooth 0.2s transition

## Accessibility
- Keyboard navigable when clickable (onClick)
- Focus ring on keyboard focus
- Semantic HTML with proper roles
- ARIA attributes when interactive
