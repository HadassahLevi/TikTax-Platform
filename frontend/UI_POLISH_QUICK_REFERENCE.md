# 🎯 UI POLISH QUICK REFERENCE

**Quick access guide for developers**

---

## ⌨️ Keyboard Shortcuts

### Global Shortcuts (Always Active)
```
Ctrl/Cmd + K    → Focus search
Ctrl/Cmd + U    → Upload receipt
Ctrl/Cmd + E    → Export page
Ctrl/Cmd + D    → Dashboard
Ctrl/Cmd + H    → Help
Ctrl/Cmd + ,    → Settings
/               → Quick search
Shift + ?       → Show shortcuts modal
ESC             → Close modals
↑↓              → Navigate lists
Enter           → Activate item
```

### Using in Components
```tsx
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts';

// In App.tsx (already added)
useKeyboardShortcuts();
```

---

## 🍞 Breadcrumbs

### Usage
```tsx
import { Breadcrumbs } from '@/components/Breadcrumbs';

// In Header (already added)
<Breadcrumbs />
```

### Adding New Routes
Edit `/src/components/Breadcrumbs.tsx`:
```tsx
const ROUTE_LABELS: Record<string, string> = {
  'dashboard': 'דשבורד',
  'your-route': 'תווית בעברית',  // Add here
};
```

---

## ✨ Animation Classes

### Quick Apply
```tsx
// Button animations
<button className="button-press color-transition focus-ring">
  Click me
</button>

// Card animations
<div className="card-hover">
  Content
</div>

// Error shake
<div className={error ? 'shake-error' : ''}>
  <Input error={error} />
</div>

// Loading
<div className="shimmer">Loading...</div>

// Entrance
<div className="fade-in">Content</div>
<div className="slide-in-right">Content</div>
<div className="scale-in">Modal</div>
```

### All Available Classes
| Class | Effect |
|-------|--------|
| `button-press` | Scale down on click |
| `card-hover` | Lift on hover |
| `smooth-transition` | 200ms all |
| `color-transition` | 200ms colors |
| `shake-error` | Shake animation |
| `pulse-soft` | Subtle pulse |
| `fade-in` | Fade + slide in |
| `slide-in-right` | Slide from right |
| `slide-in-left` | Slide from left |
| `scale-in` | Scale up |
| `bounce-soft` | Soft bounce |
| `spin` | Rotating |
| `shimmer` | Loading skeleton |
| `ripple` | Material ripple |
| `focus-ring` | Focus indicator |
| `hover-lift` | Hover lift |

---

## ♿ Accessibility

### Quick Fixes

#### Screen Reader Only Content
```tsx
<span className="sr-only">Hidden text for screen readers</span>
```

#### Skip to Main Content
```tsx
// Already in Header.tsx
<a href="#main-content" className="skip-to-content">
  דלג לתוכן הראשי
</a>

// Add to main container
<main id="main-content" role="main">
  {children}
</main>
```

#### Announce to Screen Reader
```tsx
import { announceToScreenReader } from '@/utils/accessibility';

announceToScreenReader('פעולה הושלמה', 'polite');
announceToScreenReader('שגיאה חמורה!', 'assertive');
```

#### Focus Trap (Modals)
```tsx
import { trapFocus } from '@/utils/accessibility';

useEffect(() => {
  if (isOpen) {
    const cleanup = trapFocus(modalRef.current);
    return cleanup;
  }
}, [isOpen]);
```

#### ARIA Labels
```tsx
import { getAriaLabel } from '@/utils/accessibility';

<button aria-label={getAriaLabel('close')}>X</button>
// Returns: 'סגור'
```

### Accessibility Checklist
```tsx
// ✅ Button
<button
  aria-label="תיאור"
  aria-disabled={disabled}
  tabIndex={0}
>
  Content
</button>

// ✅ Input
<input
  aria-label="שדה"
  aria-invalid={!!error}
  aria-describedby={error ? 'error-id' : undefined}
  aria-required={required}
/>

// ✅ Modal
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
/>

// ✅ List
<div
  role="list"
  aria-label="רשימת פריטים"
>
  <div role="listitem">Item</div>
</div>
```

---

## 🌐 Browser Fixes

### Auto-Applied
```tsx
// In App.tsx (already added)
import { initBrowserFixes } from '@/utils/browserFixes';

useEffect(() => {
  initBrowserFixes();
}, []);
```

### Detect Device/Browser
```tsx
import { 
  isIOS, 
  isAndroid, 
  isSafari, 
  isMobile 
} from '@/utils/browserFixes';

if (isIOS()) {
  // iOS-specific code
}

if (isSafari()) {
  // Safari-specific code
}
```

### Date Format (Safari)
```tsx
import { formatDateForSafari } from '@/utils/browserFixes';

const formattedDate = formatDateForSafari('31/12/2024');
// Returns: '2024-12-31'
```

### CSS Utilities
```css
/* iOS safe area */
.safe-area-top
.safe-area-bottom
.safe-area-left
.safe-area-right

/* Scrollbar hide */
.scrollbar-hide
```

---

## 🎨 Component Usage

### Button with Animations
```tsx
import Button from '@/components/ui/Button';

<Button 
  variant="primary"
  className="button-press"  // Already included
>
  שמור
</Button>
```

### Input with Error Shake
```tsx
import Input from '@/components/ui/Input';

<Input
  label="אימייל"
  error={error}  // Automatically triggers shake
  aria-label="שדה אימייל"
/>
```

### Card with Hover
```tsx
import Card from '@/components/ui/Card';

<Card hoverable onClick={handleClick}>
  Content
</Card>
```

### Modal with Focus Trap
```tsx
import Modal from '@/components/ui/Modal';

<Modal
  isOpen={isOpen}
  onClose={onClose}
  // Focus trap already included
>
  Content
</Modal>
```

---

## 📱 Mobile Considerations

### Touch Targets
```tsx
// Minimum 48x48px
<button className="min-h-[48px] min-w-[48px]">
  Icon
</button>
```

### iOS Safe Area
```tsx
<div className="safe-area-bottom">
  Content respects iPhone notch
</div>
```

### Prevent Input Zoom
```css
/* Already in index.css for mobile */
input {
  font-size: 16px !important;
}
```

### Hide Bottom Nav on Keyboard
```tsx
// Automatically applied when keyboard opens
// Body gets class "keyboard-open"
```

---

## 🧪 Testing Quick Start

### Keyboard Testing
```bash
1. Tab through all elements
2. Test all keyboard shortcuts
3. Navigate lists with arrows
4. ESC to close modals
5. Enter to activate buttons
```

### Screen Reader Testing
```bash
# Mac (VoiceOver)
Cmd + F5

# Windows (NVDA)
Download: https://www.nvaccess.org/

# Test:
- Tab through elements
- Listen to ARIA labels
- Test form validation
- Test dynamic content
```

### Mobile Testing
```bash
# iOS Safari
1. Test 100vh viewport
2. Test safe area insets
3. Test input zoom prevention
4. Test pull-to-refresh disabled

# Android Chrome
1. Test keyboard detection
2. Test viewport adjustments
3. Test bottom nav hiding
```

### Accessibility Audit
```bash
# Chrome DevTools
1. Open DevTools
2. Lighthouse tab
3. Run Accessibility audit
4. Fix issues flagged

# Manual checks
- Color contrast
- Keyboard navigation
- Screen reader
- Focus indicators
```

---

## 🐛 Common Issues & Fixes

### Keyboard Shortcut Not Working
```tsx
// Check if input is focused
// Shortcuts skip when typing in inputs

// Force shortcut:
if (e.key === 'k' && e.ctrlKey) {
  e.preventDefault();
  // Your logic
}
```

### Animation Not Smooth
```tsx
// Check user preference
import { prefersReducedMotion } from '@/utils/accessibility';

if (!prefersReducedMotion()) {
  // Apply animation
}
```

### iOS Viewport Issue
```tsx
// Already fixed in initBrowserFixes()
// CSS variable --vh updated dynamically
```

### Focus Trap Not Working
```tsx
// Ensure element is rendered
const modalRef = useRef<HTMLDivElement>(null);

useEffect(() => {
  if (isOpen && modalRef.current) {
    const cleanup = trapFocus(modalRef.current);
    return cleanup;
  }
}, [isOpen]);
```

---

## 📚 File Locations

```
src/
├── hooks/
│   └── useKeyboardShortcuts.ts
├── components/
│   ├── Breadcrumbs.tsx
│   └── KeyboardShortcutsModal.tsx
├── styles/
│   ├── animations.css
│   └── accessibility.css
├── utils/
│   ├── accessibility.ts
│   └── browserFixes.ts
└── index.css (main imports)
```

---

## 💡 Pro Tips

1. **Always test keyboard navigation**
   ```tsx
   // Add tabIndex to custom interactive elements
   <div role="button" tabIndex={0} onClick={...}>
   ```

2. **Use semantic HTML**
   ```tsx
   // Good
   <button>Click</button>
   
   // Avoid
   <div onClick={...}>Click</div>
   ```

3. **Add ARIA labels to icon-only buttons**
   ```tsx
   <button aria-label="סגור">
     <X />
   </button>
   ```

4. **Test with real devices**
   - iOS Safari behaves differently
   - Android keyboards vary
   - Test on actual phones

5. **Respect user preferences**
   ```tsx
   // Check motion preference
   if (prefersReducedMotion()) {
     // Skip animation
   }
   ```

---

## 🔗 Resources

- **WCAG Guidelines:** https://www.w3.org/WAI/WCAG21/quickref/
- **ARIA Practices:** https://www.w3.org/WAI/ARIA/apg/
- **WebAIM:** https://webaim.org/
- **Lighthouse:** Chrome DevTools → Lighthouse
- **axe DevTools:** Browser extension for accessibility testing

---

**Quick Reference Complete!**  
For detailed documentation, see: `UI_POLISH_IMPLEMENTATION_COMPLETE.md`
