# StatCard Component - Quick Reference

## Import
```typescript
import { StatCard } from '@/components/ui';
```

## Props
```typescript
interface StatCardProps {
  label: string;                           // Required
  value: string | number;                  // Required
  icon?: LucideIcon;
  iconColor?: string;                      // Default: 'text-gray-400'
  change?: number;                         // Percentage change
  changeLabel?: string;                    // e.g., 'vs last month'
  gradient?: boolean;                      // Default: false
  gradientColors?: { from: string; to: string };
  onClick?: () => void;
  className?: string;
}
```

## Basic Usage
```tsx
<StatCard
  label="סך הוצאות החודש"
  value="₪12,345.67"
/>
```

## With Icon
```tsx
import { Receipt } from 'lucide-react';

<StatCard
  label="קבלות החודש"
  value={42}
  icon={Receipt}
  iconColor="text-blue-500"
/>
```

## With Percentage Change
```tsx
<StatCard
  label="הוצאות החודש"
  value="₪8,500.00"
  change={12.5}
  changeLabel="לעומת חודש קודם"
/>
```

## Negative Change
```tsx
<StatCard
  label="קבלות ממתינות"
  value={3}
  change={-40}
  changeLabel="לעומת שבוע שעבר"
/>
```

## Gradient Background
```tsx
<StatCard
  label="יתרה כוללת"
  value="₪98,765.43"
  gradient
  gradientColors={{ from: 'from-blue-500', to: 'to-blue-700' }}
/>
```

## Clickable Stat
```tsx
<StatCard
  label="קבלות להשלמה"
  value={5}
  onClick={() => navigate('/pending')}
  icon={AlertCircle}
  iconColor="text-amber-500"
/>
```

## Complete Example
```tsx
import { TrendingUp } from 'lucide-react';

<StatCard
  label="הכנסות החודש"
  value="₪45,678.90"
  icon={TrendingUp}
  iconColor="text-emerald-500"
  change={23.8}
  changeLabel="לעומת חודש קודם"
  gradient
  gradientColors={{ from: 'from-emerald-500', to: 'to-emerald-700' }}
  onClick={() => viewDetails()}
/>
```

## Dashboard Grid Layout
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
  <StatCard label="סה״כ הוצאות" value="₪12,345" />
  <StatCard label="קבלות" value={42} change={15} />
  <StatCard label="ממוצע לקבלה" value="₪294" />
  <StatCard label="קטגוריות" value={8} />
</div>
```

## Change Indicator Colors
- **Positive** (+): Green (text-emerald-600) with TrendingUp icon
- **Negative** (-): Red (text-red-600) with TrendingDown icon
- **Gradient mode**: White text with reduced opacity

## Typography
- **Label**: 14px, medium weight, gray-600
- **Value**: 32px (3xl), semibold, monospace font
- **Change**: 14px, medium weight, color-coded
- **Change Label**: 12px, gray-500

## Spacing
- Default padding: lg (32px)
- Icon padding: 12px
- Gap between elements: 8-12px
