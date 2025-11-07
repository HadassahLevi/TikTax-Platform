# Loading States - Quick Reference

**Last Updated:** November 7, 2025

---

## 🚀 Quick Import

```tsx
// All loading components
import { 
  SkeletonCard, 
  SkeletonList, 
  SkeletonTable,
  LoadingSpinner,
  ProgressBar,
  ImageLoader
} from '@/components/loading';

// Custom hook
import { useMinimumLoading } from '@/hooks/useMinimumLoading';
```

---

## 🎯 Common Patterns

### 1. Page Initial Loading

```tsx
const showLoading = useMinimumLoading(loading && !data, 300);

if (showLoading) {
  return (
    <PageContainer>
      <SkeletonCard variant="stat" />
      <SkeletonList count={5} variant="receipt" />
    </PageContainer>
  );
}
```

### 2. Infinite Scroll

```tsx
const initialLoading = useMinimumLoading(loading && items.length === 0, 300);
const loadingMore = loading && items.length > 0;

return (
  <>
    {initialLoading && <SkeletonList count={12} />}
    {!initialLoading && <ContentList items={items} />}
    {loadingMore && <LoadingSpinner text="טוען עוד..." />}
  </>
);
```

### 3. Image Lazy Loading

```tsx
<ImageLoader 
  src={imageUrl}
  alt={altText}
  aspectRatio="16/9"
/>
```

### 4. File Upload Progress

```tsx
<ProgressBar 
  progress={uploadProgress}
  label="מעלה קובץ..."
  color="primary"
/>
```

---

## 📦 Component Quick Reference

| Component | Use For | Example |
|-----------|---------|---------|
| `SkeletonCard` | Card placeholders | `<SkeletonCard variant="stat" />` |
| `SkeletonList` | Multiple items | `<SkeletonList count={5} variant="receipt" />` |
| `SkeletonTable` | Tables | `<SkeletonTable rows={10} columns={5} />` |
| `LoadingSpinner` | Centered loading | `<LoadingSpinner size="lg" text="טוען..." />` |
| `ProgressBar` | Upload/progress | `<ProgressBar progress={50} />` |
| `ImageLoader` | Lazy images | `<ImageLoader src={url} alt={text} />` |

---

## 🎨 Variants

### SkeletonCard Variants

```tsx
<SkeletonCard variant="stat" />     // Dashboard stats
<SkeletonCard variant="receipt" />  // Receipt cards
<SkeletonCard variant="default" />  // Generic cards
```

### LoadingSpinner Sizes

```tsx
<LoadingSpinner size="sm" />  // 16px - inline
<LoadingSpinner size="md" />  // 24px - default
<LoadingSpinner size="lg" />  // 32px - page level
```

### ProgressBar Colors

```tsx
<ProgressBar color="primary" />   // Blue
<ProgressBar color="success" />   // Green
<ProgressBar color="warning" />   // Amber
<ProgressBar color="danger" />    // Red
```

---

## ⚡ Performance Tips

1. **Always use minimum loading time:**
   ```tsx
   const showLoading = useMinimumLoading(loading, 300);
   ```

2. **Lazy load routes:**
   ```tsx
   const Page = React.lazy(() => import('./Page'));
   ```

3. **Use ImageLoader for all images:**
   ```tsx
   <ImageLoader src={url} alt={text} loading="lazy" />
   ```

4. **Match skeleton to content:**
   ```tsx
   // ✅ Good
   <div className="grid grid-cols-3 gap-4">
     <SkeletonCard variant="stat" />
     <SkeletonCard variant="stat" />
     <SkeletonCard variant="stat" />
   </div>
   
   // ❌ Bad
   <LoadingSpinner /> // Doesn't match layout
   ```

---

## 🐛 Common Mistakes

### ❌ DON'T

```tsx
// Causes flash for quick loads
if (loading) return <Skeleton />;

// Doesn't match layout
return <div className="grid"><LoadingSpinner /></div>;

// Missing alt text
<img src={url} />
```

### ✅ DO

```tsx
// Prevents flash
const showLoading = useMinimumLoading(loading, 300);
if (showLoading) return <Skeleton />;

// Matches layout
return <div className="grid"><SkeletonCard /></div>;

// Lazy load with fallback
<ImageLoader src={url} alt={text} />
```

---

## 📱 Responsive Patterns

```tsx
// Desktop: Grid, Mobile: Stack
<SkeletonList 
  count={12}
  variant="receipt"
  className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
/>

// Adjust count based on screen
const skeletonCount = useMediaQuery('(min-width: 768px)') ? 12 : 6;
<SkeletonList count={skeletonCount} />
```

---

## 🧪 Testing Commands

```bash
# Test with slow network
npm run dev -- --throttle=slow-3g

# Test with network offline
# (Use Chrome DevTools Network tab)

# Lighthouse performance audit
npm run lighthouse
```

---

## 🎯 Checklist for New Features

- [ ] Initial loading skeleton
- [ ] Use `useMinimumLoading` (300ms)
- [ ] Pagination/infinite scroll loading
- [ ] Error state fallback
- [ ] Empty state fallback
- [ ] `ImageLoader` for images
- [ ] ARIA labels
- [ ] Test with slow network
- [ ] Test offline → online

---

## 📚 Full Documentation

See [LOADING_STATES_GUIDE.md](./LOADING_STATES_GUIDE.md) for complete details.

---

**Quick reference for implementing loading states in Tik-Tax** 🚀
