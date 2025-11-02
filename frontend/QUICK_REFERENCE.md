# Tik-Tax Frontend - Quick Reference

## 🚀 Development Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linting
npm run lint

# Format code
npm run format

# Check formatting
npm run format:check

# Type check
npm run type-check
```

## 📁 Import Aliases

```typescript
import Button from '@/components/ui/Button';
import { useAuth } from '@/hooks/useAuth';
import { authService } from '@/services/auth.service';
import { formatCurrency } from '@/utils/formatters';
import type { User } from '@/types';
import { API_ENDPOINTS } from '@/constants';
import axiosInstance from '@/config/axios';
```

## 🎨 Tailwind Color Classes

### Primary (Blue #2563EB)
```tsx
bg-primary-50   bg-primary-600   text-primary-50   text-primary-600
border-primary-50   hover:bg-primary-700
```

### Success (Green #10B981)
```tsx
bg-success-50   bg-success-600   text-success-50   text-success-600
```

### Error (Red #EF4444)
```tsx
bg-error-50   bg-error-600   text-error-50   text-error-600
```

### Info (Blue #3B82F6)
```tsx
bg-info-50   bg-info-600   text-info-50   text-info-600
```

### Warning (Amber #F59E0B)
```tsx
bg-warning-50   bg-warning-600   text-warning-50   text-warning-600
```

## 📱 Responsive Breakpoints

```tsx
// Mobile first approach
<div className="w-full sm:w-1/2 md:w-1/3 lg:w-1/4 xl:w-1/5">
  {/* Content */}
</div>

// Breakpoints:
// sm:  640px
// md:  768px
// lg:  1024px
// xl:  1280px
// 2xl: 1536px
```

## 🔧 Common Utilities

### Formatters
```typescript
import { formatCurrency, formatDate, formatPhoneNumber } from '@/utils/formatters';

formatCurrency(1234.56);           // "₪1,234.56"
formatDate('2024-01-15');          // "15/01/2024"
formatPhoneNumber('0501234567');   // "050-123-4567"
```

### Validators
```typescript
import { isValidEmail, validatePassword, isValidPhone } from '@/utils/validators';

isValidEmail('test@example.com');  // true
isValidPhone('0501234567');        // true
validatePassword('Password123');   // { isValid: true, message: '...' }
```

## 🗂️ Types

```typescript
import type { 
  User, 
  Receipt, 
  ReceiptCategory,
  ReceiptStatus,
  LoginCredentials,
  SignupData 
} from '@/types';
```

## 🎯 Constants

```typescript
import { 
  RECEIPT_CATEGORIES, 
  RECEIPT_STATUS_LABELS,
  API_ENDPOINTS,
  CURRENCY_SYMBOL 
} from '@/constants';

// Usage:
const category = RECEIPT_CATEGORIES['office-supplies'];
// { label: 'Office Supplies', labelHe: 'ציוד משרדי', color: 'bg-blue-100...' }

const endpoint = API_ENDPOINTS.AUTH.LOGIN; // '/auth/login'
```

## 🌐 RTL Support

```html
<!-- Already configured in index.html -->
<html lang="he" dir="rtl">
```

```css
/* Tailwind handles RTL automatically */
.ltr:pl-4  /* becomes pr-4 in RTL */
.rtl:text-right  /* already right in RTL */
```

## 🔐 Environment Variables

```bash
# .env file (create from .env.example)
VITE_API_URL=http://localhost:3000/api
VITE_GOOGLE_VISION_API_KEY=your_key
VITE_AWS_S3_BUCKET=your_bucket
```

```typescript
// Access in code:
const apiUrl = import.meta.env.VITE_API_URL;
```

## 📦 Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| react | ^18.2.0 | UI library |
| react-router-dom | ^6.20.0 | Routing |
| zustand | ^4.4.7 | State management |
| axios | ^1.6.2 | HTTP client |
| react-hook-form | ^7.49.2 | Forms |
| tailwindcss | ^3.3.0 | Styling |
| lucide-react | ^0.294.0 | Icons |
| framer-motion | ^10.16.16 | Animations |
| date-fns | 2.30.0 | Date utilities |
| recharts | ^2.10.3 | Charts |

## 🎨 Common Component Patterns

### Button
```tsx
<button className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
  לחץ כאן
</button>
```

### Card
```tsx
<div className="bg-white rounded-lg shadow-md p-6">
  <h3 className="text-xl font-semibold mb-4">כותרת</h3>
  <p className="text-gray-600">תוכן</p>
</div>
```

### Input
```tsx
<div>
  <label className="block text-sm font-medium text-gray-700 mb-1">
    שם משתמש
  </label>
  <input 
    type="text"
    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-200 focus:outline-none"
  />
</div>
```

### Badge/Tag
```tsx
<span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-success-100 text-success-800">
  הושלם
</span>
```

## 🔄 Zustand Store Pattern

```typescript
import { create } from 'zustand';

interface MyState {
  count: number;
  increment: () => void;
  decrement: () => void;
}

export const useMyStore = create<MyState>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
}));

// Usage in component:
const { count, increment } = useMyStore();
```

## 📡 API Service Pattern

```typescript
import axios from '@/config/axios';
import type { User } from '@/types';

export const userService = {
  async getProfile(): Promise<User> {
    const response = await axios.get('/user/profile');
    return response.data;
  },
  
  async updateProfile(data: Partial<User>): Promise<User> {
    const response = await axios.put('/user/profile', data);
    return response.data;
  },
};
```

## 🎣 Custom Hook Pattern

```typescript
import { useState, useEffect } from 'react';

export const useDebounce = <T,>(value: T, delay: number): T => {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
};
```

## 📝 Hebrew Text Examples

```typescript
// Common UI text
const hebrewText = {
  save: 'שמור',
  cancel: 'ביטול',
  delete: 'מחק',
  edit: 'ערוך',
  close: 'סגור',
  search: 'חיפוש',
  filter: 'סינון',
  loading: 'טוען...',
  error: 'שגיאה',
  success: 'הצלחה',
};
```

## 🐛 Debugging Tips

```typescript
// Type-safe console logging
const debug = (message: string, data?: unknown) => {
  if (import.meta.env.DEV) {
    console.log(`[DEBUG] ${message}`, data);
  }
};
```

## 📚 Documentation Files

- `README.md` - Project overview and setup
- `PROJECT_SETUP.md` - Detailed setup summary
- `COMPONENT_GUIDE.md` - Component development patterns
- `QUICK_REFERENCE.md` - This file
- `.env.example` - Environment variables template

---

**Keep this handy while developing! 🚀**
