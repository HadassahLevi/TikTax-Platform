# Empty States & Error Pages - Quick Reference

## 🚀 Quick Start

### Using EmptyState Component

```typescript
import { EmptyState } from '@/components/EmptyState';
import { Receipt } from 'lucide-react';

<EmptyState
  icon={Receipt}
  title="כותרת"
  description="תיאור"
  actionLabel="פעולה ראשית"
  onAction={() => {}}
  secondaryLabel="פעולה משנית" // optional
  onSecondaryAction={() => {}}  // optional
/>
```

---

## 📄 Error Pages Routes

| Route | Component | When to Use |
|-------|-----------|-------------|
| `/error/500` | ServerErrorPage | Server returns 500+ status |
| `/error/network` | NetworkErrorPage | No internet connection |
| `/maintenance` | MaintenancePage | Server returns 503 status |
| `*` (any) | NotFoundPage | Invalid route (404) |

---

## 🎨 Common Empty State Patterns

### 1. No Data at All
```typescript
<EmptyState
  icon={Receipt}
  title="אין נתונים"
  description="התחל על ידי הוספת פריט ראשון"
  actionLabel="הוסף כעת"
  onAction={handleAdd}
/>
```

### 2. No Search Results
```typescript
<EmptyState
  icon={Search}
  title="לא נמצאו תוצאות"
  description={`אין תוצאות עבור "${query}"`}
  actionLabel="נקה חיפוש"
  onAction={() => setQuery('')}
/>
```

### 3. No Filter Results
```typescript
<EmptyState
  icon={Filter}
  title="אין תוצאות לפילטר זה"
  description="נסה לשנות את הפילטרים"
  actionLabel="נקה פילטרים"
  onAction={clearFilters}
/>
```

### 4. Permission Denied
```typescript
<EmptyState
  icon={Lock}
  title="אין הרשאה"
  description="אין לך גישה לתוכן זה"
  actionLabel="חזור לדף הבית"
  onAction={() => navigate('/')}
/>
```

---

## 🔧 Axios Error Handling

Errors are **automatically handled** by axios interceptor:

- **Network Error** → Redirects to `/error/network`
- **500+ Status** → Redirects to `/error/500`
- **503 Status** → Redirects to `/maintenance`

No manual handling needed!

---

## 📱 Responsive Behavior

| Screen | Layout |
|--------|--------|
| Mobile (< 640px) | Full-width buttons, stacked content |
| Tablet (640-1024px) | Centered with padding |
| Desktop (> 1024px) | Max-width 1200px, centered |

---

## ♿ Accessibility

All components include:
- ✅ Semantic HTML
- ✅ ARIA labels
- ✅ Keyboard navigation
- ✅ Focus indicators
- ✅ WCAG 2.1 AA contrast

---

## 🧪 Testing URLs

```bash
# 404 Page
http://localhost:5173/does-not-exist

# 500 Page (needs backend mock)
http://localhost:5173/error/500

# Network Page (needs offline)
http://localhost:5173/error/network

# Maintenance Page (needs backend mock)
http://localhost:5173/maintenance
```

---

## 📦 Icon Reference

Common icons from `lucide-react`:

```typescript
import {
  Receipt,        // Receipts, documents
  Search,         // Search results
  Filter,         // Filter results
  Lock,           // Permission denied
  AlertCircle,    // Warnings
  CheckCircle,    // Success
  FileQuestion,   // 404
  ServerCrash,    // 500
  WifiOff,        // Network
  Construction,   // Maintenance
  ShoppingBag,    // Shopping/purchases
  Users,          // Team/people
  Calendar,       // Dates/events
  Settings        // Configuration
} from 'lucide-react';
```

---

## 🎯 Props Reference

### EmptyState Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `icon` | LucideIcon | Yes | Icon component |
| `title` | string | Yes | Main heading |
| `description` | string | Yes | Supporting text |
| `actionLabel` | string | No | Primary button text |
| `onAction` | () => void | No | Primary button callback |
| `secondaryLabel` | string | No | Secondary button text |
| `onSecondaryAction` | () => void | No | Secondary callback |
| `className` | string | No | Additional CSS classes |

---

## 📁 File Structure

```
src/
├── components/
│   └── EmptyState.tsx          ← Generic component
├── pages/
│   └── errors/
│       ├── index.ts            ← Exports
│       ├── NotFoundPage.tsx    ← 404
│       ├── ServerErrorPage.tsx ← 500
│       ├── NetworkErrorPage.tsx← Network
│       └── MaintenancePage.tsx ← Maintenance
└── config/
    └── axios.ts                ← Auto error handling
```

---

## 💡 Tips

### Do's ✅
- Use clear, actionable Hebrew text
- Provide helpful CTAs
- Show relevant icons
- Test on mobile devices
- Use EmptyState for consistency

### Don'ts ❌
- Don't use technical jargon
- Don't leave users stuck (always provide action)
- Don't overload with too many buttons
- Don't forget RTL layout
- Don't ignore accessibility

---

## 🔗 Related Documentation

- **Full Implementation:** `EMPTY_STATES_ERROR_PAGES_IMPLEMENTATION.md`
- **Design System:** `.github/instructions/design_rules_.instructions.md`
- **Component Library:** `src/components/ui/`

---

**Quick Access:**
```typescript
// Import everything you need:
import { EmptyState } from '@/components/EmptyState';
import { NotFoundPage, ServerErrorPage, NetworkErrorPage, MaintenancePage } from '@/pages/errors';
```

---

**Last Updated:** November 7, 2025
