# Dashboard Page - Quick Reference

**File:** `/src/pages/dashboard/DashboardPage.tsx`  
**Route:** `/dashboard`  
**Auth:** Required ✅

---

## Overview

Main dashboard page displaying expense statistics, visualizations, and quick actions.

**Key Features:**
- Monthly expense summary with trends
- Top 5 categories pie chart
- Recent receipts list (last 5)
- Quick action cards
- Usage indicator (receipts remaining)
- Empty states for new users

---

## Usage

```tsx
import { DashboardPage } from '@/pages/dashboard';

// In router
<Route path="/dashboard" element={<DashboardPage />} />
```

---

## Component Structure

```
DashboardPage
├── PageContainer (title, subtitle, action button)
│
├── Usage Warning Banner (conditional, ≥80% usage)
│
├── Quick Stats Grid (4 cards)
│   ├── Monthly Expenses (with trend)
│   ├── Receipts This Month (with average)
│   ├── Total Receipts
│   └── Receipts Remaining (with progress bar)
│
├── Main Content Grid (2 columns)
│   ├── Top Categories Chart (pie chart)
│   └── Recent Receipts List
│
└── Quick Actions Grid (3 cards)
    ├── Add Receipt
    ├── Export to Excel
    └── View Archive
```

---

## Data Dependencies

### From useAuth:
```typescript
const { 
  user,                  // User info for greeting
  remainingReceipts,     // Function: receipts left this month
  usagePercentage        // Function: 0-100 usage %
} = useAuth();
```

### From useReceipt:
```typescript
const { 
  statistics,            // Statistics object
  isLoadingStats,        // Loading state
  fetchStatistics        // Refresh function
} = useReceipt();
```

### Statistics Object:
```typescript
interface ReceiptStatistics {
  totalReceipts: number;
  totalAmount: number;
  thisMonth: {
    count: number;
    amount: number;
  };
  lastMonth: {
    count: number;
    amount: number;
  };
  byCategory: Array<{
    categoryId: string;
    category: ExpenseCategory;
    count: number;
    amount: number;
  }>;
  recentReceipts: Receipt[];  // Last 10
}
```

---

## Quick Stats Cards

### 1. Monthly Expenses
```tsx
<Card>
  <DollarSign icon />
  <Amount>{statistics.thisMonth.amount}</Amount>
  <Trend>
    {monthChange >= 0 ? <TrendingUp /> : <TrendingDown />}
    {monthChange}% vs last month
  </Trend>
</Card>
```

**Calculation:**
```typescript
const monthChange = statistics.lastMonth.amount > 0
  ? ((statistics.thisMonth.amount - statistics.lastMonth.amount) / statistics.lastMonth.amount) * 100
  : 0;
```

### 2. Receipts This Month
```tsx
<Card>
  <Receipt icon />
  <Count>{statistics.thisMonth.count}</Count>
  <Average>
    Average: {thisMonth.amount / thisMonth.count}
  </Average>
</Card>
```

### 3. Total Receipts
```tsx
<Card>
  <FileText icon />
  <Total>{statistics.totalReceipts}</Total>
  <TotalAmount>{statistics.totalAmount}</TotalAmount>
</Card>
```

### 4. Receipts Remaining
```tsx
<Card>
  <Calendar icon />
  <Remaining>{remainingReceipts()}</Remaining>
  <ProgressBar value={usagePercentage()} />
</Card>
```

---

## Top Categories Chart

### Chart Data Preparation:
```typescript
const chartData = statistics.byCategory
  .slice(0, 5)  // Top 5 only
  .map(cat => ({
    name: cat.category.nameHe,
    value: cat.amount,
    color: cat.category.color
  }));
```

### Recharts Integration:
```tsx
<PieChart>
  <Pie
    data={chartData}
    cx="50%"
    cy="50%"
    outerRadius={100}
    dataKey="value"
    label={(entry) => `${entry.name}: ${percentage}%`}
  >
    {chartData.map((entry, index) => (
      <Cell key={index} fill={entry.color} />
    ))}
  </Pie>
  <Tooltip formatter={(value) => formatAmount(value)} />
</PieChart>
```

### Legend Below Chart:
```tsx
{statistics.byCategory.slice(0, 5).map(cat => (
  <div key={cat.categoryId}>
    <ColorDot color={cat.category.color} />
    <CategoryName>{cat.category.nameHe}</CategoryName>
    <Amount>{formatAmount(cat.amount)}</Amount>
    <Count>{cat.count} קבלות</Count>
  </div>
))}
```

---

## Recent Receipts List

### Receipt Card:
```tsx
<div onClick={() => navigate(`/receipts/${receipt.id}`)}>
  <Thumbnail src={receipt.imageUrl} />
  <VendorName>{receipt.vendorName}</VendorName>
  <Amount>{formatAmount(receipt.totalAmount)}</Amount>
  <Date>{formatDateIL(receipt.date)}</Date>
  <Category color={category.color}>
    {category.nameHe}
  </Category>
</div>
```

**Shows:** Last 5 receipts from `statistics.recentReceipts`  
**Action:** Click → navigate to receipt detail

---

## Usage Warning Banner

**Triggers:**
- Shows when `usagePercentage() >= 80`

**Levels:**
```typescript
// Yellow warning (80-99%)
if (usageLevel >= 80 && usageLevel < 100) {
  message: 'אתה מתקרב למכסת הקבלות'
  detail: `נותרו לך ${remainingReceipts()} קבלות החודש`
  buttonVariant: 'secondary'
}

// Red error (100%+)
if (usageLevel >= 100) {
  message: 'הגעת למכסת הקבלות החודשית'
  detail: 'שדרג את התוכנית שלך כדי להמשיך להעלות קבלות'
  buttonVariant: 'danger'
}
```

**Action:** Click "שדרג תוכנית" → navigate to `/profile#subscription`

---

## Quick Action Cards

### 1. Add Receipt
```tsx
<Card onClick={() => navigate('/receipts/new')}>
  <Plus icon />
  <Title>הוסף קבלה חדשה</Title>
  <Description>צלם או העלה קבלה</Description>
</Card>
```
**Style:** Dashed border, primary colors

### 2. Export to Excel
```tsx
<Card onClick={() => navigate('/export')}>
  <Download icon />
  <Title>ייצוא לאקסל</Title>
  <Description>הורד דוח לרו"ח</Description>
</Card>
```

### 3. View Archive
```tsx
<Card onClick={() => navigate('/archive')}>
  <FileText icon />
  <Title>צפה בארכיון</Title>
  <Description>כל הקבלות שלך</Description>
</Card>
```

---

## Empty States

### No Statistics Available:
```tsx
if (!statistics) {
  return (
    <PageContainer title="לוח בקרה">
      <p>לא ניתן לטעון נתונים</p>
    </PageContainer>
  );
}
```

### No Categories (Chart):
```tsx
{chartData.length === 0 && (
  <EmptyState>
    <FileText icon />
    <Message>אין עדיין קבלות</Message>
    <Hint>התחל להעלות קבלות לראות סטטיסטיקות</Hint>
  </EmptyState>
)}
```

### No Recent Receipts:
```tsx
{statistics.recentReceipts.length === 0 && (
  <EmptyState>
    <Receipt icon />
    <Message>אין עדיין קבלות</Message>
    <Button onClick={() => navigate('/receipts/new')}>
      הוסף קבלה ראשונה
    </Button>
  </EmptyState>
)}
```

---

## Loading States

### Initial Load:
```tsx
if (isLoadingStats && !statistics) {
  return <PageContainer title="לוח בקרה" loading={true} />;
}
```

**Shows:** PageContainer skeleton loader

### Background Refresh:
```tsx
useEffect(() => {
  fetchStatistics();  // Refresh on mount
}, []);
```

**Note:** Loading state NOT shown on refresh (existing data remains visible)

---

## Responsive Design

### Breakpoints:

**Mobile (< 768px):**
- Quick stats: 1 column
- Main content: 1 column
- Quick actions: 1 column

**Tablet (768px - 1024px):**
- Quick stats: 2 columns
- Main content: 2 columns
- Quick actions: 3 columns

**Desktop (> 1024px):**
- Quick stats: 4 columns
- Main content: 2 columns (lg:grid-cols-2)
- Quick actions: 3 columns

---

## Navigation Paths

| Action | Route | Description |
|--------|-------|-------------|
| Add Receipt | `/receipts/new` | Upload new receipt |
| Export | `/export` | Download Excel report |
| Archive | `/archive` | View all receipts |
| Receipt Detail | `/receipts/:id` | View specific receipt |
| Upgrade Plan | `/profile#subscription` | Subscription settings |

---

## Color System

### Stat Card Icons:
- **Monthly Expenses:** `bg-primary-100` / `text-primary-600`
- **Receipts Count:** `bg-green-100` / `text-green-600`
- **Total Receipts:** `bg-blue-100` / `text-blue-600`
- **Remaining:** `bg-purple-100` / `text-purple-600`

### Trends:
- **Increase (bad):** `text-red-600` with `<TrendingUp />`
- **Decrease (good):** `text-green-600` with `<TrendingDown />`

### Usage Warning:
- **80-99%:** Yellow (`bg-yellow-50`, `border-yellow-200`)
- **100%+:** Red (`bg-red-50`, `border-red-200`)

---

## Accessibility

✅ **Semantic HTML:** Proper headings, landmarks  
✅ **Keyboard Navigation:** All cards are tabbable  
✅ **Screen Readers:** Descriptive labels and ARIA  
✅ **Focus Indicators:** Visible focus rings  
✅ **Color Contrast:** WCAG 2.1 AA compliant

---

## Performance

### Data Fetching:
- Uses `useLoadStatistics()` hook
- Auto-fetches on mount if not loaded
- Manual refresh with `fetchStatistics()`

### Chart Rendering:
- Recharts lazy loads
- Only top 5 categories rendered
- Responsive container handles resizing

### Image Loading:
- Receipt thumbnails are lazy loaded
- 16x16 thumbnails (small size)

---

## Related Components

- `PageContainer` - Page wrapper
- `Button` - All action buttons
- `Card` - All card containers
- `useReceipt` - Statistics hook
- `useAuth` - User and usage info

---

## Future Enhancements

- [ ] Date range selector for statistics
- [ ] Category filter for pie chart
- [ ] Line chart for expense trends
- [ ] Comparison with previous months
- [ ] Export statistics directly
- [ ] Customizable dashboard widgets
- [ ] Goal tracking (budget limits)

---

**Last Updated:** 2025-11-03  
**Author:** GitHub Copilot  
**Status:** ✅ Complete
