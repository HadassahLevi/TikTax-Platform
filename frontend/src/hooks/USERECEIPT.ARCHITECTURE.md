# useReceipt Hook Architecture

**Visual guide to hook system structure and data flow**

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    RECEIPT HOOK SYSTEM                       │
│                     /src/hooks/useReceipt.ts                │
└─────────────────────────────────────────────────────────────┘
                              │
                              │
        ┌─────────────────────┴─────────────────────┐
        │                                           │
        ▼                                           ▼
┌──────────────────┐                      ┌──────────────────┐
│  Receipt Store   │◄─────────────────────┤  Receipt Service │
│   (Zustand)      │                      │   (API Client)   │
└──────────────────┘                      └──────────────────┘
        │                                           │
        │                                           │
        ▼                                           ▼
┌──────────────────┐                      ┌──────────────────┐
│  6 Custom Hooks  │                      │   Backend API    │
└──────────────────┘                      └──────────────────┘
        │
        │
        ├─── useReceipt()             (main interface)
        ├─── useLoadReceipts()        (auto-load)
        ├─── useLoadStatistics()      (auto-load stats)
        ├─── useReceiptValidation()   (validators)
        ├─── useInfiniteScroll()      (pagination helper)
        └─── useReceiptFilters()      (filter management)
```

---

## 🔄 Data Flow Diagram

```
USER ACTION
    │
    ▼
┌───────────────────┐
│   Component       │
│   (uses hook)     │
└─────────┬─────────┘
          │
          │ calls hook function
          ▼
┌───────────────────┐
│   useReceipt()    │
│   Hook Layer      │
└─────────┬─────────┘
          │
          │ accesses store
          ▼
┌───────────────────┐
│  Receipt Store    │
│  (Zustand)        │
└─────────┬─────────┘
          │
          │ calls service
          ▼
┌───────────────────┐
│ Receipt Service   │
│ (API Client)      │
└─────────┬─────────┘
          │
          │ HTTP request
          ▼
┌───────────────────┐
│   Backend API     │
└─────────┬─────────┘
          │
          │ response
          ▼
┌───────────────────┐
│  Receipt Store    │
│  (state updated)  │
└─────────┬─────────┘
          │
          │ re-render
          ▼
┌───────────────────┐
│   Component       │
│   (updates UI)    │
└───────────────────┘
```

---

## 📦 Hook Dependencies

```
useReceipt.ts
    │
    ├── React Hooks
    │   ├── useCallback (memoization)
    │   └── useEffect (side effects)
    │
    ├── Zustand Store
    │   └── useReceiptStore (state management)
    │
    └── TypeScript Types
        ├── ReceiptUpdateRequest
        └── ReceiptFilterOptions
```

---

## 🎯 Hook Relationships

```
                    ┌──────────────────┐
                    │   useReceipt()   │
                    │   (main hook)    │
                    └────────┬─────────┘
                             │
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│useLoadReceipts│   │useLoadStats   │   │useValidation  │
│(specialized)  │   │(specialized)  │   │(helpers)      │
└───────────────┘   └───────────────┘   └───────────────┘

        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│Auto-load on   │   │Auto-load on   │   │Validation     │
│mount          │   │mount          │   │functions      │
└───────────────┘   └───────────────┘   └───────────────┘


                    ┌──────────────────┐
                    │useInfiniteScroll │
                    │(UI helper)       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │Scroll listener   │
                    │+ callback        │
                    └──────────────────┘


                    ┌──────────────────┐
                    │useReceiptFilters │
                    │(filter helper)   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │Filter state      │
                    │management        │
                    └──────────────────┘
```

---

## 🔌 Component Integration Pattern

```
┌─────────────────────────────────────────────────────────┐
│                    PAGE COMPONENT                       │
│                 (e.g., ReceiptArchive)                  │
└───────────────────────┬─────────────────────────────────┘
                        │
                        │ imports hooks
                        ▼
        ┌───────────────────────────────────┐
        │  useLoadReceipts()  (auto-loads)  │
        └───────────┬───────────────────────┘
                    │
                    ▼
        ┌───────────────────────────────────┐
        │  useReceipt()  (main operations)  │
        └───────────┬───────────────────────┘
                    │
                    ▼
        ┌───────────────────────────────────┐
        │  useInfiniteScroll()  (pagination)│
        └───────────┬───────────────────────┘
                    │
                    ▼
        ┌───────────────────────────────────┐
        │  useReceiptFilters()  (filtering) │
        └───────────┬───────────────────────┘
                    │
                    │ all return data/functions
                    ▼
┌─────────────────────────────────────────────────────────┐
│              COMPONENT RENDER FUNCTION                  │
│  Returns JSX using data from all hooks                 │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 State Management Flow

```
┌──────────────────────────────────────────────────────────┐
│                   RECEIPT STORE STATE                    │
│                     (Single Source of Truth)             │
├──────────────────────────────────────────────────────────┤
│  • currentReceipt: Receipt | null                        │
│  • receipts: Receipt[]                                   │
│  • total: number                                         │
│  • hasMore: boolean                                      │
│  • statistics: ReceiptStatistics | null                  │
│  • isUploading: boolean                                  │
│  • isProcessing: boolean                                 │
│  • isLoadingList: boolean                                │
│  • isLoadingStats: boolean                               │
│  • error: string | null                                  │
│  • uploadError: string | null                            │
│  • filters: ReceiptFilterOptions                         │
│  • sort: ReceiptSortOptions                              │
│  • pagination: { page, limit }                           │
└────────────────┬─────────────────────────────────────────┘
                 │
                 │ accessed by
                 ▼
      ┌──────────────────────┐
      │   useReceiptStore()  │
      │   (from hooks)       │
      └──────────┬───────────┘
                 │
                 │ returns
                 ▼
      ┌──────────────────────┐
      │  State + Actions     │
      │  (to components)     │
      └──────────────────────┘
```

---

## 🎭 Hook Usage Patterns

### Pattern 1: List View
```
Component: ReceiptList
    │
    ├── useLoadReceipts() ──► Auto-loads receipts
    │
    ├── useReceipt() ──────► Provides deleteReceipt, etc.
    │
    └── useInfiniteScroll() ► Loads more on scroll
```

### Pattern 2: Review Form
```
Component: ReceiptReview
    │
    ├── useReceipt() ──────────► Current receipt, approve
    │
    └── useReceiptValidation() ► Validate fields
```

### Pattern 3: Dashboard
```
Component: Dashboard
    │
    ├── useLoadStatistics() ──► Auto-loads stats
    │
    └── useLoadReceipts() ────► Auto-loads recent receipts
```

### Pattern 4: Filter Panel
```
Component: FilterPanel
    │
    ├── useReceiptFilters() ──► Filter management
    │
    └── useReceipt() ─────────► Apply filters
```

---

## 🔄 Action Flow Examples

### Upload Flow
```
User selects file
    │
    ▼
Component calls uploadReceipt(file)
    │
    ▼
Hook wrapper (handleUpload)
    │
    ▼
Store action (uploadReceipt)
    │
    ▼
Service API call (uploadReceipt)
    │
    ▼
Backend processing
    │
    ▼
Store state updated (isUploading, uploadError)
    │
    ▼
Component re-renders
    │
    ▼
UI shows result
```

### Delete Flow
```
User clicks delete
    │
    ▼
Component calls deleteReceipt(id)
    │
    ▼
Hook shows confirmation dialog
    │
    ├─► User cancels ──► STOP
    │
    ├─► User confirms
    │       │
    │       ▼
    │   Store action (deleteReceipt)
    │       │
    │       ▼
    │   Service API call (deleteReceipt)
    │       │
    │       ▼
    │   Backend deletion
    │       │
    │       ▼
    │   Store removes receipt from array
    │       │
    │       ▼
    │   Component re-renders
    │       │
    │       ▼
    │   Receipt removed from UI
```

### Filter Flow
```
User changes filter
    │
    ▼
Component calls updateFilter(key, value)
    │
    ▼
Hook updates filter object
    │
    ▼
Store setFilters action
    │
    ▼
Store triggers fetchReceipts with filters
    │
    ▼
Service API call with query params
    │
    ▼
Backend returns filtered results
    │
    ▼
Store updates receipts array
    │
    ▼
Component re-renders with filtered data
```

---

## 🧩 Type Flow

```
TypeScript Types
(/src/types/receipt.types.ts)
    │
    ├── Receipt
    ├── ReceiptStatus
    ├── ReceiptUpdateRequest
    ├── ReceiptFilterOptions
    ├── ReceiptSortOptions
    └── ReceiptStatistics
    │
    │ imported by
    ▼
useReceipt.ts
    │
    │ used in
    ▼
Hook function signatures
    │
    │ enforced in
    ▼
Component usage
    │
    │ results in
    ▼
Type-safe code
```

---

## 🔐 Security & Validation Layer

```
User Input
    │
    ▼
┌──────────────────────┐
│ Component Validation │
│ (useReceiptValidation)│
└────────┬─────────────┘
         │
         │ if valid
         ▼
┌──────────────────────┐
│   Hook Action        │
│   (useReceipt)       │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│   Store Action       │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  Service Validation  │
│  (client-side)       │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│   Backend API        │
│   (server validation)│
└──────────────────────┘
```

---

## 📚 Documentation Structure

```
/src/hooks/
    │
    ├── useReceipt.ts ──────────► Implementation
    │
    ├── USERECEIPT.md ──────────► Full guide (you are here)
    │
    ├── USERECEIPT.QUICKREF.md ─► Quick reference
    │
    ├── USERECEIPT.CHECKLIST.md ► Implementation tracking
    │
    ├── USERECEIPT.SUMMARY.md ──► Quick overview
    │
    └── USERECEIPT.ARCHITECTURE.md ► This file
```

---

## 🎯 Decision Tree: Which Hook to Use?

```
START: What do you need?
    │
    ├─► Load receipts on mount?
    │   └─► useLoadReceipts()
    │
    ├─► Load statistics on mount?
    │   └─► useLoadStatistics()
    │
    ├─► Validate receipt data?
    │   └─► useReceiptValidation()
    │
    ├─► Infinite scroll pagination?
    │   └─► useInfiniteScroll()
    │
    ├─► Manage filters?
    │   └─► useReceiptFilters()
    │
    └─► Any other receipt operation?
        └─► useReceipt() (main hook)
```

---

## 🔧 Performance Considerations

```
┌─────────────────────────────────────────┐
│          PERFORMANCE OPTIMIZATIONS       │
├─────────────────────────────────────────┤
│                                         │
│  useCallback ──────► Memoized functions │
│                     (prevent re-creation)│
│                                         │
│  useEffect ───────► Controlled side     │
│                     effects with cleanup │
│                                         │
│  Zustand Store ───► Minimal re-renders  │
│                     (selector pattern)   │
│                                         │
│  Debounce ────────► Search optimization │
│                     (component level)    │
│                                         │
│  Pagination ──────► Load on demand      │
│                     (infinite scroll)    │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🚀 Integration Roadmap

```
Phase 1: Setup ✅
    ├─ Create useReceipt.ts
    ├─ Export from index.ts
    └─ Documentation

Phase 2: Basic Integration 🔄
    ├─ Use in Archive page
    ├─ Use in Dashboard
    └─ Use in Review page

Phase 3: Advanced Features 📋
    ├─ Infinite scroll in lists
    ├─ Filter panels
    └─ Validation in forms

Phase 4: Optimization 📋
    ├─ Performance tuning
    ├─ Error boundaries
    └─ Loading states
```

---

**Architecture Version:** 1.0.0  
**Last Updated:** 2025-11-02  
**Status:** ✅ Complete
