"""
Manual Test Script for Notification System
Run this script to create test notifications for a user
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.services.notification_service import (
    create_receipt_approved_notification,
    create_receipt_failed_notification,
    create_limit_warning_notification,
    create_payment_success_notification,
    create_payment_failed_notification,
    create_subscription_canceled_notification,
    create_duplicate_receipt_notification,
    create_export_ready_notification,
    create_welcome_notification
)
from datetime import datetime, timedelta


def create_test_notifications(user_email: str = "test@tiktax.co.il"):
    """Create various test notifications for a user"""
    
    db: Session = SessionLocal()
    
    try:
        # Find user
        user = db.query(User).filter(User.email == user_email).first()
        
        if not user:
            print(f"❌ User not found: {user_email}")
            print("Please provide a valid user email or create a user first")
            return
        
        print(f"✅ Found user: {user.full_name} ({user.email})")
        print(f"Creating test notifications...\n")
        
        # 1. Success - Receipt Approved
        notif1 = create_receipt_approved_notification(db, user.id, "סופר פארם")
        print(f"✓ Created: {notif1.title}")
        
        # 2. Error - Receipt Failed
        notif2 = create_receipt_failed_notification(db, user.id, "הקובץ פגום או לא ברור")
        print(f"✓ Created: {notif2.title}")
        
        # 3. Warning - Limit Warning
        notif3 = create_limit_warning_notification(db, user.id, 85)
        print(f"✓ Created: {notif3.title}")
        
        # 4. Success - Payment Success
        notif4 = create_payment_success_notification(db, user.id, "Pro")
        print(f"✓ Created: {notif4.title}")
        
        # 5. Error - Payment Failed
        notif5 = create_payment_failed_notification(db, user.id)
        print(f"✓ Created: {notif5.title}")
        
        # 6. Info - Subscription Canceled
        end_date = datetime.utcnow() + timedelta(days=30)
        notif6 = create_subscription_canceled_notification(db, user.id, end_date)
        print(f"✓ Created: {notif6.title}")
        
        # 7. Warning - Duplicate Receipt
        notif7 = create_duplicate_receipt_notification(db, user.id, "רמי לוי")
        print(f"✓ Created: {notif7.title}")
        
        # 8. Success - Export Ready
        notif8 = create_export_ready_notification(db, user.id, 45)
        print(f"✓ Created: {notif8.title}")
        
        # 9. Info - Welcome
        notif9 = create_welcome_notification(db, user.id, user.full_name)
        print(f"✓ Created: {notif9.title}")
        
        print(f"\n✅ Successfully created 9 test notifications for {user.full_name}")
        print(f"\nTest the system:")
        print(f"1. Open frontend: http://localhost:5173")
        print(f"2. Login as: {user.email}")
        print(f"3. Click the bell icon to see notifications")
        print(f"4. Test marking as read, deleting, and clicking action links")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create test notifications")
    parser.add_argument(
        "--email",
        type=str,
        default="test@tiktax.co.il",
        help="User email to create notifications for"
    )
    
    args = parser.parse_args()
    create_test_notifications(args.email)
