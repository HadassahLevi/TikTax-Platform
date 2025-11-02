# BottomNav - 5-Minute Setup Guide

## 🚀 Quick Start (Copy-Paste Ready)

### Step 1: Import Component (30 seconds)

```tsx
// In your App.tsx or Layout.tsx
import { BottomNav } from '@/components/layout';
import { useState } from 'react';
```

### Step 2: Add to Layout (1 minute)

```tsx
function App() {
  const [exportOpen, setExportOpen] = useState(false);

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        {/* Desktop Header - hide on mobile */}
        <Header className="hidden md:block" />
        
        {/* Main Content - add bottom padding for mobile */}
        <main className="pt-0 md:pt-16 pb-20 md:pb-0">
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/archive" element={<ArchivePage />} />
            <Route path="/receipts/new" element={<NewReceiptPage />} />
            <Route path="/profile" element={<ProfilePage />} />
          </Routes>
        </main>
        
        {/* Mobile Bottom Navigation */}
        <BottomNav onExportClick={() => setExportOpen(true)} />
      </div>
    </BrowserRouter>
  );
}
```

### Step 3: Update index.html (30 seconds)

```html
<!-- Add viewport-fit=cover for iOS safe area -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
```

### Step 4: Test (2 minutes)

1. Open browser DevTools
2. Toggle responsive mode
3. Select mobile device (<768px)
4. ✅ BottomNav visible at bottom
5. ✅ Click each nav item
6. ✅ Active state highlights correctly

---

## ⚡ Essential Classes

```tsx
// Desktop Header
<Header className="hidden md:block" />

// Main Content
<main className="pt-0 md:pt-16 pb-20 md:pb-0">

// BottomNav (already includes md:hidden)
<BottomNav onExportClick={handleExport} />
```

---

## 📋 Navigation Routes Checklist

- [ ] `/dashboard` - Dashboard page exists
- [ ] `/archive` - Archive page exists
- [ ] `/receipts/new` - New receipt page exists
- [ ] `/profile` - Profile page exists
- [ ] Export handler defined (for Export button)

---

## 🎨 What You Get

```
Mobile View (<768px):
┌─────────────────────────────────┐
│                                 │
│      Page Content Here          │
│                                 │
├─────────────────────────────────┤
│           [+]                   │ ← Elevated center button
│  🏠   📁        💾    👤        │ ← Bottom navigation
│ בית  ארכיון    ייצוא  פרופיל   │
└─────────────────────────────────┘

Desktop View (≥768px):
┌─────────────────────────────────┐
│  Logo    Nav Links    Profile   │ ← Header only
├─────────────────────────────────┤
│                                 │
│      Page Content Here          │
│                                 │
└─────────────────────────────────┘
         (BottomNav hidden)
```

---

## ✅ Done! That's It!

**Time**: ~5 minutes  
**Complexity**: Minimal  
**Result**: Professional mobile navigation

---

## 🔧 Troubleshooting (30 seconds each)

| Issue | Fix |
|-------|-----|
| Nav overlaps content | Add `pb-20` to `<main>` |
| Nav visible on desktop | Component has `md:hidden` by default ✅ |
| Active state not working | Check route paths match exactly |
| Export button doesn't work | Pass `onExportClick` prop |

---

## 📖 Full Documentation

- **Quick Ref**: `BottomNav.QUICKREF.md`
- **Full Docs**: `BottomNav.README.md`
- **Integration**: `BottomNav.INTEGRATION.md`
- **Demo**: `BottomNav.demo.tsx`

---

**That's it! Your mobile navigation is ready! 🎉**
