"""
Notification API Endpoints
Manage user notifications and notification center
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.models.notification import Notification
from app.schemas.notification import (
    NotificationResponse,
    NotificationListResponse,
    MarkAllReadResponse
)
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=NotificationListResponse)
def get_notifications(
    skip: int = Query(0, ge=0, description="Number of notifications to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of notifications to return"),
    unread_only: bool = Query(False, description="Return only unread notifications"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user notifications with pagination
    
    Returns:
    - notifications: List of notifications (newest first)
    - total: Total count of all notifications
    - unread_count: Count of unread notifications
    
    Query Parameters:
    - skip: Number of notifications to skip (for pagination)
    - limit: Maximum number to return (1-100)
    - unread_only: If true, return only unread notifications
    """
    # Build query
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    
    if unread_only:
        query = query.filter(Notification.is_read == False)
    
    # Get total counts
    total = query.count()
    unread_count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).count()
    
    # Get paginated results (newest first)
    notifications = query.order_by(desc(Notification.created_at)).offset(skip).limit(limit).all()
    
    return NotificationListResponse(
        notifications=notifications,
        total=total,
        unread_count=unread_count
    )


@router.get("/unread-count", response_model=dict)
def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get count of unread notifications (for badge display)
    
    Returns:
    - unread_count: Number of unread notifications
    """
    unread_count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).count()
    
    return {"unread_count": unread_count}


@router.put("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark a specific notification as read
    
    Args:
        notification_id: ID of notification to mark as read
    
    Returns:
        Updated notification object
    
    Raises:
        404: Notification not found or doesn't belong to user
    """
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="הודעה לא נמצאה")
    
    # Update read status
    notification.is_read = True
    notification.read_at = datetime.utcnow()
    db.commit()
    db.refresh(notification)
    
    return notification


@router.post("/mark-all-read", response_model=MarkAllReadResponse)
def mark_all_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark all user's notifications as read
    
    Returns:
    - message: Success message
    - updated_count: Number of notifications marked as read
    """
    updated = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).update({
        "is_read": True,
        "read_at": datetime.utcnow()
    }, synchronize_session=False)
    
    db.commit()
    
    return MarkAllReadResponse(
        message="כל ההודעות סומנו כנקראו",
        updated_count=updated
    )


@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a specific notification
    
    Args:
        notification_id: ID of notification to delete
    
    Returns:
        Success message
    
    Raises:
        404: Notification not found or doesn't belong to user
    """
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="הודעה לא נמצאה")
    
    db.delete(notification)
    db.commit()
    
    return {"message": "ההודעה נמחקה בהצלחה"}


@router.delete("/delete-all")
def delete_all_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete all user's notifications
    
    Returns:
    - message: Success message
    - deleted_count: Number of notifications deleted
    """
    deleted = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).delete(synchronize_session=False)
    
    db.commit()
    
    return {
        "message": "כל ההודעות נמחקו בהצלחה",
        "deleted_count": deleted
    }
