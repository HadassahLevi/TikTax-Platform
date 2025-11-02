# Header Component System - Quick Reference

## 📁 Files Structure
```
src/components/layout/
├── Header.tsx          // Main header component
├── UserDropdown.tsx    // User avatar dropdown menu
├── MobileMenu.tsx      // Mobile slide-in menu
└── index.ts            // Exports
```

## 🎯 Usage

### Basic Usage
```tsx
import { Header } from '@/components/layout';

function App() {
  return (
    <div className="min-h-screen">
      <Header />
      <main id="main-content">
        {/* Your page content */}
      </main>
    </div>
  );
}
```

### With Custom className
```tsx
<Header className="shadow-md" />
```

## 📱 Responsive Behavior

### Desktop (>768px)
- Full horizontal navigation menu
- User dropdown with hover effect
- Logo on the left (RTL: right)
- Navigation items centered
- Avatar on the right (RTL: left)

### Mobile (<768px)
- Hamburger menu button
- Logo centered
- Avatar icon only
- Full-screen slide-in menu

## 🎨 Layout Breakdown

### Desktop Layout
```
┌─────────────────────────────────────────────────────────┐
│  [Logo]    [Dashboard] [Archive] [Export]      [Avatar▼]│
└─────────────────────────────────────────────────────────┘
```

### Mobile Layout
```
┌─────────────────────────────────────────────────────────┐
│  [☰]                [Logo]                      [Avatar]│
└─────────────────────────────────────────────────────────┘
```

## 🔧 Components

### 1. Header
**Props:**
- `className?: string` - Additional CSS classes

**Features:**
- Sticky position at top
- Active route highlighting
- Responsive navigation
- Skip to main content link (accessibility)

### 2. UserDropdown
**Props:**
- `className?: string` - Additional CSS classes

**Features:**
- Click to toggle (not hover)
- Click outside to close
- ESC key to close
- Keyboard navigation (arrow keys)
- User info header
- Profile, Settings, Logout options

**Dropdown Items:**
```tsx
interface DropdownItem {
  label: string;
  icon: React.ReactNode;
  href?: string;
  onClick?: () => void;
  variant?: 'default' | 'danger';
  divider?: boolean;
}
```

### 3. MobileMenu
**Props:**
- `isOpen: boolean` - Menu open state
- `onClose: () => void` - Close handler

**Features:**
- Full-screen overlay
- Slides in from right (RTL: left)
- Body scroll lock when open
- ESC key to close
- Click backdrop to close
- Smooth framer-motion animations

## 🎯 Navigation Items

Current navigation structure:
```tsx
const navigationItems = [
  { label: 'לוח בקרה', href: '/dashboard', key: 'dashboard' },
  { label: 'ארכיון', href: '/archive', key: 'archive' },
  { label: 'ייצוא', href: '/export', key: 'export' },
  { label: 'פרופיל', href: '/profile', key: 'profile' },
];
```

### Adding New Navigation Items
Edit `Header.tsx`:
```tsx
const navigationItems: NavigationItem[] = [
  // ... existing items
  { label: 'הגדרות', href: '/settings', key: 'settings' },
];
```

## 🔐 Authentication

### Logout Flow
1. User clicks "התנתק" (Logout)
2. `clearAuth()` called from Zustand store
3. User redirected to `/login`

```tsx
const handleLogout = () => {
  clearAuth(); // Clears tokens from memory
  navigate('/login');
};
```

### User Info Display
```tsx
// User initials in avatar
const initials = user 
  ? getInitials(user.firstName, user.lastName) 
  : 'TT';
```

## ♿ Accessibility

### Features
- Skip to main content link (shows on focus)
- ARIA labels for all icon buttons
- Keyboard navigation in dropdown
- Focus trap in mobile menu
- ESC key closes all menus
- Proper role attributes

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| Tab | Navigate through menu items |
| Arrow Down | Next item in dropdown |
| Arrow Up | Previous item in dropdown |
| Enter/Space | Select item |
| Escape | Close menu/dropdown |

## 🎨 Styling

### Header
```tsx
height: 64px
background: white
border-bottom: 1px solid #E5E7EB
box-shadow: sm
position: sticky
top: 0
z-index: 40
padding: 0 24px (desktop), 0 16px (mobile)
```

### Navigation Items
```tsx
// Default
color: #374151 (gray-700)
hover: #2563EB (primary-600)
hover:bg: #EFF6FF (primary-50)

// Active
color: #2563EB (primary-600)
underline: 3px solid #2563EB
```

### User Dropdown
```tsx
width: 224px (14rem)
background: white
border-radius: 8px
shadow: lg
border: 1px solid #E5E7EB
position: absolute
top: calc(100% + 8px)
right: 0 (RTL: left: 0)
```

### Mobile Menu
```tsx
width: 320px
max-width: 85vw
height: 100vh
background: white
shadow: 2xl
z-index: 50
slide animation: 0.3s ease-in-out
```

## 🔄 State Management

### Mobile Menu State
```tsx
const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
```

### User Dropdown State
```tsx
const [isOpen, setIsOpen] = useState(false);
```

### Auth State (Zustand)
```tsx
const { user, clearAuth } = useAuthStore();
```

## 🌐 RTL Support

All components support RTL (Hebrew):
- Logo position: right in RTL
- Navigation: right to left flow
- Dropdown: left-aligned in RTL
- Mobile menu: slides from left in RTL

## 📦 Dependencies

```json
{
  "react-router-dom": "^6.20.0",
  "framer-motion": "^10.16.16",
  "lucide-react": "^0.294.0",
  "zustand": "^4.4.7"
}
```

## 🧪 Testing Checklist

- [ ] Desktop navigation visible >768px
- [ ] Mobile menu visible <768px
- [ ] Active route highlighted
- [ ] User dropdown opens/closes
- [ ] Click outside closes dropdown
- [ ] ESC closes all menus
- [ ] Keyboard navigation works
- [ ] Logout redirects to /login
- [ ] Body scroll locks in mobile menu
- [ ] RTL layout correct
- [ ] Focus trap in mobile menu
- [ ] Skip to main content link works

## 🐛 Troubleshooting

### Header not sticky
- Ensure parent container doesn't have `overflow: hidden`
- Check z-index conflicts

### Dropdown not closing
- Check if click event is being prevented
- Verify ref is attached correctly

### Mobile menu animation broken
- Ensure framer-motion is installed
- Check AnimatePresence wraps motion components

### User initials not showing
- Verify user object has firstName/lastName
- Check getInitials utility function

## 📚 Related Components

- Button component: `/src/components/ui/Button.tsx`
- Modal component: `/src/components/ui/Modal.tsx`
- Auth store: `/src/stores/auth.store.ts`

## 🔗 Routes

Header links to:
- `/dashboard` - Main dashboard
- `/archive` - Receipt archive
- `/export` - Export functionality
- `/profile` - User profile
- `/settings` - Settings (Phase 2)
- `/login` - Login page (after logout)

---

**Last Updated:** November 2, 2025  
**Version:** 1.0.0  
**Status:** ✅ Production Ready
