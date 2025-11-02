# Component Development Guide

Quick reference for creating components in the Tik-Tax frontend.

## Component Template

### Functional Component (TypeScript)

```tsx
import type { FC, ReactNode } from 'react';

interface ButtonProps {
  children: ReactNode;
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
}

const Button: FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  type = 'button',
}) => {
  const baseClasses = 'font-medium rounded-lg transition-colors';
  
  const variantClasses = {
    primary: 'bg-primary-600 hover:bg-primary-700 text-white',
    secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-900',
    ghost: 'bg-transparent hover:bg-gray-100 text-gray-700',
  };
  
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  const disabledClasses = disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer';

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${disabledClasses}`}
    >
      {children}
    </button>
  );
};

export default Button;
```

## Common Patterns

### 1. Form Input Component

```tsx
import type { FC, InputHTMLAttributes } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  helperText?: string;
}

const Input: FC<InputProps> = ({ label, error, helperText, ...props }) => {
  return (
    <div className="w-full">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        {label}
      </label>
      <input
        {...props}
        className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:outline-none ${
          error
            ? 'border-error-500 focus:ring-error-200'
            : 'border-gray-300 focus:ring-primary-200'
        }`}
      />
      {error && <p className="text-sm text-error-600 mt-1">{error}</p>}
      {helperText && !error && <p className="text-sm text-gray-500 mt-1">{helperText}</p>}
    </div>
  );
};
```

### 2. Card Component

```tsx
import type { FC, ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  title?: string;
  className?: string;
  padding?: 'sm' | 'md' | 'lg';
}

const Card: FC<CardProps> = ({ children, title, className = '', padding = 'md' }) => {
  const paddingClasses = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };

  return (
    <div className={`bg-white rounded-lg shadow-md ${paddingClasses[padding]} ${className}`}>
      {title && <h3 className="text-xl font-semibold mb-4">{title}</h3>}
      {children}
    </div>
  );
};
```

### 3. Modal Component

```tsx
import type { FC, ReactNode } from 'react';
import { X } from 'lucide-react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
}

const Modal: FC<ModalProps> = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black bg-opacity-50" onClick={onClose} />
      
      {/* Modal */}
      <div className="relative bg-white rounded-lg shadow-xl max-w-md w-full mx-4 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold">{title}</h2>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>
        {children}
      </div>
    </div>
  );
};
```

### 4. Loading Skeleton

```tsx
const LoadingSkeleton: FC = () => {
  return (
    <div className="animate-pulse space-y-4">
      <div className="h-4 bg-gray-200 rounded w-3/4"></div>
      <div className="h-4 bg-gray-200 rounded w-1/2"></div>
      <div className="h-4 bg-gray-200 rounded w-5/6"></div>
    </div>
  );
};
```

## Hooks Examples

### Custom Hook: useDebounce

```tsx
import { useState, useEffect } from 'react';

export const useDebounce = <T,>(value: T, delay: number): T => {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};
```

### Custom Hook: useLocalStorage

```tsx
import { useState, useEffect } from 'react';

export const useLocalStorage = <T,>(key: string, initialValue: T) => {
  const [value, setValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(error);
    }
  }, [key, value]);

  return [value, setValue] as const;
};
```

## Zustand Store Example

```tsx
import { create } from 'zustand';
import type { User } from '@/types';

interface AuthState {
  user: User | null;
  accessToken: string | null;
  isAuthenticated: boolean;
  login: (user: User, token: string) => void;
  logout: () => void;
  updateUser: (user: Partial<User>) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  accessToken: null,
  isAuthenticated: false,
  
  login: (user, token) =>
    set({
      user,
      accessToken: token,
      isAuthenticated: true,
    }),
  
  logout: () =>
    set({
      user: null,
      accessToken: null,
      isAuthenticated: false,
    }),
  
  updateUser: (updates) =>
    set((state) => ({
      user: state.user ? { ...state.user, ...updates } : null,
    })),
}));
```

## Service Layer Example

```tsx
import axios from '@/config/axios';
import type { User, LoginCredentials, SignupData, AuthTokens } from '@/types';

export const authService = {
  async login(credentials: LoginCredentials): Promise<{ user: User; tokens: AuthTokens }> {
    const response = await axios.post('/auth/login', credentials);
    return response.data;
  },

  async signup(data: SignupData): Promise<{ user: User; tokens: AuthTokens }> {
    const response = await axios.post('/auth/signup', data);
    return response.data;
  },

  async logout(): Promise<void> {
    await axios.post('/auth/logout');
  },

  async refreshToken(refreshToken: string): Promise<AuthTokens> {
    const response = await axios.post('/auth/refresh', { refreshToken });
    return response.data;
  },
};
```

## Form with React Hook Form

```tsx
import { useForm } from 'react-hook-form';
import type { LoginCredentials } from '@/types';

const LoginForm: FC = () => {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginCredentials>();

  const onSubmit = async (data: LoginCredentials) => {
    try {
      // Call API
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-1">אימייל</label>
        <input
          {...register('email', { required: 'שדה חובה' })}
          type="email"
          className="w-full px-4 py-2 border rounded-lg"
        />
        {errors.email && <p className="text-sm text-error-600 mt-1">{errors.email.message}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">סיסמה</label>
        <input
          {...register('password', { required: 'שדה חובה' })}
          type="password"
          className="w-full px-4 py-2 border rounded-lg"
        />
        {errors.password && (
          <p className="text-sm text-error-600 mt-1">{errors.password.message}</p>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
      >
        {isSubmitting ? 'מתחבר...' : 'התחבר'}
      </button>
    </form>
  );
};
```

## Naming Conventions

- **Components**: PascalCase (e.g., `Button.tsx`, `UserCard.tsx`)
- **Hooks**: camelCase with "use" prefix (e.g., `useAuth.ts`, `useDebounce.ts`)
- **Utils**: camelCase (e.g., `formatters.ts`, `validators.ts`)
- **Types**: PascalCase (e.g., `User`, `Receipt`, `AuthState`)
- **Services**: camelCase with ".service" suffix (e.g., `auth.service.ts`)
- **Stores**: camelCase with ".store" suffix (e.g., `auth.store.ts`)

## File Organization

```
components/ui/Button/
├── Button.tsx          # Main component
├── Button.test.tsx     # Tests (future)
└── index.ts            # Re-export

// Or simpler:
components/ui/
├── Button.tsx
├── Input.tsx
└── index.ts            # Export all
```

## Testing (Future Setup)

```tsx
import { render, screen } from '@testing-library/react';
import Button from './Button';

describe('Button', () => {
  it('renders children correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    screen.getByText('Click me').click();
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

---

**Remember:** Always use TypeScript types, follow RTL design principles, and keep components small and focused!
