"""
Notification Pydantic Schemas
Request/response models for notification API
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class NotificationBase(BaseModel):
    """Base notification schema with common fields"""
    type: str = Field(..., description="Notification type: success, info, warning, error")
    title: str = Field(..., max_length=255, description="Notification title (Hebrew)")
    message: str = Field(..., description="Notification message (Hebrew)")
    action_url: Optional[str] = Field(None, max_length=500, description="Optional URL to navigate on click")
    action_label: Optional[str] = Field(None, max_length=100, description="Optional action button label (Hebrew)")


class NotificationCreate(NotificationBase):
    """Schema for creating a notification (internal use)"""
    user_id: int = Field(..., description="User ID to send notification to")


class NotificationUpdate(BaseModel):
    """Schema for updating notification status"""
    is_read: Optional[bool] = Field(None, description="Mark as read/unread")


class NotificationResponse(NotificationBase):
    """Schema for notification response"""
    id: int
    user_id: int
    is_read: bool
    read_at: Optional[datetime] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class NotificationListResponse(BaseModel):
    """Schema for paginated notification list"""
    notifications: list[NotificationResponse] = Field(..., description="List of notifications")
    total: int = Field(..., description="Total count of all notifications")
    unread_count: int = Field(..., description="Count of unread notifications")
    
    model_config = ConfigDict(from_attributes=True)


class MarkAllReadResponse(BaseModel):
    """Schema for mark all as read response"""
    message: str = Field(..., description="Success message")
    updated_count: int = Field(..., description="Number of notifications marked as read")
