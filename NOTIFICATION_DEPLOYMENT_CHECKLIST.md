# ✅ Notification System - Deployment Checklist

## Pre-Deployment Checklist

### Backend Setup

- [ ] **1. Run Database Migration**
  ```bash
  cd backend
  alembic upgrade head
  ```
  - Verify migration success
  - Check `notifications` table exists
  - Verify all indexes created

- [ ] **2. Update User Model Import**
  - Ensure `from app.models.notification import Notification` is imported where needed
  - Verify relationship is accessible

- [ ] **3. Test API Endpoints**
  ```bash
  # Start backend
  uvicorn app.main:app --reload
  
  # Test endpoints (use Postman or curl)
  GET    /api/v1/notifications
  GET    /api/v1/notifications/unread-count
  PUT    /api/v1/notifications/{id}/read
  POST   /api/v1/notifications/mark-all-read
  DELETE /api/v1/notifications/{id}
  ```

- [ ] **4. Create Test Notifications**
  ```bash
  python test_notifications_manual.py --email test@tiktax.co.il
  ```
  - Verify notifications appear in database
  - Check all 9 notification types created

- [ ] **5. Verify Router Registration**
  - Check `notifications.router` is in `/api/v1/router.py`
  - Verify endpoint appears in API docs: `/docs`

---

### Frontend Setup

- [ ] **1. Verify Dependencies Installed**
  ```bash
  cd frontend
  npm install
  # Should already have: framer-motion, lucide-react
  ```

- [ ] **2. Check Import Paths**
  - Verify `@/` alias works
  - Test imports in each file compile without errors
  - Run: `npm run build` to check for errors

- [ ] **3. Test Toast Context**
  - Navigate to `/notification-demo`
  - Click all toast buttons
  - Verify toasts appear and auto-dismiss
  - Check manual dismiss works

- [ ] **4. Test Notification Center**
  - Click bell icon
  - Verify panel opens
  - Check notifications load
  - Test mark as read
  - Test delete notification
  - Verify unread count updates

- [ ] **5. Verify ToastProvider Wraps App**
  - Check `App.tsx` has `<ToastProvider>` wrapper
  - Verify it wraps entire `<BrowserRouter>`

---

### Integration Points

- [ ] **1. Add NotificationCenter to Header**
  ```typescript
  import { NotificationCenter } from '@/components/NotificationCenter';
  
  // Add to header component
  <NotificationCenter />
  ```

- [ ] **2. Integrate in Receipt Processing**
  ```python
  # In receipt_service.py
  from app.services.notification_service import create_receipt_approved_notification
  
  # After approval
  create_receipt_approved_notification(db, user_id, receipt.vendor_name)
  ```

- [ ] **3. Integrate in Stripe Webhooks**
  ```python
  # In stripe_service.py
  from app.services.notification_service import (
      create_payment_success_notification,
      create_payment_failed_notification
  )
  
  # In webhook handler
  if event.type == 'invoice.payment_succeeded':
      create_payment_success_notification(db, user.id, plan_name)
  ```

- [ ] **4. Add Toast Messages to Forms**
  ```typescript
  import { useToast } from '@/contexts/ToastContext';
  
  const { showToast } = useToast();
  
  // On form submit success
  showToast({
    type: 'success',
    title: 'הצלחה',
    message: 'הטופס נשלח בהצלחה'
  });
  ```

---

### Testing

#### Manual Testing

- [ ] **Toast Messages**
  - [ ] Success toast appears (green)
  - [ ] Error toast appears (red)
  - [ ] Warning toast appears (amber)
  - [ ] Info toast appears (blue)
  - [ ] Auto-dismiss after 5 seconds
  - [ ] Custom duration works
  - [ ] Manual dismiss (X button) works
  - [ ] Multiple toasts stack properly
  - [ ] Hebrew text displays correctly (RTL)

- [ ] **Notification Center**
  - [ ] Bell icon visible in header
  - [ ] Unread count badge shows correct number
  - [ ] Badge shows "9+" when > 9 unread
  - [ ] Clicking bell opens panel
  - [ ] Clicking outside closes panel
  - [ ] Notifications load on open
  - [ ] Newest notifications appear first
  - [ ] Unread notifications highlighted
  - [ ] Clicking "סמן הכל כנקרא" marks all as read
  - [ ] Individual mark as read works
  - [ ] Delete notification works
  - [ ] Clicking notification with action_url navigates
  - [ ] Auto-refresh every 30 seconds
  - [ ] Empty state shows when no notifications
  - [ ] Loading state shows while fetching

- [ ] **API Integration**
  - [ ] GET /notifications returns user's notifications
  - [ ] Pagination works (skip/limit)
  - [ ] unread_only filter works
  - [ ] PUT mark as read updates is_read and read_at
  - [ ] POST mark all as read updates all unread
  - [ ] DELETE removes notification
  - [ ] User can only see their own notifications
  - [ ] Auth required for all endpoints

- [ ] **Backend Notification Creation**
  - [ ] Receipt approved creates notification
  - [ ] Receipt failed creates notification
  - [ ] Payment success creates notification
  - [ ] Payment failed creates notification
  - [ ] Limit warning creates notification
  - [ ] Subscription canceled creates notification
  - [ ] Duplicate receipt creates notification
  - [ ] Export ready creates notification
  - [ ] Welcome message creates notification

#### Cross-Browser Testing

- [ ] **Chrome** (Desktop)
  - [ ] Toasts display correctly
  - [ ] Notification center works
  - [ ] Animations smooth

- [ ] **Firefox** (Desktop)
  - [ ] All features work
  - [ ] No console errors

- [ ] **Safari** (Desktop & iOS)
  - [ ] RTL layout correct
  - [ ] Touch interactions work (iOS)

- [ ] **Edge** (Desktop)
  - [ ] Full functionality

#### Mobile Testing

- [ ] **Responsive Design**
  - [ ] Toast messages fit on small screens
  - [ ] Notification panel adjusts to screen width
  - [ ] Touch targets minimum 44px
  - [ ] Scrolling works in notification list

- [ ] **Touch Interactions**
  - [ ] Tap to open notification center
  - [ ] Tap to close
  - [ ] Swipe to dismiss toasts (if implemented)
  - [ ] Tap notification actions work

#### Performance Testing

- [ ] **Load Testing**
  - [ ] 100+ notifications load quickly
  - [ ] Pagination performs well
  - [ ] No lag when opening panel

- [ ] **Memory**
  - [ ] No memory leaks from toasts
  - [ ] Auto-dismiss clears memory
  - [ ] Panel close clears event listeners

#### Accessibility Testing

- [ ] **Keyboard Navigation**
  - [ ] Tab to bell icon
  - [ ] Enter to open panel
  - [ ] Escape to close panel
  - [ ] Tab through notifications
  - [ ] Enter to mark as read/delete

- [ ] **Screen Reader**
  - [ ] Bell icon labeled
  - [ ] Unread count announced
  - [ ] Notifications read properly
  - [ ] Action buttons labeled
  - [ ] Toast messages announced (aria-live)

- [ ] **Color Contrast**
  - [ ] All text meets WCAG AA (4.5:1)
  - [ ] Icons visible
  - [ ] Status colors distinguishable

---

### Production Deployment

- [ ] **Environment Variables**
  - [ ] Database connection string correct
  - [ ] API base URL configured
  - [ ] No sensitive data in frontend

- [ ] **Database**
  - [ ] Migration run on production DB
  - [ ] Indexes created
  - [ ] Backup before migration

- [ ] **Frontend Build**
  ```bash
  npm run build
  ```
  - [ ] No build errors
  - [ ] Bundle size reasonable
  - [ ] Source maps generated (if needed)

- [ ] **Backend Deployment**
  - [ ] Notification endpoints accessible
  - [ ] CORS configured for frontend domain
  - [ ] Rate limiting configured

---

### Monitoring & Maintenance

- [ ] **Logging**
  - [ ] Notification creation logged
  - [ ] API errors logged
  - [ ] Failed notifications tracked

- [ ] **Analytics** (Optional)
  - [ ] Track notification open rate
  - [ ] Track action click rate
  - [ ] Monitor unread count trends

- [ ] **Database Cleanup** (Future)
  - [ ] Plan for old notification deletion
  - [ ] Archive strategy (if needed)

---

### Documentation

- [ ] **Developer Documentation**
  - [ ] NOTIFICATION_SYSTEM_GUIDE.md reviewed
  - [ ] NOTIFICATION_QUICK_REF.md accessible
  - [ ] Code comments clear

- [ ] **User Documentation** (If needed)
  - [ ] How to use notification center
  - [ ] What notifications mean
  - [ ] How to manage notifications

---

### Rollback Plan

If issues occur in production:

1. **Backend Rollback**
   ```bash
   # Revert migration
   alembic downgrade -1
   
   # Remove router
   # Comment out in router.py:
   # api_router.include_router(notifications.router, ...)
   ```

2. **Frontend Rollback**
   ```typescript
   // Remove ToastProvider from App.tsx
   // Remove NotificationCenter from Header
   // Deploy previous build
   ```

3. **Database Rollback**
   ```sql
   -- Drop table if needed
   DROP TABLE IF EXISTS notifications CASCADE;
   ```

---

### Post-Deployment Verification

- [ ] **Smoke Tests**
  - [ ] Can create notification via backend
  - [ ] Notification appears in frontend
  - [ ] Toast messages work
  - [ ] No console errors

- [ ] **User Acceptance**
  - [ ] Test with real user
  - [ ] Verify notifications helpful
  - [ ] Check for confusion

- [ ] **Performance**
  - [ ] Page load time acceptable
  - [ ] API response time < 200ms
  - [ ] No memory leaks after 1 hour

---

## Quick Commands Reference

### Backend
```bash
# Run migration
alembic upgrade head

# Create test notifications
python test_notifications_manual.py

# Start server
uvicorn app.main:app --reload

# Check API docs
open http://localhost:8000/docs
```

### Frontend
```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Test demo page
open http://localhost:5173/notification-demo
```

### Testing
```bash
# Backend tests
pytest tests/test_notifications.py

# Frontend tests
npm run test

# E2E tests
npm run test:e2e
```

---

## Success Criteria

✅ All checklist items completed
✅ No console errors in production
✅ Notifications appear for users
✅ Toast messages work reliably
✅ Mobile experience smooth
✅ Accessibility standards met
✅ Performance benchmarks achieved

---

## Support & Troubleshooting

**Common Issues:**
1. Migration fails → Check database connection
2. Toasts not showing → Check ToastProvider in App.tsx
3. Notifications not loading → Check auth token validity
4. Bell icon not showing count → Check API endpoint

**Get Help:**
- Check `NOTIFICATION_SYSTEM_GUIDE.md`
- Review code comments
- Check browser console
- Review API logs

---

**Deployment Date:** _____________
**Deployed By:** _____________
**Production URL:** _____________
**Status:** ⬜ Pending | ⬜ In Progress | ⬜ Complete

---

🎉 **Ready to Deploy!**
