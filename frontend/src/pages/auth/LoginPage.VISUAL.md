# LoginPage - Visual Guide

## Component Preview

This document provides a visual representation of the LoginPage component in different states.

---

## 🎨 Default State (Empty Form)

```
┌─────────────────────────────────────────────────────────┐
│                   #F9FAFB (Light Gray Background)        │
│                                                          │
│         ┌──────────────────────────────────┐            │
│         │     White Card (440px width)     │            │
│         │                                  │            │
│         │    ╭─────────╮                   │            │
│         │    │ ✓ Tik   │  Tik-Tax          │            │
│         │    ╰─────────╯                   │            │
│         │                                  │            │
│         │          התחברות                 │            │
│         │   ברוכים השבים! נשמח לראותכם שוב │            │
│         │                                  │            │
│         │   אימייל *                       │            │
│         │   ┌──────────────────────┐ 📧    │            │
│         │   │ name@example.com     │       │            │
│         │   └──────────────────────┘       │            │
│         │                                  │            │
│         │   סיסמה *                        │            │
│         │   ┌──────────────────────┐ 🔒 👁 │            │
│         │   │ ••••••••             │       │            │
│         │   └──────────────────────┘       │            │
│         │                                  │            │
│         │   ☐ זכור אותי    שכחת סיסמה?    │            │
│         │                                  │            │
│         │   ┌──────────────────────────┐   │            │
│         │   │       התחבר              │   │            │
│         │   └──────────────────────────┘   │            │
│         │                                  │            │
│         │          ──── או ────            │            │
│         │                                  │            │
│         │   ┌──────────────────────────┐   │            │
│         │   │ G  התחבר עם Google      │   │            │
│         │   └──────────────────────────┘   │            │
│         │                                  │            │
│         │   אין לך חשבון? הירשם עכשיו     │            │
│         └──────────────────────────────────┘            │
│                                                          │
│         תנאי השימוש • מדיניות הפרטיות                   │
└─────────────────────────────────────────────────────────┘
```

---

## ❌ Error State (Validation Errors)

```
┌─────────────────────────────────────────────────────────┐
│                                                          │
│         ┌──────────────────────────────────┐            │
│         │                                  │            │
│         │    ╭─────────╮                   │            │
│         │    │ ✓ Tik   │  Tik-Tax          │            │
│         │    ╰─────────╯                   │            │
│         │                                  │            │
│         │          התחברות                 │            │
│         │   ברוכים השבים! נשמח לראותכם שוב │            │
│         │                                  │            │
│         │   אימייל *                       │            │
│         │   ┌──────────────────────┐ 📧    │            │
│         │   │ invalid-email        │       │   RED      │
│         │   └──────────────────────┘       │   BORDER   │
│         │   ⚠ כתובת אימייל לא תקינה       │  (ERROR)   │
│         │                                  │            │
│         │   סיסמה *                        │            │
│         │   ┌──────────────────────┐ 🔒 👁 │            │
│         │   │ 123                  │       │   RED      │
│         │   └──────────────────────┘       │   BORDER   │
│         │   ⚠ סיסמה חייבת להכיל לפחות 8    │  (ERROR)   │
│         │     תווים                        │            │
│         │                                  │            │
│         │   ☐ זכור אותי    שכחת סיסמה?    │            │
│         │                                  │            │
│         │   ┌──────────────────────────┐   │            │
│         │   │       התחבר              │   │  DISABLED  │
│         │   └──────────────────────────┘   │            │
│         │                                  │            │
│         │          ──── או ────            │            │
│         │                                  │            │
│         │   ┌──────────────────────────┐   │            │
│         │   │ G  התחבר עם Google      │   │            │
│         │   └──────────────────────────┘   │            │
│         │                                  │            │
│         │   אין לך חשבון? הירשם עכשיו     │            │
│         └──────────────────────────────────┘            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## ⏳ Loading State (Submitting)

```
┌─────────────────────────────────────────────────────────┐
│                                                          │
│         ┌──────────────────────────────────┐            │
│         │                                  │            │
│         │    ╭─────────╮                   │            │
│         │    │ ✓ Tik   │  Tik-Tax          │            │
│         │    ╰─────────╯                   │            │
│         │                                  │            │
│         │          התחברות                 │            │
│         │   ברוכים השבים! נשמח לראותכם שוב │            │
│         │                                  │            │
│         │   אימייל *                       │            │
│         │   ┌──────────────────────┐ 📧    │            │
│         │   │ user@tiktax.co.il    │       │   BLUE     │
│         │   └──────────────────────┘       │   BORDER   │
│         │                                  │  (FOCUS)   │
│         │   סיסמה *                        │            │
│         │   ┌──────────────────────┐ 🔒 👁 │            │
│         │   │ ••••••••             │       │            │
│         │   └──────────────────────┘       │            │
│         │                                  │            │
│         │   ☑ זכור אותי    שכחת סיסמה?    │  CHECKED   │
│         │                                  │            │
│         │   ┌──────────────────────────┐   │            │
│         │   │  ⟳  מתחבר...             │   │  LOADING   │
│         │   └──────────────────────────┘   │  DISABLED  │
│         │                                  │            │
│         │          ──── או ────            │            │
│         │                                  │            │
│         │   ┌──────────────────────────┐   │            │
│         │   │ G  התחבר עם Google      │   │  DISABLED  │
│         │   └──────────────────────────┘   │            │
│         │                                  │            │
│         │   אין לך חשבון? הירשם עכשיו     │            │
│         └──────────────────────────────────┘            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 👁️ Password Visible State

```
┌─────────────────────────────────────────────────────────┐
│                                                          │
│         ┌──────────────────────────────────┐            │
│         │                                  │            │
│         │   סיסמה *                        │            │
│         │   ┌──────────────────────┐ 🔒 👁‍🗨│  EYE-OFF  │
│         │   │ password123          │       │  ICON      │
│         │   └──────────────────────┘       │  (VISIBLE) │
│         │                                  │            │
│         └──────────────────────────────────┘            │
│                                                          │
└─────────────────────────────────────────────────────────┘

Password text is visible instead of dots
```

---

## 📱 Mobile View (< 640px)

```
┌────────────────────────┐
│   #F9FAFB Background   │
│                        │
│  ┌──────────────────┐  │
│  │ White Card       │  │
│  │ (Full width -32) │  │
│  │                  │  │
│  │  ✓ Tik-Tax       │  │
│  │                  │  │
│  │   התחברות        │  │
│  │   ברוכים השבים!  │  │
│  │                  │  │
│  │  אימייל *        │  │
│  │  ┌────────────┐  │  │
│  │  │            │📧│  │
│  │  └────────────┘  │  │
│  │                  │  │
│  │  סיסמה *         │  │
│  │  ┌────────────┐  │  │
│  │  │            │🔒│  │
│  │  └────────────┘ 👁│  │
│  │                  │  │
│  │  ☐ זכור אותי     │  │
│  │  שכחת סיסמה?     │  │
│  │                  │  │
│  │  ┌────────────┐  │  │
│  │  │   התחבר    │  │  │ Touch
│  │  └────────────┘  │  │ 48px
│  │                  │  │ Height
│  │   ─── או ───     │  │
│  │                  │  │
│  │  ┌────────────┐  │  │
│  │  │ G Google   │  │  │
│  │  └────────────┘  │  │
│  │                  │  │
│  │  הירשם עכשיו     │  │
│  └──────────────────┘  │
│                        │
│  תנאי השימוש           │
└────────────────────────┘
```

---

## 🎨 Color Specifications

### Primary Colors
```
Card Background:      #FFFFFF (white)
Page Background:      #F9FAFB (gray-50)
Primary Blue:         #2563EB (buttons, links)
Primary Blue Hover:   #1D4ED8 (darker blue)
```

### Text Colors
```
Main Title:           #111827 (gray-900)
Subtitle:             #6B7280 (gray-500)
Body Text:            #374151 (gray-700)
Link Text:            #2563EB (blue-600)
Link Hover:           #1D4ED8 (blue-700)
```

### State Colors
```
Error Border:         #EF4444 (red-500)
Error Text:           #DC2626 (red-600)
Error Background:     #FEF2F2 (red-50)

Focus Border:         #2563EB (blue-600)
Focus Ring:           rgba(37, 99, 235, 0.1)

Disabled Background:  #F9FAFB (gray-50)
Disabled Text:        #9CA3AF (gray-400)
```

---

## 📐 Spacing & Sizing

### Card Dimensions
```
Max Width:            440px
Padding:              40px (2.5rem)
Border Radius:        16px
Box Shadow:           0 10px 15px -3px rgba(0,0,0,0.1)
```

### Logo
```
Height:               48px
Margin Bottom:        32px (2rem)
```

### Form Elements
```
Input Height:         48px
Input Padding:        12px 16px
Input Border Radius:  8px
Input Font Size:      16px

Button Height:        48px
Button Padding:       12px 24px
Button Border Radius: 8px
Button Font Size:     15px
```

### Spacing
```
Between Fields:       20px (1.25rem)
Submit Button Top:    24px (1.5rem)
Divider Margin:       24px vertical
Logo to Title:        32px (2rem)
Title to Subtitle:    8px (0.5rem)
```

---

## 🔤 Typography

### Font Family
```
Primary:   'Inter', -apple-system, BlinkMacSystemFont, sans-serif
Fallback:  System default sans-serif
```

### Font Sizes
```
Page Title:         24px (text-2xl)
Subtitle:           14px (text-sm)
Input Labels:       14px (text-sm)
Input Text:         16px (text-base)
Button Text:        15px
Error Messages:     14px (text-sm)
Footer Links:       12px (text-xs)
```

### Font Weights
```
Page Title:         600 (semi-bold)
Input Labels:       500 (medium)
Button Text:        500 (medium)
Body Text:          400 (regular)
Links:              500 (medium)
```

---

## 🔄 Interactive States

### Button States

#### Primary Button (התחבר)
```
Default:
  Background: #2563EB
  Color: #FFFFFF
  Border: none
  
Hover:
  Background: #1D4ED8
  Box Shadow: 0 4px 6px rgba(0,0,0,0.1)
  Transform: translateY(-1px)
  
Active:
  Background: #1E40AF
  Transform: translateY(0)
  
Loading:
  Background: #2563EB
  Cursor: not-allowed
  Opacity: 0.7
  Icon: Spinning loader
  
Disabled:
  Background: #E5E7EB
  Color: #9CA3AF
  Cursor: not-allowed
```

#### Secondary Button (Google)
```
Default:
  Background: #FFFFFF
  Color: #374151
  Border: 1px solid #E5E7EB
  
Hover:
  Background: #F9FAFB
  Border: 1px solid #D1D5DB
  
Active:
  Background: #F3F4F6
```

### Input States

```
Default:
  Border: 1.5px solid #D1D5DB
  Background: #FFFFFF
  
Focus:
  Border: 1.5px solid #2563EB
  Ring: 0 0 0 3px rgba(37,99,235,0.1)
  
Error:
  Border: 1.5px solid #EF4444
  Ring: 0 0 0 3px rgba(239,68,68,0.1)
  
Disabled:
  Background: #F9FAFB
  Color: #9CA3AF
  Border: 1px solid #E5E7EB
  Cursor: not-allowed
```

### Link States

```
Default:
  Color: #2563EB
  Text Decoration: none
  
Hover:
  Color: #1D4ED8
  Text Decoration: underline
  
Active:
  Color: #1E40AF
  
Visited:
  Color: #2563EB (same as default)
```

---

## ♿ Accessibility Indicators

### Focus Indicators
```
All Interactive Elements:
  Outline: 2px solid #2563EB
  Outline Offset: 2px
  Border Radius: matches element
```

### Keyboard Navigation Order
```
1. Email Input
2. Password Input  
3. Password Toggle Button
4. Remember Me Checkbox
5. Forgot Password Link
6. Submit Button
7. Google OAuth Button
8. Signup Link
9. Terms Link
10. Privacy Link
```

### ARIA Labels
```
Logo: aria-label="Tik-Tax Logo"
Password Toggle: aria-label="הצג סיסמה" / "הסתר סיסמה"
Email Input: aria-invalid="true" (when error)
Password Input: aria-invalid="true" (when error)
```

---

## 📊 Component Hierarchy

```
LoginPage
├── Container (min-h-screen, centered)
│   └── Card Container (max-w-440px)
│       ├── Logo Section
│       │   └── SVG + Text
│       ├── Title Section
│       │   ├── h1: "התחברות"
│       │   └── p: "ברוכים השבים..."
│       ├── Form
│       │   ├── Email Input
│       │   │   ├── Label
│       │   │   ├── Input Field
│       │   │   ├── Mail Icon
│       │   │   └── Error Message
│       │   ├── Password Input
│       │   │   ├── Label
│       │   │   ├── Input Field
│       │   │   ├── Lock Icon
│       │   │   ├── Eye Toggle
│       │   │   └── Error Message
│       │   ├── Remember Me + Forgot Password
│       │   │   ├── Checkbox + Label
│       │   │   └── Link
│       │   ├── Submit Button
│       │   ├── Divider ("או")
│       │   └── Google OAuth Button
│       └── Footer
│           └── Signup Link
└── Legal Links (Terms, Privacy)
```

---

## 🌐 RTL (Right-to-Left) Considerations

### Hebrew Text
```
All Hebrew text flows right-to-left:
- Page title: "התחברות"
- Subtitle: "ברוכים השבים! נשמח לראותכם שוב"
- Labels: "אימייל", "סיסמה"
- Buttons: "התחבר", "התחבר עם Google"
- Links: "שכחת סיסמה?", "הירשם עכשיו"
```

### Input Fields
```
Email and Password inputs use dir="ltr":
- Email: name@example.com (left-to-right)
- Password: ••••••••(left-to-right)

This prevents Hebrew UI from affecting input directionality
```

### Icon Positions
```
Icons in RTL layout:
- Mail icon: RIGHT side of email input
- Lock icon: RIGHT side of password input
- Eye toggle: LEFT side of password input (functional position)
- Google icon: RIGHT side of Google button
```

---

## 🎭 Animation & Transitions

### Button Hover Animation
```css
transition: all 0.2s ease;
transform: translateY(-1px);
box-shadow: 0 4px 6px rgba(0,0,0,0.1);
```

### Input Focus Animation
```css
transition: border-color 0.15s ease, box-shadow 0.15s ease;
```

### Loading Spinner
```css
animation: spin 0.8s linear infinite;
```

### Error Message Slide In
```css
transition: all 0.2s ease-out;
opacity: 0 → 1;
transform: translateY(-4px) → translateY(0);
```

---

**Visual Guide Version:** 1.0.0  
**Last Updated:** November 2, 2025  
**Status:** Complete
