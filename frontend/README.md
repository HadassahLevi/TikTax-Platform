# Tik-Tax Frontend# React + TypeScript + Vite



A Hebrew-first, RTL-optimized fintech web application built with React 18.2, TypeScript, and Tailwind CSS.This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.



## 🚀 Tech StackCurrently, two official plugins are available:



### Core- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh

- **React** 18.2.0 - UI library- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

- **TypeScript** 5.9.3 - Type safety

- **Vite** 7.x - Build tool and dev server## React Compiler



### StylingThe React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

- **Tailwind CSS** 3.3.x - Utility-first CSS framework

- **@tailwindcss/forms** - Form styling plugin## Expanding the ESLint configuration

- **Rubik Font** - Hebrew-optimized Google Font

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

### State Management & Routing

- **Zustand** 4.4.7 - Lightweight state management```js

- **React Router** 6.20.0 - Client-side routingexport default defineConfig([

  globalIgnores(['dist']),

### Forms & Validation  {

- **React Hook Form** 7.49.2 - Performant form handling    files: ['**/*.{ts,tsx}'],

    extends: [

### UI & UX      // Other configs...

- **Lucide React** 0.294.0 - Icon library

- **Framer Motion** 10.16.16 - Animations      // Remove tseslint.configs.recommended and replace with this

- **Recharts** 2.10.3 - Data visualization      tseslint.configs.recommendedTypeChecked,

      // Alternatively, use this for stricter rules

### Utilities      tseslint.configs.strictTypeChecked,

- **Axios** 1.6.2 - HTTP client      // Optionally, add this for stylistic rules

- **date-fns** 3.0.0 - Date utilities      tseslint.configs.stylisticTypeChecked,

- **React Dropzone** - File upload

- **React OTP Input** - SMS verification      // Other configs...

    ],

### Development Tools    languageOptions: {

- **ESLint** 9.x - Code linting      parserOptions: {

- **Prettier** 3.1.1 - Code formatting        project: ['./tsconfig.node.json', './tsconfig.app.json'],

- **TypeScript ESLint** 8.x - TypeScript-specific linting        tsconfigRootDir: import.meta.dirname,

      },

## 📁 Project Structure      // other options...

    },

```  },

frontend/])

├── src/```

│   ├── components/          # React components

│   │   ├── ui/             # Reusable UI components (Button, Input, Card, Modal)You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

│   │   ├── layout/         # Layout components (Header, Footer, Navigation)

│   │   ├── receipt/        # Receipt-specific components```js

│   │   ├── category/       # Category management components// eslint.config.js

│   │   ├── loading/        # Loading states and skeletonsimport reactX from 'eslint-plugin-react-x'

│   │   └── export/         # Export functionality componentsimport reactDom from 'eslint-plugin-react-dom'

│   ├── pages/              # Page components

│   │   ├── auth/           # Authentication pages (Login, Signup)export default defineConfig([

│   │   └── receipts/       # Receipt management pages  globalIgnores(['dist']),

│   ├── services/           # API services (auth, receipt, user)  {

│   ├── hooks/              # Custom React hooks    files: ['**/*.{ts,tsx}'],

│   ├── stores/             # Zustand state management stores    extends: [

│   ├── utils/              # Utility functions (formatters, validators, helpers)      // Other configs...

│   ├── types/              # TypeScript type definitions      // Enable lint rules for React

│   ├── contexts/           # React contexts (Toast, Theme)      reactX.configs['recommended-typescript'],

│   ├── config/             # Configuration files      // Enable lint rules for React DOM

│   ├── constants/          # Constants (categories, status values)      reactDom.configs.recommended,

│   └── assets/             # Static assets    ],

│       ├── images/         # Image files    languageOptions: {

│       └── icons/          # Icon files      parserOptions: {

├── public/                 # Public static files        project: ['./tsconfig.node.json', './tsconfig.app.json'],

├── eslint.config.js       # ESLint configuration        tsconfigRootDir: import.meta.dirname,

├── .prettierrc            # Prettier configuration      },

├── tailwind.config.js     # Tailwind CSS configuration      // other options...

├── tsconfig.json          # TypeScript configuration    },

├── vite.config.ts         # Vite configuration  },

└── package.json           # Project dependencies and scripts])

``````


## 🎨 Design System

### Color Palette

**Primary Blue** (`#2563EB`)
- Used for primary actions, links, and brand elements
- Shades: 50-900 available as `primary-{shade}`

**Success Green** (`#10B981`)
- Used for success messages and positive actions
- Shades: 50-900 available as `success-{shade}`

**Error Red** (`#EF4444`)
- Used for error messages and destructive actions
- Shades: 50-900 available as `error-{shade}`

**Info Blue** (`#3B82F6`)
- Used for informational messages
- Shades: 50-900 available as `info-{shade}`

**Warning Amber** (`#F59E0B`)
- Used for warning messages and caution
- Shades: 50-900 available as `warning-{shade}`

### Typography

- **Font Family**: Rubik (optimized for Hebrew)
- **Weights**: 300 (light), 400 (regular), 500 (medium), 600 (semi-bold), 700 (bold)

### Breakpoints

- **sm**: 640px (Mobile)
- **md**: 768px (Tablet)
- **lg**: 1024px (Desktop)
- **xl**: 1280px (Large Desktop)
- **2xl**: 1536px (Extra Large)

## 🌐 RTL (Right-to-Left) Support

The application is optimized for Hebrew with full RTL support:

1. Set `dir="rtl"` on the `<html>` element for Hebrew interface
2. Tailwind automatically handles RTL layout adjustments
3. Use Rubik font for optimal Hebrew rendering

## 🛠️ Getting Started

### Prerequisites

- **Node.js**: 20.17.0 or higher
- **npm**: 10.8.2 or higher

### Installation

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies** (if not already done):
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

4. **Open in browser**:
   Navigate to `http://localhost:5173`

## 📜 Available Scripts

### Development
```bash
npm run dev          # Start Vite dev server with HMR
```

### Build
```bash
npm run build        # Type-check and build for production
npm run preview      # Preview production build locally
```

### Code Quality
```bash
npm run lint         # Run ESLint
npm run format       # Format code with Prettier
npm run format:check # Check code formatting
npm run type-check   # Run TypeScript type checking
```

## 🔧 Path Aliases

The project uses path aliases for cleaner imports:

```typescript
import Button from '@/components/ui/Button';
import { useAuth } from '@/hooks/useAuth';
import { authService } from '@/services/auth.service';
import { User } from '@/types/user';
```

Available aliases:
- `@/*` → `src/*`
- `@components/*` → `src/components/*`
- `@pages/*` → `src/pages/*`
- `@services/*` → `src/services/*`
- `@hooks/*` → `src/hooks/*`
- `@stores/*` → `src/stores/*`
- `@utils/*` → `src/utils/*`
- `@types/*` → `src/types/*`
- `@contexts/*` → `src/contexts/*`
- `@config/*` → `src/config/*`
- `@constants/*` → `src/constants/*`
- `@assets/*` → `src/assets/*`

## 🎯 Best Practices

### TypeScript
- **Strict mode enabled**: All strict TypeScript checks are active
- **No implicit any**: Always define types explicitly
- **Type-first development**: Define types before implementation

### React
- **Functional components**: Use hooks, avoid class components
- **Component composition**: Build small, reusable components
- **Props typing**: Always type component props

### Styling
- **Tailwind-first**: Use Tailwind utilities before custom CSS
- **Mobile-first**: Design for mobile, enhance for desktop
- **RTL-aware**: Test all components in RTL mode

### State Management
- **Zustand stores**: For global state (auth, user preferences)
- **React Query**: For server state (future implementation)
- **Local state**: For UI-only state

### Code Quality
- **ESLint**: Fix all linting errors before committing
- **Prettier**: Format code automatically
- **Type-check**: Run type-check before builds

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:3000/api
VITE_GOOGLE_VISION_API_KEY=your_key_here
VITE_AWS_S3_BUCKET=your_bucket_here
```

Access in code:
```typescript
const apiUrl = import.meta.env.VITE_API_URL;
```

## 📦 Build Output

```bash
npm run build
```

- Output directory: `dist/`
- Optimized for production
- Code splitting enabled
- Source maps generated

## 🧪 Testing (Future)

Testing setup to be added:
- **Vitest** - Unit testing
- **React Testing Library** - Component testing
- **Playwright** - E2E testing

## 🚢 Deployment

### Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### Netlify
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

### Manual
1. Build the project: `npm run build`
2. Upload `dist/` folder to your hosting provider

## 📝 Contributing

1. Follow the existing code style
2. Run `npm run lint` and `npm run format` before committing
3. Ensure `npm run type-check` passes
4. Test in both LTR and RTL modes
5. Mobile-first responsive design

## 📄 License

Private project - All rights reserved

## 👥 Team

Tik-Tax Development Team

---

**Built with ❤️ for Israeli small businesses**
