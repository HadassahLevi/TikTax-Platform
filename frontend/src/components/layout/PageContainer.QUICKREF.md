# PageContainer Component - Quick Reference

**Path:** `src/components/layout/PageContainer.tsx`  
**Purpose:** Consistent page wrapper with loading states and responsive design

---

## 📦 Import

```tsx
import { PageContainer } from '@/components/layout';
// Or with skeleton loaders
import { 
  PageContainer, 
  GridSkeleton, 
  ListSkeleton, 
  StatsSkeleton,
  FormSkeleton 
} from '@/components/layout';
```

---

## ⚡ Basic Usage

### Simple Page
```tsx
<PageContainer title="לוח בקרה" maxWidth="md">
  <YourContent />
</PageContainer>
```

### With Subtitle and Action
```tsx
<PageContainer 
  title="ארכיון קבלות"
  subtitle="כל הקבלות שלך במקום אחד"
  action={<Button>הוסף קבלה</Button>}
  maxWidth="lg"
>
  <ReceiptGrid />
</PageContainer>
```

### Loading State
```tsx
<PageContainer title="טוען..." loading>
  <Content />
</PageContainer>
```

---

## 🎨 Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | **required** | Page content |
| `loading` | `boolean` | `false` | Show skeleton + spinner overlay |
| `title` | `string` | - | Page title (optional) |
| `subtitle` | `string` | - | Page description (optional) |
| `action` | `ReactNode` | - | Action button(s) in header |
| `maxWidth` | `'sm' \| 'md' \| 'lg' \| 'xl' \| 'full'` | `'md'` | Max width constraint |
| `noPadding` | `boolean` | `false` | Disable default padding |
| `className` | `string` | - | Additional CSS classes |

---

## 📏 Max Width Variants

| Variant | Width | Use Case |
|---------|-------|----------|
| `sm` | 640px | Forms, settings, narrow content |
| `md` | 880px | Default, most pages |
| `lg` | 1200px | Archive, grids, wide content |
| `xl` | 1440px | Dashboard, analytics |
| `full` | 100% | Custom layouts, full-width |

---

## 🎯 Common Patterns

### Dashboard Page
```tsx
<PageContainer title="לוח בקרה" maxWidth="xl">
  <div className="grid gap-6">
    <StatsRow />
    <ChartsSection />
    <RecentActivity />
  </div>
</PageContainer>
```

### Archive with Search
```tsx
<PageContainer 
  title="ארכיון" 
  action={
    <div className="flex gap-3">
      <SearchBar />
      <FilterButton />
    </div>
  }
  maxWidth="lg"
>
  <ReceiptGrid />
</PageContainer>
```

### Settings Page
```tsx
<PageContainer 
  title="הגדרות"
  subtitle="נהל את הפרופיל שלך"
  maxWidth="sm"
>
  <SettingsForm />
</PageContainer>
```

### Full Width (No Padding)
```tsx
<PageContainer maxWidth="full" noPadding>
  <CustomLayout />
</PageContainer>
```

### Page without Header
```tsx
<PageContainer maxWidth="md">
  {/* No title = no header */}
  <Content />
</PageContainer>
```

---

## 🔄 Loading States

### Basic Loading
```tsx
const [loading, setLoading] = useState(true);

<PageContainer title="נתונים" loading={loading}>
  <DataTable />
</PageContainer>
```

### Custom Skeleton
```tsx
<PageContainer title="גלריה">
  {loading ? (
    <GridSkeleton count={9} />
  ) : (
    <Gallery />
  )}
</PageContainer>
```

---

## 🎨 Available Skeletons

### GridSkeleton
```tsx
<GridSkeleton count={6} />
```
**Use for:** Card grids, image galleries

### ListSkeleton
```tsx
<ListSkeleton count={5} />
```
**Use for:** Transaction lists, rows

### StatsSkeleton
```tsx
<StatsSkeleton />
```
**Use for:** Dashboard metrics (4 cards)

### FormSkeleton
```tsx
<FormSkeleton />
```
**Use for:** Forms, input-heavy pages

---

## 💡 Best Practices

### ✅ DO
- Use `maxWidth="md"` for most pages (default)
- Use `maxWidth="xl"` for dashboards with grids
- Use `maxWidth="sm"` for forms and settings
- Provide `title` for better UX and SEO
- Use `loading` prop for API data fetching
- Use custom skeletons matching your layout

### ❌ DON'T
- Don't use `noPadding` unless you have custom layout
- Don't nest PageContainers
- Don't put navigation in PageContainer (use Header/BottomNav)
- Don't override min-height unless necessary

---

## 🎬 Responsive Behavior

| Breakpoint | Padding | Title Size |
|------------|---------|------------|
| Mobile (< 640px) | 16px | 28px |
| Tablet (640px - 1024px) | 24px | 32px |
| Desktop (> 1024px) | 32px | 32px |

**Min Height:** `calc(100vh - 128px)` (accounts for 64px header + 64px bottom nav)

---

## 🔧 Advanced Usage

### Multiple Actions
```tsx
<PageContainer 
  title="ניהול"
  action={
    <>
      <Button variant="secondary">ייצוא</Button>
      <Button variant="primary">הוסף</Button>
    </>
  }
>
  <Content />
</PageContainer>
```

### Conditional Actions
```tsx
<PageContainer 
  title="קבלות"
  action={hasSelection && <DeleteButton />}
>
  <ReceiptList />
</PageContainer>
```

### Custom Loading Message
```tsx
<PageContainer title="מייבא קבלות..." loading={importing}>
  <ImportResults />
</PageContainer>
```

---

## 🎨 Styling

### Custom Max Width
```tsx
<PageContainer className="max-w-[950px]">
  {/* Overrides default maxWidth */}
</PageContainer>
```

### Custom Background
```tsx
<PageContainer className="bg-gray-50">
  <Content />
</PageContainer>
```

---

## ♿ Accessibility

**Built-in Features:**
- ✅ Semantic HTML (`<h1>` for title)
- ✅ ARIA labels on loading spinner
- ✅ `role="status"` on loading overlay
- ✅ `aria-live="polite"` for status updates
- ✅ Proper heading hierarchy

---

## 🚀 Performance

**Optimizations:**
- ✅ Smooth fade-in animation (framer-motion)
- ✅ Staggered skeleton animations
- ✅ Automatic scroll to top on mount
- ✅ Minimal re-renders

---

## 📱 Mobile-First Design

**Mobile Considerations:**
- ✅ Single column layout on mobile
- ✅ Actions stack vertically on small screens
- ✅ Touch-friendly padding (16px minimum)
- ✅ Responsive text sizes

---

## 🔗 Related Components

- **Header** - App header with logo/menu
- **BottomNav** - Mobile navigation
- **Card** - Content containers
- **Button** - Action buttons
- **Modal** - Overlays (not for pages)

---

## 📝 Examples from Codebase

### Dashboard Page
```tsx
// src/pages/Dashboard.tsx
<PageContainer title="לוח בקרה" maxWidth="xl">
  <StatsSummary />
  <CategoryBreakdown />
  <RecentReceipts />
</PageContainer>
```

### Archive Page
```tsx
// src/pages/Archive.tsx
<PageContainer 
  title="ארכיון קבלות"
  action={<SearchAndFilter />}
  maxWidth="lg"
>
  <ReceiptGrid />
</PageContainer>
```

### Profile Page
```tsx
// src/pages/Profile.tsx
<PageContainer 
  title="הפרופיל שלי"
  subtitle="עדכן את הפרטים האישיים שלך"
  maxWidth="sm"
>
  <ProfileForm />
</PageContainer>
```

---

## 🐛 Common Issues

### Issue: Header not showing
**Solution:** Make sure to provide `title` prop

### Issue: Content too narrow
**Solution:** Increase `maxWidth` prop (`md` → `lg` → `xl`)

### Issue: Too much padding
**Solution:** Use `noPadding` prop and add custom padding

### Issue: Loading spinner not centered
**Solution:** Ensure content has height (skeleton provides this)

---

## 🎯 Quick Decision Tree

```
Need page wrapper?
├─ Yes
│  ├─ Form/Settings → maxWidth="sm"
│  ├─ Regular page → maxWidth="md" (default)
│  ├─ Grid/Archive → maxWidth="lg"
│  └─ Dashboard → maxWidth="xl"
└─ No → Use regular div
```

---

**Last Updated:** November 2, 2025  
**Component Version:** 1.0.0  
**Tik-Tax Design System**
