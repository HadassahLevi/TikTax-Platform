"""
Global Error Handler Middleware for Tik-Tax API
Catches all exceptions and returns consistent Hebrew error messages
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from ..core.exceptions import (
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    ResourceNotFoundError,
    DuplicateResourceError,
    ProcessingError
)
import logging

logger = logging.getLogger(__name__)


async def error_handler_middleware(request: Request, call_next):
    """
    Global error handler with Hebrew error messages.
    
    Catches all exceptions during request processing and returns
    consistent JSON responses with Hebrew error messages for the frontend.
    
    Exception Hierarchy:
    - AuthenticationError (401): Invalid credentials, expired tokens
    - AuthorizationError (403): Insufficient permissions
    - ResourceNotFoundError (404): Resource doesn't exist
    - DuplicateResourceError (409): Resource already exists
    - ValidationError (422): Invalid input data
    - ProcessingError (422): Business logic errors
    - Exception (500): Unexpected server errors
    
    Args:
        request: FastAPI request object
        call_next: Next middleware in chain
        
    Returns:
        JSONResponse: Formatted error response with Hebrew message
    """
    try:
        # Process request through the chain
        return await call_next(request)
    
    except AuthenticationError as e:
        logger.warning(f"Authentication error: {e.hebrew_message} | Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": e.hebrew_message}
        )
    
    except AuthorizationError as e:
        logger.warning(f"Authorization error: {e.hebrew_message} | Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": e.hebrew_message}
        )
    
    except ResourceNotFoundError as e:
        logger.info(f"Resource not found: {e.hebrew_message} | Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": e.hebrew_message}
        )
    
    except DuplicateResourceError as e:
        logger.info(f"Duplicate resource: {e.hebrew_message} | Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": e.hebrew_message}
        )
    
    except ProcessingError as e:
        logger.error(f"Processing error: {e.hebrew_message} | Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": e.hebrew_message}
        )
    
    except ValidationError as e:
        logger.warning(f"Validation error: {e.hebrew_message} | Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": e.hebrew_message}
        )
    
    except Exception as e:
        # Log full error with traceback for debugging
        logger.error(
            f"Unhandled error: {str(e)} | Path: {request.url.path} | "
            f"Method: {request.method}",
            exc_info=True  # Include full traceback
        )
        
        # Return generic error message to client (don't expose internals)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "שגיאה פנימית בשרת. אנא נסה שוב מאוחר יותר."}
        )
