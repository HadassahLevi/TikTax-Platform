# Dashboard Page - Visual Structure

## Layout Preview

```
┌────────────────────────────────────────────────────────────────────┐
│ Header: Tik-Tax Logo                    [Settings] [Profile Icon] │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│ לוח בקרה                                        [+ הוסף קבלה]    │
│ שלום, David Cohen                                                  │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│ ⚠️ אתה מתקרב למכסת הקבלות                     [שדרג תוכנית]     │
│ נותרו לך 5 קבלות החודש                                           │
└────────────────────────────────────────────────────────────────────┘

┌─────────────┬─────────────┬─────────────┬─────────────┐
│  💰         │  📄         │  📁         │  📅         │
│ הוצאות      │ קבלות       │ סך כל      │ קבלות       │
│ החודש       │ החודש       │ הקבלות     │ שנותרו      │
│             │             │             │             │
│ ₪3,245.80   │    12       │    45       │    15       │
│             │             │             │             │
│ 📈 +12.5%   │ ממוצע:      │ ₪12,458.30  │ ▓▓▓▓▓░░░░░ │
│ לעומת חודש  │ ₪270.48     │ סך הכל      │             │
│ שעבר        │             │             │             │
└─────────────┴─────────────┴─────────────┴─────────────┘

┌───────────────────────────────┬───────────────────────────────┐
│ קטגוריות מובילות              │ קבלות אחרונות   [הצג הכל]    │
│                               │                               │
│       ┌─────────────┐         │ ┌──┬─────────────────────────┐│
│       │    ●●●●     │         │ │📷│ רמי לוי שיווק השקמה    ││
│       │  ●     ●    │         │ │  │ ₪125.40    15/03/2025  ││
│       │ ●   ○   ●   │         │ │  │ ציוד משרדי              ││
│       │  ●     ●    │         │ └──┴─────────────────────────┘│
│       │    ●●●●     │         │                               │
│       └─────────────┘         │ ┌──┬─────────────────────────┐│
│                               │ │📷│ קפה ג'ו                 ││
│ ● ציוד משרדי      ₪890.50    │ │  │ ₪45.00     14/03/2025  ││
│                   5 קבלות     │ │  │ אירוח ואוכל            ││
│                               │ └──┴─────────────────────────┘│
│ ● שיווק ופרסום    ₪750.00    │                               │
│                   3 קבלות     │ ┌──┬─────────────────────────┐│
│                               │ │📷│ סופר-פארם              ││
│ ● נסיעות         ₪620.30     │ │  │ ₪89.90     13/03/2025  ││
│                   8 קבלות     │ │  │ ציוד משרדי              ││
│                               │ └──┴─────────────────────────┘│
│ ● אירוח ואוכל     ₪485.00    │                               │
│                   10 קבלות    │ [Empty State If No Receipts]  │
│                               │ ┌──────────────────────────┐  │
│ ● שכירות          ₪500.00    │ │      📄                  │  │
│                   1 קבלות     │ │  אין עדיין קבלות        │  │
└───────────────────────────────┤ │  [+ הוסף קבלה ראשונה]  │  │
                                │ └──────────────────────────┘  │
                                └───────────────────────────────┘

┌─────────────────┬─────────────────┬─────────────────┐
│ ┌─────────────┐ │ ┌─────────────┐ │ ┌─────────────┐ │
│ │      ➕     │ │ │      📥     │ │ │      📁     │ │
│ │             │ │ │             │ │ │             │ │
│ │ הוסף קבלה   │ │ │ ייצוא       │ │ │ צפה         │ │
│ │ חדשה        │ │ │ לאקסל       │ │ │ בארכיון     │ │
│ │             │ │ │             │ │ │             │ │
│ │ צלם או      │ │ │ הורד דוח    │ │ │ כל הקבלות  │ │
│ │ העלה קבלה   │ │ │ לרו"ח       │ │ │ שלך         │ │
│ └─────────────┘ │ └─────────────┘ │ └─────────────┘ │
└─────────────────┴─────────────────┴─────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│ Footer: [🏠 Home] [📁 Archive] [👤 Profile]                        │
└────────────────────────────────────────────────────────────────────┘
```

---

## Mobile Layout (< 768px)

```
┌──────────────────────────┐
│ [☰] Tik-Tax      [⚙️][👤]│
├──────────────────────────┤
│ לוח בקרה                 │
│ שלום, David              │
├──────────────────────────┤
│ ⚠️ אתה מתקרב למכסה      │
│ [שדרג תוכנית]           │
├──────────────────────────┤
│ ┌──────────────────────┐ │
│ │ 💰 הוצאות החודש      │ │
│ │ ₪3,245.80            │ │
│ │ 📈 +12.5%            │ │
│ └──────────────────────┘ │
│ ┌──────────────────────┐ │
│ │ 📄 קבלות החודש      │ │
│ │ 12                   │ │
│ │ ממוצע: ₪270.48      │ │
│ └──────────────────────┘ │
│ ┌──────────────────────┐ │
│ │ 📁 סך כל הקבלות     │ │
│ │ 45                   │ │
│ │ ₪12,458.30          │ │
│ └──────────────────────┘ │
│ ┌──────────────────────┐ │
│ │ 📅 קבלות שנותרו     │ │
│ │ 15                   │ │
│ │ ▓▓▓▓▓░░░░░          │ │
│ └──────────────────────┘ │
├──────────────────────────┤
│ קטגוריות מובילות         │
│                          │
│    ┌──────────┐          │
│    │  Pie     │          │
│    │  Chart   │          │
│    └──────────┘          │
│                          │
│ ● ציוד משרדי   ₪890.50  │
│ ● שיווק       ₪750.00   │
│ ● נסיעות      ₪620.30   │
├──────────────────────────┤
│ קבלות אחרונות [הכל]     │
│                          │
│ ┌────────────────────┐   │
│ │📷 רמי לוי          │   │
│ │₪125.40  15/03/2025 │   │
│ └────────────────────┘   │
│ ┌────────────────────┐   │
│ │📷 קפה ג'ו          │   │
│ │₪45.00   14/03/2025 │   │
│ └────────────────────┘   │
├──────────────────────────┤
│ ┌──────────────────────┐ │
│ │  ➕ הוסף קבלה       │ │
│ │  צלם או העלה קבלה   │ │
│ └──────────────────────┘ │
│ ┌──────────────────────┐ │
│ │  📥 ייצוא לאקסל     │ │
│ │  הורד דוח לרו"ח     │ │
│ └──────────────────────┘ │
│ ┌──────────────────────┐ │
│ │  📁 צפה בארכיון     │ │
│ │  כל הקבלות שלך      │ │
│ └──────────────────────┘ │
├──────────────────────────┤
│ [🏠] [📁] [👤]          │
└──────────────────────────┘
```

---

## Color Guide

### Quick Stats Icons
```
💰 Monthly Expenses:   bg-primary-100 (light blue) / text-primary-600 (blue)
📄 Receipts Count:     bg-green-100 (light green) / text-green-600 (green)
📁 Total Receipts:     bg-blue-100 (light blue) / text-blue-600 (blue)
📅 Receipts Remaining: bg-purple-100 (light purple) / text-purple-600 (purple)
```

### Trend Indicators
```
📈 Increase: text-red-600 (red - bad for expenses)
📉 Decrease: text-green-600 (green - good for expenses)
```

### Usage Warning
```
⚠️ Warning (80-99%):  bg-yellow-50 / border-yellow-200 / text-yellow-600
🔴 Alert (100%+):     bg-red-50 / border-red-200 / text-red-600
```

### Category Chart Colors
```
● Cyan:    #06B6D4 (Equipment & Technology)
● Blue:    #3B82F6 (Office Supplies)
● Purple:  #8B5CF6 (Professional Services)
● Red:     #EF4444 (Marketing)
● Green:   #10B981 (Travel)
● Orange:  #F59E0B (Meals)
● Indigo:  #6366F1 (Rent)
● Lime:    #84CC16 (Maintenance)
● Teal:    #14B8A6 (Insurance)
● Violet:  #A855F7 (Bank Fees)
● Pink:    #EC4899 (Education)
● Tangerine: #F97316 (Subscriptions)
● Gray:    #6B7280 (Other)
```

---

## Interactive Elements

### Clickable Areas
```
✅ Header "הוסף קבלה" button → /receipts/new
✅ Each stat card → (future: filter by metric)
✅ Chart segments → (future: filter by category)
✅ Each recent receipt card → /receipts/:id
✅ "הצג הכל" link → /archive
✅ "הוסף קבלה חדשה" card → /receipts/new
✅ "ייצוא לאקסל" card → /export
✅ "צפה בארכיון" card → /archive
✅ "שדרג תוכנית" button → /profile#subscription
```

### Hover Effects
```
• Stat cards: subtle shadow increase
• Recent receipt cards: bg-gray-50
• Quick action cards: lift + shadow increase
• "הוסף קבלה" card: border color change (dashed → solid)
• All buttons: color darken + shadow
```

---

## Animation Timing

```
Page Load:        fade-in 0.3s
Card Hover:       0.2s ease
Button Click:     0.15s ease
Chart Render:     0.5s ease-out
Skeleton Pulse:   1.5s infinite
Progress Bar:     0.3s ease (on update)
```

---

## Spacing & Sizing

```
Page Padding:       16px (mobile) / 24px (tablet) / 32px (desktop)
Section Gap:        24px (6 in Tailwind)
Card Gap:           16px (4 in Tailwind)
Card Padding:       16px (sm) / 24px (lg)
Icon Size (small):  20px
Icon Size (medium): 24px
Icon Size (large):  32px
Chart Height:       300px
Thumbnail Size:     64×64px (w-16 h-16)
```

---

## Typography Scale

```
Page Title:         32px / 40px (text-3xl)
Section Title:      20px / 28px (text-xl)
Card Title:         18px / 28px (text-lg)
Stat Amount:        28px / 36px (text-2xl)
Body Text:          16px / 24px (text-base)
Small Text:         14px / 20px (text-sm)
Extra Small:        13px / 18px (text-xs)
```

---

## Border Radius

```
Small (badges):     4px (rounded)
Standard (cards):   8px (rounded-lg)
Large (icons bg):   12px (rounded-xl)
Circle (progress):  9999px (rounded-full)
```

---

## Shadows

```
Small (cards):      0 1px 3px rgba(0,0,0,0.08)
Medium (hover):     0 4px 8px rgba(0,0,0,0.12)
Large (active):     0 10px 15px rgba(0,0,0,0.15)
```

---

**Visual Reference Complete**  
Use this as a design guide during implementation and reviews.
