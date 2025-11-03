"""
Custom exceptions for Tik-Tax API
All exceptions include Hebrew messages for frontend display
"""

from typing import Any, Optional
from fastapi import HTTPException, status


class TikTaxException(HTTPException):
    """Base exception for all Tik-Tax custom exceptions"""
    
    def __init__(
        self,
        status_code: int,
        message: str,
        hebrew_message: str,
        details: Optional[Any] = None
    ):
        self.hebrew_message = hebrew_message
        self.details = details
        super().__init__(
            status_code=status_code,
            detail={
                "message": message,
                "hebrew_message": hebrew_message,
                "details": details
            }
        )


class AuthenticationError(TikTaxException):
    """Authentication failed - invalid credentials"""
    
    def __init__(
        self,
        message: str = "Authentication failed",
        hebrew_message: str = "אימות נכשל. אנא בדוק את פרטי ההתחברות",
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            hebrew_message=hebrew_message,
            details=details
        )


class AuthorizationError(TikTaxException):
    """User not authorized to perform this action"""
    
    def __init__(
        self,
        message: str = "Not authorized",
        hebrew_message: str = "אין לך הרשאה לבצע פעולה זו",
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            hebrew_message=hebrew_message,
            details=details
        )


class ValidationError(TikTaxException):
    """Input validation failed"""
    
    def __init__(
        self,
        message: str = "Validation failed",
        hebrew_message: str = "נתונים שגויים. אנא בדוק את הפרטים שהזנת",
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message,
            hebrew_message=hebrew_message,
            details=details
        )


class ResourceNotFoundError(TikTaxException):
    """Requested resource not found"""
    
    def __init__(
        self,
        resource: str = "Resource",
        hebrew_message: str = "הפריט המבוקש לא נמצא",
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"{resource} not found",
            hebrew_message=hebrew_message,
            details=details
        )


class DuplicateResourceError(TikTaxException):
    """Resource already exists"""
    
    def __init__(
        self,
        resource: str = "Resource",
        hebrew_message: str = "פריט זה כבר קיים במערכת",
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=f"{resource} already exists",
            hebrew_message=hebrew_message,
            details=details
        )


class ProcessingError(TikTaxException):
    """Error during receipt processing (OCR, storage, etc.)"""
    
    def __init__(
        self,
        message: str = "Processing failed",
        hebrew_message: str = "אירעה שגיאה בעיבוד. אנא נסה שוב",
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            hebrew_message=hebrew_message,
            details=details
        )


class RateLimitExceeded(TikTaxException):
    """Rate limit exceeded"""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        hebrew_message: str = "ביצעת יותר מדי בקשות. אנא נסה שוב מאוחר יותר",
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            message=message,
            hebrew_message=hebrew_message,
            details=details
        )


class OCRError(TikTaxException):
    """OCR processing failed"""
    
    def __init__(
        self,
        message: str = "OCR processing failed",
        hebrew_message: str = "לא הצלחנו לקרוא את הקבלה. אנא צלם תמונה ברורה יותר",
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message,
            hebrew_message=hebrew_message,
            details=details
        )


class StorageError(TikTaxException):
    """File storage failed"""
    
    def __init__(
        self,
        message: str = "Storage operation failed",
        hebrew_message: str = "שגיאה בשמירת הקובץ. אנא נסה שוב",
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            hebrew_message=hebrew_message,
            details=details
        )


class SubscriptionError(TikTaxException):
    """Subscription-related error"""
    
    def __init__(
        self,
        message: str = "Subscription error",
        hebrew_message: str = "בעיה במנוי שלך. אנא צור קשר עם התמיכה",
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            message=message,
            hebrew_message=hebrew_message,
            details=details
        )


class EmailError(TikTaxException):
    """Email sending failed"""
    
    def __init__(
        self,
        message: str = "Email sending failed",
        hebrew_message: str = "שליחת המייל נכשלה. אנא נסה שוב",
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            hebrew_message=hebrew_message,
            details=details
        )


class SMSError(TikTaxException):
    """SMS sending failed"""
    
    def __init__(
        self,
        message: str = "SMS sending failed",
        hebrew_message: str = "שליחת ה-SMS נכשלה. אנא נסה שוב",
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            hebrew_message=hebrew_message,
            details=details
        )
