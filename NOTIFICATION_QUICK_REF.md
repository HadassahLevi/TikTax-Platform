# Notification System - Quick Reference

## 🚀 Quick Start

### Backend Setup
```bash
# 1. Run migration
cd backend
alembic upgrade head

# 2. Test notifications
python test_notifications_manual.py --email your@email.com
```

### Frontend Setup
```bash
# Already integrated in App.tsx
npm run dev
```

## 📝 Common Use Cases

### 1. Show Toast Message
```typescript
import { useToast } from '@/contexts/ToastContext';

const { showToast } = useToast();

showToast({
  type: 'success',  // success | error | warning | info
  title: 'הצלחה',
  message: 'הפעולה בוצעה בהצלחה'
});
```

### 2. Create Backend Notification
```python
from app.services.notification_service import create_notification

create_notification(
    db=db,
    user_id=user.id,
    type="success",
    title="קבלה אושרה",
    message="הקבלה נשמרה בארכיון",
    action_url="/archive",
    action_label="צפה בארכיון"
)
```

### 3. Add Notification Center to Layout
```typescript
import { NotificationCenter } from '@/components/NotificationCenter';

<header>
  <NotificationCenter />
</header>
```

## 🎨 Notification Types

| Type | Color | Use Case | Icon |
|------|-------|----------|------|
| `success` | Green | Actions completed | ✓ |
| `error` | Red | Failures, errors | ✕ |
| `warning` | Amber | Warnings, attention needed | ⚠ |
| `info` | Blue | Informational | ℹ |

## 🔧 Pre-built Notification Functions

### Receipt Events
```python
create_receipt_approved_notification(db, user_id, vendor_name)
create_receipt_failed_notification(db, user_id, reason)
create_duplicate_receipt_notification(db, user_id, vendor_name)
```

### Payment Events
```python
create_payment_success_notification(db, user_id, plan_name)
create_payment_failed_notification(db, user_id)
```

### Subscription Events
```python
create_limit_warning_notification(db, user_id, percentage)
create_subscription_canceled_notification(db, user_id, end_date)
```

### Other Events
```python
create_export_ready_notification(db, user_id, receipt_count)
create_welcome_notification(db, user_id, user_name)
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notifications` | Get notifications list |
| GET | `/notifications/unread-count` | Get unread count |
| PUT | `/notifications/{id}/read` | Mark as read |
| POST | `/notifications/mark-all-read` | Mark all as read |
| DELETE | `/notifications/{id}` | Delete notification |
| DELETE | `/notifications/delete-all` | Delete all |

## 📊 Database Schema

```sql
notifications (
  id: INT PRIMARY KEY,
  user_id: INT FOREIGN KEY,
  type: VARCHAR(50),
  title: VARCHAR(255),
  message: TEXT,
  action_url: VARCHAR(500),
  action_label: VARCHAR(100),
  is_read: BOOLEAN,
  read_at: TIMESTAMP,
  created_at: TIMESTAMP,
  updated_at: TIMESTAMP
)
```

## 🧪 Testing

### Manual Test
```bash
# Create test notifications
python backend/test_notifications_manual.py

# Or for specific user
python backend/test_notifications_manual.py --email user@example.com
```

### Frontend Testing
1. Open http://localhost:5173
2. Login
3. Click bell icon (top right)
4. Test features:
   - View notifications
   - Mark as read
   - Delete notifications
   - Click action links

### Toast Testing
```typescript
// Add to any component for testing
showToast({ type: 'success', title: 'Test', message: 'Toast works!' });
```

## 💡 Best Practices

### Toast Messages
- ✅ Immediate user feedback
- ✅ Auto-dismiss (5 seconds)
- ✅ Short messages
- ❌ Don't use for critical info

### Notifications
- ✅ Important events
- ✅ Include action URLs
- ✅ Clear titles & messages
- ❌ Don't spam users

### When to Use Both
- **Toast**: Immediate feedback (e.g., "Uploading...")
- **Notification**: Background result (e.g., "Receipt processed")

## 🐛 Troubleshooting

### Toast not showing?
- Check `ToastProvider` wraps app
- Check import path
- Check browser console

### Notifications not loading?
- Check backend is running
- Check user is authenticated
- Check API endpoint `/notifications`
- Check database has notifications table

### Bell icon not showing count?
- Check API `/notifications/unread-count`
- Check auth token is valid
- Check user has notifications

## 📁 File Structure

```
backend/
├── app/
│   ├── models/notification.py          ✨ NEW
│   ├── schemas/notification.py         ✨ NEW
│   ├── services/notification_service.py ✨ NEW
│   └── api/v1/endpoints/notifications.py ✨ NEW
├── alembic_create_notifications.py     ✨ NEW
└── test_notifications_manual.py        ✨ NEW

frontend/
├── src/
│   ├── contexts/ToastContext.tsx        ✨ NEW
│   ├── components/NotificationCenter.tsx ✨ NEW
│   ├── services/notification.service.ts  ✨ NEW
│   └── App.tsx                          ✏️ UPDATED
```

## 🎯 Integration Examples

### Receipt Service
```python
# In receipt_service.py
from app.services.notification_service import create_receipt_approved_notification

def approve_receipt(db, receipt_id, user_id):
    receipt = db.query(Receipt).get(receipt_id)
    receipt.status = ReceiptStatus.APPROVED
    db.commit()
    
    # Create notification
    create_receipt_approved_notification(db, user_id, receipt.vendor_name)
```

### Stripe Webhook
```python
# In stripe_service.py
from app.services.notification_service import create_payment_success_notification

def handle_payment_success(event):
    user = get_user_from_event(event)
    plan = get_plan_from_event(event)
    
    # Create notification
    create_payment_success_notification(db, user.id, plan.name)
```

## 📞 Support

For detailed documentation, see:
- `NOTIFICATION_SYSTEM_GUIDE.md` - Full usage guide
- Backend code comments
- Frontend component comments
