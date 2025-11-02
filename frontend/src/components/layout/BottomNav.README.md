# BottomNav Component

## Overview

The `BottomNav` component is a mobile-only bottom navigation bar designed for the Tik-Tax application. It provides easy access to the main app sections with a special elevated center button for the primary action (adding a receipt).

**Key Features:**
- 📱 Mobile-only (automatically hidden on desktop ≥768px)
- ⬆️ Elevated center button for primary action
- ✨ Active route highlighting with smooth transitions
- 🎯 Touch-friendly 48px minimum targets
- 🍎 iOS safe area support
- ♿ Fully accessible (WCAG 2.1 AA)
- 🎨 Follows Tik-Tax design system

---

## Component API

### Props

```typescript
interface BottomNavProps {
  /**
   * Callback function when Export button is clicked
   * Typically used to open an export modal
   */
  onExportClick?: () => void;
  
  /**
   * Additional CSS classes to apply to the nav container
   */
  className?: string;
}
```

### Navigation Items

The component includes 5 navigation items by default:

| Position | Icon | Label (Hebrew) | Route | Type |
|----------|------|----------------|-------|------|
| 1 | Home | בית | `/dashboard` | Link |
| 2 | FolderOpen | ארכיון | `/archive` | Link |
| 3 (Center) | Plus | - | `/receipts/new` | Link (Elevated) |
| 4 | Download | ייצוא | - | Button (onClick) |
| 5 | User | פרופיל | `/profile` | Link |

---

## Usage

### Basic Implementation

```tsx
import { BottomNav } from '@/components/layout';

function App() {
  return (
    <>
      <main className="pb-20 md:pb-0">
        {/* Your page content */}
      </main>
      
      <BottomNav />
    </>
  );
}
```

### With Export Handler

```tsx
import { BottomNav } from '@/components/layout';
import { useState } from 'react';

function App() {
  const [isExportOpen, setIsExportOpen] = useState(false);

  return (
    <>
      <main className="pb-20 md:pb-0">
        {/* Page content */}
      </main>
      
      <BottomNav onExportClick={() => setIsExportOpen(true)} />
      
      {/* Export Modal */}
      {isExportOpen && (
        <ExportModal onClose={() => setIsExportOpen(false)} />
      )}
    </>
  );
}
```

### Complete Layout Example

```tsx
import { Header, BottomNav } from '@/components/layout';
import { Outlet } from 'react-router-dom';

function Layout() {
  const [isExportOpen, setIsExportOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Desktop Header */}
      <Header className="hidden md:block" />
      
      {/* Main Content */}
      <main className="pt-0 md:pt-16 pb-20 md:pb-0">
        <Outlet />
      </main>
      
      {/* Mobile Bottom Navigation */}
      <BottomNav onExportClick={() => setIsExportOpen(true)} />
    </div>
  );
}
```

---

## Design Specifications

### Container

```css
Position:     fixed bottom-0
Width:        100%
Height:       64px
Background:   #FFFFFF
Border Top:   1px solid #E5E7EB
Shadow:       0 -2px 8px rgba(0, 0, 0, 0.08)
Z-Index:      50
Padding:      env(safe-area-inset-bottom) /* iOS notch support */
```

### Regular Navigation Items

```css
Display:          flex-column (icon above label)
Icon Size:        24px
Label Font:       12px, weight 500
Gap:              4px
Min Touch Size:   48px × 48px
Padding:          8px 12px

Colors:
  Inactive:       #6B7280 (text-gray-500)
  Active:         #2563EB (text-primary-600)
  Hover:          #374151 (text-gray-700)

Transitions:
  Color:          200ms ease
  Transform:      200ms ease (icon scales to 110% when active)
```

### Center Button (Add Receipt)

```css
Position:     absolute, -20px from top
Size:         64px × 64px
Background:   linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%)
Border:       none
Radius:       50% (full circle)
Shadow:       0 4px 12px rgba(37, 99, 235, 0.4)
Icon Size:    28px
Color:        #FFFFFF

States:
  Hover:        scale(1.05)
  Active:       scale(0.95)
  Focus:        2px ring #2563EB, offset 2px

Transition:   all 200ms ease-in-out
```

---

## Features Explained

### 1. Mobile-Only Visibility

The component uses Tailwind's responsive classes to hide on desktop:

```tsx
className="md:hidden"  // Hidden on screens ≥768px
```

Ensure your desktop header is hidden on mobile:

```tsx
<Header className="hidden md:block" />
```

### 2. Active Route Highlighting

Uses React Router's `useLocation()` hook to detect the current route:

```typescript
const location = useLocation();
const isActive = (route: string) => location.pathname === route;
```

Active items get:
- Primary blue color (#2563EB)
- Icon scales to 110%
- Semi-bold label (weight 600)
- `aria-current="page"` attribute

### 3. Elevated Center Button

The center "Add Receipt" button is visually elevated:

```typescript
className="absolute left-1/2 -translate-x-1/2 -top-5"
```

This creates a floating effect 20px above the nav bar.

**Why elevated?**
- Draws attention to primary action
- Follows iOS design patterns
- Improves discoverability
- Creates visual hierarchy

### 4. iOS Safe Area Support

The component includes padding for iPhone notches:

```css
padding-bottom: env(safe-area-inset-bottom);
```

**Required:** Ensure your `index.html` has:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
```

### 5. Touch-Friendly Targets

All navigation items meet the 48px minimum touch target size:

```tsx
className="min-w-[48px] min-h-[48px]"
```

This ensures easy tapping on mobile devices.

### 6. Accessibility

**ARIA Attributes:**
- `role="navigation"` on container
- `aria-label` on all buttons
- `aria-current="page"` for active links
- Proper semantic HTML (nav, button, Link)

**Keyboard Navigation:**
- Tab through items
- Enter/Space to activate
- Focus indicators visible

---

## Layout Considerations

### Content Padding

**Critical:** Add bottom padding to your main content to prevent overlap:

```tsx
<main className="pb-20 md:pb-0">
  {/* pb-20 (80px) on mobile for BottomNav */}
  {/* pb-0 on desktop where BottomNav is hidden */}
</main>
```

**Why 80px (pb-20)?**
- 64px nav height
- 16px comfortable spacing
- Total: 80px

### With Fixed Header

If you have both Header and BottomNav:

```tsx
<main className="pt-16 pb-20 md:pb-0">
  {/* pt-16: Top padding for Header */}
  {/* pb-20: Bottom padding for BottomNav (mobile) */}
  {/* md:pb-0: Remove bottom padding on desktop */}
</main>
```

### Z-Index Stacking

Default z-index hierarchy:

```
BottomNav:      z-50
Modal/Overlay:  z-[100] or higher
Dropdown:       z-[60] or similar
```

Adjust if needed:

```tsx
<BottomNav className="z-[60]" />
```

---

## Customization

### Changing Navigation Items

Edit the `navItems` array in `BottomNav.tsx`:

```typescript
const navItems: NavItem[] = [
  {
    id: 'home',
    label: 'בית',
    icon: <Home className="w-6 h-6" />,
    route: '/dashboard',
  },
  // Add more items...
];
```

### Adding Badge/Notification

Extend the `NavItem` interface:

```typescript
interface NavItem {
  // ... existing props
  badge?: number;  // New prop
}
```

Then render conditionally:

```tsx
{item.badge && (
  <span className="absolute top-0 right-0 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
    {item.badge}
  </span>
)}
```

### Custom Colors

Override Tailwind classes:

```tsx
<BottomNav className="bg-gray-900 border-gray-800" />
```

Or modify in the component:

```typescript
// Change active color
active ? 'text-success-600' : 'text-gray-500'

// Change center button gradient
'bg-gradient-to-br from-success-600 to-success-700'
```

---

## Routing Setup

Ensure all routes referenced by BottomNav exist in your router:

```tsx
import { createBrowserRouter } from 'react-router-dom';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      {
        path: 'dashboard',
        element: <DashboardPage />,
      },
      {
        path: 'archive',
        element: <ArchivePage />,
      },
      {
        path: 'receipts/new',
        element: <NewReceiptPage />,
      },
      {
        path: 'profile',
        element: <ProfilePage />,
      },
    ],
  },
]);
```

---

## Performance

### Bundle Impact
- Component size: ~2KB gzipped
- No external dependencies beyond React Router and lucide-react
- CSS is utility-based (Tailwind), already in bundle

### Optimization
- Uses CSS transitions (hardware-accelerated)
- `touch-manipulation` for better mobile performance
- No unnecessary re-renders (stable component)

### Rendering
- Only re-renders on route change (via `useLocation`)
- Icons are SVG (small, scalable)

---

## Browser Support

| Browser | Version | Support |
|---------|---------|---------|
| Chrome Mobile | 90+ | ✅ Full |
| Safari iOS | 14+ | ✅ Full (with safe-area) |
| Firefox Mobile | 88+ | ✅ Full |
| Samsung Internet | 15+ | ✅ Full |
| Chrome Desktop | Any | ✅ Hidden via responsive classes |
| Safari Desktop | Any | ✅ Hidden via responsive classes |

---

## Troubleshooting

### Issue: Navigation overlaps content

**Solution:** Add bottom padding to main content:

```tsx
<main className="pb-20 md:pb-0">
```

### Issue: Center button not visible

**Possible causes:**
1. Z-index conflict → Increase BottomNav z-index
2. Parent has `overflow: hidden` → Remove or adjust
3. Wrong positioning → Check for conflicting CSS

### Issue: Active state not highlighting

**Possible causes:**
1. Route mismatch → Routes are case-sensitive, check exact match
2. Router not set up → Ensure React Router is configured
3. Location hook failing → Verify BrowserRouter wraps component

### Issue: iOS safe area not working

**Solution:** Add to `index.html`:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
```

### Issue: Touch targets feel too small

**Solution:** The component already uses `min-w-[48px] min-h-[48px]`. If still too small, increase:

```tsx
className="min-w-[56px] min-h-[56px]"
```

---

## Testing

### Manual Testing Checklist

- [ ] Component visible on mobile (<768px)
- [ ] Component hidden on desktop (≥768px)
- [ ] Center button elevated and clickable
- [ ] Active route highlighted correctly
- [ ] All navigation links work
- [ ] Export button triggers callback
- [ ] Smooth transitions on state changes
- [ ] No content overlap (proper padding)
- [ ] iOS safe area working on iPhone
- [ ] Touch targets easy to tap
- [ ] Accessibility: keyboard navigation works
- [ ] Accessibility: screen reader announces items

### Device Testing

Test on:
- iPhone SE (small screen)
- iPhone 14 Pro (notch)
- Android phone (various sizes)
- Tablet (iPad mini)

---

## Design System Compliance

✅ **Colors**: Uses Tik-Tax color palette  
✅ **Typography**: 12px labels, proper font weights  
✅ **Spacing**: 8-point grid system (8px, 12px, 16px)  
✅ **Shadows**: Design system elevation levels  
✅ **Transitions**: 200ms standard timing  
✅ **Touch Targets**: 48px minimum (meets WCAG)  
✅ **Accessibility**: WCAG 2.1 AA compliant  
✅ **Responsive**: Mobile-first approach  

---

## Related Components

- **Header**: Desktop navigation (pair with BottomNav)
- **MobileMenu**: Alternative mobile nav (hamburger menu)
- **UserDropdown**: User profile menu (used in Header)

---

## Future Enhancements

Potential improvements for Phase 2:

1. **Badge Support**: Notification badges on icons
2. **Haptic Feedback**: Vibration on tap (mobile)
3. **Swipe Gestures**: Swipe between tabs
4. **Animation**: More sophisticated transitions
5. **Theming**: Dark mode support
6. **Customization**: User can rearrange items

---

## Migration Guide

If migrating from a different navigation system:

1. **Install Dependencies** (if not already):
   ```bash
   npm install react-router-dom lucide-react
   ```

2. **Update Routes**: Ensure all nav routes exist in router

3. **Add Padding**: Update main content container:
   ```tsx
   <main className="pb-20 md:pb-0">
   ```

4. **Hide Old Nav**: Remove/hide old mobile navigation

5. **Import Component**:
   ```tsx
   import { BottomNav } from '@/components/layout';
   ```

6. **Add to Layout**:
   ```tsx
   <BottomNav onExportClick={handleExport} />
   ```

7. **Test**: Verify on mobile and desktop

---

## Support

**Questions?** Check:
- Quick Reference: `BottomNav.QUICKREF.md`
- Demo: `BottomNav.demo.tsx`
- Design System: `.github/instructions/design_rules_.instructions.md`

**Issues?** Review Troubleshooting section above.

---

**Component Version:** 1.0  
**Last Updated:** November 2024  
**Author:** Tik-Tax Development Team
