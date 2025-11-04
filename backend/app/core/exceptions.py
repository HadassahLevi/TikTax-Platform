"""
Custom exceptions for Tik-Tax API
Production-grade exception hierarchy with Hebrew messages for frontend display

All exceptions inherit from TikTaxException which provides:
- Bilingual error messages (English + Hebrew)
- HTTP status codes
- Optional detailed context
- Structured error responses
"""

from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class TikTaxException(HTTPException):
    """
    Base exception for all Tik-Tax custom exceptions
    
    Provides structured error responses with:
    - English message for logging/debugging
    - Hebrew message for user-facing display
    - HTTP status code
    - Optional details dictionary
    
    Attributes:
        message: English error message
        message_he: Hebrew error message
        status_code: HTTP status code
        details: Additional error context
    """
    
    def __init__(
        self,
        message: str,
        message_he: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.message_he = message_he
        self.status_code = status_code
        self.details = details or {}
        
        super().__init__(
            status_code=status_code,
            detail={
                "error": message,
                "error_he": message_he,
                "details": self.details
            }
        )


class AuthenticationError(TikTaxException):
    """Authentication failed - invalid credentials or expired tokens"""
    
    def __init__(
        self,
        message: str = "Authentication failed",
        message_he: str = "אימות נכשל"
    ):
        super().__init__(
            message=message,
            message_he=message_he,
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class AuthorizationError(TikTaxException):
    """Authorization/permission denied"""
    
    def __init__(
        self,
        message: str = "Access denied",
        message_he: str = "אין הרשאה לגישה"
    ):
        super().__init__(
            message=message,
            message_he=message_he,
            status_code=status.HTTP_403_FORBIDDEN
        )


class ResourceNotFoundError(TikTaxException):
    """Requested resource not found"""
    
    def __init__(
        self,
        resource: str = "Resource",
        resource_he: str = "פריט"
    ):
        super().__init__(
            message=f"{resource} not found",
            message_he=f"{resource_he} לא נמצא",
            status_code=status.HTTP_404_NOT_FOUND
        )


class ValidationError(TikTaxException):
    """Data validation errors"""
    
    def __init__(
        self,
        message: str,
        message_he: str,
        details: Dict[str, Any]
    ):
        super().__init__(
            message=message,
            message_he=message_he,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )


class DuplicateResourceError(TikTaxException):
    """Resource already exists"""
    
    def __init__(
        self,
        resource: str = "Resource",
        resource_he: str = "פריט"
    ):
        super().__init__(
            message=f"{resource} already exists",
            message_he=f"{resource_he} כבר קיים",
            status_code=status.HTTP_409_CONFLICT
        )


class ExternalServiceError(TikTaxException):
    """External service (OCR, S3, payment gateway, etc.) errors"""
    
    def __init__(
        self,
        service: str,
        message: str,
        message_he: str = "שגיאת שירות חיצוני"
    ):
        super().__init__(
            message=f"{service} error: {message}",
            message_he=f"שגיאת {service}: {message_he}",
            status_code=status.HTTP_502_BAD_GATEWAY,
            details={"service": service}
        )


class RateLimitError(TikTaxException):
    """Rate limit exceeded"""
    
    def __init__(self):
        super().__init__(
            message="Too many requests",
            message_he="יותר מדי בקשות, נסה שוב מאוחר יותר",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )


class SubscriptionLimitError(TikTaxException):
    """Subscription limit reached"""
    
    def __init__(self, limit: int):
        super().__init__(
            message=f"Monthly receipt limit ({limit}) reached",
            message_he=f"הגעת למגבלת הקבלות החודשית ({limit})",
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            details={"limit": limit}
        )


class FileUploadError(TikTaxException):
    """File upload related errors"""
    
    def __init__(
        self,
        reason: str,
        reason_he: str = "שגיאה בהעלאת קובץ"
    ):
        super().__init__(
            message=f"File upload failed: {reason}",
            message_he=f"העלאת קובץ נכשלה: {reason_he}",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"reason": reason}
        )


class OCRProcessingError(TikTaxException):
    """OCR processing errors"""
    
    def __init__(
        self,
        reason: str = "Could not extract data from receipt",
        reason_he: str = "לא ניתן לחלץ מידע מהקבלה"
    ):
        super().__init__(
            message=reason,
            message_he=reason_he,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details={"stage": "ocr"}
        )


class DatabaseError(TikTaxException):
    """Database operation errors"""
    
    def __init__(
        self,
        operation: str,
        message: str
    ):
        super().__init__(
            message=f"Database {operation} failed: {message}",
            message_he=f"פעולת מסד נתונים נכשלה: {operation}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details={"operation": operation}
        )


class StorageError(TikTaxException):
    """File storage (S3) errors"""
    
    def __init__(
        self,
        message: str = "Storage operation failed",
        message_he: str = "שגיאה בשמירת הקובץ"
    ):
        super().__init__(
            message=message,
            message_he=message_he,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details={"service": "s3"}
        )


class EmailError(TikTaxException):
    """Email sending errors"""
    
    def __init__(
        self,
        message: str = "Email sending failed",
        message_he: str = "שליחת המייל נכשלה"
    ):
        super().__init__(
            message=message,
            message_he=message_he,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details={"service": "sendgrid"}
        )


class SMSError(TikTaxException):
    """SMS sending errors"""
    
    def __init__(
        self,
        message: str = "SMS sending failed",
        message_he: str = "שליחת ה-SMS נכשלה"
    ):
        super().__init__(
            message=message,
            message_he=message_he,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details={"service": "twilio"}
        )


# Legacy exception classes for backward compatibility
# These map to the new exception hierarchy

class ProcessingError(TikTaxException):
    """Legacy: General processing error"""
    
    def __init__(
        self,
        message: str = "Processing failed",
        hebrew_message: str = "אירעה שגיאה בעיבוד",
        details: Optional[Any] = None
    ):
        super().__init__(
            message=message,
            message_he=hebrew_message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details or {}
        )


class RateLimitExceeded(RateLimitError):
    """Legacy: Rate limit exceeded (maps to RateLimitError)"""
    pass


class OCRError(OCRProcessingError):
    """Legacy: OCR error (maps to OCRProcessingError)"""
    pass


class SubscriptionError(SubscriptionLimitError):
    """Legacy: Subscription error (maps to SubscriptionLimitError)"""
    
    def __init__(
        self,
        message: str = "Subscription error",
        hebrew_message: str = "בעיה במנוי שלך",
        details: Optional[Any] = None
    ):
        # Default limit if not specified
        limit = details.get("limit", 0) if details else 0
        super().__init__(limit=limit)

