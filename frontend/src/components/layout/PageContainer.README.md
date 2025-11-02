# PageContainer Component

**Professional page wrapper for consistent layouts with loading states**

---

## Overview

The `PageContainer` component provides a standardized wrapper for all pages in the Tik-Tax application. It handles:

- ✅ Consistent max-width constraints and padding
- ✅ Responsive design across all breakpoints
- ✅ Optional title/subtitle header with action buttons
- ✅ Built-in loading states with skeleton loaders
- ✅ Smooth animations and transitions
- ✅ Automatic scroll-to-top behavior
- ✅ Mobile-first approach
- ✅ RTL support for Hebrew
- ✅ Accessibility compliance (WCAG 2.1 AA)

---

## Design Philosophy

Following the Tik-Tax design system:

1. **Consistency** - Every page has the same structure and spacing
2. **Simplicity** - One component to rule them all
3. **Performance** - Optimized animations and minimal re-renders
4. **Accessibility** - Semantic HTML and ARIA labels
5. **Mobile-First** - Designed for mobile, enhanced for desktop

---

## Installation

The component is already available in the layout components:

```tsx
import { PageContainer } from '@/components/layout';
```

**Dependencies:**
- `framer-motion` - Animations
- `lucide-react` - Icons (loading spinner)
- `@/utils/formatters` - Class name utilities

---

## Basic Usage

### Minimal Example

```tsx
<PageContainer>
  <p>Hello World</p>
</PageContainer>
```

### With Title

```tsx
<PageContainer title="לוח בקרה">
  <Dashboard />
</PageContainer>
```

### With Title, Subtitle, and Action

```tsx
<PageContainer 
  title="ארכיון קבלות"
  subtitle="כל הקבלות שלך במקום אחד"
  action={<Button>הוסף קבלה</Button>}
>
  <ReceiptGrid />
</PageContainer>
```

---

## Props API

### PageContainerProps

```tsx
interface PageContainerProps {
  children: React.ReactNode;
  loading?: boolean;
  title?: string;
  subtitle?: string;
  action?: React.ReactNode;
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  noPadding?: boolean;
  className?: string;
}
```

#### `children` (required)
- **Type:** `React.ReactNode`
- **Description:** Page content to display

#### `loading`
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Shows skeleton loader and spinner overlay when `true`

#### `title`
- **Type:** `string`
- **Optional:** Yes
- **Description:** Page title displayed in header (H1)

#### `subtitle`
- **Type:** `string`
- **Optional:** Yes
- **Description:** Page description below title

#### `action`
- **Type:** `React.ReactNode`
- **Optional:** Yes
- **Description:** Action button(s) or elements displayed in header (right side on LTR, left side on RTL)

#### `maxWidth`
- **Type:** `'sm' | 'md' | 'lg' | 'xl' | 'full'`
- **Default:** `'md'`
- **Description:** Maximum width constraint

**Variants:**
- `sm` - 640px (forms, settings)
- `md` - 880px (default, most pages)
- `lg` - 1200px (grids, archives)
- `xl` - 1440px (dashboards)
- `full` - 100% (custom layouts)

#### `noPadding`
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Disables default responsive padding

#### `className`
- **Type:** `string`
- **Optional:** Yes
- **Description:** Additional CSS classes for customization

---

## Loading States

### Using the Built-in Loading Prop

```tsx
const [loading, setLoading] = useState(true);

useEffect(() => {
  fetchData().finally(() => setLoading(false));
}, []);

<PageContainer title="נתונים" loading={loading}>
  <DataDisplay />
</PageContainer>
```

**When `loading={true}`:**
- ✅ Shows title skeleton (if title provided)
- ✅ Shows content skeleton (default cards)
- ✅ Displays centered spinner overlay
- ✅ Dims content (60% opacity)
- ✅ Disables interactions

---

## Skeleton Loaders

### Built-in Skeletons

The package includes ready-to-use skeleton components:

#### GridSkeleton

```tsx
import { GridSkeleton } from '@/components/layout';

<GridSkeleton count={6} />
```

**Use for:** Card grids, image galleries  
**Layout:** Responsive grid (1 → 2 → 3 columns)

#### ListSkeleton

```tsx
import { ListSkeleton } from '@/components/layout';

<ListSkeleton count={5} />
```

**Use for:** Transaction lists, table rows  
**Layout:** Vertical stack with avatar + text

#### StatsSkeleton

```tsx
import { StatsSkeleton } from '@/components/layout';

<StatsSkeleton />
```

**Use for:** Dashboard metrics  
**Layout:** 4 stat cards in responsive grid

#### FormSkeleton

```tsx
import { FormSkeleton } from '@/components/layout';

<FormSkeleton />
```

**Use for:** Forms, input-heavy pages  
**Layout:** 4 fields + 2 buttons

### Custom Loading Pattern

```tsx
<PageContainer title="תוצאות">
  {loading ? (
    <GridSkeleton count={9} />
  ) : (
    <ResultsGrid data={data} />
  )}
</PageContainer>
```

---

## Responsive Design

### Breakpoints

| Breakpoint | Range | Padding | Title Size |
|------------|-------|---------|------------|
| **Mobile** | < 640px | 16px | 28px |
| **Tablet** | 640px - 1024px | 24px | 32px |
| **Desktop** | > 1024px | 32px | 32px |

### Layout Behavior

**Mobile (< 640px):**
- Single column
- Actions stack below title
- Full-width buttons
- Touch-friendly spacing

**Tablet (640px - 1024px):**
- Actions inline with title
- Increased padding
- Better use of space

**Desktop (> 1024px):**
- Maximum padding
- Actions always inline
- Centered with max-width constraint

---

## Advanced Usage

### Multiple Actions

```tsx
<PageContainer 
  title="ניהול קבלות"
  action={
    <div className="flex gap-3">
      <Button variant="secondary" icon={<Download />}>
        ייצוא
      </Button>
      <Button variant="primary" icon={<Plus />}>
        הוסף
      </Button>
    </div>
  }
>
  <ReceiptManager />
</PageContainer>
```

### Conditional Actions

```tsx
<PageContainer 
  title="בחירת קבלות"
  action={selectedCount > 0 && (
    <Button variant="danger" icon={<Trash />}>
      מחק ({selectedCount})
    </Button>
  )}
>
  <SelectableList />
</PageContainer>
```

### Full-Width Custom Layout

```tsx
<PageContainer maxWidth="full" noPadding>
  <div className="custom-layout">
    <Sidebar />
    <MainContent />
  </div>
</PageContainer>
```

### Custom Styling

```tsx
<PageContainer 
  title="דוח חודשי"
  className="bg-gray-50 min-h-screen"
>
  <Report />
</PageContainer>
```

---

## Accessibility

### Built-in Features

- ✅ Semantic HTML (`<h1>` for title)
- ✅ ARIA labels on loading overlay
- ✅ `role="status"` for loading state
- ✅ `aria-live="polite"` for updates
- ✅ Proper heading hierarchy
- ✅ Keyboard navigation support

### Best Practices

```tsx
// ✅ Good - Descriptive title
<PageContainer title="ארכיון קבלות מ-2024">
  <Archive />
</PageContainer>

// ❌ Bad - Generic title
<PageContainer title="דף">
  <Archive />
</PageContainer>

// ✅ Good - Clear loading message
<PageContainer title="טוען קבלות..." loading>
  <Content />
</PageContainer>
```

---

## Performance

### Optimizations

1. **Framer Motion** - GPU-accelerated animations
2. **Lazy Loading** - Children only rendered when not loading
3. **Memoization** - Skeleton components prevent re-renders
4. **CSS Animations** - Pulse effect uses CSS, not JS

### Animation Timing

- **Page fade-in:** 300ms ease-out
- **Content reveal:** 200ms with 100ms delay
- **Skeleton pulse:** 1.5s infinite loop

---

## Common Patterns

### Dashboard Page

```tsx
// src/pages/Dashboard.tsx
<PageContainer title="לוח בקרה" maxWidth="xl">
  <div className="space-y-6">
    <StatsRow />
    <ChartsSection />
    <RecentActivity />
  </div>
</PageContainer>
```

### Archive with Filters

```tsx
// src/pages/Archive.tsx
<PageContainer 
  title="ארכיון קבלות"
  action={
    <div className="flex gap-3">
      <SearchInput />
      <FilterDropdown />
    </div>
  }
  maxWidth="lg"
>
  <ReceiptGrid />
</PageContainer>
```

### Settings Form

```tsx
// src/pages/Settings.tsx
<PageContainer 
  title="הגדרות"
  subtitle="נהל את הפרופיל והעדפות שלך"
  maxWidth="sm"
>
  <SettingsForm />
</PageContainer>
```

### Empty State

```tsx
// src/pages/EmptyReceipts.tsx
<PageContainer title="אין לך קבלות עדיין">
  <EmptyState 
    icon={<Receipt />}
    title="התחל להוסיף קבלות"
    action={<Button>העלה קבלה ראשונה</Button>}
  />
</PageContainer>
```

---

## Troubleshooting

### Issue: Header not showing

**Problem:** Title missing even though prop provided  
**Solution:** Check if `title` is actually a string and not undefined

```tsx
// ❌ Bad
<PageContainer title={undefined}>

// ✅ Good
<PageContainer title="כותרת">
```

### Issue: Content too narrow

**Problem:** Default max-width too small  
**Solution:** Increase `maxWidth` prop

```tsx
// Change from default (md - 880px)
<PageContainer maxWidth="lg"> {/* 1200px */}
```

### Issue: Unwanted padding

**Problem:** Custom layout needs full control  
**Solution:** Use `noPadding` prop

```tsx
<PageContainer noPadding>
  <CustomLayout />
</PageContainer>
```

### Issue: Loading state not working

**Problem:** Content still visible during loading  
**Solution:** Check boolean value and use controlled pattern

```tsx
const [loading, setLoading] = useState(true);

<PageContainer loading={loading}> {/* Ensure boolean */}
```

### Issue: Actions not aligned

**Problem:** Actions wrapping on mobile  
**Solution:** Wrap multiple actions in flex container

```tsx
<PageContainer 
  action={
    <div className="flex gap-3 flex-wrap">
      {/* actions */}
    </div>
  }
>
```

---

## Migration Guide

### From Raw div to PageContainer

**Before:**
```tsx
<div className="max-w-4xl mx-auto px-4 py-8">
  <h1 className="text-3xl font-bold mb-6">כותרת</h1>
  <Content />
</div>
```

**After:**
```tsx
<PageContainer title="כותרת" maxWidth="lg">
  <Content />
</PageContainer>
```

### From Custom Loading to PageContainer

**Before:**
```tsx
{loading ? (
  <div className="flex items-center justify-center min-h-screen">
    <Spinner />
  </div>
) : (
  <div className="max-w-4xl mx-auto p-8">
    <Content />
  </div>
)}
```

**After:**
```tsx
<PageContainer loading={loading}>
  <Content />
</PageContainer>
```

---

## TypeScript Support

### Type Imports

```tsx
import { PageContainerProps } from '@/components/layout';

const MyPage: React.FC<PageContainerProps> = (props) => {
  return <PageContainer {...props} />;
};
```

### Extending Props

```tsx
interface CustomPageProps extends PageContainerProps {
  customProp: string;
}

const CustomPage: React.FC<CustomPageProps> = ({ customProp, ...rest }) => {
  return (
    <PageContainer {...rest}>
      <div>{customProp}</div>
    </PageContainer>
  );
};
```

---

## Testing

### Example Test

```tsx
import { render, screen } from '@testing-library/react';
import { PageContainer } from './PageContainer';

describe('PageContainer', () => {
  it('renders title when provided', () => {
    render(<PageContainer title="Test Title"><div /></PageContainer>);
    expect(screen.getByText('Test Title')).toBeInTheDocument();
  });

  it('shows loading spinner when loading', () => {
    render(<PageContainer loading><div /></PageContainer>);
    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('renders action buttons', () => {
    render(
      <PageContainer action={<button>Action</button>}>
        <div />
      </PageContainer>
    );
    expect(screen.getByText('Action')).toBeInTheDocument();
  });
});
```

---

## Changelog

### Version 1.0.0 (2025-11-02)
- ✨ Initial release
- ✅ Responsive design (mobile-first)
- ✅ Loading states with skeletons
- ✅ Title/subtitle/action support
- ✅ Max-width variants (sm, md, lg, xl, full)
- ✅ Smooth animations with framer-motion
- ✅ Accessibility compliance
- ✅ TypeScript support
- ✅ RTL support for Hebrew

---

## Related Components

- **Header** - App-wide header with logo and navigation
- **BottomNav** - Mobile bottom navigation
- **Card** - Content containers within pages
- **Button** - Action buttons in header
- **Modal** - Overlay dialogs (not for page content)

---

## License

Part of the Tik-Tax design system.  
For internal use only.

---

**Questions?** Check the demo file: `PageContainer.demo.tsx`  
**Quick Reference:** See `PageContainer.QUICKREF.md`
