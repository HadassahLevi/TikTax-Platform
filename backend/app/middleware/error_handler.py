"""
Global Error Handler Middleware
Catches and formats all exceptions
"""

import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to handle all exceptions globally"""
    
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error(f"Unhandled error: {str(exc)}", exc_info=True)
            
            return JSONResponse(
                status_code=500,
                content={
                    "message": "Internal server error",
                    "hebrew_message": "אירעה שגיאה בשרת. אנא נסה שוב מאוחר יותר",
                    "details": None
                }
            )
