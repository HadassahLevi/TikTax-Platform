# BottomNav Integration Guide

## Quick Integration Checklist

- [ ] Import BottomNav component
- [ ] Add to app layout (after main content)
- [ ] Add bottom padding to main content (`pb-20 md:pb-0`)
- [ ] Create export handler (if using Export button)
- [ ] Ensure all routes exist in React Router
- [ ] Add viewport meta tag for iOS safe area
- [ ] Test on mobile and desktop

---

## Step-by-Step Integration

### Step 1: Update App.tsx (or Main Layout)

```tsx
// File: src/App.tsx
import { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Header, BottomNav } from '@/components/layout';
import './App.css';

// Import your pages
import DashboardPage from '@/pages/DashboardPage';
import ArchivePage from '@/pages/ArchivePage';
import NewReceiptPage from '@/pages/receipts/NewReceiptPage';
import ProfilePage from '@/pages/ProfilePage';

function App() {
  const [isExportModalOpen, setIsExportModalOpen] = useState(false);

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        {/* Desktop Header - hidden on mobile */}
        <Header className="hidden md:block" />
        
        {/* Main Content Area */}
        <main className="pt-0 md:pt-16 pb-20 md:pb-0 min-h-screen">
          {/* 
            pt-0: No top padding on mobile
            md:pt-16: Top padding for Header on desktop (64px)
            pb-20: Bottom padding for BottomNav on mobile (80px)
            md:pb-0: No bottom padding on desktop
          */}
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/archive" element={<ArchivePage />} />
            <Route path="/receipts/new" element={<NewReceiptPage />} />
            <Route path="/profile" element={<ProfilePage />} />
          </Routes>
        </main>
        
        {/* Mobile Bottom Navigation - hidden on desktop */}
        <BottomNav onExportClick={() => setIsExportModalOpen(true)} />

        {/* Export Modal (example) */}
        {isExportModalOpen && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-[100]">
            <div className="bg-white rounded-lg p-6 max-w-md mx-4">
              <h2 className="text-xl font-bold mb-4">ייצוא קבלות</h2>
              <p className="text-gray-600 mb-4">בחר טווח תאריכים לייצוא</p>
              <button
                onClick={() => setIsExportModalOpen(false)}
                className="w-full px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
              >
                סגור
              </button>
            </div>
          </div>
        )}
      </div>
    </BrowserRouter>
  );
}

export default App;
```

---

### Step 2: Update index.html

Add viewport meta tag for iOS safe area support:

```html
<!-- File: index.html -->
<!DOCTYPE html>
<html lang="he" dir="rtl">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
    <!-- ⬆️ viewport-fit=cover is critical for iOS safe area -->
    <title>Tik-Tax</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

---

### Step 3: Create Placeholder Pages (if needed)

If you don't have the pages yet, create placeholders:

```tsx
// File: src/pages/DashboardPage.tsx
export default function DashboardPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">לוח בקרה</h1>
      <p className="text-gray-600">ברוכים הבאים ל-Tik-Tax</p>
    </div>
  );
}
```

```tsx
// File: src/pages/ArchivePage.tsx
export default function ArchivePage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">ארכיון קבלות</h1>
      <p className="text-gray-600">כל הקבלות שלך במקום אחד</p>
    </div>
  );
}
```

```tsx
// File: src/pages/receipts/NewReceiptPage.tsx
export default function NewReceiptPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">קבלה חדשה</h1>
      <p className="text-gray-600">צלם או העלה קבלה</p>
    </div>
  );
}
```

```tsx
// File: src/pages/ProfilePage.tsx
export default function ProfilePage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">פרופיל</h1>
      <p className="text-gray-600">הגדרות המשתמש שלך</p>
    </div>
  );
}
```

---

### Step 4: Alternative - Using Layout Component

For cleaner code, create a Layout component:

```tsx
// File: src/components/layout/Layout.tsx
import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Header, BottomNav } from '@/components/layout';

export const Layout: React.FC = () => {
  const [isExportModalOpen, setIsExportModalOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Desktop Header */}
      <Header className="hidden md:block" />
      
      {/* Main Content */}
      <main className="pt-0 md:pt-16 pb-20 md:pb-0 min-h-screen">
        <Outlet />
      </main>
      
      {/* Mobile Bottom Nav */}
      <BottomNav onExportClick={() => setIsExportModalOpen(true)} />

      {/* Export Modal */}
      {isExportModalOpen && (
        <ExportModal onClose={() => setIsExportModalOpen(false)} />
      )}
    </div>
  );
};
```

Then simplify App.tsx:

```tsx
// File: src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from '@/components/layout/Layout';
import DashboardPage from '@/pages/DashboardPage';
import ArchivePage from '@/pages/ArchivePage';
import NewReceiptPage from '@/pages/receipts/NewReceiptPage';
import ProfilePage from '@/pages/ProfilePage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/archive" element={<ArchivePage />} />
          <Route path="/receipts/new" element={<NewReceiptPage />} />
          <Route path="/profile" element={<ProfilePage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

---

### Step 5: Test the Integration

#### Desktop (≥768px):
1. Open app in browser
2. Resize to desktop width
3. ✅ Header should be visible at top
4. ✅ BottomNav should be hidden
5. ✅ No extra bottom padding on content

#### Mobile (<768px):
1. Open DevTools responsive mode
2. Select iPhone or mobile device
3. ✅ Header should be hidden
4. ✅ BottomNav should be visible at bottom
5. ✅ Center button should be elevated
6. ✅ Content should have bottom padding (not overlapping nav)
7. ✅ Click each nav item to verify routes work
8. ✅ Click Export button to verify callback works

#### Active State:
1. Navigate to /dashboard
2. ✅ Home icon should be blue
3. Navigate to /archive
4. ✅ Archive icon should be blue
5. ✅ Only one item highlighted at a time

#### iOS Device:
1. Open on iPhone
2. ✅ Safe area insets respected (no notch overlap)
3. ✅ Bottom navigation above home indicator

---

## Common Integration Patterns

### Pattern 1: With Authentication

```tsx
import { useAuthStore } from '@/stores/auth.store';
import { Navigate } from 'react-router-dom';

function ProtectedLayout() {
  const { isAuthenticated } = useAuthStore();

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header className="hidden md:block" />
      <main className="pt-0 md:pt-16 pb-20 md:pb-0">
        <Outlet />
      </main>
      <BottomNav onExportClick={handleExport} />
    </div>
  );
}
```

### Pattern 2: Conditional Bottom Nav

Show BottomNav only on certain routes:

```tsx
import { useLocation } from 'react-router-dom';

function Layout() {
  const location = useLocation();
  const showBottomNav = !location.pathname.startsWith('/auth');

  return (
    <div className="min-h-screen bg-gray-50">
      <main className={showBottomNav ? 'pb-20 md:pb-0' : ''}>
        <Outlet />
      </main>
      {showBottomNav && <BottomNav onExportClick={handleExport} />}
    </div>
  );
}
```

### Pattern 3: With Loading State

```tsx
function Layout() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading
    setTimeout(() => setIsLoading(false), 1000);
  }, []);

  if (isLoading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header className="hidden md:block" />
      <main className="pt-0 md:pt-16 pb-20 md:pb-0">
        <Outlet />
      </main>
      <BottomNav onExportClick={handleExport} />
    </div>
  );
}
```

---

## Troubleshooting Integration Issues

### Issue: BottomNav visible on desktop

**Check:**
```tsx
// BottomNav should have md:hidden class (it does by default)
<BottomNav className="md:hidden" />
```

### Issue: Content overlapping BottomNav

**Solution:**
```tsx
// Add bottom padding to main
<main className="pb-20 md:pb-0">
```

### Issue: Routes not working

**Check:**
1. All routes defined in router ✅
2. BrowserRouter wrapping app ✅
3. Route paths match exactly (case-sensitive) ✅

### Issue: Export button not working

**Check:**
```tsx
// Ensure onExportClick prop is passed
<BottomNav onExportClick={() => console.log('Export clicked')} />
```

### Issue: Active state not showing

**Check:**
1. React Router installed ✅
2. Component inside BrowserRouter ✅
3. Route paths match nav items ✅

---

## Next Steps

After integration:

1. **Customize Export Modal**: Replace placeholder with real ExportModal component
2. **Add Loading States**: Show skeletons while pages load
3. **Error Boundaries**: Wrap routes in error boundaries
4. **Analytics**: Track navigation events
5. **Accessibility Test**: Verify with screen reader
6. **Performance**: Measure and optimize

---

## Related Documentation

- `BottomNav.README.md` - Full component documentation
- `BottomNav.QUICKREF.md` - Quick reference guide
- `BottomNav.demo.tsx` - Interactive demo
- `Header.README.md` - Desktop header documentation

---

**Need Help?** Review the demo file or check the Quick Reference!
