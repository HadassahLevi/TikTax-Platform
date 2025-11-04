"""
Global Error Handler Middleware for Tik-Tax API
Production-grade exception handling with:
- Structured error responses
- Request context tracking
- Sensitive data filtering
- Comprehensive logging
- Hebrew error messages
"""

import logging
import uuid
from typing import Any, Dict
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, OperationalError, DatabaseError as SQLAlchemyDatabaseError

from app.core.exceptions import TikTaxException
from app.core.monitoring import capture_exception

logger = logging.getLogger(__name__)


def get_request_context(request: Request) -> Dict[str, Any]:
    """
    Extract request context for logging
    
    Args:
        request: FastAPI request object
        
    Returns:
        Dictionary with request context
    """
    return {
        "request_id": getattr(request.state, "request_id", str(uuid.uuid4())),
        "user_id": getattr(request.state, "user_id", None),
        "ip_address": request.client.host if request.client else None,
        "method": request.method,
        "path": request.url.path,
        "user_agent": request.headers.get("user-agent")
    }


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle all exceptions globally with structured responses
    
    Processes exceptions in order of specificity:
    1. TikTaxException - Our custom exceptions
    2. RequestValidationError - FastAPI/Pydantic validation
    3. IntegrityError - Database constraint violations
    4. OperationalError - Database connection issues
    5. Exception - Catch-all for unexpected errors
    
    Args:
        request: FastAPI request object
        exc: Exception that was raised
        
    Returns:
        JSONResponse with error details
    """
    
    # Get request context for logging
    context = get_request_context(request)
    
    # Handle TikTaxException (our custom exceptions)
    if isinstance(exc, TikTaxException):
        logger.warning(
            f"TikTax error: {exc.message}",
            extra={
                **context,
                "exception_type": exc.__class__.__name__,
                "status_code": exc.status_code
            }
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.message,
                "error_he": exc.message_he,
                "details": exc.details
            }
        )
    
    # Handle FastAPI/Pydantic validation errors
    if isinstance(exc, RequestValidationError):
        validation_errors = exc.errors()
        
        logger.warning(
            f"Validation error: {len(validation_errors)} field(s) failed",
            extra={
                **context,
                "validation_errors": validation_errors
            }
        )
        
        # Extract field names for user-friendly message
        field_names = []
        for error in validation_errors:
            field = error.get("loc", [])[-1] if error.get("loc") else "unknown"
            field_names.append(str(field))
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "Validation error",
                "error_he": "שגיאת אימות נתונים",
                "details": {
                    "fields": field_names,
                    "errors": validation_errors
                }
            }
        )
    
    # Handle database integrity errors (unique constraints, foreign keys, etc.)
    if isinstance(exc, IntegrityError):
        logger.error(
            f"Database integrity error: {str(exc.orig) if hasattr(exc, 'orig') else str(exc)}",
            extra=context
        )
        
        # Try to provide user-friendly message
        error_message = str(exc.orig) if hasattr(exc, "orig") else str(exc)
        
        if "unique constraint" in error_message.lower():
            message = "Resource already exists"
            message_he = "הפריט כבר קיים במערכת"
        elif "foreign key" in error_message.lower():
            message = "Related resource not found"
            message_he = "פריט קשור לא נמצא"
        else:
            message = "Database constraint violation"
            message_he = "שגיאת אילוץ במסד נתונים"
        
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": message,
                "error_he": message_he,
                "details": {}
            }
        )
    
    # Handle database operational errors (connection issues, timeouts, etc.)
    if isinstance(exc, (OperationalError, SQLAlchemyDatabaseError)):
        logger.error(
            f"Database operational error: {str(exc.orig) if hasattr(exc, 'orig') else str(exc)}",
            extra=context,
            exc_info=True
        )
        
        # Send to Sentry for monitoring
        capture_exception(exc, context)
        
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": "Database unavailable",
                "error_he": "מסד הנתונים לא זמין כרגע. אנא נסה שוב מאוחר יותר",
                "details": {}
            }
        )
    
    # Handle all other unexpected exceptions
    logger.error(
        f"Unhandled exception: {exc.__class__.__name__}: {str(exc)}",
        extra=context,
        exc_info=True
    )
    
    # Send to Sentry for monitoring
    capture_exception(exc, context)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "error_he": "אירעה שגיאה בשרת. אנא נסה שוב מאוחר יותר",
            "details": {}
        }
    )


async def tiktax_exception_handler(request: Request, exc: TikTaxException) -> JSONResponse:
    """
    Dedicated handler for TikTaxException
    
    This is registered as a FastAPI exception handler for TikTaxException.
    It delegates to the global handler for consistent processing.
    
    Args:
        request: FastAPI request object
        exc: TikTaxException instance
        
    Returns:
        JSONResponse with error details
    """
    return await global_exception_handler(request, exc)

