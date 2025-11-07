# Notification System - Usage Examples

## Overview
Complete notification system with toast messages (temporary alerts) and persistent notification center (inbox).

## Toast Usage

### Import
```typescript
import { useToast } from '@/contexts/ToastContext';
```

### Basic Usage
```typescript
const { showToast } = useToast();

// Success toast
showToast({
  type: 'success',
  title: 'הצלחה!',
  message: 'הקבלה נשמרה בהצלחה'
});

// Error toast
showToast({
  type: 'error',
  title: 'שגיאה',
  message: 'לא ניתן לעבד את הקבלה'
});

// Warning toast
showToast({
  type: 'warning',
  title: 'אזהרה',
  message: 'אתה מתקרב למגבלת החבילה'
});

// Info toast
showToast({
  type: 'info',
  title: 'מידע',
  message: 'המנוי שלך יפוג בקרוב'
});
```

### Custom Duration
```typescript
showToast({
  type: 'success',
  title: 'הצלחה',
  message: 'פעולה הושלמה',
  duration: 3000 // 3 seconds (default is 5000)
});
```

## Notification Center Usage

### Add to Header/Layout
```typescript
import { NotificationCenter } from '@/components/NotificationCenter';

function Header() {
  return (
    <header>
      <div className="flex items-center gap-4">
        {/* Other header items */}
        <NotificationCenter />
      </div>
    </header>
  );
}
```

## Backend Integration Examples

### 1. Receipt Processing Success
```python
from app.services.notification_service import create_receipt_approved_notification

# After receipt approval
create_receipt_approved_notification(db, user_id, receipt.vendor_name)
```

### 2. Receipt Processing Failure
```python
from app.services.notification_service import create_receipt_failed_notification

# After OCR failure
try:
    process_receipt(receipt)
except Exception as e:
    create_receipt_failed_notification(db, user_id, str(e))
```

### 3. Subscription Limit Warning
```python
from app.services.notification_service import create_limit_warning_notification

# When checking limits
usage_percentage = (receipts_count / receipt_limit) * 100
if usage_percentage >= 80:
    create_limit_warning_notification(db, user_id, int(usage_percentage))
```

### 4. Payment Events
```python
from app.services.notification_service import (
    create_payment_success_notification,
    create_payment_failed_notification
)

# Stripe webhook handler
if event.type == 'invoice.payment_succeeded':
    create_payment_success_notification(db, user.id, plan_name)
elif event.type == 'invoice.payment_failed':
    create_payment_failed_notification(db, user.id)
```

### 5. Welcome New Users
```python
from app.services.notification_service import create_welcome_notification

# After user registration
user = create_user(db, user_data)
create_welcome_notification(db, user.id, user.full_name)
```

### 6. Duplicate Detection
```python
from app.services.notification_service import create_duplicate_receipt_notification

# When duplicate detected
if is_duplicate:
    create_duplicate_receipt_notification(db, user_id, vendor_name)
```

## Frontend Service Usage

### Get Notifications
```typescript
import notificationService from '@/services/notification.service';

// Get first 20 notifications
const data = await notificationService.getNotifications();
console.log(data.notifications); // Array of notifications
console.log(data.unread_count);  // Number of unread

// Get next page
const nextPage = await notificationService.getNotifications(20, 20);

// Get only unread
const unread = await notificationService.getNotifications(0, 20, true);
```

### Mark as Read
```typescript
// Single notification
await notificationService.markAsRead(notificationId);

// All notifications
await notificationService.markAllAsRead();
```

### Delete Notifications
```typescript
// Single notification
await notificationService.deleteNotification(notificationId);

// All notifications
await notificationService.deleteAllNotifications();
```

### Get Unread Count
```typescript
const count = await notificationService.getUnreadCount();
console.log(count); // e.g., 5
```

## Combined Toast + Notification Example

### Receipt Upload Flow
```typescript
// Frontend - Receipt Upload
const handleUpload = async (file: File) => {
  try {
    const response = await receiptService.upload(file);
    
    // Show immediate toast feedback
    showToast({
      type: 'success',
      title: 'קבלה הועלתה',
      message: 'הקבלה בתהליך עיבוד...'
    });
    
    // Backend will create a notification when processing completes
    // User will see it in notification center
    
  } catch (error) {
    showToast({
      type: 'error',
      title: 'שגיאה',
      message: 'העלאת הקבלה נכשלה'
    });
  }
};

// Backend - After OCR Processing
# In receipt_service.py
try:
    ocr_result = process_ocr(receipt_file)
    receipt.status = ReceiptStatus.REVIEW
    db.commit()
    
    # Create notification for user
    create_notification(
        db=db,
        user_id=user_id,
        type="success",
        title="קבלה מוכנה לאישור",
        message=f"הקבלה מ-{ocr_result.vendor_name} ממתינה לאישור",
        action_url="/review",
        action_label="אשר קבלה"
    )
except Exception as e:
    create_receipt_failed_notification(db, user_id, str(e))
```

## Notification Types Reference

### Success (Green)
- Receipt approved
- Payment successful
- Export completed
- Settings saved

### Error (Red)
- Receipt processing failed
- Payment failed
- Upload error
- Network error

### Warning (Amber)
- Approaching limit (80%+)
- Subscription expiring soon
- Duplicate detected
- Action required

### Info (Blue)
- Subscription canceled
- New feature available
- System maintenance
- General updates

## Best Practices

### Toast Messages
✅ **DO:**
- Use for immediate feedback
- Keep messages short (< 50 chars)
- Auto-dismiss (5 seconds default)
- Use for transient events

❌ **DON'T:**
- Use for critical information (use notifications instead)
- Show multiple toasts at once
- Use for long messages

### Notifications
✅ **DO:**
- Use for important events user should review
- Include action URLs when relevant
- Keep titles under 50 characters
- Write clear, actionable messages

❌ **DON'T:**
- Create notification for every minor action
- Send notifications without context
- Duplicate toast messages as notifications

### When to Use Each

**Toast Only:**
- Form validation errors
- Button click confirmations
- Quick status updates

**Notification Only:**
- Background processing complete
- Payment status changes
- Subscription changes
- Important account updates

**Both:**
- Receipt upload: Toast for immediate feedback, Notification when processing completes
- Payment: Toast for submission, Notification for success/failure

## API Endpoints Reference

### GET /notifications
- **Query params:** skip, limit, unread_only
- **Returns:** NotificationListResponse
- **Auth:** Required

### GET /notifications/unread-count
- **Returns:** { unread_count: number }
- **Auth:** Required

### PUT /notifications/{id}/read
- **Returns:** Updated notification
- **Auth:** Required

### POST /notifications/mark-all-read
- **Returns:** { message, updated_count }
- **Auth:** Required

### DELETE /notifications/{id}
- **Returns:** { message }
- **Auth:** Required

### DELETE /notifications/delete-all
- **Returns:** { message, deleted_count }
- **Auth:** Required

## Testing Checklist

### Toast System
- [ ] Success toast appears and auto-dismisses
- [ ] Error toast shows with correct styling
- [ ] Warning toast displays properly
- [ ] Info toast works
- [ ] Manual dismiss works
- [ ] Multiple toasts stack correctly
- [ ] RTL text displays properly

### Notification Center
- [ ] Bell icon shows unread count
- [ ] Clicking bell opens panel
- [ ] Notifications load correctly
- [ ] Mark as read works
- [ ] Mark all as read works
- [ ] Delete notification works
- [ ] Action URL navigation works
- [ ] Auto-refresh (30s) works
- [ ] Empty state displays
- [ ] Loading state displays

### Integration
- [ ] Backend creates notifications correctly
- [ ] Frontend fetches notifications
- [ ] Real-time updates work
- [ ] Pagination works
- [ ] Filters work (unread only)
- [ ] Mobile responsive

## Migration Notes

After implementing, run:
```bash
# Backend
cd backend
alembic upgrade head

# Frontend
npm install  # If any new dependencies
npm run dev
```

## Support

For issues or questions:
1. Check browser console for errors
2. Verify API endpoints are accessible
3. Check database for notification records
4. Review network tab for failed requests
