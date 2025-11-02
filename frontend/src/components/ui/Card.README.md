# Card Component

## Overview
The Card component is a flexible, reusable content container that follows the Tik-Tax design system. It provides consistent styling with configurable shadow depths, padding levels, and hover interactions.

## Design System Compliance
- ✅ Professional FinTech aesthetic
- ✅ Consistent elevation system (4 shadow levels)
- ✅ 8-point grid spacing system
- ✅ Smooth transitions (0.2s ease)
- ✅ Accessible and semantic HTML
- ✅ Keyboard navigable when interactive

## Features
- **Shadow Variants**: 4 elevation levels (none, sm, md, lg)
- **Padding Variants**: 4 spacing levels (none, sm, md, lg)
- **Hoverable**: Optional lift and shadow increase on hover
- **Clickable**: Support for onClick with keyboard navigation
- **Semantic HTML**: Render as div, article, or section
- **Customizable**: Accept additional className for overrides
- **Accessible**: WCAG 2.1 AA compliant with focus indicators

## Installation
```bash
# Component is part of the UI components library
import { Card } from '@/components/ui';
```

## Props API

### CardProps Interface
```typescript
interface CardProps {
  children: React.ReactNode;        // Required - Card content
  shadow?: 'none' | 'sm' | 'md' | 'lg';  // Default: 'md'
  padding?: 'none' | 'sm' | 'md' | 'lg'; // Default: 'md'
  hoverable?: boolean;              // Default: false
  onClick?: () => void;             // Optional click handler
  className?: string;               // Additional CSS classes
  as?: 'div' | 'article' | 'section';    // Default: 'div'
}
```

## Usage Examples

### Basic Card (Default Styling)
```tsx
<Card>
  <h3 className="text-lg font-semibold mb-2">כותרת כרטיס</h3>
  <p className="text-gray-600">תוכן הכרטיס</p>
</Card>
```

### Shadow Variants
```tsx
{/* No shadow - flat appearance */}
<Card shadow="none">
  <p>Flat card</p>
</Card>

{/* Small shadow - resting state */}
<Card shadow="sm">
  <p>Level 1 elevation</p>
</Card>

{/* Medium shadow - default */}
<Card shadow="md">
  <p>Standard card elevation</p>
</Card>

{/* Large shadow - elevated state */}
<Card shadow="lg">
  <p>Highly elevated card</p>
</Card>
```

### Padding Variants
```tsx
{/* No padding - for images */}
<Card padding="none">
  <img src="/image.jpg" alt="Full width image" className="w-full" />
</Card>

{/* Small padding - 16px */}
<Card padding="sm">
  <p>Compact card</p>
</Card>

{/* Medium padding - 24px (default) */}
<Card padding="md">
  <p>Standard card</p>
</Card>

{/* Large padding - 32px */}
<Card padding="lg">
  <p>Spacious card</p>
</Card>
```

### Hoverable Interactive Card
```tsx
<Card hoverable onClick={() => navigate('/details')}>
  <h3>לחץ עלי</h3>
  <p>הכרטיס יתרומם ויגדיל את הצל בהעברת עכבר</p>
</Card>
```

### Image Card (No Padding + Hover)
```tsx
<Card padding="none" shadow="sm" hoverable>
  <img src="/receipt.jpg" alt="Receipt" className="w-full aspect-video object-cover" />
  <div className="p-4">
    <h3 className="font-semibold">סופר פארם</h3>
    <p className="text-gray-600">₪234.50</p>
  </div>
</Card>
```

### Semantic HTML Variants
```tsx
{/* Article card - for blog posts, news items */}
<Card as="article">
  <h2>Blog Post Title</h2>
  <p>Content...</p>
</Card>

{/* Section card - for page sections */}
<Card as="section">
  <h2>Dashboard Section</h2>
  <div>Statistics...</div>
</Card>
```

### Custom Styling
```tsx
{/* Add custom border */}
<Card className="border-2 border-primary">
  <p>Highlighted card with blue border</p>
</Card>

{/* Gradient background */}
<Card className="bg-gradient-to-br from-blue-50 to-purple-50 border-none">
  <p>Gradient card</p>
</Card>
```

### Dashboard Stats Container
```tsx
<Card>
  <div className="flex items-center justify-between">
    <div>
      <p className="text-sm text-gray-600">סך הוצאות החודש</p>
      <p className="text-3xl font-bold font-mono">₪12,345.67</p>
    </div>
    <div className="p-3 bg-blue-100 rounded-lg">
      <DollarSignIcon className="w-6 h-6 text-blue-600" />
    </div>
  </div>
</Card>
```

### Feature Card with Icon
```tsx
<Card hoverable>
  <div className="flex items-start gap-4">
    <div className="p-3 bg-emerald-100 rounded-lg">
      <CheckIcon className="w-6 h-6 text-emerald-600" />
    </div>
    <div>
      <h3 className="text-lg font-semibold mb-2">OCR Accuracy</h3>
      <p className="text-gray-600">95%+ accuracy for Hebrew receipts</p>
    </div>
  </div>
</Card>
```

## Design System Mapping

### Shadow Levels
| Variant | Tailwind Class | CSS Value | Design System Level | Use Case |
|---------|---------------|-----------|---------------------|----------|
| `none` | - | No shadow | Level 0 | Flat elements, nested cards |
| `sm` | `shadow-sm` | `0 1px 3px 0 rgba(0,0,0,0.08)` | Level 1 | Resting state, subtle elevation |
| `md` | `shadow-md` | `0 4px 6px -1px rgba(0,0,0,0.1)` | Level 2 | Standard cards (default) |
| `lg` | `shadow-lg` | `0 10px 15px -3px rgba(0,0,0,0.15)` | Level 3 | Elevated cards, dropdowns |

### Padding Levels (8-Point Grid)
| Variant | Tailwind Class | Pixels | Use Case |
|---------|---------------|--------|----------|
| `none` | `p-0` | 0px | Image cards, custom layouts |
| `sm` | `p-4` | 16px | Compact cards, tight layouts |
| `md` | `p-6` | 24px | Standard cards (default) |
| `lg` | `p-8` | 32px | Large cards, spacious layouts |

### Hover Behavior
When `hoverable={true}`:
- **Transform**: `translateY(-2px)` - Lifts card up by 2px
- **Shadow**: Increases to next level (e.g., sm → md → lg → xl)
- **Cursor**: Changes to `pointer`
- **Transition**: Smooth `0.2s ease` animation
- **Focus**: Visible ring on keyboard focus (accessibility)

## Accessibility Features

### Keyboard Navigation
- **Tab**: Focus on clickable cards
- **Enter/Space**: Trigger onClick when focused
- **Visual Focus**: Blue ring indicator (`ring-2 ring-primary`)

### ARIA Attributes
- `role="button"`: Applied when onClick is provided
- `tabIndex={0}`: Makes clickable cards keyboard accessible

### Screen Reader Support
- Semantic HTML elements (div, article, section)
- Proper heading hierarchy when used with headings
- Interactive cards announced as buttons

## Best Practices

### ✅ DO
- Use `padding="none"` for image-based cards
- Use `hoverable` for clickable/navigable cards
- Provide semantic HTML (`as="article"`) when appropriate
- Use consistent shadow levels across your app
- Combine with layout utilities (grid, flex) for responsive designs

### ❌ DON'T
- Don't nest hoverable cards (causes double hover effect)
- Don't use extremely large padding (stick to sm/md/lg)
- Don't override core styles (shadow, border-radius) - use variants instead
- Don't make non-interactive cards hoverable
- Don't forget onClick when using hoverable (poor UX)

## Common Patterns

### Grid Layout (Archive/Gallery)
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {items.map(item => (
    <Card key={item.id} hoverable onClick={() => viewItem(item)}>
      <ItemContent {...item} />
    </Card>
  ))}
</div>
```

### Dashboard Stats Grid
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
  <Card><Stat1 /></Card>
  <Card><Stat2 /></Card>
  <Card><Stat3 /></Card>
  <Card><Stat4 /></Card>
</div>
```

### List View
```tsx
<div className="space-y-4">
  {items.map(item => (
    <Card key={item.id} padding="sm" hoverable>
      <ListItemContent {...item} />
    </Card>
  ))}
</div>
```

## Responsive Design

### Mobile-First Approach
```tsx
{/* Single column on mobile, 2 on tablet, 3 on desktop */}
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
  <Card>...</Card>
  <Card>...</Card>
  <Card>...</Card>
</div>
```

### Touch-Friendly Spacing
```tsx
{/* Smaller gaps on mobile for better space usage */}
<div className="grid grid-cols-1 gap-4 md:gap-6">
  <Card>...</Card>
</div>
```

## Browser Support
- ✅ Chrome 90+
- ✅ Safari 14+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Mobile Safari (iOS 14+)
- ✅ Chrome Mobile

## Performance
- Lightweight: ~2KB gzipped
- CSS-only animations (GPU-accelerated)
- No JavaScript for static cards
- Optimized re-renders with React.memo (if needed)

## Testing
```tsx
// Example test
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Card from './Card';

test('calls onClick when clicked', async () => {
  const handleClick = jest.fn();
  render(<Card onClick={handleClick}>Test</Card>);
  
  await userEvent.click(screen.getByText('Test'));
  expect(handleClick).toHaveBeenCalledTimes(1);
});
```

## Related Components
- **StatCard**: Specialized card for dashboard statistics
- **ReceiptCard**: Specialized card for receipt archive display
- **Modal**: For overlay dialogs (uses Card internally)
- **Dropdown**: For popover menus (uses Card shadow levels)

## Changelog
- **v1.0.0** (2024-11-02): Initial release with all core features

## Support
For questions or issues, refer to:
- Design system documentation: `.github/instructions/design_rules_.instructions.md`
- Component guide: `frontend/COMPONENT_GUIDE.md`
- Quick reference: `Card.QUICKREF.md`
