"""
Notification Service
Helper functions for creating and managing notifications
"""

from sqlalchemy.orm import Session
from app.models.notification import Notification
from datetime import datetime
from typing import Optional


def create_notification(
    db: Session,
    user_id: int,
    type: str,
    title: str,
    message: str,
    action_url: Optional[str] = None,
    action_label: Optional[str] = None
) -> Notification:
    """
    Create a new notification for a user
    
    Args:
        db: Database session
        user_id: Target user ID
        type: Notification type (success, info, warning, error)
        title: Notification title (Hebrew)
        message: Notification message (Hebrew)
        action_url: Optional URL to navigate on click
        action_label: Optional action button label
    
    Returns:
        Created notification object
    """
    notification = Notification(
        user_id=user_id,
        type=type,
        title=title,
        message=message,
        action_url=action_url,
        action_label=action_label
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


# ==========================
# PRE-DEFINED NOTIFICATIONS
# ==========================

def create_receipt_approved_notification(db: Session, user_id: int, vendor_name: str) -> Notification:
    """
    Create notification when receipt is approved and archived
    
    Args:
        db: Database session
        user_id: User ID
        vendor_name: Vendor name from receipt
    
    Returns:
        Created notification
    """
    return create_notification(
        db=db,
        user_id=user_id,
        type="success",
        title="קבלה אושרה בהצלחה",
        message=f'הקבלה מ-{vendor_name} נשמרה בארכיון',
        action_url="/archive",
        action_label="צפה בארכיון"
    )


def create_receipt_failed_notification(db: Session, user_id: int, reason: str) -> Notification:
    """
    Create notification when receipt processing fails
    
    Args:
        db: Database session
        user_id: User ID
        reason: Failure reason
    
    Returns:
        Created notification
    """
    return create_notification(
        db=db,
        user_id=user_id,
        type="error",
        title="עיבוד הקבלה נכשל",
        message=f'לא הצלחנו לעבד את הקבלה: {reason}',
        action_url="/upload",
        action_label="נסה שוב"
    )


def create_limit_warning_notification(db: Session, user_id: int, usage_percentage: int) -> Notification:
    """
    Create notification when user approaches monthly receipt limit
    
    Args:
        db: Database session
        user_id: User ID
        usage_percentage: Percentage of limit used (e.g., 80)
    
    Returns:
        Created notification
    """
    return create_notification(
        db=db,
        user_id=user_id,
        type="warning",
        title="מתקרבים למגבלת החבילה",
        message=f'השתמשת ב-{usage_percentage}% ממכסת הקבלות החודשית',
        action_url="/subscription",
        action_label="שדרג חבילה"
    )


def create_payment_success_notification(db: Session, user_id: int, plan_name: str) -> Notification:
    """
    Create notification when payment is successful
    
    Args:
        db: Database session
        user_id: User ID
        plan_name: Subscription plan name
    
    Returns:
        Created notification
    """
    return create_notification(
        db=db,
        user_id=user_id,
        type="success",
        title="התשלום בוצע בהצלחה",
        message=f'חבילת {plan_name} שלך פעילה',
        action_url="/subscription",
        action_label="נהל מנוי"
    )


def create_payment_failed_notification(db: Session, user_id: int) -> Notification:
    """
    Create notification when payment fails
    
    Args:
        db: Database session
        user_id: User ID
    
    Returns:
        Created notification
    """
    return create_notification(
        db=db,
        user_id=user_id,
        type="error",
        title="התשלום נכשל",
        message="לא הצלחנו לחייב את כרטיס האשראי שלך",
        action_url="/subscription/billing-portal",
        action_label="עדכן פרטי תשלום"
    )


def create_subscription_canceled_notification(db: Session, user_id: int, end_date: datetime) -> Notification:
    """
    Create notification when subscription is canceled
    
    Args:
        db: Database session
        user_id: User ID
        end_date: Subscription end date
    
    Returns:
        Created notification
    """
    return create_notification(
        db=db,
        user_id=user_id,
        type="info",
        title="המנוי בוטל",
        message=f'המנוי שלך יסתיים ב-{end_date.strftime("%d/%m/%Y")}',
        action_url="/subscription",
        action_label="שחזר מנוי"
    )


def create_duplicate_receipt_notification(db: Session, user_id: int, vendor_name: str) -> Notification:
    """
    Create notification when duplicate receipt is detected
    
    Args:
        db: Database session
        user_id: User ID
        vendor_name: Vendor name from receipt
    
    Returns:
        Created notification
    """
    return create_notification(
        db=db,
        user_id=user_id,
        type="warning",
        title="קבלה כפולה זוהתה",
        message=f'הקבלה מ-{vendor_name} כבר קיימת במערכת',
        action_url="/archive",
        action_label="צפה בקבלה הקיימת"
    )


def create_export_ready_notification(db: Session, user_id: int, receipt_count: int) -> Notification:
    """
    Create notification when export is ready for download
    
    Args:
        db: Database session
        user_id: User ID
        receipt_count: Number of receipts in export
    
    Returns:
        Created notification
    """
    return create_notification(
        db=db,
        user_id=user_id,
        type="success",
        title="הייצוא מוכן להורדה",
        message=f'ייצוא של {receipt_count} קבלות הושלם בהצלחה',
        action_url="/export",
        action_label="הורד קובץ"
    )


def create_welcome_notification(db: Session, user_id: int, user_name: str) -> Notification:
    """
    Create welcome notification for new users
    
    Args:
        db: Database session
        user_id: User ID
        user_name: User's full name
    
    Returns:
        Created notification
    """
    return create_notification(
        db=db,
        user_id=user_id,
        type="info",
        title=f"ברוך הבא, {user_name}!",
        message="התחל לסרוק קבלות ולחסוך זמן בניהול החשבוניות שלך",
        action_url="/upload",
        action_label="העלה קבלה ראשונה"
    )
