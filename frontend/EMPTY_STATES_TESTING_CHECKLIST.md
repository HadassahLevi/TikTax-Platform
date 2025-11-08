# Empty States & Error Pages - Testing Checklist

## ✅ Complete Testing Guide

---

## 🧪 FUNCTIONAL TESTS

### 1. EmptyState Component ✅

#### Test 1.1: Basic Rendering
```typescript
✅ Renders icon correctly
✅ Displays title text
✅ Shows description text
✅ Icon is centered
✅ Text is center-aligned
```

#### Test 1.2: With Primary Action
```typescript
✅ Primary button appears when actionLabel provided
✅ Button click triggers onAction callback
✅ Button has correct variant (primary)
✅ Button size is 'lg'
```

#### Test 1.3: With Secondary Action
```typescript
✅ Secondary button appears when secondaryLabel provided
✅ Button click triggers onSecondaryAction callback
✅ Button has 'secondary' variant
✅ Both buttons display side-by-side on desktop
```

#### Test 1.4: Custom Styling
```typescript
✅ className prop adds custom classes
✅ Does not override default classes
```

---

## 🚨 ERROR PAGES TESTS

### 2. NotFoundPage (404) ✅

#### Test 2.1: Content Display
```typescript
Navigate to: /invalid-route-12345

✅ "404" heading visible
✅ "הדף לא נמצא" heading visible
✅ Error description in Hebrew
✅ FileQuestion icon displayed
✅ Icon in primary-100 background circle
```

#### Test 2.2: Navigation
```typescript
✅ "חזור לדף הבית" button navigates to /dashboard
✅ "חזור לדף הקודם" button goes back in history
✅ Support email link: mailto:support@tiktax.co.il
✅ Email link styled as primary-600 with hover underline
```

#### Test 2.3: Responsive
```typescript
Mobile (< 640px):
✅ Max width appropriate
✅ Padding on sides (16px)
✅ Buttons full-width
✅ Text readable

Desktop:
✅ Centered on screen
✅ Max width 448px (max-w-md)
✅ Buttons maintain size
```

---

### 3. ServerErrorPage (500) ✅

#### Test 3.1: Content Display
```typescript
Navigate to: /error/500

✅ "500" heading visible
✅ "משהו השתבש" heading visible
✅ Error description in Hebrew
✅ ServerCrash icon displayed
✅ Icon in red-100 background
```

#### Test 3.2: Functionality
```typescript
✅ "נסה שוב" button reloads page
✅ "חזור לדף הבית" navigates to /dashboard
✅ Error code displayed: "500 - Internal Server Error"
✅ Support email link present
```

#### Test 3.3: Info Box
```typescript
✅ Blue info box (bg-blue-50) displayed
✅ Error code visible
✅ Support contact visible
✅ Proper Hebrew text formatting
```

---

### 4. NetworkErrorPage ✅

#### Test 4.1: Online State
```typescript
While online:

✅ Green icon background (bg-green-100)
✅ "החיבור חזר!" heading
✅ Positive message displayed
✅ Status indicator shows "מחובר לאינטרנט"
✅ Green pulse dot (bg-green-500)
✅ "נסה שוב" button ENABLED
```

#### Test 4.2: Offline State
```typescript
Disconnect internet, navigate to /error/network:

✅ Amber icon background (bg-amber-100)
✅ "בעיית חיבור לאינטרנט" heading
✅ Error message displayed
✅ Status indicator shows "לא מחובר לאינטרנט"
✅ Amber pulse dot (bg-amber-500)
✅ "נסה שוב" button DISABLED
```

#### Test 4.3: Real-time Detection
```typescript
Start offline:
✅ Shows offline state

Reconnect internet:
✅ Automatically detects connection
✅ Updates to online state
✅ Button becomes enabled
✅ Background color changes
✅ Message updates

Disconnect again:
✅ Automatically detects disconnection
✅ Updates to offline state
```

#### Test 4.4: Troubleshooting Tips
```typescript
✅ Tips section visible
✅ 4 tips displayed in Hebrew
✅ Text aligned right (RTL)
✅ Bullet points visible
✅ Tips are helpful and actionable
```

---

### 5. MaintenancePage ✅

#### Test 5.1: Content Display
```typescript
Navigate to: /maintenance

✅ Construction icon displayed
✅ "תחזוקה מתוזמנת" heading visible
✅ Explanation text in Hebrew
✅ Gradient background (primary-50 to blue-50)
```

#### Test 5.2: Time Display
```typescript
✅ Clock icon visible
✅ "זמן משוער לחזרה" label visible
✅ "30 דקות" estimated time shown
✅ Current timestamp displayed
✅ Timestamp in Hebrew format (toLocaleTimeString('he-IL'))
```

#### Test 5.3: Updates Section
```typescript
✅ "מה חדש?" heading visible
✅ 3 update items listed
✅ Items in Hebrew
✅ Proper RTL alignment
✅ Bordered white card (border-gray-200)
```

#### Test 5.4: Contact Info
```typescript
✅ Support email visible
✅ Email link styled correctly
✅ Link opens mail client
```

---

## 📱 RESPONSIVE TESTS

### 6. Mobile (< 640px)

```typescript
Test on iPhone 12 (390px width):

EmptyState:
✅ Icon size appropriate (64px)
✅ Title readable (18px)
✅ Description readable (16px)
✅ Buttons full-width
✅ Vertical padding sufficient

Error Pages:
✅ Content fits within viewport
✅ No horizontal scroll
✅ Touch targets >= 44px height
✅ Text wraps properly
✅ Icons scale appropriately
✅ Margins/padding: 16px sides
```

### 7. Tablet (640px - 1024px)

```typescript
Test on iPad (768px width):

✅ Content centered
✅ Max width respected
✅ Buttons appropriate width
✅ Increased padding (24px)
✅ Icon size comfortable
✅ Text line-height optimal
```

### 8. Desktop (> 1024px)

```typescript
Test on 1920px width:

✅ Content centered
✅ Max width enforced (448px for errors)
✅ No stretched elements
✅ Hover states work
✅ Cursor changes to pointer on buttons
✅ Focus states visible on tab navigation
```

---

## ♿ ACCESSIBILITY TESTS

### 9. Keyboard Navigation

```typescript
Test with keyboard only (no mouse):

✅ Tab moves focus to buttons
✅ Focus ring visible (2px outline)
✅ Enter activates buttons
✅ Tab order logical (top to bottom)
✅ No focus traps
✅ Skip to main content (if applicable)
```

### 10. Screen Reader

```typescript
Test with NVDA/JAWS/VoiceOver:

✅ All text read correctly
✅ Hebrew text pronounced properly
✅ Button labels descriptive
✅ Icon labels present (aria-label if needed)
✅ Heading hierarchy correct (h1 → h2 → h3)
✅ Landmark regions defined
```

### 11. Color Contrast

```typescript
Use Chrome DevTools:

✅ Title text: #111827 on #FFF (passes AAA)
✅ Description: #4B5563 on #FFF (passes AA)
✅ Button text: #FFF on #2563EB (passes AA)
✅ Error icons: sufficient contrast
✅ All status colors meet WCAG 2.1 AA
```

---

## 🔗 INTEGRATION TESTS

### 12. Dashboard Integration

```typescript
Test new user (0 receipts):

✅ Dashboard loads
✅ Empty state shown immediately
✅ No flash of loading state
✅ Title: "עדיין לא העלית קבלות"
✅ "העלה קבלה ראשונה" button works
✅ "למד עוד" button works
✅ User greeting shown: "שלום, [name]"
```

### 13. Archive Integration

#### Test 13.1: No Receipts
```typescript
New user, navigate to /archive:

✅ Archive page loads
✅ Empty state: "הארכיון ריק"
✅ "העלה קבלה" button navigates to /receipts/new
✅ Search bar still visible
✅ Stats show zeros
```

#### Test 13.2: No Search Results
```typescript
User has receipts, searches for "xyz123":

✅ Search input shows query
✅ Empty state: "לא נמצאו תוצאות"
✅ Query displayed in message
✅ "נקה חיפוש" button clears search
✅ After clear, receipts reappear
```

#### Test 13.3: No Filter Results
```typescript
User applies impossible filters:

✅ Filter chips displayed
✅ Empty state: "אין קבלות בסינון זה"
✅ "נקה פילטרים" button shown
✅ Clicking button clears all filters
✅ Filter chips disappear
✅ Receipts reappear
```

---

## 🌐 AXIOS INTEGRATION TESTS

### 14. Automatic Error Redirects

#### Test 14.1: Network Error
```typescript
Disconnect internet, make API call:

✅ Axios intercepts error
✅ Logs: "❌ Network Error: Unable to connect"
✅ Redirects to /error/network
✅ Page loads correctly
✅ No console errors
```

#### Test 14.2: Server Error (500)
```typescript
Backend returns 500:

✅ Axios intercepts 500 status
✅ Logs: "❌ Server Error"
✅ Redirects to /error/500
✅ Page loads correctly
```

#### Test 14.3: Maintenance (503)
```typescript
Backend returns 503:

✅ Axios intercepts 503 status
✅ Logs: "⚠️ Maintenance Mode (503)"
✅ Redirects to /maintenance
✅ Page loads correctly
```

#### Test 14.4: Not Found (404)
```typescript
Backend returns 404 for API resource:

✅ Axios logs error
✅ Does NOT redirect (resource 404, not page)
✅ Error handled by component
```

---

## 🎨 VISUAL REGRESSION TESTS

### 15. Design System Compliance

```typescript
Check all components:

✅ Colors match design system:
   - Primary: #2563EB
   - Success: #10B981
   - Error: #EF4444
   - Amber: #F59E0B
   - Gray: #6B7280, #E5E7EB

✅ Typography matches:
   - Font: Inter
   - Headings: 24-32px, weight 600
   - Body: 16px, weight 400
   - Small: 14px

✅ Spacing on 8px grid:
   - Padding: 16px, 24px, 32px
   - Margins: 8px, 16px, 24px
   - Gap: 12px, 16px, 24px

✅ Border radius:
   - Standard: 8px
   - Large: 12px
   - Full: 9999px (circles)

✅ Shadows:
   - None (flat)
   - sm: 0 1px 2px
   - md: 0 4px 6px
```

---

## 🔄 RTL (Right-to-Left) TESTS

### 16. Hebrew Layout

```typescript
All pages and components:

✅ Text flows right-to-left
✅ Icons positioned correctly
✅ Buttons aligned properly
✅ Lists/bullets on right side
✅ Margins/padding mirror correctly
✅ Tooltips/popovers on correct side
```

---

## 📊 PERFORMANCE TESTS

### 17. Load Times

```typescript
Measure with Chrome DevTools:

✅ EmptyState renders < 50ms
✅ Error pages load < 100ms
✅ No layout shift (CLS = 0)
✅ First paint < 200ms
✅ Interactive < 300ms
```

### 18. Bundle Size

```typescript
Check bundle:

✅ EmptyState component < 2KB gzipped
✅ Error pages < 5KB each (gzipped)
✅ No unnecessary dependencies
✅ Icons tree-shaken from lucide-react
```

---

## 🐛 EDGE CASES

### 19. Edge Case Testing

```typescript
Test unusual scenarios:

✅ Very long title text (truncates/wraps)
✅ Very long description (wraps properly)
✅ Missing optional props (graceful)
✅ Unicode characters in Hebrew
✅ Special characters (emojis, symbols)
✅ Network toggles rapidly (debounced)
✅ Multiple error states simultaneously
```

---

## ✅ FINAL CHECKLIST

Before marking complete:

- [ ] All 19 test sections passed
- [ ] No console errors
- [ ] No TypeScript errors
- [ ] No accessibility violations
- [ ] Responsive on all breakpoints
- [ ] RTL working correctly
- [ ] Performance acceptable
- [ ] Design system compliant
- [ ] User testing passed
- [ ] Documentation complete

---

## 📝 Test Results Template

```markdown
## Test Results - [Date]

**Tester:** [Name]
**Environment:** [Local/Staging/Production]
**Browser:** [Chrome/Safari/Firefox + Version]

### Functional Tests
- EmptyState Component: ✅ PASS
- NotFoundPage (404): ✅ PASS
- ServerErrorPage (500): ✅ PASS
- NetworkErrorPage: ✅ PASS
- MaintenancePage: ✅ PASS

### Responsive Tests
- Mobile: ✅ PASS
- Tablet: ✅ PASS
- Desktop: ✅ PASS

### Accessibility Tests
- Keyboard Navigation: ✅ PASS
- Screen Reader: ✅ PASS
- Color Contrast: ✅ PASS

### Integration Tests
- Dashboard Empty State: ✅ PASS
- Archive Empty States: ✅ PASS
- Axios Error Handling: ✅ PASS

### Issues Found
None / [List issues]

### Overall Status
✅ READY FOR PRODUCTION
```

---

**Last Updated:** November 7, 2025
