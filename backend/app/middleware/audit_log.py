"""
Audit Log Middleware
Logs all API requests for compliance and debugging
Records: timestamp, user, method, path, status, duration, IP
"""

from fastapi import Request
from datetime import datetime
import logging
import json
from typing import Optional

logger = logging.getLogger(__name__)

# Sensitive paths that should not log request/response bodies
SENSITIVE_PATHS = [
    '/api/v1/auth/login',
    '/api/v1/auth/signup',
    '/api/v1/auth/refresh',
    '/api/v1/auth/password'
]

# Paths to exclude from audit logging (health checks, etc.)
EXCLUDE_PATHS = [
    '/health',
    '/api/v1/docs',
    '/api/v1/redoc',
    '/api/v1/openapi.json'
]


async def audit_log_middleware(request: Request, call_next):
    """
    Log all API requests for audit trail
    
    Features:
    - Timestamp tracking
    - User identification (if authenticated)
    - Request method and path
    - Query parameters (non-sensitive)
    - Response status code
    - Request duration (performance monitoring)
    - IP address tracking
    
    Security:
    - Never logs passwords, tokens, or sensitive data
    - Redacts sensitive paths
    - Respects privacy requirements
    
    Args:
        request: FastAPI Request object
        call_next: Next middleware in chain
        
    Returns:
        Response from next middleware
    """
    # Skip audit logging for excluded paths
    if request.url.path in EXCLUDE_PATHS:
        return await call_next(request)
    
    # Record start time
    start_time = datetime.utcnow()
    
    # Extract user info if authenticated
    user_id: Optional[int] = None
    if hasattr(request.state, 'user') and request.state.user:
        user_id = request.state.user.id
    
    # Process request
    try:
        response = await call_next(request)
    except Exception as e:
        # Log error and re-raise
        duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        audit_entry = {
            'timestamp': start_time.isoformat(),
            'user_id': user_id,
            'method': request.method,
            'path': request.url.path,
            'query_params': dict(request.query_params) if request.url.path not in SENSITIVE_PATHS else '[REDACTED]',
            'status_code': 500,
            'duration_ms': round(duration_ms, 2),
            'ip_address': request.client.host if request.client else 'unknown',
            'error': str(e),
            'user_agent': request.headers.get('user-agent', 'unknown')
        }
        
        logger.error(f"API Error: {json.dumps(audit_entry, ensure_ascii=False)}")
        raise
    
    # Calculate duration
    duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
    
    # Determine if path is sensitive
    is_sensitive = request.url.path in SENSITIVE_PATHS
    
    # Build audit entry
    audit_entry = {
        'timestamp': start_time.isoformat(),
        'user_id': user_id,
        'method': request.method,
        'path': request.url.path,
        'query_params': '[REDACTED]' if is_sensitive else dict(request.query_params),
        'status_code': response.status_code,
        'duration_ms': round(duration_ms, 2),
        'ip_address': request.client.host if request.client else 'unknown',
        'user_agent': request.headers.get('user-agent', 'unknown')
    }
    
    # Log based on status code
    if response.status_code >= 500:
        logger.error(f"API Server Error: {json.dumps(audit_entry, ensure_ascii=False)}")
    elif response.status_code >= 400:
        logger.warning(f"API Client Error: {json.dumps(audit_entry, ensure_ascii=False)}")
    else:
        # Only log successful requests at DEBUG level to reduce noise
        # Critical operations (POST, PUT, DELETE) logged at INFO
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            logger.info(f"API Request: {json.dumps(audit_entry, ensure_ascii=False)}")
        else:
            logger.debug(f"API Request: {json.dumps(audit_entry, ensure_ascii=False)}")
    
    # Add performance warning for slow requests (>1 second)
    if duration_ms > 1000:
        logger.warning(
            f"Slow API Request: {request.method} {request.url.path} took {duration_ms}ms "
            f"(user: {user_id})"
        )
    
    return response


def log_user_action(user_id: int, action: str, details: dict = None):
    """
    Log specific user action for audit trail
    
    Use this for critical business operations:
    - Receipt approval
    - Export generation
    - Account changes
    - Subscription changes
    
    Args:
        user_id: User who performed action
        action: Action type (e.g., 'receipt_approved', 'export_generated')
        details: Additional context (serializable dict)
    """
    audit_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'user_id': user_id,
        'action': action,
        'details': details or {}
    }
    
    logger.info(f"User Action: {json.dumps(audit_entry, ensure_ascii=False)}")
