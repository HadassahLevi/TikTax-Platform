# BottomNav Quick Reference

## Import
```tsx
import { BottomNav } from '@/components/layout';
```

## Basic Usage
```tsx
function App() {
  const [isExportModalOpen, setIsExportModalOpen] = useState(false);

  return (
    <>
      {/* Your page content */}
      <main className="pb-20"> {/* Add padding for BottomNav */}
        {/* Page content here */}
      </main>

      {/* Bottom Navigation */}
      <BottomNav onExportClick={() => setIsExportModalOpen(true)} />
    </>
  );
}
```

## Props
```tsx
interface BottomNavProps {
  onExportClick?: () => void;  // Callback for export button
  className?: string;           // Additional CSS classes
}
```

## Navigation Items

| Icon | Label | Route | Action |
|------|-------|-------|--------|
| Home | בית | `/dashboard` | Navigate to dashboard |
| FolderOpen | ארכיון | `/archive` | Navigate to archive |
| Plus (elevated) | - | `/receipts/new` | Add new receipt |
| Download | ייצוא | - | Trigger export modal |
| User | פרופיל | `/profile` | Navigate to profile |

## Features

### ✅ Mobile-Only Display
- Visible: `<768px` (mobile/tablet)
- Hidden: `≥768px` (desktop)

### ✅ Elevated Center Button
- 64px diameter circle
- Gradient background (primary blue)
- Positioned 20px above nav bar
- Large shadow for depth
- Hover: scale(1.05)
- Active: scale(0.95)

### ✅ Active State Highlighting
- Uses `useLocation()` to detect current route
- Active color: Primary blue (#2563EB)
- Inactive color: Gray (#6B7280)
- Icon scales up when active (110%)
- Label becomes semi-bold when active

### ✅ Touch-Friendly
- Minimum touch target: 48px × 48px
- Touch manipulation CSS for better mobile performance
- Smooth transitions (200ms)

### ✅ iOS Safe Area Support
- Automatic padding for iPhone notch
- Uses `env(safe-area-inset-bottom)`

### ✅ Accessibility
- `role="navigation"`
- ARIA labels on all buttons
- `aria-current="page"` for active items
- Keyboard accessible

## Styling Details

### Container
```css
position: fixed;
bottom: 0;
height: 64px;
background: white;
border-top: 1px solid #E5E7EB;
box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.08);
z-index: 50;
```

### Center Button
```css
position: absolute;
top: -20px;
width: 64px;
height: 64px;
background: linear-gradient(135deg, #2563EB, #1D4ED8);
box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
border-radius: 50%;
```

### Regular Items
```css
display: flex;
flex-direction: column;
gap: 4px;
font-size: 12px;
font-weight: 500;
min-width: 48px;
min-height: 48px;
```

## Layout Considerations

### Page Padding
Add bottom padding to your main content to prevent overlap:

```tsx
<main className="pb-20 md:pb-0">
  {/* pb-20 on mobile, pb-0 on desktop */}
  {/* Your content */}
</main>
```

### With Header
```tsx
function Layout() {
  return (
    <>
      <Header /> {/* Desktop header */}
      <main className="pt-16 pb-20 md:pb-0">
        {/* pt-16 for header, pb-20 for BottomNav */}
        <Outlet />
      </main>
      <BottomNav onExportClick={handleExport} />
    </>
  );
}
```

## Route Configuration

Ensure these routes exist in your React Router setup:

```tsx
const router = createBrowserRouter([
  {
    path: '/dashboard',
    element: <DashboardPage />,
  },
  {
    path: '/archive',
    element: <ArchivePage />,
  },
  {
    path: '/receipts/new',
    element: <NewReceiptPage />,
  },
  {
    path: '/profile',
    element: <ProfilePage />,
  },
]);
```

## Customization Examples

### Custom Export Handler
```tsx
const handleExport = () => {
  console.log('Export clicked');
  // Open modal, trigger download, etc.
};

<BottomNav onExportClick={handleExport} />
```

### With Additional Classes
```tsx
<BottomNav 
  onExportClick={handleExport}
  className="custom-class"
/>
```

## Common Patterns

### Complete App Layout
```tsx
function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        {/* Desktop Navigation */}
        <Header className="hidden md:block" />
        
        {/* Main Content with proper padding */}
        <main className="pt-0 md:pt-16 pb-20 md:pb-0">
          <Routes>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/archive" element={<Archive />} />
            <Route path="/receipts/new" element={<NewReceipt />} />
            <Route path="/profile" element={<Profile />} />
          </Routes>
        </main>
        
        {/* Mobile Navigation */}
        <BottomNav onExportClick={() => setExportOpen(true)} />
      </div>
    </BrowserRouter>
  );
}
```

## Design System Compliance

✅ **Colors**: Primary blue (#2563EB), Gray scale  
✅ **Typography**: 12px labels, weight 500/600  
✅ **Spacing**: 8px grid system  
✅ **Shadows**: Design system elevation levels  
✅ **Transitions**: 200ms standard timing  
✅ **Touch Targets**: 48px minimum  
✅ **Accessibility**: WCAG 2.1 AA compliant  

## Browser Support

- ✅ Chrome Mobile (90+)
- ✅ Safari iOS (14+)
- ✅ Chrome Desktop (hidden via responsive classes)
- ✅ Safari Desktop (hidden via responsive classes)
- ✅ Firefox Mobile (88+)

## Performance Notes

- Uses `touch-manipulation` for better mobile performance
- CSS transitions (hardware-accelerated)
- No unnecessary re-renders (stable component)
- Small bundle impact (~2KB gzipped)

## Troubleshooting

### Issue: Navigation overlaps content
**Solution**: Add `pb-20` to your main content container

### Issue: Center button not visible
**Solution**: Check z-index stacking, ensure parent has `relative` positioning

### Issue: Active state not highlighting
**Solution**: Verify routes match exactly (case-sensitive)

### Issue: iOS safe area not working
**Solution**: Ensure viewport meta tag includes `viewport-fit=cover`

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
```
