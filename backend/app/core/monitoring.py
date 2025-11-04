"""
Sentry Integration and Monitoring for Tik-Tax API
Configures error tracking, performance monitoring, and sensitive data filtering
"""

import logging
from typing import Any, Dict, Optional

try:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    SENTRY_AVAILABLE = True
except ImportError:
    SENTRY_AVAILABLE = False

from app.core.config import settings

logger = logging.getLogger(__name__)


def before_send_handler(event: Dict[str, Any], hint: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Filter sensitive data before sending events to Sentry
    
    Removes or masks sensitive information from:
    - HTTP headers (Authorization, Cookie, API keys)
    - Request data (passwords, tokens)
    - User context (email addresses, phone numbers)
    
    Args:
        event: Sentry event dictionary
        hint: Additional context about the event
        
    Returns:
        Filtered event or None to drop the event
    """
    
    # Filter sensitive HTTP headers
    if "request" in event and "headers" in event["request"]:
        headers = event["request"]["headers"]
        sensitive_headers = [
            "Authorization",
            "Cookie",
            "X-API-Key",
            "X-Auth-Token",
            "X-CSRF-Token"
        ]
        for header in sensitive_headers:
            if header in headers:
                headers[header] = "[FILTERED]"
            # Case-insensitive check
            for key in list(headers.keys()):
                if key.lower() == header.lower():
                    headers[key] = "[FILTERED]"
    
    # Filter sensitive request data
    if "request" in event and "data" in event["request"]:
        data = event["request"]["data"]
        if isinstance(data, dict):
            sensitive_fields = [
                "password",
                "current_password",
                "new_password",
                "password_confirmation",
                "token",
                "refresh_token",
                "access_token",
                "api_key",
                "secret",
                "credit_card",
                "card_number",
                "cvv",
                "ssn"
            ]
            for field in sensitive_fields:
                if field in data:
                    data[field] = "[FILTERED]"
                # Case-insensitive check
                for key in list(data.keys()):
                    if key.lower() in [f.lower() for f in sensitive_fields]:
                        data[key] = "[FILTERED]"
    
    # Filter query parameters
    if "request" in event and "query_string" in event["request"]:
        query_string = event["request"]["query_string"]
        if query_string and ("token" in query_string.lower() or "key" in query_string.lower()):
            event["request"]["query_string"] = "[FILTERED]"
    
    # Filter user email (keep only domain for analytics)
    if "user" in event and "email" in event["user"]:
        email = event["user"]["email"]
        if email and "@" in email:
            domain = email.split("@")[1]
            event["user"]["email"] = f"***@{domain}"
    
    # Filter user phone numbers
    if "user" in event and "phone" in event["user"]:
        event["user"]["phone"] = "[FILTERED]"
    
    # Filter tags with sensitive data
    if "tags" in event:
        for key in list(event["tags"].keys()):
            if "password" in key.lower() or "token" in key.lower() or "secret" in key.lower():
                event["tags"][key] = "[FILTERED]"
    
    # Filter extra context
    if "extra" in event:
        for key in list(event["extra"].keys()):
            if "password" in key.lower() or "token" in key.lower() or "secret" in key.lower():
                event["extra"][key] = "[FILTERED]"
    
    return event


def before_breadcrumb_handler(crumb: Dict[str, Any], hint: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Filter sensitive data from breadcrumbs
    
    Breadcrumbs are events leading up to an error. We filter:
    - SQL queries with sensitive data
    - HTTP requests with authentication
    - Console logs with passwords/tokens
    
    Args:
        crumb: Breadcrumb dictionary
        hint: Additional context
        
    Returns:
        Filtered breadcrumb or None to drop it
    """
    
    # Filter SQL queries (don't log full queries with potentially sensitive data)
    if crumb.get("category") == "query":
        # Only log the table name, not the full query
        if "message" in crumb:
            message = crumb["message"]
            if "INSERT" in message or "UPDATE" in message:
                # These might contain sensitive data
                crumb["message"] = "[SQL QUERY - FILTERED FOR SECURITY]"
            elif len(message) > 200:
                # Truncate very long queries
                crumb["message"] = message[:200] + "... [TRUNCATED]"
    
    # Filter HTTP breadcrumbs with authentication
    if crumb.get("category") == "http":
        if "data" in crumb:
            # Remove request/response bodies
            crumb["data"] = {
                "method": crumb["data"].get("method"),
                "url": crumb["data"].get("url"),
                "status_code": crumb["data"].get("status_code")
            }
    
    # Filter console logs
    if crumb.get("category") == "console":
        message = crumb.get("message", "").lower()
        if any(word in message for word in ["password", "token", "secret", "key"]):
            return None  # Drop this breadcrumb entirely
    
    return crumb


def init_sentry():
    """
    Initialize Sentry for error tracking and performance monitoring
    
    Configures:
    - DSN from environment variables
    - Environment tagging (development/staging/production)
    - Performance monitoring with sampling
    - FastAPI and SQLAlchemy integrations
    - Sensitive data filtering
    - Logging integration
    """
    
    if not SENTRY_AVAILABLE:
        logger.warning("Sentry SDK not installed. Error tracking disabled.")
        return
    
    if not settings.SENTRY_DSN:
        logger.info("Sentry DSN not configured. Error tracking disabled.")
        return
    
    try:
        # Configure logging integration
        sentry_logging = LoggingIntegration(
            level=logging.INFO,        # Capture info and above as breadcrumbs
            event_level=logging.ERROR  # Send errors as events
        )
        
        # Initialize Sentry
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.ENVIRONMENT,
            
            # Performance monitoring
            traces_sample_rate=get_traces_sample_rate(settings.ENVIRONMENT),
            
            # Integrations
            integrations=[
                FastApiIntegration(),
                SqlalchemyIntegration(),
                sentry_logging
            ],
            
            # Data filtering
            before_send=before_send_handler,
            before_breadcrumb=before_breadcrumb_handler,
            
            # Release tracking (optional)
            release=f"tiktax-api@{settings.VERSION}",
            
            # Additional options
            attach_stacktrace=True,
            send_default_pii=False,  # Don't send personally identifiable information
            
            # Request body size limit
            max_request_body_size="medium",  # small/medium/large/always
            
            # Sampling for breadcrumbs
            max_breadcrumbs=50,
        )
        
        logger.info(
            f"Sentry initialized successfully",
            extra={
                "environment": settings.ENVIRONMENT,
                "traces_sample_rate": get_traces_sample_rate(settings.ENVIRONMENT),
                "release": f"tiktax-api@{settings.VERSION}"
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to initialize Sentry: {e}", exc_info=True)


def get_traces_sample_rate(environment: str) -> float:
    """
    Get appropriate trace sample rate based on environment
    
    Args:
        environment: Current environment (development/staging/production)
        
    Returns:
        Sample rate between 0.0 and 1.0
    """
    if environment == "production":
        return 0.1  # 10% of transactions in production
    elif environment == "staging":
        return 0.5  # 50% in staging
    else:
        return 1.0  # 100% in development


def capture_exception(exception: Exception, context: Optional[Dict[str, Any]] = None):
    """
    Manually capture an exception and send to Sentry
    
    Args:
        exception: Exception to capture
        context: Additional context to include
    """
    if not SENTRY_AVAILABLE or not settings.SENTRY_DSN:
        return
    
    try:
        with sentry_sdk.push_scope() as scope:
            if context:
                for key, value in context.items():
                    scope.set_context(key, value)
            
            sentry_sdk.capture_exception(exception)
    except Exception as e:
        logger.error(f"Failed to capture exception in Sentry: {e}")


def capture_message(message: str, level: str = "info", context: Optional[Dict[str, Any]] = None):
    """
    Manually capture a message and send to Sentry
    
    Args:
        message: Message to capture
        level: Severity level (debug/info/warning/error/fatal)
        context: Additional context to include
    """
    if not SENTRY_AVAILABLE or not settings.SENTRY_DSN:
        return
    
    try:
        with sentry_sdk.push_scope() as scope:
            if context:
                for key, value in context.items():
                    scope.set_context(key, value)
            
            sentry_sdk.capture_message(message, level=level)
    except Exception as e:
        logger.error(f"Failed to capture message in Sentry: {e}")


def set_user_context(user_id: int, email: Optional[str] = None):
    """
    Set user context for Sentry events
    
    Args:
        user_id: User ID
        email: User email (will be partially filtered)
    """
    if not SENTRY_AVAILABLE or not settings.SENTRY_DSN:
        return
    
    try:
        sentry_sdk.set_user({
            "id": user_id,
            "email": email  # Will be filtered by before_send_handler
        })
    except Exception as e:
        logger.error(f"Failed to set user context in Sentry: {e}")


def clear_user_context():
    """Clear user context (e.g., on logout)"""
    if not SENTRY_AVAILABLE or not settings.SENTRY_DSN:
        return
    
    try:
        sentry_sdk.set_user(None)
    except Exception as e:
        logger.error(f"Failed to clear user context in Sentry: {e}")
