# Export Page - Visual Layout Guide

## 📐 Desktop Layout (> 1024px)

```
┌────────────────────────────────────────────────────────────────────────┐
│                          EXPORT PAGE HEADER                            │
│                    ייצוא נתונים                                        │
│              הורד דוח מסודר לרואה חשבון                                │
└────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────┬─────────────────────────┐
│ LEFT COLUMN (2/3 width)                      │ RIGHT COLUMN (1/3)      │
│                                              │                         │
│ ┌──────────────────────────────────────────┐ │ ┌─────────────────────┐ │
│ │ 📊 FORMAT SELECTION                      │ │ │ 📋 SUMMARY (STICKY) │ │
│ │ ┌─────┐ ┌─────┐ ┌─────┐                 │ │ │                     │ │
│ │ │ 📊  │ │ 📄  │ │ 📝  │                 │ │ │ קבלות לייצוא:      │ │
│ │ │Excel│ │ PDF │ │ CSV │                 │ │ │       42            │ │
│ │ └─────┘ └─────┘ └─────┘                 │ │ │                     │ │
│ └──────────────────────────────────────────┘ │ │ ─────────────────── │ │
│                                              │ │ סכום כולל:          │ │
│ ┌──────────────────────────────────────────┐ │ │ ₪12,345.67          │ │
│ │ 📅 DATE RANGE                            │ │ │ מע"מ:               │ │
│ │ [החודש] [חודש שעבר] [השנה] [מותאם]     │ │ │ ₪1,866.85           │ │
│ │                                          │ │ │                     │ │
│ │ ┌────────────────────────────────────┐   │ │ │ ─────────────────── │ │
│ │ │ טווח נבחר: 01/11/2025 - 03/11/2025│   │ │ │ פורמט: EXCEL        │ │
│ │ └────────────────────────────────────┘   │ │ │ קטגוריות: 3         │ │
│ └──────────────────────────────────────────┘ │ │                     │ │
│                                              │ │ ┌─────────────────┐ │ │
│ ┌──────────────────────────────────────────┐ │ │ │  הורד דוח  ⬇   │ │ │
│ │ 🏷️ CATEGORY FILTER                       │ │ │ └─────────────────┘ │ │
│ │ ┌────┐ ┌────┐ ┌────┐ ┌────┐             │ │ │                     │ │
│ │ │📦  │ │💼  │ │📢  │ │🚗  │             │ │ │ ▓▓▓▓▓▓▓▓░░ 80%      │ │
│ │ │ציוד│ │שרת.│ │שיוק│ │נסע.│             │ │ └─────────────────────┘ │
│ │ └────┘ └────┘ └────┘ └────┘             │ │                         │
│ │ ┌────┐ ┌────┐ ┌────┐ ┌────┐             │ │ ┌─────────────────────┐ │
│ │ │☕  │ │🏠  │ │💻  │ │🔧  │             │ │ │ 💡 טיפים לייצוא    │ │
│ │ │אוכל│ │שכר.│ │ציוד│ │תחז.│             │ │ │                     │ │
│ │ └────┘ └────┘ └────┘ └────┘             │ │ │ • Excel מומלץ      │ │
│ │ [More categories...]                    │ │ │ • PDF להדפסה       │ │
│ │                                         │ │ │ • CSV למערכות      │ │
│ │ נקה בחירה (3 נבחרו)                    │ │ │ • קובץ נשמר 7 ימים │ │
│ └──────────────────────────────────────────┘ │ └─────────────────────┘ │
│                                              │                         │
│ ┌──────────────────────────────────────────┐ │                         │
│ │ ⚙️ ADDITIONAL OPTIONS                    │ │                         │
│ │ ☑️ כלול תמונות קבלות                     │ │                         │
│ │    יצוצר קובץ ZIP עם התמונות            │ │                         │
│ └──────────────────────────────────────────┘ │                         │
│                                              │                         │
└──────────────────────────────────────────────┴─────────────────────────┘
```

---

## 📱 Mobile Layout (< 640px)

```
┌─────────────────────────────────┐
│   EXPORT PAGE HEADER            │
│   ייצוא נתונים                  │
│   הורד דוח מסודר לרואה חשבון    │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ 📊 FORMAT SELECTION             │
│ ┌─────┐ ┌─────┐ ┌─────┐         │
│ │ 📊  │ │ 📄  │ │ 📝  │         │
│ │Excel│ │ PDF │ │ CSV │         │
│ └─────┘ └─────┘ └─────┘         │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ 📅 DATE RANGE                   │
│ ┌─────────┐ ┌─────────┐         │
│ │ החודש   │ │חודש שעבר│         │
│ └─────────┘ └─────────┘         │
│ ┌─────────┐ ┌─────────┐         │
│ │ השנה    │ │ מותאם   │         │
│ └─────────┘ └─────────┘         │
│                                 │
│ ┌───────────────────────────┐   │
│ │ טווח: 01/11 - 03/11       │   │
│ └───────────────────────────┘   │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ 🏷️ CATEGORY FILTER              │
│ ┌──────┐ ┌──────┐               │
│ │ 📦   │ │ 💼   │               │
│ │ציוד  │ │שרותים│               │
│ └──────┘ └──────┘               │
│ ┌──────┐ ┌──────┐               │
│ │ 📢   │ │ 🚗   │               │
│ │שיווק │ │נסיעות│               │
│ └──────┘ └──────┘               │
│ [More...]                       │
│                                 │
│ נקה בחירה (3)                   │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ ⚙️ OPTIONS                      │
│ ☑️ כלול תמונות                  │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ 📋 SUMMARY                      │
│ קבלות: 42                       │
│ סכום: ₪12,345.67                │
│ מע"מ: ₪1,866.85                 │
│                                 │
│ ┌───────────────────────────┐   │
│ │    הורד דוח ⬇             │   │
│ └───────────────────────────┘   │
│ ▓▓▓▓▓▓▓▓░░ 80%                  │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ 💡 טיפים                        │
│ • Excel מומלץ                   │
│ • PDF להדפסה                    │
└─────────────────────────────────┘
```

---

## 🎨 Component Breakdown

### Format Selection Card
```
┌────────────────────────────────────┐
│ 📄 בחר פורמט ייצוא                │
│                                    │
│  [  📊  ]  [  📄  ]  [  📝  ]      │
│  [ Excel]  [ PDF ]  [ CSV ]        │
│  [מומלץ  ]  [מעוצב ]  [גולמי]      │
│                                    │
│  Selected: Blue border + bg        │
│  Hover: Gray border                │
└────────────────────────────────────┘
```

### Date Range Card
```
┌────────────────────────────────────┐
│ 📅 טווח תאריכים                   │
│                                    │
│  Presets:                          │
│  [החודש] [חודש שעבר] [השנה] [מותאם]│
│                                    │
│  Custom (if selected):             │
│  ┌──────────┐ ┌──────────┐         │
│  │מתאריך:   │ │עד תאריך: │         │
│  │[date]    │ │[date]    │         │
│  └──────────┘ └──────────┘         │
│                                    │
│  ┌──────────────────────────────┐  │
│  │ טווח נבחר: DD/MM - DD/MM    │  │
│  └──────────────────────────────┘  │
└────────────────────────────────────┘
```

### Category Filter Card
```
┌────────────────────────────────────┐
│ סינון לפי קטגוריות (אופציונלי)    │
│                                    │
│  Grid (3 cols desktop, 2 mobile):  │
│  ┌────┐ ┌────┐ ┌────┐              │
│  │ 📦 │ │ 💼 │ │ 📢 │              │
│  │ציוד│ │שרת │ │שוק │              │
│  └────┘ └────┘ └────┘              │
│                                    │
│  Selected: Blue border + bg        │
│  Unselected: Gray border           │
│                                    │
│  נקה בחירה (N נבחרו)               │
└────────────────────────────────────┘
```

### Summary Card (Sticky)
```
┌────────────────────────────────────┐
│ סיכום                              │
│                                    │
│  קבלות לייצוא:          42        │
│  ──────────────────────────        │
│  סכום כולל:      ₪12,345.67       │
│  מע"מ:           ₪1,866.85         │
│  ──────────────────────────        │
│  פורמט: EXCEL                      │
│  קטגוריות: 3                       │
│                                    │
│  ┌──────────────────────────────┐  │
│  │      הורד דוח ⬇              │  │
│  └──────────────────────────────┘  │
│                                    │
│  Progress Bar:                     │
│  ▓▓▓▓▓▓▓▓░░░░░░░░ 60%              │
│                                    │
│  Warning (if no receipts):         │
│  ⚠️ לא נמצאו קבלות                 │
└────────────────────────────────────┘
```

### Tips Card
```
┌────────────────────────────────────┐
│ 💡 טיפים לייצוא                   │
│                                    │
│  • קובץ Excel מומלץ לרוב רואי ח'   │
│  • PDF מתאים להדפסה ולשמירה        │
│  • CSV לעיבוד במערכות אחרות        │
│  • הקובץ יישמר 7 ימים בהיסטוריה   │
│                                    │
│  Background: Blue-50               │
│  Border: Blue-200                  │
└────────────────────────────────────┘
```

---

## 🎭 State Visualization

### Initial State
```
Format: Excel (default)
Date: This Month (default)
Categories: [] (none selected)
Images: false (unchecked)
Exporting: false
Progress: 0
```

### During Export
```
Format: Excel
Date: This Month
Categories: [office-supplies, travel]
Images: true
Exporting: true ← Active
Progress: 65 ← Animating
```

### After Export
```
Format: Excel
Date: This Month
Categories: [office-supplies, travel]
Images: true
Exporting: false ← Reset
Progress: 0 ← Reset
```

---

## 🌊 User Flow Diagram

```
┌─────────────┐
│   START     │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ 1. Select Format    │ ◄── Excel/PDF/CSV
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ 2. Choose Date      │ ◄── Preset or Custom
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ 3. Filter (opt)     │ ◄── Categories
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ 4. Options (opt)    │ ◄── Include Images
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ 5. Review Preview   │ ◄── Count, Total, VAT
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ 6. Click Export     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ 7. Watch Progress   │ ◄── 0% → 100%
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ 8. Download Opens   │ ◄── New Tab
└──────┬──────────────┘
       │
       ▼
┌─────────────┐
│    DONE     │
└─────────────┘
```

---

## 🎯 Interactive Elements Map

### Clickable Elements
```
1. Format Cards (3)          → setSelectedFormat
2. Date Preset Buttons (4)   → setDatePreset
3. Category Cards (13)       → toggleCategory
4. Clear Categories          → setSelectedCategories([])
5. Include Images Checkbox   → setIncludeImages
6. Custom Date Inputs (2)    → setCustomStartDate/End
7. Export Button             → handleExport
```

### Keyboard Navigation Order
```
Tab 1:  Excel format
Tab 2:  PDF format
Tab 3:  CSV format
Tab 4:  This Month preset
Tab 5:  Last Month preset
Tab 6:  This Year preset
Tab 7:  Custom preset
Tab 8:  Start date (if custom)
Tab 9:  End date (if custom)
Tab 10: Category 1
Tab 11: Category 2
...
Tab 22: Category 13
Tab 23: Clear categories
Tab 24: Include images checkbox
Tab 25: Export button
```

---

## 🎨 Color States

### Format/Category Cards
```
Default:
  border: #E5E7EB (gray-200)
  background: transparent

Hover:
  border: #D1D5DB (gray-300)
  background: transparent

Selected:
  border: #2563EB (primary-600)
  background: #DBEAFE (primary-50)
  shadow: 0 4px 8px rgba(0,0,0,0.12)
```

### Date Preset Buttons
```
Default:
  background: #F3F4F6 (gray-100)
  color: #374151 (gray-700)

Hover:
  background: #E5E7EB (gray-200)

Selected:
  background: #2563EB (primary-600)
  color: #FFFFFF
```

### Export Button
```
Default:
  background: #2563EB (primary-600)
  color: #FFFFFF

Hover:
  background: #1D4ED8 (primary-700)

Disabled:
  background: #E5E7EB (gray-200)
  color: #9CA3AF (gray-400)

Loading:
  background: #2563EB (primary-600)
  opacity: 0.7
  cursor: not-allowed
```

---

**Visual Guide Version**: 1.0  
**Last Updated**: November 3, 2025  
**Purpose**: Quick visual reference for developers and designers
